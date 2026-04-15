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
