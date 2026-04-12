"""Pydantic event models for the trace subsystem.

All events are frozen. `TraceEvent` is a discriminated union over `kind`.
"""
from __future__ import annotations

from typing import Annotated, Final, Literal

from pydantic import BaseModel, ConfigDict, Field

Grade = Literal["A", "B", "C", "F"]

SESSION_START_KIND: Final = "session_start"
LLM_CALL_KIND: Final = "llm_call"
TOOL_CALL_KIND: Final = "tool_call"
COMPACTION_KIND: Final = "compaction"
SCRATCHPAD_WRITE_KIND: Final = "scratchpad_write"
FINAL_OUTPUT_KIND: Final = "final_output"
SESSION_END_KIND: Final = "session_end"


class PromptSection(BaseModel):
    model_config = ConfigDict(frozen=True)
    source: str
    lines: str
    text: str


class _EventBase(BaseModel):
    model_config = ConfigDict(frozen=True)
    seq: int
    timestamp: str


class SessionStartEvent(_EventBase):
    kind: Literal["session_start"] = SESSION_START_KIND
    session_id: str
    started_at: str
    level: int
    level_label: str
    input_query: str


class LlmCallEvent(_EventBase):
    kind: Literal["llm_call"] = LLM_CALL_KIND
    step_id: str
    turn: int
    model: str
    temperature: float
    max_tokens: int
    prompt_text: str
    sections: list[PromptSection]
    response_text: str
    tool_calls: list[dict[str, object]]
    stop_reason: str
    input_tokens: int
    output_tokens: int
    cache_read_tokens: int
    cache_creation_tokens: int
    latency_ms: int


class ToolCallEvent(_EventBase):
    kind: Literal["tool_call"] = TOOL_CALL_KIND
    turn: int
    tool_name: str
    tool_input: dict[str, object]
    tool_output: str
    duration_ms: int
    error: str | None


class CompactionEvent(_EventBase):
    kind: Literal["compaction"] = COMPACTION_KIND
    turn: int
    before_token_count: int
    after_token_count: int
    dropped_layers: list[str]
    kept_layers: list[str]


class ScratchpadWriteEvent(_EventBase):
    kind: Literal["scratchpad_write"] = SCRATCHPAD_WRITE_KIND
    turn: int
    key: str
    value_preview: str


class FinalOutputEvent(_EventBase):
    kind: Literal["final_output"] = FINAL_OUTPUT_KIND
    output_text: str
    final_grade: Grade | None
    judge_dimensions: dict[str, float]


class SessionEndEvent(_EventBase):
    kind: Literal["session_end"] = SESSION_END_KIND
    ended_at: str
    duration_ms: int
    outcome: Literal["ok", "error"]
    error: str | None


TraceEvent = Annotated[
    SessionStartEvent
    | LlmCallEvent
    | ToolCallEvent
    | CompactionEvent
    | ScratchpadWriteEvent
    | FinalOutputEvent
    | SessionEndEvent,
    Field(discriminator="kind"),
]


class TraceSummary(BaseModel):
    model_config = ConfigDict(frozen=True)
    session_id: str
    started_at: str
    ended_at: str
    duration_ms: int
    level: int
    level_label: str
    turn_count: int
    llm_call_count: int
    total_input_tokens: int
    total_output_tokens: int
    outcome: Literal["ok", "error"]
    final_grade: Grade | None
    step_ids: list[str]
    trace_mode: Literal["always", "on_failure"]
    judge_runs_cached: int


class JudgeRun(BaseModel):
    model_config = ConfigDict(frozen=True)
    dimensions: dict[str, float]


class Trace(BaseModel):
    model_config = ConfigDict(frozen=True)
    trace_schema_version: int = 1
    summary: TraceSummary
    judge_runs: list[JudgeRun]
    events: list[TraceEvent]
