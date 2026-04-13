# Multiple Comparisons

**Slug:** `multiple_comparisons`
**One-liner:** Running many tests without correction turns noise into "discoveries".

## What it is

Each hypothesis test at α=0.05 has a 5% false-positive rate. Run 20 independent tests on random data and you expect one "significant" result. Pick the best-looking one and report its p-value, and you've published a lie.

## How to detect it

- Count the tests: every pairwise comparison, every exploratory correlation, every subgroup analysis is a test.
- `stat_validate` counts tests in the current turn via the turn trace; >5 tests at α<0.05 without correction → WARN.
- Watch for "we tried everything and only this worked" narratives in scratchpad COT.

## Mitigation

- **Bonferroni** (`α/m`) for a small number of pre-specified tests; conservative.
- **Benjamini-Hochberg FDR** for exploratory screens; controls expected proportion of false discoveries.
- Split the data: discovery set (exploratory) and validation set (confirm only the surviving hypotheses with corrected α).
- Pre-register the tests you plan to run — the cleanest fix.

## See also

- `spurious_correlation`
- `look_ahead_bias`
