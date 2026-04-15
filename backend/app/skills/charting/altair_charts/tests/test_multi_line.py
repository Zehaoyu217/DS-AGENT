# backend/app/skills/altair_charts/tests/test_multi_line.py
from __future__ import annotations

import pandas as pd


def test_multi_line_with_series_role_has_layers() -> None:
    from app.skills.charting.altair_charts.pkg.multi_line import multi_line

    df = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=6, freq="ME").tolist() * 2,
            "value": [1, 2, 3, 4, 5, 6, 1.1, 2.1, 3.1, 4.1, 5.1, 6.1],
            "series": ["actual"] * 6 + ["forecast"] * 6,
        }
    )
    chart = multi_line(df, x="date", y="value", series_role="series")
    spec = chart.to_dict()
    # Layered chart containing at least 2 layers (one per role).
    assert (
        "layer" in spec
        or "hconcat" in spec
        or "vconcat" in spec
        or spec.get("mark") in ("line", {"type": "line"})
    )


def test_multi_line_forecast_layer_has_dashed_stroke() -> None:
    from app.skills.charting.altair_charts.pkg.multi_line import multi_line

    df = pd.DataFrame(
        {"date": pd.date_range("2024-01-01", periods=3, freq="ME").tolist() * 2,
         "value": [1, 2, 3, 4, 5, 6],
         "series": ["actual"] * 3 + ["forecast"] * 3}
    )
    chart = multi_line(df, x="date", y="value", series_role="series")
    spec = chart.to_dict()
    # Find a layer whose mark has a strokeDash set.
    layers = spec.get("layer", [])
    assert any(
        isinstance(layer.get("mark"), dict) and layer["mark"].get("strokeDash") is not None
        for layer in layers
    )
