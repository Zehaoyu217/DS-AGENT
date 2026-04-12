from __future__ import annotations

from pathlib import Path
from typing import Any

import altair as alt

from config.themes.theme_switcher import ThemeTokens, VariantTokens

_DEFAULT_TOKENS: ThemeTokens | None = None


def _build_spec(tokens: VariantTokens, typography: dict[str, Any]) -> dict[str, Any]:
    sans = typography["sans"]
    font = sans
    override = tokens.typography_override()
    title_font = typography.get("serif", sans) if override.get("headings") == "serif" else sans
    base_size = override.get("base_size", typography["scale"]["base"])

    return {
        "background": tokens.surface("base"),
        "config": {
            "background": tokens.surface("base"),
            "font": font,
            "title": {
                "anchor": tokens.chart("title_anchor"),
                "color": tokens.surface("text"),
                "font": title_font,
                "fontSize": typography["scale"]["xl"],
                "fontWeight": typography["weight"]["semibold"],
                "subtitleColor": tokens.surface("text_muted"),
                "subtitleFont": font,
            },
            "view": {
                "continuousWidth": tokens.chart("default_width"),
                "continuousHeight": tokens.chart("default_height"),
                "stroke": tokens.surface("border"),
            },
            "axis": {
                "domainColor": tokens.surface("border"),
                "gridColor": tokens.surface("grid"),
                "labelColor": tokens.surface("text_muted"),
                "labelFont": font,
                "labelFontSize": typography["scale"]["sm"],
                "tickColor": tokens.surface("border"),
                "titleColor": tokens.surface("text"),
                "titleFont": font,
                "titleFontSize": typography["scale"]["base"],
                "titleFontWeight": typography["weight"]["medium"],
            },
            "legend": {
                "labelColor": tokens.surface("text"),
                "labelFont": font,
                "labelFontSize": typography["scale"]["sm"],
                "titleColor": tokens.surface("text"),
                "titleFont": font,
                "titleFontSize": typography["scale"]["sm"],
                "titleFontWeight": typography["weight"]["medium"],
            },
            "range": {
                "category": tokens.categorical(),
                "diverging": [
                    tokens.diverging()["negative"],
                    tokens.diverging()["neutral"],
                    tokens.diverging()["positive"],
                ],
                "ramp": [tokens.series_color("ghost"), tokens.series_color("actual")],
                "ordinal": [
                    tokens.series_color(role)
                    for role in (
                        "ghost", "scenario", "forecast", "projection",
                        "reference", "secondary", "primary", "actual",
                    )
                ],
            },
            "mark": {"font": font, "fontSize": base_size},
            "text": {"font": font, "fontSize": typography["scale"]["sm"], "color": tokens.surface("text")},
            "header": {"labelFont": font, "titleFont": font},
        },
    }


def register_all(tokens_path: Path | None = None) -> None:
    """Load tokens.yaml and register one Altair theme per variant as `gir_<variant>`.

    Repeated calls re-register each `gir_<variant>` theme, overwriting any
    previous registration with the same name.
    """
    global _DEFAULT_TOKENS
    path = tokens_path or (Path(__file__).parent / "tokens.yaml")
    _DEFAULT_TOKENS = ThemeTokens.load(path)
    typography = _DEFAULT_TOKENS.typography
    for variant_name in _DEFAULT_TOKENS.variants:
        variant = _DEFAULT_TOKENS.for_variant(variant_name)
        spec = _build_spec(variant, typography)
        alt.themes.register(f"gir_{variant_name}", lambda s=spec: s)
    alt.themes.enable(f"gir_{_DEFAULT_TOKENS.default_variant}")


def use_variant(variant: str) -> None:
    if _DEFAULT_TOKENS is None:
        register_all()
    alt.themes.enable(f"gir_{variant}")


def active_tokens() -> VariantTokens:
    if _DEFAULT_TOKENS is None:
        register_all()
    assert _DEFAULT_TOKENS is not None
    active = alt.themes.active or f"gir_{_DEFAULT_TOKENS.default_variant}"
    if not active.startswith("gir_"):
        return _DEFAULT_TOKENS.for_variant(_DEFAULT_TOKENS.default_variant)
    variant_name = active.removeprefix("gir_")
    return _DEFAULT_TOKENS.for_variant(variant_name)
