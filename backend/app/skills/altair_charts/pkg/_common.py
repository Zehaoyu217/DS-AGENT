# backend/app/skills/altair_charts/pkg/_common.py
from __future__ import annotations

from typing import Any

import altair as alt

from config.themes.altair_theme import active_tokens, register_all


def ensure_theme_registered() -> None:
    """Call once at chart build time to guarantee themes exist."""
    try:
        if "gir_light" not in alt.themes.names():
            register_all()
    except Exception:  # noqa: BLE001
        register_all()


def resolve_series_style(role: str) -> dict[str, Any]:
    """Return a dict of Altair mark kwargs for a named series role."""
    tokens = active_tokens()
    color = tokens.series_color(role)
    stroke = tokens.series_stroke(role)
    props: dict[str, Any] = {"color": color, "strokeWidth": stroke.width}
    if stroke.dash is not None:
        props["strokeDash"] = stroke.dash
    return props


def diverging_scheme_values() -> list[str]:
    tokens = active_tokens()
    div = tokens.diverging()
    return [div["negative"], div["neutral"], div["positive"]]
