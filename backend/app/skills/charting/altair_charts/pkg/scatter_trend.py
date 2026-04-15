# backend/app/skills/altair_charts/pkg/scatter_trend.py
from __future__ import annotations

import altair as alt
import pandas as pd

from app.skills.charting.altair_charts.pkg._common import (
    ensure_theme_registered,
    resolve_series_style,
)


def scatter_trend(
    df: pd.DataFrame,
    x: str,
    y: str,
    trend: str = "linear",
    title: str | None = None,
) -> alt.Chart:
    ensure_theme_registered()
    for f in (x, y):
        if f not in df.columns:
            raise KeyError(f"scatter_trend(): missing field '{f}'")
        if not pd.api.types.is_numeric_dtype(df[f]):
            raise ValueError(f"scatter_trend(): '{f}' must be numeric")

    primary = resolve_series_style("primary")
    reference = resolve_series_style("reference")

    points = (
        alt.Chart(df)
        .mark_circle(color=primary["color"], size=45, opacity=0.75)
        .encode(
            x=alt.X(x, type="quantitative"),
            y=alt.Y(y, type="quantitative"),
        )
    )
    line_kwargs: dict[str, object] = {
        "color": reference["color"],
        "strokeWidth": reference["strokeWidth"],
    }
    if "strokeDash" in reference:
        line_kwargs["strokeDash"] = reference["strokeDash"]
    line = (
        alt.Chart(df)
        .transform_regression(x, y, method=trend)
        .mark_line(**line_kwargs)
        .encode(
            x=alt.X(x, type="quantitative"),
            y=alt.Y(y, type="quantitative"),
        )
    )
    chart = alt.layer(points, line)
    if title:
        chart = chart.properties(title=title)
    return chart
