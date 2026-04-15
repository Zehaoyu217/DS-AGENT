# backend/app/skills/dashboard_builder/tests/test_layouts.py
from __future__ import annotations


def test_grid_layout_forces_uniform_span() -> None:
    from app.skills.reporting.dashboard_builder.pkg.layouts import resolve_spans

    spans = resolve_spans([12, 6, 3, 4, 12], layout="grid")
    assert set(spans) == {4}


def test_single_column_layout_forces_full_span() -> None:
    from app.skills.reporting.dashboard_builder.pkg.layouts import resolve_spans

    spans = resolve_spans([1, 2, 3], layout="single_column")
    assert spans == [12, 12, 12]


def test_bento_preserves_requested_spans_clamped_to_12() -> None:
    from app.skills.reporting.dashboard_builder.pkg.layouts import resolve_spans

    assert resolve_spans([3, 6, 20, 0], layout="bento") == [3, 6, 12, 1]
