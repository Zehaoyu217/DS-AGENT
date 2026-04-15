from __future__ import annotations

import numpy as np

from app.skills.statistical_analysis.distribution_fit.fit_one import FitCandidate, fit_one


def rank_candidates(arr: np.ndarray, names: list[str]) -> list[FitCandidate]:
    fits: list[FitCandidate] = []
    for name in names:
        try:
            fits.append(fit_one(name, arr))
        except Exception:
            continue
    return sorted(fits, key=lambda c: c.aic)
