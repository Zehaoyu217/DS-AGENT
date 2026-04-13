from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from app.skills.time_series.characterize import _dominant_period


@dataclass(frozen=True, slots=True)
class AnomalyResult:
    indices: list[int]
    values: list[float]
    method_used: str
    threshold: float


def _robust_z(arr: np.ndarray, z_threshold: float) -> np.ndarray:
    median = np.median(arr)
    mad = np.median(np.abs(arr - median))
    if mad == 0:
        return np.zeros(arr.size, dtype=bool)
    z = 0.6745 * (arr - median) / mad
    return np.abs(z) > z_threshold


def _seasonal_esd(arr: np.ndarray, period: int, z_threshold: float) -> np.ndarray:
    from statsmodels.tsa.seasonal import STL
    stl = STL(arr, period=period, robust=True).fit()
    resid = stl.resid.to_numpy() if hasattr(stl.resid, "to_numpy") else stl.resid
    return _robust_z(resid, z_threshold)


def find_anomalies(
    series: pd.Series | np.ndarray,
    method: str = "auto",
    z_threshold: float = 3.5,
) -> AnomalyResult:
    arr = series.dropna().to_numpy() if isinstance(series, pd.Series) else np.asarray(series, dtype=float)
    if method == "auto":
        period = _dominant_period(arr)
        method = "seasonal_esd" if period is not None else "robust_z"
    if method == "robust_z":
        mask = _robust_z(arr, z_threshold)
    elif method == "seasonal_esd":
        period = _dominant_period(arr) or 12
        mask = _seasonal_esd(arr, period=period, z_threshold=z_threshold)
    else:
        raise ValueError(f"unknown anomaly method: {method}")
    idx = np.where(mask)[0].tolist()
    return AnomalyResult(
        indices=idx,
        values=[float(arr[i]) for i in idx],
        method_used=method,
        threshold=z_threshold,
    )
