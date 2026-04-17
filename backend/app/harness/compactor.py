"""Proactive MicroCompact for the agent loop (P17).

Large tool results (DuckDB query dumps, stdout blobs, artifact payloads) are
the dominant driver of context growth.  When the turn's message history crosses
a char-budget threshold we drop the *content* of older tool-result messages,
replacing it with a compact summary that preserves the artifact refs.  The
agent can re-fetch via ``save_artifact``-style handles, but we stop paying the
token cost for stale intermediate dumps.

Design goals
------------
* Drop only tool *results* (role="tool"), never user/assistant text — the
  reasoning trail is what keeps the loop coherent.
* Keep the newest ``keep_recent`` tool results intact so the agent always has
  immediate context.
* Preserve artifact references so the agent can still resolve them.
* Return a ``CompactionReport`` the loop can surface via a ``micro_compact``
  stream event.
"""
from __future__ import annotations

import json
from dataclasses import dataclass

from app.harness.clients.base import Message

_ROUGH_CHARS_PER_TOKEN = 4  # Anthropic / OpenAI rule-of-thumb.


@dataclass(frozen=True, slots=True)
class CompactionReport:
    triggered: bool
    dropped_messages: int
    chars_before: int
    chars_after: int
    tokens_before: int
    tokens_after: int
    artifact_refs: tuple[str, ...]


class MicroCompactor:
    """Drop old tool-result payloads once the message history gets too heavy.

    Parameters
    ----------
    char_budget:
        Trigger threshold in characters of the full messages list (JSON-ish
        sum).  Default is 40 000 chars ≈ 10 000 tokens, well below the 200 K
        Claude limit but enough headroom for the system prompt + wiki digest.
    keep_recent:
        Number of most-recent tool-result messages to preserve verbatim.
    """

    def __init__(self, char_budget: int = 40_000, keep_recent: int = 3) -> None:
        if char_budget <= 0:
            raise ValueError("char_budget must be positive")
        if keep_recent < 1:
            raise ValueError("keep_recent must be >= 1")
        self._char_budget = char_budget
        self._keep_recent = keep_recent

    @property
    def char_budget(self) -> int:
        return self._char_budget

    def estimate_chars(self, messages: list[Message]) -> int:
        return sum(len(m.content or "") for m in messages)

    def maybe_compact(
        self, messages: list[Message]
    ) -> tuple[list[Message], CompactionReport]:
        """Return (possibly-compacted) messages plus a report.

        When the char budget is not exceeded, the input list is returned
        unchanged and ``report.triggered`` is False.
        """
        chars_before = self.estimate_chars(messages)
        if chars_before <= self._char_budget:
            return messages, CompactionReport(
                triggered=False,
                dropped_messages=0,
                chars_before=chars_before,
                chars_after=chars_before,
                tokens_before=chars_before // _ROUGH_CHARS_PER_TOKEN,
                tokens_after=chars_before // _ROUGH_CHARS_PER_TOKEN,
                artifact_refs=(),
            )

        # Find tool-result indices, chronological order preserved.
        tool_idx = [i for i, m in enumerate(messages) if m.role == "tool"]
        if len(tool_idx) <= self._keep_recent:
            return messages, CompactionReport(
                triggered=False,
                dropped_messages=0,
                chars_before=chars_before,
                chars_after=chars_before,
                tokens_before=chars_before // _ROUGH_CHARS_PER_TOKEN,
                tokens_after=chars_before // _ROUGH_CHARS_PER_TOKEN,
                artifact_refs=(),
            )

        drop_targets = set(tool_idx[: -self._keep_recent])
        collected_refs: list[str] = []
        new_messages: list[Message] = []
        for i, m in enumerate(messages):
            if i not in drop_targets:
                new_messages.append(m)
                continue
            refs = _extract_artifact_refs(m.content or "")
            collected_refs.extend(refs)
            placeholder = json.dumps(
                {
                    "compacted": True,
                    "tool": m.name,
                    "artifact_refs": refs,
                    "note": "older tool result dropped by MicroCompact",
                }
            )
            new_messages.append(
                Message(
                    role=m.role,
                    content=placeholder,
                    name=m.name,
                    tool_use_id=m.tool_use_id,
                    tool_calls=m.tool_calls,
                )
            )

        chars_after = self.estimate_chars(new_messages)
        return new_messages, CompactionReport(
            triggered=True,
            dropped_messages=len(drop_targets),
            chars_before=chars_before,
            chars_after=chars_after,
            tokens_before=chars_before // _ROUGH_CHARS_PER_TOKEN,
            tokens_after=chars_after // _ROUGH_CHARS_PER_TOKEN,
            artifact_refs=tuple(dict.fromkeys(collected_refs)),  # dedup, keep order
        )


def _extract_artifact_refs(content: str) -> list[str]:
    """Best-effort pull of artifact ids from a tool result JSON blob."""
    if not content:
        return []
    try:
        payload = json.loads(content)
    except (json.JSONDecodeError, ValueError):
        return []
    if not isinstance(payload, dict):
        return []
    refs: list[str] = []
    for key in ("artifact_refs", "new_artifact_ids", "artifact_id"):
        value = payload.get(key)
        if isinstance(value, list):
            refs.extend(str(v) for v in value if v)
        elif isinstance(value, str) and value:
            refs.append(value)
    return refs
