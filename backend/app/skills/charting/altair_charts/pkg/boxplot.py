# backend/app/skills/altair_charts/pkg/boxplot.py
from __future__ import annotations

import altair as alt
import pandas as pd

from app.skills.charting.altair_charts.pkg._common import (
    ensure_theme_registered,
    resolve_series_style,
)


def boxplot(
    df: pd.DataFrame,
    field: str,
    group: str | None = None,
    title: str | None = None,
) -> alt.Chart:
    ensure_theme_registered()
    if field not in df.columns:
        raise KeyError(f"boxplot(): missing field '{field}'")
    if not pd.api.types.is_numeric_dtype(df[field]):
        raise ValueError(f"boxplot(): '{field}' must be numeric")
    if group and group not in df.columns:
        raise KeyError(f"boxplot(): missing group '{group}'")

    primary = resolve_series_style("primary")
    encoding: dict = {"y": alt.Y(field, type="quantitative", title=field)}
    if group:
        encoding["x"] = alt.X(group, type="nominal", title=group)
    chart = (
        alt.Chart(df)
        .mark_boxplot(color=primary["color"], size=40)
        .encode(**encoding)
    )
    if title:
        chart = chart.properties(title=title)
    return chart
