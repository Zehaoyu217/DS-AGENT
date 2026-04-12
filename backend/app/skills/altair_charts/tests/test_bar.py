# backend/app/skills/altair_charts/tests/test_bar.py
from __future__ import annotations

import pandas as pd
import pytest


def test_bar_returns_chart_with_bar_mark() -> None:
    # Local import so the rest of the suite does not fail before all templates exist.
    from app.skills.altair_charts.pkg.bar import bar

    df = pd.DataFrame({"country": ["US", "UK"], "revenue": [100, 80]})
    chart = bar(df, x="country", y="revenue")
    spec = chart.to_dict()
    assert spec["mark"] in ("bar", {"type": "bar"}) or spec["mark"]["type"] == "bar"


def test_bar_with_category_adds_color_channel() -> None:
    from app.skills.altair_charts.pkg.bar import bar

    df = pd.DataFrame(
        {"country": ["US", "US", "UK", "UK"], "segment": ["A", "B", "A", "B"], "revenue": [10, 20, 15, 25]}
    )
    chart = bar(df, x="country", y="revenue", category="segment")
    spec = chart.to_dict()
    assert "color" in spec["encoding"]


def test_bar_raises_on_missing_field() -> None:
    from app.skills.altair_charts.pkg.bar import bar

    df = pd.DataFrame({"country": ["US"]})
    with pytest.raises(KeyError, match="y"):
        bar(df, x="country", y="revenue")
