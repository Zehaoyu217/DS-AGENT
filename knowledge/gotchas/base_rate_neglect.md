# Base Rate Neglect

**Slug:** `base_rate_neglect`
**One-liner:** Ignoring prior probability when interpreting a test result or conditional claim.

## What it is

P(disease | positive test) ≠ sensitivity. If prevalence is 1% and the test has 99% sensitivity and 99% specificity, P(disease | +) ≈ 50%, not 99%. People routinely read off sensitivity as the answer and act on it.

## How to detect it

- Any conditional claim ("users who did X are Y% likely to churn") — is the base rate of Y reported alongside?
- Classifier reports with only precision/recall and no class balance.
- `stat_validate` flags a probability claim that lacks a prevalence/base-rate companion.

## Mitigation

- Always show the base rate next to the conditional.
- Report **lift** (conditional / base) rather than raw conditional.
- For classifiers, report PPV and NPV at the operating point given the actual class prevalence, not just recall.

## See also

- `spurious_correlation`
