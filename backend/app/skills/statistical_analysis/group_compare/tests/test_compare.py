from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from app.artifacts.store import ArtifactStore
from app.skills.statistical_analysis.group_compare import compare


def _store(tmp_path) -> ArtifactStore:
    return ArtifactStore(
        db_path=tmp_path / "artifacts.db",
        disk_root=tmp_path / "disk",
    )


def test_compare_two_groups_auto_picks_reasonable(tmp_path, two_groups) -> None:
    r = compare(two_groups, value="value", group="group",
                store=_store(tmp_path), session_id="s1", bootstrap_n=200)
    assert r.effect_name == "cohens_d"
    assert r.method_used in {"student", "welch"}
    assert 0.4 <= r.effect_size <= 0.9
    assert r.effect_ci_low < r.effect_size < r.effect_ci_high
    assert r.n_per_group == (80, 80)


def test_compare_nonnormal_falls_back_to_mann_whitney(tmp_path) -> None:
    rng = np.random.default_rng(0)
    a = rng.standard_t(df=2, size=100)
    b = rng.standard_t(df=2, size=100) + 0.5
    df = pd.DataFrame({
        "group": ["A"] * 100 + ["B"] * 100,
        "value": np.concatenate([a, b]),
    })
    r = compare(df, value="value", group="group",
                store=_store(tmp_path), session_id="s1", bootstrap_n=200)
    assert r.method_used == "mann_whitney"
    assert r.effect_name == "cliffs_delta"


def test_compare_k_groups_eta_squared(tmp_path) -> None:
    rng = np.random.default_rng(1)
    rows = []
    for i, mean in enumerate([0.0, 1.0, 2.0]):
        vals = rng.normal(mean, 1.0, 80)
        rows.extend([(chr(65 + i), v) for v in vals])
    df = pd.DataFrame(rows, columns=["group", "value"])
    r = compare(df, value="value", group="group",
                store=_store(tmp_path), session_id="s1", bootstrap_n=200)
    assert r.method_used in {"anova", "kruskal"}
    assert r.effect_name == "eta_sq"
    assert r.effect_size > 0.2


def test_compare_raises_on_small_group(tmp_path) -> None:
    df = pd.DataFrame({
        "group": ["A"] * 4 + ["B"] * 40,
        "value": [1.0, 2, 3, 4] + list(range(40)),
    })
    with pytest.raises(ValueError, match="n="):
        compare(df, value="value", group="group",
                store=_store(tmp_path), session_id="s1", bootstrap_n=100)


def test_compare_paired_requires_paired_id(tmp_path) -> None:
    df = pd.DataFrame({
        "group": ["pre"] * 20 + ["post"] * 20,
        "value": list(range(20)) + [v + 1 for v in range(20)],
    })
    with pytest.raises(ValueError, match="paired_id"):
        compare(df, value="value", group="group", paired=True,
                store=_store(tmp_path), session_id="s1", bootstrap_n=100)
