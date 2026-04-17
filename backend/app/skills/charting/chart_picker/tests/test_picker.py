from __future__ import annotations

import pytest

from app.skills.charting.chart_picker.pkg.picker import pick_chart


def shape(**kw):
    base = {"rows": 10, "x_type": "nominal", "y_type": "quantitative", "n_series": 1}
    base.update(kw)
    return base


def test_compare_single_few_categories_picks_bar():
    s = pick_chart("compare", shape(n_categories=6))
    assert s.template == "bar"
    assert s.confidence > 0.9


def test_compare_single_many_categories_picks_lollipop():
    s = pick_chart("compare", shape(n_categories=20))
    assert s.template == "lollipop"
    assert "bar" in s.alternates


def test_compare_with_target_picks_bar_with_reference():
    s = pick_chart("compare", shape(has_target=True))
    assert s.template == "bar_with_reference"


def test_compare_multi_series_picks_grouped_bar():
    s = pick_chart("compare", shape(n_series=3, n_categories=6))
    assert s.template == "grouped_bar"


def test_trend_single_series_picks_multi_line():
    s = pick_chart("trend", shape(x_type="temporal", n_series=1))
    assert s.template == "multi_line"


def test_trend_many_series_picks_small_multiples():
    s = pick_chart("trend", shape(x_type="temporal", n_series=12))
    assert s.template == "small_multiples"


def test_trend_cumulative_picks_area_cumulative():
    s = pick_chart("trend", shape(x_type="temporal", cumulative=True))
    assert s.template == "area_cumulative"


def test_trend_range_band_picks_range_band():
    s = pick_chart("trend", shape(x_type="temporal", range_band=True))
    assert s.template == "range_band"


def test_distribution_single_picks_histogram():
    s = pick_chart("distribution", shape(x_type="quantitative", y_type="quantitative"))
    assert s.template == "histogram"


def test_distribution_grouped_small_picks_boxplot():
    s = pick_chart(
        "distribution", shape(rows=80, n_series=4, grouped=True)
    )
    assert s.template == "boxplot"


def test_distribution_grouped_large_picks_violin():
    s = pick_chart(
        "distribution", shape(rows=400, n_series=4, grouped=True)
    )
    assert s.template == "violin"


def test_relationship_two_columns_picks_scatter_trend():
    s = pick_chart("relationship", shape(n_numeric_cols=2))
    assert s.template == "scatter_trend"


def test_relationship_many_columns_picks_heatmap():
    s = pick_chart("relationship", shape(n_numeric_cols=8))
    assert s.template == "correlation_heatmap"


def test_change_two_periods_picks_slope():
    s = pick_chart("change", shape(has_periods=True))
    assert s.template == "slope"


def test_forecast_picks_actual_vs_forecast():
    s = pick_chart("forecast", shape(x_type="temporal", n_series=2))
    assert s.template == "actual_vs_forecast"


def test_composition_temporal_picks_stacked_bar():
    s = pick_chart("composition", shape(x_type="temporal"))
    assert s.template == "stacked_bar"


def test_synonym_resolves():
    a = pick_chart("rank", shape(n_categories=5))
    b = pick_chart("compare", shape(n_categories=5))
    assert a.template == b.template


def test_other_intent_returns_none_with_alternates():
    s = pick_chart("other", shape())
    assert s.template is None
    assert len(s.alternates) > 0
    assert s.fallback_layer >= 2


def test_unknown_intent_raises():
    with pytest.raises(ValueError):
        pick_chart("teleport", shape())


def test_missing_required_keys_raises():
    with pytest.raises(ValueError):
        pick_chart("compare", {"rows": 10})


def test_suggestion_is_pure():
    a = pick_chart("compare", shape(n_categories=6))
    b = pick_chart("compare", shape(n_categories=6))
    assert a == b
