from __future__ import annotations

import pandas as pd
import pytest

from app.skills._stat_fixtures.generators import (
    confounded_frame,
    heavy_tailed_series,
    linear_xy,
    monotonic_nonlinear_xy,
    noisy_groups,
    seasonal_series,
    simpsons_paradox_frame,
)


@pytest.fixture
def linear_07():
    return linear_xy(n=400, rho=0.7, seed=42)


@pytest.fixture
def monotonic_df():
    x, y = monotonic_nonlinear_xy(n=300, seed=7)
    return pd.DataFrame({"x": x, "y": y})


@pytest.fixture
def two_groups():
    return noisy_groups(per_group=80, effect=0.6, seed=3)


@pytest.fixture
def seasonal_240():
    return seasonal_series(n=240, period=12, seed=0)


@pytest.fixture
def heavy_1k():
    return heavy_tailed_series(n=1000, seed=1)


@pytest.fixture
def simpsons_df():
    return simpsons_paradox_frame(seed=9)


@pytest.fixture
def confounded_df():
    return confounded_frame(seed=11)
