from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from ....issue import IntegrityIssue
from ....protocol import ScanContext
from ..orphans import find_orphans
from ..wrappers.knip import KnipResult, run_knip
from ..wrappers.vulture import VultureResult, run_vulture


# Thin indirections so tests can patch.
def _run_vulture(target: Path, min_confidence: int) -> VultureResult:
    return run_vulture(target, min_confidence=min_confidence)


def _run_knip(frontend_dir: Path) -> KnipResult:
    return run_knip(frontend_dir)


_NOQA_MARKERS = ("# noqa: dead-code", "// knip-ignore")


def _has_noqa(repo_root: Path, source_file: str, line: int) -> bool:
    p = repo_root / source_file
    if not p.exists():
        return False
    try:
        src = p.read_text().splitlines()
    except OSError:
        return False
    if line < 1 or line > len(src):
        return False
    return any(marker in src[line - 1] for marker in _NOQA_MARKERS)


def _python_dead_code(
    ctx: ScanContext,
    orphans: set[str],
    vulture_result: VultureResult,
    ignored: set[str],
) -> list[IntegrityIssue]:
    if vulture_result.failure_message or not vulture_result.findings:
        return []
    nodes_by_path_and_name: dict[tuple[str, str], dict[str, Any]] = {}
    for n in ctx.graph.nodes:
        src = n.get("source_file", "") or ""
        if not src.endswith(".py"):
            continue
        nodes_by_path_and_name[(src, n.get("label", ""))] = n

    out: list[IntegrityIssue] = []
    for v in vulture_result.findings:
        node = nodes_by_path_and_name.get((v.path, v.name))
        if node is None:
            continue
        if node["id"] not in orphans:
            continue
        if node["id"] in ignored:
            continue
        if _has_noqa(ctx.repo_root, v.path, v.line):
            continue
        out.append(
            IntegrityIssue(
                rule="graph.dead_code",
                severity="WARN",
                node_id=node["id"],
                location=f"{v.path}:{v.line}",
                message="Symbol unreferenced (vulture+graph triple-confirm)",
                evidence={"vulture": True, "knip": False, "graph_orphan": True},
                fix_class="delete_dead_code",
            )
        )
    return out


def _frontend_dead_code(
    ctx: ScanContext,
    orphans: set[str],
    knip_result: KnipResult,
    ignored: set[str],
) -> list[IntegrityIssue]:
    if knip_result.failure_message or not knip_result.findings:
        return []
    files_flagged: set[str] = {f.path for f in knip_result.findings if f.kind == "file"}
    exports_flagged: dict[str, set[str]] = {}
    for f in knip_result.findings:
        if f.kind == "export":
            exports_flagged.setdefault(f.path, set()).add(f.name)

    out: list[IntegrityIssue] = []
    for n in ctx.graph.nodes:
        src = n.get("source_file", "") or ""
        if not src.endswith((".ts", ".tsx", ".js", ".jsx")):
            continue
        if n["id"] not in orphans:
            continue
        if n["id"] in ignored:
            continue
        knip_match = src in files_flagged or n.get("label", "") in exports_flagged.get(src, set())
        if not knip_match:
            continue
        out.append(
            IntegrityIssue(
                rule="graph.dead_code",
                severity="WARN",
                node_id=n["id"],
                location=f"{src}:{n.get('source_location', 1) or 1}",
                message="Symbol unreferenced (knip+graph triple-confirm)",
                evidence={"vulture": False, "knip": True, "graph_orphan": True},
                fix_class="delete_dead_code",
            )
        )
    return out


def run(ctx: ScanContext, config: dict[str, Any], today: date) -> list[IntegrityIssue]:
    thresholds = config.get("thresholds", {})
    min_conf = int(thresholds.get("vulture_min_confidence", 80))
    ignored = set(config.get("ignored_dead_code", []))

    backend_app = ctx.repo_root / "backend" / "app"
    frontend_dir = ctx.repo_root / "frontend"

    vulture_result = (
        _run_vulture(backend_app, min_conf) if backend_app.exists() else VultureResult()
    )
    knip_result = _run_knip(frontend_dir) if frontend_dir.exists() else KnipResult()

    orphans = set(find_orphans(ctx.graph))

    return [
        *_python_dead_code(ctx, orphans, vulture_result, ignored),
        *_frontend_dead_code(ctx, orphans, knip_result, ignored),
    ]
