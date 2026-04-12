"""Tests for SOP Pydantic models."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.sop.types import (
    Baseline,
    DiffVsBaseline,
    DimensionScore,
    FailureReport,
    FixApplied,
    IterationLogEntry,
    PreflightResult,
    Signals,
    TriageDecision,
)


def test_signals_required_fields() -> None:
    s = Signals(
        token_count=18400,
        duration_ms=47200,
        compaction_events=3,
        scratchpad_writes=0,
        tool_errors=1,
        retries=0,
        subagents_spawned=0,
        models_used={"haiku": 12, "sonnet": 0},
    )
    assert s.scratchpad_writes == 0
    assert s.models_used["haiku"] == 12


def test_failure_report_roundtrip() -> None:
    fr = FailureReport(
        level=3,
        overall_grade="C",
        dimensions=[DimensionScore(name="detection_recall", score="B", weight=0.3)],
        signals=Signals(
            token_count=100, duration_ms=10, compaction_events=0,
            scratchpad_writes=0, tool_errors=0, retries=0,
            subagents_spawned=0, models_used={},
        ),
        judge_justifications={"detection_recall": "ok"},
        top_failure_signature="missed_anomaly",
        trace_id="eval-x",
        trace_path="path/to/trace.json",
        diff_vs_baseline=None,
    )
    dumped = fr.model_dump()
    restored = FailureReport.model_validate(dumped)
    assert restored == fr


def test_failure_report_invalid_grade_rejected() -> None:
    with pytest.raises(ValidationError):
        FailureReport.model_validate({
            "level": 3,
            "overall_grade": "Z",  # invalid — runtime rejection expected
            "dimensions": [],
            "signals": {
                "token_count": 0, "duration_ms": 0, "compaction_events": 0,
                "scratchpad_writes": 0, "tool_errors": 0, "retries": 0,
                "subagents_spawned": 0, "models_used": {},
            },
            "judge_justifications": {},
            "top_failure_signature": "x",
            "trace_id": "x",
            "trace_path": "x",
            "diff_vs_baseline": None,
        })


def test_baseline_minimum_fields() -> None:
    b = Baseline(
        level=3, date="2026-04-10", trace_id="eval-y", grade="B",
        signals=Signals(
            token_count=12800, duration_ms=30000, compaction_events=1,
            scratchpad_writes=8, tool_errors=0, retries=0,
            subagents_spawned=2, models_used={"sonnet": 3, "haiku": 5},
        ),
    )
    assert b.level == 3
    assert b.grade == "B"


def test_diff_vs_baseline_shape() -> None:
    d = DiffVsBaseline(
        baseline_date="2026-04-10",
        baseline_grade="B",
        changes={"scratchpad_writes": {"before": 8, "after": 0}},
    )
    assert d.changes["scratchpad_writes"]["before"] == 8


def test_iteration_log_entry_minimum() -> None:
    e = IterationLogEntry(
        date="2026-04-12",
        session_id="2026-04-12-level3-001",
        level=3,
        overall_grade_before="C",
        preflight=PreflightResult(evaluation_bias="pass", data_quality="pass", determinism="pass"),
        triage=TriageDecision(bucket="context", evidence=["x"], hypothesis="y"),
        fix=FixApplied(
            ladder_id="context-01", name="z", files_changed=["a"],
            model_used_for_fix="sonnet", cost_bucket="trivial",
        ),
        outcome={"grade_after": "B", "regressions": "none", "iterations": 1, "success": True},
        trace_links={"before": "a.json", "after": "b.json"},
    )
    assert e.triage.bucket == "context"
