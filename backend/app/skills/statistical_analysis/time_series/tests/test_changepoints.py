from __future__ import annotations

import numpy as np
import pandas as pd

from app.skills.statistical_analysis.time_series.changepoints import find_changepoints


def test_step_change_detected() -> None:
    rng = np.random.default_rng(0)
    a = rng.normal(0, 1, 200)
    b = rng.normal(5, 1, 200)
    s = pd.Series(np.concatenate([a, b]))
    result = find_changepoints(s, penalty=5.0)
    assert any(190 <= cp <= 220 for cp in result.indices)


def test_no_change_returns_few_or_none() -> None:
    rng = np.random.default_rng(1)
    s = pd.Series(rng.normal(0, 1, 300))
    result = find_changepoints(s, penalty=20.0)
    assert len(result.indices) <= 1
