from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from app.skills.statistical_analysis.time_series.lag_correlate import lag_correlate


def test_lagged_relationship_found() -> None:
    rng = np.random.default_rng(0)
    noise = rng.standard_normal(500)
    x = pd.Series(rng.standard_normal(500))
    y = pd.Series(x.shift(3).fillna(0) + noise * 0.2)
    result = lag_correlate(x, y, max_lag=8)
    peak_lag = int(np.argmax(np.abs(result.coefficients)))
    lags_axis = np.arange(-8, 9)
    assert abs(lags_axis[peak_lag]) in {2, 3, 4}


def test_lag_correlate_refuses_non_stationary() -> None:
    rng = np.random.default_rng(1)
    walk = pd.Series(np.cumsum(rng.standard_normal(300)))
    with pytest.raises(ValueError, match="non_stationary"):
        lag_correlate(walk, walk * 1.1, max_lag=5)


def test_lag_correlate_allowed_with_override() -> None:
    rng = np.random.default_rng(2)
    walk = pd.Series(np.cumsum(rng.standard_normal(300)))
    result = lag_correlate(walk, walk * 1.1, max_lag=5, accept_non_stationary=True)
    assert result.coefficients.size == 11
