"""Main triage: evaluate bucket signals in cost order, stop at first actionable."""
from __future__ import annotations

from collections.abc import Callable

from app.sop.types import FailureReport, TriageDecision


def _check_context(r: FailureReport) -> list[str] | None:
    evidence: list[str] = []
    if r.signals.compaction_events >= 3:
        evidence.append(f"compaction_events={r.signals.compaction_events} in one session")
    if r.signals.scratchpad_writes == 0 and r.signals.token_count > 5000:
        evidence.append("scratchpad_writes=0 with substantial token usage")
    if r.diff_vs_baseline and "token_count" in r.diff_vs_baseline.changes:
        chg = r.diff_vs_baseline.changes["token_count"]
        before, after = chg.get("before"), chg.get("after")
        if (
            isinstance(before, int) and isinstance(after, int)
            and before > 0 and after > before * 1.5
        ):
            evidence.append(f"token_count {before} -> {after} (>1.5x baseline)")
    return evidence or None


# Heuristic: substring match on judge justifications. False positives acceptable;
# wrong-bucket fixes surface in the iteration log and prompt moving on.
def _check_prompt(r: FailureReport) -> list[str] | None:
    keywords = ("ignored", "contradic", "missing guidance", "unclear instruction")
    hits = [
        f"judge cites `{k}` in {dim}"
        for dim, text in r.judge_justifications.items()
        for k in keywords
        if k in text.lower()
    ]
    return hits or None


# Heuristic: substring match on judge justifications. False positives acceptable;
# wrong-bucket fixes surface in the iteration log and prompt moving on.
def _check_capability(r: FailureReport) -> list[str] | None:
    hits = [
        f"judge flags wrong output in {dim}"
        for dim, text in r.judge_justifications.items()
        if "wrong" in text.lower() or "incorrect" in text.lower()
    ]
    if r.signals.tool_errors > 0 and r.signals.retries > r.signals.tool_errors:
        hits.append("repeated retries on same tool (skill churn)")
    return hits or None


def _check_routing(r: FailureReport) -> list[str] | None:
    models = r.signals.models_used
    if not models:
        return None
    sonnet = models.get("sonnet", 0)
    haiku = models.get("haiku", 0)
    # Level 1 tasks are mechanical (format/extract) and haiku-only is correct.
    if haiku > 0 and sonnet == 0 and r.level >= 2:
        return [f"models_used has no sonnet on level {r.level} (reasoning-heavy)"]
    return None


def _check_architecture(r: FailureReport) -> list[str] | None:
    if r.level == 5 and r.signals.subagents_spawned == 0:
        return ["level 5 with subagents_spawned=0 (single-loop state tracking)"]
    return None


def _check_harness(r: FailureReport) -> list[str] | None:
    if r.signals.tool_errors > 0 and r.signals.retries == 0:
        return [f"tool_errors={r.signals.tool_errors} with retries=0"]
    return None


BUCKET_CHECKS: dict[str, Callable[[FailureReport], list[str] | None]] = {
    "context": _check_context,
    "prompt": _check_prompt,
    "capability": _check_capability,
    "routing": _check_routing,
    "architecture": _check_architecture,
    "harness": _check_harness,
}

# Single source of truth for iteration order (dict preserves insertion order, Python 3.7+).
TRIAGE_ORDER: tuple[str, ...] = tuple(BUCKET_CHECKS)


_HYPOTHESIS_TEMPLATES: dict[str, str] = {
    "context": "Context layer is leaking or compaction is mis-tuned",
    "prompt": "System prompt has a gap or a conflicting directive",
    "capability": "Skill output is incorrect or skill is churning",
    "routing": "Wrong model selected for the step",
    "architecture": "Single-loop cannot hold multi-step state; subagent needed",
    "harness": "Tool-error path has no retry or fallback",
}


def _hypothesis(bucket: str, evidence: list[str]) -> str:
    return f"{_HYPOTHESIS_TEMPLATES[bucket]} (evidence: {'; '.join(evidence)})"


def triage(report: FailureReport) -> TriageDecision | None:
    """Return the first bucket (cost-ordered) whose signals fire, else None."""
    for bucket, check in BUCKET_CHECKS.items():
        evidence = check(report)
        if evidence:
            return TriageDecision(
                bucket=bucket,
                evidence=evidence,
                hypothesis=_hypothesis(bucket, evidence),
            )
    return None
