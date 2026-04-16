---
name: distribution_fit
description: Auto-select distribution candidates from data shape, rank by AIC with BIC cross-check, GOF via KS + Anderson-Darling. Hill estimator for heavy tails.
---

# Distribution Fit Skill

## Entry point

`fit` is available as a pre-injected sandbox global — no import needed.

```python
result = fit(
    series,                       # pd.Series or np.ndarray
    candidates="auto",            # or list[str] like ["normal", "lognormal", "gamma"]
    store=artifact_store,
    session_id=session_id,
)
# result.best                    FitCandidate(name, params, aic, bic, ks_p, ad_stat)
# result.ranked                  tuple[FitCandidate, ...]
# result.hill_alpha              float | None (heavy-tail estimate)
# result.qq_artifact_id          str  — Q-Q plot
# result.pdf_overlay_artifact_id str — PDF overlay
# result.outlier_threshold       float — p=0.001 tail under best fit
# result.outlier_indices         list[int]
```

## Candidate selection (when `candidates="auto"`)

- unbounded symmetric (skew ≈ 0) → `normal`, `t`, `laplace`
- positive, right-skew → `lognormal`, `gamma`, `weibull_min`, `pareto`
- bounded [0, 1] → `beta`, `uniform`
- discrete, count-like → (returns stub; scipy.stats.poisson/NB handled by future enhancement)

## Rules

- Minimum n=50 for fitting; below → raise.
- Ranks by AIC; BIC shown for cross-check in ranked list.
- KS test uses Lilliefors correction when parameters estimated from data.
- Outliers = values in tails where survival function < 0.001 under best fit.
