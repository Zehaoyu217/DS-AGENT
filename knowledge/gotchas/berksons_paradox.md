# Berkson's Paradox

**Slug:** `berksons_paradox`
**One-liner:** Selection into a sample creates spurious negative correlation between independent traits.

## What it is

Conditioning on being in a sample (e.g., hospitalized, admitted to a program, funded by a VC) can induce a negative correlation between two independently positive traits because having at least one is required for admission. In hospital patients, disease A and disease B look inversely correlated even when independent in the general population.

## How to detect it

- Is the sample filter plausibly correlated with multiple included variables?
- Check the correlation in an unfiltered reference population where possible.

## Mitigation

- Run the analysis on the unfiltered population, or a randomly-sampled subset.
- Report "inside the hospital, A and B appear inversely correlated; this may be Berkson's, not a real effect" in caveats.

## See also

- `selection_bias`
- `survivorship_bias`
- Reference: Berkson (1946), Biometrics
