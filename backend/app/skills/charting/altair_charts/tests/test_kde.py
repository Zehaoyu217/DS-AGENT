# backend/app/skills/altair_charts/tests/test_kde.py
from __future__ import annotations

import numpy as np
import pandas as pd


def test_kde_uses_density_transform() -> None:
    from app.skills.charting.altair_charts.pkg.kde import kde

    rng = np.random.default_rng(0)
    df = pd.DataFrame({"x": rng.normal(size=200)})
    chart = kde(df, value="x")
    spec = chart.to_dict()
    transforms = spec.get("transform", [])
    assert any("density" in t for t in transforms)


def test_kde_with_group_facets_density_per_group() -> None:
    from app.skills.charting.altair_charts.pkg.kde import kde

    rng = np.random.default_rng(0)
    df = pd.DataFrame(
        {
            "x": np.concatenate([rng.normal(size=80), rng.normal(loc=2, size=80)]),
            "g": ["A"] * 80 + ["B"] * 80,
        }
    )
    chart = kde(df, value="x", group="g")
    spec = chart.to_dict()
    transforms = spec.get("transform", [])
    density = next((t for t in transforms if "density" in t), {})
    assert density.get("groupby") == ["g"]
