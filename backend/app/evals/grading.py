"""Grade calculations and rollup logic for the eval framework."""

from __future__ import annotations

from app.evals.types import DimensionGrade, EvalResult, LevelResult

GRADE_SCORES: dict[str, float] = {"A": 1.0, "B": 0.7, "C": 0.4, "F": 0.0}

GRADE_THRESHOLDS: list[tuple[str, float]] = [
    ("A", 0.85),
    ("B", 0.60),
    ("C", 0.40),
]


def grade_to_score(grade: str) -> float:
    """Convert a letter grade to its numeric score."""
    return GRADE_SCORES[grade]


def score_to_grade(score: float) -> str:
    """Convert a numeric score to a letter grade using thresholds."""
    for letter, threshold in GRADE_THRESHOLDS:
        if score >= threshold:
            return letter
    return "F"


def calculate_weighted_score(dimensions: list[DimensionGrade]) -> float:
    """Calculate the weighted score across graded dimensions."""
    if not dimensions:
        return 0.0
    return sum(d.score * d.weight for d in dimensions)


def grade_level(
    level: int,
    name: str,
    dimensions: list[DimensionGrade],
) -> LevelResult:
    """Produce a graded LevelResult from scored dimensions."""
    weighted = calculate_weighted_score(dimensions)
    return LevelResult(
        level=level,
        name=name,
        dimensions=dimensions,
        weighted_score=round(weighted, 4),
        grade=score_to_grade(weighted),
    )


def grade_eval(levels: list[LevelResult]) -> EvalResult:
    """Aggregate level results into an overall EvalResult."""
    if not levels:
        return EvalResult(levels=[], overall_score=0.0, overall_grade="F")
    avg = sum(lev.weighted_score for lev in levels) / len(levels)
    return EvalResult(
        levels=levels,
        overall_score=round(avg, 4),
        overall_grade=score_to_grade(avg),
    )
