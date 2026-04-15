# backend/app/skills/altair_charts/pkg/histogram.py
from __future__ import annotations

import altair as alt
import pandas as pd

from app.skills.charting.altair_charts.pkg._common import ensure_theme_registered


def histogram(
    df: pd.DataFrame,
    field: str,
    bins: int = 30,
    title: str | None = None,
) -> alt.Chart:
    ensure_theme_registered()
    if field not in df.columns:
        raise KeyError(f"histogram(): missing field '{field}'")
    if not pd.api.types.is_numeric_dtype(df[field]):
        raise ValueError(f"histogram(): field '{field}' must be numeric")

    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X(field, bin=alt.Bin(maxbins=bins), title=field),
            y=alt.Y("count()", title="count"),
        )
    )
    if title:
        chart = chart.properties(title=title)
    return chart
