from __future__ import annotations

import numpy as np
import pandas as pd


def linear_xy(n: int, rho: float, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(n)
    noise = rng.standard_normal(n)
    y = rho * x + np.sqrt(max(0.0, 1 - rho ** 2)) * noise
    return x, y


def monotonic_nonlinear_xy(n: int, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    log_x = rng.uniform(-5.0, 5.0, n)
    x = np.exp(log_x)
    y = log_x + rng.normal(0, 0.1, n)
    return x, y


def noisy_groups(per_group: int, effect: float, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    a = rng.normal(0.0, 1.0, per_group)
    b = rng.normal(effect, 1.0, per_group)
    return pd.DataFrame(
        {
            "group": ["A"] * per_group + ["B"] * per_group,
            "value": np.concatenate([a, b]),
        }
    )


def seasonal_series(n: int, period: int, seed: int = 0) -> pd.Series:
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    trend = 0.01 * t
    seasonal = np.sin(2 * np.pi * t / period)
    noise = rng.normal(0, 0.3, n)
    idx = pd.date_range("2022-01-01", periods=n, freq="D")
    return pd.Series(trend + seasonal + noise, index=idx, name="y")


def heavy_tailed_series(n: int, seed: int = 0) -> pd.Series:
    rng = np.random.default_rng(seed)
    values = rng.pareto(1.8, n) + 1
    return pd.Series(values, name="heavy")


def simpsons_paradox_frame(seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    frames = []
    for stratum, (mean_x, slope) in enumerate(
        [(0.0, -0.6), (3.0, -0.6), (6.0, -0.6)]
    ):
        x = rng.normal(mean_x, 0.6, 120)
        y = slope * (x - mean_x) + mean_x * 1.5 + rng.normal(0, 0.3, 120)
        frames.append(
            pd.DataFrame({"stratum": str(stratum), "x": x, "y": y})
        )
    return pd.concat(frames, ignore_index=True)


def confounded_frame(seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    z = rng.normal(0, 1, 500)
    x = 0.9 * z + rng.normal(0, 0.4, 500)
    y = 0.9 * z + rng.normal(0, 0.4, 500)
    return pd.DataFrame({"confounder": z, "x": x, "y": y})
