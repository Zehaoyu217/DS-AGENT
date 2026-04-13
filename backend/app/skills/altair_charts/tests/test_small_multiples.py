# backend/app/skills/altair_charts/tests/test_small_multiples.py
from __future__ import annotations

import pandas as pd


def test_small_multiples_facets_by_column() -> None:
    from app.skills.altair_charts.pkg.small_multiples import small_multiples

    df = pd.DataFrame(
        {
            "date": list(pd.date_range("2024-01-01", periods=4, freq="D")) * 3,
            "region": ["N"] * 4 + ["S"] * 4 + ["E"] * 4,
            "value": [1.0, 2, 3, 4] + [0.5, 1, 2, 3] + [2.0, 3, 4, 5],
        }
    )
    chart = small_multiples(df, x="date", y="value", facet="region", columns=3)
    spec = chart.to_dict()
    # Altair faceted chart exposes 'facet' key.
    assert "facet" in spec or "columns" in spec


def test_small_multiples_raises_on_missing_field() -> None:
    from app.skills.altair_charts.pkg.small_multiples import small_multiples

    df = pd.DataFrame({"date": [1], "value": [1]})
    try:
        small_multiples(df, x="date", y="value", facet="region")
    except KeyError as exc:
        assert "region" in str(exc)
    else:
        raise AssertionError("expected KeyError")
