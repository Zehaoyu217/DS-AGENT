---
name: correlation_methodology
description: '[Reference] Deep methodology for correlation analysis — when to pick Pearson vs Spearman vs Kendall vs distance vs partial; bootstrap CI rationale; nonlinearity detection; NA handling philosophy. Load when the agent must justify a method choice, debug an unexpected coefficient, or explain CI width to a user.'
version: '0.1'
---

# Correlation Methodology (Reference)

This skill is **methodology**, not API. The callable entry point is `correlate(...)` from the parent `correlation` skill. Load this skill when:

- A user asks **"why did you pick Spearman?"** or **"why is the CI so wide?"**
- The result has `nonlinear_warning=True` and you need to explain it to the user.
- You are choosing between `partial_on=`, `detrend=`, or rejecting non-stationary input.
- The coefficient disagrees with a naive `df.corr()` — you need to explain what `correlate` did differently.
- You are writing a methodology section for an analytical report.

---

## 1. Choosing a method

The `method="auto"` resolver applies a single rule:

```
if abs(r_spearman) - abs(r_pearson) > 0.10:
    return "spearman"
return "pearson"
```

This rule comes from the empirical observation that monotonic-but-nonlinear relationships
(power-law, log-linear, sigmoid in the linear regime) lift Spearman above Pearson by
more than 0.1 well before they break Pearson's interpretability. Below 0.1 the two
estimators agree to within sampling noise on most real data, so we default to Pearson
because its CI is tighter and it has a closed-form null distribution.

### When to override `auto`

| You want | Use | Why |
|----------|-----|-----|
| The classic linear association | `"pearson"` | Maximum power if data is bivariate-normal-ish. |
| Rank-only association, robust to outliers | `"spearman"` | Invariant under monotonic transforms; immune to single-point leverage. |
| Small-n ordinal or tied data | `"kendall"` | Better small-sample distribution than Spearman; handles ties cleanly. |
| Nonlinear, possibly non-monotonic | `"distance"` | Distance correlation is 0 iff variables are independent (Pearson is 0 iff uncorrelated, which is weaker). |
| Effect after controlling for a covariate | partial via `partial_on=[z]` | Removes linear influence of z from both x and y, then correlates the residuals. |

### Why we never silently use Pearson

`pandas.DataFrame.corr()` defaults to Pearson and silently drops NaN pairwise. That
hides three real bugs:

1. **Nonlinear monotonic relationships look weak.** A perfect log-linear pair
   `y = log(x)` returns `r ≈ 0.92`, not 1.0. Spearman returns 1.0.
2. **Sample size shrinkage is invisible.** If 60% of pairs have a NaN in either
   column, the reported `r` is computed on the surviving 40% with no warning.
3. **Outliers dominate.** A single leverage point can flip the sign of Pearson on
   small `n`. Spearman/Kendall are immune.

`correlate(...)` always reports `n_effective` and `na_dropped`, and sets
`nonlinear_warning=True` when the gap exceeds the threshold.

---

## 2. Bootstrap confidence intervals

We default to **1000 bootstrap resamples** rather than the closed-form Fisher-z CI
because:

- Fisher's z transform assumes bivariate normality. Real data is rarely normal.
- Fisher's z is undefined for `|r| ≥ 1`, which happens with small-n ranked data.
- Bootstrap gives a CI for **any** estimator (Pearson, Spearman, Kendall, distance,
  partial) using the same code path — no special cases.
- Bootstrap CIs are honest about heavy tails and skew.

### Reading the CI width

| Width | Meaning |
|-------|---------|
| `< 0.10` | Tight estimate — n is large or the relationship is strong. |
| `0.10–0.30` | Typical for n = 50–200 with moderate r. Treat point estimate as approximate. |
| `> 0.30` | Wide. Either small n, weak r, or both. **Do not report a single number** — report the interval. |

### When to bump `bootstrap_n`

- Default 1000 is fine for reporting a CI.
- Bump to 5000 if the CI bounds are reported to two decimals **and** users will make
  a quantitative decision on the bound (not the point).
- Bump to 10000 only for publication-quality reporting; the CI bound stabilizes by
  then to within ±0.005.

---

## 3. Detecting nonlinearity

The `nonlinear_warning` flag fires when `|r_spearman| - |r_pearson| > 0.10`. This is a
**screening signal**, not a diagnosis. When it fires, the next steps depend on shape:

| Visual shape | Likely cause | Action |
|--------------|--------------|--------|
| Curved-but-monotonic | Power, log, sigmoid in linear regime | Spearman is the right number. Mention curvature in narrative. |
| U-shape / inverted-U | True nonmonotonic | Pearson AND Spearman are both bad summaries. Report distance correlation; consider polynomial regression or piecewise. |
| Two clusters | Simpson's paradox / mixture | Stratify and report per-stratum correlations. The pooled number is misleading. |
| Outlier-driven | Single leverage point | Spearman/Kendall reflect the truth; Pearson is the bug. |

The artifact returned by `correlate()` always includes a scatter chart with a smoother
overlaid — eyeball that chart before believing any single coefficient.

---

## 4. Partial correlation

`partial_on=[z]` regresses `x` and `y` separately on `z` (OLS), then correlates the
residuals. This isolates the x-y association from any common dependence on z.

### When to use

- **Confounding suspected.** "Sales correlates with ad spend, but maybe both just
  scale with season." → `partial_on=["season_index"]`.
- **Mediator removal.** You want the direct association after controlling for a
  known mediator.

### When **NOT** to use

- The covariate is itself an outcome of x (downstream effect). Conditioning on a
  collider opens a non-causal path and introduces spurious correlation. This is the
  classic "selection bias" mistake.
- The covariate has fewer than ~30 unique values for n < 200. The OLS residuals
  become noisy and the reported `r` overstates precision.

For more than one covariate, pass a list: `partial_on=["season", "region_code"]`.
The implementation regresses against all covariates jointly.

---

## 5. Non-stationary inputs

For two time-indexed series, raw correlation is meaningless if either is non-stationary
— a shared trend produces large `r` even when there is no relationship between the
innovations. `correlate(...)` refuses to run on inputs that fail ADF without an
explicit `detrend=` choice.

| `detrend=` | What it does | When to pick it |
|------------|--------------|-----------------|
| `None` | No transform. Raises on non-stationary. | You believe both series are stationary in level. |
| `"difference"` | First differences `x[t] - x[t-1]`. | Series has a unit root or linear trend. Standard for financial returns. |
| `"stl_residual"` | STL decomposition, keep residual. | Series has both trend and seasonality. |

After detrending, you are correlating **innovations**, not levels. State this in the
narrative: "After first-differencing both series, the correlation of returns is r = X."

---

## 6. NA handling

`handle_na` has three modes, and the default is deliberately the loudest:

- `"report"` (default) — Drop pairs with any NaN, return `n_effective` and
  `na_dropped` so the caller sees the loss.
- `"drop"` — Same drop, but suppress the count fields. Use only inside an automated
  pipeline that has already validated upstream.
- `"fail"` — Raise on any NaN. Use when missingness itself is a data quality bug
  that must surface.

### Why `"report"` is the default

Pairwise drop is the only honest default. Listwise drop (when there are >2 columns)
discards rows where ANY column is NaN, which over-drops. Imputation invents data and
biases the coefficient toward whatever the imputer assumes (mean → toward zero,
KNN → toward the local pattern). Reporting the drop count puts the burden of
interpretation on the caller, which is where it belongs.

---

## 7. Reporting checklist

When you report a correlation result to a user, include:

- [ ] Method used (`result.method_used`).
- [ ] Coefficient with 2-decimal precision.
- [ ] CI as `[low, high]` — never a bare standard error.
- [ ] `n_effective` if `na_dropped > 0`.
- [ ] Nonlinearity warning if `nonlinear_warning=True` — say what you did with it.
- [ ] Detrend transform if applied.
- [ ] Partial covariate(s) if applied.
- [ ] The scatter artifact (the chart is the report; the number is the headline).

A good one-liner:

> "Pearson r = 0.74 [0.62, 0.83], n=180. Spearman agreement (Δ=0.03) confirms
> linear relationship. No detrending applied; both series are stationary in level."

A bad one-liner:

> "The correlation is 0.74."

---

## 8. References

- Fisher, R. A. (1915). *Frequency distribution of the values of the correlation
  coefficient in samples of an indefinitely large population.* Biometrika.
- Székely, Rizzo & Bakirov (2007). *Measuring and testing dependence by correlation
  of distances.* Annals of Statistics. — distance correlation.
- Efron & Tibshirani (1993). *An Introduction to the Bootstrap.* — CI methodology.
- Pearl, J. (2009). *Causality.* — partial correlation as adjustment + collider bias.
