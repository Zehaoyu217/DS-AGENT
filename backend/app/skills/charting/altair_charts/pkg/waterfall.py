# backend/app/skills/altair_charts/pkg/waterfall.py
from __future__ import annotations

import altair as alt
import pandas as pd

from app.skills.charting.altair_charts.pkg._common import ensure_theme_registered


def waterfall(
    df: pd.DataFrame,
    step: str,
    delta: str,
    kind: str | None = None,
    title: str | None = None,
) -> alt.Chart:
    """Classic waterfall. `kind` values: 'total' (absolute bar) or 'delta' (stepped)."""
    ensure_theme_registered()
    required = [step, delta] + ([kind] if kind else [])
    missing = [f for f in required if f not in df.columns]
    if missing:
        raise KeyError(
            f"waterfall(): missing fields {missing}; df has columns {list(df.columns)}"
        )

    # Pre-compute cumulative range per row.
    kind_col = kind or "_kind"
    data = df.copy()
    if not kind:
        data[kind_col] = "delta"
    running = 0.0
    lo: list[float] = []
    hi: list[float] = []
    sign: list[str] = []
    for _, row in data.iterrows():
        if row[kind_col] == "total":
            lo.append(0.0)
            hi.append(float(row[delta]))
            running = float(row[delta])
            sign.append("total")
        else:
            d = float(row[delta])
            start = running
            running = running + d
            lo.append(start if d >= 0 else running)
            hi.append(running if d >= 0 else start)
            sign.append("positive" if d >= 0 else "negative")
    data["_lo"] = lo
    data["_hi"] = hi
    data["_sign"] = sign

    bars = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X(step, type="nominal", sort=None, title=step),
            y=alt.Y("_lo:Q", title=delta),
            y2=alt.Y2("_hi:Q"),
            color=alt.Color(
                "_sign:N",
                scale=alt.Scale(
                    domain=["positive", "negative", "total"],
                    range=["#5C7F67", "#8C3B3B", "#0B2545"],
                ),
                legend=alt.Legend(title=""),
            ),
        )
    )
    chart = alt.layer(bars)
    if title:
        chart = chart.properties(title=title)
    return chart
