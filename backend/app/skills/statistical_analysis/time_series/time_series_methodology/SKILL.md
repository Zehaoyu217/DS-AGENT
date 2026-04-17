---
name: time_series_methodology
description: '[Reference] Deep methodology for time-series analysis — stationarity tests (ADF vs KPSS conjunction), STL decomposition, anomaly methods (seasonal-ESD vs robust-z), changepoint algorithms (PELT), lag correlation pitfalls. Load when the agent must justify a method choice, explain a stationarity verdict, or debug a counterintuitive result.'
version: '0.1'
---

# Time Series Methodology (Reference)

This skill is **methodology**, not API. The callable entry points (`characterize`,
`decompose`, `find_anomalies`, `find_changepoints`, `lag_correlate`) live in the
parent `time_series` skill. Load this skill when:

- A user asks **"why is this series flagged non-stationary?"** or **"why didn't lag
  correlate run?"**
- You need to choose between `find_anomalies(method=...)` modes.
- The decomposition's `dominant_period` looks wrong.
- You are writing a methodology section for a forecast or anomaly report.

---

## 1. Stationarity: the ADF + KPSS conjunction

`characterize()` declares a series **stationary** only when:

```
adf_p < 0.05  AND  kpss_p > 0.05
```

This is intentional. ADF and KPSS test opposite null hypotheses:

| Test | H₀ | H₁ |
|------|----|----|
| ADF (Augmented Dickey-Fuller) | "has a unit root" (non-stationary) | "stationary" |
| KPSS (Kwiatkowski-Phillips-Schmidt-Shin) | "stationary" | "has a unit root" |

A single test is easy to fool:

- ADF alone: an over-differenced series may falsely reject the unit root null.
- KPSS alone: a borderline trend-stationary series may fail to reject stationarity
  but actually have a slow drift.

The conjunction (reject ADF's null **and** fail to reject KPSS's null) gives a
**two-sided agreement** that the series behaves like a stationary process at the
chosen significance level.

### What the four outcomes mean

| ADF rejects? | KPSS rejects? | Verdict | What to do |
|--------------|---------------|---------|------------|
| Yes | No | **Stationary** | Proceed with stationary methods. |
| No | Yes | **Has unit root** | First-difference. |
| No | No | **Inconclusive** | Likely trend-stationary; try `detrend="stl_residual"` or `"difference"`. |
| Yes | Yes | **Inconclusive (heteroskedastic)** | Variance is not constant. Consider log transform or volatility model. |

`characterize()` reports `stationary=True` only in case 1. The other three return
`stationary=False`, and downstream methods like `lag_correlate` refuse to run unless
the caller passes `accept_non_stationary=True` (which is a deliberate code smell).

---

## 2. STL decomposition

`decompose(series, period=None)` runs **STL** (Seasonal-Trend decomposition using
LOESS, Cleveland et al. 1990) returning three additive components:

```
series = trend + seasonal + residual
```

Why STL over classical decomposition or X-13:

- **Robust to outliers.** STL uses LOESS smoothing, which down-weights anomalies
  rather than letting them propagate into the seasonal component.
- **Handles any period.** Classical decomposition assumes monthly/quarterly. STL
  takes any integer period.
- **No model spec required.** Unlike SARIMA-based decompositions, no order tuple to
  guess.

### When `period=None` auto-detection is wrong

Auto-detection runs autocorrelation, picks the highest peak above lag 1, and returns
the lag index. This works for clean monthly seasonality. It fails when:

- The series has **multiple seasonalities** (daily + weekly). It picks the strongest
  and ignores the other. → Pass `period=` explicitly to lock the period you care
  about, or use MSTL (not currently exposed).
- The series is **shorter than 2 full cycles**. Autocorrelation is noisy. → Pass the
  expected period from domain knowledge.
- The series has a **strong trend** that wasn't differenced first. The trend
  contaminates the autocorrelation. → Detrend first, then characterize.

### The residual is your anomaly signal

After STL, the `residual` component should look like white noise around zero. If it
doesn't (clusters of large values, persistent drift, fat tails), the decomposition
hasn't fully captured the structure — anomaly detection on this residual will
over-flag.

---

## 3. Anomaly detection

`find_anomalies(series, method="auto")` picks:

```
if dominant_period detected:
    return seasonal_esd
return robust_z
```

### Seasonal-ESD (Generalized ESD on STL residuals)

Procedure: STL-decompose, then run Generalized ESD on the residual.

- **Strength.** Handles seasonal data without flagging routine seasonal peaks as
  anomalies.
- **Weakness.** Requires `n ≥ ~50` for STL to be meaningful; needs a clear period.
  If `dominant_period` was wrong, every seasonal peak shows as an anomaly.

### Robust z-score (median + MAD)

Procedure: compute median and MAD (median absolute deviation), flag points where
`|x - median| / (1.4826 * MAD) > threshold`.

- **Strength.** No model assumptions, no period needed, works on any length.
- **Weakness.** Doesn't account for trend or seasonality — a series that is just
  growing will flag the most recent points as anomalies forever.

### Picking manually

| Situation | Pick |
|-----------|------|
| Clean stationary or detrended series, no seasonality | `robust_z` |
| Daily/weekly seasonal data, n ≥ 50 | `seasonal_esd` |
| Streaming / online anomaly flag (no batch context) | `robust_z` (but recompute window) |
| Series with trend AND seasonality | Detrend first, then `seasonal_esd` |
| Heavy-tailed innovations (financial returns) | Neither — use a volatility model. |

---

## 4. Changepoint detection

`find_changepoints(series, penalty=10.0)` runs **PELT** (Pruned Exact Linear Time,
Killick et al. 2012) with an L2 cost function.

PELT is exact (not heuristic) and has linear-time complexity. It segments the series
into pieces with different means/variances.

### Tuning `penalty`

The penalty controls the **bias-variance tradeoff** for segment count:

- `penalty=10.0` (default) — moderate sensitivity; suitable for series of length
  100–5000 with a few real changepoints.
- `penalty=5.0` — more sensitive; flags smaller shifts. Use when changepoints are
  expected to be subtle.
- `penalty=20.0` — stricter; only flags large shifts. Use when noise is high.
- BIC-style penalty: `3 * log(n)` is a reasonable starting point, where n is series
  length.

### Common pitfalls

- **Too many changepoints.** Penalty too low, or noise misread as shifts. Increase
  penalty.
- **Missing a known event.** The cost function assumes shifts in mean. If the change
  is in **variance only**, PELT under L2 will not find it. Use a different cost
  (not currently exposed) or test variance directly.
- **Changepoint at the boundary.** PELT often places one near the start or end
  because the segment is short and the cost is misleading. Filter out changepoints
  in the first/last 5% of the series.

---

## 5. Lag correlation

`lag_correlate(x, y, max_lag, accept_non_stationary=False)` computes Pearson
correlation between `x[t]` and `y[t-k]` for `k = -max_lag .. max_lag` and flags
`significant_lags`.

### Why the stationarity guard

If either series has a trend, `corr(x[t], y[t-k])` is dominated by the shared trend
and produces large coefficients at every lag. The "significant" lags are an
artifact, not a signal. The guard at `pre_tool_gate` raises unless the caller has
explicitly opted in via `accept_non_stationary=True` (which should be paired with a
narrative explanation that the result is a phase shift in trend, not a lead-lag
relationship).

### Reading the result

- `coefficients[max_lag + k]` is the correlation for lag `k`.
- `significant_lags` returns the integer lags whose Bonferroni-corrected p-value
  is below 0.05.
- A peak at positive lag `k` means **x leads y by k periods** (knowing x[t-k]
  predicts y[t]).
- A peak at negative lag `k` means y leads x by `|k|` periods.
- A peak at lag 0 with smaller peaks at ±1, ±2 is contemporaneous correlation
  bleeding through autocorrelation, not multiple lead-lag relationships.

### Bonferroni vs FDR

We use Bonferroni because the number of tested lags is small (`2 * max_lag + 1`,
typically < 100). For larger lag windows or multi-pair scans, switch to BH-FDR.

---

## 6. When to skip these tools entirely

| You want | Use instead |
|----------|-------------|
| Forecast | A forecasting model (ARIMA, ETS, Prophet, NN). Decomposition is descriptive, not predictive. |
| Causal inference | An identification strategy (RCT, IV, DiD). Lag correlation is at best a screening tool. |
| Multivariate volatility | A GARCH/MGARCH family model. STL won't help. |
| Regime detection | HMM or Markov-switching model. Changepoints find boundaries, not regimes. |

---

## 7. Reporting checklist

When you report time-series findings to a user, include:

- [ ] Series length and date range.
- [ ] Stationarity verdict + ADF p, KPSS p.
- [ ] Detrending applied (if any) and why.
- [ ] Dominant period (auto-detected or supplied), and confidence in it.
- [ ] Anomaly method used and threshold.
- [ ] Changepoint penalty used.
- [ ] Lag correlation only with a stationarity statement.
- [ ] At least one chart (decomposition, anomaly overlay, or lag-corr stem plot).

---

## 8. References

- Cleveland, Cleveland, McRae & Terpenning (1990). *STL: A Seasonal-Trend
  Decomposition Procedure Based on Loess.* Journal of Official Statistics.
- Hyndman & Athanasopoulos (2021). *Forecasting: Principles and Practice* (3rd ed),
  ch. 3 (decomposition), ch. 9 (ARIMA). Free online.
- Killick, Fearnhead & Eckley (2012). *Optimal detection of changepoints with a
  linear computational cost.* JASA. — PELT.
- Rosner (1983). *Percentage Points for a Generalized ESD Many-Outlier Procedure.*
  Technometrics. — ESD.
- Kwiatkowski, Phillips, Schmidt & Shin (1992). *Testing the null hypothesis of
  stationarity against the alternative of a unit root.* Journal of Econometrics.
