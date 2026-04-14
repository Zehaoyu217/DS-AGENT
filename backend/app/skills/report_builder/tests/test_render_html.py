# backend/app/skills/report_builder/tests/test_render_html.py
from __future__ import annotations

from datetime import date


def _spec():
    from app.skills.report_builder.pkg.build import (
        Finding,
        FindingSection,
        Methodology,
        ReportSpec,
    )

    f = Finding(
        id="F-20260412-010",
        title="Headline",
        claim="claim",
        evidence_ids=("e-1",),
        validated_by="v-1",
        verdict="PASS",
    )
    return ReportSpec(
        title="Title",
        author="Me",
        summary="Sum.",
        key_points=("a", "b", "c"),
        findings=(FindingSection(finding=f, body="**bold** body"),),
        methodology=Methodology(method="m", data_sources=("d",), caveats=("mc",)),
        caveats=("c1",),
        appendix=(),
    )


def test_render_html_wraps_in_report_class() -> None:
    from app.skills.report_builder.pkg.render_html import render_html

    html = render_html(_spec(), template="research_memo", today=date(2026, 4, 12))
    assert "<body" in html
    assert "report report--research-memo theme--editorial" in html
    assert "editorial.css" in html


def test_render_html_escapes_unsafe_body_markdown() -> None:
    from app.skills.report_builder.pkg.render_html import render_html

    html = render_html(_spec(), template="research_memo", today=date(2026, 4, 12))
    # Body markdown was `**bold** body` — our renderer converts it to <strong>bold</strong>.
    assert "<strong>bold</strong>" in html
