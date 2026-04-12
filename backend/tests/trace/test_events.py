from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.trace.events import (
    TOOL_CALL_KIND,
    CompactionEvent,
    FinalOutputEvent,
    Grade,
    LlmCallEvent,
    PromptSection,
    ScratchpadWriteEvent,
    SessionEndEvent,
    SessionStartEvent,
    ToolCallEvent,
    Trace,
    TraceSummary,
)


def _llm_call_kwargs() -> dict[str, object]:
    return {
        "seq": 2,
        "timestamp": "2026-04-12T08:42:15Z",
        "step_id": "s1",
        "turn": 1,
        "model": "claude-opus-4-6",
        "temperature": 1.0,
        "max_tokens": 4096,
        "prompt_text": "hello",
        "sections": [PromptSection(source="SYSTEM_PROMPT", lines="1-50", text="...")],
        "response_text": "world",
        "tool_calls": [],
        "stop_reason": "end_turn",
        "input_tokens": 100,
        "output_tokens": 20,
        "cache_read_tokens": 0,
        "cache_creation_tokens": 0,
        "latency_ms": 250,
    }


def test_grade_accepts_valid_values() -> None:
    valid: list[Grade] = ["A", "B", "C", "F"]
    assert len(valid) == 4


def test_prompt_section_is_frozen() -> None:
    section = PromptSection(source="SYSTEM_PROMPT", lines="1-10", text="hi")
    with pytest.raises(ValidationError):
        section.source = "other"  # type: ignore[misc]


def test_llm_call_event_round_trip() -> None:
    event = LlmCallEvent(**_llm_call_kwargs())
    dumped = event.model_dump()
    restored = LlmCallEvent.model_validate(dumped)
    assert restored == event
    assert restored.kind == "llm_call"


def test_llm_call_event_is_frozen() -> None:
    event = LlmCallEvent(**_llm_call_kwargs())
    with pytest.raises(ValidationError):
        event.input_tokens = 9999  # type: ignore[misc]


def test_tool_call_event_kind_constant() -> None:
    assert TOOL_CALL_KIND == "tool_call"
    event = ToolCallEvent(
        seq=3,
        timestamp="2026-04-12T08:42:17Z",
        turn=1,
        tool_name="read_file",
        tool_input={"path": "/x"},
        tool_output="content",
        duration_ms=50,
        error=None,
    )
    assert event.kind == TOOL_CALL_KIND


def test_all_event_kinds_distinct() -> None:
    events = [
        SessionStartEvent(
            seq=1, timestamp="t", session_id="s", started_at="t",
            level=3, level_label="eval-level3", input_query="q",
        ),
        LlmCallEvent(**_llm_call_kwargs()),
        ToolCallEvent(
            seq=3, timestamp="t", turn=1, tool_name="x",
            tool_input={}, tool_output="y", duration_ms=1, error=None,
        ),
        CompactionEvent(
            seq=4, timestamp="t", turn=1,
            before_token_count=1000, after_token_count=500,
            dropped_layers=["a"], kept_layers=["b"],
        ),
        ScratchpadWriteEvent(
            seq=5, timestamp="t", turn=1, key="k", value_preview="v",
        ),
        FinalOutputEvent(
            seq=6, timestamp="t", output_text="out",
            final_grade="B", judge_dimensions={"acc": 0.9},
        ),
        SessionEndEvent(
            seq=7, timestamp="t", ended_at="t",
            duration_ms=100, outcome="ok", error=None,
        ),
    ]
    kinds = {e.kind for e in events}
    assert len(kinds) == 7


def test_trace_summary_round_trip() -> None:
    summary = TraceSummary(
        session_id="s1",
        started_at="t1",
        ended_at="t2",
        duration_ms=1000,
        level=3,
        level_label="eval-level3",
        turn_count=2,
        llm_call_count=3,
        total_input_tokens=100,
        total_output_tokens=50,
        outcome="ok",
        final_grade="F",
        step_ids=["s1", "s2", "s3"],
        trace_mode="on_failure",
        judge_runs_cached=5,
    )
    dumped = summary.model_dump()
    restored = TraceSummary.model_validate(dumped)
    assert restored == summary


def test_trace_full_round_trip() -> None:
    trace = Trace(
        trace_schema_version=1,
        summary=TraceSummary(
            session_id="s1", started_at="t1", ended_at="t2", duration_ms=10,
            level=3, level_label="eval-level3", turn_count=1, llm_call_count=1,
            total_input_tokens=100, total_output_tokens=20, outcome="ok",
            final_grade="F", step_ids=["s1"], trace_mode="on_failure",
            judge_runs_cached=0,
        ),
        judge_runs=[],
        events=[LlmCallEvent(**_llm_call_kwargs())],
    )
    dumped = trace.model_dump()
    restored = Trace.model_validate(dumped)
    assert restored == trace
    assert restored.events[0].kind == "llm_call"
