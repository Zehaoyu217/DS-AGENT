from app.context.manager import ContextLayer, ContextManager


def test_add_layer() -> None:
    mgr = ContextManager(max_tokens=32768)
    mgr.add_layer(ContextLayer(
        name="system",
        tokens=1640,
        compactable=False,
        items=[{"name": "system_prompt", "tokens": 1640}],
    ))
    assert mgr.total_tokens == 1640
    assert mgr.utilization < 0.1


def test_utilization_calculation() -> None:
    mgr = ContextManager(max_tokens=10000)
    mgr.add_layer(ContextLayer(name="system", tokens=5000, compactable=False, items=[]))
    assert mgr.utilization == 0.5


def test_snapshot_returns_all_layers() -> None:
    mgr = ContextManager(max_tokens=32768)
    mgr.add_layer(ContextLayer(name="system", tokens=1640, compactable=False, items=[]))
    mgr.add_layer(ContextLayer(name="l1_always", tokens=1600, compactable=False, items=[]))
    mgr.add_layer(ContextLayer(name="conversation", tokens=3000, compactable=True, items=[]))
    snapshot = mgr.snapshot()
    assert snapshot["total_tokens"] == 6240
    assert len(snapshot["layers"]) == 3
    assert snapshot["max_tokens"] == 32768


def test_compaction_needed() -> None:
    mgr = ContextManager(max_tokens=10000, compaction_threshold=0.8)
    mgr.add_layer(ContextLayer(name="system", tokens=2000, compactable=False, items=[]))
    assert not mgr.compaction_needed
    mgr.add_layer(ContextLayer(name="conversation", tokens=7000, compactable=True, items=[]))
    assert mgr.compaction_needed


def test_compaction_history() -> None:
    mgr = ContextManager(max_tokens=10000, compaction_threshold=0.8)
    mgr.record_compaction(
        tokens_before=8500,
        tokens_after=4200,
        removed=[{"name": "old_ref.md", "tokens": 1200}],
        survived=["system", "l1_always"],
    )
    history = mgr.compaction_history
    assert len(history) == 1
    assert history[0]["tokens_freed"] == 4300
