"""Rubric YAML loader for the eval framework."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass(frozen=True)
class DimensionRubric:
    """Grading rubric for a single dimension."""

    weight: float
    type: str  # "deterministic", "llm_judge", "hybrid"
    criteria: dict[str, str]  # A/B/C descriptions
    deterministic: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class RubricConfig:
    """Parsed rubric configuration for one evaluation level."""

    level: int
    name: str
    prompt: str
    prompt_sequence: list[str]
    dimensions: dict[str, DimensionRubric]
    grading_thresholds: dict[str, float]
    token_budget_optimal: int | None = None


def load_rubric(path: Path) -> RubricConfig:
    """Load and parse a rubric YAML file."""
    data = yaml.safe_load(path.read_text())

    dimensions: dict[str, DimensionRubric] = {}
    for name, dim in data["dimensions"].items():
        dimensions[name] = DimensionRubric(
            weight=dim["weight"],
            type=dim["type"],
            criteria=dim["criteria"],
            deterministic=dim.get("deterministic", []),
        )

    return RubricConfig(
        level=data["level"],
        name=data["name"],
        prompt=data.get("prompt", ""),
        prompt_sequence=data.get("prompt_sequence", []),
        dimensions=dimensions,
        grading_thresholds=data["grading"],
        token_budget_optimal=data.get("token_budget_optimal"),
    )
