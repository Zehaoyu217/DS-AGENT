from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from ....schema import GraphSnapshot
from ..schema import ExtractedEdge, ExtractionResult

HELPER_DIR = Path(__file__).parent / "_node_helper"
HELPER_SCRIPT = HELPER_DIR / "parse_jsx.mjs"


def _build_resolver(graph: GraphSnapshot) -> dict[str, str]:
    """Map lowercased component name → graphify node id, preferring function-level nodes."""
    by_paren: dict[str, str] = {}
    by_file: dict[str, str] = {}
    for n in graph.nodes:
        lab = n.get("label", "") or ""
        nid = n.get("id") or ""
        if lab.endswith("()"):
            by_paren.setdefault(lab[:-2].lower(), nid)
        elif lab.endswith(".tsx") or lab.endswith(".jsx"):
            by_file.setdefault(lab.rsplit(".", 1)[0].lower(), nid)
    return {**by_file, **by_paren}


def _resolve(name: str, resolver: dict[str, str]) -> str:
    """Resolve a JSX component name to a graphify-compatible node id."""
    key = name.lower()
    return resolver.get(key, f"{key}_{key}")


class ExtractorUnavailable(RuntimeError):
    """Raised when Node or @babel/parser is not installed."""


def extract(repo_root: Path, graph: GraphSnapshot) -> ExtractionResult:
    src_dir = repo_root / "frontend" / "src"
    if not src_dir.exists():
        return ExtractionResult()

    files = sorted(
        str(p) for p in src_dir.rglob("*.tsx")
    ) + sorted(
        str(p) for p in src_dir.rglob("*.jsx")
    )
    if not files:
        return ExtractionResult()

    if shutil.which("node") is None:
        return ExtractionResult(failures=["node executable not found on PATH"])
    if not (HELPER_DIR / "node_modules" / "@babel" / "parser").exists():
        return ExtractionResult(
            failures=[
                f"@babel/parser missing — run `npm install` in {HELPER_DIR}"
            ]
        )

    try:
        proc = subprocess.run(
            ["node", str(HELPER_SCRIPT)],
            input=json.dumps(files),
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return ExtractionResult(failures=["jsx_usage subprocess timed out"])

    if proc.returncode != 0:
        return ExtractionResult(failures=[f"node helper exit {proc.returncode}: {proc.stderr.strip()}"])

    try:
        records = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        return ExtractionResult(failures=[f"helper output not JSON: {exc}"])

    resolver = _build_resolver(graph)
    edges: list[ExtractedEdge] = []
    failures: list[str] = []
    files_skipped: list[str] = []
    edge_keys: set[tuple[str, str, str]] = set()

    for rec in records:
        rel = str(Path(rec["file"]).relative_to(repo_root))
        if rec.get("errors"):
            files_skipped.append(rel)
            failures.extend(f"{rel}: {e}" for e in rec["errors"])
            continue
        for edge in rec.get("edges", []):
            source = _resolve(edge["source"], resolver)
            target = _resolve(edge["target"], resolver)
            key = (source, target, "uses")
            if key in edge_keys or source == target:
                continue
            edge_keys.add(key)
            edges.append(
                ExtractedEdge(
                    source=source,
                    target=target,
                    relation="uses",
                    source_file=rel,
                    source_location=edge.get("line"),
                    extractor="jsx_usage",
                )
            )

    return ExtractionResult(edges=edges, files_skipped=files_skipped, failures=failures)
