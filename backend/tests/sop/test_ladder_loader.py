from __future__ import annotations

import pytest

from app.sop.ladder_loader import load_all_ladders, load_ladder

EXPECTED_BUCKETS = {
    "context", "prompt", "capability", "routing", "architecture", "harness",
    "evaluation_bias", "data_quality", "determinism",
}


def test_load_all_ladders_covers_nine_buckets() -> None:
    ladders = load_all_ladders()
    assert {ld.bucket for ld in ladders} == EXPECTED_BUCKETS


def test_each_ladder_has_at_least_three_rungs() -> None:
    for ld in load_all_ladders():
        assert len(ld.ladder) >= 3, f"bucket {ld.bucket} has fewer than 3 rungs"


def test_ladder_rung_ids_are_prefixed_by_bucket() -> None:
    for ld in load_all_ladders():
        for rung in ld.ladder:
            assert rung.id.startswith(ld.bucket.replace("_", "-")), rung.id


def test_load_ladder_by_bucket() -> None:
    ladder = load_ladder("context")
    assert ladder.bucket == "context"
    assert ladder.ladder[0].cost == "trivial"


def test_load_ladder_unknown_raises() -> None:
    with pytest.raises(FileNotFoundError):
        load_ladder("no_such_bucket")


def test_ladders_sorted_by_cost() -> None:
    order = {"trivial": 0, "small": 1, "medium": 2, "large": 3}
    for ld in load_all_ladders():
        costs = [order[r.cost] for r in ld.ladder]
        assert costs == sorted(costs), f"ladder {ld.bucket} not cost-ordered: {costs}"
