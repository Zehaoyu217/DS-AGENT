# backend/app/skills/dashboard_builder/tests/test_build.py
from __future__ import annotations

from pathlib import Path


def _spec():
    from app.skills.dashboard_builder.pkg.build import (
        DashboardSpec,
        KPICard,
        SectionSpec,
    )

    return DashboardSpec(
        title="Build Dash",
        author="A",
        layout="bento",
        sections=(
            SectionSpec(
                kind="kpi",
                span=3,
                payload=KPICard(
                    label="MRR",
                    value=1_000_000,
                    delta=0.08,
                    comparison_period="last Q",
                    direction="up_is_good",
                    sparkline_artifact_id=None,
                    unit="USD",
                ),
            ),
        ),
        theme_variant="light",
        subtitle=None,
    )


def test_build_standalone_html_writes_file(tmp_path: Path, monkeypatch) -> None:
    from app.skills.dashboard_builder.pkg import build as build_mod

    monkeypatch.setattr(build_mod, "_OUTPUT_DIR", tmp_path)
    result = build_mod.build(_spec(), mode="standalone_html", session_id="s1")
    assert result.path is not None and result.path.exists()
    text = result.path.read_text()
    assert "Build Dash" in text
    assert "dash--bento" in text
    assert "theme--light" in text


def test_build_a2ui_returns_payload_no_path(monkeypatch) -> None:
    from app.skills.dashboard_builder.pkg import build as build_mod

    result = build_mod.build(_spec(), mode="a2ui", session_id="s2")
    assert result.path is None
    assert result.a2ui_payload is not None
    assert result.a2ui_payload["kind"] == "dashboard"
