from __future__ import annotations

import numpy as np

from app.skills.distribution_fit.hill import hill_alpha


def test_hill_estimator_recovers_pareto_alpha() -> None:
    rng = np.random.default_rng(0)
    s = rng.pareto(2.0, 5000) + 1
    alpha = hill_alpha(s, k_frac=0.10)
    assert 1.5 < alpha < 2.5


def test_hill_returns_none_on_small_n() -> None:
    s = np.arange(20, dtype=float)
    assert hill_alpha(s, k_frac=0.10) is None
