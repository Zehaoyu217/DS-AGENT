# Regression to the Mean

**Slug:** `regression_to_mean`
**One-liner:** Extreme values move toward the mean on remeasurement; pre-post designs without controls fake treatment effects.

## What it is

If a unit was selected because it had an extreme value, its next measurement is, on average, less extreme. Any "intervention" applied between the two measurements gets credit for the regression — which would have happened with no intervention at all.

Classic: athletes featured on Sports Illustrated slump the next season ("the SI curse"). They were featured because they had an extreme good run; reversion is the expected behavior.

## How to detect it

- Was the sample selected on the basis of a pre-intervention value being high or low?
- If yes, any pre→post change estimate without a control group is suspect.
- `stat_validate` flags pre-post paired comparisons that lack a named control group.

## Mitigation

- Add a control group selected by the same criterion; the treatment effect is the difference-in-differences, not the pre-post change of the treated group.
- For individual cases, caveat the estimate.
- If no control exists, use a historical counterfactual (base rate of reversion for similar units).

## See also

- `selection_bias`
- `non_stationarity`
