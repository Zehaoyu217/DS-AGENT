# backend/app/skills/altair_charts/tests/test_histogram.py
from __future__ import annotations

import pandas as pd


def test_histogram_uses_bar_mark_with_bin() -> None:
    from app.skills.altair_charts.pkg.histogram import histogram

    df = pd.DataFrame({"revenue": list(range(100))})
    chart = histogram(df, field="revenue", bins=10)
    spec = chart.to_dict()
    enc = spec["encoding"]
    assert enc["x"]["bin"] in (True, {"maxbins": 10})


def test_histogram_raises_on_non_numeric_field() -> None:
    import pytest

    from app.skills.altair_charts.pkg.histogram import histogram

    df = pd.DataFrame({"cat": ["a", "b"]})
    with pytest.raises(ValueError, match="numeric"):
        histogram(df, field="cat")
