# Ecological Fallacy

**Slug:** `ecological_fallacy`
**One-liner:** Inferring individual-level relationships from group-level aggregates.

## What it is

A correlation between group means does not imply the same correlation at the individual level. Countries with higher average income have different outcomes than rich-vs-poor individuals within any one country. Treating aggregate associations as individual-level claims is the ecological fallacy.

## How to detect it

- Claims of the form "X is correlated with Y" when the unit of observation is `country`, `state`, `month`, etc., but the narrative is about individuals.
- `stat_validate` checks the grouping level recorded in the turn trace against the claim language.

## Mitigation

- Restate claims at the unit of observation: "countries with higher X have higher Y" — not "people with higher X have higher Y".
- Run a multilevel model if you have individual-level data nested in groups.

## See also

- `simpsons_paradox`
- `confounding`
