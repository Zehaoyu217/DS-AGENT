"""Test that micro_compact SSE events are recorded in the ContextManager."""
from __future__ import annotations

from app.context.manager import ContextManager


def test_record_compaction_appends_to_history():
    ctx = ContextManager()
    ctx.record_compaction(
        tokens_before=10_000,
        tokens_after=6_000,
        removed=[{"name": "compacted_tool_0"}, {"name": "compacted_tool_1"}],
        survived=["artifact-abc"],
    )
    history = ctx.compaction_history
    assert len(history) == 1
    entry = history[0]
    assert entry["tokens_before"] == 10_000
    assert entry["tokens_after"] == 6_000
    assert entry["tokens_freed"] == 4_000
    assert entry["id"] == 1
    assert len(entry["removed"]) == 2
    assert entry["survived"] == ["artifact-abc"]


def test_record_compaction_increments_id():
    ctx = ContextManager()
    ctx.record_compaction(5000, 4000, [], [])
    ctx.record_compaction(4000, 3000, [], [])
    ids = [e["id"] for e in ctx.compaction_history]
    assert ids == [1, 2]
