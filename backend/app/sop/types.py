"""Pydantic models for SOP data contracts."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

Grade = Literal["A", "B", "C", "F"]
PreflightVerdict = Literal["pass", "fail", "skipped"]
CostBucket = Literal["trivial", "small", "medium", "large"]


class Signals(BaseModel):
    model_config = ConfigDict(frozen=True)

    token_count: int
    duration_ms: int
    compaction_events: int
    scratchpad_writes: int
    tool_errors: int
    retries: int
    subagents_spawned: int
    models_used: dict[str, int]


class DimensionScore(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    score: Grade
    weight: float = Field(ge=0.0, le=1.0)


class DiffVsBaseline(BaseModel):
    model_config = ConfigDict(frozen=True)

    baseline_date: str
    baseline_grade: Grade
    changes: dict[str, dict[str, Any]]


class FailureReport(BaseModel):
    model_config = ConfigDict(frozen=True)

    level: int = Field(ge=1, le=5)
    overall_grade: Grade
    dimensions: list[DimensionScore]
    signals: Signals
    judge_justifications: dict[str, str]
    top_failure_signature: str
    trace_id: str
    trace_path: str
    diff_vs_baseline: DiffVsBaseline | None


class Baseline(BaseModel):
    model_config = ConfigDict(frozen=True)

    level: int = Field(ge=1, le=5)
    date: str
    trace_id: str
    signals: Signals


class PreflightResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    evaluation_bias: PreflightVerdict
    data_quality: PreflightVerdict
    determinism: PreflightVerdict

    def any_failed(self) -> bool:
        return "fail" in (self.evaluation_bias, self.data_quality, self.determinism)


class TriageDecision(BaseModel):
    model_config = ConfigDict(frozen=True)

    bucket: str
    evidence: list[str]
    hypothesis: str


class FixApplied(BaseModel):
    model_config = ConfigDict(frozen=True)

    ladder_id: str
    name: str
    files_changed: list[str]
    model_used_for_fix: str
    cost_bucket: CostBucket


class IterationLogEntry(BaseModel):
    model_config = ConfigDict(frozen=True)

    date: str
    session_id: str
    level: int = Field(ge=1, le=5)
    overall_grade_before: Grade
    preflight: PreflightResult
    triage: TriageDecision
    fix: FixApplied
    outcome: dict[str, Any]
    trace_links: dict[str, str]


class LadderRung(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    cost: CostBucket
    files: list[str]
    pattern: str | None = None


class LadderDefinition(BaseModel):
    model_config = ConfigDict(frozen=True)

    bucket: str
    description: str
    triage_signals: list[str]
    ladder: list[LadderRung]
