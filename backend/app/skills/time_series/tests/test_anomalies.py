from __future__ import annotations

import numpy as np
import pandas as pd

from app.skills.time_series.anomalies import find_anomalies


def test_injected_spikes_detected() -> None:
    rng = np.random.default_rng(0)
    base = rng.standard_normal(200)
    base[37] = 8.0
    base[112] = -7.5
    idx = pd.date_range("2022-01-01", periods=200, freq="D")
    s = pd.Series(base, index=idx)
    result = find_anomalies(s, method="robust_z")
    assert 37 in result.indices
    assert 112 in result.indices


def test_clean_series_returns_empty(seasonal_240) -> None:
    result = find_anomalies(seasonal_240, method="robust_z")
    assert len(result.indices) < 10
