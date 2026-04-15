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
