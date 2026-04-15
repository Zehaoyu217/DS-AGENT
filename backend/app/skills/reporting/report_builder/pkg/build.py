# backend/app/skills/report_builder/pkg/build.py
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

Template = Literal["research_memo", "analysis_brief", "full_report"]
Verdict = Literal["PASS", "WARN", "FAIL"]


@dataclass(frozen=True)
class Finding:
    id: str                         # e.g. F-20260412-001
    title: str
    claim: str
    evidence_ids: tuple[str, ...]
    validated_by: str               # stat_validate artifact id
    verdict: Verdict


@dataclass(frozen=True)
class FindingSection:
    finding: Finding
    body: str                       # markdown
    chart_id: str | None = None
    table_id: str | None = None
    caveats: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class Methodology:
    method: str
    data_sources: tuple[str, ...]
    caveats: tuple[str, ...]


@dataclass(frozen=True)
class ReportSpec:
    title: str
    author: str
    summary: str
    key_points: tuple[str, ...]
    findings: tuple[FindingSection, ...]
    methodology: Methodology
    caveats: tuple[str, ...]
    appendix: tuple[str, ...]
    theme_variant: str = "editorial"
    subtitle: str | None = None


@dataclass(frozen=True)
class ReportResult:
    template: Template
    formats: tuple[str, ...]
    paths: dict[str, Path]          # format → absolute path
    artifact_ids: dict[str, str]    # format → artifact id


_REQUIRED_KP = {"research_memo": 3, "analysis_brief": 3, "full_report": 3}


def validate_spec(spec: ReportSpec, template: Template) -> None:
    if template not in _REQUIRED_KP:
        raise ValueError(
            f"UNKNOWN_TEMPLATE: Unknown template '{template}'. "
            f"Use research_memo | analysis_brief | full_report."
        )
    n = _REQUIRED_KP[template]
    if len(spec.key_points) != n:
        raise ValueError(
            f"WRONG_KEY_POINT_COUNT: {template} requires exactly {n} key points, "
            f"got {len(spec.key_points)}."
        )
    if not spec.methodology.method.strip() or not spec.methodology.data_sources:
        raise ValueError("MISSING_METHODOLOGY: Methodology section is required.")
    if not spec.caveats:
        raise ValueError("MISSING_METHODOLOGY: Caveats must not be empty.")
    for fs in spec.findings:
        if fs.finding.verdict == "FAIL":
            raise ValueError(
                f"FAILED_FINDING: Finding {fs.finding.id} has stat_validate "
                "verdict FAIL; cannot include."
            )
        if not fs.finding.evidence_ids:
            raise ValueError(
                f"FAILED_FINDING: Finding {fs.finding.id} has no evidence_ids."
            )


# ---------------------------------------------------------------------------
# Orchestrator. Appended after the contracts + validate_spec above.
# ---------------------------------------------------------------------------
from datetime import date as _date  # noqa: E402

from app.skills.reporting.report_builder.pkg.render_html import render_html  # noqa: E402
from app.skills.reporting.report_builder.pkg.render_md import render_md  # noqa: E402

_OUTPUT_DIR = Path("data/reports")  # overridable in tests


def build(
    spec: ReportSpec,
    template: Template = "research_memo",
    formats: tuple[str, ...] = ("md", "html"),
    session_id: str | None = None,
    today: _date | None = None,
) -> ReportResult:
    validate_spec(spec, template)

    today = today or _date.today()
    base = _OUTPUT_DIR / (session_id or "default")
    base.mkdir(parents=True, exist_ok=True)

    stem = _slugify(spec.title) or "report"
    paths: dict[str, Path] = {}
    artifact_ids: dict[str, str] = {}

    if "md" in formats:
        p = base / f"{stem}.md"
        p.write_text(render_md(spec, template=template, today=today), encoding="utf-8")
        paths["md"] = p
        artifact_ids["md"] = f"report-md-{stem}"

    if "html" in formats:
        p = base / f"{stem}.html"
        p.write_text(render_html(spec, template=template, today=today), encoding="utf-8")
        paths["html"] = p
        artifact_ids["html"] = f"report-html-{stem}"

    if "pdf" in formats:
        from app.skills.reporting.report_builder.pkg.render_pdf import render_pdf

        p = base / f"{stem}.pdf"
        render_pdf(spec, template=template, output_path=p, today=today)
        paths["pdf"] = p
        artifact_ids["pdf"] = f"report-pdf-{stem}"

    return ReportResult(
        template=template,
        formats=formats,
        paths=paths,
        artifact_ids=artifact_ids,
    )


def _slugify(s: str) -> str:
    import re

    s = re.sub(r"[^A-Za-z0-9]+", "-", s.strip().lower())
    return s.strip("-")
