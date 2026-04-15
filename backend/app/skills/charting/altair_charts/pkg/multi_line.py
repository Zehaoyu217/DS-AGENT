# backend/app/skills/altair_charts/pkg/multi_line.py
from __future__ import annotations

import altair as alt
import pandas as pd

from app.skills.charting.altair_charts.pkg._common import (
    ensure_theme_registered,
    resolve_series_style,
)


def multi_line(
    df: pd.DataFrame,
    x: str,
    y: str,
    series_role: str,
    title: str | None = None,
) -> alt.Chart:
    ensure_theme_registered()
    for f in (x, y, series_role):
        if f not in df.columns:
            raise KeyError(f"multi_line(): missing field '{f}'; df has {list(df.columns)}")

    roles = list(df[series_role].dropna().unique())
    x_type = "temporal" if pd.api.types.is_datetime64_any_dtype(df[x]) else "quantitative"

    layers: list[alt.Chart] = []
    for role in roles:
        style = resolve_series_style(str(role))
        mark_kwargs = {"strokeWidth": style["strokeWidth"], "color": style["color"]}
        if "strokeDash" in style:
            mark_kwargs["strokeDash"] = style["strokeDash"]
        sub = (
            alt.Chart(df[df[series_role] == role])
            .mark_line(**mark_kwargs)
            .encode(
                x=alt.X(x, type=x_type, title=x),
                y=alt.Y(y, type="quantitative", title=y),
            )
        )
        layers.append(sub)
    chart = alt.layer(*layers) if len(layers) > 1 else layers[0]
    if title:
        chart = chart.properties(title=title)
    return chart
