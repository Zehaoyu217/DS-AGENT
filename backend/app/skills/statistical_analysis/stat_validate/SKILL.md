---
name: stat_validate
description: PASS/WARN/FAIL gate for any inferential claim. Checks effect size, sample size, multiple comparisons, Simpson's paradox, confounders, leakage. Must be called before promoting a Finding.
---

# Stat Validate Skill

## When to use

Before promoting any quantitative or inferential claim to a Finding. Harness guardrail blocks `promote_finding` if no `stat_validate` with `verdict=PASS` exists in the current turn trace.

## Entry point

```python
from app.skills.stat_validate import validate

verdict = validate(
    claim_kind="correlation",      # "correlation"|"group_diff"|"regression"|"classifier"|"forecast"
    payload=correlation_result.to_dict(),
    turn_trace=current_turn,       # list[dict] — used for multi-comparison count
    frame=df,                       # optional — enables Simpson's and segmentation checks
    stratify_candidates=("segment", "region"),
    claim_text="Price negatively drives quantity",  # for causal-shape detection
)
# verdict.status          "PASS" | "WARN" | "FAIL"
# verdict.failures         tuple[Violation, ...] — severity HIGH
# verdict.warnings         tuple[Violation, ...]
# verdict.passes           tuple[Check, ...]
# verdict.gotcha_refs      tuple[str, ...] — slugs to read
```

## Rules

Checks run in order:
1. **Effect-size gate** — FAIL if CI entirely within negligible band (|effect| < 0.10 for d/r/delta).
2. **Sample-size gate** — FAIL on n < 10 per group.
3. **Multiple-comparisons** — WARN if turn_trace shows >5 tests at α<0.05 without correction.
4. **Assumption passthrough** — HIGH warn on Shapiro/Levene flags (already in upstream payload).
5. **Simpson's paradox** — if `frame` + `stratify_candidates` given: recompute by stratum, FLIP → FAIL, shrink→WARN.
6. **Confounder risk** — WARN on causal-shape claim text without `partial_on` or `controls` in payload.
7. **Spurious correlation heuristic** — WARN if both inputs non-stationary and no `detrend` applied.
8. **Look-ahead / leakage** — checks `as_of` alignment in payload metadata, WARN on violation.

`gotcha_refs` slug each maps to `knowledge/gotchas/<slug>.md` via `load_gotcha`.
