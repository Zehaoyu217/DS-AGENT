from __future__ import annotations

from app.harness.guardrails.end_of_turn import end_of_turn
from app.harness.guardrails.types import Severity


def test_scratchpad_with_valid_structure_passes() -> None:
    scratchpad = """
## TODO
- [x] check

## COT
[01:00] picked pearson

## Findings
[F-20260412-001] X correlates with Y. Evidence: c1-abc. Validated: v1-xyz.

## Evidence
- c1-abc — scatter plot
"""
    findings = end_of_turn(scratchpad=scratchpad,
                           claims=[{"text": "X correlates with Y",
                                    "artifact_ids": ["c1-abc"]}])
    assert not findings


def test_missing_section_warns() -> None:
    scratchpad = "## TODO\n- [x] a\n"  # no COT/Findings/Evidence
    findings = end_of_turn(scratchpad=scratchpad, claims=[])
    codes = {f.code for f in findings}
    assert "scratchpad_missing_sections" in codes


def test_finding_without_artifact_citation_fails() -> None:
    scratchpad = """
## TODO
- [x] a

## COT
[01:00] x

## Findings
[F-20260412-002] Revenue grew 20%.

## Evidence
"""
    findings = end_of_turn(scratchpad=scratchpad,
                           claims=[{"text": "Revenue grew 20%",
                                    "artifact_ids": []}])
    assert any(f.code == "finding_without_citation"
               and f.severity is Severity.FAIL for f in findings)


def test_quantitative_claim_without_artifact_warns() -> None:
    scratchpad = """
## TODO
## COT
## Findings
## Evidence
"""
    findings = end_of_turn(
        scratchpad=scratchpad,
        claims=[{"text": "The uplift was 14.2%", "artifact_ids": []}],
    )
    assert any(f.code == "claim_without_artifact" for f in findings)
