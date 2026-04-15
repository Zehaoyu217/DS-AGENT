# backend/app/skills/altair_charts/pkg/small_multiples.py
from __future__ import annotations

import altair as alt
import pandas as pd

from app.skills.charting.altair_charts.pkg._common import (
    ensure_theme_registered,
    resolve_series_style,
)


def small_multiples(
    df: pd.DataFrame,
    x: str,
    y: str,
    facet: str,
    columns: int = 3,
    title: str | None = None,
) -> alt.Chart:
    ensure_theme_registered()
    missing = [f for f in (x, y, facet) if f not in df.columns]
    if missing:
        raise KeyError(
            f"small_multiples(): missing fields {missing}; df has columns {list(df.columns)}"
        )
    x_type = "temporal" if pd.api.types.is_datetime64_any_dtype(df[x]) else "quantitative"
    style = resolve_series_style("primary")
    base = (
        alt.Chart(df)
        .mark_line(color=style["color"], strokeWidth=style["strokeWidth"])
        .encode(
            x=alt.X(x, type=x_type, title=x),
            y=alt.Y(y, type="quantitative", title=y),
        )
        .properties(width=180, height=120)
    )
    chart = base.facet(
        facet=alt.Facet(facet, type="nominal", title=facet),
        columns=columns,
    )
    if title:
        chart = chart.properties(title=title)
    return chart
