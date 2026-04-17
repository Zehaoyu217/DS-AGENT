from __future__ import annotations

import re
from pathlib import Path

from ....schema import GraphSnapshot
from ..schema import ExtractedEdge, ExtractionResult
from ._ast_helpers import node_id

_IMPORT_RE = re.compile(
    r"^\s*import(?:\s+type)?\s+(?P<spec>[\w*\s,{}$]+?)\s+from\s+['\"](?P<src>[^'\"]+)['\"]\s*;?",
    re.MULTILINE,
)
_NAMED_RE = re.compile(r"\{([^}]+)\}")
_DEFAULT_RE = re.compile(r"^([A-Za-z_$][\w$]*)\s*(?:,|$)")
_NS_RE = re.compile(r"\*\s+as\s+([A-Za-z_$][\w$]*)")
_ALIAS_RE = re.compile(r"^([A-Za-z_$][\w$]*)\s+as\s+([A-Za-z_$][\w$]*)$")


def _names_from_spec(spec: str) -> list[str]:
    """Extract bound names (source side, not alias) from an ESM import specifier."""
    names: list[str] = []
    rest = spec.strip()

    m = _DEFAULT_RE.match(rest)
    if m:
        names.append(m.group(1))
        rest = rest[m.end():].lstrip(", ")

    m = _NS_RE.search(rest)
    if m:
        names.append(m.group(1))
        rest = rest.replace(m.group(0), "")

    m = _NAMED_RE.search(rest)
    if m:
        for raw in m.group(1).split(","):
            raw = raw.strip()
            if not raw:
                continue
            if raw.startswith("type "):
                raw = raw[5:].strip()
            elif raw.startswith("typeof "):
                raw = raw[7:].strip()
            am = _ALIAS_RE.match(raw)
            names.append(am.group(1) if am else raw)

    return names


def _normalize_stem(name: str) -> str:
    """Lowercase + map '-' → '_' to match graphify's id convention for hyphenated filenames."""
    return name.lower().replace("-", "_")


def _module_leaf(src: str) -> str:
    """Resolve the leaf segment of an import path, treating '/index' as the parent."""
    parts = [p for p in src.rstrip("/").split("/") if p]
    while parts and parts[-1] in ("index", "index.ts", "index.tsx", "index.js"):
        parts.pop()
    if not parts:
        return ""
    leaf = parts[-1]
    return _normalize_stem(leaf.split(".")[0])


def extract(repo_root: Path, graph: GraphSnapshot) -> ExtractionResult:
    """Emit edges for cross-file TS/TSX named imports.

    Only resolves project-relative imports (``.``, ``./``, ``../``, ``@/``, ``~/``).
    Bare specifiers like ``react`` or ``zustand`` are skipped — those are external.

    For ``import { Foo } from "./bar/baz"``: emits ``caller → baz_foo`` (symbol target)
    and ``caller → foo`` (in case ``Foo`` is itself a module/namespace), mirroring
    cross_file_imports.py's dual-emit so both halves of the resolver hit.
    """
    src_root = repo_root / "frontend" / "src"
    if not src_root.exists():
        return ExtractionResult()

    failures: list[str] = []
    edges: list[ExtractedEdge] = []
    edge_keys: set[tuple[str, str, str]] = set()

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
                extractor="ts_imports",
            )
        )

    files = sorted(src_root.rglob("*.ts")) + sorted(src_root.rglob("*.tsx"))
    for path in files:
        if any(part.startswith(("node_modules", ".")) for part in path.parts):
            continue
        try:
            text = path.read_text()
        except OSError as exc:
            failures.append(f"{path}: {exc}")
            continue

        rel = str(path.relative_to(repo_root))
        caller_stem = _normalize_stem(path.stem)

        for match in _IMPORT_RE.finditer(text):
            src = match.group("src")
            if not (src.startswith(".") or src.startswith("@/") or src.startswith("~/")):
                continue
            leaf = _module_leaf(src)
            if not leaf:
                continue
            lineno = text[: match.start()].count("\n") + 1
            for name in _names_from_spec(match.group("spec")):
                add(caller_stem, node_id(leaf, name), rel, lineno)
                add(caller_stem, name.lstrip("_").lower(), rel, lineno)

    return ExtractionResult(edges=edges, failures=failures)
