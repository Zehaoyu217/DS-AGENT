# backend/app/skills/altair_charts/pkg/actual_vs_forecast.py
from __future__ import annotations

import altair as alt
import pandas as pd

from app.skills.altair_charts.pkg._common import (
    ensure_theme_registered,
    resolve_series_style,
)


def actual_vs_forecast(
    df: pd.DataFrame,
    x: str,
    actual: str,
    forecast: str,
    forecast_low: str | None = None,
    forecast_high: str | None = None,
    reference_value: float | None = None,
    scenario: str | None = None,
    title: str | None = None,
) -> alt.Chart:
    ensure_theme_registered()
    required = [x, actual, forecast]
    optional = [c for c in (forecast_low, forecast_high, scenario) if c]
    missing = [f for f in required + optional if f not in df.columns]
    if missing:
        raise KeyError(
            f"actual_vs_forecast(): missing fields {missing}; df has columns {list(df.columns)}"
        )

    x_type = "temporal" if pd.api.types.is_datetime64_any_dtype(df[x]) else "quantitative"
    layers: list[alt.Chart] = []

    # Forecast band (filled area) if both low/high present.
    if forecast_low and forecast_high:
        band_style = resolve_series_style("scenario")
        band = (
            alt.Chart(df)
            .mark_area(opacity=0.35, color=band_style["color"])
            .encode(
                x=alt.X(x, type=x_type, title=x),
                y=alt.Y(forecast_low, type="quantitative", title=actual),
                y2=alt.Y2(forecast_high),
            )
        )
        layers.append(band)

    # Reference rule.
    if reference_value is not None:
        ref_style = resolve_series_style("reference")
        rule = (
            alt.Chart(pd.DataFrame({"_ref": [reference_value]}))
            .mark_rule(
                color=ref_style["color"],
                strokeWidth=ref_style["strokeWidth"],
                strokeDash=ref_style.get("strokeDash", [2, 2]),
            )
            .encode(y="_ref:Q")
        )
        layers.append(rule)

    # Scenario line.
    if scenario:
        sc_style = resolve_series_style("scenario")
        sc_line = (
            alt.Chart(df)
            .mark_line(
                color=sc_style["color"],
                strokeWidth=sc_style["strokeWidth"],
                strokeDash=sc_style.get("strokeDash", [4, 3]),
            )
            .encode(
                x=alt.X(x, type=x_type),
                y=alt.Y(scenario, type="quantitative"),
            )
        )
        layers.append(sc_line)

    # Forecast line (dashed).
    fc_style = resolve_series_style("forecast")
    fc_line = (
        alt.Chart(df)
        .mark_line(
            color=fc_style["color"],
            strokeWidth=fc_style["strokeWidth"],
            strokeDash=fc_style.get("strokeDash", [5, 3]),
        )
        .encode(
            x=alt.X(x, type=x_type),
            y=alt.Y(forecast, type="quantitative", title=actual),
        )
    )
    layers.append(fc_line)

    # Actual line (solid, thickest, darkest).
    ac_style = resolve_series_style("actual")
    ac_line = (
        alt.Chart(df)
        .mark_line(color=ac_style["color"], strokeWidth=ac_style["strokeWidth"])
        .encode(
            x=alt.X(x, type=x_type),
            y=alt.Y(actual, type="quantitative"),
        )
    )
    layers.append(ac_line)

    chart = alt.layer(*layers)
    if title:
        chart = chart.properties(title=title)
    return chart
