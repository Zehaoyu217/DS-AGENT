# backend/app/skills/altair_charts/pkg/correlation_heatmap.py
from __future__ import annotations

import altair as alt
import pandas as pd

from app.skills.charting.altair_charts.pkg._common import (
    diverging_scheme_values,
    ensure_theme_registered,
)


def correlation_heatmap(
    df: pd.DataFrame,
    fields: list[str] | None = None,
    title: str | None = None,
) -> alt.Chart:
    ensure_theme_registered()
    numeric_df = df.select_dtypes(include="number")
    if fields is not None:
        numeric_df = numeric_df[[f for f in fields if f in numeric_df.columns]]
    corr = numeric_df.corr(numeric_only=True).round(3)

    # Melt to long form.
    long = (
        corr.reset_index()
        .melt(id_vars="index", var_name="var_y", value_name="corr")
        .rename(columns={"index": "var_x"})
    )

    diverging = diverging_scheme_values()
    chart = (
        alt.Chart(long)
        .mark_rect()
        .encode(
            x=alt.X("var_x:N", title=None),
            y=alt.Y("var_y:N", title=None),
            color=alt.Color(
                "corr:Q",
                scale=alt.Scale(domain=[-1, 0, 1], range=diverging),
                title="corr",
            ),
            tooltip=[
                alt.Tooltip("var_x:N"),
                alt.Tooltip("var_y:N"),
                alt.Tooltip("corr:Q", format=".2f"),
            ],
        )
    )
    if title:
        chart = chart.properties(title=title)
    return chart
