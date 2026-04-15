# backend/app/skills/altair_charts/tests/test_correlation_heatmap.py
from __future__ import annotations

import pandas as pd


def test_correlation_heatmap_returns_square_matrix() -> None:
    from app.skills.altair_charts.pkg.correlation_heatmap import correlation_heatmap

    df = pd.DataFrame({"a": range(20), "b": range(20, 40), "c": list(range(0, 40, 2))})
    chart = correlation_heatmap(df)
    spec = chart.to_dict()
    assert spec["mark"]["type"] == "rect"
    # data embedded should have n*n rows (3×3 = 9)
    values = spec.get("data", {}).get("values") or spec.get("datasets", {}).get(
        next(iter(spec.get("datasets", {})), ""), []
    )
    assert len(values) == 9


def test_correlation_heatmap_ignores_non_numeric_fields() -> None:
    from app.skills.altair_charts.pkg.correlation_heatmap import correlation_heatmap

    df = pd.DataFrame({"a": range(5), "b": range(5), "cat": list("abcde")})
    chart = correlation_heatmap(df)
    spec = chart.to_dict()
    values = spec.get("data", {}).get("values") or []
    if not values:
        datasets = spec.get("datasets", {})
        values = datasets[next(iter(datasets))]
    fields = {v["var_x"] for v in values}
    assert "cat" not in fields
