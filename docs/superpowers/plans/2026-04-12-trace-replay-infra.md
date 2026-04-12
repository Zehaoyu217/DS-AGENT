# Trace-Replay Infrastructure & DevTools Selection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the trace subsystem that captures per-session agent events into YAML files, the `/api/trace/*` REST surface that serves derived diagnostic views, and the DevTools selection wiring that activates the Judge Variance / Prompt Inspector / Compaction Timeline tabs.

**Architecture:** Sync in-process event bus with Pydantic v2 frozen event models. `TraceRecorder` subscribes, buffers in-memory, writes atomically at finalize. Read-only `TraceStore` serves Pydantic-validated views to FastAPI handlers under `/api/trace/*`. Frontend Zustand store gains selection state mirrored to URL via a `useSelectionUrlSync` hook. Trace package has zero dependency on `sop/`.

**Tech Stack:** Python 3.12, Pydantic v2, FastAPI + TestClient, PyYAML, pytest + tmp_path + monkeypatch, mypy --strict, ruff. Frontend: TypeScript 5.7 strict, Zustand 5, React 19, vitest + @testing-library/react.

**Source of truth:** `docs/superpowers/specs/2026-04-12-trace-replay-infra-design.md`

---

## File Structure

### Backend — new files

- `backend/app/trace/__init__.py` — package init, re-exports public API
- `backend/app/trace/events.py` — Pydantic event models (`SessionStartEvent`, `LlmCallEvent`, `ToolCallEvent`, `CompactionEvent`, `ScratchpadWriteEvent`, `FinalOutputEvent`, `SessionEndEvent`), `PromptSection`, `Grade` alias, `TraceSummary`, `Trace`, `TraceEvent` discriminated union
- `backend/app/trace/bus.py` — sync pub/sub singleton
- `backend/app/trace/recorder.py` — `TraceRecorder` subscriber + finalize
- `backend/app/trace/store.py` — `list_traces`, `load_trace` with regex guards
- `backend/app/trace/assembler.py` — `assemble_prompt` returns `{sections, conflicts}`
- `backend/app/trace/timeline.py` — `build_timeline` returns `{turns, events}`
- `backend/app/trace/judge_replay.py` — `run_judge_variance` (cached + live)
- `backend/app/trace/retention.py` — CLI module with `--clear-all`, `--older-than`, `--grade`
- `backend/app/trace/publishers.py` — typed publish helpers + `TraceSession` context manager
- `backend/app/api/trace_api.py` — FastAPI router `/api/trace/*`
- `backend/tests/trace/__init__.py` — empty
- `backend/tests/trace/test_events.py`
- `backend/tests/trace/test_bus.py`
- `backend/tests/trace/test_recorder.py`
- `backend/tests/trace/test_store.py`
- `backend/tests/trace/test_assembler.py`
- `backend/tests/trace/test_timeline.py`
- `backend/tests/trace/test_judge_replay.py`
- `backend/tests/trace/test_retention.py`
- `backend/tests/trace/test_trace_api.py`
- `backend/tests/trace/test_publishers.py`
- `backend/tests/trace/test_integration.py`

### Backend — modified files

- `backend/app/main.py` — mount `trace_router`
- `backend/app/context/manager.py` — `record_compaction` also publishes `CompactionEvent`
- `backend/app/api/sop_api.py` — stub handlers become forwarding shims
- `backend/app/sop/types.py` — add `trace_id: str | None = None` to `SOPSession`
- `.env.example` — new env vars
- `Makefile` — `eval-trace`, `clean-traces` targets
- `.gitignore` — `traces/`

### Frontend — new files

- `frontend/src/devtools/sop/useSelectionUrlSync.ts`
- `frontend/src/devtools/sop/sop.css` — (only if doesn't exist) `.sop-row--selected`
- `frontend/src/stores/__tests__/devtools.test.ts`
- `frontend/src/devtools/sop/__tests__/useSelectionUrlSync.test.ts`

### Frontend — modified files

- `frontend/src/stores/devtools.ts` — + selection state
- `frontend/src/devtools/sop/api.ts` — endpoints flip to `/api/trace/*`
- `frontend/src/devtools/sop/SessionReplay.tsx` — row click
- `frontend/src/devtools/sop/PromptInspector.tsx` — step dropdown
- `frontend/src/devtools/sop/CompactionTimeline.tsx` — bar click
- `frontend/src/devtools/DevToolsPanel.tsx` — remove hardcoded nulls, wire URL hook
- `frontend/src/devtools/sop/SessionReplay.test.tsx`
- `frontend/src/devtools/sop/PromptInspector.test.tsx`
- `frontend/src/devtools/sop/CompactionTimeline.test.tsx`

---

## Conventions

- **All backend files:** `from __future__ import annotations` at the top.
- **All Pydantic models:** v2 syntax, `ConfigDict(frozen=True)` on public data contracts.
- **Dict annotations:** `dict[str, object]`, never bare `dict`.
- **Python version:** 3.12+.
- **Test runner:** `cd backend && uv run python -m pytest` (plain python not on PATH).
- **Type check:** `cd backend && uv run mypy --strict app/trace app/api/trace_api.py`.
- **Lint:** `cd backend && uv run ruff check app/trace app/api/trace_api.py`.
- **Frontend tests:** `cd frontend && npm test -- --run <path>` (vitest).
- **Commits:** `<type>: <short description>` (feat, fix, refactor, test, docs, chore).

---

## Task 1: Event models and Grade alias

**Files:**
- Create: `backend/app/trace/__init__.py`
- Create: `backend/app/trace/events.py`
- Create: `backend/tests/trace/__init__.py`
- Create: `backend/tests/trace/test_events.py`

- [ ] **Step 1.1: Create empty package init files**

Write `backend/app/trace/__init__.py`:

```python
"""Trace subsystem: event capture, storage, and derived views.

This package has zero dependency on app.sop.
"""
from __future__ import annotations
```

Write `backend/tests/trace/__init__.py`: empty file.

- [ ] **Step 1.2: Write failing test for event models**

Write `backend/tests/trace/test_events.py`:

```python
from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.trace.events import (
    CompactionEvent,
    FinalOutputEvent,
    Grade,
    LlmCallEvent,
    PromptSection,
    ScratchpadWriteEvent,
    SessionEndEvent,
    SessionStartEvent,
    TOOL_CALL_KIND,
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
```

- [ ] **Step 1.3: Run tests — expect failure**

Run: `cd backend && uv run python -m pytest tests/trace/test_events.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'app.trace.events'`.

- [ ] **Step 1.4: Implement events.py**

Write `backend/app/trace/events.py`:

```python
"""Pydantic event models for the trace subsystem.

All events are frozen. `TraceEvent` is a discriminated union over `kind`.
"""
from __future__ import annotations

from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, Field

Grade = Literal["A", "B", "C", "F"]

SESSION_START_KIND = "session_start"
LLM_CALL_KIND = "llm_call"
TOOL_CALL_KIND = "tool_call"
COMPACTION_KIND = "compaction"
SCRATCHPAD_WRITE_KIND = "scratchpad_write"
FINAL_OUTPUT_KIND = "final_output"
SESSION_END_KIND = "session_end"


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
    Union[
        SessionStartEvent,
        LlmCallEvent,
        ToolCallEvent,
        CompactionEvent,
        ScratchpadWriteEvent,
        FinalOutputEvent,
        SessionEndEvent,
    ],
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
```

- [ ] **Step 1.5: Run tests — expect pass + typecheck + lint**

```bash
cd backend && uv run python -m pytest tests/trace/test_events.py -v
cd backend && uv run mypy --strict app/trace/events.py
cd backend && uv run ruff check app/trace/events.py tests/trace/test_events.py
```

All three expected to pass.

- [ ] **Step 1.6: Commit**

```bash
git add backend/app/trace/__init__.py backend/app/trace/events.py backend/tests/trace/__init__.py backend/tests/trace/test_events.py
git commit -m "feat(trace): add Pydantic event models and data contracts"
```

---

## Task 2: Event bus

**Files:**
- Create: `backend/app/trace/bus.py`
- Create: `backend/tests/trace/test_bus.py`

- [ ] **Step 2.1: Write failing test for bus**

Write `backend/tests/trace/test_bus.py`:

```python
from __future__ import annotations

import pytest

from app.trace import bus
from app.trace.events import SessionEndEvent


@pytest.fixture(autouse=True)
def _reset_bus() -> None:
    bus.reset()


def _event(seq: int = 0) -> SessionEndEvent:
    return SessionEndEvent(
        seq=seq, timestamp="t", ended_at="t",
        duration_ms=1, outcome="ok", error=None,
    )


def test_publish_fans_out_to_all_subscribers() -> None:
    received_a: list[object] = []
    received_b: list[object] = []
    bus.subscribe(received_a.append)
    bus.subscribe(received_b.append)
    bus.publish(_event())
    assert len(received_a) == 1
    assert len(received_b) == 1


def test_publish_assigns_monotonic_seq() -> None:
    received: list[int] = []
    bus.subscribe(lambda e: received.append(e.seq))
    bus.publish(_event(seq=0))
    bus.publish(_event(seq=0))
    bus.publish(_event(seq=0))
    assert received == [1, 2, 3]


def test_publish_with_no_subscribers_is_noop() -> None:
    bus.publish(_event())  # must not raise


def test_reset_clears_subscribers_and_counter() -> None:
    received: list[object] = []
    bus.subscribe(received.append)
    bus.publish(_event())
    bus.reset()
    bus.publish(_event())
    assert len(received) == 1  # second publish had no subscriber


def test_seq_resets_with_reset() -> None:
    received: list[int] = []
    bus.publish(_event())  # seq 1, no subscriber
    bus.reset()
    bus.subscribe(lambda e: received.append(e.seq))
    bus.publish(_event())
    assert received == [1]
```

- [ ] **Step 2.2: Run tests — expect failure**

Run: `cd backend && uv run python -m pytest tests/trace/test_bus.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'app.trace.bus'`.

- [ ] **Step 2.3: Implement bus.py**

Write `backend/app/trace/bus.py`:

```python
"""Sync in-process event bus for the trace subsystem.

Module-level singleton. Synchronous publish — no threads, no async.
"""
from __future__ import annotations

from collections.abc import Callable

from app.trace.events import TraceEvent

Subscriber = Callable[[TraceEvent], None]

_subscribers: list[Subscriber] = []
_seq_counter: int = 0


def publish(event: TraceEvent) -> None:
    """Assign monotonic seq, then fan out to all subscribers."""
    global _seq_counter
    _seq_counter += 1
    stamped = event.model_copy(update={"seq": _seq_counter})
    for sub in _subscribers:
        sub(stamped)


def subscribe(fn: Subscriber) -> None:
    _subscribers.append(fn)


def reset() -> None:
    """Clear subscribers and reset seq counter (test-only)."""
    global _seq_counter
    _subscribers.clear()
    _seq_counter = 0
```

- [ ] **Step 2.4: Run tests + typecheck + lint**

```bash
cd backend && uv run python -m pytest tests/trace/test_bus.py -v
cd backend && uv run mypy --strict app/trace/bus.py
cd backend && uv run ruff check app/trace/bus.py tests/trace/test_bus.py
```

- [ ] **Step 2.5: Commit**

```bash
git add backend/app/trace/bus.py backend/tests/trace/test_bus.py
git commit -m "feat(trace): add sync in-process event bus"
```

---

## Task 3: Trace recorder

**Files:**
- Create: `backend/app/trace/recorder.py`
- Create: `backend/tests/trace/test_recorder.py`

- [ ] **Step 3.1: Write failing tests for recorder**

Write `backend/tests/trace/test_recorder.py`:

```python
from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import cast

import pytest
import yaml

from app.trace.events import (
    FinalOutputEvent,
    JudgeRun,
    LlmCallEvent,
    PromptSection,
    SessionEndEvent,
    SessionStartEvent,
    ToolCallEvent,
)
from app.trace.recorder import TraceRecorder


def _session_start(seq: int) -> SessionStartEvent:
    return SessionStartEvent(
        seq=seq, timestamp="2026-04-12T08:42:13Z",
        session_id="sess-1", started_at="2026-04-12T08:42:13Z",
        level=3, level_label="eval-level3", input_query="q",
    )


def _llm_call(seq: int, step_id: str, turn: int = 1) -> LlmCallEvent:
    return LlmCallEvent(
        seq=seq, timestamp="2026-04-12T08:42:15Z",
        step_id=step_id, turn=turn, model="claude-opus-4-6",
        temperature=1.0, max_tokens=4096, prompt_text="hi",
        sections=[PromptSection(source="SYSTEM_PROMPT", lines="1-10", text="...")],
        response_text="out", tool_calls=[], stop_reason="end_turn",
        input_tokens=100, output_tokens=20,
        cache_read_tokens=0, cache_creation_tokens=0, latency_ms=50,
    )


def _tool_call(seq: int, turn: int = 1) -> ToolCallEvent:
    return ToolCallEvent(
        seq=seq, timestamp="2026-04-12T08:42:17Z",
        turn=turn, tool_name="read_file", tool_input={"path": "/x"},
        tool_output="content", duration_ms=5, error=None,
    )


def _final_output(seq: int, grade: str | None = "F") -> FinalOutputEvent:
    return FinalOutputEvent(
        seq=seq, timestamp="2026-04-12T08:42:50Z",
        output_text="final", final_grade=cast("object", grade),  # type: ignore[arg-type]
        judge_dimensions={"accuracy": 0.5},
    )


def _session_end(seq: int) -> SessionEndEvent:
    return SessionEndEvent(
        seq=seq, timestamp="2026-04-12T08:42:55Z",
        ended_at="2026-04-12T08:42:55Z",
        duration_ms=42000, outcome="ok", error=None,
    )


def _feed(recorder: TraceRecorder, grade: str | None = "F") -> None:
    recorder.on_event(_session_start(1))
    recorder.on_event(_llm_call(2, "s1"))
    recorder.on_event(_tool_call(3))
    recorder.on_event(_llm_call(4, "s2"))
    recorder.on_event(_final_output(5, grade))
    recorder.on_event(_session_end(6))


def test_finalize_writes_file_when_trace_mode_always(tmp_path: Path) -> None:
    rec = TraceRecorder(session_id="sess-1", trace_mode="always", output_dir=tmp_path)
    _feed(rec, grade="A")
    result = rec.finalize(final_grade="A")
    assert result == tmp_path / "sess-1.yaml"
    assert result.exists()


def test_finalize_skips_write_on_failure_mode_with_passing_grade(tmp_path: Path) -> None:
    rec = TraceRecorder(session_id="sess-1", trace_mode="on_failure", output_dir=tmp_path)
    _feed(rec, grade="B")
    result = rec.finalize(final_grade="B")
    assert result is None
    assert not (tmp_path / "sess-1.yaml").exists()


def test_finalize_writes_on_failure_mode_with_failing_grade(tmp_path: Path) -> None:
    rec = TraceRecorder(session_id="sess-1", trace_mode="on_failure", output_dir=tmp_path)
    _feed(rec, grade="F")
    result = rec.finalize(final_grade="F")
    assert result is not None
    assert result.exists()


def test_finalize_writes_on_failure_mode_when_grade_is_none(tmp_path: Path) -> None:
    rec = TraceRecorder(session_id="sess-1", trace_mode="on_failure", output_dir=tmp_path)
    _feed(rec, grade=None)
    result = rec.finalize(final_grade=None)
    assert result is not None


def test_trace_file_contains_schema_version_summary_and_events(tmp_path: Path) -> None:
    rec = TraceRecorder(session_id="sess-1", trace_mode="always", output_dir=tmp_path)
    _feed(rec, grade="F")
    path = rec.finalize(final_grade="F")
    assert path is not None
    data = yaml.safe_load(path.read_text())
    assert data["trace_schema_version"] == 1
    assert data["summary"]["session_id"] == "sess-1"
    assert data["summary"]["turn_count"] == 1
    assert data["summary"]["llm_call_count"] == 2
    assert data["summary"]["step_ids"] == ["s1", "s2"]
    assert data["summary"]["total_input_tokens"] == 200
    assert data["summary"]["total_output_tokens"] == 40
    assert data["summary"]["outcome"] == "ok"
    assert data["summary"]["final_grade"] == "F"
    assert data["summary"]["trace_mode"] == "always"
    assert len(data["events"]) == 6


def test_finalize_runs_judge_runner_when_provided(tmp_path: Path) -> None:
    calls: list[str] = []

    def judge_runner(final_output: str, n: int) -> list[JudgeRun]:
        calls.append(final_output)
        return [JudgeRun(dimensions={"accuracy": float(i)}) for i in range(n)]

    rec = TraceRecorder(
        session_id="sess-1", trace_mode="always",
        output_dir=tmp_path, judge_runner=judge_runner, judge_n=3,
    )
    _feed(rec, grade="F")
    path = rec.finalize(final_grade="F")
    assert path is not None
    data = yaml.safe_load(path.read_text())
    assert len(data["judge_runs"]) == 3
    assert data["summary"]["judge_runs_cached"] == 3
    assert calls == ["final"]


def test_finalize_truncates_oversized_fields(tmp_path: Path) -> None:
    rec = TraceRecorder(
        session_id="sess-1", trace_mode="always",
        output_dir=tmp_path, max_event_size_bytes=32,
    )
    big = "x" * 1000
    rec.on_event(_session_start(1))
    rec.on_event(ToolCallEvent(
        seq=2, timestamp="t", turn=1, tool_name="t",
        tool_input={}, tool_output=big, duration_ms=1, error=None,
    ))
    rec.on_event(_session_end(3))
    path = rec.finalize(final_grade=None)
    assert path is not None
    data = yaml.safe_load(path.read_text())
    tool_event = next(e for e in data["events"] if e["kind"] == "tool_call")
    assert len(tool_event["tool_output"]) < len(big)
    assert tool_event.get("__truncated") is True


def test_finalize_swallows_write_errors(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    rec = TraceRecorder(session_id="sess-1", trace_mode="always", output_dir=tmp_path)
    _feed(rec)

    def boom(*_: object, **__: object) -> None:
        raise OSError("disk full")

    monkeypatch.setattr("app.trace.recorder.atomic_write_yaml", cast(Callable[..., None], boom))
    assert rec.finalize(final_grade="F") is None  # must not raise
```

- [ ] **Step 3.2: Run tests — expect failure**

Run: `cd backend && uv run python -m pytest tests/trace/test_recorder.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'app.trace.recorder'`.

- [ ] **Step 3.3: Implement recorder.py**

Write `backend/app/trace/recorder.py`:

```python
"""TraceRecorder — buffers events in-memory and finalizes to disk."""
from __future__ import annotations

import os
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import yaml

from app.trace.events import (
    FinalOutputEvent,
    Grade,
    JudgeRun,
    LlmCallEvent,
    SessionEndEvent,
    SessionStartEvent,
    ToolCallEvent,
    Trace,
    TraceEvent,
    TraceSummary,
)

JudgeRunner = Callable[[str, int], list[JudgeRun]]

TRUNCATABLE_FIELDS: tuple[str, ...] = (
    "prompt_text", "response_text", "tool_output", "value_preview", "output_text",
)


def atomic_write_yaml(path: Path, data: dict[str, Any]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    os.replace(tmp, path)


class TraceRecorder:
    def __init__(
        self,
        session_id: str,
        trace_mode: str,
        output_dir: Path,
        judge_runner: JudgeRunner | None = None,
        judge_n: int = 5,
        max_event_size_bytes: int = 10240,
    ) -> None:
        self._session_id = session_id
        self._trace_mode = trace_mode
        self._output_dir = output_dir
        self._judge_runner = judge_runner
        self._judge_n = judge_n
        self._max_event_size_bytes = max_event_size_bytes
        self._events: list[TraceEvent] = []

    def on_event(self, ev: TraceEvent) -> None:
        self._events.append(ev)

    def finalize(self, final_grade: Grade | None) -> Path | None:
        if not self._should_write(final_grade):
            return None
        try:
            summary = self._build_summary(final_grade)
            judge_runs = self._run_judge()
            event_dumps = [self._truncate(e.model_dump()) for e in self._events]
            trace = {
                "trace_schema_version": 1,
                "summary": summary.model_dump(),
                "judge_runs": [jr.model_dump() for jr in judge_runs],
                "events": event_dumps,
            }
            path = self._output_dir / f"{self._session_id}.yaml"
            atomic_write_yaml(path, trace)
            return path
        except Exception as exc:  # noqa: BLE001  — tracing must never raise
            print(f"[trace] finalize failed for {self._session_id}: {exc}", file=sys.stderr)
            return None

    def _should_write(self, final_grade: Grade | None) -> bool:
        if self._trace_mode == "always":
            return True
        return final_grade not in ("A", "B")

    def _run_judge(self) -> list[JudgeRun]:
        if self._judge_runner is None:
            return []
        final_event = next(
            (e for e in self._events if isinstance(e, FinalOutputEvent)), None,
        )
        if final_event is None:
            return []
        return self._judge_runner(final_event.output_text, self._judge_n)

    def _build_summary(self, final_grade: Grade | None) -> TraceSummary:
        start = next((e for e in self._events if isinstance(e, SessionStartEvent)), None)
        end = next((e for e in self._events if isinstance(e, SessionEndEvent)), None)
        llm_calls = [e for e in self._events if isinstance(e, LlmCallEvent)]
        tool_calls = [e for e in self._events if isinstance(e, ToolCallEvent)]
        turns = {e.turn for e in llm_calls} | {e.turn for e in tool_calls}
        if start is None:
            raise ValueError("trace missing SessionStartEvent")
        return TraceSummary(
            session_id=start.session_id,
            started_at=start.started_at,
            ended_at=end.ended_at if end else start.started_at,
            duration_ms=end.duration_ms if end else 0,
            level=start.level,
            level_label=start.level_label,
            turn_count=len(turns),
            llm_call_count=len(llm_calls),
            total_input_tokens=sum(e.input_tokens for e in llm_calls),
            total_output_tokens=sum(e.output_tokens for e in llm_calls),
            outcome=end.outcome if end else "ok",
            final_grade=final_grade,
            step_ids=[e.step_id for e in llm_calls],
            trace_mode="always" if self._trace_mode == "always" else "on_failure",
            judge_runs_cached=self._judge_n if self._judge_runner else 0,
        )

    def _truncate(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        truncated = dict(event_dict)
        was_truncated = False
        for field in TRUNCATABLE_FIELDS:
            value = truncated.get(field)
            if isinstance(value, str):
                encoded = value.encode("utf-8")
                if len(encoded) > self._max_event_size_bytes:
                    cut = encoded[: self._max_event_size_bytes].decode("utf-8", errors="ignore")
                    truncated[field] = cut
                    was_truncated = True
        if was_truncated:
            truncated["__truncated"] = True
        return truncated
```

- [ ] **Step 3.4: Run tests + typecheck + lint**

```bash
cd backend && uv run python -m pytest tests/trace/test_recorder.py -v
cd backend && uv run mypy --strict app/trace/recorder.py
cd backend && uv run ruff check app/trace/recorder.py tests/trace/test_recorder.py
```

- [ ] **Step 3.5: Commit**

```bash
git add backend/app/trace/recorder.py backend/tests/trace/test_recorder.py
git commit -m "feat(trace): add TraceRecorder with finalize gating and truncation"
```

---

## Task 4: Trace store (read-only load + list)

**Files:**
- Create: `backend/app/trace/store.py`
- Create: `backend/tests/trace/test_store.py`

- [ ] **Step 4.1: Write failing tests for store**

Write `backend/tests/trace/test_store.py`:

```python
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from app.trace.store import TraceNotFoundError, list_traces, load_trace


def _minimal_trace_yaml(session_id: str, grade: str | None = "F") -> dict[str, object]:
    return {
        "trace_schema_version": 1,
        "summary": {
            "session_id": session_id, "started_at": "t1", "ended_at": "t2",
            "duration_ms": 1000, "level": 3, "level_label": "eval-level3",
            "turn_count": 1, "llm_call_count": 1,
            "total_input_tokens": 100, "total_output_tokens": 20,
            "outcome": "ok", "final_grade": grade,
            "step_ids": ["s1"], "trace_mode": "on_failure",
            "judge_runs_cached": 0,
        },
        "judge_runs": [],
        "events": [
            {
                "kind": "session_start", "seq": 1, "timestamp": "t1",
                "session_id": session_id, "started_at": "t1",
                "level": 3, "level_label": "eval-level3", "input_query": "q",
            },
            {
                "kind": "session_end", "seq": 2, "timestamp": "t2",
                "ended_at": "t2", "duration_ms": 1000,
                "outcome": "ok", "error": None,
            },
        ],
    }


def _write(dir_: Path, session_id: str, grade: str | None = "F") -> None:
    (dir_ / f"{session_id}.yaml").write_text(
        yaml.safe_dump(_minimal_trace_yaml(session_id, grade)),
        encoding="utf-8",
    )


def test_list_traces_returns_summaries_sorted_by_session_id(tmp_path: Path) -> None:
    _write(tmp_path, "sess-b")
    _write(tmp_path, "sess-a")
    _write(tmp_path, "sess-c")
    summaries = list_traces(tmp_path)
    assert [s.session_id for s in summaries] == ["sess-a", "sess-b", "sess-c"]


def test_list_traces_returns_empty_list_when_dir_missing(tmp_path: Path) -> None:
    assert list_traces(tmp_path / "missing") == []


def test_list_traces_skips_non_yaml_files(tmp_path: Path) -> None:
    (tmp_path / "notes.txt").write_text("hi")
    _write(tmp_path, "sess-1")
    summaries = list_traces(tmp_path)
    assert [s.session_id for s in summaries] == ["sess-1"]


def test_load_trace_returns_full_trace(tmp_path: Path) -> None:
    _write(tmp_path, "sess-1")
    trace = load_trace(tmp_path, "sess-1")
    assert trace.summary.session_id == "sess-1"
    assert len(trace.events) == 2


def test_load_trace_raises_on_invalid_id(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="invalid trace_id"):
        load_trace(tmp_path, "../etc/passwd")


def test_load_trace_raises_not_found(tmp_path: Path) -> None:
    with pytest.raises(TraceNotFoundError):
        load_trace(tmp_path, "missing")


def test_load_trace_raises_on_corrupted_yaml(tmp_path: Path) -> None:
    (tmp_path / "sess-1.yaml").write_text(": : :", encoding="utf-8")
    with pytest.raises(ValueError):
        load_trace(tmp_path, "sess-1")


def test_list_traces_skips_corrupted_files(tmp_path: Path) -> None:
    _write(tmp_path, "good")
    (tmp_path / "bad.yaml").write_text("not valid: : :", encoding="utf-8")
    summaries = list_traces(tmp_path)
    assert [s.session_id for s in summaries] == ["good"]
```

- [ ] **Step 4.2: Run tests — expect failure**

Run: `cd backend && uv run python -m pytest tests/trace/test_store.py -v`
Expected: FAIL — `ModuleNotFoundError`.

- [ ] **Step 4.3: Implement store.py**

Write `backend/app/trace/store.py`:

```python
"""Read-only store: list summaries and load full traces from disk."""
from __future__ import annotations

import re
from pathlib import Path

import yaml
from pydantic import ValidationError

from app.trace.events import Trace, TraceSummary

_TRACE_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")


class TraceNotFoundError(FileNotFoundError):
    pass


def _validate_trace_id(trace_id: str) -> None:
    if not _TRACE_ID_RE.match(trace_id):
        raise ValueError("invalid trace_id")


def list_traces(traces_dir: Path) -> list[TraceSummary]:
    if not traces_dir.exists():
        return []
    summaries: list[TraceSummary] = []
    for path in sorted(traces_dir.glob("*.yaml")):
        try:
            raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            continue
        if not isinstance(raw, dict):
            continue
        summary_raw = raw.get("summary")
        if not isinstance(summary_raw, dict):
            continue
        try:
            summaries.append(TraceSummary.model_validate(summary_raw))
        except ValidationError:
            continue
    return summaries


def load_trace(traces_dir: Path, trace_id: str) -> Trace:
    _validate_trace_id(trace_id)
    path = traces_dir / f"{trace_id}.yaml"
    if not path.exists():
        raise TraceNotFoundError(f"trace not found: {trace_id}")
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"corrupted trace YAML: {trace_id}") from exc
    if not isinstance(raw, dict):
        raise ValueError(f"invalid trace structure: {trace_id}")
    try:
        return Trace.model_validate(raw)
    except ValidationError as exc:
        raise ValueError(f"trace failed schema validation: {trace_id}") from exc
```

- [ ] **Step 4.4: Run tests + typecheck + lint**

```bash
cd backend && uv run python -m pytest tests/trace/test_store.py -v
cd backend && uv run mypy --strict app/trace/store.py
cd backend && uv run ruff check app/trace/store.py tests/trace/test_store.py
```

- [ ] **Step 4.5: Commit**

```bash
git add backend/app/trace/store.py backend/tests/trace/test_store.py
git commit -m "feat(trace): add read-only TraceStore with path-traversal guard"
```

---

## Task 5: Prompt assembler

**Files:**
- Create: `backend/app/trace/assembler.py`
- Create: `backend/tests/trace/test_assembler.py`

- [ ] **Step 5.1: Write failing tests for assembler**

Write `backend/tests/trace/test_assembler.py`:

```python
from __future__ import annotations

import pytest

from app.trace.assembler import (
    StepNotFoundError,
    assemble_prompt,
    detect_conflicts,
)
from app.trace.events import (
    LlmCallEvent,
    PromptSection,
    SessionEndEvent,
    SessionStartEvent,
    Trace,
    TraceSummary,
)


def _trace(sections_per_step: dict[str, list[PromptSection]]) -> Trace:
    step_ids = list(sections_per_step.keys())
    events: list[object] = [
        SessionStartEvent(
            seq=1, timestamp="t", session_id="sess-1", started_at="t",
            level=3, level_label="eval-level3", input_query="q",
        ),
    ]
    for i, step_id in enumerate(step_ids, start=2):
        events.append(LlmCallEvent(
            seq=i, timestamp="t", step_id=step_id, turn=1,
            model="m", temperature=1.0, max_tokens=10, prompt_text="p",
            sections=sections_per_step[step_id], response_text="r",
            tool_calls=[], stop_reason="end_turn",
            input_tokens=0, output_tokens=0,
            cache_read_tokens=0, cache_creation_tokens=0, latency_ms=0,
        ))
    events.append(SessionEndEvent(
        seq=99, timestamp="t", ended_at="t",
        duration_ms=1, outcome="ok", error=None,
    ))
    return Trace(
        trace_schema_version=1,
        summary=TraceSummary(
            session_id="sess-1", started_at="t", ended_at="t",
            duration_ms=1, level=3, level_label="eval-level3",
            turn_count=1, llm_call_count=len(step_ids),
            total_input_tokens=0, total_output_tokens=0,
            outcome="ok", final_grade=None,
            step_ids=step_ids, trace_mode="always",
            judge_runs_cached=0,
        ),
        judge_runs=[],
        events=events,  # type: ignore[arg-type]
    )


def test_assemble_returns_sections_for_step() -> None:
    sections = [
        PromptSection(source="SYSTEM_PROMPT", lines="1-50", text="..."),
        PromptSection(source="user_query", lines="51-52", text="..."),
    ]
    trace = _trace({"s1": sections})
    result = assemble_prompt(trace, "s1")
    assert result["sections"] == [s.model_dump() for s in sections]
    assert result["conflicts"] == []


def test_assemble_raises_for_missing_step() -> None:
    trace = _trace({"s1": []})
    with pytest.raises(StepNotFoundError):
        assemble_prompt(trace, "s99")


def test_detect_conflicts_flags_overlapping_ranges() -> None:
    sections = [
        PromptSection(source="rules.md", lines="100-150", text="a"),
        PromptSection(source="rules.md", lines="120-170", text="b"),
    ]
    conflicts = detect_conflicts(sections)
    assert len(conflicts) == 1
    assert conflicts[0]["source_a"] == "rules.md"
    assert conflicts[0]["source_b"] == "rules.md"
    assert conflicts[0]["overlap"] == "120-150"


def test_detect_conflicts_ignores_different_sources() -> None:
    sections = [
        PromptSection(source="a.md", lines="1-10", text="a"),
        PromptSection(source="b.md", lines="1-10", text="b"),
    ]
    assert detect_conflicts(sections) == []


def test_detect_conflicts_ignores_non_overlapping_same_source() -> None:
    sections = [
        PromptSection(source="a.md", lines="1-10", text="a"),
        PromptSection(source="a.md", lines="20-30", text="b"),
    ]
    assert detect_conflicts(sections) == []


def test_detect_conflicts_handles_malformed_range() -> None:
    sections = [
        PromptSection(source="a.md", lines="garbage", text="a"),
        PromptSection(source="a.md", lines="1-10", text="b"),
    ]
    assert detect_conflicts(sections) == []
```

- [ ] **Step 5.2: Run tests — expect failure**

Run: `cd backend && uv run python -m pytest tests/trace/test_assembler.py -v`
Expected: FAIL — `ModuleNotFoundError`.

- [ ] **Step 5.3: Implement assembler.py**

Write `backend/app/trace/assembler.py`:

```python
"""Prompt assembler: reads captured sections, detects byte-range conflicts."""
from __future__ import annotations

import re

from app.trace.events import LlmCallEvent, PromptSection, Trace

_RANGE_RE = re.compile(r"^(\d+)-(\d+)$")


class StepNotFoundError(LookupError):
    pass


def _parse_range(spec: str) -> tuple[int, int] | None:
    match = _RANGE_RE.match(spec.strip())
    if not match:
        return None
    start, end = int(match.group(1)), int(match.group(2))
    if start > end:
        return None
    return start, end


def detect_conflicts(sections: list[PromptSection]) -> list[dict[str, str]]:
    conflicts: list[dict[str, str]] = []
    for i, a in enumerate(sections):
        range_a = _parse_range(a.lines)
        if range_a is None:
            continue
        for b in sections[i + 1:]:
            if a.source != b.source:
                continue
            range_b = _parse_range(b.lines)
            if range_b is None:
                continue
            overlap_start = max(range_a[0], range_b[0])
            overlap_end = min(range_a[1], range_b[1])
            if overlap_start <= overlap_end:
                conflicts.append({
                    "source_a": a.source,
                    "source_b": b.source,
                    "overlap": f"{overlap_start}-{overlap_end}",
                })
    return conflicts


def assemble_prompt(trace: Trace, step_id: str) -> dict[str, object]:
    for event in trace.events:
        if isinstance(event, LlmCallEvent) and event.step_id == step_id:
            return {
                "sections": [s.model_dump() for s in event.sections],
                "conflicts": detect_conflicts(list(event.sections)),
            }
    raise StepNotFoundError(f"step_id not in trace: {step_id}")
```

- [ ] **Step 5.4: Run tests + typecheck + lint**

```bash
cd backend && uv run python -m pytest tests/trace/test_assembler.py -v
cd backend && uv run mypy --strict app/trace/assembler.py
cd backend && uv run ruff check app/trace/assembler.py tests/trace/test_assembler.py
```

- [ ] **Step 5.5: Commit**

```bash
git add backend/app/trace/assembler.py backend/tests/trace/test_assembler.py
git commit -m "feat(trace): add prompt assembler with conflict detection"
```

---

## Task 6: Timeline builder

**Files:**
- Create: `backend/app/trace/timeline.py`
- Create: `backend/tests/trace/test_timeline.py`

- [ ] **Step 6.1: Write failing tests for timeline**

Write `backend/tests/trace/test_timeline.py`:

```python
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
```

- [ ] **Step 6.2: Run tests — expect failure**

Run: `cd backend && uv run python -m pytest tests/trace/test_timeline.py -v`
Expected: FAIL — `ModuleNotFoundError`.

- [ ] **Step 6.3: Implement timeline.py**

Write `backend/app/trace/timeline.py`:

```python
"""Timeline builder: groups events by turn, produces layers + event list."""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable

from app.trace.events import (
    CompactionEvent,
    LlmCallEvent,
    ScratchpadWriteEvent,
    ToolCallEvent,
    Trace,
)


def build_timeline(trace: Trace) -> dict[str, object]:
    input_by_turn: dict[int, int] = defaultdict(int)
    tool_count_by_turn: dict[int, int] = defaultdict(int)
    events_out: list[dict[str, object]] = []

    for event in trace.events:
        if isinstance(event, LlmCallEvent):
            input_by_turn[event.turn] += event.input_tokens
        elif isinstance(event, ToolCallEvent):
            tool_count_by_turn[event.turn] += 1
        elif isinstance(event, CompactionEvent):
            freed = event.before_token_count - event.after_token_count
            detail = f"dropped {len(event.dropped_layers)} layers, -{freed} tokens"
            events_out.append({
                "turn": event.turn,
                "kind": "compaction",
                "detail": detail,
            })
        elif isinstance(event, ScratchpadWriteEvent):
            events_out.append({
                "turn": event.turn,
                "kind": "scratchpad_write",
                "detail": event.key,
            })

    turn_ids: Iterable[int] = sorted(set(input_by_turn) | set(tool_count_by_turn))
    turns_out: list[dict[str, object]] = [
        {
            "turn": turn,
            "layers": {
                "input": input_by_turn.get(turn, 0),
                "tool_calls": tool_count_by_turn.get(turn, 0),
            },
        }
        for turn in turn_ids
    ]
    return {"turns": turns_out, "events": events_out}
```

- [ ] **Step 6.4: Run tests + typecheck + lint**

```bash
cd backend && uv run python -m pytest tests/trace/test_timeline.py -v
cd backend && uv run mypy --strict app/trace/timeline.py
cd backend && uv run ruff check app/trace/timeline.py tests/trace/test_timeline.py
```

- [ ] **Step 6.5: Commit**

```bash
git add backend/app/trace/timeline.py backend/tests/trace/test_timeline.py
git commit -m "feat(trace): add timeline builder grouping events by turn"
```

---

## Task 7: Judge replayer (cached + live)

**Files:**
- Create: `backend/app/trace/judge_replay.py`
- Create: `backend/tests/trace/test_judge_replay.py`

- [ ] **Step 7.1: Write failing tests for judge_replay**

Write `backend/tests/trace/test_judge_replay.py`:

```python
from __future__ import annotations

from collections.abc import Callable

import pytest

from app.trace.events import (
    FinalOutputEvent,
    JudgeRun,
    SessionEndEvent,
    SessionStartEvent,
    Trace,
    TraceSummary,
)
from app.trace.judge_replay import (
    MissingApiKeyError,
    compute_variance,
    run_judge_variance,
)


def _trace(judge_runs: list[JudgeRun], output_text: str = "final") -> Trace:
    return Trace(
        trace_schema_version=1,
        summary=TraceSummary(
            session_id="sess", started_at="t", ended_at="t",
            duration_ms=1, level=3, level_label="eval-level3",
            turn_count=0, llm_call_count=0, total_input_tokens=0,
            total_output_tokens=0, outcome="ok", final_grade="F",
            step_ids=[], trace_mode="always",
            judge_runs_cached=len(judge_runs),
        ),
        judge_runs=judge_runs,
        events=[
            SessionStartEvent(
                seq=1, timestamp="t", session_id="sess", started_at="t",
                level=3, level_label="eval-level3", input_query="q",
            ),
            FinalOutputEvent(
                seq=2, timestamp="t", output_text=output_text,
                final_grade="F", judge_dimensions={},
            ),
            SessionEndEvent(
                seq=3, timestamp="t", ended_at="t",
                duration_ms=1, outcome="ok", error=None,
            ),
        ],
    )


def test_compute_variance_on_identical_runs_is_zero() -> None:
    runs = [JudgeRun(dimensions={"a": 1.0}) for _ in range(3)]
    variance = compute_variance(runs)
    assert variance == {"a": 0.0}


def test_compute_variance_spread() -> None:
    runs = [
        JudgeRun(dimensions={"a": 0.0}),
        JudgeRun(dimensions={"a": 1.0}),
    ]
    variance = compute_variance(runs)
    assert 0.4 < variance["a"] < 0.6  # spread is |max-min|/2 or std-dev-ish


def test_cached_path_returns_cached_variance() -> None:
    trace = _trace([
        JudgeRun(dimensions={"accuracy": 0.5}),
        JudgeRun(dimensions={"accuracy": 0.9}),
    ])
    result = run_judge_variance(trace, n=5, refresh=False, threshold=0.1)
    assert result["source"] == "cached"
    assert result["n"] == 2
    assert "accuracy" in result["variance"]
    assert result["threshold_exceeded"] == ["accuracy"]


def test_threshold_exceeded_is_empty_when_below_threshold() -> None:
    trace = _trace([
        JudgeRun(dimensions={"accuracy": 0.5}),
        JudgeRun(dimensions={"accuracy": 0.51}),
    ])
    result = run_judge_variance(trace, n=5, refresh=False, threshold=0.1)
    assert result["threshold_exceeded"] == []


def test_live_path_calls_runner(monkeypatch: pytest.MonkeyPatch) -> None:
    trace = _trace([], output_text="the output")
    calls: list[tuple[str, int]] = []

    def runner(text: str, n: int) -> list[JudgeRun]:
        calls.append((text, n))
        return [JudgeRun(dimensions={"accuracy": float(i)}) for i in range(n)]

    result = run_judge_variance(
        trace, n=3, refresh=True, threshold=0.1,
        live_runner=runner, api_key="key",
    )
    assert calls == [("the output", 3)]
    assert result["source"] == "live"
    assert result["n"] == 3


def test_live_path_raises_when_api_key_missing() -> None:
    trace = _trace([])
    with pytest.raises(MissingApiKeyError):
        run_judge_variance(
            trace, n=3, refresh=True, threshold=0.1,
            live_runner=lambda _t, _n: [],
            api_key=None,
        )


def test_cached_path_returns_empty_when_no_runs() -> None:
    trace = _trace([])
    result = run_judge_variance(trace, n=5, refresh=False, threshold=0.1)
    assert result["variance"] == {}
    assert result["threshold_exceeded"] == []
    assert result["n"] == 0
```

- [ ] **Step 7.2: Run tests — expect failure**

Run: `cd backend && uv run python -m pytest tests/trace/test_judge_replay.py -v`
Expected: FAIL — `ModuleNotFoundError`.

- [ ] **Step 7.3: Implement judge_replay.py**

Write `backend/app/trace/judge_replay.py`:

```python
"""Judge variance replayer: cached path + live re-run escape hatch."""
from __future__ import annotations

from collections.abc import Callable
from statistics import pstdev

from app.trace.events import FinalOutputEvent, JudgeRun, Trace

LiveRunner = Callable[[str, int], list[JudgeRun]]


class MissingApiKeyError(RuntimeError):
    pass


def compute_variance(runs: list[JudgeRun]) -> dict[str, float]:
    if not runs:
        return {}
    dims: set[str] = set()
    for run in runs:
        dims.update(run.dimensions.keys())
    variance: dict[str, float] = {}
    for dim in dims:
        values = [r.dimensions.get(dim, 0.0) for r in runs]
        variance[dim] = pstdev(values) if len(values) > 1 else 0.0
    return variance


def run_judge_variance(
    trace: Trace,
    n: int,
    refresh: bool,
    threshold: float,
    live_runner: LiveRunner | None = None,
    api_key: str | None = None,
) -> dict[str, object]:
    if refresh:
        if api_key is None or api_key == "":
            raise MissingApiKeyError("ANTHROPIC_API_KEY required for live refresh")
        if live_runner is None:
            raise MissingApiKeyError("live_runner must be provided for refresh")
        final_event = next(
            (e for e in trace.events if isinstance(e, FinalOutputEvent)), None,
        )
        output = final_event.output_text if final_event else ""
        runs = live_runner(output, n)
        source = "live"
    else:
        runs = list(trace.judge_runs)
        source = "cached"
    variance = compute_variance(runs)
    exceeded = sorted([dim for dim, v in variance.items() if v > threshold])
    return {
        "variance": variance,
        "threshold_exceeded": exceeded,
        "n": len(runs),
        "source": source,
    }
```

- [ ] **Step 7.4: Run tests + typecheck + lint**

```bash
cd backend && uv run python -m pytest tests/trace/test_judge_replay.py -v
cd backend && uv run mypy --strict app/trace/judge_replay.py
cd backend && uv run ruff check app/trace/judge_replay.py tests/trace/test_judge_replay.py
```

- [ ] **Step 7.5: Commit**

```bash
git add backend/app/trace/judge_replay.py backend/tests/trace/test_judge_replay.py
git commit -m "feat(trace): add judge-variance replayer with cached + live paths"
```

---

## Task 8: Retention CLI

**Files:**
- Create: `backend/app/trace/retention.py`
- Create: `backend/tests/trace/test_retention.py`

- [ ] **Step 8.1: Write failing tests for retention**

Write `backend/tests/trace/test_retention.py`:

```python
from __future__ import annotations

import time
from pathlib import Path

import yaml

from app.trace.retention import delete_by_age, delete_by_grade, delete_all


def _write_trace(dir_: Path, session_id: str, grade: str | None) -> Path:
    path = dir_ / f"{session_id}.yaml"
    path.write_text(yaml.safe_dump({
        "trace_schema_version": 1,
        "summary": {
            "session_id": session_id, "started_at": "t", "ended_at": "t",
            "duration_ms": 1, "level": 3, "level_label": "x",
            "turn_count": 0, "llm_call_count": 0,
            "total_input_tokens": 0, "total_output_tokens": 0,
            "outcome": "ok", "final_grade": grade,
            "step_ids": [], "trace_mode": "always", "judge_runs_cached": 0,
        },
        "judge_runs": [],
        "events": [],
    }), encoding="utf-8")
    return path


def test_delete_all_removes_all_yaml_files(tmp_path: Path) -> None:
    _write_trace(tmp_path, "a", "F")
    _write_trace(tmp_path, "b", "A")
    (tmp_path / "notes.txt").write_text("keep")
    count = delete_all(tmp_path)
    assert count == 2
    assert not (tmp_path / "a.yaml").exists()
    assert (tmp_path / "notes.txt").exists()


def test_delete_by_grade_keeps_matching_grades(tmp_path: Path) -> None:
    _write_trace(tmp_path, "fail1", "F")
    _write_trace(tmp_path, "pass1", "A")
    _write_trace(tmp_path, "pass2", "B")
    count = delete_by_grade(tmp_path, keep_grades={"A", "B"})
    assert count == 1
    assert not (tmp_path / "fail1.yaml").exists()
    assert (tmp_path / "pass1.yaml").exists()
    assert (tmp_path / "pass2.yaml").exists()


def test_delete_by_age_removes_old_files(tmp_path: Path) -> None:
    old = _write_trace(tmp_path, "old", "F")
    fresh = _write_trace(tmp_path, "fresh", "F")
    old_time = time.time() - 60 * 60 * 24 * 60  # 60 days ago
    import os
    os.utime(old, (old_time, old_time))
    count = delete_by_age(tmp_path, older_than_days=30)
    assert count == 1
    assert not old.exists()
    assert fresh.exists()


def test_delete_all_empty_dir_returns_zero(tmp_path: Path) -> None:
    assert delete_all(tmp_path) == 0
```

- [ ] **Step 8.2: Run tests — expect failure**

Run: `cd backend && uv run python -m pytest tests/trace/test_retention.py -v`
Expected: FAIL — `ModuleNotFoundError`.

- [ ] **Step 8.3: Implement retention.py**

Write `backend/app/trace/retention.py`:

```python
"""Retention CLI: delete traces by --clear-all / --older-than / --grade.

Usage:
    python -m app.trace.retention --clear-all
    python -m app.trace.retention --older-than 30d
    python -m app.trace.retention --grade A,B        # keep A and B, delete rest
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import time
from pathlib import Path

import yaml


def delete_all(traces_dir: Path) -> int:
    if not traces_dir.exists():
        return 0
    count = 0
    for path in traces_dir.glob("*.yaml"):
        path.unlink()
        count += 1
    return count


def delete_by_age(traces_dir: Path, older_than_days: int) -> int:
    if not traces_dir.exists():
        return 0
    cutoff = time.time() - older_than_days * 86400
    count = 0
    for path in traces_dir.glob("*.yaml"):
        if path.stat().st_mtime < cutoff:
            path.unlink()
            count += 1
    return count


def delete_by_grade(traces_dir: Path, keep_grades: set[str]) -> int:
    if not traces_dir.exists():
        return 0
    count = 0
    for path in traces_dir.glob("*.yaml"):
        try:
            raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            continue
        if not isinstance(raw, dict):
            continue
        summary = raw.get("summary")
        if not isinstance(summary, dict):
            continue
        grade = summary.get("final_grade")
        if grade not in keep_grades:
            path.unlink()
            count += 1
    return count


_AGE_RE = re.compile(r"^(\d+)d$")


def _parse_age(spec: str) -> int:
    match = _AGE_RE.match(spec)
    if not match:
        raise argparse.ArgumentTypeError(f"invalid age spec: {spec}; use e.g. '30d'")
    return int(match.group(1))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="app.trace.retention")
    parser.add_argument("--clear-all", action="store_true")
    parser.add_argument("--older-than", type=_parse_age, metavar="Nd")
    parser.add_argument("--grade", type=str, help="comma-separated grades to keep")
    parser.add_argument(
        "--traces-dir",
        default=os.environ.get("TRACE_DIR", "traces"),
    )
    args = parser.parse_args(argv)

    traces_dir = Path(args.traces_dir)
    flag_count = sum(1 for f in (args.clear_all, args.older_than, args.grade) if f)
    if flag_count != 1:
        parser.error("exactly one of --clear-all / --older-than / --grade required")

    if args.clear_all:
        deleted = delete_all(traces_dir)
    elif args.older_than is not None:
        deleted = delete_by_age(traces_dir, args.older_than)
    else:
        keep = {g.strip() for g in args.grade.split(",") if g.strip()}
        deleted = delete_by_grade(traces_dir, keep)
    print(f"deleted {deleted} trace(s) from {traces_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 8.4: Run tests + typecheck + lint**

```bash
cd backend && uv run python -m pytest tests/trace/test_retention.py -v
cd backend && uv run mypy --strict app/trace/retention.py
cd backend && uv run ruff check app/trace/retention.py tests/trace/test_retention.py
```

- [ ] **Step 8.5: Commit**

```bash
git add backend/app/trace/retention.py backend/tests/trace/test_retention.py
git commit -m "feat(trace): add retention CLI with clear-all/older-than/grade flags"
```

---

## Task 9: Trace API router

**Files:**
- Create: `backend/app/api/trace_api.py`
- Modify: `backend/app/main.py` — mount the new router
- Create: `backend/tests/trace/test_trace_api.py`

- [ ] **Step 9.1: Write failing tests for trace_api**

Write `backend/tests/trace/test_trace_api.py`:

```python
from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from fastapi.testclient import TestClient

from app.main import create_app


def _trace_doc(session_id: str, grade: str | None = "F") -> dict[str, object]:
    return {
        "trace_schema_version": 1,
        "summary": {
            "session_id": session_id, "started_at": "t", "ended_at": "t",
            "duration_ms": 1, "level": 3, "level_label": "eval-level3",
            "turn_count": 1, "llm_call_count": 1,
            "total_input_tokens": 100, "total_output_tokens": 20,
            "outcome": "ok", "final_grade": grade,
            "step_ids": ["s1"], "trace_mode": "on_failure",
            "judge_runs_cached": 2,
        },
        "judge_runs": [
            {"dimensions": {"accuracy": 0.0}},
            {"dimensions": {"accuracy": 1.0}},
        ],
        "events": [
            {
                "kind": "session_start", "seq": 1, "timestamp": "t",
                "session_id": session_id, "started_at": "t",
                "level": 3, "level_label": "eval-level3", "input_query": "q",
            },
            {
                "kind": "llm_call", "seq": 2, "timestamp": "t",
                "step_id": "s1", "turn": 1, "model": "m",
                "temperature": 1.0, "max_tokens": 10, "prompt_text": "p",
                "sections": [{"source": "SYSTEM_PROMPT", "lines": "1-10", "text": "..."}],
                "response_text": "r", "tool_calls": [], "stop_reason": "end_turn",
                "input_tokens": 100, "output_tokens": 20,
                "cache_read_tokens": 0, "cache_creation_tokens": 0, "latency_ms": 0,
            },
            {
                "kind": "session_end", "seq": 3, "timestamp": "t",
                "ended_at": "t", "duration_ms": 1, "outcome": "ok", "error": None,
            },
        ],
    }


@pytest.fixture
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("TRACE_DIR", str(tmp_path))
    (tmp_path / "sess-1.yaml").write_text(
        yaml.safe_dump(_trace_doc("sess-1")), encoding="utf-8",
    )
    return TestClient(create_app())


def test_list_traces_returns_summaries(client: TestClient) -> None:
    r = client.get("/api/trace/traces")
    assert r.status_code == 200
    body = r.json()
    assert len(body["traces"]) == 1
    assert body["traces"][0]["session_id"] == "sess-1"


def test_get_trace_by_id(client: TestClient) -> None:
    r = client.get("/api/trace/traces/sess-1")
    assert r.status_code == 200
    assert r.json()["summary"]["session_id"] == "sess-1"


def test_get_trace_invalid_id_returns_400(client: TestClient) -> None:
    r = client.get("/api/trace/traces/..%2Fetc%2Fpasswd")
    assert r.status_code == 400


def test_get_trace_missing_returns_404(client: TestClient) -> None:
    r = client.get("/api/trace/traces/missing")
    assert r.status_code == 404


def test_prompt_assembly(client: TestClient) -> None:
    r = client.get("/api/trace/traces/sess-1/prompt/s1")
    assert r.status_code == 200
    body = r.json()
    assert len(body["sections"]) == 1
    assert body["sections"][0]["source"] == "SYSTEM_PROMPT"
    assert body["conflicts"] == []


def test_prompt_assembly_step_not_found_returns_404(client: TestClient) -> None:
    r = client.get("/api/trace/traces/sess-1/prompt/s99")
    assert r.status_code == 404


def test_prompt_assembly_invalid_step_id_returns_400(client: TestClient) -> None:
    r = client.get("/api/trace/traces/sess-1/prompt/notastep")
    assert r.status_code == 400


def test_timeline(client: TestClient) -> None:
    r = client.get("/api/trace/traces/sess-1/timeline")
    assert r.status_code == 200
    body = r.json()
    assert "turns" in body
    assert "events" in body


def test_judge_variance_cached(client: TestClient) -> None:
    r = client.get("/api/trace/traces/sess-1/judge-variance?refresh=0&n=5")
    assert r.status_code == 200
    body = r.json()
    assert body["source"] == "cached"
    assert "accuracy" in body["variance"]


def test_judge_variance_live_without_api_key_returns_503(
    client: TestClient, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    r = client.get("/api/trace/traces/sess-1/judge-variance?refresh=1&n=5")
    assert r.status_code == 503


def test_events_filtered_by_kind(client: TestClient) -> None:
    r = client.get("/api/trace/traces/sess-1/events?kind=llm_call")
    assert r.status_code == 200
    body = r.json()
    assert len(body["events"]) == 1
    assert body["events"][0]["kind"] == "llm_call"


def test_events_no_filter_returns_all(client: TestClient) -> None:
    r = client.get("/api/trace/traces/sess-1/events")
    assert r.status_code == 200
    assert len(r.json()["events"]) == 3
```

- [ ] **Step 9.2: Run tests — expect failure**

Run: `cd backend && uv run python -m pytest tests/trace/test_trace_api.py -v`
Expected: FAIL — `ImportError` or 404s.

- [ ] **Step 9.3: Implement trace_api.py**

Write `backend/app/api/trace_api.py`:

```python
"""REST endpoints for the trace subsystem."""
from __future__ import annotations

import os
import re
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError

from app.trace.assembler import StepNotFoundError, assemble_prompt
from app.trace.judge_replay import MissingApiKeyError, run_judge_variance
from app.trace.store import TraceNotFoundError, list_traces, load_trace
from app.trace.timeline import build_timeline

router = APIRouter(prefix="/api/trace", tags=["trace"])

_TRACE_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")
_STEP_ID_RE = re.compile(r"^s\d+$")


def _traces_dir() -> Path:
    return Path(os.environ.get("TRACE_DIR", "traces"))


def _threshold() -> float:
    return float(os.environ.get("JUDGE_VARIANCE_THRESHOLD", "0.10"))


def _validate_trace_id(trace_id: str) -> None:
    if not _TRACE_ID_RE.match(trace_id):
        raise HTTPException(status_code=400, detail="invalid trace_id")


def _validate_step_id(step_id: str) -> None:
    if not _STEP_ID_RE.match(step_id):
        raise HTTPException(status_code=400, detail="invalid step_id")


def _load_trace_or_raise(trace_id: str) -> object:
    _validate_trace_id(trace_id)
    try:
        return load_trace(_traces_dir(), trace_id)
    except TraceNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=500, detail="Failed to load trace") from exc
    except ValidationError as exc:
        raise HTTPException(status_code=500, detail="Failed to load trace") from exc


@router.get("/traces")
def list_traces_endpoint() -> dict[str, object]:
    try:
        summaries = list_traces(_traces_dir())
    except (ValueError, ValidationError) as exc:
        raise HTTPException(status_code=500, detail="Failed to list traces") from exc
    return {"traces": [s.model_dump() for s in summaries]}


@router.get("/traces/{trace_id}")
def get_trace(trace_id: str) -> dict[str, object]:
    trace = _load_trace_or_raise(trace_id)
    return trace.model_dump()  # type: ignore[attr-defined]


@router.get("/traces/{trace_id}/prompt/{step_id}")
def get_prompt_assembly(trace_id: str, step_id: str) -> dict[str, object]:
    _validate_step_id(step_id)
    trace = _load_trace_or_raise(trace_id)
    try:
        return assemble_prompt(trace, step_id)  # type: ignore[arg-type]
    except StepNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/traces/{trace_id}/timeline")
def get_timeline(trace_id: str) -> dict[str, object]:
    trace = _load_trace_or_raise(trace_id)
    return build_timeline(trace)  # type: ignore[arg-type]


@router.get("/traces/{trace_id}/judge-variance")
def get_judge_variance(
    trace_id: str,
    refresh: int = Query(default=0),
    n: int = Query(default=5, ge=1, le=20),
) -> dict[str, object]:
    trace = _load_trace_or_raise(trace_id)
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    try:
        return run_judge_variance(
            trace,  # type: ignore[arg-type]
            n=n,
            refresh=bool(refresh),
            threshold=_threshold(),
            live_runner=None,  # v1 returns 503 on refresh=1; concrete Anthropic-backed runner is follow-up work
            api_key=api_key,
        )
    except MissingApiKeyError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.get("/traces/{trace_id}/events")
def get_events(
    trace_id: str, kind: str | None = Query(default=None),
) -> dict[str, object]:
    trace = _load_trace_or_raise(trace_id)
    events = trace.events  # type: ignore[attr-defined]
    if kind is not None:
        events = [e for e in events if e.kind == kind]
    return {"events": [e.model_dump() for e in events]}
```

Modify `backend/app/main.py` — add the router import and mount:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.context_api import router as context_router
from app.api.health import router as health_router
from app.api.sop_api import router as sop_router
from app.api.trace_api import router as trace_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Analytical Agent",
        version="0.1.0",
        description="Full-stack analytical platform for MLE, data scientists, and quants",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(context_router)
    app.include_router(sop_router)
    app.include_router(trace_router)

    return app
```

- [ ] **Step 9.4: Run tests + typecheck + lint**

```bash
cd backend && uv run python -m pytest tests/trace/test_trace_api.py -v
cd backend && uv run mypy --strict app/api/trace_api.py app/main.py
cd backend && uv run ruff check app/api/trace_api.py app/main.py tests/trace/test_trace_api.py
```

- [ ] **Step 9.5: Commit**

```bash
git add backend/app/api/trace_api.py backend/app/main.py backend/tests/trace/test_trace_api.py
git commit -m "feat(trace): add /api/trace/* FastAPI router"
```

---

## Task 10: Publish helpers + context manager hook

**Files:**
- Create: `backend/app/trace/publishers.py`
- Create: `backend/tests/trace/test_publishers.py`
- Modify: `backend/app/context/manager.py` — emit `CompactionEvent` from `record_compaction`

- [ ] **Step 10.1: Write failing tests for publishers**

Write `backend/tests/trace/test_publishers.py`:

```python
from __future__ import annotations

from pathlib import Path

import pytest

from app.trace import bus
from app.trace.events import (
    CompactionEvent,
    LlmCallEvent,
    PromptSection,
    ScratchpadWriteEvent,
    SessionStartEvent,
    ToolCallEvent,
)
from app.trace.publishers import (
    TraceSession,
    publish_compaction,
    publish_final_output,
    publish_llm_call,
    publish_scratchpad_write,
    publish_session_end,
    publish_session_start,
    publish_tool_call,
)


@pytest.fixture(autouse=True)
def _reset_bus() -> None:
    bus.reset()


def test_publish_session_start() -> None:
    received: list[object] = []
    bus.subscribe(received.append)
    publish_session_start(
        session_id="sess", started_at="t",
        level=3, level_label="eval-level3", input_query="q",
    )
    assert len(received) == 1
    assert isinstance(received[0], SessionStartEvent)


def test_publish_llm_call() -> None:
    received: list[object] = []
    bus.subscribe(received.append)
    publish_llm_call(
        step_id="s1", turn=1, model="m", temperature=1.0,
        max_tokens=10, prompt_text="p",
        sections=[PromptSection(source="x", lines="1-10", text="...")],
        response_text="r", tool_calls=[], stop_reason="end_turn",
        input_tokens=100, output_tokens=20,
        cache_read_tokens=0, cache_creation_tokens=0, latency_ms=50,
    )
    assert isinstance(received[0], LlmCallEvent)
    assert received[0].step_id == "s1"


def test_publish_tool_call() -> None:
    received: list[object] = []
    bus.subscribe(received.append)
    publish_tool_call(
        turn=1, tool_name="t", tool_input={"a": 1},
        tool_output="y", duration_ms=10, error=None,
    )
    assert isinstance(received[0], ToolCallEvent)


def test_publish_compaction() -> None:
    received: list[object] = []
    bus.subscribe(received.append)
    publish_compaction(
        turn=1, before_token_count=1000, after_token_count=500,
        dropped_layers=["a"], kept_layers=["b"],
    )
    assert isinstance(received[0], CompactionEvent)


def test_publish_scratchpad_write() -> None:
    received: list[object] = []
    bus.subscribe(received.append)
    publish_scratchpad_write(turn=1, key="k", value_preview="v")
    assert isinstance(received[0], ScratchpadWriteEvent)


def test_trace_session_context_publishes_start_and_end(tmp_path: Path) -> None:
    received: list[object] = []
    bus.subscribe(received.append)
    with TraceSession(
        session_id="sess", level=3, level_label="eval-level3",
        input_query="q", trace_mode="always", output_dir=tmp_path,
    ) as session:
        publish_final_output(
            output_text="out", final_grade="A", judge_dimensions={"a": 1.0},
        )
        session.set_final_grade("A")
    kinds = [e.kind for e in received]
    assert kinds[0] == "session_start"
    assert "final_output" in kinds
    assert kinds[-1] == "session_end"


def test_trace_session_writes_trace_file_when_always(tmp_path: Path) -> None:
    with TraceSession(
        session_id="sess-w", level=3, level_label="eval-level3",
        input_query="q", trace_mode="always", output_dir=tmp_path,
    ) as session:
        publish_final_output(
            output_text="out", final_grade="F", judge_dimensions={},
        )
        session.set_final_grade("F")
    assert (tmp_path / "sess-w.yaml").exists()


def test_trace_session_skips_write_on_failure_mode_when_grade_passes(
    tmp_path: Path,
) -> None:
    with TraceSession(
        session_id="sess-s", level=3, level_label="eval-level3",
        input_query="q", trace_mode="on_failure", output_dir=tmp_path,
    ) as session:
        publish_final_output(
            output_text="out", final_grade="A", judge_dimensions={},
        )
        session.set_final_grade("A")
    assert not (tmp_path / "sess-s.yaml").exists()
```

- [ ] **Step 10.2: Run tests — expect failure**

Run: `cd backend && uv run python -m pytest tests/trace/test_publishers.py -v`
Expected: FAIL — `ModuleNotFoundError`.

- [ ] **Step 10.3: Implement publishers.py**

Write `backend/app/trace/publishers.py`:

```python
"""Typed publish helpers + TraceSession context manager.

Agent code uses these instead of constructing event objects directly.
The bus assigns seq at publish time; callers pass seq=0 as a placeholder.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from types import TracebackType

from app.trace import bus
from app.trace.events import (
    CompactionEvent,
    FinalOutputEvent,
    Grade,
    LlmCallEvent,
    PromptSection,
    ScratchpadWriteEvent,
    SessionEndEvent,
    SessionStartEvent,
    ToolCallEvent,
)
from app.trace.recorder import JudgeRunner, TraceRecorder


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def publish_session_start(
    session_id: str, started_at: str, level: int,
    level_label: str, input_query: str,
) -> None:
    bus.publish(SessionStartEvent(
        seq=0, timestamp=_now(),
        session_id=session_id, started_at=started_at,
        level=level, level_label=level_label, input_query=input_query,
    ))


def publish_llm_call(
    step_id: str, turn: int, model: str, temperature: float,
    max_tokens: int, prompt_text: str, sections: list[PromptSection],
    response_text: str, tool_calls: list[dict[str, object]],
    stop_reason: str, input_tokens: int, output_tokens: int,
    cache_read_tokens: int, cache_creation_tokens: int, latency_ms: int,
) -> None:
    bus.publish(LlmCallEvent(
        seq=0, timestamp=_now(), step_id=step_id, turn=turn,
        model=model, temperature=temperature, max_tokens=max_tokens,
        prompt_text=prompt_text, sections=sections,
        response_text=response_text, tool_calls=tool_calls,
        stop_reason=stop_reason, input_tokens=input_tokens,
        output_tokens=output_tokens, cache_read_tokens=cache_read_tokens,
        cache_creation_tokens=cache_creation_tokens, latency_ms=latency_ms,
    ))


def publish_tool_call(
    turn: int, tool_name: str, tool_input: dict[str, object],
    tool_output: str, duration_ms: int, error: str | None,
) -> None:
    bus.publish(ToolCallEvent(
        seq=0, timestamp=_now(), turn=turn, tool_name=tool_name,
        tool_input=tool_input, tool_output=tool_output,
        duration_ms=duration_ms, error=error,
    ))


def publish_compaction(
    turn: int, before_token_count: int, after_token_count: int,
    dropped_layers: list[str], kept_layers: list[str],
) -> None:
    bus.publish(CompactionEvent(
        seq=0, timestamp=_now(), turn=turn,
        before_token_count=before_token_count,
        after_token_count=after_token_count,
        dropped_layers=dropped_layers, kept_layers=kept_layers,
    ))


def publish_scratchpad_write(turn: int, key: str, value_preview: str) -> None:
    bus.publish(ScratchpadWriteEvent(
        seq=0, timestamp=_now(), turn=turn,
        key=key, value_preview=value_preview,
    ))


def publish_final_output(
    output_text: str, final_grade: Grade | None,
    judge_dimensions: dict[str, float],
) -> None:
    bus.publish(FinalOutputEvent(
        seq=0, timestamp=_now(), output_text=output_text,
        final_grade=final_grade, judge_dimensions=judge_dimensions,
    ))


def publish_session_end(
    ended_at: str, duration_ms: int,
    outcome: str, error: str | None,
) -> None:
    bus.publish(SessionEndEvent(
        seq=0, timestamp=_now(), ended_at=ended_at,
        duration_ms=duration_ms,
        outcome=outcome,  # type: ignore[arg-type]
        error=error,
    ))


class TraceSession:
    """Context manager that wires a recorder to the bus and finalizes on exit."""

    def __init__(
        self,
        session_id: str,
        level: int,
        level_label: str,
        input_query: str,
        trace_mode: str,
        output_dir: Path,
        judge_runner: JudgeRunner | None = None,
    ) -> None:
        self._session_id = session_id
        self._level = level
        self._level_label = level_label
        self._input_query = input_query
        self._trace_mode = trace_mode
        self._output_dir = output_dir
        self._judge_runner = judge_runner
        self._final_grade: Grade | None = None
        self._started_at: str = ""
        self._recorder: TraceRecorder | None = None

    def set_final_grade(self, grade: Grade | None) -> None:
        self._final_grade = grade

    def __enter__(self) -> TraceSession:
        self._recorder = TraceRecorder(
            session_id=self._session_id,
            trace_mode=self._trace_mode,
            output_dir=self._output_dir,
            judge_runner=self._judge_runner,
        )
        bus.subscribe(self._recorder.on_event)
        self._started_at = _now()
        publish_session_start(
            session_id=self._session_id,
            started_at=self._started_at,
            level=self._level,
            level_label=self._level_label,
            input_query=self._input_query,
        )
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None,
        exc: BaseException | None, tb: TracebackType | None,
    ) -> None:
        outcome = "ok" if exc is None else "error"
        error = None if exc is None else str(exc)
        ended_at = _now()
        publish_session_end(
            ended_at=ended_at, duration_ms=0, outcome=outcome, error=error,
        )
        if self._recorder is not None:
            self._recorder.finalize(self._final_grade)
```

- [ ] **Step 10.4: Modify `backend/app/context/manager.py` — emit `CompactionEvent` from `record_compaction`**

Find the `record_compaction` method (current lines 82-98) and modify it to also publish the event. The updated method:

```python
    def record_compaction(
        self,
        tokens_before: int,
        tokens_after: int,
        removed: list[dict[str, Any]],
        survived: list[str],
    ) -> None:
        self._compaction_history.append({
            "id": len(self._compaction_history) + 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tokens_before": tokens_before,
            "tokens_after": tokens_after,
            "tokens_freed": tokens_before - tokens_after,
            "trigger_utilization": round(tokens_before / self._max_tokens, 4),
            "removed": removed,
            "survived": survived,
        })
        from app.trace.publishers import publish_compaction
        dropped_names = [r.get("name", "") for r in removed if isinstance(r, dict)]
        publish_compaction(
            turn=self._current_turn(),
            before_token_count=tokens_before,
            after_token_count=tokens_after,
            dropped_layers=[str(n) for n in dropped_names],
            kept_layers=survived,
        )
```

And add the `_current_turn` helper and the instance attribute to track it. Near the top of `__init__`, add:

```python
        self._turn: int = 0
```

And add this method at the end of the class (before the final newline):

```python
    def set_turn(self, turn: int) -> None:
        self._turn = turn

    def _current_turn(self) -> int:
        return self._turn
```

The import for `publish_compaction` is local inside `record_compaction` to avoid a circular-import risk between the trace package and context manager.

- [ ] **Step 10.5: Add test for context manager → bus emission**

Append to `backend/tests/trace/test_publishers.py`:

```python
def test_context_manager_record_compaction_emits_event(tmp_path: Path) -> None:
    from app.context.manager import ContextManager
    received: list[object] = []
    bus.subscribe(received.append)
    cm = ContextManager()
    cm.set_turn(3)
    cm.record_compaction(
        tokens_before=1000, tokens_after=400,
        removed=[{"name": "layer_a", "tokens": 300},
                 {"name": "layer_b", "tokens": 300}],
        survived=["layer_c"],
    )
    compactions = [e for e in received if isinstance(e, CompactionEvent)]
    assert len(compactions) == 1
    assert compactions[0].turn == 3
    assert compactions[0].before_token_count == 1000
    assert compactions[0].after_token_count == 400
    assert compactions[0].dropped_layers == ["layer_a", "layer_b"]
    assert compactions[0].kept_layers == ["layer_c"]
```

- [ ] **Step 10.6: Run tests + typecheck + lint**

```bash
cd backend && uv run python -m pytest tests/trace/test_publishers.py -v
cd backend && uv run mypy --strict app/trace/publishers.py app/context/manager.py
cd backend && uv run ruff check app/trace/publishers.py app/context/manager.py tests/trace/test_publishers.py
```

- [ ] **Step 10.7: Commit**

```bash
git add backend/app/trace/publishers.py backend/app/context/manager.py backend/tests/trace/test_publishers.py
git commit -m "feat(trace): add publisher helpers, TraceSession, and context manager hook"
```

---

## Task 11: SOP integration — `trace_id` + forwarding shims

**Files:**
- Modify: `backend/app/sop/types.py` — add `trace_id: str | None = None` to `SOPSession`
- Modify: `backend/app/api/sop_api.py` — replace the three stub handlers with shims
- Modify: `backend/tests/sop/` — update any test that constructs `SOPSession`

- [ ] **Step 11.1: Locate SOPSession + existing test usages**

Run:

```bash
cd backend && uv run python -m pytest tests/sop -v --co -q | head -20
```

Search for `SOPSession(` in tests to find construction sites:

```bash
grep -rn "SOPSession(" backend/tests/sop
```

Each existing call site must still pass (the new field has a default, so no change needed, but verify no tests pin `model_fields` count).

- [ ] **Step 11.2: Write failing test for trace_id in SOPSession**

Append to `backend/tests/sop/test_types.py` (create the file if it doesn't exist):

```python
from __future__ import annotations

from app.sop.types import SOPSession  # type: ignore[attr-defined]


def test_sop_session_has_nullable_trace_id() -> None:
    fields = SOPSession.model_fields
    assert "trace_id" in fields
    assert fields["trace_id"].default is None
```

If `test_types.py` already exists, add the test case but keep existing tests unchanged.

- [ ] **Step 11.3: Write failing test for shim forwarding**

Write `backend/tests/sop/test_sop_api_shims.py` (create new):

```python
from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from fastapi.testclient import TestClient

from app.main import create_app


def _trace_doc(session_id: str) -> dict[str, object]:
    return {
        "trace_schema_version": 1,
        "summary": {
            "session_id": session_id, "started_at": "t", "ended_at": "t",
            "duration_ms": 1, "level": 3, "level_label": "eval-level3",
            "turn_count": 0, "llm_call_count": 0,
            "total_input_tokens": 0, "total_output_tokens": 0,
            "outcome": "ok", "final_grade": "F",
            "step_ids": [], "trace_mode": "on_failure", "judge_runs_cached": 1,
        },
        "judge_runs": [{"dimensions": {"accuracy": 0.5}}],
        "events": [
            {
                "kind": "session_start", "seq": 1, "timestamp": "t",
                "session_id": session_id, "started_at": "t",
                "level": 3, "level_label": "eval-level3", "input_query": "q",
            },
        ],
    }


@pytest.fixture
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("TRACE_DIR", str(tmp_path))
    (tmp_path / "sess-1.yaml").write_text(
        yaml.safe_dump(_trace_doc("sess-1")), encoding="utf-8",
    )
    return TestClient(create_app())


def test_legacy_judge_variance_shim_delegates_to_trace(client: TestClient) -> None:
    r = client.get("/api/sop/judge-variance/sess-1")
    assert r.status_code == 200
    body = r.json()
    assert "variance" in body
    assert "threshold_exceeded" in body


def test_legacy_prompt_assembly_shim_returns_empty_sections_on_missing_step(
    client: TestClient,
) -> None:
    r = client.get("/api/sop/prompt-assembly/sess-1/s99")
    assert r.status_code == 200
    body = r.json()
    assert body["sections"] == []


def test_legacy_timeline_shim_delegates_to_trace(client: TestClient) -> None:
    r = client.get("/api/sop/timeline/sess-1")
    assert r.status_code == 200
    body = r.json()
    assert "turns" in body
    assert "events" in body
```

- [ ] **Step 11.4: Modify `backend/app/sop/types.py` — add `trace_id`**

Find the `SOPSession` class and add the field. The exact addition (next to existing optional fields):

```python
    trace_id: str | None = None
```

Place it after `session_id` to keep related identifiers together.

- [ ] **Step 11.5: Rewrite the three shim handlers in `backend/app/api/sop_api.py`**

Replace the `judge_variance`, `prompt_assembly`, and `timeline` handlers (current lines 62-96) with forwarding shims:

```python
from app.api.trace_api import (
    get_judge_variance as _get_judge_variance,
    get_prompt_assembly as _get_prompt_assembly,
    get_timeline as _get_timeline,
)


@router.get("/judge-variance/{trace_id}")
def judge_variance(trace_id: str, n: int = 5) -> dict[str, object]:
    return _get_judge_variance(trace_id=trace_id, refresh=0, n=n)


@router.get("/prompt-assembly/{trace_id}/{step_id}")
def prompt_assembly(trace_id: str, step_id: str) -> dict[str, object]:
    try:
        return _get_prompt_assembly(trace_id=trace_id, step_id=step_id)
    except HTTPException as exc:
        if exc.status_code == 404:
            # Legacy shape returned empty sections for missing step — preserve that.
            return {"sections": [], "conflicts": []}
        raise
```

Keep `timeline`:

```python
@router.get("/timeline/{trace_id}")
def timeline(trace_id: str) -> dict[str, object]:
    return _get_timeline(trace_id=trace_id)
```

Remove the now-unused `load_prompt_assembly`, `load_timeline`, and `compute_judge_variance` imports or references (check `from app.sop.preflight import JUDGE_VARIANCE_THRESHOLD` — still used elsewhere, keep it only if referenced; otherwise remove the import).

- [ ] **Step 11.6: Run tests + typecheck + lint**

```bash
cd backend && uv run python -m pytest tests/sop tests/trace -v
cd backend && uv run mypy --strict app/sop/types.py app/api/sop_api.py
cd backend && uv run ruff check app/sop/types.py app/api/sop_api.py tests/sop/test_types.py tests/sop/test_sop_api_shims.py
```

- [ ] **Step 11.7: Commit**

```bash
git add backend/app/sop/types.py backend/app/api/sop_api.py backend/tests/sop/test_types.py backend/tests/sop/test_sop_api_shims.py
git commit -m "feat(sop): link SOPSession to trace via trace_id and add API shims"
```

---

## Task 12: Integration test (synthetic agent run → trace round-trip)

**Files:**
- Create: `backend/tests/trace/test_integration.py`

- [ ] **Step 12.1: Write failing integration test**

Write `backend/tests/trace/test_integration.py`:

```python
from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from fastapi.testclient import TestClient

from app.main import create_app
from app.trace import bus
from app.trace.events import JudgeRun, PromptSection
from app.trace.publishers import (
    TraceSession,
    publish_compaction,
    publish_final_output,
    publish_llm_call,
    publish_scratchpad_write,
    publish_tool_call,
)


@pytest.fixture(autouse=True)
def _reset_bus() -> None:
    bus.reset()


def _judge_runner(_text: str, n: int) -> list[JudgeRun]:
    return [
        JudgeRun(dimensions={"accuracy": float(i) / max(n - 1, 1)})
        for i in range(n)
    ]


def test_synthetic_agent_run_produces_readable_trace(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("TRACE_DIR", str(tmp_path))

    with TraceSession(
        session_id="sess-int", level=3, level_label="eval-level3",
        input_query="q", trace_mode="always",
        output_dir=tmp_path, judge_runner=_judge_runner,
    ) as session:
        publish_llm_call(
            step_id="s1", turn=1, model="claude-opus-4-6",
            temperature=1.0, max_tokens=4096, prompt_text="prompt 1",
            sections=[
                PromptSection(source="SYSTEM_PROMPT", lines="1-50", text="..."),
                PromptSection(source="user_query", lines="51-52", text="..."),
            ],
            response_text="use a tool", tool_calls=[{"name": "read_file"}],
            stop_reason="tool_use", input_tokens=500, output_tokens=50,
            cache_read_tokens=0, cache_creation_tokens=0, latency_ms=120,
        )
        publish_tool_call(
            turn=1, tool_name="read_file",
            tool_input={"path": "/x"}, tool_output="content",
            duration_ms=10, error=None,
        )
        publish_compaction(
            turn=1, before_token_count=2000, after_token_count=1500,
            dropped_layers=["old_context"], kept_layers=["system", "task"],
        )
        publish_scratchpad_write(turn=1, key="findings", value_preview="...")
        publish_llm_call(
            step_id="s2", turn=2, model="claude-opus-4-6",
            temperature=1.0, max_tokens=4096, prompt_text="prompt 2",
            sections=[PromptSection(source="SYSTEM_PROMPT", lines="1-50", text="...")],
            response_text="done", tool_calls=[], stop_reason="end_turn",
            input_tokens=1500, output_tokens=100,
            cache_read_tokens=0, cache_creation_tokens=0, latency_ms=150,
        )
        publish_final_output(
            output_text="final answer", final_grade="F",
            judge_dimensions={"accuracy": 0.5},
        )
        session.set_final_grade("F")

    trace_path = tmp_path / "sess-int.yaml"
    assert trace_path.exists()

    data = yaml.safe_load(trace_path.read_text())
    assert data["trace_schema_version"] == 1
    assert data["summary"]["llm_call_count"] == 2
    assert data["summary"]["step_ids"] == ["s1", "s2"]
    assert data["summary"]["turn_count"] == 2
    assert data["summary"]["final_grade"] == "F"
    assert len(data["judge_runs"]) == 5

    client = TestClient(create_app())

    r = client.get("/api/trace/traces")
    assert r.status_code == 200
    assert any(t["session_id"] == "sess-int" for t in r.json()["traces"])

    r = client.get("/api/trace/traces/sess-int/prompt/s1")
    assert r.status_code == 200
    body = r.json()
    assert len(body["sections"]) == 2

    r = client.get("/api/trace/traces/sess-int/timeline")
    assert r.status_code == 200
    body = r.json()
    assert len(body["turns"]) == 2

    r = client.get("/api/trace/traces/sess-int/judge-variance?refresh=0")
    assert r.status_code == 200
    body = r.json()
    assert body["source"] == "cached"
    assert "accuracy" in body["variance"]
```

- [ ] **Step 12.2: Run test — expect initial pass (if all earlier tasks are green)**

```bash
cd backend && uv run python -m pytest tests/trace/test_integration.py -v
```

If failures: fix the wiring, do not weaken the test.

- [ ] **Step 12.3: Typecheck + lint**

```bash
cd backend && uv run mypy --strict tests/trace/test_integration.py
cd backend && uv run ruff check tests/trace/test_integration.py
```

- [ ] **Step 12.4: Commit**

```bash
git add backend/tests/trace/test_integration.py
git commit -m "test(trace): add synthetic agent run integration test"
```

---

## Task 13: Config, Makefile, .gitignore

**Files:**
- Modify: `.env.example`
- Modify: `Makefile`
- Modify: `.gitignore`

- [ ] **Step 13.1: Add env vars to `.env.example`**

Read the existing file, then append at the end (preserve everything above):

```
# Trace subsystem
TRACE_ENABLED=1
TRACE_MODE=on_failure
TRACE_DIR=traces
TRACE_MAX_EVENT_SIZE_BYTES=10240
JUDGE_VARIANCE_THRESHOLD=0.10
JUDGE_VARIANCE_N=5
```

If `.env.example` does not exist, create it with only the above lines.

- [ ] **Step 13.2: Add `traces/` to `.gitignore`**

Append to `.gitignore`:

```
traces/
```

Run `git status` first to confirm the path is not already ignored.

- [ ] **Step 13.3: Add `eval-trace` and `clean-traces` to Makefile**

Open the root `Makefile`. Add `eval-trace` and `clean-traces` to `.PHONY`, then add the targets after the existing `eval` target (or near `sop` if present):

```makefile
eval-trace:
	TRACE_MODE=always $(MAKE) eval

clean-traces:
	cd backend && uv run python -m app.trace.retention --clear-all
```

If the `eval` target doesn't exist yet, still add `eval-trace` so the target name is documented; `make eval-trace` will fall through to the existing eval-framework targets that are expected to be in a separate plan.

- [ ] **Step 13.4: Verify make targets parse**

```bash
make -n eval-trace
make -n clean-traces
```

Expected: commands print without errors (dry-run mode). No actual deletion.

- [ ] **Step 13.5: Commit**

```bash
git add .env.example .gitignore Makefile
git commit -m "chore(trace): add env vars, ignore traces dir, and make targets"
```

---

## Task 14: Frontend devtools store — selection state

**Files:**
- Modify: `frontend/src/stores/devtools.ts`
- Create: `frontend/src/stores/__tests__/devtools.test.ts`

- [ ] **Step 14.1: Write failing test for store selection state**

Write `frontend/src/stores/__tests__/devtools.test.ts`:

```ts
import { beforeEach, describe, expect, it } from 'vitest'
import { useDevtoolsStore } from '../devtools'

describe('devtools store selection', () => {
  beforeEach(() => {
    useDevtoolsStore.setState({
      selectedTraceId: null,
      selectedStepId: null,
    })
  })

  it('setSelectedTrace updates traceId and clears stepId', () => {
    useDevtoolsStore.setState({ selectedStepId: 's3' })
    useDevtoolsStore.getState().setSelectedTrace('trace-abc')
    const s = useDevtoolsStore.getState()
    expect(s.selectedTraceId).toBe('trace-abc')
    expect(s.selectedStepId).toBeNull()
  })

  it('setSelectedTrace(null) clears both', () => {
    useDevtoolsStore.setState({ selectedTraceId: 'x', selectedStepId: 's1' })
    useDevtoolsStore.getState().setSelectedTrace(null)
    const s = useDevtoolsStore.getState()
    expect(s.selectedTraceId).toBeNull()
    expect(s.selectedStepId).toBeNull()
  })

  it('setSelectedStep updates stepId without touching traceId', () => {
    useDevtoolsStore.setState({ selectedTraceId: 'trace-xyz' })
    useDevtoolsStore.getState().setSelectedStep('s2')
    const s = useDevtoolsStore.getState()
    expect(s.selectedTraceId).toBe('trace-xyz')
    expect(s.selectedStepId).toBe('s2')
  })
})
```

- [ ] **Step 14.2: Run test — expect failure**

```bash
cd frontend && npm test -- --run src/stores/__tests__/devtools.test.ts
```

Expected: FAIL — `setSelectedTrace is not a function`.

- [ ] **Step 14.3: Modify `frontend/src/stores/devtools.ts`**

Overwrite to:

```ts
import { create } from 'zustand'
import type { ContextSnapshot } from '../lib/api'

interface DevtoolsState {
  isOpen: boolean
  activeTab: 'events' | 'skills' | 'config' | 'wiki' | 'evals' | 'context'
          | 'sop-sessions' | 'sop-judge' | 'sop-prompt' | 'sop-timeline'
  contextSnapshot: ContextSnapshot | null
  selectedTraceId: string | null
  selectedStepId: string | null
  toggle: () => void
  setActiveTab: (tab: DevtoolsState['activeTab']) => void
  setContextSnapshot: (snapshot: ContextSnapshot) => void
  setSelectedTrace: (traceId: string | null) => void
  setSelectedStep: (stepId: string | null) => void
}

export const useDevtoolsStore = create<DevtoolsState>((set) => ({
  isOpen: false,
  activeTab: 'context',
  contextSnapshot: null,
  selectedTraceId: null,
  selectedStepId: null,
  toggle: () => set((s) => ({ isOpen: !s.isOpen })),
  setActiveTab: (tab) => set({ activeTab: tab }),
  setContextSnapshot: (snapshot) => set({ contextSnapshot: snapshot }),
  setSelectedTrace: (traceId) =>
    set({ selectedTraceId: traceId, selectedStepId: null }),
  setSelectedStep: (stepId) => set({ selectedStepId: stepId }),
}))
```

- [ ] **Step 14.4: Run tests + typecheck**

```bash
cd frontend && npm test -- --run src/stores/__tests__/devtools.test.ts
cd frontend && npx tsc --noEmit --pretty false
```

- [ ] **Step 14.5: Commit**

```bash
git add frontend/src/stores/devtools.ts frontend/src/stores/__tests__/devtools.test.ts
git commit -m "feat(devtools): add selection state to devtools store"
```

---

## Task 15: URL sync hook

**Files:**
- Create: `frontend/src/devtools/sop/useSelectionUrlSync.ts`
- Create: `frontend/src/devtools/sop/__tests__/useSelectionUrlSync.test.ts`

- [ ] **Step 15.1: Write failing test for URL sync hook**

Write `frontend/src/devtools/sop/__tests__/useSelectionUrlSync.test.ts`:

```ts
import { renderHook, act } from '@testing-library/react'
import { beforeEach, describe, expect, it } from 'vitest'
import { useDevtoolsStore } from '../../../stores/devtools'
import { useSelectionUrlSync } from '../useSelectionUrlSync'

describe('useSelectionUrlSync', () => {
  beforeEach(() => {
    window.history.replaceState(null, '', '/')
    useDevtoolsStore.setState({
      selectedTraceId: null,
      selectedStepId: null,
    })
  })

  it('reads ?trace= and ?step= from URL on mount', () => {
    window.history.replaceState(null, '', '/?trace=trace-1&step=s2')
    renderHook(() => useSelectionUrlSync())
    const s = useDevtoolsStore.getState()
    expect(s.selectedTraceId).toBe('trace-1')
    expect(s.selectedStepId).toBe('s2')
  })

  it('writes selection back to URL when store changes', () => {
    renderHook(() => useSelectionUrlSync())
    act(() => {
      useDevtoolsStore.getState().setSelectedTrace('trace-xyz')
    })
    expect(window.location.search).toContain('trace=trace-xyz')
  })

  it('clears query params when trace is cleared', () => {
    window.history.replaceState(null, '', '/?trace=old&step=s1')
    renderHook(() => useSelectionUrlSync())
    act(() => {
      useDevtoolsStore.getState().setSelectedTrace(null)
    })
    expect(window.location.search).not.toContain('trace=')
    expect(window.location.search).not.toContain('step=')
  })

  it('uses replaceState (not pushState) so history does not grow', () => {
    const historyLengthBefore = window.history.length
    renderHook(() => useSelectionUrlSync())
    act(() => {
      useDevtoolsStore.getState().setSelectedTrace('t1')
      useDevtoolsStore.getState().setSelectedTrace('t2')
      useDevtoolsStore.getState().setSelectedTrace('t3')
    })
    expect(window.history.length).toBe(historyLengthBefore)
  })
})
```

- [ ] **Step 15.2: Run test — expect failure**

```bash
cd frontend && npm test -- --run src/devtools/sop/__tests__/useSelectionUrlSync.test.ts
```

Expected: FAIL — module not found.

- [ ] **Step 15.3: Implement useSelectionUrlSync.ts**

Write `frontend/src/devtools/sop/useSelectionUrlSync.ts`:

```ts
import { useEffect } from 'react'
import { useDevtoolsStore } from '../../stores/devtools'

export function useSelectionUrlSync(): void {
  const selectedTraceId = useDevtoolsStore((s) => s.selectedTraceId)
  const selectedStepId = useDevtoolsStore((s) => s.selectedStepId)
  const setSelectedTrace = useDevtoolsStore((s) => s.setSelectedTrace)
  const setSelectedStep = useDevtoolsStore((s) => s.setSelectedStep)

  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    const trace = params.get('trace')
    const step = params.get('step')
    if (trace) {
      setSelectedTrace(trace)
      if (step) setSelectedStep(step)
    }
  }, [setSelectedTrace, setSelectedStep])

  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    if (selectedTraceId) {
      params.set('trace', selectedTraceId)
    } else {
      params.delete('trace')
    }
    if (selectedStepId) {
      params.set('step', selectedStepId)
    } else {
      params.delete('step')
    }
    const search = params.toString()
    const newUrl =
      window.location.pathname + (search ? `?${search}` : '') + window.location.hash
    window.history.replaceState(null, '', newUrl)
  }, [selectedTraceId, selectedStepId])
}
```

- [ ] **Step 15.4: Run tests + typecheck**

```bash
cd frontend && npm test -- --run src/devtools/sop/__tests__/useSelectionUrlSync.test.ts
cd frontend && npx tsc --noEmit --pretty false
```

- [ ] **Step 15.5: Commit**

```bash
git add frontend/src/devtools/sop/useSelectionUrlSync.ts frontend/src/devtools/sop/__tests__/useSelectionUrlSync.test.ts
git commit -m "feat(devtools): add useSelectionUrlSync hook with replaceState"
```

---

## Task 16: Frontend api.ts — swap to `/api/trace/*`

**Files:**
- Modify: `frontend/src/devtools/sop/api.ts`

- [ ] **Step 16.1: Read the existing api.ts to know its shape**

```bash
cat frontend/src/devtools/sop/api.ts
```

Expected: three functions (`fetchJudgeVariance`, `fetchPromptAssembly`, `fetchTimeline`) pointing at `/api/sop/*`.

- [ ] **Step 16.2: Update api.ts to hit `/api/trace/*`**

Overwrite `frontend/src/devtools/sop/api.ts` (preserving any existing types that are correct — `SOPSession`, `Grade`, `PreflightVerdict` stay):

```ts
export type Grade = 'A' | 'B' | 'C' | 'F'
export type PreflightVerdict = 'pass' | 'fail' | 'skipped'

export interface SOPSession {
  session_id: string
  date: string
  level: number
  overall_grade_before: Grade | null
  preflight: { verdict: PreflightVerdict }
  triage: { bucket: string | null }
  fix: { name: string | null; evidence: string | null }
  outcome: { grade_after: Grade | null }
  trace_links: { trace_id: string | null }
}

export async function listSessions(): Promise<SOPSession[]> {
  const r = await fetch('/api/sop/sessions')
  if (!r.ok) throw new Error(`listSessions failed: ${r.status}`)
  const body = (await r.json()) as { sessions: SOPSession[] }
  return body.sessions
}

export interface JudgeVarianceResponse {
  variance: Record<string, number>
  threshold_exceeded: string[]
  n?: number
  source?: 'cached' | 'live'
}

export async function fetchJudgeVariance(
  traceId: string,
  n = 5,
): Promise<JudgeVarianceResponse> {
  const r = await fetch(
    `/api/trace/traces/${encodeURIComponent(traceId)}/judge-variance?refresh=0&n=${n}`,
  )
  if (!r.ok) throw new Error(`fetchJudgeVariance failed: ${r.status}`)
  return (await r.json()) as JudgeVarianceResponse
}

export interface PromptSection {
  source: string
  lines: string
  text: string
}

export interface PromptConflict {
  source_a: string
  source_b: string
  overlap: string
}

export interface PromptAssembly {
  sections: PromptSection[]
  conflicts: PromptConflict[]
}

export async function fetchPromptAssembly(
  traceId: string,
  stepId: string,
): Promise<PromptAssembly> {
  const r = await fetch(
    `/api/trace/traces/${encodeURIComponent(traceId)}/prompt/${encodeURIComponent(stepId)}`,
  )
  if (!r.ok) throw new Error(`fetchPromptAssembly failed: ${r.status}`)
  return (await r.json()) as PromptAssembly
}

export interface TimelineTurn {
  turn: number
  layers: Record<string, number>
}

export interface TimelineEvent {
  turn: number
  kind: string
  detail: string
}

export interface Timeline {
  turns: TimelineTurn[]
  events: TimelineEvent[]
}

export async function fetchTimeline(traceId: string): Promise<Timeline> {
  const r = await fetch(
    `/api/trace/traces/${encodeURIComponent(traceId)}/timeline`,
  )
  if (!r.ok) throw new Error(`fetchTimeline failed: ${r.status}`)
  return (await r.json()) as Timeline
}

export interface TraceSummary {
  session_id: string
  level: number
  outcome: string
  final_grade: Grade | null
  turn_count: number
  llm_call_count: number
  step_ids: string[]
}

export async function fetchTraceSummary(traceId: string): Promise<TraceSummary> {
  const r = await fetch(`/api/trace/traces/${encodeURIComponent(traceId)}`)
  if (!r.ok) throw new Error(`fetchTraceSummary failed: ${r.status}`)
  const body = (await r.json()) as { summary: TraceSummary }
  return body.summary
}
```

Notes:
- `listSessions` still points at `/api/sop/sessions` — that endpoint is not part of the trace subsystem.
- `fetchTraceSummary` is new; used by `PromptInspector` to populate the step dropdown.
- Frontend component tests that mocked `/api/sop/judge-variance/...`, `/api/sop/prompt-assembly/...`, and `/api/sop/timeline/...` are rewritten against the new `/api/trace/*` URLs in Tasks 17, 18, and 19 respectively. Backend tests for the SOP shims are added in Task 11 and exercise the legacy URLs end-to-end.

- [ ] **Step 16.3: Typecheck**

```bash
cd frontend && npx tsc --noEmit --pretty false
```

Expected: PASS. If a component file fails because an unused type was removed, fix it in the next tasks.

- [ ] **Step 16.4: Commit**

```bash
git add frontend/src/devtools/sop/api.ts
git commit -m "feat(devtools): flip api.ts endpoints to /api/trace/*"
```

---

## Task 17: SessionReplay — row click + selection highlight

**Files:**
- Modify: `frontend/src/devtools/sop/SessionReplay.tsx`
- Modify: `frontend/src/devtools/sop/SessionReplay.test.tsx`

- [ ] **Step 17.1: Read the current SessionReplay.tsx**

```bash
cat frontend/src/devtools/sop/SessionReplay.tsx
```

- [ ] **Step 17.2: Add failing test for row click → store update**

Append the following `it(...)` blocks into the existing `describe(...)` in `frontend/src/devtools/sop/SessionReplay.test.tsx`. If the file is empty or missing tests, replace it with this minimal test file (preserving pre-existing imports):

```tsx
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { useDevtoolsStore } from '../../stores/devtools'
import { SessionReplay } from './SessionReplay'

const mockSessions = [
  {
    session_id: 's-001',
    date: '2026-04-12',
    level: 3,
    overall_grade_before: 'F' as const,
    preflight: { verdict: 'pass' as const },
    triage: { bucket: 'context-management' },
    fix: { name: 'reduce-compaction', evidence: null },
    outcome: { grade_after: null },
    trace_links: { trace_id: 's-001' },
  },
  {
    session_id: 's-002',
    date: '2026-04-12',
    level: 3,
    overall_grade_before: 'F' as const,
    preflight: { verdict: 'pass' as const },
    triage: { bucket: 'other' },
    fix: { name: null, evidence: null },
    outcome: { grade_after: null },
    trace_links: { trace_id: null },
  },
]

beforeEach(() => {
  useDevtoolsStore.setState({ selectedTraceId: null })
  vi.stubGlobal('fetch', vi.fn(async () =>
    new Response(JSON.stringify({ sessions: mockSessions }), { status: 200 }),
  ))
})

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('SessionReplay', () => {
  it('row click with trace_id sets selectedTraceId', async () => {
    render(<SessionReplay />)
    const row = await screen.findByRole('button', { name: /s-001/i })
    fireEvent.click(row)
    await waitFor(() => {
      expect(useDevtoolsStore.getState().selectedTraceId).toBe('s-001')
    })
  })

  it('row without trace_id is disabled and shows (no trace) label', async () => {
    render(<SessionReplay />)
    const noTraceRow = await screen.findByText(/s-002/i)
    expect(noTraceRow.parentElement).toHaveTextContent(/no trace/i)
  })

  it('selected row has aria-selected true', async () => {
    useDevtoolsStore.setState({ selectedTraceId: 's-001' })
    render(<SessionReplay />)
    const row = await screen.findByRole('button', { name: /s-001/i })
    expect(row).toHaveAttribute('aria-selected', 'true')
  })
})
```

- [ ] **Step 17.3: Run test — expect failure**

```bash
cd frontend && npm test -- --run src/devtools/sop/SessionReplay.test.tsx
```

Expected: FAIL — click behavior not implemented.

- [ ] **Step 17.4: Modify SessionReplay.tsx**

Replace the component body so rows are `<button role="button">` with keyboard support, and use the store for selection:

```tsx
import { useEffect, useState } from 'react'
import { useDevtoolsStore } from '../../stores/devtools'
import { listSessions, type SOPSession } from './api'

export function SessionReplay() {
  const [sessions, setSessions] = useState<SOPSession[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const selectedTraceId = useDevtoolsStore((s) => s.selectedTraceId)
  const setSelectedTrace = useDevtoolsStore((s) => s.setSelectedTrace)

  useEffect(() => {
    listSessions()
      .then(setSessions)
      .catch((e: unknown) => setError(e instanceof Error ? e.message : 'error'))
  }, [])

  if (error) return <div className="sop-empty">Failed to load sessions: {error}</div>
  if (sessions === null) return <div className="sop-empty">Loading…</div>
  if (sessions.length === 0) {
    return (
      <div className="sop-empty">
        No sessions yet. Run eval with <code>TRACE_MODE=always make eval</code> to populate.
      </div>
    )
  }

  return (
    <div className="sop-session-list">
      {sessions.map((s) => {
        const traceId = s.trace_links.trace_id
        const selected = traceId !== null && traceId === selectedTraceId
        const disabled = traceId === null
        return (
          <button
            key={s.session_id}
            type="button"
            role="button"
            aria-selected={selected}
            disabled={disabled}
            onClick={() => { if (traceId) setSelectedTrace(traceId) }}
            className={`sop-row ${selected ? 'sop-row--selected' : ''}`}
            style={{
              display: 'flex',
              flexDirection: 'column',
              padding: '8px 12px',
              background: 'transparent',
              border: 'none',
              borderLeft: selected ? '2px solid #818cf8' : '2px solid transparent',
              color: '#e0e0e8',
              textAlign: 'left',
              cursor: disabled ? 'not-allowed' : 'pointer',
              opacity: disabled ? 0.5 : 1,
              fontFamily: 'monospace',
              fontSize: 11,
            }}
          >
            <span>
              <strong>{s.session_id}</strong> — level {s.level} — {s.triage.bucket ?? '—'}
              {disabled ? ' (no trace)' : ''}
            </span>
            <span style={{ color: '#94a3b8' }}>
              {s.overall_grade_before ?? '—'} → {s.outcome.grade_after ?? '—'} · {s.fix.name ?? 'no-fix'}
            </span>
          </button>
        )
      })}
    </div>
  )
}
```

- [ ] **Step 17.5: Run tests + typecheck**

```bash
cd frontend && npm test -- --run src/devtools/sop/SessionReplay.test.tsx
cd frontend && npx tsc --noEmit --pretty false
```

- [ ] **Step 17.6: Commit**

```bash
git add frontend/src/devtools/sop/SessionReplay.tsx frontend/src/devtools/sop/SessionReplay.test.tsx
git commit -m "feat(devtools): make SessionReplay rows clickable and selectable"
```

---

## Task 18: PromptInspector — step dropdown

**Files:**
- Modify: `frontend/src/devtools/sop/PromptInspector.tsx`
- Modify: `frontend/src/devtools/sop/PromptInspector.test.tsx`

- [ ] **Step 18.1: Write failing test for dropdown-driven step selection**

Replace `frontend/src/devtools/sop/PromptInspector.test.tsx` with:

```tsx
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { useDevtoolsStore } from '../../stores/devtools'
import { PromptInspector } from './PromptInspector'

const summaryBody = {
  summary: {
    session_id: 'trace-1',
    level: 3, outcome: 'ok', final_grade: 'F',
    turn_count: 2, llm_call_count: 2,
    step_ids: ['s1', 's2'],
  },
}

const assemblyBody = {
  sections: [{ source: 'SYSTEM_PROMPT', lines: '1-50', text: 'sys...' }],
  conflicts: [],
}

beforeEach(() => {
  useDevtoolsStore.setState({ selectedTraceId: 'trace-1', selectedStepId: null })
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    if (url.includes('/prompt/')) {
      return new Response(JSON.stringify(assemblyBody), { status: 200 })
    }
    return new Response(JSON.stringify(summaryBody), { status: 200 })
  }))
})

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('PromptInspector', () => {
  it('renders dropdown populated from step_ids', async () => {
    render(<PromptInspector traceId="trace-1" stepId="s1" />)
    const select = await screen.findByRole('combobox')
    const options = Array.from(select.querySelectorAll('option')).map((o) => o.value)
    expect(options).toEqual(['s1', 's2'])
  })

  it('changing dropdown updates selectedStepId in store', async () => {
    render(<PromptInspector traceId="trace-1" stepId="s1" />)
    const select = await screen.findByRole('combobox')
    fireEvent.change(select, { target: { value: 's2' } })
    await waitFor(() => {
      expect(useDevtoolsStore.getState().selectedStepId).toBe('s2')
    })
  })

  it('renders sections from assembly response', async () => {
    render(<PromptInspector traceId="trace-1" stepId="s1" />)
    expect(await screen.findByText(/SYSTEM_PROMPT/)).toBeInTheDocument()
  })
})
```

- [ ] **Step 18.2: Run test — expect failure**

```bash
cd frontend && npm test -- --run src/devtools/sop/PromptInspector.test.tsx
```

- [ ] **Step 18.3: Modify PromptInspector.tsx**

Replace with:

```tsx
import { useEffect, useState } from 'react'
import { useDevtoolsStore } from '../../stores/devtools'
import {
  fetchPromptAssembly,
  fetchTraceSummary,
  type PromptAssembly,
  type TraceSummary,
} from './api'

interface Props {
  traceId: string
  stepId: string
}

export function PromptInspector({ traceId, stepId }: Props) {
  const [summary, setSummary] = useState<TraceSummary | null>(null)
  const [assembly, setAssembly] = useState<PromptAssembly | null>(null)
  const [error, setError] = useState<string | null>(null)
  const setSelectedStep = useDevtoolsStore((s) => s.setSelectedStep)

  useEffect(() => {
    fetchTraceSummary(traceId)
      .then(setSummary)
      .catch((e: unknown) => setError(e instanceof Error ? e.message : 'error'))
  }, [traceId])

  useEffect(() => {
    fetchPromptAssembly(traceId, stepId)
      .then(setAssembly)
      .catch((e: unknown) => setError(e instanceof Error ? e.message : 'error'))
  }, [traceId, stepId])

  if (error) return <div className="sop-empty">{error}</div>
  if (!summary || !assembly) return <div className="sop-empty">Loading…</div>

  return (
    <div style={{ padding: 12, color: '#e0e0e8', fontFamily: 'monospace', fontSize: 11 }}>
      <div style={{ marginBottom: 12 }}>
        <label>Step: </label>
        <select
          value={stepId}
          onChange={(e) => setSelectedStep(e.target.value)}
          style={{ fontFamily: 'monospace', fontSize: 11 }}
        >
          {summary.step_ids.map((id) => (
            <option key={id} value={id}>{id}</option>
          ))}
        </select>
      </div>
      {assembly.sections.map((section, i) => (
        <div key={i} style={{ marginBottom: 8 }}>
          <div style={{ color: '#818cf8' }}>
            {section.source} ({section.lines})
          </div>
          <pre style={{ margin: 0, whiteSpace: 'pre-wrap' }}>{section.text}</pre>
        </div>
      ))}
      {assembly.conflicts.length > 0 && (
        <div style={{ marginTop: 16, color: '#f87171' }}>
          <strong>Conflicts:</strong>
          <ul>
            {assembly.conflicts.map((c, i) => (
              <li key={i}>{c.source_a} ↔ {c.source_b} at {c.overlap}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
```

- [ ] **Step 18.4: Run tests + typecheck**

```bash
cd frontend && npm test -- --run src/devtools/sop/PromptInspector.test.tsx
cd frontend && npx tsc --noEmit --pretty false
```

- [ ] **Step 18.5: Commit**

```bash
git add frontend/src/devtools/sop/PromptInspector.tsx frontend/src/devtools/sop/PromptInspector.test.tsx
git commit -m "feat(devtools): add step dropdown to PromptInspector"
```

---

## Task 19: CompactionTimeline — bar click

**Files:**
- Modify: `frontend/src/devtools/sop/CompactionTimeline.tsx`
- Modify: `frontend/src/devtools/sop/CompactionTimeline.test.tsx`

- [ ] **Step 19.1: Write failing test for bar click**

Replace `frontend/src/devtools/sop/CompactionTimeline.test.tsx` with:

```tsx
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { useDevtoolsStore } from '../../stores/devtools'
import { CompactionTimeline } from './CompactionTimeline'

const traceBody = {
  trace_schema_version: 1,
  summary: {
    session_id: 'trace-1', level: 3,
    outcome: 'ok', final_grade: 'F',
    turn_count: 2, llm_call_count: 2,
    step_ids: ['s1', 's2'],
  },
  events: [
    {
      kind: 'llm_call', seq: 1, timestamp: 't',
      step_id: 's1', turn: 1, model: 'm',
      temperature: 1, max_tokens: 1, prompt_text: '',
      sections: [], response_text: '', tool_calls: [],
      stop_reason: 'end_turn', input_tokens: 100, output_tokens: 0,
      cache_read_tokens: 0, cache_creation_tokens: 0, latency_ms: 0,
    },
    {
      kind: 'llm_call', seq: 2, timestamp: 't',
      step_id: 's2', turn: 2, model: 'm',
      temperature: 1, max_tokens: 1, prompt_text: '',
      sections: [], response_text: '', tool_calls: [],
      stop_reason: 'end_turn', input_tokens: 200, output_tokens: 0,
      cache_read_tokens: 0, cache_creation_tokens: 0, latency_ms: 0,
    },
  ],
}

const timelineBody = {
  turns: [
    { turn: 1, layers: { input: 100, tool_calls: 0 } },
    { turn: 2, layers: { input: 200, tool_calls: 0 } },
  ],
  events: [
    { turn: 1, kind: 'compaction', detail: 'dropped 2 layers, -500 tokens' },
  ],
}

beforeEach(() => {
  useDevtoolsStore.setState({ selectedTraceId: 'trace-1', selectedStepId: null })
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    if (url.includes('/timeline')) {
      return new Response(JSON.stringify(timelineBody), { status: 200 })
    }
    return new Response(JSON.stringify(traceBody), { status: 200 })
  }))
})

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('CompactionTimeline', () => {
  it('bar click sets selectedStepId to first step in that turn', async () => {
    render(<CompactionTimeline traceId="trace-1" />)
    const btn = await screen.findByRole('button', { name: /select turn 2/i })
    fireEvent.click(btn)
    await waitFor(() => {
      expect(useDevtoolsStore.getState().selectedStepId).toBe('s2')
    })
  })

  it('disables button when turn has no llm_call events', async () => {
    const noStepsBody = {
      ...timelineBody,
      turns: [{ turn: 99, layers: { input: 0, tool_calls: 1 } }],
    }
    const emptyTraceBody = {
      ...traceBody,
      events: [
        {
          kind: 'tool_call', seq: 1, timestamp: 't',
          turn: 99, tool_name: 't', tool_input: {},
          tool_output: '', duration_ms: 0, error: null,
        },
      ],
    }
    vi.stubGlobal('fetch', vi.fn(async (url: string) => {
      if (url.includes('/timeline')) {
        return new Response(JSON.stringify(noStepsBody), { status: 200 })
      }
      return new Response(JSON.stringify(emptyTraceBody), { status: 200 })
    }))
    render(<CompactionTimeline traceId="trace-1" />)
    const btn = await screen.findByRole('button', { name: /select turn 99/i })
    expect(btn).toBeDisabled()
  })
})
```

- [ ] **Step 19.2: Run test — expect failure**

```bash
cd frontend && npm test -- --run src/devtools/sop/CompactionTimeline.test.tsx
```

- [ ] **Step 19.3: Modify CompactionTimeline.tsx**

Replace with:

```tsx
import { useEffect, useMemo, useState } from 'react'
import { useDevtoolsStore } from '../../stores/devtools'
import { fetchTimeline, type Timeline } from './api'

interface Props {
  traceId: string
}

interface FullTrace {
  events: Array<{ kind: string; turn?: number; step_id?: string }>
}

export function CompactionTimeline({ traceId }: Props) {
  const [timeline, setTimeline] = useState<Timeline | null>(null)
  const [trace, setTrace] = useState<FullTrace | null>(null)
  const setSelectedStep = useDevtoolsStore((s) => s.setSelectedStep)

  useEffect(() => {
    fetchTimeline(traceId).then(setTimeline)
    fetch(`/api/trace/traces/${encodeURIComponent(traceId)}`)
      .then((r) => r.json())
      .then((body: FullTrace) => setTrace(body))
  }, [traceId])

  const firstStepByTurn = useMemo(() => {
    const m = new Map<number, string>()
    if (!trace) return m
    for (const e of trace.events) {
      if (e.kind === 'llm_call' && e.turn !== undefined && e.step_id !== undefined) {
        if (!m.has(e.turn)) m.set(e.turn, e.step_id)
      }
    }
    return m
  }, [trace])

  if (!timeline) return <div className="sop-empty">Loading…</div>

  return (
    <div style={{ padding: 12, color: '#e0e0e8', fontFamily: 'monospace', fontSize: 11 }}>
      <div style={{ display: 'flex', gap: 8, alignItems: 'flex-end', marginBottom: 16 }}>
        {timeline.turns.map((t) => {
          const stepId = firstStepByTurn.get(t.turn)
          const disabled = stepId === undefined
          return (
            <button
              key={t.turn}
              type="button"
              role="button"
              aria-label={`Select turn ${t.turn}`}
              disabled={disabled}
              onClick={() => { if (stepId) setSelectedStep(stepId) }}
              style={{
                background: 'transparent',
                border: '1px solid #2a2a3a',
                color: '#e0e0e8',
                padding: 8,
                cursor: disabled ? 'not-allowed' : 'pointer',
                opacity: disabled ? 0.5 : 1,
                fontFamily: 'monospace',
                fontSize: 11,
              }}
            >
              <div>Turn {t.turn}</div>
              <div style={{ color: '#818cf8' }}>in: {t.layers.input ?? 0}</div>
              <div style={{ color: '#94a3b8' }}>tools: {t.layers.tool_calls ?? 0}</div>
            </button>
          )
        })}
      </div>
      <ul style={{ margin: 0, padding: 0, listStyle: 'none' }}>
        {timeline.events.map((e, i) => (
          <li key={i} style={{ marginBottom: 4 }}>
            t{e.turn}: <span style={{ color: '#f59e0b' }}>[{e.kind}]</span> {e.detail}
          </li>
        ))}
      </ul>
    </div>
  )
}
```

- [ ] **Step 19.4: Run tests + typecheck**

```bash
cd frontend && npm test -- --run src/devtools/sop/CompactionTimeline.test.tsx
cd frontend && npx tsc --noEmit --pretty false
```

- [ ] **Step 19.5: Commit**

```bash
git add frontend/src/devtools/sop/CompactionTimeline.tsx frontend/src/devtools/sop/CompactionTimeline.test.tsx
git commit -m "feat(devtools): make CompactionTimeline bars clickable per turn"
```

---

## Task 20: DevToolsPanel — wire selection store and URL hook

**Files:**
- Modify: `frontend/src/devtools/DevToolsPanel.tsx`

- [ ] **Step 20.1: Read existing DevToolsPanel.tsx**

```bash
cat frontend/src/devtools/DevToolsPanel.tsx
```

Confirm current state has `useState<string | null>(null)` for both `selectedTraceId` and `selectedStepId`.

- [ ] **Step 20.2: Modify DevToolsPanel.tsx**

Replace the top of the component function (imports + selection state + useEffects) with store-backed reads and the URL sync hook. The complete updated file:

```tsx
import { useDevtoolsStore } from '../stores/devtools'
import { ContextInspector } from './ContextInspector'
import { SessionReplay } from './sop/SessionReplay'
import { JudgeVariance } from './sop/JudgeVariance'
import { PromptInspector } from './sop/PromptInspector'
import { CompactionTimeline } from './sop/CompactionTimeline'
import { useSelectionUrlSync } from './sop/useSelectionUrlSync'

const TABS = [
  'events', 'skills', 'config', 'wiki', 'evals', 'context',
  'sop-sessions', 'sop-judge', 'sop-prompt', 'sop-timeline',
] as const

function Placeholder({ name }: { name: string }) {
  return (
    <div style={{ color: '#4a4a5a', padding: 16, fontSize: 12 }}>
      {name} tab — not yet implemented
    </div>
  )
}

export function DevToolsPanel() {
  const { isOpen, activeTab, setActiveTab, selectedTraceId, selectedStepId } =
    useDevtoolsStore()
  useSelectionUrlSync()

  if (!isOpen) return null

  return (
    <div style={{
      position: 'fixed',
      top: 0, left: 0, right: 0, bottom: 32,
      background: '#0a0a0f', color: '#e0e0e8',
      fontFamily: 'monospace', fontSize: 11,
      zIndex: 1000, display: 'flex', flexDirection: 'column',
    }}>
      <div style={{
        display: 'flex', gap: 16, padding: '8px 12px',
        borderBottom: '1px solid #2a2a3a', background: '#14141f',
      }}>
        <span style={{ color: '#818cf8', fontWeight: 600 }}>⚙ DEV MODE</span>
        {TABS.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            style={{
              background: 'none', border: 'none',
              color: activeTab === tab ? '#818cf8' : '#94a3b8',
              borderBottom: activeTab === tab ? '1px solid #818cf8' : 'none',
              cursor: 'pointer', fontSize: 11,
              fontFamily: 'monospace', textTransform: 'capitalize',
              padding: '0 4px 4px',
            }}
          >
            {tab}
          </button>
        ))}
      </div>

      <div style={{ flex: 1, overflow: 'hidden' }}>
        {activeTab === 'context' && <ContextInspector />}
        {activeTab === 'sop-sessions' && <SessionReplay />}
        {activeTab === 'sop-judge' && (
          selectedTraceId
            ? <JudgeVariance traceId={selectedTraceId} />
            : <div className="sop-empty">Select a trace from the Session Replay tab.</div>
        )}
        {activeTab === 'sop-prompt' && (
          selectedTraceId && selectedStepId
            ? <PromptInspector traceId={selectedTraceId} stepId={selectedStepId} />
            : <div className="sop-empty">Select a trace+step from the Session Replay tab.</div>
        )}
        {activeTab === 'sop-timeline' && (
          selectedTraceId
            ? <CompactionTimeline traceId={selectedTraceId} />
            : <div className="sop-empty">Select a trace from the Session Replay tab.</div>
        )}
        {!['context', 'sop-sessions', 'sop-judge', 'sop-prompt', 'sop-timeline'].includes(activeTab) && (
          <Placeholder name={activeTab} />
        )}
      </div>
    </div>
  )
}
```

Note: the `useState` imports are removed since state now comes from the store.

- [ ] **Step 20.3: Run full frontend test suite + typecheck**

```bash
cd frontend && npm test -- --run
cd frontend && npx tsc --noEmit --pretty false
```

- [ ] **Step 20.4: Run dev server smoke check (manual)**

```bash
cd frontend && npm run dev &
```

Open `http://localhost:5173/?trace=<any-existing-trace>&step=s1` and confirm the three SOP tabs show content (or "no such trace" depending on state). Kill the dev server afterward.

- [ ] **Step 20.5: Commit**

```bash
git add frontend/src/devtools/DevToolsPanel.tsx
git commit -m "feat(devtools): wire selection store and URL sync into DevToolsPanel"
```

---

## Final verification

- [ ] **Run the full backend test suite + typecheck + lint**

```bash
cd backend && uv run python -m pytest -v
cd backend && uv run mypy --strict app/trace app/api/trace_api.py app/api/sop_api.py app/main.py app/sop/types.py app/context/manager.py
cd backend && uv run ruff check app/trace app/api/trace_api.py app/api/sop_api.py app/main.py app/sop/types.py app/context/manager.py tests/trace tests/sop
```

- [ ] **Run the full frontend test suite + typecheck**

```bash
cd frontend && npm test -- --run
cd frontend && npx tsc --noEmit --pretty false
```

- [ ] **Verify endpoints manually with a real server**

```bash
cd backend && uv run uvicorn app.main:create_app --factory --port 8000 &
curl -s http://localhost:8000/api/trace/traces | head
curl -s http://localhost:8000/api/sop/judge-variance/sess-int | head   # shim path
```

Kill the uvicorn process afterward.

- [ ] **Create a synthetic trace via the integration test flow to smoke the UI end-to-end**

```bash
cd backend && uv run python -c "
from pathlib import Path
from app.trace.publishers import TraceSession, publish_llm_call, publish_final_output
from app.trace.events import PromptSection
with TraceSession(
    session_id='manual-smoke', level=3, level_label='eval-level3',
    input_query='q', trace_mode='always', output_dir=Path('traces'),
) as s:
    publish_llm_call(
        step_id='s1', turn=1, model='m', temperature=1.0, max_tokens=10,
        prompt_text='p',
        sections=[PromptSection(source='SYSTEM_PROMPT', lines='1-50', text='...')],
        response_text='r', tool_calls=[], stop_reason='end_turn',
        input_tokens=100, output_tokens=20, cache_read_tokens=0,
        cache_creation_tokens=0, latency_ms=10,
    )
    publish_final_output(output_text='done', final_grade='F', judge_dimensions={})
    s.set_final_grade('F')
"
```

Then visit `http://localhost:5173/?trace=manual-smoke` with both dev servers running and confirm tabs light up.

- [ ] **Final commit for any missed lint/format fixes**

If anything still fails, fix and commit.
