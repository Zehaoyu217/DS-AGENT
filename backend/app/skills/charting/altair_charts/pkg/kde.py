# backend/app/skills/altair_charts/pkg/kde.py
from __future__ import annotations

import altair as alt
import pandas as pd

from app.skills.charting.altair_charts.pkg._common import (
    ensure_theme_registered,
    resolve_series_style,
)


def kde(
    df: pd.DataFrame,
    value: str,
    group: str | None = None,
    title: str | None = None,
) -> alt.Chart:
    ensure_theme_registered()
    required = [value] + ([group] if group else [])
    missing = [f for f in required if f not in df.columns]
    if missing:
        raise KeyError(
            f"kde(): missing fields {missing}; df has columns {list(df.columns)}"
        )
    primary = resolve_series_style("primary")
    density_kwargs: dict = {"density": value, "as_": [value, "density"]}
    if group:
        density_kwargs["groupby"] = [group]
    enc: dict = {
        "x": alt.X(f"{value}:Q", title=value),
        "y": alt.Y("density:Q", title="density"),
    }
    mark_kwargs: dict = {"strokeWidth": primary["strokeWidth"], "opacity": 0.85}
    if group:
        enc["color"] = alt.Color(group, type="nominal", title=group)
    else:
        mark_kwargs["color"] = primary["color"]
    chart = (
        alt.Chart(df)
        .transform_density(**density_kwargs)
        .mark_area(**mark_kwargs)
        .encode(**enc)
    )
    if title:
        chart = chart.properties(title=title)
    return chart
