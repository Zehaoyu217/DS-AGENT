from __future__ import annotations

import numpy as np
import pandas as pd

from app.skills._stat_fixtures.generators import (
    confounded_frame,
    heavy_tailed_series,
    linear_xy,
    monotonic_nonlinear_xy,
    noisy_groups,
    seasonal_series,
    simpsons_paradox_frame,
)


def test_linear_xy_has_known_pearson() -> None:
    x, y = linear_xy(n=500, rho=0.75, seed=42)
    r = np.corrcoef(x, y)[0, 1]
    assert abs(r - 0.75) < 0.05


def test_monotonic_nonlinear_low_pearson_high_spearman() -> None:
    x, y = monotonic_nonlinear_xy(n=300, seed=7)
    r_pearson = np.corrcoef(x, y)[0, 1]
    from scipy.stats import spearmanr
    r_spearman = spearmanr(x, y).correlation
    assert r_spearman > 0.9
    assert r_pearson < r_spearman - 0.1


def test_noisy_groups_shape() -> None:
    df = noisy_groups(per_group=80, effect=0.6, seed=3)
    assert set(df["group"].unique()) == {"A", "B"}
    assert len(df) == 160
    assert df["value"].notna().all()


def test_seasonal_series_has_period() -> None:
    s = seasonal_series(n=240, period=12, seed=0)
    assert isinstance(s, pd.Series)
    assert len(s) == 240
    assert s.index.freq is not None


def test_heavy_tailed_series_has_extremes() -> None:
    s = heavy_tailed_series(n=1000, seed=1)
    q99 = s.quantile(0.99)
    median = s.median()
    assert q99 > 6 * median


def test_simpsons_paradox_frame_reverses() -> None:
    df = simpsons_paradox_frame(seed=9)
    pooled = np.corrcoef(df["x"], df["y"])[0, 1]
    by_group = []
    for _, grp in df.groupby("stratum"):
        by_group.append(np.corrcoef(grp["x"], grp["y"])[0, 1])
    assert pooled * np.mean(by_group) < 0


def test_confounded_frame_has_hidden_common_cause() -> None:
    df = confounded_frame(seed=11)
    assert set(df.columns) == {"confounder", "x", "y"}
    r_xy = np.corrcoef(df["x"], df["y"])[0, 1]
    assert abs(r_xy) > 0.3
