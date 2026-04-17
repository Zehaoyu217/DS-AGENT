import json
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / "graphify").mkdir()
    (tmp_path / "graphify" / "graph.json").write_text(
        json.dumps({"nodes": [], "links": []})
    )
    return tmp_path


def run_cli(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "backend.app.integrity", *args],
        cwd=str(repo),
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(Path(__file__).resolve().parent.parent.parent.parent)},
    )


def test_cli_runs_and_writes_report(repo: Path):
    result = run_cli(repo, "--no-augment")
    assert result.returncode == 0, result.stderr
    today_dirs = list((repo / "integrity-out").glob("*"))
    assert any((d / "report.json").exists() for d in today_dirs if d.is_dir())


def test_cli_plugin_filter_runs_only_named(repo: Path):
    result = run_cli(repo, "--no-augment", "--plugin", "graph_lint")
    assert result.returncode == 0, result.stderr


def test_cli_unknown_plugin_exits_nonzero(repo: Path):
    result = run_cli(repo, "--plugin", "nonexistent")
    assert result.returncode != 0
    assert "nonexistent" in result.stderr
