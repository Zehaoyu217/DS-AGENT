from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml


def test_cli_prints_result_for_latest_report(tmp_path: Path) -> None:
    reports = tmp_path / "reports"
    reports.mkdir()
    report = {
        "level": 3, "overall_grade": "C", "dimensions": [],
        "signals": {
            "token_count": 20000, "duration_ms": 10, "compaction_events": 3,
            "scratchpad_writes": 0, "tool_errors": 0, "retries": 0,
            "subagents_spawned": 0, "models_used": {"haiku": 5, "sonnet": 2},
        },
        "judge_justifications": {}, "top_failure_signature": "x",
        "trace_id": "x", "trace_path": "x", "diff_vs_baseline": None,
    }
    (reports / "2026-04-12-level3.yaml").write_text(yaml.safe_dump(report))

    result = subprocess.run(
        [sys.executable, "-m", "app.sop.cli", "--level", "3", "--reports-dir", str(reports)],
        capture_output=True, text=True, cwd=Path(__file__).resolve().parents[2],
    )
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["triage"]["bucket"] == "context"
    assert data["proposal"]["id"] == "context-01"
