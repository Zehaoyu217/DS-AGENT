"""Read/write baseline snapshots for eval levels."""
from __future__ import annotations

from pathlib import Path

import yaml

from app.sop.types import Baseline, Grade

GRADE_ORDER: dict[Grade, int] = {"A": 3, "B": 2, "C": 1, "F": 0}


def _baseline_path(level: int, baselines_dir: Path) -> Path:
    return baselines_dir / f"level{level}.yaml"


def load_baseline(level: int, baselines_dir: Path) -> Baseline | None:
    """Return the last-passing baseline for the given level, or None if missing."""
    path = _baseline_path(level, baselines_dir)
    if not path.exists():
        return None
    data = yaml.safe_load(path.read_text())
    return Baseline.model_validate(data)


def update_baseline(baseline: Baseline, baselines_dir: Path) -> None:
    """Write baseline YAML for its level."""
    baselines_dir.mkdir(parents=True, exist_ok=True)
    path = _baseline_path(baseline.level, baselines_dir)
    path.write_text(yaml.safe_dump(baseline.model_dump(), sort_keys=False))


def should_update_baseline(
    target_level: int,
    prior_grades: dict[int, Grade],
    new_grades: dict[int, Grade],
) -> bool:
    """True iff target_level is >= B and no other level regressed."""
    target_new = new_grades.get(target_level)
    if target_new is None or GRADE_ORDER[target_new] < GRADE_ORDER["B"]:
        return False
    if GRADE_ORDER[target_new] <= GRADE_ORDER.get(prior_grades.get(target_level, "F"), 0):
        return False
    for lvl, prior in prior_grades.items():
        if lvl == target_level:
            continue
        if GRADE_ORDER[new_grades.get(lvl, "F")] < GRADE_ORDER[prior]:
            return False
    return True
