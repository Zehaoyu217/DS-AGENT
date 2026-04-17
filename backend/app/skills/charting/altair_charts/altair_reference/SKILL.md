---
name: altair_reference
description: '[Reference] Deep reference for the project Altair theme — series roles & color resolution, layer doctrine (templates → composed → themed raw → raw), grammar-of-graphics fundamentals, encoding rules, theme escape hatches. Load when an agent needs to compose templates, write themed raw Altair, or debug a chart that renders wrong.'
version: '0.1'
---

# Altair Reference

This skill is **methodology and reference**, not the chart catalog. The catalog
lives in the parent `altair_charts` skill (20 named templates with field signatures).
Load this skill when:

- A user asks **"why is this color what it is?"** or **"can I add an annotation?"**
- You need to **compose two templates** with `alt.layer` / `alt.hconcat` / `alt.vconcat`.
- You hit the limits of the catalog and must drop to **themed raw Altair** without
  breaking the look-and-feel.
- You are debugging an unexpected color, axis, or stroke.

---

## 1. The four-layer doctrine

```
1. Templates      ← first choice. Catalog of 20 in altair_charts.
2. Composed       ← compose templates with alt.layer / alt.hconcat / alt.vconcat.
3. Themed raw     ← raw Altair with the project theme already active.
4. Raw Altair     ← last-resort escape hatch. Loses theming guarantees.
```

You should be at the lowest layer that solves the problem. Each step down loses
guarantees:

- Step **1 → 2**: still themed, but you own the layout decision.
- Step **2 → 3**: you own the encoding decisions; you must respect the role mapping.
- Step **3 → 4**: nothing is guaranteed; you've left the design system.

If you find yourself at layer 4, write a brief note in the artifact metadata
explaining why no template fit — that note is a feature request for the next
template.

---

## 2. Series roles, not colors

Every multi-series template takes a `series_role` mapping:

```python
series_role={"sales_q1": "actual", "forecast_q1": "forecast"}
```

The roles are **semantic**, not chromatic. The theme resolves them:

| Role | Default visual | Use for |
|------|----------------|---------|
| `actual` | Solid line, primary blue | Realized observed values. |
| `primary` | Solid line, primary blue | The headline series in single-line charts. |
| `secondary` | Solid line, secondary blue | A comparison series equal in importance. |
| `reference` | Dashed line, neutral | Targets, baselines, averages. |
| `projection` | Dotted line, projection blue | Plan / projection (committed). |
| `forecast` | Dashed line, projection blue | Model forecast (uncertain). |
| `scenario` | Filled band, low alpha | Range or scenario envelope. |
| `ghost` | Solid line, neutral grey | "Before" state in a comparison. |

### Why never pass hex colors

If you pass `color='#3b82f6'`, the chart breaks the moment a user switches theme
variants (dark ↔ light) or the brand palette shifts. The role-based system insulates
charts from the color palette. **There is no escape hatch for colors at layers 1–3.**
If you need a literal color that is not in the role table, that is layer 4.

---

## 3. Composing templates (layer 2)

The three composition functions:

```python
import altair as alt

# Overlay two charts on the same axes (e.g. line over scatter)
chart = alt.layer(scatter_trend(df, "x", "y"),
                  multi_line(df, "x", "y", series_role={"trend": "reference"}))

# Side-by-side
chart = alt.hconcat(bar(df, "category", "value"),
                    histogram(df, "value"))

# Stacked vertically
chart = alt.vconcat(actual_vs_forecast(df, "date", "actual", "forecast"),
                    bar(df, "date", "residual"))
```

### Composition rules

- **`alt.layer`** requires the layered charts to share the same data shape and the
  same x-axis. Mismatched encodings produce a confusing chart but no error.
- **`alt.hconcat` / `alt.vconcat`** accept any two charts. They each get their own
  axes and legend.
- The active theme is preserved across composition — you do not need to reapply it.
- Resolve scale / legend conflicts with `.resolve_scale(color='independent')` etc.

---

## 4. Themed raw Altair (layer 3)

When no template fits, write raw Altair but **stay inside the theme**. Two rules:

1. Do not pass any `color`, `stroke`, or `fill` literals. Use channel encodings
   driven by data fields, and let the theme resolve them.
2. Do not override `axis`, `legend`, or `view` config blocks. They are owned by
   the theme.

A correct layer-3 example:

```python
chart = (
    alt.Chart(df)
    .mark_circle(size=80, opacity=0.7)
    .encode(
        x=alt.X("x:Q", title="X"),
        y=alt.Y("y:Q", title="Y"),
        color=alt.Color("category:N"),  # theme picks the categorical palette
        tooltip=["x", "y", "category"],
    )
    .properties(title="Themed scatter")
)
```

A broken layer-3 example (drops to layer 4):

```python
.mark_circle(color="#1f77b4", size=80)  # ← hex color escapes the theme
.configure_axis(labelColor="#000")      # ← config override owns the theme
```

---

## 5. Grammar of graphics quick reference

Altair is a Python wrapper over Vega-Lite, which is a grammar-of-graphics dialect.
Every chart is `data` + `mark` + `encoding` + (optional) `transform`.

### Marks

| Mark | Use for |
|------|---------|
| `mark_bar` | Categorical comparison, histogram, stacked. |
| `mark_line` | Continuous trend over ordered axis. |
| `mark_area` | Cumulative, stacked area, range band. |
| `mark_point` / `mark_circle` | Scatter, dot plot. |
| `mark_rect` | Heatmap, calendar plot. |
| `mark_rule` | Reference lines (target, mean). |
| `mark_text` | Labels, annotations. |
| `mark_boxplot` | Box-whisker. |
| `mark_errorband` | Confidence interval band. |

### Encoding channels

| Channel | Type | Notes |
|---------|------|-------|
| `x`, `y` | `:Q`, `:O`, `:N`, `:T` | Quantitative, ordinal, nominal, temporal. Theme owns axis style. |
| `color` | `:N` or `:Q` | Theme owns palettes — categorical or sequential. Do not pass literals. |
| `size` | `:Q` | Bubble plots; keep range modest to avoid swamping. |
| `shape` | `:N` | Scatter with categorical groups when color is taken. |
| `opacity` | `:Q` | Density layers. |
| `tooltip` | `list[str]` | Always include — interactive charts must explain themselves. |
| `xOffset`, `yOffset` | `:N` | Side-by-side grouping. |
| `column`, `row`, `facet` | `:N` | Faceting. |

### Type suffixes

- `:Q` quantitative (continuous numeric).
- `:T` temporal (datetime).
- `:O` ordinal (ordered categories — small, medium, large).
- `:N` nominal (unordered categories).

Pick the right type — Altair's defaults are sometimes wrong (it will treat a numeric
ID column as `:Q` and apply a continuous scale; force `:N`).

---

## 6. Common pitfalls

### Mixing absolute and relative scales

When you compose a bar chart with a line chart at layer 2, the y-axis scales must
be reconciled. Either share the scale (default) or resolve independently:

```python
chart = alt.layer(bars, lines).resolve_scale(y='independent')
```

Two y-axes in one panel is usually a smell — consider `alt.vconcat` instead.

### Faceting blows up

Faceting on a column with thousands of unique values produces an unrenderable
chart. Pre-aggregate or filter to the top N before faceting.

### Tooltip misses fields

`tooltip=["x", "y"]` shows only those fields. To show all data fields:

```python
tooltip=alt.Tooltip(list(df.columns))
```

### Time axis misaligned

If your data is monthly but you encode as `:T`, Altair places ticks at the day level.
Specify the axis scale explicitly:

```python
x=alt.X("date:T", axis=alt.Axis(format="%Y-%m", tickCount="month"))
```

### Bar chart is sorted weirdly

Default sort is alphabetical. Force a sort:

```python
x=alt.X("category:N", sort=alt.EncodingSortField(field="value", order="descending"))
# or
x=alt.X("category:N", sort=["A", "B", "C"])  # explicit order
```

---

## 7. Theme escape hatches (use sparingly)

The theme module exposes a small surface for cases the templates do not cover:

```python
from app.skills.charting.altair_charts.pkg.theme import (
    get_role_color,    # role name → resolved hex for current variant
    get_role_stroke,   # role name → stroke dasharray spec
    list_roles,        # all valid role names
    use_variant,       # 'dark' | 'light'
    ensure_registered, # idempotent registration of project theme
)
```

Use these only at layer 3 when you must reference a role color from inside a
custom encoding. **Never** copy the resolved hex into a literal — call the function
each time so theme changes propagate.

---

## 8. Checklist before returning a chart

- [ ] Layer is as low as possible (template > composed > themed raw > raw).
- [ ] No hex colors in the chart spec.
- [ ] Axis types are correct (`:Q`, `:T`, `:O`, `:N`).
- [ ] Tooltip is non-empty.
- [ ] Sort is explicit if order matters.
- [ ] If composed: scales resolved correctly.
- [ ] Title is set (helps the chart stand alone in an artifact).
- [ ] If at layer 4: artifact metadata explains why.

---

## 9. References

- Wilkinson, L. (2005). *The Grammar of Graphics* (2nd ed). — the source.
- Satyanarayan et al. (2017). *Vega-Lite: A Grammar of Interactive Graphics.* IEEE
  TVCG. — the spec Altair compiles to.
- Cleveland, W. S. (1985). *The Elements of Graphing Data.* — perceptual basis for
  the role-based design.
