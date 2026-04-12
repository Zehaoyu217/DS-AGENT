from __future__ import annotations

from pathlib import Path

import pytest

from app.sop.baseline import load_baseline, should_update_baseline, update_baseline
from app.sop.types import Baseline, Grade, Signals


@pytest.fixture
def baselines_dir(tmp_path: Path) -> Path:
    d = tmp_path / "baselines"
    d.mkdir()
    return d


def _sample(level: int, writes: int) -> Baseline:
    return Baseline(
        level=level, date="2026-04-10", trace_id="t",
        signals=Signals(
            token_count=100, duration_ms=10, compaction_events=0,
            scratchpad_writes=writes, tool_errors=0, retries=0,
            subagents_spawned=0, models_used={},
        ),
    )


def test_load_missing_baseline_returns_none(baselines_dir: Path) -> None:
    assert load_baseline(3, baselines_dir) is None


def test_roundtrip_update_and_load(baselines_dir: Path) -> None:
    b = _sample(3, 8)
    update_baseline(b, baselines_dir)
    loaded = load_baseline(3, baselines_dir)
    assert loaded == b


def test_should_update_when_target_improved_no_regression() -> None:
    prior: dict[int, Grade] = {1: "B", 2: "B", 3: "C", 4: "B", 5: "B"}
    new: dict[int, Grade] = {1: "B", 2: "B", 3: "B", 4: "B", 5: "B"}
    assert should_update_baseline(target_level=3, prior_grades=prior, new_grades=new)


def test_should_not_update_when_regression_on_other_level() -> None:
    prior: dict[int, Grade] = {1: "B", 2: "B", 3: "C", 4: "B", 5: "B"}
    new: dict[int, Grade] = {1: "B", 2: "B", 3: "B", 4: "C", 5: "B"}
    assert not should_update_baseline(target_level=3, prior_grades=prior, new_grades=new)


def test_should_not_update_when_target_below_grade_b() -> None:
    prior: dict[int, Grade] = {1: "B", 2: "B", 3: "C", 4: "B", 5: "B"}
    new: dict[int, Grade] = {1: "B", 2: "B", 3: "C", 4: "B", 5: "B"}
    assert not should_update_baseline(target_level=3, prior_grades=prior, new_grades=new)
