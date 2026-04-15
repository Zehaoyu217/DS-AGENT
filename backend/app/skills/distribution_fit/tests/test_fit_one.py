from __future__ import annotations

import numpy as np

from app.skills.distribution_fit.fit_one import fit_one


def test_fit_normal_returns_aic_bic_params() -> None:
    rng = np.random.default_rng(0)
    s = rng.normal(5, 2, 500)
    cand = fit_one("norm", s)
    assert cand.name == "norm"
    assert len(cand.params) == 2
    assert 4.7 < cand.params[0] < 5.3
    assert cand.aic < cand.bic
    assert 0.0 <= cand.ks_p <= 1.0


def test_fit_unknown_raises() -> None:
    import pytest
    with pytest.raises(ValueError):
        fit_one("not_a_dist", np.array([1.0, 2, 3, 4]))
