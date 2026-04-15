from __future__ import annotations

import numpy as np
import pandas as pd

from app.skills.statistical_analysis.correlation.preprocess import (
    apply_detrend,
    drop_na_rows,
    partial_residuals,
)


def test_drop_na_rows_reports_count() -> None:
    df = pd.DataFrame({"x": [1.0, 2.0, np.nan, 4.0], "y": [1, np.nan, 3, 4]})
    out, dropped = drop_na_rows(df[["x", "y"]])
    assert dropped == 2
    assert len(out) == 2
    assert out.iloc[0].tolist() == [1.0, 1.0]


def test_apply_detrend_difference_shortens_by_one() -> None:
    s = pd.Series([1.0, 2, 4, 7, 11])
    out = apply_detrend(s, method="difference")
    assert len(out) == len(s) - 1
    assert out.tolist() == [1.0, 2.0, 3.0, 4.0]


def test_apply_detrend_none_passthrough() -> None:
    s = pd.Series([1.0, 2, 3])
    out = apply_detrend(s, method=None)
    assert out.equals(s)


def test_partial_residuals_removes_common_cause(confounded_df) -> None:
    x_res, y_res = partial_residuals(
        x=confounded_df["x"].to_numpy(),
        y=confounded_df["y"].to_numpy(),
        z=confounded_df[["confounder"]].to_numpy(),
    )
    r_raw = np.corrcoef(confounded_df["x"], confounded_df["y"])[0, 1]
    r_partial = np.corrcoef(x_res, y_res)[0, 1]
    assert abs(r_partial) < abs(r_raw) - 0.4
