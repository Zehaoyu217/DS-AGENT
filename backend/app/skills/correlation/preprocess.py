from __future__ import annotations

import numpy as np
import pandas as pd
from statsmodels.api import OLS, add_constant


def drop_na_rows(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    before = len(df)
    cleaned = df.dropna()
    return cleaned.reset_index(drop=True), before - len(cleaned)


def apply_detrend(series: pd.Series, method: str | None) -> pd.Series:
    if method is None:
        return series
    if method == "difference":
        return series.diff().dropna().reset_index(drop=True)
    if method == "stl_residual":
        from statsmodels.tsa.seasonal import STL
        if not isinstance(series.index, pd.DatetimeIndex):
            raise ValueError("stl_residual requires DatetimeIndex")
        stl = STL(series, robust=True).fit()
        return stl.resid.dropna().reset_index(drop=True)
    raise ValueError(f"unknown detrend method: {method}")


def _residuals(target: np.ndarray, z: np.ndarray) -> np.ndarray:
    model = OLS(target, add_constant(z)).fit()
    return np.asarray(model.resid)


def partial_residuals(
    x: np.ndarray, y: np.ndarray, z: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    return _residuals(x, z), _residuals(y, z)
