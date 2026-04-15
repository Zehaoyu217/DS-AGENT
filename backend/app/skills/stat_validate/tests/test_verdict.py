from __future__ import annotations

from app.skills.stat_validate.verdict import Check, Validation, Violation


def test_validation_status_rolls_up_from_violations() -> None:
    v = Validation(
        status="PASS",
        failures=(),
        warnings=(Violation(code="multiple_comparisons", severity="WARN",
                            message="ran 8 tests", gotcha_refs=("multiple_comparisons",)),),
        passes=(Check(code="effect_size", message="d=0.4 CI[0.2,0.6]"),),
    )
    assert v.rollup_status() == "WARN"


def test_validation_status_fail_wins() -> None:
    v = Validation(
        status="PASS",
        failures=(Violation(code="effect_size", severity="FAIL",
                            message="d CI entirely in negligible",
                            gotcha_refs=()),),
        warnings=(),
        passes=(),
    )
    assert v.rollup_status() == "FAIL"


def test_gotcha_refs_are_deduplicated() -> None:
    v = Validation(
        status="PASS",
        failures=(),
        warnings=(
            Violation("a", "WARN", "x", gotcha_refs=("confounding",)),
            Violation("b", "WARN", "y", gotcha_refs=("confounding", "simpsons_paradox")),
        ),
        passes=(),
    )
    assert v.gotcha_refs() == ("confounding", "simpsons_paradox")
