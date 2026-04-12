from __future__ import annotations

from typing import Any

from app.sop.preflight import run_preflight
from app.sop.types import FailureReport, Signals


def _report(**overrides: Any) -> FailureReport:
    base: dict[str, Any] = dict(
        level=3, overall_grade="C", dimensions=[],
        signals=Signals(
            token_count=100, duration_ms=10, compaction_events=0,
            scratchpad_writes=0, tool_errors=0, retries=0,
            subagents_spawned=0, models_used={},
        ),
        judge_justifications={}, top_failure_signature="x",
        trace_id="x", trace_path="x", diff_vs_baseline=None,
    )
    base.update(overrides)
    return FailureReport(**base)


def test_all_pass_when_no_variance_no_drift() -> None:
    result = run_preflight(
        report=_report(),
        judge_variance={"detection_recall": 0.0},
        seed_fingerprint_matches=True,
        rerun_grades=["B", "B", "B"],
    )
    assert not result.any_failed()


def test_evaluation_bias_fails_when_judge_variance_exceeds_threshold() -> None:
    result = run_preflight(
        report=_report(),
        judge_variance={"detection_recall": 0.6},
        seed_fingerprint_matches=True,
        rerun_grades=["B", "B", "B"],
    )
    assert result.evaluation_bias == "fail"
    assert result.data_quality == "pass"
    assert result.determinism == "pass"


def test_data_quality_fails_on_seed_mismatch() -> None:
    result = run_preflight(
        report=_report(),
        judge_variance={},
        seed_fingerprint_matches=False,
        rerun_grades=["B", "B", "B"],
    )
    assert result.data_quality == "fail"


def test_determinism_fails_on_rerun_grade_variance() -> None:
    result = run_preflight(
        report=_report(),
        judge_variance={},
        seed_fingerprint_matches=True,
        rerun_grades=["B", "C", "B"],
    )
    assert result.determinism == "fail"


def test_determinism_skipped_when_fewer_than_two_reruns() -> None:
    result = run_preflight(
        report=_report(),
        judge_variance={},
        seed_fingerprint_matches=True,
        rerun_grades=["B"],
    )
    assert result.determinism == "skipped"
