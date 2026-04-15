# Simpson's Paradox

**Slug:** `simpsons_paradox`
**One-liner:** A trend visible in subgroups reverses when aggregated (or vice versa).

## What it is

A correlation or difference visible inside every subgroup points one way, yet the same relationship aggregated across subgroups points the other way. This happens when group sizes are unequal and group membership is correlated with both X and Y. The paradox is entirely arithmetic — no statistical trickery — yet it flips the practical interpretation of the result.

Classic example: a hospital whose overall mortality rate is higher than a second hospital's, even though it has lower mortality in every severity stratum, because it admits sicker patients.

## How to detect it

- Whenever you report a pooled correlation, slope, or rate: also compute it per stratum for every categorical covariate you have. If the sign flips or magnitude shrinks meaningfully, investigate.
- `stat_validate` runs a Simpson's check when it sees a single-number claim and you have a categorical column with >1 level in the frame.
- Watch for large imbalance in subgroup sizes (hospital example: one hospital mostly low-severity, the other mostly high-severity).

## Mitigation

- Report stratified results alongside the pooled number; lead with the stratified version if the pooled one is misleading.
- If the goal is a causal conclusion, use adjustment (regression, stratification, weighting) rather than the pooled number.
- Flag the stratification variable as a confounder candidate; see `confounding`.

## See also

- `confounding`
- `ecological_fallacy`
- Reference: Pearl, "Simpson's Paradox: An Anatomy" (UCLA TR)
