from __future__ import annotations

import re

from app.harness.guardrails.types import GuardrailFinding, Severity

REQUIRED_SECTIONS = ("## TODO", "## COT", "## Findings", "## Evidence")
FINDING_LINE_RE = re.compile(r"^\[F-\d{8}-\d{3}\]", re.MULTILINE)
NUMBER_RE = re.compile(r"(-?\d+(?:\.\d+)?\s*%?)")


def _section_bodies(scratchpad: str) -> dict[str, str]:
    bodies: dict[str, str] = {s: "" for s in REQUIRED_SECTIONS}
    current = None
    for line in scratchpad.splitlines():
        stripped = line.strip()
        if stripped in REQUIRED_SECTIONS:
            current = stripped
            continue
        if current:
            bodies[current] += line + "\n"
    return bodies


def _has_quantitative_shape(text: str) -> bool:
    return bool(NUMBER_RE.search(text))


def end_of_turn(
    scratchpad: str,
    claims: list[dict],
) -> list[GuardrailFinding]:
    findings: list[GuardrailFinding] = []

    missing = [s for s in REQUIRED_SECTIONS if s not in scratchpad]
    if missing:
        findings.append(GuardrailFinding(
            code="scratchpad_missing_sections",
            severity=Severity.WARN,
            message=f"scratchpad missing required sections: {missing}",
        ))

    bodies = _section_bodies(scratchpad)
    findings_body = bodies.get("## Findings", "")
    for match in FINDING_LINE_RE.finditer(findings_body):
        # extract full finding block (one line after)
        start = match.start()
        end = findings_body.find("\n", start)
        block = findings_body[start:end if end != -1 else None]
        if "Evidence:" not in block or "Validated:" not in block:
            findings.append(GuardrailFinding(
                code="finding_without_citation",
                severity=Severity.FAIL,
                message=f"finding missing Evidence/Validated fields: {block[:80]}",
            ))

    for claim in claims:
        text = str(claim.get("text", ""))
        ids = claim.get("artifact_ids") or []
        if _has_quantitative_shape(text) and not ids:
            findings.append(GuardrailFinding(
                code="claim_without_artifact",
                severity=Severity.WARN,
                message=f"quantitative claim without artifact: {text[:80]}",
            ))

    return findings
