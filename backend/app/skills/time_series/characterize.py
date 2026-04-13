from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from statsmodels.tsa.stattools import acf, adfuller, kpss


@dataclass(frozen=True, slots=True)
class TSCharacterization:
    stationary: bool
    adf_p: float
    kpss_p: float
    trend_slope: float
    dominant_period: int | None
    autocorrelation_lag1: float
    n: int

    def to_dict(self) -> dict:
        return asdict(self)


def _as_array(series: pd.Series | np.ndarray) -> np.ndarray:
    if isinstance(series, pd.Series):
        return series.dropna().to_numpy()
    arr = np.asarray(series, dtype=float)
    return arr[~np.isnan(arr)]


def _trend_slope(arr: np.ndarray) -> float:
    x = np.arange(arr.size)
    if arr.size < 3:
        return 0.0
    slope, _ = np.polyfit(x, arr, 1)
    return float(slope)


def _dominant_period(arr: np.ndarray, min_period: int = 2) -> int | None:
    if arr.size < 40:
        return None
    max_lag = min(arr.size // 2, 180)
    ac = acf(arr, nlags=max_lag, fft=True)
    peaks, props = find_peaks(ac[min_period:], height=0.2)
    if peaks.size == 0:
        return None
    best = int(peaks[np.argmax(props["peak_heights"])]) + min_period
    return best


def characterize(series: pd.Series | np.ndarray) -> TSCharacterization:
    arr = _as_array(series)
    if arr.size < 20:
        raise ValueError(f"time_series.characterize: n={arr.size} < 20")
    adf_p = float(adfuller(arr, autolag="AIC")[1])
    try:
        kpss_p = float(kpss(arr, regression="c", nlags="auto")[1])
    except Exception:
        kpss_p = 1.0
    stationary = adf_p < 0.05 and kpss_p > 0.05
    slope = _trend_slope(arr)
    period = _dominant_period(arr)
    lag1 = float(acf(arr, nlags=1, fft=True)[1])
    return TSCharacterization(
        stationary=stationary,
        adf_p=adf_p,
        kpss_p=kpss_p,
        trend_slope=slope,
        dominant_period=period,
        autocorrelation_lag1=lag1,
        n=int(arr.size),
    )
