# Statistical Gotchas Index

One-liner per gotcha. Full bodies at `<slug>.md`. This file is injected into the system prompt; full bodies load on-demand when `stat_validate` flags them.

- **base_rate_neglect** — Ignoring prior probability when interpreting a test result or conditional claim.
- **berksons_paradox** — Selection into a sample creates spurious negative correlation between independent traits.
- **confounding** — A third variable drives both X and Y; the X↔Y correlation is real but causally misleading.
- **ecological_fallacy** — Inferring individual-level relationships from group-level aggregates.
- **immortal_time_bias** — Cohort definitions that guarantee survival during a look-back window inflate treatment effects.
- **look_ahead_bias** — Using information not available at the time of the event (train leakage, future joins).
- **multicollinearity** — Highly correlated predictors inflate standard errors and swap coefficient signs.
- **multiple_comparisons** — Running many tests without correction turns noise into "discoveries".
- **non_stationarity** — Mean/variance/autocorrelation drift invalidates correlations, tests, and models assuming iid data.
- **regression_to_mean** — Extreme values move toward the mean on remeasurement; pre-post designs without controls fake treatment effects.
- **selection_bias** — Conditioning on the outcome or a non-random sample breaks inference about the population.
- **simpsons_paradox** — A trend visible in subgroups reverses when aggregated (or vice versa).
- **spurious_correlation** — Two unrelated series share trend/seasonality and look correlated without a real link.
- **survivorship_bias** — Analyzing only survivors (funds, firms, patients) biases results toward positive outcomes.
