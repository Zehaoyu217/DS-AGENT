---
name: altair_charts
description: 20 pre-themed chart templates (bar, multi_line, histogram, scatter_trend, boxplot, correlation_heatmap, and more). Theme resolves colors and strokes; templates never take color args.
level: 1
version: '0.1'
---
# altair_charts

Pre-themed Altair chart templates. Every template takes a DataFrame plus field mappings and returns an `alt.Chart` fully themed by the active variant. Agents should reach for these FIRST before writing raw Altair.

## When to use

Default for all chart rendering. Falls through to raw Altair only if no template fits.

## Layer doctrine

1. Templates (this skill) — first choice.
2. Composed — `alt.layer`, `alt.hconcat`, `alt.vconcat` of templates.
3. Themed raw — raw Altair with theme already active.
4. Raw Altair — last-resort escape hatch.

## Series roles

Every template that draws multiple series takes a `series_role` field mapping rather than color literals. Roles (`actual`, `primary`, `secondary`, `reference`, `projection`, `forecast`, `scenario`, `ghost`) resolve to the 8 named blues with role-specific strokes.

## Templates shipped in this phase (6 of 20)

- `bar(df, x, y, category=None)` — simple and grouped.
- `multi_line(df, x, y, series_role)` — time-series with role-typed strokes.
- `histogram(df, field, bins=30)` — distribution.
- `scatter_trend(df, x, y, trend="linear")` — x vs y with regression line.
- `boxplot(df, field, group=None)` — distribution grouped.
- `correlation_heatmap(df, fields=None)` — diverging palette, square matrix.

Remaining 14 ship in Plan 4.
