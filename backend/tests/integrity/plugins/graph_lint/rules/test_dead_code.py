from __future__ import annotations

from datetime import date
from pathlib import Path
from unittest.mock import patch

import pytest
from backend.app.integrity.plugins.graph_lint.rules import dead_code
from backend.app.integrity.plugins.graph_lint.wrappers.knip import KnipFinding, KnipResult
from backend.app.integrity.plugins.graph_lint.wrappers.vulture import (
    VultureFinding,
    VultureResult,
)
from backend.app.integrity.protocol import ScanContext
from backend.app.integrity.schema import GraphSnapshot


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / "backend" / "app").mkdir(parents=True)
    (tmp_path / "frontend" / "src").mkdir(parents=True)
    return tmp_path


def make_ctx(repo: Path, nodes: list[dict], links: list[dict]) -> ScanContext:
    return ScanContext(repo_root=repo, graph=GraphSnapshot(nodes=nodes, links=links))


def test_python_orphan_confirmed_by_vulture(repo: Path):
    (repo / "backend" / "app" / "x.py").write_text("def old_helper():\n    pass\n")
    nodes = [
        {"id": "x_old_helper", "label": "old_helper", "file_type": "code",
         "source_file": "backend/app/x.py", "kind": "function"},
    ]
    ctx = make_ctx(repo, nodes, [])
    with patch.object(dead_code, "_run_vulture") as mv, patch.object(dead_code, "_run_knip") as mk:
        mv.return_value = VultureResult(findings=[
            VultureFinding(
                path="backend/app/x.py", line=1, kind="function",
                name="old_helper", confidence=90,
            )
        ])
        mk.return_value = KnipResult()
        issues = dead_code.run(
            ctx, {"thresholds": {"vulture_min_confidence": 80}}, date(2026, 4, 17)
        )
    assert len(issues) == 1
    assert issues[0].rule == "graph.dead_code"
    assert issues[0].evidence == {"vulture": True, "knip": False, "graph_orphan": True}


def test_frontend_orphan_confirmed_by_knip_file(repo: Path):
    nodes = [
        {"id": "orphan_default", "label": "default", "file_type": "code",
         "source_file": "frontend/src/dead/orphan.tsx", "kind": "function"},
    ]
    ctx = make_ctx(repo, nodes, [])
    with patch.object(dead_code, "_run_vulture") as mv, patch.object(dead_code, "_run_knip") as mk:
        mv.return_value = VultureResult()
        mk.return_value = KnipResult(findings=[
            KnipFinding(kind="file", path="frontend/src/dead/orphan.tsx")
        ])
        issues = dead_code.run(
            ctx, {"thresholds": {"vulture_min_confidence": 80}}, date(2026, 4, 17)
        )
    assert len(issues) == 1
    assert issues[0].evidence == {"vulture": False, "knip": True, "graph_orphan": True}


def test_orphan_not_in_vulture_or_knip_skipped(repo: Path):
    (repo / "backend" / "app" / "x.py").write_text("def maybe_used():\n    pass\n")
    nodes = [
        {"id": "x_maybe_used", "label": "maybe_used", "file_type": "code",
         "source_file": "backend/app/x.py", "kind": "function"},
    ]
    ctx = make_ctx(repo, nodes, [])
    with patch.object(dead_code, "_run_vulture") as mv, patch.object(dead_code, "_run_knip") as mk:
        mv.return_value = VultureResult()
        mk.return_value = KnipResult()
        issues = dead_code.run(
            ctx, {"thresholds": {"vulture_min_confidence": 80}}, date(2026, 4, 17)
        )
    assert issues == []


def test_ignored_node_id_skipped(repo: Path):
    (repo / "backend" / "app" / "x.py").write_text("def old():\n    pass\n")
    nodes = [
        {"id": "x_old", "label": "old", "file_type": "code",
         "source_file": "backend/app/x.py", "kind": "function"},
    ]
    ctx = make_ctx(repo, nodes, [])
    with patch.object(dead_code, "_run_vulture") as mv, patch.object(dead_code, "_run_knip") as mk:
        mv.return_value = VultureResult(findings=[
            VultureFinding(
                path="backend/app/x.py", line=1, kind="function", name="old", confidence=90,
            )
        ])
        mk.return_value = KnipResult()
        issues = dead_code.run(
            ctx,
            {"thresholds": {"vulture_min_confidence": 80}, "ignored_dead_code": ["x_old"]},
            date(2026, 4, 17),
        )
    assert issues == []


def test_noqa_comment_at_definition_line_skipped(repo: Path):
    src = (repo / "backend" / "app" / "x.py")
    src.write_text("def old():  # noqa: dead-code\n    pass\n")
    nodes = [
        {"id": "x_old", "label": "old", "file_type": "code",
         "source_file": "backend/app/x.py", "kind": "function"},
    ]
    ctx = make_ctx(repo, nodes, [])
    with patch.object(dead_code, "_run_vulture") as mv, patch.object(dead_code, "_run_knip") as mk:
        mv.return_value = VultureResult(findings=[
            VultureFinding(
                path="backend/app/x.py", line=1, kind="function", name="old", confidence=90,
            )
        ])
        mk.return_value = KnipResult()
        issues = dead_code.run(
            ctx, {"thresholds": {"vulture_min_confidence": 80}}, date(2026, 4, 17)
        )
    assert issues == []


def test_vulture_failure_emits_info_issue(repo: Path):
    """When vulture wrapper returns a failure_message, an INFO issue is emitted."""
    nodes: list[dict] = []
    ctx = make_ctx(repo, nodes, [])
    with patch.object(dead_code, "_run_vulture") as mv, patch.object(dead_code, "_run_knip") as mk:
        mv.return_value = VultureResult(failure_message="vulture binary not found: /some/path")
        mk.return_value = KnipResult()
        issues = dead_code.run(
            ctx, {"thresholds": {"vulture_min_confidence": 80}}, date(2026, 4, 17)
        )
    info_issues = [i for i in issues if i.rule == "graph.dead_code.tool_unavailable"]
    assert len(info_issues) == 1
    issue = info_issues[0]
    assert issue.severity == "INFO"
    assert issue.node_id == "<vulture-unavailable>"
    assert issue.location == "backend/"
    assert "vulture binary not found" in issue.message


def test_knip_failure_emits_info_issue(repo: Path):
    """When knip wrapper returns a failure_message, an INFO issue is emitted."""
    nodes: list[dict] = []
    ctx = make_ctx(repo, nodes, [])
    with patch.object(dead_code, "_run_vulture") as mv, patch.object(dead_code, "_run_knip") as mk:
        mv.return_value = VultureResult()
        mk.return_value = KnipResult(failure_message="knip binary not found: npx")
        issues = dead_code.run(
            ctx, {"thresholds": {"vulture_min_confidence": 80}}, date(2026, 4, 17)
        )
    info_issues = [i for i in issues if i.rule == "graph.dead_code.tool_unavailable"]
    assert len(info_issues) == 1
    issue = info_issues[0]
    assert issue.severity == "INFO"
    assert issue.node_id == "<knip-unavailable>"
    assert issue.location == "frontend/"
    assert "knip binary not found" in issue.message


def test_both_tool_failures_emit_two_info_issues(repo: Path):
    """When both tools fail, two INFO issues are emitted."""
    nodes: list[dict] = []
    ctx = make_ctx(repo, nodes, [])
    with patch.object(dead_code, "_run_vulture") as mv, patch.object(dead_code, "_run_knip") as mk:
        mv.return_value = VultureResult(failure_message="vulture timed out")
        mk.return_value = KnipResult(failure_message="knip timed out")
        issues = dead_code.run(
            ctx, {"thresholds": {"vulture_min_confidence": 80}}, date(2026, 4, 17)
        )
    info_issues = [i for i in issues if i.rule == "graph.dead_code.tool_unavailable"]
    assert len(info_issues) == 2
    node_ids = {i.node_id for i in info_issues}
    assert node_ids == {"<vulture-unavailable>", "<knip-unavailable>"}


def test_vulture_failure_does_not_emit_python_dead_code(repo: Path):
    """A vulture failure must not produce graph.dead_code WARN issues (only INFO)."""
    nodes = [
        {"id": "x_old", "label": "old", "file_type": "code",
         "source_file": "backend/app/x.py", "kind": "function"},
    ]
    ctx = make_ctx(repo, nodes, [])
    with patch.object(dead_code, "_run_vulture") as mv, patch.object(dead_code, "_run_knip") as mk:
        mv.return_value = VultureResult(failure_message="vulture broke")
        mk.return_value = KnipResult()
        issues = dead_code.run(
            ctx, {"thresholds": {"vulture_min_confidence": 80}}, date(2026, 4, 17)
        )
    warn_issues = [i for i in issues if i.rule == "graph.dead_code" and i.severity == "WARN"]
    assert warn_issues == []
