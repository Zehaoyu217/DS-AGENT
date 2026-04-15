# backend/app/skills/report_builder/tests/test_render_pdf.py
from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest


def _spec():
    from app.skills.report_builder.pkg.build import (
        Finding,
        FindingSection,
        Methodology,
        ReportSpec,
    )

    f = Finding(
        id="F-20260412-020",
        title="X",
        claim="y",
        evidence_ids=("e-1",),
        validated_by="v-1",
        verdict="PASS",
    )
    return ReportSpec(
        title="PDF Smoke",
        author="A",
        summary="S",
        key_points=("1", "2", "3"),
        findings=(FindingSection(finding=f, body="x"),),
        methodology=Methodology(method="m", data_sources=("d",), caveats=("mc",)),
        caveats=("c",),
        appendix=(),
    )


def test_render_pdf_produces_nonempty_bytes_or_skips(tmp_path: Path) -> None:
    from app.skills.report_builder.pkg import render_pdf

    out = tmp_path / "r.pdf"
    try:
        render_pdf.render_pdf(
            _spec(),
            template="research_memo",
            output_path=out,
            today=date(2026, 4, 12),
        )
    except render_pdf.PDFBackendUnavailable:
        pytest.skip("weasyprint unavailable on this host")
    assert out.exists()
    assert out.stat().st_size > 0
    assert out.read_bytes()[:4] == b"%PDF"
