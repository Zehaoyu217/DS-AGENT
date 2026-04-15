# Immortal Time Bias

**Slug:** `immortal_time_bias`
**One-liner:** Cohort definitions that guarantee survival during a look-back window inflate treatment effects.

## What it is

If a cohort is defined by an event that happened during a window (e.g., "patients who received drug X within 90 days of diagnosis"), the members are by construction alive for at least 90 days. Comparing their survival to a control that includes the first 90 days makes the treatment look protective — the time was immortal by definition.

## How to detect it

- Any cohort definition involving a time-varying eligibility event.
- Compare hazards over the window: a step-function drop at day 0 in the treated group is a red flag.

## Mitigation

- **Landmark analysis**: start the clock at a common landmark after the eligibility window, include only those alive at the landmark in both arms.
- **Time-varying treatment modeling**: treatment status varies over time in the model.
- Explicitly report the eligibility definition in methodology.

## See also

- `look_ahead_bias`
- `selection_bias`
- `survivorship_bias`
