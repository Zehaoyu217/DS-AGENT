"""
Doom-loop detection for repeated tool call patterns.

Adapted from huggingface/ml-intern (agent/core/doom_loop.py).
Detects when the agent is stuck calling the same tools repeatedly
and injects a corrective prompt message to break the cycle.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from app.harness.clients.base import Message, ToolCall  # noqa: F401


@dataclass(frozen=True)
class ToolCallSignature:
    name: str
    args_hash: str


def _hash_args(args: dict) -> str:
    return hashlib.md5(
        json.dumps(args, sort_keys=True, default=str).encode()
    ).hexdigest()[:12]


def _extract_recent_signatures(
    messages: list[Message],
    lookback: int = 30,
) -> list[ToolCallSignature]:
    recent = messages[-lookback:] if len(messages) > lookback else messages
    sigs: list[ToolCallSignature] = []
    for msg in recent:
        if msg.role != "assistant":
            continue
        for tc in msg.tool_calls:
            sigs.append(ToolCallSignature(name=tc.name, args_hash=_hash_args(tc.arguments)))
    return sigs


def _detect_identical_consecutive(
    sigs: list[ToolCallSignature],
    threshold: int = 3,
) -> str | None:
    """Return the tool name if threshold+ identical consecutive calls are found."""
    if len(sigs) < threshold:
        return None
    count = 1
    for i in range(1, len(sigs)):
        if sigs[i] == sigs[i - 1]:
            count += 1
            if count >= threshold:
                return sigs[i].name
        else:
            count = 1
    return None


def _detect_repeating_sequence(
    sigs: list[ToolCallSignature],
) -> list[ToolCallSignature] | None:
    """Detect repeating patterns like [A,B,A,B] for seq lengths 2–5 with 2+ reps."""
    n = len(sigs)
    for seq_len in range(2, 6):
        min_required = seq_len * 2
        if n < min_required:
            continue
        tail = sigs[-min_required:]
        pattern = tail[:seq_len]
        reps = 0
        for start in range(n - seq_len, -1, -seq_len):
            chunk = sigs[start : start + seq_len]
            if chunk == pattern:
                reps += 1
            else:
                break
        if reps >= 2:
            return pattern
    return None


def check_for_doom_loop(messages: list[Message]) -> Message | None:
    """Return a corrective user Message to inject, or None if no loop detected."""
    sigs = _extract_recent_signatures(messages)

    tool_name = _detect_identical_consecutive(sigs)
    if tool_name:
        return Message(
            role="user",
            content=(
                f"[SYSTEM] Doom-loop detected: you have called '{tool_name}' with "
                f"identical arguments 3+ times without making progress. "
                f"Stop and change your approach: use a different tool, modify your "
                f"strategy, or synthesise what you have gathered so far."
            ),
        )

    pattern = _detect_repeating_sequence(sigs)
    if pattern:
        names = " → ".join(s.name for s in pattern)
        return Message(
            role="user",
            content=(
                f"[SYSTEM] Doom-loop detected: you are cycling through [{names}] "
                f"repeatedly without making progress. Break the cycle: try a different "
                f"tool, change your approach, or report your findings so far."
            ),
        )

    return None
