from __future__ import annotations

import numpy as np

from app.skills.distribution_fit.rank import rank_candidates


def test_normal_beats_heavy_on_normal_data() -> None:
    rng = np.random.default_rng(0)
    s = rng.normal(0, 1, 500)
    ranked = rank_candidates(s, ["norm", "t", "laplace"])
    assert ranked[0].name == "norm"


def test_ranked_sorted_by_aic() -> None:
    rng = np.random.default_rng(0)
    s = rng.normal(0, 1, 500)
    ranked = rank_candidates(s, ["norm", "t", "laplace"])
    aics = [c.aic for c in ranked]
    assert aics == sorted(aics)
