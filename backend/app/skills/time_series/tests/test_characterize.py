from __future__ import annotations

import numpy as np
import pandas as pd

from app.skills.time_series.characterize import characterize


def test_white_noise_declared_stationary() -> None:
    rng = np.random.default_rng(0)
    s = pd.Series(rng.standard_normal(500))
    result = characterize(s)
    assert result.stationary is True
    assert result.adf_p < 0.05
    assert result.kpss_p > 0.05


def test_random_walk_declared_non_stationary() -> None:
    rng = np.random.default_rng(1)
    s = pd.Series(np.cumsum(rng.standard_normal(500)))
    result = characterize(s)
    assert result.stationary is False


def test_seasonal_series_period_detected(seasonal_240) -> None:
    result = characterize(seasonal_240)
    assert result.dominant_period is not None
    assert 8 <= result.dominant_period <= 16


def test_trend_slope_positive_when_monotonic_up() -> None:
    idx = pd.date_range("2022-01-01", periods=100, freq="D")
    s = pd.Series(np.linspace(0, 10, 100), index=idx)
    result = characterize(s)
    assert result.trend_slope > 0.05
