from __future__ import annotations

from typing import Any

from app.sop.triage import triage
from app.sop.types import DiffVsBaseline, FailureReport, Signals


def _report(
    *, signals: Signals, diff: DiffVsBaseline | None = None, level: int = 3
) -> FailureReport:
    return FailureReport(
        level=level, overall_grade="C", dimensions=[],
        signals=signals, judge_justifications={}, top_failure_signature="x",
        trace_id="x", trace_path="x", diff_vs_baseline=diff,
    )


def _signals(**overrides: Any) -> Signals:
    base: dict[str, Any] = dict(
        token_count=1000, duration_ms=1000, compaction_events=0,
        scratchpad_writes=0, tool_errors=0, retries=0,
        subagents_spawned=0, models_used={},
    )
    base.update(overrides)
    return Signals(**base)


def test_picks_context_when_compaction_high_and_no_scratchpad() -> None:
    decision = triage(_report(
        signals=_signals(compaction_events=3, scratchpad_writes=0, token_count=20000),
        diff=DiffVsBaseline(baseline_date="2026-04-10", baseline_grade="B",
                            changes={"token_count": {"before": 10000, "after": 20000}}),
    ))
    assert decision is not None
    assert decision.bucket == "context"
    assert any("scratchpad" in e or "compaction" in e for e in decision.evidence)


def test_picks_harness_when_tool_errors_no_retries() -> None:
    decision = triage(_report(
        signals=_signals(tool_errors=2, retries=0),
    ))
    assert decision is not None
    assert decision.bucket == "harness"


def test_stops_at_first_actionable_bucket_preferring_context_over_harness() -> None:
    decision = triage(_report(
        signals=_signals(compaction_events=5, scratchpad_writes=0, tool_errors=2, retries=0),
    ))
    assert decision is not None
    assert decision.bucket == "context"


def test_returns_none_when_no_signal_matches() -> None:
    decision = triage(_report(signals=_signals()))
    assert decision is None


def test_picks_routing_when_sonnet_absent_on_reasoning_level() -> None:
    decision = triage(_report(
        signals=_signals(models_used={"haiku": 10, "sonnet": 0}),
    ))
    assert decision is not None
    assert decision.bucket == "routing"


def test_picks_architecture_on_level5_with_no_subagents() -> None:
    decision = triage(_report(
        signals=_signals(subagents_spawned=0),
        level=5,
    ))
    assert decision is not None
    assert decision.bucket == "architecture"
