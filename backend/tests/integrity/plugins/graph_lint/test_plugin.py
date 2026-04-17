from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest
from backend.app.integrity.plugins.graph_lint.plugin import GraphLintPlugin
from backend.app.integrity.protocol import ScanContext
from backend.app.integrity.schema import GraphSnapshot


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / "graphify").mkdir()
    (tmp_path / "graphify" / "graph.json").write_text(json.dumps({"nodes": [], "links": []}))
    return tmp_path


def test_plugin_returns_scan_result(repo: Path):
    ctx = ScanContext(repo_root=repo, graph=GraphSnapshot.load(repo))
    plugin = GraphLintPlugin(today=date(2026, 4, 17))
    result = plugin.scan(ctx)
    assert result.plugin_name == "graph_lint"
    assert isinstance(result.issues, list)


def test_plugin_writes_artifact(repo: Path):
    ctx = ScanContext(repo_root=repo, graph=GraphSnapshot.load(repo))
    plugin = GraphLintPlugin(today=date(2026, 4, 17))
    result = plugin.scan(ctx)
    artifact = repo / "integrity-out" / "2026-04-17" / "graph_lint.json"
    assert artifact.exists()
    assert artifact in result.artifacts
    data = json.loads(artifact.read_text())
    assert "issues" in data and "rules_run" in data


def test_plugin_skips_disabled_rules(repo: Path):
    ctx = ScanContext(repo_root=repo, graph=GraphSnapshot.load(repo))
    plugin = GraphLintPlugin(
        today=date(2026, 4, 17),
        config={"thresholds": {}, "ignored_dead_code": [], "excluded_paths": [],
                "disabled_rules": ["graph.dead_code"]},
    )
    plugin.scan(ctx)
    artifact_data = json.loads(
        (repo / "integrity-out" / "2026-04-17" / "graph_lint.json").read_text()
    )
    assert "graph.dead_code" not in artifact_data["rules_run"]
