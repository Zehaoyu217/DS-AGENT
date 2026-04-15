from __future__ import annotations

import numpy as np


def hill_alpha(arr: np.ndarray, k_frac: float = 0.10) -> float | None:
    x = np.asarray(arr, dtype=float)
    x = x[(~np.isnan(x)) & (x > 0)]
    n = x.size
    if n < 100:
        return None
    k = max(10, int(k_frac * n))
    sorted_desc = np.sort(x)[::-1]
    top_k = sorted_desc[:k]
    if top_k[-1] <= 0:
        return None
    log_ratios = np.log(top_k[:-1] / top_k[-1])
    hill = float(np.mean(log_ratios))
    if hill == 0:
        return None
    return float(1.0 / hill)
