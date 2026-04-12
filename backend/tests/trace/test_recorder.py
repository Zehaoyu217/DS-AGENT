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
