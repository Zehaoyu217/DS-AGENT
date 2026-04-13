from __future__ import annotations

from app.knowledge.gotchas import (
    GOTCHA_SLUGS,
    GotchaIndex,
    load_gotcha,
    load_index,
)


def test_all_slugs_present() -> None:
    assert len(GOTCHA_SLUGS) == 14
    expected = {
        "base_rate_neglect",
        "berksons_paradox",
        "confounding",
        "ecological_fallacy",
        "immortal_time_bias",
        "look_ahead_bias",
        "multicollinearity",
        "multiple_comparisons",
        "non_stationarity",
        "regression_to_mean",
        "selection_bias",
        "simpsons_paradox",
        "spurious_correlation",
        "survivorship_bias",
    }
    assert set(GOTCHA_SLUGS) == expected


def test_load_index_produces_one_line_per_slug() -> None:
    idx: GotchaIndex = load_index()
    assert len(idx.entries) == 14
    for slug, one_liner in idx.entries.items():
        assert slug in GOTCHA_SLUGS
        assert len(one_liner) <= 140
        assert "\n" not in one_liner


def test_load_gotcha_returns_body() -> None:
    body = load_gotcha("simpsons_paradox")
    assert "Simpson" in body
    assert "remedy" in body.lower() or "mitigation" in body.lower()


def test_load_gotcha_unknown_raises() -> None:
    import pytest
    with pytest.raises(KeyError):
        load_gotcha("not_a_real_gotcha")
