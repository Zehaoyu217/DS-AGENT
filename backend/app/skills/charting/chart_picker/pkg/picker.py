"""Decision tree for picking a chart template from intent + data shape.

Pure: no I/O, no DataFrame inspection. The caller summarizes shape into a dict.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, TypedDict

Intent = Literal[
    "compare",
    "trend",
    "distribution",
    "relationship",
    "composition",
    "change",
    "forecast",
    "other",
]

INTENT_SYNONYMS: dict[str, Intent] = {
    "compare": "compare",
    "rank": "compare",
    "compare across categories": "compare",
    "trend": "trend",
    "over time": "trend",
    "time series": "trend",
    "evolution": "trend",
    "distribution": "distribution",
    "spread": "distribution",
    "histogram": "distribution",
    "relationship": "relationship",
    "correlate": "relationship",
    "regress": "relationship",
    "scatter": "relationship",
    "composition": "composition",
    "breakdown": "composition",
    "parts of whole": "composition",
    "stacked": "composition",
    "change": "change",
    "before vs after": "change",
    "delta": "change",
    "change between two points": "change",
    "forecast": "forecast",
    "actual vs forecast": "forecast",
    "projection": "forecast",
    "plan vs actual": "forecast",
    "other": "other",
}

REQUIRED_SHAPE_KEYS = {"rows", "x_type", "y_type", "n_series"}


class DataShape(TypedDict, total=False):
    rows: int
    x_type: Literal["quantitative", "nominal", "ordinal", "temporal"]
    y_type: Literal["quantitative", "nominal", "ordinal", "temporal"]
    n_series: int
    n_categories: int
    has_periods: bool
    has_target: bool
    cumulative: bool
    range_band: bool
    facet: bool
    grouped: bool
    n_numeric_cols: int


@dataclass(frozen=True, slots=True)
class ChartSuggestion:
    template: str | None
    alternates: tuple[str, ...] = ()
    reason: str = ""
    confidence: float = 0.0
    fallback_layer: int = 1


def _normalize_intent(raw: str) -> Intent:
    key = raw.strip().lower()
    if key in INTENT_SYNONYMS:
        return INTENT_SYNONYMS[key]
    raise ValueError(
        f"Unknown intent: {raw!r}. Use one of: "
        "compare, trend, distribution, relationship, composition, change, "
        "forecast, other."
    )


def _validate_shape(shape: dict) -> None:
    missing = REQUIRED_SHAPE_KEYS - set(shape.keys())
    if missing:
        raise ValueError(
            f"Bad data_shape: missing keys {sorted(missing)}. "
            "Required: rows, x_type, y_type, n_series."
        )


def _pick_compare(shape: dict) -> ChartSuggestion:
    if shape.get("has_target"):
        return ChartSuggestion(
            template="bar_with_reference",
            alternates=("bar",),
            reason="Comparison with a target/baseline value.",
            confidence=0.96,
        )
    n_series = int(shape.get("n_series", 1))
    n_categories = int(shape.get("n_categories", shape.get("rows", 0)))
    if n_series >= 2:
        if shape.get("grouped") or n_series <= 4:
            return ChartSuggestion(
                template="grouped_bar",
                alternates=("stacked_bar", "small_multiples"),
                reason=(
                    f"{n_series} series across {n_categories} categories — "
                    "grouped bar keeps each category comparable."
                ),
                confidence=0.9,
            )
        return ChartSuggestion(
            template="stacked_bar",
            alternates=("grouped_bar", "small_multiples"),
            reason="Many series — stacked is more legible than grouped at this width.",
            confidence=0.78,
        )
    if n_categories <= 8:
        return ChartSuggestion(
            template="bar",
            reason=f"Single series, {n_categories} categories — classic bar.",
            confidence=0.97,
        )
    if n_categories <= 30:
        return ChartSuggestion(
            template="lollipop",
            alternates=("bar",),
            reason=(
                f"{n_categories} categories — lollipop sorts cleanly with long names."
            ),
            confidence=0.88,
        )
    return ChartSuggestion(
        template="bar",
        alternates=("lollipop",),
        reason=(
            f"{n_categories} categories — apply top-N filter; bar is still the "
            "right shape after filtering."
        ),
        confidence=0.62,
    )


def _pick_trend(shape: dict) -> ChartSuggestion:
    if shape.get("range_band"):
        return ChartSuggestion(
            template="range_band",
            alternates=("multi_line",),
            reason="Low/high band overlaid on time axis.",
            confidence=0.92,
        )
    if shape.get("cumulative"):
        return ChartSuggestion(
            template="area_cumulative",
            alternates=("multi_line",),
            reason="Running cumulative — area is the standard.",
            confidence=0.92,
        )
    n_series = int(shape.get("n_series", 1))
    if shape.get("facet") or n_series > 8:
        return ChartSuggestion(
            template="small_multiples",
            alternates=("multi_line",),
            reason=(
                f"{n_series} series — too many for one panel; facet into a small-"
                "multiples grid."
            ),
            confidence=0.9,
        )
    return ChartSuggestion(
        template="multi_line",
        alternates=("small_multiples", "actual_vs_forecast"),
        reason=f"{n_series} series over time — multi_line with series_role mapping.",
        confidence=0.93,
    )


def _pick_distribution(shape: dict) -> ChartSuggestion:
    n_series = int(shape.get("n_series", 1))
    if n_series == 1:
        if shape.get("range_band") or shape.get("cumulative"):
            return ChartSuggestion(
                template="ecdf",
                alternates=("histogram",),
                reason="ECDF surfaces tails without binning artifacts.",
                confidence=0.85,
            )
        return ChartSuggestion(
            template="histogram",
            alternates=("kde",),
            reason="Single-series distribution — histogram is the default.",
            confidence=0.95,
        )
    if shape.get("grouped"):
        rows_per_group = int(shape.get("rows", 0)) / max(1, n_series)
        if rows_per_group >= 60:
            return ChartSuggestion(
                template="violin",
                alternates=("boxplot", "ecdf"),
                reason=(
                    f"{n_series} groups with ~{int(rows_per_group)} rows each — "
                    "violin shows shape that boxplot hides."
                ),
                confidence=0.85,
            )
        return ChartSuggestion(
            template="boxplot",
            alternates=("violin", "ecdf"),
            reason=f"{n_series} groups — boxplot summarizes each cleanly.",
            confidence=0.9,
        )
    return ChartSuggestion(
        template="ecdf",
        alternates=("kde", "boxplot"),
        reason="Comparing full distributions across series — ECDF beats boxes.",
        confidence=0.8,
    )


def _pick_relationship(shape: dict) -> ChartSuggestion:
    n_numeric = int(shape.get("n_numeric_cols", 2))
    if n_numeric >= 3:
        return ChartSuggestion(
            template="correlation_heatmap",
            alternates=("scatter_trend",),
            reason=(
                f"{n_numeric} numeric columns — heatmap surfaces all pairwise "
                "relationships at once."
            ),
            confidence=0.94,
        )
    return ChartSuggestion(
        template="scatter_trend",
        alternates=("correlation_heatmap",),
        reason="Two numeric columns — scatter with trend line.",
        confidence=0.96,
    )


def _pick_composition(shape: dict) -> ChartSuggestion:
    if str(shape.get("x_type", "")) == "temporal":
        return ChartSuggestion(
            template="stacked_bar",
            alternates=("area_cumulative",),
            reason="Composition over time — stacked bar with mode='percent' for share.",
            confidence=0.9,
        )
    return ChartSuggestion(
        template="stacked_bar",
        reason="Composition at one snapshot — stacked bar with mode='absolute'.",
        confidence=0.88,
    )


def _pick_change(shape: dict) -> ChartSuggestion:
    if shape.get("has_periods") and int(shape.get("n_series", 1)) == 1:
        return ChartSuggestion(
            template="slope",
            alternates=("dumbbell",),
            reason="Two-period change per category — slope shows direction.",
            confidence=0.93,
        )
    if shape.get("range_band") or "low" in str(shape).lower():
        return ChartSuggestion(
            template="dumbbell",
            alternates=("slope",),
            reason="Two endpoints per category — dumbbell shows distance and direction.",
            confidence=0.9,
        )
    return ChartSuggestion(
        template="waterfall",
        alternates=("bar",),
        reason="Sequential deltas summing to a total — waterfall.",
        confidence=0.88,
    )


def _pick_forecast(_: dict) -> ChartSuggestion:
    return ChartSuggestion(
        template="actual_vs_forecast",
        alternates=("multi_line", "range_band"),
        reason="Actuals + forecast (with optional band) — flagship template.",
        confidence=0.97,
    )


_DISPATCH = {
    "compare": _pick_compare,
    "trend": _pick_trend,
    "distribution": _pick_distribution,
    "relationship": _pick_relationship,
    "composition": _pick_composition,
    "change": _pick_change,
    "forecast": _pick_forecast,
}


def pick_chart(intent: str, data_shape: dict | None = None) -> ChartSuggestion:
    """Map analyst intent + data shape to a chart template.

    Returns a `ChartSuggestion` with `.template`, `.alternates`, `.reason`,
    `.confidence`, and `.fallback_layer`. `.template` is None when no template
    in the catalog fits — at which point `.fallback_layer >= 2` indicates that
    composition or themed-raw is the right next step.
    """
    shape: dict = dict(data_shape or {})
    _validate_shape(shape)
    norm = _normalize_intent(intent)
    if norm == "other":
        return ChartSuggestion(
            template=None,
            alternates=(
                "scatter_trend",
                "multi_line",
                "bar",
                "histogram",
            ),
            reason=(
                "Intent='other' — no single template fits. Compose from the "
                "alternates or write themed raw Altair."
            ),
            confidence=0.3,
            fallback_layer=2,
        )
    return _DISPATCH[norm](shape)
