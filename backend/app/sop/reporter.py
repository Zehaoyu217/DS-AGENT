"""Build and persist FailureReport from eval output."""
from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any, cast

import yaml

from app.evals.types import AgentTrace, LevelResult
from app.sop.types import (
    Baseline,
    DiffVsBaseline,
    DimensionScore,
    FailureReport,
    Grade,
    Signals,
)


def _extract_signals(trace: AgentTrace) -> Signals:
    kinds: Counter[str] = Counter()
    models: Counter[str] = Counter()
    for step in trace.intermediate:
        if isinstance(step, dict):
            kind = step.get("kind", "")
            kinds[kind] += 1
            if kind == "tool_call" and (model := step.get("model")):
                models[model] += 1
    return Signals(
        token_count=trace.token_count,
        duration_ms=trace.duration_ms,
        compaction_events=kinds.get("compaction", 0),
        scratchpad_writes=kinds.get("scratchpad_write", 0),
        tool_errors=kinds.get("tool_error", 0),
        retries=kinds.get("retry", 0),
        subagents_spawned=kinds.get("subagent_spawn", 0),
        models_used=dict(models),
    )


def _failure_signature(level_result: LevelResult) -> str:
    worst = min(level_result.dimensions, key=lambda d: d.score)
    return f"{worst.name}__{worst.grade}"


def _compute_diff(current: Signals, baseline: Baseline) -> DiffVsBaseline:
    before = baseline.signals.model_dump()
    after = current.model_dump()
    changes: dict[str, dict[str, Any]] = {}
    for key, b_val in before.items():
        a_val = after.get(key)
        if b_val != a_val:
            entry: dict[str, Any] = {"before": b_val, "after": a_val}
            if isinstance(b_val, int) and isinstance(a_val, int) and b_val > 0:
                entry["delta_pct"] = round((a_val - b_val) / b_val * 100, 2)
            changes[key] = entry
    return DiffVsBaseline(
        baseline_date=baseline.date,
        baseline_grade=baseline.grade,
        changes=changes,
    )


def build_failure_report(
    *,
    level_result: LevelResult,
    trace: AgentTrace,
    trace_id: str,
    trace_path: str,
    baseline: Baseline | None,
) -> FailureReport:
    signals = _extract_signals(trace)
    dims = [
        DimensionScore(name=d.name, score=cast("Grade", d.grade), weight=d.weight)
        for d in level_result.dimensions
    ]
    justifications = {d.name: d.justification for d in level_result.dimensions}
    diff = _compute_diff(signals, baseline) if baseline else None
    return FailureReport(
        level=level_result.level,
        overall_grade=cast("Grade", level_result.grade),
        dimensions=dims,
        signals=signals,
        judge_justifications=justifications,
        top_failure_signature=_failure_signature(level_result),
        trace_id=trace_id,
        trace_path=trace_path,
        diff_vs_baseline=diff,
    )


def write_failure_report(report: FailureReport, reports_dir: Path, *, date: str) -> Path:
    reports_dir.mkdir(parents=True, exist_ok=True)
    path = reports_dir / f"{date}-level{report.level}.yaml"
    path.write_text(yaml.safe_dump(report.model_dump(), sort_keys=False))
    return path
