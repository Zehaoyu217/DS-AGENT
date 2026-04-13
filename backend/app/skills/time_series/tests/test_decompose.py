from __future__ import annotations

import pytest

from app.skills.time_series.decompose import decompose


def test_decompose_seasonal_series_returns_three_components(seasonal_240) -> None:
    d = decompose(seasonal_240, period=12)
    assert d.trend is not None
    assert d.seasonal is not None
    assert d.residual is not None
    assert len(d.trend) == len(seasonal_240)


def test_decompose_requires_period_when_not_auto(seasonal_240) -> None:
    with pytest.raises(ValueError, match="period"):
        decompose(seasonal_240.to_numpy(), period=None)
