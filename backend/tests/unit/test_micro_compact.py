"""Tests for the proactive MicroCompact (P17)."""
from __future__ import annotations

import json

import pytest

from app.harness.clients.base import Message
from app.harness.compactor import MicroCompactor, _extract_artifact_refs


def _tool_msg(name: str, payload: dict, *, tool_use_id: str = "t") -> Message:
    return Message(
        role="tool",
        content=json.dumps(payload),
        name=name,
        tool_use_id=tool_use_id,
    )


def test_no_compaction_below_budget():
    comp = MicroCompactor(char_budget=10_000, keep_recent=3)
    messages = [
        Message(role="user", content="hello"),
        _tool_msg("execute_python", {"value": "x" * 100}),
    ]
    out, report = comp.maybe_compact(messages)
    assert report.triggered is False
    assert out is messages  # same identity when no work to do
    assert report.dropped_messages == 0


def test_no_compaction_when_not_enough_tool_results():
    comp = MicroCompactor(char_budget=50, keep_recent=3)
    messages = [
        Message(role="user", content="a" * 100),  # over budget
        _tool_msg("execute_python", {"value": "b" * 100}),
    ]
    out, report = comp.maybe_compact(messages)
    # Over budget but only one tool result → nothing to drop.
    assert report.triggered is False
    assert out is messages


def test_compaction_drops_oldest_tool_results():
    comp = MicroCompactor(char_budget=100, keep_recent=2)
    big = "x" * 400
    messages = [
        Message(role="user", content="run it"),
        _tool_msg("execute_python", {"stdout": big, "artifact_refs": ["a1"]}),
        Message(role="assistant", content="thinking"),
        _tool_msg("save_artifact", {"artifact_id": "a2", "stdout": big}),
        _tool_msg("execute_python", {"stdout": big, "artifact_refs": ["a3"]}),
        _tool_msg("execute_python", {"stdout": big, "artifact_refs": ["a4"]}),
    ]
    chars_before = sum(len(m.content) for m in messages)
    assert chars_before > 100  # sanity

    out, report = comp.maybe_compact(messages)
    assert report.triggered is True
    # 4 tool results, keep_recent=2 → drop the first 2.
    assert report.dropped_messages == 2
    assert report.chars_after < report.chars_before
    # The two oldest tool results must be placeholder blobs, newest two intact.
    tool_messages = [m for m in out if m.role == "tool"]
    assert len(tool_messages) == 4

    first_payload = json.loads(tool_messages[0].content)
    assert first_payload["compacted"] is True
    assert first_payload["tool"] == "execute_python"
    assert first_payload["artifact_refs"] == ["a1"]

    second_payload = json.loads(tool_messages[1].content)
    assert second_payload["compacted"] is True
    assert second_payload["artifact_refs"] == ["a2"]

    # Newest two must still carry the big stdout.
    third_payload = json.loads(tool_messages[2].content)
    assert third_payload.get("stdout") == big
    fourth_payload = json.loads(tool_messages[3].content)
    assert fourth_payload.get("stdout") == big


def test_compaction_preserves_non_tool_messages():
    comp = MicroCompactor(char_budget=100, keep_recent=1)
    messages = [
        Message(role="user", content="u" * 200),
        _tool_msg("t1", {"stdout": "a" * 200}),
        Message(role="assistant", content="assistant mid"),
        _tool_msg("t2", {"stdout": "b" * 200}),
        _tool_msg("t3", {"stdout": "c" * 200}),
    ]
    out, report = comp.maybe_compact(messages)
    assert report.triggered is True
    # User + assistant should not be dropped or rewritten.
    assert out[0].role == "user" and out[0].content == "u" * 200
    assert out[2].role == "assistant" and out[2].content == "assistant mid"


def test_compaction_dedups_artifact_refs():
    comp = MicroCompactor(char_budget=50, keep_recent=1)
    messages = [
        Message(role="user", content="x" * 100),
        _tool_msg("t1", {"artifact_refs": ["a", "b"], "pad": "p" * 200}),
        _tool_msg("t2", {"artifact_refs": ["b", "c"], "pad": "p" * 200}),
        _tool_msg("t3", {"pad": "p" * 200}),
    ]
    _, report = comp.maybe_compact(messages)
    assert report.triggered is True
    assert report.artifact_refs == ("a", "b", "c")  # deduped, order preserved


def test_extract_artifact_refs_handles_variants():
    assert _extract_artifact_refs('{"artifact_refs": ["a", "b"]}') == ["a", "b"]
    assert _extract_artifact_refs('{"artifact_id": "a1"}') == ["a1"]
    assert _extract_artifact_refs('{"new_artifact_ids": ["n1", "n2"]}') == ["n1", "n2"]
    assert _extract_artifact_refs("not-json") == []
    assert _extract_artifact_refs("") == []
    assert _extract_artifact_refs("[1,2,3]") == []


def test_constructor_validates():
    with pytest.raises(ValueError):
        MicroCompactor(char_budget=0)
    with pytest.raises(ValueError):
        MicroCompactor(keep_recent=0)
