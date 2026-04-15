from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL

from app.skills.statistical_analysis.time_series.characterize import _dominant_period


@dataclass(frozen=True, slots=True)
class Decomposition:
    trend: pd.Series
    seasonal: pd.Series
    residual: pd.Series
    period: int


def decompose(series: pd.Series | np.ndarray, period: int | None = None) -> Decomposition:
    if isinstance(series, pd.Series):
        work = series.dropna()
    else:
        arr = np.asarray(series, dtype=float)
        idx = pd.RangeIndex(len(arr))
        work = pd.Series(arr, index=idx).dropna()

    if period is None:
        if isinstance(work.index, pd.DatetimeIndex):
            detected = _dominant_period(work.to_numpy())
            period = detected
        if period is None:
            raise ValueError(
                "time_series.decompose: period required when autocorrelation "
                "cannot infer it."
            )
    stl = STL(work, period=period, robust=True).fit()
    return Decomposition(
        trend=stl.trend,
        seasonal=stl.seasonal,
        residual=stl.resid,
        period=period,
    )
