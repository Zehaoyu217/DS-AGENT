# backend/app/skills/altair_charts/pkg/bar.py
from __future__ import annotations

import altair as alt
import pandas as pd

from app.skills.charting.altair_charts.pkg._common import ensure_theme_registered


def bar(
    df: pd.DataFrame,
    x: str,
    y: str,
    category: str | None = None,
    title: str | None = None,
) -> alt.Chart:
    ensure_theme_registered()
    missing = [f for f in (x, y) + ((category,) if category else ()) if f not in df.columns]
    if missing:
        raise KeyError(
            f"bar(): missing fields {missing}; df has columns {list(df.columns)}"
        )

    x_type = "nominal" if not pd.api.types.is_numeric_dtype(df[x]) else "quantitative"
    encoding: dict = {
        "x": alt.X(x, type=x_type, title=x),
        "y": alt.Y(y, type="quantitative", title=y),
    }
    if category:
        encoding["color"] = alt.Color(category, type="nominal", title=category)
        encoding["xOffset"] = alt.XOffset(category, type="nominal")
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(**encoding)
    )
    if title:
        chart = chart.properties(title=title)
    return chart
