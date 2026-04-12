from __future__ import annotations

from pathlib import Path

from app.evals.types import AgentTrace, DimensionGrade, LevelResult
from app.sop.baseline import update_baseline
from app.sop.reporter import build_failure_report, write_failure_report
from app.sop.types import Baseline, Signals


def _trace() -> AgentTrace:
    return AgentTrace(
        queries=["SELECT 1"],
        intermediate=[
            {"kind": "tool_call", "name": "sql"},
            {"kind": "compaction"},
            {"kind": "compaction"},
            {"kind": "compaction"},
            {"kind": "tool_error", "error": "timeout"},
        ],
        final_output="...",
        token_count=18400,
        duration_ms=47200,
        errors=["timeout"],
    )


def _level_result() -> LevelResult:
    return LevelResult(
        level=3,
        name="anomaly",
        dimensions=[
            DimensionGrade(
                name="detection_recall", grade="B", score=0.7, weight=0.3, justification="ok"
            ),
            DimensionGrade(
                name="false_positive_handling",
                grade="F",
                score=0.0,
                weight=0.3,
                justification="flagged bonus",
            ),
        ],
        weighted_score=0.35,
        grade="C",
    )


def test_build_failure_report_extracts_signals() -> None:
    fr = build_failure_report(
        level_result=_level_result(),
        trace=_trace(),
        trace_id="eval-x",
        trace_path="traces/eval-x.json",
        baseline=None,
    )
    assert fr.level == 3
    assert fr.overall_grade == "C"
    assert fr.signals.compaction_events == 3
    assert fr.signals.tool_errors == 1
    assert fr.signals.token_count == 18400
    assert fr.top_failure_signature


def test_build_failure_report_computes_diff(tmp_path: Path) -> None:
    baseline = Baseline(
        level=3, date="2026-04-10", trace_id="prior",
        signals=Signals(
            token_count=12800, duration_ms=30000, compaction_events=1,
            scratchpad_writes=8, tool_errors=0, retries=0,
            subagents_spawned=2, models_used={"sonnet": 3, "haiku": 5},
        ),
    )
    update_baseline(baseline, tmp_path)
    fr = build_failure_report(
        level_result=_level_result(),
        trace=_trace(),
        trace_id="eval-x",
        trace_path="traces/eval-x.json",
        baseline=baseline,
    )
    assert fr.diff_vs_baseline is not None
    assert fr.diff_vs_baseline.changes["token_count"]["before"] == 12800
    assert fr.diff_vs_baseline.changes["token_count"]["after"] == 18400
    assert fr.diff_vs_baseline.changes["scratchpad_writes"]["before"] == 8
    assert fr.diff_vs_baseline.changes["scratchpad_writes"]["after"] == 0


def test_write_failure_report_yaml(tmp_path: Path) -> None:
    fr = build_failure_report(
        level_result=_level_result(), trace=_trace(),
        trace_id="eval-x", trace_path="x.json", baseline=None,
    )
    path = write_failure_report(fr, tmp_path, date="2026-04-12")
    assert path.exists()
    assert path.name == "2026-04-12-level3.yaml"
