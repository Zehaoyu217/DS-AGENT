---
name: chart_picker
description: 'Decision tree for picking the right chart type from intent and data shape. Returns a template name from the altair_charts catalog. Load this BEFORE altair_charts whenever the right template is not obvious — e.g. "show change over time", "compare across categories", "explain why two variables relate".'
version: '0.1'
---

# chart_picker

This skill is a **decision tree**, not a renderer. It maps **analyst intent + data
shape** to a specific template from the `altair_charts` sub-skill. Load this skill
when the agent is about to chart something but isn't certain which template fits.

## When to use

- You know **what question the chart should answer**, but you don't yet know which
  template to call.
- You are tempted to drop to raw Altair because nothing seems to fit — let the
  decision tree confirm that's true before you do.
- You need to **defend the choice** to a user ("why a slope chart and not a bar?").

## Entry point

Pre-injected as a sandbox global:

```python
suggestion = pick_chart(
    intent="compare across categories",   # see "Intent vocabulary" below
    data_shape={
        "rows": 12,
        "x_type": "nominal",              # quantitative | nominal | ordinal | temporal
        "y_type": "quantitative",
        "n_series": 1,                    # 1 means single-series; 2+ means multi-series
        "n_categories": 12,
        "has_periods": False,             # True if "before/after" or "Q1/Q2"
        "has_target": False,              # True if a baseline/target value to compare to
    },
)
# suggestion.template       → 'bar'
# suggestion.alternates     → ['lollipop', 'grouped_bar']  (if any)
# suggestion.reason         → human-readable justification
# suggestion.confidence     → 0.0..1.0
# suggestion.fallback_layer → 1 | 2 | 3 | 4  (which doctrine layer to compose at)
```

## Intent vocabulary

The `intent` argument is one of these short verbs (synonyms collapse to the same
branch):

| Intent | Synonyms | Tree branch |
|--------|----------|-------------|
| `compare` | `rank`, `compare across categories` | comparison templates |
| `trend` | `over time`, `time series`, `evolution` | time-series templates |
| `distribution` | `spread`, `histogram` | distribution templates |
| `relationship` | `correlate`, `regress`, `scatter` | relationship templates |
| `composition` | `breakdown`, `parts of whole`, `stacked` | composition templates |
| `change` | `before vs after`, `delta`, `change between two points` | flow / change templates |
| `forecast` | `actual vs forecast`, `projection`, `plan vs actual` | actual_vs_forecast |

Anything else → `intent="other"` returns `template=None` and a non-empty `alternates`
list of close matches.

## The decision tree

### `intent="compare"`

```
n_series == 1?
├── n_categories ≤ 8       → bar
├── n_categories ∈ 9..30   → lollipop  (long names sort cleanly)
├── n_categories > 30      → bar  (apply top-N filter first; warn in suggestion.reason)
n_series ≥ 2?
└── grouped_bar  (alternate: stacked_bar if values are parts of a whole)

has_target=True             → bar_with_reference
```

### `intent="trend"`

```
n_series == 1                                → multi_line  (single series)
n_series ≥ 2                                 → multi_line  with series_role mapping
intent contains "vs forecast" or "projection" → actual_vs_forecast
data_shape.has_periods AND n=2 periods       → slope  (already on the change branch)
faceting requested OR n_series > 8           → small_multiples
"cumulative" or "running"                    → area_cumulative
"range" or "low/high band"                   → range_band
```

### `intent="distribution"`

```
n_series == 1                                → histogram
"smooth" or "density"                        → kde
n_series ≥ 2 AND grouped                     → boxplot   (alternate: violin if n large per group)
"compare full distributions, not summaries"  → ecdf
```

### `intent="relationship"`

```
2 numeric columns                            → scatter_trend
≥ 3 numeric columns                          → correlation_heatmap
"residuals" or "regression diagnostic"       → scatter_trend with trend="poly"
```

### `intent="composition"`

```
share of total over time              → stacked_bar with mode="percent"
share of total at one point in time   → stacked_bar with mode="absolute" + filter
```

### `intent="change"`

```
exactly 2 periods                     → slope
running totals with positive/negative deltas → waterfall
two endpoints per category            → dumbbell
```

### `intent="forecast"`

```
actuals + forecast (with/without CI band)  → actual_vs_forecast
```

## When the tree returns `None`

`pick_chart` returns `template=None` when **no template fits**. This signals layer-2
composition (compose two templates) or layer-3 themed raw. The `alternates` list
gives candidate templates for composition, and `fallback_layer` indicates whether
to compose (2), drop to themed raw (3), or drop to raw Altair (4).

A cardinal rule: do not silently pick a template that "kind of fits". Returning
`None` and forcing composition is the right answer when the analyst question doesn't
match any single chart type.

## Reading the `confidence` field

| Range | Meaning |
|-------|---------|
| `≥ 0.85` | Tree had a clean match. Use the template as-is. |
| `0.6..0.85` | Tree matched but data shape stretches the template. Read `reason`. |
| `< 0.6` | Best-effort match. Consider explicitly asking the user. |

## Examples

```python
# Headline metric across regions
pick_chart(intent="compare", data_shape={
    "rows": 10, "x_type":"nominal", "y_type":"quantitative",
    "n_series": 1, "n_categories": 10,
})
# → bar  (confidence 0.95)

# Daily revenue over 2 years, with a forecast
pick_chart(intent="forecast", data_shape={
    "rows": 730, "x_type":"temporal", "y_type":"quantitative",
    "n_series": 2, "has_periods": False,
})
# → actual_vs_forecast  (confidence 0.97)

# Conversion rate before vs after rollout
pick_chart(intent="change", data_shape={
    "rows": 24, "x_type":"nominal", "y_type":"quantitative",
    "n_series": 1, "n_categories": 12, "has_periods": True,
})
# → slope  (confidence 0.93)
```

## Anti-patterns the tree explicitly avoids

- **Pie / donut.** Not in the catalog. Use `stacked_bar(mode="percent")` for parts of
  whole — comparisons across categories are easier on bars than on angle.
- **Dual-axis line chart.** Not in the catalog. Use `alt.vconcat` of two line charts
  with shared x-axis instead.
- **3D bar.** Hard no.
- **Word cloud.** Not a chart.

## Contract

`pick_chart` is pure: same arguments produce the same suggestion. It does not read
the DataFrame; the caller summarizes data shape and passes it as a dict. This makes
the picker fast and deterministic, and lets the agent explain the reasoning to the
user without rerendering.
