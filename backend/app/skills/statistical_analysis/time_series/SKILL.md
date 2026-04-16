---
name: time_series
description: Stationarity, decomposition, anomaly detection, changepoints, lag correlation. Refuses non-stationary lag-corr without explicit override.
---

# Time Series Skill

## Entry points

All five functions are pre-injected sandbox globals — no import needed.

```python
char = characterize(series)
#   .stationary (bool, ADF_reject AND NOT KPSS_reject)
#   .adf_p, .kpss_p, .trend_slope, .dominant_period, .autocorrelation_lag1

dec = decompose(series, period=None)  # STL
#   .trend, .seasonal, .residual

anomalies = find_anomalies(series, method="auto")  # seasonal_esd | robust_z
#   .indices (list[int]), .values, .method_used

cps = find_changepoints(series, penalty=10.0)
#   .indices, .segments

lc = lag_correlate(x, y, max_lag=30, accept_non_stationary=False)
#   .coefficients (array), .significant_lags
```

## Rules

- `characterize()` declares stationary only if ADF p<0.05 AND KPSS p>0.05.
- `decompose()` auto-detects period if `period=None` (from autocorrelation).
- `find_anomalies(method="auto")` picks seasonal_esd if period detected, robust_z otherwise.
- `lag_correlate()` **refuses** to run on non-stationary inputs unless `accept_non_stationary=True`. Guardrail enforces this at pre_tool_gate.
- All entry points accept DatetimeIndex-backed `pd.Series`; `characterize` accepts bare numpy arrays too.
