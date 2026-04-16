---
name: altair_charts
description: 20 pre-themed Altair chart templates (bar, grouped_bar, stacked_bar, bar_with_reference, lollipop, dumbbell, multi_line, actual_vs_forecast, area_cumulative, range_band, small_multiples, histogram, kde, boxplot, violin, ecdf, scatter_trend, correlation_heatmap, slope, waterfall). Theme resolves colors and strokes.
version: '0.2'
---
# altair_charts

Pre-themed Altair chart templates. Every template takes a DataFrame plus field mappings and returns an `alt.Chart` fully themed by the active variant. Agents should reach for these FIRST before writing raw Altair. All templates are available as pre-injected sandbox globals.

## When to use

Default for all chart rendering. Falls through to raw Altair only if no template fits.

## Layer doctrine

1. Templates (this skill) — first choice.
2. Composed — `alt.layer`, `alt.hconcat`, `alt.vconcat` of templates.
3. Themed raw — raw Altair with theme already active.
4. Raw Altair — last-resort escape hatch.

## Series roles

Every template that draws multiple series takes a `series_role` field mapping rather than color literals. Roles (`actual`, `primary`, `secondary`, `reference`, `projection`, `forecast`, `scenario`, `ghost`) resolve to the 8 named blues with role-specific strokes. Never pass hex colors.

---

## Comparison templates

**`bar(df, x, y, category=None, title=None)`**
Simple bar chart. Pass `category` to get a side-by-side grouped view using offset encoding.

**`grouped_bar(df, x, y, category, title=None)`**
Dedicated grouped bar — explicit `category` required; uses xOffset encoding for side-by-side groups.

**`stacked_bar(df, x, y, category, mode="absolute", title=None)`**
Stacked bar. `mode="absolute"` (default) or `mode="percent"` for 100% stacking.

**`bar_with_reference(df, x, y, reference_value, reference_label=None, title=None)`**
Bars with a horizontal reference line (e.g. target, average). `reference_value` is a scalar float.

**`lollipop(df, category, value, title=None)`**
Horizontal lollipop sorted descending by value. Good alternative to bar when category names are long.

**`dumbbell(df, category, start, end, title=None)`**
Two-endpoint dumbbell per category — shows change between two periods. `start` gets `ghost` role, `end` gets `actual`.

---

## Time-series templates

**`multi_line(df, x, y, series_role, title=None)`**
Multi-line chart. `series_role` maps series values to named roles (`actual`, `reference`, `forecast`, etc.) that resolve stroke weight and color.

**`actual_vs_forecast(df, x, actual, forecast, forecast_low=None, forecast_high=None, reference_value=None, scenario=None, title=None)`**
Flagship time-series template. Actuals as solid line, forecast as dashed, optional confidence band (forecast_low/high), optional reference line, optional scenario band.

**`area_cumulative(df, x, y, title=None)`**
Running cumulative area chart. `x` can be temporal or quantitative; auto-detected. Uses `primary` series role.

**`range_band(df, x, low, high, mid=None, title=None)`**
Shaded band between `low` and `high`. Optional `mid` line (e.g. median within a range). Uses `scenario` fill + `reference` midline.

**`small_multiples(df, x, y, facet, columns=3, title=None)`**
Faceted line chart wrapped into a grid. `facet` is the column to split on; `columns` controls wrap width.

---

## Distribution templates

**`histogram(df, field, bins=30, title=None)`**
Basic histogram with bin count control.

**`kde(df, value, group=None, title=None)`**
Kernel density estimate. Optional `group` draws overlapping densities per category.

**`boxplot(df, field, group=None, title=None)`**
Box-and-whisker. Optional `group` splits into side-by-side boxes per category.

**`violin(df, value, group, title=None)`**
Violin plot using KDE density transform. `group` is required (use boxplot for ungrouped distribution).

**`ecdf(df, value, group=None, title=None)`**
Empirical CDF (step function). Optional `group` overlays multiple ECDFs. Good for comparing distributions without binning artifacts.

---

## Relationship templates

**`scatter_trend(df, x, y, trend="linear", title=None)`**
Scatter plot with regression trend line. `trend` accepts `"linear"`, `"poly"`, or `None`.

**`correlation_heatmap(df, fields=None, title=None)`**
Pairwise correlation matrix using diverging palette. `fields=None` uses all numeric columns.

---

## Flow / change templates

**`slope(df, category, period, value, title=None)`**
Slope chart showing directional change across exactly two periods. `period` should have 2 distinct values.

**`waterfall(df, step, delta, kind=None, title=None)`**
Classic waterfall chart. `delta` is the incremental value per step. `kind` column marks `"total"` rows for absolute bars; omit for pure delta.

---

## Errors

All templates raise `KeyError` with a message naming the missing field(s) and listing the actual columns available.
