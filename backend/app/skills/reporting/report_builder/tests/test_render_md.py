# backend/app/skills/report_builder/tests/test_render_md.py
from __future__ import annotations

from datetime import date


def _spec():
    from app.skills.reporting.report_builder.pkg.build import (
        Finding,
        FindingSection,
        Methodology,
        ReportSpec,
    )

    f = Finding(
        id="F-20260412-001",
        title="Revenue up 12% YoY",
        claim="Revenue grew 12%.",
        evidence_ids=("chart-ab12cd34", "tbl-12345678"),
        validated_by="val-11223344",
        verdict="PASS",
    )
    return ReportSpec(
        title="Q1 Revenue Review",
        author="Analytics",
        summary="Revenue rose across all regions except N.",
        key_points=("Rev up 12% YoY", "N region flat", "Churn steady"),
        findings=(FindingSection(finding=f, body="Growth driven by SMB retention."),),
        methodology=Methodology(
            method="Matched-period comparison",
            data_sources=("revenue_daily_v3",),
            caveats=("Excludes refunds.",),
        ),
        caveats=("Fiscal calendar shift affects comparability.",),
        appendix=("Extra discussion text.",),
    )


def test_render_research_memo_md_contains_key_sections() -> None:
    from app.skills.reporting.report_builder.pkg.render_md import render_md

    text = render_md(_spec(), template="research_memo", today=date(2026, 4, 12))
    assert "# Q1 Revenue Review" in text
    assert "Key points" in text
    assert "1. Rev up 12% YoY" in text
    assert "chart-ab12cd34" in text
    assert "val-11223344" in text
    assert "Methodology" in text
    assert "Caveats" in text


def test_render_analysis_brief_md_is_short() -> None:
    import re

    from app.skills.reporting.report_builder.pkg.render_md import render_md

    text = render_md(_spec(), template="analysis_brief", today=date(2026, 4, 12))
    # brief uses h1 and h3 only — no standalone h2 (## ) headings.
    assert re.search(r"(?m)^## [^#]", text) is None
    assert "Revenue up 12% YoY" in text
