from __future__ import annotations

import numpy as np

from app.skills.statistical_analysis.distribution_fit.candidates import auto_candidates


def test_unbounded_symmetric_picks_normal_family() -> None:
    rng = np.random.default_rng(0)
    s = rng.standard_normal(500)
    names = auto_candidates(s)
    assert "norm" in names
    assert "t" in names


def test_positive_skew_picks_heavy_family(heavy_1k) -> None:
    names = auto_candidates(heavy_1k.to_numpy())
    assert "lognorm" in names or "pareto" in names
    assert "gamma" in names


def test_bounded_unit_picks_beta() -> None:
    rng = np.random.default_rng(1)
    s = rng.beta(2.0, 5.0, 500)
    names = auto_candidates(s)
    assert "beta" in names
