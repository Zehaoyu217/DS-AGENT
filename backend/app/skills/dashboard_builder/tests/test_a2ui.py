# backend/app/skills/dashboard_builder/tests/test_a2ui.py
from __future__ import annotations


def _spec_with_kpi_and_chart():
    from app.skills.dashboard_builder.pkg.build import (
        DashboardSpec,
        KPICard,
        SectionSpec,
    )

    kpi_card = KPICard(
        label="MRR",
        value=1_250_000,
        delta=0.12,
        comparison_period="last Q",
        direction="up_is_good",
        sparkline_artifact_id="chart-sp000001",
        unit="USD",
    )
    return DashboardSpec(
        title="Q1 Dash",
        author="A",
        layout="bento",
        sections=(
            SectionSpec(kind="kpi", span=3, payload=kpi_card),
            SectionSpec(kind="chart", span=9, payload="chart-main0001", title="Revenue"),
        ),
        theme_variant="light",
        subtitle=None,
    )


def test_a2ui_has_version_and_tiles() -> None:
    from app.skills.dashboard_builder.pkg.a2ui import to_a2ui

    payload = to_a2ui(_spec_with_kpi_and_chart())
    assert payload["a2ui_version"] == "1"
    assert payload["kind"] == "dashboard"
    assert len(payload["tiles"]) == 2


def test_a2ui_chart_tile_references_artifact_id() -> None:
    from app.skills.dashboard_builder.pkg.a2ui import to_a2ui

    payload = to_a2ui(_spec_with_kpi_and_chart())
    chart_tile = next(t for t in payload["tiles"] if t["kind"] == "chart")
    assert chart_tile["artifact_id"] == "chart-main0001"
    assert chart_tile["span"] == 9
