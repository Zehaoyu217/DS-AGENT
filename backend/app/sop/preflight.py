"""Pre-flight triage: buckets 7 (evaluation bias), 8 (data quality), 9 (determinism)."""
from __future__ import annotations

from app.sop.types import FailureReport, PreflightResult, PreflightVerdict

JUDGE_VARIANCE_THRESHOLD = 0.5


def _evaluation_bias(judge_variance: dict[str, float]) -> PreflightVerdict:
    if not judge_variance:
        return "skipped"
    return "fail" if max(judge_variance.values()) > JUDGE_VARIANCE_THRESHOLD else "pass"


def _data_quality(seed_fingerprint_matches: bool) -> PreflightVerdict:
    return "pass" if seed_fingerprint_matches else "fail"


def _determinism(rerun_grades: list[str]) -> PreflightVerdict:
    if len(rerun_grades) < 2:
        return "skipped"
    return "pass" if len(set(rerun_grades)) == 1 else "fail"


def run_preflight(
    *,
    report: FailureReport,
    judge_variance: dict[str, float],
    seed_fingerprint_matches: bool,
    rerun_grades: list[str],
) -> PreflightResult:
    """Run the three pre-flight checks. `report` is reserved for future signal use."""
    del report
    return PreflightResult(
        evaluation_bias=_evaluation_bias(judge_variance),
        data_quality=_data_quality(seed_fingerprint_matches),
        determinism=_determinism(rerun_grades),
    )
