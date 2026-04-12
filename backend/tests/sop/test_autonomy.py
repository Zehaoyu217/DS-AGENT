from __future__ import annotations

from pathlib import Path

from app.sop.autonomy import (
    evaluate_graduation_readiness,
    load_autonomy_config,
    mark_autonomous,
    revert_to_proposed,
)
from app.sop.log import write_entry
from app.sop.types import (
    FixApplied,
    IterationLogEntry,
    PreflightResult,
    TriageDecision,
)


def _entry(
    session_id: str,
    bucket: str,
    *,
    ladder_id: str,
    success: bool,
    regressions: str = "none",
) -> IterationLogEntry:
    return IterationLogEntry(
        date=session_id[:10],
        session_id=session_id,
        level=3,
        overall_grade_before="C",
        preflight=PreflightResult(evaluation_bias="pass", data_quality="pass", determinism="pass"),
        triage=TriageDecision(bucket=bucket, evidence=["e"], hypothesis="h"),
        fix=FixApplied(
            ladder_id=ladder_id, name="n", files_changed=["f"],
            model_used_for_fix="sonnet", cost_bucket="trivial",
        ),
        outcome={
            "grade_after": "B" if success else "C",
            "regressions": regressions,
            "iterations": 1,
            "success": success,
        },
        trace_links={"before": "a.json", "after": "b.json"},
    )


def test_load_missing_config_returns_empty(tmp_path: Path) -> None:
    cfg = load_autonomy_config(tmp_path / "missing.yaml")
    assert cfg.autonomous_buckets == []


def test_mark_autonomous_and_revert_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "autonomy.yaml"
    mark_autonomous("context", path)
    assert load_autonomy_config(path).autonomous_buckets == ["context"]
    revert_to_proposed("context", path)
    assert load_autonomy_config(path).autonomous_buckets == []


def test_graduation_fails_without_five_sessions(tmp_path: Path) -> None:
    for i in range(4):
        write_entry(_entry(f"2026-04-0{i+1}-level3-001", "context",
                           ladder_id=f"context-0{i%3+1}", success=True), tmp_path)
    assert not evaluate_graduation_readiness("context", tmp_path)


def test_graduation_passes_with_five_sessions_80pct_success_three_rungs(tmp_path: Path) -> None:
    rungs = ["context-01", "context-02", "context-03", "context-01", "context-02"]
    for i, rung in enumerate(rungs):
        write_entry(_entry(f"2026-04-0{i+1}-level3-001", "context",
                           ladder_id=rung, success=True), tmp_path)
    assert evaluate_graduation_readiness("context", tmp_path)


def test_graduation_fails_with_low_success_rate(tmp_path: Path) -> None:
    for i in range(5):
        write_entry(_entry(f"2026-04-0{i+1}-level3-001", "context",
                           ladder_id=f"context-0{i%3+1}",
                           success=(i < 3)), tmp_path)
    assert not evaluate_graduation_readiness("context", tmp_path)


def test_graduation_fails_when_only_two_distinct_rungs(tmp_path: Path) -> None:
    for i in range(5):
        write_entry(_entry(f"2026-04-0{i+1}-level3-001", "context",
                           ladder_id=f"context-0{i%2+1}", success=True), tmp_path)
    assert not evaluate_graduation_readiness("context", tmp_path)
