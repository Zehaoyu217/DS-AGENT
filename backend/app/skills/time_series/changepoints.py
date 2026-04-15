from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
import ruptures as rpt


@dataclass(frozen=True, slots=True)
class ChangepointResult:
    indices: list[int]
    segments: list[tuple[int, int]]


def find_changepoints(
    series: pd.Series | np.ndarray, penalty: float = 10.0
) -> ChangepointResult:
    arr = (
        series.dropna().to_numpy()
        if isinstance(series, pd.Series)
        else np.asarray(series, dtype=float)
    )
    algo = rpt.Pelt(model="rbf").fit(arr.reshape(-1, 1))
    raw = algo.predict(pen=penalty)
    indices = [int(i) for i in raw[:-1]]
    segments: list[tuple[int, int]] = []
    prev = 0
    for end in raw:
        segments.append((prev, int(end)))
        prev = int(end)
    return ChangepointResult(indices=indices, segments=segments)
