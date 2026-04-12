from __future__ import annotations

from app.trace.events import (
    CompactionEvent,
    LlmCallEvent,
    PromptSection,
    ScratchpadWriteEvent,
    SessionEndEvent,
    SessionStartEvent,
    ToolCallEvent,
    Trace,
    TraceSummary,
)
from app.trace.timeline import build_timeline


def _base_events() -> list[object]:
    return [
        SessionStartEvent(
            seq=1, timestamp="t", session_id="sess", started_at="t",
            level=3, level_label="eval-level3", input_query="q",
        ),
        SessionEndEvent(
            seq=99, timestamp="t", ended_at="t",
            duration_ms=1, outcome="ok", error=None,
        ),
    ]


def _trace(events: list[object]) -> Trace:
    return Trace(
        trace_schema_version=1,
        summary=TraceSummary(
            session_id="sess", started_at="t", ended_at="t",
            duration_ms=1, level=3, level_label="eval-level3",
            turn_count=0, llm_call_count=0, total_input_tokens=0,
            total_output_tokens=0, outcome="ok", final_grade=None,
            step_ids=[], trace_mode="always", judge_runs_cached=0,
        ),
        judge_runs=[],
        events=events,  # type: ignore[arg-type]
    )


def _llm(seq: int, turn: int, input_tokens: int = 100) -> LlmCallEvent:
    return LlmCallEvent(
        seq=seq, timestamp="t", step_id=f"s{seq}", turn=turn,
        model="m", temperature=1.0, max_tokens=10, prompt_text="p",
        sections=[PromptSection(source="sys", lines="1-10", text="...")],
        response_text="r", tool_calls=[], stop_reason="end_turn",
        input_tokens=input_tokens, output_tokens=20,
        cache_read_tokens=0, cache_creation_tokens=0, latency_ms=0,
    )


def test_build_timeline_empty_trace_returns_empty_arrays() -> None:
    result = build_timeline(_trace(_base_events()))
    assert result["turns"] == []
    assert result["events"] == []


def test_build_timeline_groups_llm_calls_by_turn() -> None:
    events = _base_events()
    events.append(_llm(2, turn=1, input_tokens=500))
    events.append(_llm(3, turn=1, input_tokens=300))
    events.append(_llm(4, turn=2, input_tokens=1000))
    result = build_timeline(_trace(events))
    assert [t["turn"] for t in result["turns"]] == [1, 2]
    assert result["turns"][0]["layers"]["input"] == 800
    assert result["turns"][1]["layers"]["input"] == 1000


def test_build_timeline_includes_compaction_events() -> None:
    events = _base_events()
    events.append(_llm(2, turn=1))
    events.append(CompactionEvent(
        seq=3, timestamp="t", turn=1,
        before_token_count=5000, after_token_count=2000,
        dropped_layers=["a", "b"], kept_layers=["c"],
    ))
    result = build_timeline(_trace(events))
    compactions = [e for e in result["events"] if e["kind"] == "compaction"]
    assert len(compactions) == 1
    assert "3000" in compactions[0]["detail"] or "dropped 2" in compactions[0]["detail"]
    assert compactions[0]["turn"] == 1


def test_build_timeline_includes_scratchpad_events() -> None:
    events = _base_events()
    events.append(_llm(2, turn=1))
    events.append(ScratchpadWriteEvent(
        seq=3, timestamp="t", turn=1, key="findings", value_preview="preview...",
    ))
    result = build_timeline(_trace(events))
    scratch = [e for e in result["events"] if e["kind"] == "scratchpad_write"]
    assert len(scratch) == 1
    assert scratch[0]["detail"] == "findings"


def test_build_timeline_counts_tool_calls_per_turn() -> None:
    events = _base_events()
    events.append(_llm(2, turn=1))
    events.append(ToolCallEvent(
        seq=3, timestamp="t", turn=1, tool_name="read_file",
        tool_input={}, tool_output="x", duration_ms=1, error=None,
    ))
    events.append(ToolCallEvent(
        seq=4, timestamp="t", turn=1, tool_name="read_file",
        tool_input={}, tool_output="y", duration_ms=1, error=None,
    ))
    result = build_timeline(_trace(events))
    assert result["turns"][0]["layers"]["tool_calls"] == 2
