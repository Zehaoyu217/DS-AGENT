# backend/app/skills/altair_charts/tests/test_boxplot.py
from __future__ import annotations

import pandas as pd


def test_boxplot_with_group_has_category_axis() -> None:
    from app.skills.charting.altair_charts.pkg.boxplot import boxplot

    df = pd.DataFrame(
        {"segment": ["A", "A", "B", "B", "A", "B"], "revenue": [1.0, 2.0, 5.0, 6.0, 1.5, 5.5]}
    )
    chart = boxplot(df, field="revenue", group="segment")
    spec = chart.to_dict()
    assert spec["mark"]["type"] == "boxplot"
    assert spec["encoding"]["x"]["field"] == "segment"


def test_boxplot_without_group_is_single_box() -> None:
    from app.skills.charting.altair_charts.pkg.boxplot import boxplot

    df = pd.DataFrame({"revenue": [1.0, 2.0, 5.0, 6.0, 1.5, 5.5]})
    chart = boxplot(df, field="revenue")
    spec = chart.to_dict()
    assert spec["mark"]["type"] == "boxplot"
