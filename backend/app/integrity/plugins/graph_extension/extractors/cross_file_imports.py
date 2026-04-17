from __future__ import annotations

import ast
from pathlib import Path

from ....schema import GraphSnapshot
from ..schema import ExtractedEdge, ExtractionResult
from ._ast_helpers import node_id


def extract(repo_root: Path, graph: GraphSnapshot) -> ExtractionResult:
    """Emit edges for cross-file Python symbol imports.

    Handles three import shapes:

    - ``from .foo.bar import Baz`` → emits ``caller → bar_baz`` (symbol target)
      AND ``caller → baz`` (in case ``Baz`` is itself a module).
    - ``from .foo import bar`` → same dual emit as above (``foo_bar`` + ``bar``).
    - ``from . import bar`` (no module name) → emits ``caller → bar`` only.
    - ``import foo.bar`` / ``import foo`` → emits ``caller → bar`` (leaf as
      module target).

    Walks the entire ``backend/`` tree (not just ``backend/app``) so that
    scripts importing app symbols also contribute incoming edges. Aliases
    (``import X as Y``) preserve the original name ``X`` for resolution.
    """
    failures: list[str] = []
    edges: list[ExtractedEdge] = []
    edge_keys: set[tuple[str, str, str]] = set()

    backend_root = repo_root / "backend"
    if not backend_root.exists():
        return ExtractionResult()

    def add(src_id: str, tgt_id: str, rel_path: str, lineno: int) -> None:
        if src_id == tgt_id or not tgt_id:
            return
        key = (src_id, tgt_id, "imports_from")
        if key in edge_keys:
            return
        edge_keys.add(key)
        edges.append(
            ExtractedEdge(
                source=src_id,
                target=tgt_id,
                relation="imports_from",
                source_file=rel_path,
                source_location=lineno,
                extractor="cross_file_imports",
            )
        )

    for path in sorted(backend_root.rglob("*.py")):
        if any(part.startswith(("__pycache__", ".")) for part in path.parts):
            continue
        try:
            tree = ast.parse(path.read_text())
        except SyntaxError as exc:
            failures.append(f"{path}: {exc}")
            continue

        rel = str(path.relative_to(repo_root))
        caller_stem = path.stem.lower()

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ImportFrom):
                module_leaf = (node.module or "").split(".")[-1].lower()
                for alias in node.names:
                    name = alias.name
                    if name == "*" or not name:
                        continue
                    if module_leaf:
                        add(caller_stem, node_id(module_leaf, name), rel, node.lineno)
                    add(caller_stem, name.lstrip("_").lower(), rel, node.lineno)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    leaf = alias.name.split(".")[-1].lower()
                    add(caller_stem, leaf, rel, node.lineno)

    return ExtractionResult(edges=edges, failures=failures)
