# backend/app/skills/altair_charts/tests/test_ecdf.py
from __future__ import annotations

import numpy as np
import pandas as pd


def test_ecdf_uses_window_cumulative_count() -> None:
    from app.skills.charting.altair_charts.pkg.ecdf import ecdf

    rng = np.random.default_rng(0)
    df = pd.DataFrame({"x": rng.normal(size=100)})
    chart = ecdf(df, value="x")
    spec = chart.to_dict()
    transforms = spec.get("transform", [])
    assert any("window" in t for t in transforms)
