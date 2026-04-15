from __future__ import annotations

import numpy as np
from scipy.stats import skew


def auto_candidates(arr: np.ndarray) -> list[str]:
    x = np.asarray(arr, dtype=float)
    x = x[~np.isnan(x)]
    if x.size < 50:
        return []
    min_val, max_val = float(x.min()), float(x.max())
    skewness = float(skew(x))

    if 0.0 <= min_val <= 1.0 and 0.0 <= max_val <= 1.0:
        return ["beta", "uniform"]
    if min_val >= 0:
        cands = ["lognorm", "gamma", "weibull_min"]
        if skewness > 1.5:
            cands.append("pareto")
        return cands
    if abs(skewness) < 0.5:
        return ["norm", "t", "laplace"]
    return ["norm", "t", "laplace", "lognorm"]
