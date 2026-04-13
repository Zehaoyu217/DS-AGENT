# Confounding

**Slug:** `confounding`
**One-liner:** A third variable drives both X and Y; the X↔Y correlation is real but causally misleading.

## What it is

A confounder Z causes both X and Y. Observed X↔Y correlation is genuine but reflects the shared cause, not a causal X→Y link. Without accounting for Z, any policy built on "increase X to change Y" is unfounded.

Classic example: ice cream sales and drownings rise together; temperature is the confounder.

## How to detect it

- Ask: could any variable plausibly cause both X and Y? List them by domain knowledge before running the test.
- Partial correlation (`correlation` skill with `partial_on=[z]`) strips the shared variance; a large drop from `r(x,y)` to `r(x,y|z)` is a confounding signature.
- `stat_validate` raises `confounder_risk` WARN when the claim is causal-shaped ("X causes Y", "X drives Y") and no `partial_on` or `controls` argument was used in the correlation call.

## Mitigation

- Add the confounder as a control: `correlate(x, y, partial_on=[z])` or explicit regression.
- Report the unadjusted and adjusted effect side by side.
- If you cannot measure Z, state the confounder hypothesis explicitly in the Finding's caveats.

## See also

- `simpsons_paradox`
- `spurious_correlation`
- `selection_bias`
