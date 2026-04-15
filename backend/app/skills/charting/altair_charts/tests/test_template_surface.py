# backend/app/skills/altair_charts/tests/test_template_surface.py
from __future__ import annotations


def test_all_twenty_templates_exported() -> None:
    from app.skills.charting.altair_charts import pkg

    expected = {
        # Plan 1 (6)
        "bar", "multi_line", "histogram", "scatter_trend", "boxplot", "correlation_heatmap",
        # Plan 4 (14)
        "grouped_bar", "stacked_bar", "bar_with_reference", "lollipop", "dumbbell",
        "actual_vs_forecast", "area_cumulative", "range_band", "small_multiples",
        "kde", "violin", "ecdf", "slope", "waterfall",
    }
    exported = set(getattr(pkg, "__all__", []))
    missing = expected - exported
    assert not missing, f"missing templates from __all__: {missing}"
    for name in expected:
        assert callable(getattr(pkg, name)), f"{name} is not callable"
