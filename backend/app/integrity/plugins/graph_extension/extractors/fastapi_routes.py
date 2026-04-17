from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path

from ....schema import GraphSnapshot  # type: ignore[no-redef]
from ..schema import ExtractedEdge, ExtractedNode, ExtractionResult
from ._ast_helpers import extract_kw_str, name_of

ROUTE_DECORATORS = {"get", "post", "put", "delete", "patch", "websocket"}


@dataclass
class RouterMap:
    """router-variable-name → declared prefix; composition tracks include_router."""

    prefixes: dict[str, str] = field(default_factory=dict)
    composition: list[tuple[str, str, str]] = field(default_factory=list)

    def resolve(self) -> dict[str, str]:
        """Walk composition transitively to compute final prefix per router."""
        resolved = dict(self.prefixes)
        changed = True
        while changed:
            changed = False
            for parent, child, added in self.composition:
                parent_prefix = resolved.get(parent, "")
                child_prefix = self.prefixes.get(child, "")
                full = parent_prefix + added + child_prefix
                if resolved.get(child) != full:
                    resolved[child] = full
                    changed = True
        return resolved


def extract(repo_root: Path, graph: GraphSnapshot) -> ExtractionResult:
    api_dir = repo_root / "backend" / "app" / "api"
    if not api_dir.exists():
        return ExtractionResult()

    py_files = sorted(api_dir.rglob("*.py"))
    main_py = repo_root / "backend" / "app" / "main.py"
    topology_files = list(py_files)
    if main_py.exists():
        topology_files.append(main_py)

    router_map = RouterMap()
    failures: list[str] = []

    for path in topology_files:
        try:
            tree = ast.parse(path.read_text())
        except SyntaxError as exc:
            failures.append(f"{path}: {exc}")
            continue
        _collect_router_topology(tree, router_map)

    resolved = router_map.resolve()

    nodes: list[ExtractedNode] = []
    edges: list[ExtractedEdge] = []
    seen_route_ids: set[str] = set()

    for path in py_files:
        try:
            tree = ast.parse(path.read_text())
        except SyntaxError:
            continue
        rel = str(path.relative_to(repo_root))
        stem = path.stem
        n, e = _walk_endpoints(tree, rel, stem, resolved, seen_route_ids)
        nodes.extend(n)
        edges.extend(e)

    # Programmatic add_api_route calls
    for path in py_files:
        try:
            tree = ast.parse(path.read_text())
        except SyntaxError:
            continue
        rel = str(path.relative_to(repo_root))
        stem = path.stem
        n, e = _walk_add_api_route(tree, rel, stem, resolved, seen_route_ids)
        nodes.extend(n)
        edges.extend(e)

    return ExtractionResult(nodes=nodes, edges=edges, failures=failures)


def _collect_router_topology(tree: ast.AST, router_map: RouterMap) -> None:
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and isinstance(node.value, ast.Call)
            and name_of(node.value.func) == "APIRouter"
        ):
            router_map.prefixes[node.targets[0].id] = extract_kw_str(node.value, "prefix") or ""

        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "include_router"
            and node.args
        ):
            parent = name_of(node.func.value)
            child_full = name_of(node.args[0])
            if parent and child_full:
                # Normalize dotted names (e.g. "module.router") to the leaf attr
                child = child_full.split(".")[-1]
                added = extract_kw_str(node, "prefix") or ""
                router_map.composition.append((parent, child, added))


def _walk_endpoints(
    tree: ast.AST,
    rel_path: str,
    stem: str,
    resolved: dict[str, str],
    seen_route_ids: set[str],
) -> tuple[list[ExtractedNode], list[ExtractedEdge]]:
    nodes: list[ExtractedNode] = []
    edges: list[ExtractedEdge] = []

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for dec in node.decorator_list:
            for method, route_path in _routes_from_decorator(dec, resolved):
                route_id = f"route::{method}::{route_path}"
                if route_id not in seen_route_ids:
                    seen_route_ids.add(route_id)
                    nodes.append(
                        ExtractedNode(
                            id=route_id,
                            label=f"{method} {route_path}",
                            file_type="route",
                            source_file=rel_path,
                            source_location=node.lineno,
                            extractor="fastapi_routes",
                        )
                    )
                edges.append(
                    ExtractedEdge(
                        source=route_id,
                        target=f"{stem}_{node.name}",
                        relation="routes_to",
                        source_file=rel_path,
                        source_location=node.lineno,
                        extractor="fastapi_routes",
                    )
                )
    return nodes, edges


def _walk_add_api_route(
    tree: ast.AST,
    rel_path: str,
    stem: str,
    resolved: dict[str, str],
    seen_route_ids: set[str],
) -> tuple[list[ExtractedNode], list[ExtractedEdge]]:
    nodes: list[ExtractedNode] = []
    edges: list[ExtractedEdge] = []
    for node in ast.walk(tree):
        if not (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "add_api_route"
            and len(node.args) >= 2
        ):
            continue
        path_arg = node.args[0]
        if not (isinstance(path_arg, ast.Constant) and isinstance(path_arg.value, str)):
            continue
        url = path_arg.value
        handler_name = name_of(node.args[1])
        if not handler_name:
            continue
        for method in _extract_methods_kw(node):
            route_id = f"route::{method.upper()}::{url}"
            if route_id not in seen_route_ids:
                seen_route_ids.add(route_id)
                nodes.append(
                    ExtractedNode(
                        id=route_id,
                        label=f"{method.upper()} {url}",
                        file_type="route",
                        source_file=rel_path,
                        source_location=node.lineno,
                        extractor="fastapi_routes",
                    )
                )
            target = handler_name.split(".")[-1]
            edges.append(
                ExtractedEdge(
                    source=route_id,
                    target=f"{stem}_{target}",
                    relation="routes_to",
                    source_file=rel_path,
                    source_location=node.lineno,
                    extractor="fastapi_routes",
                )
            )
    return nodes, edges


def _routes_from_decorator(
    dec: ast.expr, resolved: dict[str, str]
) -> list[tuple[str, str]]:
    if not isinstance(dec, ast.Call):
        return []
    if not isinstance(dec.func, ast.Attribute):
        return []
    router_name = name_of(dec.func.value)
    if not router_name:
        return []
    method = dec.func.attr
    prefix = resolved.get(router_name, "")
    path = _first_str_arg(dec) or ""

    if method.lower() in ROUTE_DECORATORS:
        return [(method.upper(), prefix + path)]
    if method == "api_route":
        methods = _extract_methods_kw(dec)
        return [(m.upper(), prefix + path) for m in methods]
    return []


def _first_str_arg(call: ast.Call) -> str | None:
    if call.args and isinstance(call.args[0], ast.Constant) and isinstance(call.args[0].value, str):
        return call.args[0].value
    return None


def _extract_methods_kw(call: ast.Call) -> list[str]:
    for kw in call.keywords:
        if kw.arg == "methods" and isinstance(kw.value, ast.List):
            out: list[str] = []
            for elt in kw.value.elts:
                if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                    out.append(elt.value)
            return out
    return []
