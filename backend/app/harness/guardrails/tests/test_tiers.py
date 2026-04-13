from __future__ import annotations

from app.harness.guardrails.tiers import apply_tier
from app.harness.guardrails.types import GuardrailFinding, GuardrailOutcome, Severity


def _finding(sev: Severity) -> GuardrailFinding:
    return GuardrailFinding(code="demo", severity=sev, message="m")


def test_strict_fail_blocks() -> None:
    out = apply_tier(tier="strict", findings=[_finding(Severity.FAIL)])
    assert out == GuardrailOutcome.BLOCK


def test_strict_warn_does_not_block() -> None:
    out = apply_tier(tier="strict", findings=[_finding(Severity.WARN)])
    assert out == GuardrailOutcome.WARN


def test_advisory_fail_warns_only() -> None:
    out = apply_tier(tier="advisory", findings=[_finding(Severity.FAIL)])
    assert out == GuardrailOutcome.WARN


def test_observatory_never_blocks_or_warns() -> None:
    out = apply_tier(tier="observatory", findings=[_finding(Severity.FAIL)])
    assert out == GuardrailOutcome.OBSERVE
