# backend/app/skills/report_builder/tests/test_build.py
from __future__ import annotations

from pathlib import Path

import pytest


def _spec_minimal():
    from app.skills.reporting.report_builder.pkg.build import (
        Finding,
        FindingSection,
        Methodology,
        ReportSpec,
    )

    f = Finding(
        id="F-20260412-100",
        title="Signal",
        claim="Claim",
        evidence_ids=("chart-abcdef01",),
        validated_by="val-12345678",
        verdict="PASS",
    )
    return ReportSpec(
        title="Report",
        author="Me",
        summary="Summary",
        key_points=("a", "b", "c"),
        findings=(FindingSection(finding=f, body="body"),),
        methodology=Methodology(method="ols", data_sources=("x",), caveats=("c",)),
        caveats=("c",),
        appendix=(),
    )


def test_build_returns_paths_for_every_requested_format(tmp_path: Path, monkeypatch) -> None:
    from app.skills.reporting.report_builder.pkg import build as build_mod

    monkeypatch.setattr(build_mod, "_OUTPUT_DIR", tmp_path)

    result = build_mod.build(
        _spec_minimal(),
        template="research_memo",
        formats=("md", "html"),
        session_id="sess-1",
    )
    assert set(result.formats) == {"md", "html"}
    assert result.paths["md"].exists()
    assert result.paths["html"].exists()
    assert result.paths["md"].read_text().startswith("# Report")


def test_build_rejects_failed_finding() -> None:
    from app.skills.reporting.report_builder.pkg import build as build_mod
    from app.skills.reporting.report_builder.pkg.build import (
        Finding,
        FindingSection,
        Methodology,
        ReportSpec,
    )

    bad = Finding(
        id="F-X",
        title="t",
        claim="c",
        evidence_ids=("e-1",),
        validated_by="v-1",
        verdict="FAIL",
    )
    spec = ReportSpec(
        title="t",
        author="a",
        summary="s",
        key_points=("a", "b", "c"),
        findings=(FindingSection(finding=bad, body="."),),
        methodology=Methodology(method="m", data_sources=("x",), caveats=("c",)),
        caveats=("x",),
        appendix=(),
    )
    with pytest.raises(ValueError, match="FAILED_FINDING"):
        build_mod.build(spec, template="research_memo", formats=("md",), session_id="sess-2")
