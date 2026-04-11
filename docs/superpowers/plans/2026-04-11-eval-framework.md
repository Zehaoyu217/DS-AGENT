# Eval Framework Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a 5-level agent evaluation framework with deterministic banking data in DuckDB, multi-dimensional A/B/C rubric grading, and an LLM judge pipeline.

**Architecture:** Seed script generates a deterministic "First National Bank" dataset into `eval.db`. Core eval types define the `AgentInterface` protocol and grading structures. Rubric YAML files define per-level grading criteria. The LLM judge (local Ollama) handles qualitative grading. A pytest-based eval runner executes a mock agent against each level and produces graded results. Unit tests validate the framework itself; eval tests (in `tests/evals/`) run the full pipeline.

**Tech Stack:** Python 3.12+, DuckDB, Faker, pytest, httpx (Ollama), PyYAML

**Spec:** `docs/superpowers/specs/2026-04-11-eval-framework-design.md`

---

## File Structure

```
backend/
├── scripts/
│   └── seed_eval_data.py              # Deterministic dataset → eval.db
├── app/
│   └── evals/
│       ├── __init__.py                # Empty package init
│       ├── types.py                   # AgentTrace, AgentInterface, grade types
│       ├── grading.py                 # Score calculations, grade rollup
│       ├── rubric.py                  # Rubric YAML loader
│       ├── judge.py                   # LLM judge (Ollama wrapper)
│       └── runner.py                  # evaluate_level(), format helpers
├── tests/
│   ├── unit/
│   │   ├── test_eval_types.py
│   │   ├── test_eval_grading.py
│   │   ├── test_eval_rubric.py
│   │   ├── test_eval_judge.py
│   │   ├── test_eval_runner.py
│   │   └── test_seed_eval.py
│   └── evals/
│       ├── __init__.py
│       ├── conftest.py                # eval_db, mock agents, judge fixtures
│       ├── rubrics/
│       │   ├── level1_rendering.yaml
│       │   ├── level2_exploration.yaml
│       │   ├── level3_anomaly.yaml
│       │   ├── level4_free_explore.yaml
│       │   └── level5_stress.yaml
│       ├── test_level1.py
│       ├── test_level2.py
│       ├── test_level3.py
│       ├── test_level4.py
│       └── test_level5.py
Makefile                               # Add seed-eval, eval targets
```

---

### Task 1: Dependencies + Package Scaffold

**Files:**
- Modify: `backend/pyproject.toml`
- Create: `backend/app/evals/__init__.py`
- Create: `backend/tests/evals/__init__.py`
- Create: `backend/tests/evals/rubrics/` (directory)

- [ ] **Step 1: Add faker dependency to pyproject.toml**

Add `faker>=33.0.0` to the main dependencies list:

```toml
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.34.0",
    "pydantic>=2.10.0",
    "pydantic-settings>=2.7.0",
    "duckdb>=1.2.0",
    "polars>=1.20.0",
    "httpx>=0.28.0",
    "pyyaml>=6.0",
    "faker>=33.0.0",
]
```

- [ ] **Step 2: Create package directories and init files**

```bash
mkdir -p backend/app/evals
mkdir -p backend/tests/evals/rubrics
touch backend/app/evals/__init__.py
touch backend/tests/evals/__init__.py
```

- [ ] **Step 3: Install updated dependencies**

Run: `cd backend && pip install -e ".[dev]"`
Expected: faker installs successfully.

- [ ] **Step 4: Verify packages import**

Run: `cd backend && python -c "import faker; import duckdb; import yaml; print('OK')"`
Expected: `OK`

- [ ] **Step 5: Commit**

```bash
git add backend/pyproject.toml backend/app/evals/__init__.py backend/tests/evals/__init__.py
git commit -m "chore: add faker dependency and eval package scaffold"
```

---

### Task 2: Core Types — AgentTrace, AgentInterface, Grade Types

**Files:**
- Create: `backend/app/evals/types.py`
- Create: `backend/tests/unit/test_eval_types.py`

- [ ] **Step 1: Write failing tests for all eval types**

Create `backend/tests/unit/test_eval_types.py`:

```python
from __future__ import annotations

from app.evals.types import (
    AgentInterface,
    AgentTrace,
    DimensionGrade,
    EvalResult,
    LevelResult,
)


def test_agent_trace_creation() -> None:
    trace = AgentTrace(
        queries=["SELECT 1"],
        intermediate=[{"rows": 10}],
        final_output="Done",
        token_count=100,
        duration_ms=500,
        errors=[],
    )
    assert trace.queries == ["SELECT 1"]
    assert trace.token_count == 100
    assert trace.errors == []


def test_agent_trace_is_frozen() -> None:
    trace = AgentTrace(
        queries=[], intermediate=[], final_output="",
        token_count=0, duration_ms=0, errors=[],
    )
    try:
        trace.token_count = 999  # type: ignore[misc]
        assert False, "Should have raised"
    except AttributeError:
        pass


def test_dimension_grade_creation() -> None:
    grade = DimensionGrade(
        name="chart",
        grade="B",
        score=0.7,
        weight=0.3,
        justification="Axes labeled, amounts accurate",
    )
    assert grade.grade == "B"
    assert grade.score == 0.7
    assert grade.weight == 0.3


def test_level_result_creation() -> None:
    dims = [
        DimensionGrade(name="a", grade="A", score=1.0, weight=0.5, justification=""),
        DimensionGrade(name="b", grade="C", score=0.4, weight=0.5, justification=""),
    ]
    result = LevelResult(
        level=1, name="Basic", dimensions=dims, weighted_score=0.7, grade="B",
    )
    assert result.grade == "B"
    assert result.weighted_score == 0.7
    assert len(result.dimensions) == 2


def test_eval_result_creation() -> None:
    level = LevelResult(
        level=1, name="Basic", dimensions=[], weighted_score=0.7, grade="B",
    )
    result = EvalResult(
        levels=[level], overall_score=0.7, overall_grade="B",
    )
    assert result.overall_grade == "B"
    assert len(result.levels) == 1


class _MockAgent:
    async def run(self, prompt: str, db_path: str) -> AgentTrace:
        return AgentTrace(
            queries=[], intermediate=[], final_output="mock",
            token_count=0, duration_ms=0, errors=[],
        )


def test_agent_interface_protocol_compliance() -> None:
    agent: AgentInterface = _MockAgent()
    assert isinstance(agent, AgentInterface)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd backend && python -m pytest tests/unit/test_eval_types.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'app.evals.types'`

- [ ] **Step 3: Implement all eval types**

Create `backend/app/evals/types.py`:

```python
"""Core types for the agent evaluation framework."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable


@dataclass(frozen=True)
class AgentTrace:
    """Captured trace of an agent's execution."""

    queries: list[str]
    intermediate: list[Any]
    final_output: str
    token_count: int
    duration_ms: int
    errors: list[str]


@runtime_checkable
class AgentInterface(Protocol):
    """Protocol that all agent implementations must satisfy."""

    async def run(self, prompt: str, db_path: str) -> AgentTrace: ...


@dataclass(frozen=True)
class DimensionGrade:
    """Grade for a single rubric dimension."""

    name: str
    grade: str  # A, B, C, F
    score: float  # A=1.0, B=0.7, C=0.4, F=0.0
    weight: float
    justification: str


@dataclass(frozen=True)
class LevelResult:
    """Graded result for one evaluation level."""

    level: int
    name: str
    dimensions: list[DimensionGrade]
    weighted_score: float
    grade: str  # A, B, C, F


@dataclass(frozen=True)
class EvalResult:
    """Aggregate result across all evaluation levels."""

    levels: list[LevelResult]
    overall_score: float
    overall_grade: str  # A, B, C, F
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd backend && python -m pytest tests/unit/test_eval_types.py -v`
Expected: 6 passed

- [ ] **Step 5: Commit**

```bash
git add backend/app/evals/types.py backend/tests/unit/test_eval_types.py
git commit -m "feat: add core eval types — AgentTrace, AgentInterface, grade types"
```

---

### Task 3: Grading Logic

**Files:**
- Create: `backend/app/evals/grading.py`
- Create: `backend/tests/unit/test_eval_grading.py`

- [ ] **Step 1: Write failing tests for grading logic**

Create `backend/tests/unit/test_eval_grading.py`:

```python
from __future__ import annotations

from app.evals.grading import (
    calculate_weighted_score,
    grade_eval,
    grade_level,
    grade_to_score,
    score_to_grade,
)
from app.evals.types import DimensionGrade, EvalResult, LevelResult


def test_grade_to_score_all_grades() -> None:
    assert grade_to_score("A") == 1.0
    assert grade_to_score("B") == 0.7
    assert grade_to_score("C") == 0.4
    assert grade_to_score("F") == 0.0


def test_grade_to_score_invalid_raises() -> None:
    try:
        grade_to_score("X")
        assert False, "Should have raised"
    except KeyError:
        pass


def test_score_to_grade_thresholds() -> None:
    assert score_to_grade(1.0) == "A"
    assert score_to_grade(0.85) == "A"
    assert score_to_grade(0.84) == "B"
    assert score_to_grade(0.60) == "B"
    assert score_to_grade(0.59) == "C"
    assert score_to_grade(0.40) == "C"
    assert score_to_grade(0.39) == "F"
    assert score_to_grade(0.0) == "F"


def test_calculate_weighted_score() -> None:
    dims = [
        DimensionGrade(name="a", grade="A", score=1.0, weight=0.5, justification=""),
        DimensionGrade(name="b", grade="C", score=0.4, weight=0.5, justification=""),
    ]
    result = calculate_weighted_score(dims)
    assert result == 0.7  # (1.0*0.5 + 0.4*0.5)


def test_calculate_weighted_score_empty() -> None:
    assert calculate_weighted_score([]) == 0.0


def test_grade_level() -> None:
    dims = [
        DimensionGrade(name="x", grade="B", score=0.7, weight=0.6, justification=""),
        DimensionGrade(name="y", grade="A", score=1.0, weight=0.4, justification=""),
    ]
    result = grade_level(1, "Basic", dims)
    assert result.level == 1
    assert result.name == "Basic"
    assert result.weighted_score == 0.82  # 0.7*0.6 + 1.0*0.4
    assert result.grade == "B"  # 0.82 < 0.85


def test_grade_level_perfect() -> None:
    dims = [
        DimensionGrade(name="x", grade="A", score=1.0, weight=1.0, justification=""),
    ]
    result = grade_level(1, "Perfect", dims)
    assert result.grade == "A"


def test_grade_eval() -> None:
    levels = [
        LevelResult(level=1, name="L1", dimensions=[], weighted_score=0.9, grade="A"),
        LevelResult(level=2, name="L2", dimensions=[], weighted_score=0.7, grade="B"),
    ]
    result = grade_eval(levels)
    assert result.overall_score == 0.8  # (0.9 + 0.7) / 2
    assert result.overall_grade == "B"  # 0.80 < 0.85


def test_grade_eval_empty() -> None:
    result = grade_eval([])
    assert result.overall_score == 0.0
    assert result.overall_grade == "F"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd backend && python -m pytest tests/unit/test_eval_grading.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'app.evals.grading'`

- [ ] **Step 3: Implement grading logic**

Create `backend/app/evals/grading.py`:

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd backend && python -m pytest tests/unit/test_eval_grading.py -v`
Expected: 8 passed

- [ ] **Step 5: Commit**

```bash
git add backend/app/evals/grading.py backend/tests/unit/test_eval_grading.py
git commit -m "feat: add grading logic — score calculations and grade rollup"
```

---

### Task 4: Rubric Loader

**Files:**
- Create: `backend/app/evals/rubric.py`
- Create: `backend/tests/unit/test_eval_rubric.py`

- [ ] **Step 1: Write failing tests for rubric loading**

Create `backend/tests/unit/test_eval_rubric.py`:

```python
from __future__ import annotations

from pathlib import Path

from app.evals.rubric import DimensionRubric, RubricConfig, load_rubric


SAMPLE_RUBRIC_YAML = """\
level: 1
name: "Basic Rendering"
prompt: "Show me a chart."
dimensions:
  chart_correctness:
    weight: 0.5
    type: llm_judge
    criteria:
      A: "Perfect chart"
      B: "Good chart"
      C: "Okay chart"
  table_correctness:
    weight: 0.5
    type: hybrid
    deterministic:
      - "output contains 10 rows"
    criteria:
      A: "Perfect table"
      B: "Good table"
      C: "Okay table"
grading:
  A: 0.85
  B: 0.60
  C: 0.40
"""

SEQUENCE_RUBRIC_YAML = """\
level: 5
name: "Stress Test"
prompt_sequence:
  - "Step one"
  - "Step two"
  - "Step three"
dimensions:
  step_completion:
    weight: 1.0
    type: deterministic
    criteria:
      A: "All steps"
      B: "Most steps"
      C: "Some steps"
grading:
  A: 0.85
  B: 0.60
  C: 0.40
token_budget_optimal: 4000
"""


def test_load_rubric_basic(tmp_path: Path) -> None:
    rubric_file = tmp_path / "test.yaml"
    rubric_file.write_text(SAMPLE_RUBRIC_YAML)
    rubric = load_rubric(rubric_file)
    assert rubric.level == 1
    assert rubric.name == "Basic Rendering"
    assert rubric.prompt == "Show me a chart."
    assert len(rubric.dimensions) == 2


def test_load_rubric_dimension_types(tmp_path: Path) -> None:
    rubric_file = tmp_path / "test.yaml"
    rubric_file.write_text(SAMPLE_RUBRIC_YAML)
    rubric = load_rubric(rubric_file)
    chart = rubric.dimensions["chart_correctness"]
    assert chart.type == "llm_judge"
    assert chart.weight == 0.5
    assert chart.criteria["A"] == "Perfect chart"
    assert chart.deterministic == []


def test_load_rubric_hybrid_has_deterministic(tmp_path: Path) -> None:
    rubric_file = tmp_path / "test.yaml"
    rubric_file.write_text(SAMPLE_RUBRIC_YAML)
    rubric = load_rubric(rubric_file)
    table = rubric.dimensions["table_correctness"]
    assert table.type == "hybrid"
    assert table.deterministic == ["output contains 10 rows"]


def test_load_rubric_grading_thresholds(tmp_path: Path) -> None:
    rubric_file = tmp_path / "test.yaml"
    rubric_file.write_text(SAMPLE_RUBRIC_YAML)
    rubric = load_rubric(rubric_file)
    assert rubric.grading_thresholds == {"A": 0.85, "B": 0.60, "C": 0.40}


def test_load_rubric_prompt_sequence(tmp_path: Path) -> None:
    rubric_file = tmp_path / "test.yaml"
    rubric_file.write_text(SEQUENCE_RUBRIC_YAML)
    rubric = load_rubric(rubric_file)
    assert rubric.prompt == ""
    assert rubric.prompt_sequence == ["Step one", "Step two", "Step three"]
    assert rubric.token_budget_optimal == 4000


def test_load_rubric_no_token_budget(tmp_path: Path) -> None:
    rubric_file = tmp_path / "test.yaml"
    rubric_file.write_text(SAMPLE_RUBRIC_YAML)
    rubric = load_rubric(rubric_file)
    assert rubric.token_budget_optimal is None
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd backend && python -m pytest tests/unit/test_eval_rubric.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'app.evals.rubric'`

- [ ] **Step 3: Implement rubric loader**

Create `backend/app/evals/rubric.py`:

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd backend && python -m pytest tests/unit/test_eval_rubric.py -v`
Expected: 6 passed

- [ ] **Step 5: Commit**

```bash
git add backend/app/evals/rubric.py backend/tests/unit/test_eval_rubric.py
git commit -m "feat: add rubric YAML loader with dimension and threshold parsing"
```

---

### Task 5: LLM Judge

**Files:**
- Create: `backend/app/evals/judge.py`
- Create: `backend/tests/unit/test_eval_judge.py`

- [ ] **Step 1: Write failing tests for the LLM judge**

Create `backend/tests/unit/test_eval_judge.py`:

```python
from __future__ import annotations

import pytest

from app.evals.judge import JudgeConfig, LLMJudge
from app.evals.rubric import DimensionRubric
from app.evals.types import AgentTrace


def test_judge_config_defaults() -> None:
    config = JudgeConfig()
    assert config.model == "qwen3.5:9b"
    assert config.base_url == "http://localhost:11434"
    assert config.temperature == 0.0


def test_judge_build_prompt() -> None:
    judge = LLMJudge(config=JudgeConfig())
    rubric = DimensionRubric(
        weight=0.3,
        type="llm_judge",
        criteria={"A": "Excellent", "B": "Good", "C": "OK"},
    )
    trace = AgentTrace(
        queries=["SELECT 1"],
        intermediate=[],
        final_output="Here is my analysis.",
        token_count=100,
        duration_ms=500,
        errors=["minor warning"],
    )
    prompt = judge.build_prompt("chart_quality", rubric, trace)
    assert "chart_quality" in prompt
    assert "Here is my analysis." in prompt
    assert "SELECT 1" in prompt
    assert "Excellent" in prompt
    assert "minor warning" in prompt


def test_judge_parse_response_valid() -> None:
    judge = LLMJudge()
    grade, justification = judge.parse_response(
        "GRADE: B — Axes labeled and amounts accurate"
    )
    assert grade == "B"
    assert "Axes labeled" in justification


def test_judge_parse_response_multiline() -> None:
    judge = LLMJudge()
    grade, justification = judge.parse_response(
        "Some preamble text\nGRADE: A — Perfect output\nMore text"
    )
    assert grade == "A"
    assert "Perfect output" in justification


def test_judge_parse_response_invalid_falls_to_f() -> None:
    judge = LLMJudge()
    grade, justification = judge.parse_response("I don't know how to grade this")
    assert grade == "F"
    assert "Could not parse" in justification


def test_judge_parse_response_invalid_letter() -> None:
    judge = LLMJudge()
    grade, justification = judge.parse_response("GRADE: Z — Not a real grade")
    assert grade == "F"


@pytest.mark.asyncio
async def test_judge_grade_dimension_with_mocked_call(monkeypatch: pytest.MonkeyPatch) -> None:
    judge = LLMJudge()

    async def fake_call(self: LLMJudge, prompt: str) -> str:
        return "GRADE: B — Good work"

    monkeypatch.setattr(LLMJudge, "_call_ollama", fake_call)

    rubric = DimensionRubric(
        weight=0.3,
        type="llm_judge",
        criteria={"A": "Excellent", "B": "Good", "C": "OK"},
    )
    trace = AgentTrace(
        queries=[], intermediate=[], final_output="output",
        token_count=0, duration_ms=0, errors=[],
    )
    result = await judge.grade_dimension("test_dim", rubric, trace)
    assert result.grade == "B"
    assert result.score == 0.7
    assert result.weight == 0.3
    assert result.name == "test_dim"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd backend && python -m pytest tests/unit/test_eval_judge.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'app.evals.judge'`

- [ ] **Step 3: Implement the LLM judge**

Create `backend/app/evals/judge.py`:

```python
"""LLM judge for qualitative dimension grading via local Ollama."""

from __future__ import annotations

from dataclasses import dataclass

import httpx

from app.evals.grading import grade_to_score
from app.evals.rubric import DimensionRubric
from app.evals.types import AgentTrace, DimensionGrade


@dataclass(frozen=True)
class JudgeConfig:
    """Configuration for the LLM judge."""

    model: str = "qwen3.5:9b"
    base_url: str = "http://localhost:11434"
    temperature: float = 0.0


class LLMJudge:
    """Grades agent traces against rubric criteria using a local LLM."""

    def __init__(self, config: JudgeConfig | None = None) -> None:
        self._config = config or JudgeConfig()

    async def grade_dimension(
        self,
        dimension_name: str,
        rubric: DimensionRubric,
        trace: AgentTrace,
    ) -> DimensionGrade:
        """Grade a single dimension by calling the LLM judge."""
        prompt = self.build_prompt(dimension_name, rubric, trace)
        response = await self._call_ollama(prompt)
        grade, justification = self.parse_response(response)
        return DimensionGrade(
            name=dimension_name,
            grade=grade,
            score=grade_to_score(grade),
            weight=rubric.weight,
            justification=justification,
        )

    def build_prompt(
        self,
        dimension_name: str,
        rubric: DimensionRubric,
        trace: AgentTrace,
    ) -> str:
        """Build the grading prompt for the LLM."""
        errors_text = "\n".join(trace.errors) if trace.errors else "None"
        queries_text = "\n".join(trace.queries) if trace.queries else "None"
        return (
            f"You are grading an AI agent's performance on the dimension: "
            f"{dimension_name}\n\n"
            f"Agent's final output:\n{trace.final_output}\n\n"
            f"SQL queries executed:\n{queries_text}\n\n"
            f"Errors encountered:\n{errors_text}\n\n"
            f"Grading criteria:\n"
            f"- A (excellent): {rubric.criteria['A']}\n"
            f"- B (pretty useful): {rubric.criteria['B']}\n"
            f"- C (minimally ok): {rubric.criteria['C']}\n\n"
            f"Respond with exactly one line: "
            f"GRADE: <A|B|C|F> — <one-sentence justification>"
        )

    async def _call_ollama(self, prompt: str) -> str:
        """Call the Ollama generate API."""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self._config.base_url}/api/generate",
                json={
                    "model": self._config.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": self._config.temperature},
                },
                timeout=60.0,
            )
            resp.raise_for_status()
            return resp.json()["response"]

    def parse_response(self, response: str) -> tuple[str, str]:
        """Parse the judge's response into (grade, justification)."""
        for line in response.strip().splitlines():
            line = line.strip()
            if line.upper().startswith("GRADE:"):
                rest = line[6:].strip()
                parts = rest.split("—", 1)
                if not parts:
                    continue
                grade = parts[0].strip().upper()
                justification = parts[1].strip() if len(parts) > 1 else ""
                if grade in ("A", "B", "C", "F"):
                    return grade, justification
        return "F", "Could not parse judge response"
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd backend && python -m pytest tests/unit/test_eval_judge.py -v`
Expected: 7 passed

- [ ] **Step 5: Commit**

```bash
git add backend/app/evals/judge.py backend/tests/unit/test_eval_judge.py
git commit -m "feat: add LLM judge — Ollama wrapper for qualitative grading"
```

---

### Task 6: Eval Runner

**Files:**
- Create: `backend/app/evals/runner.py`
- Create: `backend/tests/unit/test_eval_runner.py`

- [ ] **Step 1: Write failing tests for the eval runner**

Create `backend/tests/unit/test_eval_runner.py`:

```python
from __future__ import annotations

import pytest

from app.evals.judge import LLMJudge
from app.evals.rubric import DimensionRubric, RubricConfig
from app.evals.runner import (
    evaluate_level,
    format_eval_result,
    format_level_result,
    grade_deterministic,
)
from app.evals.types import AgentTrace, DimensionGrade, EvalResult, LevelResult


def _make_trace(output: str = "test output") -> AgentTrace:
    return AgentTrace(
        queries=["SELECT 1"],
        intermediate=[],
        final_output=output,
        token_count=100,
        duration_ms=500,
        errors=[],
    )


def _make_rubric(dim_type: str = "llm_judge") -> RubricConfig:
    return RubricConfig(
        level=1,
        name="Test Level",
        prompt="Test prompt",
        prompt_sequence=[],
        dimensions={
            "quality": DimensionRubric(
                weight=1.0,
                type=dim_type,
                criteria={"A": "Great", "B": "Good", "C": "OK"},
            ),
        },
        grading_thresholds={"A": 0.85, "B": 0.60, "C": 0.40},
    )


def test_grade_deterministic_all_pass() -> None:
    trace = _make_trace("hello world")
    checks = [lambda t: "hello" in t.final_output, lambda t: "world" in t.final_output]
    result = grade_deterministic("dim", DimensionRubric(
        weight=0.5, type="deterministic", criteria={"A": "", "B": "", "C": ""},
    ), trace, checks)
    assert result.grade == "A"
    assert result.score == 1.0


def test_grade_deterministic_partial_pass() -> None:
    trace = _make_trace("hello")
    checks = [
        lambda t: "hello" in t.final_output,
        lambda t: "world" in t.final_output,
        lambda t: "foo" in t.final_output,
    ]
    result = grade_deterministic("dim", DimensionRubric(
        weight=0.5, type="deterministic", criteria={"A": "", "B": "", "C": ""},
    ), trace, checks)
    assert result.grade == "C"  # 1/3 = 0.33


def test_grade_deterministic_none_pass() -> None:
    trace = _make_trace("nothing matches")
    checks = [lambda t: "xyz" in t.final_output]
    result = grade_deterministic("dim", DimensionRubric(
        weight=0.5, type="deterministic", criteria={"A": "", "B": "", "C": ""},
    ), trace, checks)
    assert result.grade == "F"


def test_grade_deterministic_no_checks_defaults_c() -> None:
    trace = _make_trace()
    result = grade_deterministic("dim", DimensionRubric(
        weight=0.5, type="deterministic", criteria={"A": "", "B": "", "C": ""},
    ), trace, [])
    assert result.grade == "C"


class _FakeJudge:
    """Fake judge that always returns a fixed grade."""

    def __init__(self, grade: str = "B") -> None:
        self._grade = grade

    async def grade_dimension(
        self, name: str, rubric: DimensionRubric, trace: AgentTrace,
    ) -> DimensionGrade:
        from app.evals.grading import grade_to_score
        return DimensionGrade(
            name=name, grade=self._grade,
            score=grade_to_score(self._grade),
            weight=rubric.weight, justification="fake",
        )


@pytest.mark.asyncio
async def test_evaluate_level_llm_judge() -> None:
    rubric = _make_rubric("llm_judge")
    trace = _make_trace()
    result = await evaluate_level(rubric, trace, _FakeJudge("B"))  # type: ignore[arg-type]
    assert result.grade == "B"
    assert result.weighted_score == 0.7


@pytest.mark.asyncio
async def test_evaluate_level_hybrid_passes() -> None:
    rubric = RubricConfig(
        level=1, name="T", prompt="p", prompt_sequence=[],
        dimensions={"dim": DimensionRubric(
            weight=1.0, type="hybrid",
            criteria={"A": "", "B": "", "C": ""},
            deterministic=["has output"],
        )},
        grading_thresholds={"A": 0.85, "B": 0.60, "C": 0.40},
    )
    trace = _make_trace("has output here")
    checks = {"dim": [lambda t: "output" in t.final_output]}
    result = await evaluate_level(rubric, trace, _FakeJudge("A"), checks)  # type: ignore[arg-type]
    assert result.grade == "A"  # deterministic passed → use LLM grade


@pytest.mark.asyncio
async def test_evaluate_level_hybrid_fails_deterministic() -> None:
    rubric = RubricConfig(
        level=1, name="T", prompt="p", prompt_sequence=[],
        dimensions={"dim": DimensionRubric(
            weight=1.0, type="hybrid",
            criteria={"A": "", "B": "", "C": ""},
            deterministic=["must have xyz"],
        )},
        grading_thresholds={"A": 0.85, "B": 0.60, "C": 0.40},
    )
    trace = _make_trace("no match")
    checks = {"dim": [lambda t: "xyz" in t.final_output]}
    result = await evaluate_level(rubric, trace, _FakeJudge("A"), checks)  # type: ignore[arg-type]
    assert result.grade == "F"  # deterministic failed → F


def test_format_level_result() -> None:
    dims = [
        DimensionGrade(name="chart", grade="B", score=0.7, weight=0.5, justification=""),
        DimensionGrade(name="table", grade="A", score=1.0, weight=0.5, justification=""),
    ]
    result = LevelResult(level=1, name="Basic Rendering", dimensions=dims,
                         weighted_score=0.85, grade="A")
    text = format_level_result(result)
    assert "Level 1" in text
    assert "Basic Rendering" in text
    assert "chart:B" in text
    assert "table:A" in text


def test_format_eval_result() -> None:
    levels = [
        LevelResult(level=1, name="L1", dimensions=[], weighted_score=0.7, grade="B"),
        LevelResult(level=2, name="L2", dimensions=[], weighted_score=0.9, grade="A"),
    ]
    result = EvalResult(levels=levels, overall_score=0.8, overall_grade="B")
    text = format_eval_result(result)
    assert "Overall:" in text
    assert "B" in text
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd backend && python -m pytest tests/unit/test_eval_runner.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'app.evals.runner'`

- [ ] **Step 3: Implement the eval runner**

Create `backend/app/evals/runner.py`:

```python
"""Eval runner — evaluates agent traces against rubric configurations."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from app.evals.grading import grade_level, grade_to_score
from app.evals.types import AgentTrace, DimensionGrade, EvalResult, LevelResult

if TYPE_CHECKING:
    from app.evals.judge import LLMJudge
    from app.evals.rubric import DimensionRubric, RubricConfig

DeterministicCheck = Callable[[AgentTrace], bool]


def grade_deterministic(
    name: str,
    rubric: DimensionRubric,
    trace: AgentTrace,
    checks: list[DeterministicCheck],
) -> DimensionGrade:
    """Grade a purely deterministic dimension by check pass ratio."""
    if not checks:
        return DimensionGrade(
            name=name,
            grade="C",
            score=0.4,
            weight=rubric.weight,
            justification="No deterministic checks defined — default C",
        )
    passed = sum(1 for check in checks if check(trace))
    ratio = passed / len(checks)
    if ratio >= 0.9:
        grade_str, score = "A", 1.0
    elif ratio >= 0.6:
        grade_str, score = "B", 0.7
    elif ratio >= 0.3:
        grade_str, score = "C", 0.4
    else:
        grade_str, score = "F", 0.0
    return DimensionGrade(
        name=name,
        grade=grade_str,
        score=score,
        weight=rubric.weight,
        justification=f"Passed {passed}/{len(checks)} deterministic checks",
    )


async def evaluate_level(
    rubric: RubricConfig,
    trace: AgentTrace,
    judge: LLMJudge,
    deterministic_checks: dict[str, list[DeterministicCheck]] | None = None,
) -> LevelResult:
    """Run a full level evaluation against an agent trace.

    For 'llm_judge' dimensions: delegates to the LLM judge.
    For 'deterministic' dimensions: uses check functions (pass ratio → grade).
    For 'hybrid' dimensions: deterministic checks must all pass; then LLM grades.
      If deterministic checks fail → F.
    """
    checks = deterministic_checks or {}
    dimensions: list[DimensionGrade] = []

    for dim_name, dim_rubric in rubric.dimensions.items():
        if dim_rubric.type == "llm_judge":
            grade = await judge.grade_dimension(dim_name, dim_rubric, trace)
        elif dim_rubric.type == "deterministic":
            grade = grade_deterministic(
                dim_name, dim_rubric, trace, checks.get(dim_name, []),
            )
        else:  # hybrid
            dim_checks = checks.get(dim_name, [])
            all_pass = all(check(trace) for check in dim_checks) if dim_checks else True
            if not all_pass:
                grade = DimensionGrade(
                    name=dim_name,
                    grade="F",
                    score=0.0,
                    weight=dim_rubric.weight,
                    justification="Failed deterministic checks",
                )
            else:
                grade = await judge.grade_dimension(dim_name, dim_rubric, trace)
        dimensions.append(grade)

    return grade_level(rubric.level, rubric.name, dimensions)


def format_level_result(result: LevelResult) -> str:
    """Format a single level result for console output."""
    dims = "  ".join(f"{d.name}:{d.grade}" for d in result.dimensions)
    return (
        f"Level {result.level} — {result.name}:"
        f"{result.grade:>6}  ({dims})"
    )


def format_eval_result(result: EvalResult) -> str:
    """Format the full eval result for console output."""
    lines = [format_level_result(lev) for lev in result.levels]
    lines.append(f"Overall:{result.overall_grade:>25}")
    return "\n".join(lines)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd backend && python -m pytest tests/unit/test_eval_runner.py -v`
Expected: 10 passed

- [ ] **Step 5: Run all unit tests to check nothing is broken**

Run: `cd backend && python -m pytest tests/unit/ -v`
Expected: All tests pass (previous 18 + new 31 = 49 total)

- [ ] **Step 6: Commit**

```bash
git add backend/app/evals/runner.py backend/tests/unit/test_eval_runner.py
git commit -m "feat: add eval runner — evaluate_level with deterministic/hybrid/llm grading"
```

---

### Task 7: Seed Script — Deterministic Banking Dataset

**Files:**
- Create: `backend/scripts/seed_eval_data.py`
- Create: `backend/tests/unit/test_seed_eval.py`

- [ ] **Step 1: Write failing tests for the seed script**

Create `backend/tests/unit/test_seed_eval.py`:

```python
from __future__ import annotations

from pathlib import Path

import duckdb
import pytest


def test_seed_creates_all_tables(tmp_path: Path) -> None:
    from scripts.seed_eval_data import seed_all

    db_path = tmp_path / "eval.db"
    counts = seed_all(db_path)
    assert counts["customers"] == 200
    assert 380 <= counts["accounts"] <= 420
    assert 4900 <= counts["transactions"] <= 5100
    assert counts["loans"] == 80
    assert counts["daily_rates"] == 365


def test_seed_is_idempotent(tmp_path: Path) -> None:
    from scripts.seed_eval_data import seed_all

    db_path = tmp_path / "eval.db"
    counts1 = seed_all(db_path)
    counts2 = seed_all(db_path)
    assert counts1 == counts2


def test_anomalies_are_flagged(tmp_path: Path) -> None:
    from scripts.seed_eval_data import seed_all

    db_path = tmp_path / "eval.db"
    seed_all(db_path)
    con = duckdb.connect(str(db_path))
    flagged = con.execute(
        "SELECT COUNT(*) FROM transactions WHERE is_flagged"
    ).fetchone()
    con.close()
    assert flagged is not None
    # 1 (A1) + 12 (A2) + 4 (A3) + 1 (A4) + 1 (A5) + 8 (A6) = 27
    assert flagged[0] == 27


def test_anomalies_in_q3_2025(tmp_path: Path) -> None:
    from scripts.seed_eval_data import seed_all

    db_path = tmp_path / "eval.db"
    seed_all(db_path)
    con = duckdb.connect(str(db_path))
    result = con.execute("""
        SELECT COUNT(*) FROM transactions
        WHERE is_flagged
        AND txn_date >= '2025-07-01' AND txn_date < '2025-10-01'
    """).fetchone()
    con.close()
    assert result is not None
    assert result[0] == 27  # all anomalies in Q3


def test_credit_score_segment_correlation(tmp_path: Path) -> None:
    from scripts.seed_eval_data import seed_all

    db_path = tmp_path / "eval.db"
    seed_all(db_path)
    con = duckdb.connect(str(db_path))
    result = con.execute("""
        SELECT segment, AVG(credit_score) AS avg_score
        FROM customers
        GROUP BY segment
        ORDER BY avg_score
    """).fetchall()
    con.close()
    # retail < business < premium
    segments = [row[0] for row in result]
    assert segments.index("retail") < segments.index("premium")


def test_loan_rate_inversely_correlated_with_credit(tmp_path: Path) -> None:
    from scripts.seed_eval_data import seed_all

    db_path = tmp_path / "eval.db"
    seed_all(db_path)
    con = duckdb.connect(str(db_path))
    result = con.execute("""
        SELECT
            CASE WHEN c.credit_score < 700 THEN 'low' ELSE 'high' END AS bucket,
            AVG(l.interest_rate) AS avg_rate
        FROM loans l
        JOIN customers c ON l.customer_id = c.customer_id
        GROUP BY bucket
    """).fetchall()
    con.close()
    rates = {row[0]: row[1] for row in result}
    assert rates["low"] > rates["high"]


def test_daily_rates_has_two_cuts(tmp_path: Path) -> None:
    from scripts.seed_eval_data import seed_all

    db_path = tmp_path / "eval.db"
    seed_all(db_path)
    con = duckdb.connect(str(db_path))
    result = con.execute("""
        SELECT COUNT(DISTINCT fed_funds_rate)
        FROM daily_rates
    """).fetchone()
    con.close()
    assert result is not None
    assert result[0] == 3  # 5.25, 5.00, 4.75
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd backend && python -m pytest tests/unit/test_seed_eval.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'scripts.seed_eval_data'`

- [ ] **Step 3: Create the scripts package init**

Create `backend/scripts/__init__.py`:

```python
```

(Empty file — makes `scripts` importable as a package.)

- [ ] **Step 4: Implement the seed script**

Create `backend/scripts/seed_eval_data.py`:

```python
#!/usr/bin/env python3
"""Seed deterministic eval dataset into DuckDB.

Run: python -m scripts.seed_eval_data
Or:  make seed-eval
"""

from __future__ import annotations

import math
import random
from datetime import date, timedelta
from pathlib import Path

import duckdb
from faker import Faker

SEED = 42
DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "duckdb" / "eval.db"

fake = Faker()
Faker.seed(SEED)
random.seed(SEED)

SEGMENTS = ["retail", "business", "premium"]
SEGMENT_WEIGHTS = [0.5, 0.3, 0.2]
REGIONS = ["northeast", "southeast", "midwest", "west"]
ACCOUNT_TYPES = ["checking", "savings", "money_market"]
LOAN_TYPES = ["personal", "auto", "mortgage", "business"]
TXN_CATEGORIES = ["payroll", "utilities", "transfer", "merchant", "atm", "wire"]


def create_tables(con: duckdb.DuckDBPyConnection) -> None:
    """Drop and recreate all 5 eval tables."""
    for table in ("transactions", "loans", "accounts", "daily_rates", "customers"):
        con.execute(f"DROP TABLE IF EXISTS {table}")

    con.execute("""
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            name VARCHAR NOT NULL,
            segment VARCHAR NOT NULL,
            region VARCHAR NOT NULL,
            join_date DATE NOT NULL,
            credit_score INTEGER NOT NULL,
            is_active BOOLEAN NOT NULL
        )
    """)
    con.execute("""
        CREATE TABLE accounts (
            account_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            account_type VARCHAR NOT NULL,
            opened_date DATE NOT NULL,
            balance DECIMAL(12, 2) NOT NULL,
            status VARCHAR NOT NULL
        )
    """)
    con.execute("""
        CREATE TABLE transactions (
            txn_id INTEGER PRIMARY KEY,
            account_id INTEGER NOT NULL,
            txn_date DATE NOT NULL,
            amount DECIMAL(12, 2) NOT NULL,
            category VARCHAR NOT NULL,
            counterparty VARCHAR NOT NULL,
            description VARCHAR NOT NULL,
            is_flagged BOOLEAN NOT NULL DEFAULT FALSE
        )
    """)
    con.execute("""
        CREATE TABLE loans (
            loan_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            loan_type VARCHAR NOT NULL,
            principal DECIMAL(12, 2) NOT NULL,
            interest_rate DECIMAL(4, 2) NOT NULL,
            term_months INTEGER NOT NULL,
            origination_date DATE NOT NULL,
            status VARCHAR NOT NULL,
            monthly_payment DECIMAL(10, 2) NOT NULL
        )
    """)
    con.execute("""
        CREATE TABLE daily_rates (
            rate_date DATE PRIMARY KEY,
            fed_funds_rate DECIMAL(4, 2) NOT NULL,
            prime_rate DECIMAL(4, 2) NOT NULL,
            mortgage_30y DECIMAL(4, 2) NOT NULL,
            savings_apy DECIMAL(4, 2) NOT NULL
        )
    """)


def seed_customers(con: duckdb.DuckDBPyConnection) -> list[dict[str, object]]:
    """Generate 200 customers with segment-correlated credit scores."""
    base_scores = {"retail": 650, "business": 700, "premium": 750}
    customers: list[dict[str, object]] = []

    for i in range(1, 201):
        segment = random.choices(SEGMENTS, weights=SEGMENT_WEIGHTS, k=1)[0]
        credit_score = max(580, min(850, base_scores[segment] + random.randint(-70, 100)))
        join_date = date(2020, 1, 1) + timedelta(days=random.randint(0, 2190))
        is_active = random.random() < 0.9

        customer: dict[str, object] = {
            "customer_id": i,
            "name": fake.name(),
            "segment": segment,
            "region": random.choice(REGIONS),
            "join_date": join_date,
            "credit_score": credit_score,
            "is_active": is_active,
        }
        customers.append(customer)
        con.execute(
            "INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?)",
            [i, customer["name"], segment, customer["region"],
             join_date, credit_score, is_active],
        )
    return customers


def seed_accounts(
    con: duckdb.DuckDBPyConnection,
    customers: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Generate ~400 accounts linked to customers."""
    balance_ranges = {
        "retail": (500, 15_000),
        "business": (5_000, 100_000),
        "premium": (20_000, 500_000),
    }
    accounts: list[dict[str, object]] = []
    account_id = 1

    for cust in customers:
        num = random.choices([1, 2, 3], weights=[0.25, 0.50, 0.25], k=1)[0]
        for _ in range(num):
            acct_type = random.choice(ACCOUNT_TYPES)
            seg = str(cust["segment"])
            lo, hi = balance_ranges[seg]
            balance = round(random.uniform(lo, hi), 2)
            join = cust["join_date"]
            assert isinstance(join, date)
            opened = join + timedelta(days=random.randint(0, 365))
            status = random.choices(
                ["active", "dormant", "closed"],
                weights=[0.85, 0.10, 0.05],
                k=1,
            )[0]

            account: dict[str, object] = {
                "account_id": account_id,
                "customer_id": cust["customer_id"],
                "account_type": acct_type,
                "opened_date": opened,
                "balance": balance,
                "status": status,
            }
            accounts.append(account)
            con.execute(
                "INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?)",
                [account_id, cust["customer_id"], acct_type, opened, balance, status],
            )
            account_id += 1
    return accounts


def _plant_anomalies(
    con: duckdb.DuckDBPyConnection,
    accounts: list[dict[str, object]],
    start_txn_id: int,
) -> int:
    """Plant 6 anomaly groups (3 true + 3 false positive) in Q3 2025.

    Returns the next available txn_id.
    """
    txn_id = start_txn_id
    dormant = [a for a in accounts if a["status"] == "dormant"]
    active = [a for a in accounts if a["status"] == "active"]

    # A1: $47,000 wire from dormant account — stolen credentials
    a1_acct = dormant[0] if dormant else active[0]
    con.execute(
        "INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        [txn_id, a1_acct["account_id"], date(2025, 7, 14), -47_000.00,
         "wire", "Unknown Entity LLC", "Wire transfer — urgent request", True],
    )
    txn_id += 1

    # A2: 12 ATM withdrawals in 2 hours across 3 cities — card cloning
    a2_acct = active[0]
    cities = ["New York ATM #4412", "Chicago ATM #7891", "Miami ATM #2234"]
    for j in range(12):
        amt = round(random.uniform(200, 500), 2)
        con.execute(
            "INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [txn_id, a2_acct["account_id"], date(2025, 8, 3), -amt,
             "atm", cities[j % 3], f"ATM withdrawal #{j + 1}", True],
        )
        txn_id += 1

    # A3: Series of transfers to shell company — never seen before
    a3_acct = active[1]
    for j in range(4):
        amt = round(random.uniform(5_000, 15_000), 2)
        d = date(2025, 8, 10) + timedelta(days=j * 7)
        con.execute(
            "INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [txn_id, a3_acct["account_id"], d, -amt,
             "transfer", "Oceanic Holdings Ltd",
             f"Transfer to Oceanic Holdings — invoice {1000 + j}", True],
        )
        txn_id += 1

    # A4: $15,000 deposit — annual bonus (FALSE POSITIVE)
    a4_acct = active[2]
    con.execute(
        "INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        [txn_id, a4_acct["account_id"], date(2025, 7, 7), 15_000.00,
         "payroll", "Acme Corporation", "Annual Performance Bonus 2025", True],
    )
    txn_id += 1

    # A5: $50,000 savings→checking — house purchase (FALSE POSITIVE)
    a5_acct = active[3]
    con.execute(
        "INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        [txn_id, a5_acct["account_id"], date(2025, 8, 20), 50_000.00,
         "transfer", "Self — savings closure",
         "Transfer from savings — home purchase down payment", True],
    )
    txn_id += 1

    # A6: 8 small merchant charges on Saturday — shopping trip (FALSE POSITIVE)
    a6_acct = active[4]
    merchants = [
        "Target", "Whole Foods", "Home Depot", "Starbucks",
        "Best Buy", "CVS Pharmacy", "Trader Joe's", "Shell Gas",
    ]
    for j in range(8):
        amt = round(random.uniform(8, 120), 2)
        con.execute(
            "INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [txn_id, a6_acct["account_id"], date(2025, 9, 6), -amt,
             "merchant", merchants[j], f"Purchase at {merchants[j]}", True],
        )
        txn_id += 1

    return txn_id


def seed_transactions(
    con: duckdb.DuckDBPyConnection,
    accounts: list[dict[str, object]],
) -> None:
    """Generate ~5000 transactions for 2025 with planted anomalies."""
    txn_id = 1
    txn_id = _plant_anomalies(con, accounts, txn_id)

    active_accounts = [a for a in accounts if a["status"] != "closed"]
    target_normal = 5000 - (txn_id - 1)
    counterparties: dict[str, list[str]] = {
        "payroll": ["Acme Corp", "TechCo Inc", "Global Services LLC"],
        "utilities": ["City Electric", "Water Authority", "Internet Plus"],
        "transfer": ["Chase Bank", "Wells Fargo", "Internal Transfer"],
        "merchant": ["Amazon", "Walmart", "Target", "Costco", "Best Buy"],
        "atm": ["Bank ATM #101", "Bank ATM #202", "Partner ATM #303"],
        "wire": ["First National Wire", "International Wire Svc"],
    }
    cat_weights = [0.20, 0.15, 0.15, 0.30, 0.10, 0.10]

    for _ in range(target_normal):
        acct = random.choice(active_accounts)
        category = random.choices(TXN_CATEGORIES, weights=cat_weights, k=1)[0]
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        txn_date = date(2025, month, day)

        if category == "payroll":
            amount = round(random.uniform(2_000, 8_000), 2)
        elif category == "utilities":
            amount = -round(random.uniform(50, 300), 2)
        elif category == "transfer":
            amount = round(random.uniform(-5_000, 5_000), 2)
        elif category == "merchant":
            base = random.uniform(10, 500)
            if month in (11, 12):
                base *= 1.5  # holiday spending spike
            amount = -round(base, 2)
        elif category == "atm":
            amount = -round(random.uniform(20, 500), 2)
        else:  # wire
            amount = round(random.uniform(-10_000, 10_000), 2)

        cp = random.choice(counterparties[category])
        con.execute(
            "INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [txn_id, acct["account_id"], txn_date, amount,
             category, cp, f"{category.title()} — {cp}", False],
        )
        txn_id += 1


def seed_loans(
    con: duckdb.DuckDBPyConnection,
    customers: list[dict[str, object]],
) -> None:
    """Generate 80 loans with credit-score-correlated rates and default patterns."""
    loan_customers = random.sample(customers, 80)
    principal_ranges = {
        "personal": (5_000, 30_000),
        "auto": (10_000, 50_000),
        "mortgage": (100_000, 500_000),
        "business": (25_000, 200_000),
    }
    term_ranges = {
        "personal": (12, 60),
        "auto": (24, 72),
        "mortgage": (180, 360),
        "business": (12, 120),
    }
    region_risk = {"southeast": 1.5, "midwest": 1.2, "northeast": 1.0, "west": 0.8}

    for i, cust in enumerate(loan_customers):
        loan_type = random.choices(
            LOAN_TYPES, weights=[0.30, 0.25, 0.25, 0.20], k=1,
        )[0]
        lo, hi = principal_ranges[loan_type]
        principal = round(random.uniform(lo, hi), 2)

        score = int(cust["credit_score"])  # type: ignore[arg-type]
        base_rate = 18.0 - (score - 580) * (14.5 / 270)
        interest_rate = round(max(3.5, min(18.0, base_rate + random.uniform(-1, 1))), 2)

        term = random.randint(*term_ranges[loan_type])
        orig_date = date(2021, 1, 1) + timedelta(days=random.randint(0, 1460))

        monthly_rate = interest_rate / 100 / 12
        if monthly_rate > 0:
            payment = principal * monthly_rate / (1 - (1 + monthly_rate) ** -term)
        else:
            payment = principal / term
        monthly_payment = round(payment, 2)

        region = str(cust["region"])
        default_prob = max(0.02, 0.35 - (score - 580) * 0.001)
        default_prob *= region_risk.get(region, 1.0)
        roll = random.random()
        if roll < default_prob * 0.4:
            status = "default"
        elif roll < default_prob:
            status = "delinquent"
        elif roll < 0.85:
            status = "current"
        else:
            status = "paid_off"

        con.execute(
            "INSERT INTO loans VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [i + 1, cust["customer_id"], loan_type, principal,
             interest_rate, term, orig_date, status, monthly_payment],
        )


def seed_daily_rates(con: duckdb.DuckDBPyConnection) -> None:
    """Generate 365 daily rate records for 2025 with two fed rate cuts."""
    fed_rate = 5.25
    for day_offset in range(365):
        d = date(2025, 1, 1) + timedelta(days=day_offset)
        if d == date(2025, 6, 15):
            fed_rate = 5.00
        elif d == date(2025, 9, 15):
            fed_rate = 4.75
        prime = round(fed_rate + 3.0, 2)
        mortgage = round(prime + 0.5 + random.uniform(0, 1.0), 2)
        savings = round(4.0 + random.uniform(-0.5, 0.5), 2)
        con.execute(
            "INSERT INTO daily_rates VALUES (?, ?, ?, ?, ?)",
            [d, fed_rate, prime, mortgage, savings],
        )


def get_row_counts(con: duckdb.DuckDBPyConnection) -> dict[str, int]:
    """Return row counts for all eval tables."""
    tables = ["customers", "accounts", "transactions", "loans", "daily_rates"]
    counts: dict[str, int] = {}
    for table in tables:
        result = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
        counts[table] = result[0] if result else 0
    return counts


def seed_all(db_path: Path) -> dict[str, int]:
    """Seed all eval tables into the given database path. Returns row counts."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(db_path))
    try:
        create_tables(con)
        customers = seed_customers(con)
        accounts = seed_accounts(con, customers)
        seed_transactions(con, accounts)
        seed_loans(con, customers)
        seed_daily_rates(con)
        return get_row_counts(con)
    finally:
        con.close()


if __name__ == "__main__":
    counts = seed_all(DB_PATH)
    print("Eval dataset seeded successfully:")
    for table, count in counts.items():
        print(f"  {table}: {count} rows")
    con = duckdb.connect(str(DB_PATH))
    flagged = con.execute("SELECT COUNT(*) FROM transactions WHERE is_flagged").fetchone()
    con.close()
    print(f"  flagged anomalies: {flagged[0] if flagged else 0} transactions")
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd backend && python -m pytest tests/unit/test_seed_eval.py -v`
Expected: 7 passed

- [ ] **Step 6: Commit**

```bash
git add backend/scripts/__init__.py backend/scripts/seed_eval_data.py backend/tests/unit/test_seed_eval.py
git commit -m "feat: add deterministic eval seed script — 5 tables with planted anomalies"
```

---

### Task 8: Rubric YAML Files

**Files:**
- Create: `backend/tests/evals/rubrics/level1_rendering.yaml`
- Create: `backend/tests/evals/rubrics/level2_exploration.yaml`
- Create: `backend/tests/evals/rubrics/level3_anomaly.yaml`
- Create: `backend/tests/evals/rubrics/level4_free_explore.yaml`
- Create: `backend/tests/evals/rubrics/level5_stress.yaml`

- [ ] **Step 1: Create Level 1 rubric**

Create `backend/tests/evals/rubrics/level1_rendering.yaml`:

```yaml
level: 1
name: "Basic Rendering"
prompt: "Show me the monthly transaction volume and total amount for 2025 as a bar chart. Also show the top 10 customers by total deposits as a table. Finally, draw the relationship between the 5 tables as a mermaid ERD."
dimensions:
  chart_correctness:
    weight: 0.3
    type: llm_judge
    criteria:
      A: "Formatted amounts, clear title, color-coded volume vs amount"
      B: "Axes labeled, amounts accurate, months in order"
      C: "Bar chart renders with 12 months, values roughly correct"
  table_correctness:
    weight: 0.3
    type: hybrid
    deterministic:
      - "output contains exactly 10 customer rows"
      - "rows sorted descending by deposit amount"
    criteria:
      A: "Includes account types, percentage of total, clean alignment"
      B: "Correct ranking order, properly formatted currency"
      C: "Table with 10 rows, customer names and amounts present"
  mermaid_erd:
    weight: 0.2
    type: deterministic
    criteria:
      A: "Column names in entities, PK/FK marked, clean layout"
      B: "Correct FK relationships, correct cardinality notation"
      C: "Renders without syntax error, shows 5 tables"
  process_quality:
    weight: 0.2
    type: llm_judge
    criteria:
      A: "Efficient queries, no redundant calls"
      B: "Reasonable query design, not SELECT *"
      C: "Ran queries and produced output"
grading:
  A: 0.85
  B: 0.60
  C: 0.40
```

- [ ] **Step 2: Create Level 2 rubric**

Create `backend/tests/evals/rubrics/level2_exploration.yaml`:

```yaml
level: 2
name: "Multi-Step Exploration"
prompt: "Which customer segment has the highest loan default rate, and is that driven by credit score, loan type, or region? Walk me through your analysis."
dimensions:
  logical_chain:
    weight: 0.25
    type: llm_judge
    criteria:
      A: "Systematic elimination, explicitly rules out confounders"
      B: "4-5 steps in sensible order, considers multiple factors"
      C: "At least 3 steps, reaches a conclusion"
  correctness:
    weight: 0.30
    type: hybrid
    deterministic:
      - "identifies credit score as primary driver of loan default"
    criteria:
      A: "Quantifies effect size, notes interaction with loan type"
      B: "Correctly identifies credit score as primary driver"
      C: "Identifies the right segment with highest default rate"
  error_recovery:
    weight: 0.20
    type: llm_judge
    criteria:
      A: "Proactively validates intermediate results"
      B: "Notices and corrects analytical missteps"
      C: "Completes despite any query errors"
  communication:
    weight: 0.25
    type: llm_judge
    criteria:
      A: "Clear narrative arc, caveats noted, actionable summary"
      B: "Explains reasoning at each step"
      C: "States a conclusion"
grading:
  A: 0.85
  B: 0.60
  C: 0.40
```

- [ ] **Step 3: Create Level 3 rubric**

Create `backend/tests/evals/rubrics/level3_anomaly.yaml`:

```yaml
level: 3
name: "Anomaly Detection"
prompt: "Run anomaly detection on all transactions from Q3 2025. Flag statistical outliers, then manually review the raw data for each flag to identify false positives. Give me a final list of confirmed anomalies with your reasoning for each inclusion/exclusion."
dimensions:
  detection_recall:
    weight: 0.30
    type: deterministic
    criteria:
      A: "Flags all 3 true anomalies with correct anomaly type classification"
      B: "Flags all 3 true anomalies"
      C: "Flags at least 2 of 3 true anomalies"
  false_positive_handling:
    weight: 0.30
    type: hybrid
    deterministic:
      - "dismisses at least 2 of 3 false positives with reasoning"
    criteria:
      A: "Dismisses all 3 FPs with specific evidence: annual bonus pattern, house purchase, shopping trip"
      B: "Correctly dismisses at least 2 of 3 FPs with reasoning"
      C: "Acknowledges some flags might be benign"
  methodology:
    weight: 0.20
    type: llm_judge
    criteria:
      A: "Two-pass methodology explicit, documents thresholds, explains statistical method"
      B: "Statistical detection then inspects raw records"
      C: "Uses at least one statistical method"
  final_report:
    weight: 0.20
    type: llm_judge
    criteria:
      A: "Per-item reasoning, confidence levels, recommended actions"
      B: "Structured report with flag/dismiss decisions"
      C: "Lists anomalies"
grading:
  A: 0.85
  B: 0.60
  C: 0.40
```

- [ ] **Step 4: Create Level 4 rubric**

Create `backend/tests/evals/rubrics/level4_free_explore.yaml`:

```yaml
level: 4
name: "Free Exploration"
prompt: "Explore this banking dataset freely. Profile the data, find the most interesting correlations and causal relationships, and identify the strongest predictors of loan default. Surprise me with what you find."
dimensions:
  breadth:
    weight: 0.20
    type: llm_judge
    criteria:
      A: "Systematic profiling of all 5 tables, cross-table analysis"
      B: "Profiles 3+ tables, finds 3+ insights"
      C: "Profiles at least 2 tables, finds 1 insight"
  depth:
    weight: 0.25
    type: llm_judge
    criteria:
      A: "Distinguishes correlation from causation, controls for confounders"
      B: "Correlation analysis with quantified relationships"
      C: "Surface-level stats like means and counts"
  discovery_quality:
    weight: 0.30
    type: hybrid
    deterministic:
      - "identifies credit score as a predictor of loan default"
    criteria:
      A: "Finds planted relationships plus at least 1 non-obvious insight"
      B: "Finds 2-3 planted relationships"
      C: "Finds the obvious credit score to default relationship"
  presentation:
    weight: 0.25
    type: llm_judge
    criteria:
      A: "Narrative with visualizations, ranked by actionability"
      B: "Structured by importance with evidence"
      C: "Lists findings"
grading:
  A: 0.85
  B: 0.60
  C: 0.40
```

- [ ] **Step 5: Create Level 5 rubric**

Create `backend/tests/evals/rubrics/level5_stress.yaml`:

```yaml
level: 5
name: "Stress Test"
prompt_sequence:
  - "Summarize the loans table — count, average principal, default rate by loan_type"
  - "Edit the result: remove the 'auto' row and add a column for average credit score per loan type"
  - "Now summarize transactions — monthly total by category for Q4 2025 only"
  - "Edit: combine the 'atm' and 'merchant' categories into 'cash_and_retail'"
  - "Combine these two summary tables into one view — loan metrics alongside transaction metrics, joined by month where applicable"
  - "Calculate a new column: ratio of monthly transaction volume to outstanding loan principal per customer segment"
  - "Modify the combined table: filter to only segments where that ratio exceeds 0.5"
  - "Compare this final filtered table to the original loans summary from step 1 — what changed and what does it mean?"
dimensions:
  step_completion:
    weight: 0.25
    type: deterministic
    criteria:
      A: "All 8 steps with correct output at each stage"
      B: "Completes all 8 steps"
      C: "Completes at least 6 of 8 steps"
  state_correctness:
    weight: 0.30
    type: hybrid
    deterministic:
      - "references correct table versions, no stale data used"
    criteria:
      A: "Explicitly labels versions, e.g. loans_summary_v1"
      B: "All references correct, no stale data"
      C: "Mostly references correct table versions"
  efficiency:
    weight: 0.20
    type: deterministic
    criteria:
      A: "Within 1.2x optimal token budget, no redundant queries"
      B: "Within 1.5x optimal token budget"
      C: "Within 2x optimal token budget"
  final_comparison:
    weight: 0.25
    type: llm_judge
    criteria:
      A: "Explains why changes matter analytically"
      B: "Correctly identifies changes between step 1 and 8"
      C: "Produces some comparison"
grading:
  A: 0.85
  B: 0.60
  C: 0.40
token_budget_optimal: 4000
```

- [ ] **Step 6: Verify all rubrics load correctly**

Run:

```bash
cd backend && python -c "
from pathlib import Path
from app.evals.rubric import load_rubric
rubrics = Path('tests/evals/rubrics')
for f in sorted(rubrics.glob('*.yaml')):
    r = load_rubric(f)
    print(f'{f.name}: level={r.level} dims={len(r.dimensions)} ok')
"
```

Expected:

```
level1_rendering.yaml: level=1 dims=4 ok
level2_exploration.yaml: level=2 dims=4 ok
level3_anomaly.yaml: level=3 dims=4 ok
level4_free_explore.yaml: level=4 dims=4 ok
level5_stress.yaml: level=5 dims=4 ok
```

- [ ] **Step 7: Commit**

```bash
git add backend/tests/evals/rubrics/
git commit -m "feat: add rubric YAML files for all 5 eval levels"
```

---

### Task 9: Eval Conftest + Test Levels 1-2

**Files:**
- Create: `backend/tests/evals/conftest.py`
- Create: `backend/tests/evals/test_level1.py`
- Create: `backend/tests/evals/test_level2.py`

- [ ] **Step 1: Create the eval conftest with fixtures and mock agents**

Create `backend/tests/evals/conftest.py`:

```python
"""Shared fixtures for agent evaluation tests.

These tests run the full grading pipeline with a mock agent.
They require Ollama running locally for LLM-judged dimensions.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from app.evals.judge import LLMJudge
from app.evals.types import AgentTrace

RUBRICS_DIR = Path(__file__).parent / "rubrics"


@pytest.fixture
def rubrics_path() -> Path:
    """Path to the rubrics directory."""
    return RUBRICS_DIR


@pytest.fixture
def eval_db(tmp_path: Path) -> str:
    """Seed a fresh eval database and return its path."""
    from scripts.seed_eval_data import seed_all

    db_path = tmp_path / "eval.db"
    seed_all(db_path)
    return str(db_path)


@pytest.fixture
def llm_judge() -> LLMJudge:
    """LLM judge using default Ollama config."""
    return LLMJudge()


class MockAgent:
    """Returns a fixed trace for any prompt."""

    def __init__(self, trace: AgentTrace) -> None:
        self._trace = trace

    async def run(self, prompt: str, db_path: str) -> AgentTrace:
        return self._trace


class SequentialMockAgent:
    """Returns different traces for sequential calls (Level 5)."""

    def __init__(self, traces: list[AgentTrace]) -> None:
        self._traces = traces
        self._index = 0

    async def run(self, prompt: str, db_path: str) -> AgentTrace:
        trace = self._traces[min(self._index, len(self._traces) - 1)]
        self._index += 1
        return trace
```

- [ ] **Step 2: Create Level 1 eval test**

Create `backend/tests/evals/test_level1.py`:

```python
"""Level 1: Basic Rendering — chart, table, and mermaid ERD.

Requires Ollama running locally for LLM-judged dimensions.
Run: cd backend && python -m pytest tests/evals/test_level1.py -v -s
"""

from __future__ import annotations

from pathlib import Path

import pytest

from app.evals.judge import LLMJudge
from app.evals.rubric import load_rubric
from app.evals.runner import evaluate_level, format_level_result
from app.evals.types import AgentTrace

LEVEL1_RESPONSE = """\
## Monthly Transaction Volume and Amount — 2025

| Month | Volume | Total Amount |
|-------|--------|-------------|
| January | 425 | $1,234,567.89 |
| February | 398 | $1,189,234.56 |
| March | 445 | $1,345,678.90 |
| April | 410 | $1,267,890.12 |
| May | 432 | $1,298,456.78 |
| June | 418 | $1,256,789.01 |
| July | 467 | $1,456,789.23 |
| August | 455 | $1,423,456.78 |
| September | 440 | $1,378,901.23 |
| October | 430 | $1,312,345.67 |
| November | 458 | $1,445,678.90 |
| December | 472 | $1,512,345.67 |

[Bar chart rendered with labeled axes]

## Top 10 Customers by Total Deposits

| Rank | Customer | Total Deposits |
|------|----------|---------------|
| 1 | James Wilson | $234,567.89 |
| 2 | Sarah Johnson | $198,456.78 |
| 3 | Michael Chen | $187,234.56 |
| 4 | Emily Rodriguez | $176,890.12 |
| 5 | David Kim | $165,678.90 |
| 6 | Lisa Thompson | $154,321.09 |
| 7 | Robert Davis | $143,567.89 |
| 8 | Jennifer Martinez | $132,890.45 |
| 9 | William Brown | $121,456.78 |
| 10 | Amanda Taylor | $110,234.56 |

## Entity Relationship Diagram

```mermaid
erDiagram
    customers ||--o{ accounts : has
    customers ||--o{ loans : has
    accounts ||--o{ transactions : contains
    customers {
        int customer_id PK
        varchar name
        varchar segment
    }
    accounts {
        int account_id PK
        int customer_id FK
    }
    transactions {
        int txn_id PK
        int account_id FK
    }
    loans {
        int loan_id PK
        int customer_id FK
    }
    daily_rates {
        date rate_date PK
    }
```\
"""


@pytest.fixture
def level1_trace() -> AgentTrace:
    return AgentTrace(
        queries=[
            "SELECT DATE_TRUNC('month', txn_date) AS month, COUNT(*) AS volume, "
            "SUM(amount) AS total FROM transactions WHERE txn_date >= '2025-01-01' "
            "GROUP BY 1 ORDER BY 1",
            "SELECT c.name, SUM(t.amount) AS total_deposits FROM customers c "
            "JOIN accounts a ON c.customer_id = a.customer_id "
            "JOIN transactions t ON a.account_id = t.account_id "
            "WHERE t.amount > 0 GROUP BY c.name ORDER BY total_deposits DESC LIMIT 10",
            "SELECT table_name, column_name FROM information_schema.columns "
            "WHERE table_schema = 'main'",
        ],
        intermediate=[],
        final_output=LEVEL1_RESPONSE,
        token_count=800,
        duration_ms=5000,
        errors=[],
    )


@pytest.mark.asyncio
async def test_level1_grading(
    rubrics_path: Path,
    eval_db: str,
    llm_judge: LLMJudge,
    level1_trace: AgentTrace,
) -> None:
    """Verify Level 1 grading pipeline produces a non-F result."""
    rubric = load_rubric(rubrics_path / "level1_rendering.yaml")

    checks = {
        "table_correctness": [
            lambda t: t.final_output.count("$") >= 10,
            lambda t: "Top 10" in t.final_output,
        ],
        "mermaid_erd": [
            lambda t: "```mermaid" in t.final_output,
            lambda t: "erDiagram" in t.final_output,
            lambda t: all(
                name in t.final_output
                for name in [
                    "customers", "accounts", "transactions",
                    "loans", "daily_rates",
                ]
            ),
        ],
    }

    result = await evaluate_level(rubric, level1_trace, llm_judge, checks)
    print("\n" + format_level_result(result))
    for d in result.dimensions:
        print(f"  {d.name}: {d.grade} — {d.justification}")
    assert result.grade != "F", f"Level 1 failed: score={result.weighted_score:.2f}"
```

- [ ] **Step 3: Create Level 2 eval test**

Create `backend/tests/evals/test_level2.py`:

```python
"""Level 2: Multi-Step Exploration — analytical chaining and conclusions.

Requires Ollama running locally for LLM-judged dimensions.
Run: cd backend && python -m pytest tests/evals/test_level2.py -v -s
"""

from __future__ import annotations

from pathlib import Path

import pytest

from app.evals.judge import LLMJudge
from app.evals.rubric import load_rubric
from app.evals.runner import evaluate_level, format_level_result
from app.evals.types import AgentTrace

LEVEL2_RESPONSE = """\
## Analysis: Loan Default Rate by Customer Segment

### Step 1: Default Rate by Segment

| Segment | Total Loans | Defaults | Default Rate |
|---------|-------------|----------|-------------|
| retail | 38 | 8 | 21.1% |
| business | 25 | 4 | 16.0% |
| premium | 17 | 2 | 11.8% |

Retail has the highest default rate at 21.1%.

### Step 2: Credit Score Distribution by Segment

| Segment | Avg Credit Score | Min | Max |
|---------|-----------------|-----|-----|
| retail | 648 | 580 | 749 |
| business | 701 | 630 | 800 |
| premium | 752 | 680 | 850 |

Retail has significantly lower credit scores. This could explain defaults.

### Step 3: Default Rate by Credit Score Bucket

| Credit Bucket | Default Rate |
|---------------|-------------|
| 580-649 | 28.6% |
| 650-719 | 14.3% |
| 720-850 | 5.9% |

Strong inverse relationship: lower credit score = higher default rate.

### Step 4: Controlling for Credit Score — Default Rate by Region

| Region | Default Rate | Avg Credit Score |
|--------|-------------|-----------------|
| southeast | 22.7% | 680 |
| midwest | 16.7% | 695 |
| northeast | 13.3% | 710 |
| west | 10.5% | 715 |

Southeast has higher defaults even after accounting for credit scores.

### Step 5: Conclusion

**Credit score is the primary driver of loan default rate.** The default rate \
drops from 28.6% (score <650) to 5.9% (score >720). Retail customers default \
more because they have lower credit scores on average (648 vs 752 for premium), \
not because of their segment per se.

Region is a secondary factor — southeast shows elevated defaults even \
controlling for credit score, suggesting regional economic conditions play a role.

Loan type has minimal independent effect once credit score is controlled for.\
"""


@pytest.fixture
def level2_trace() -> AgentTrace:
    return AgentTrace(
        queries=[
            "SELECT c.segment, COUNT(*) AS total, "
            "SUM(CASE WHEN l.status = 'default' THEN 1 ELSE 0 END) AS defaults "
            "FROM loans l JOIN customers c ON l.customer_id = c.customer_id "
            "GROUP BY c.segment",
            "SELECT c.segment, AVG(c.credit_score), MIN(c.credit_score), "
            "MAX(c.credit_score) FROM customers c "
            "JOIN loans l ON c.customer_id = l.customer_id GROUP BY c.segment",
            "SELECT CASE WHEN credit_score < 650 THEN '580-649' "
            "WHEN credit_score < 720 THEN '650-719' ELSE '720-850' END AS bucket, "
            "AVG(CASE WHEN l.status = 'default' THEN 1.0 ELSE 0.0 END) AS rate "
            "FROM loans l JOIN customers c ON l.customer_id = c.customer_id "
            "GROUP BY bucket ORDER BY bucket",
            "SELECT c.region, AVG(CASE WHEN l.status = 'default' THEN 1.0 ELSE 0.0 END), "
            "AVG(c.credit_score) FROM loans l JOIN customers c "
            "ON l.customer_id = c.customer_id GROUP BY c.region ORDER BY 2 DESC",
        ],
        intermediate=[],
        final_output=LEVEL2_RESPONSE,
        token_count=600,
        duration_ms=8000,
        errors=[],
    )


@pytest.mark.asyncio
async def test_level2_grading(
    rubrics_path: Path,
    eval_db: str,
    llm_judge: LLMJudge,
    level2_trace: AgentTrace,
) -> None:
    """Verify Level 2 grading pipeline produces a non-F result."""
    rubric = load_rubric(rubrics_path / "level2_exploration.yaml")

    checks = {
        "correctness": [
            lambda t: "credit score" in t.final_output.lower()
            and "primary" in t.final_output.lower(),
        ],
    }

    result = await evaluate_level(rubric, level2_trace, llm_judge, checks)
    print("\n" + format_level_result(result))
    for d in result.dimensions:
        print(f"  {d.name}: {d.grade} — {d.justification}")
    assert result.grade != "F", f"Level 2 failed: score={result.weighted_score:.2f}"
```

- [ ] **Step 4: Run unit tests to verify nothing is broken**

Run: `cd backend && python -m pytest tests/unit/ -v`
Expected: All unit tests pass.

- [ ] **Step 5: Commit**

```bash
git add backend/tests/evals/conftest.py backend/tests/evals/test_level1.py backend/tests/evals/test_level2.py
git commit -m "feat: add eval conftest, mock agents, and test levels 1-2"
```

---

### Task 10: Test Levels 3-5 + Makefile Integration

**Files:**
- Create: `backend/tests/evals/test_level3.py`
- Create: `backend/tests/evals/test_level4.py`
- Create: `backend/tests/evals/test_level5.py`
- Modify: `Makefile`

- [ ] **Step 1: Create Level 3 eval test**

Create `backend/tests/evals/test_level3.py`:

```python
"""Level 3: Anomaly Detection + False Positive Screening.

Requires Ollama running locally for LLM-judged dimensions.
Run: cd backend && python -m pytest tests/evals/test_level3.py -v -s
"""

from __future__ import annotations

from pathlib import Path

import pytest

from app.evals.judge import LLMJudge
from app.evals.rubric import load_rubric
from app.evals.runner import evaluate_level, format_level_result
from app.evals.types import AgentTrace

LEVEL3_RESPONSE = """\
## Anomaly Detection Report — Q3 2025

### Methodology
Applied z-score analysis (threshold > 3.0) on transaction amounts per account, \
followed by frequency analysis for burst patterns. Then manually reviewed raw \
data for each flagged group.

### Flagged Anomaly Groups

#### A1: Large Wire Transfer — CONFIRMED ANOMALY
- Account status: dormant (no activity for months)
- Transaction: $47,000 wire to "Unknown Entity LLC" on 2025-07-14
- Risk: Dormant account suddenly executing a large wire transfer to an unknown \
entity is a strong indicator of compromised credentials.
- **Classification: TRUE ANOMALY — stolen credentials**

#### A2: ATM Withdrawal Burst — CONFIRMED ANOMALY
- 12 ATM withdrawals on 2025-08-03 totaling ~$4,200
- Locations: New York, Chicago, Miami (3 different cities)
- Timing: All within the same day — physically impossible
- **Classification: TRUE ANOMALY — card cloning**

#### A3: Shell Company Transfers — CONFIRMED ANOMALY
- 4 transfers to "Oceanic Holdings Ltd" between Aug 10 - Aug 31
- Total: ~$38,000
- This counterparty has no prior transaction history
- Regular weekly cadence suggests automated transfers
- **Classification: TRUE ANOMALY — suspicious new counterparty**

#### A4: $15,000 Deposit — DISMISSED (False Positive)
- Deposit from "Acme Corporation" labeled "Annual Performance Bonus 2025"
- Category: payroll — consistent with employer deposits
- Amount is within expected range for annual bonuses
- **Classification: FALSE POSITIVE — annual bonus deposit**

#### A5: $50,000 Transfer — DISMISSED (False Positive)
- Internal transfer labeled "Transfer from savings — home purchase down payment"
- Counterparty: "Self — savings closure"
- This is a customer moving their own money between accounts
- **Classification: FALSE POSITIVE — planned savings withdrawal for home purchase**

#### A6: Weekend Merchant Charges — DISMISSED (False Positive)
- 8 charges on 2025-09-06 (Saturday) totaling ~$480
- Merchants: Target, Whole Foods, Home Depot, Starbucks, Best Buy, CVS, \
Trader Joe's, Shell Gas
- All are common retail stores, small amounts ($8-$120)
- **Classification: FALSE POSITIVE — normal weekend shopping trip**

### Summary
| ID | Type | Decision | Confidence |
|----|------|----------|------------|
| A1 | Wire from dormant | CONFIRMED | High |
| A2 | ATM burst | CONFIRMED | High |
| A3 | Shell company | CONFIRMED | High |
| A4 | Large deposit | DISMISSED | High |
| A5 | Large transfer | DISMISSED | High |
| A6 | Weekend charges | DISMISSED | Medium |

**3 confirmed anomalies, 3 false positives dismissed.**

### Recommended Actions
1. A1: Freeze account, investigate credentials breach
2. A2: Block card, issue replacement, file fraud report
3. A3: Flag for compliance review, possible SAR filing\
"""


@pytest.fixture
def level3_trace() -> AgentTrace:
    return AgentTrace(
        queries=[
            "SELECT account_id, amount, txn_date, category, counterparty "
            "FROM transactions WHERE txn_date >= '2025-07-01' AND txn_date < '2025-10-01' "
            "ORDER BY ABS(amount) DESC LIMIT 50",
            "SELECT account_id, COUNT(*) AS cnt, SUM(amount) AS total "
            "FROM transactions WHERE txn_date >= '2025-07-01' AND txn_date < '2025-10-01' "
            "GROUP BY account_id HAVING COUNT(*) > 10",
            "SELECT t.*, a.status FROM transactions t "
            "JOIN accounts a ON t.account_id = a.account_id "
            "WHERE t.is_flagged ORDER BY t.txn_date",
            "SELECT counterparty, COUNT(*) FROM transactions "
            "WHERE txn_date < '2025-07-01' AND counterparty = 'Oceanic Holdings Ltd'",
        ],
        intermediate=[],
        final_output=LEVEL3_RESPONSE,
        token_count=1200,
        duration_ms=15000,
        errors=[],
    )


def _check_detects_true_anomalies(trace: AgentTrace) -> bool:
    output = trace.final_output.lower()
    return (
        "a1" in output and "confirmed" in output
        and "a2" in output
        and "a3" in output
    )


def _check_dismisses_false_positives(trace: AgentTrace) -> bool:
    output = trace.final_output.lower()
    return (
        "a4" in output and "false positive" in output
        and "a5" in output
        and "a6" in output and "dismissed" in output
    )


@pytest.mark.asyncio
async def test_level3_grading(
    rubrics_path: Path,
    eval_db: str,
    llm_judge: LLMJudge,
    level3_trace: AgentTrace,
) -> None:
    """Verify Level 3 grading pipeline produces a non-F result."""
    rubric = load_rubric(rubrics_path / "level3_anomaly.yaml")

    checks = {
        "detection_recall": [
            _check_detects_true_anomalies,
            lambda t: "wire" in t.final_output.lower(),
            lambda t: "atm" in t.final_output.lower(),
            lambda t: "oceanic" in t.final_output.lower(),
        ],
        "false_positive_handling": [
            _check_dismisses_false_positives,
            lambda t: "bonus" in t.final_output.lower(),
            lambda t: "shopping" in t.final_output.lower()
            or "weekend" in t.final_output.lower(),
        ],
    }

    result = await evaluate_level(rubric, level3_trace, llm_judge, checks)
    print("\n" + format_level_result(result))
    for d in result.dimensions:
        print(f"  {d.name}: {d.grade} — {d.justification}")
    assert result.grade != "F", f"Level 3 failed: score={result.weighted_score:.2f}"
```

- [ ] **Step 2: Create Level 4 eval test**

Create `backend/tests/evals/test_level4.py`:

```python
"""Level 4: Free Exploration for Insights.

Requires Ollama running locally for LLM-judged dimensions.
Run: cd backend && python -m pytest tests/evals/test_level4.py -v -s
"""

from __future__ import annotations

from pathlib import Path

import pytest

from app.evals.judge import LLMJudge
from app.evals.rubric import load_rubric
from app.evals.runner import evaluate_level, format_level_result
from app.evals.types import AgentTrace

LEVEL4_RESPONSE = """\
## Dataset Exploration — First National Bank

### Data Profile

| Table | Rows | Columns | Notes |
|-------|------|---------|-------|
| customers | 200 | 7 | 3 segments, 4 regions |
| accounts | ~400 | 6 | avg 2 per customer |
| transactions | ~5000 | 8 | 2025 full year |
| loans | 80 | 9 | 4 loan types |
| daily_rates | 365 | 5 | 2025 daily |

### Key Findings

#### 1. Credit Score → Loan Default (Strongest Predictor)
Customers with credit scores below 650 have a 28.6% default rate vs 5.9% for \
scores above 720. This is the single strongest predictor of loan default, \
explaining most of the segment-level variation.

Correlation coefficient: r = -0.72 (strong negative).

#### 2. Regional Delinquency Pattern
Default rates by region: southeast (22.7%) > midwest (16.7%) > northeast \
(13.3%) > west (10.5%). The southeast effect persists even after controlling \
for credit score, suggesting regional economic factors.

#### 3. Premium Customer Paradox
Premium customers have the lowest default rate (11.8%) but the highest average \
loan principal ($187K vs $23K for retail). Lower risk per loan but much higher \
exposure per default event.

#### 4. Seasonal Transaction Patterns
Holiday spending spike: November-December merchant transactions are 50% higher \
than the annual average. July shows a deposit spike from annual bonuses.

#### 5. Fed Rate Environment and Savings
The two fed rate cuts (June, September) correlate with a 12% increase in savings \
account balances in the following months. Customers appear to lock in higher APYs.

#### 6. Dormant Account Age Correlation
85% of dormant accounts belong to customers who joined before 2022. Older \
accounts are more likely to become dormant, suggesting customer lifecycle \
management opportunity.\
"""


@pytest.fixture
def level4_trace() -> AgentTrace:
    return AgentTrace(
        queries=[
            "SELECT table_name, COUNT(*) FROM information_schema.columns GROUP BY 1",
            "SELECT segment, COUNT(*), AVG(credit_score) FROM customers GROUP BY 1",
            "SELECT c.credit_score / 50 * 50 AS bucket, "
            "AVG(CASE WHEN l.status='default' THEN 1.0 ELSE 0.0 END) "
            "FROM loans l JOIN customers c ON l.customer_id=c.customer_id "
            "GROUP BY 1 ORDER BY 1",
            "SELECT c.region, AVG(CASE WHEN l.status='default' THEN 1.0 ELSE 0.0 END) "
            "FROM loans l JOIN customers c ON l.customer_id=c.customer_id GROUP BY 1",
            "SELECT c.segment, AVG(l.principal), "
            "AVG(CASE WHEN l.status='default' THEN 1.0 ELSE 0.0 END) "
            "FROM loans l JOIN customers c ON l.customer_id=c.customer_id GROUP BY 1",
            "SELECT EXTRACT(MONTH FROM txn_date) AS m, category, SUM(amount) "
            "FROM transactions GROUP BY 1,2 ORDER BY 1",
            "SELECT a.status, AVG(EXTRACT(YEAR FROM c.join_date)) "
            "FROM accounts a JOIN customers c ON a.customer_id=c.customer_id "
            "GROUP BY 1",
        ],
        intermediate=[],
        final_output=LEVEL4_RESPONSE,
        token_count=1500,
        duration_ms=20000,
        errors=[],
    )


@pytest.mark.asyncio
async def test_level4_grading(
    rubrics_path: Path,
    eval_db: str,
    llm_judge: LLMJudge,
    level4_trace: AgentTrace,
) -> None:
    """Verify Level 4 grading pipeline produces a non-F result."""
    rubric = load_rubric(rubrics_path / "level4_free_explore.yaml")

    checks = {
        "discovery_quality": [
            lambda t: "credit score" in t.final_output.lower()
            and "default" in t.final_output.lower(),
        ],
    }

    result = await evaluate_level(rubric, level4_trace, llm_judge, checks)
    print("\n" + format_level_result(result))
    for d in result.dimensions:
        print(f"  {d.name}: {d.grade} — {d.justification}")
    assert result.grade != "F", f"Level 4 failed: score={result.weighted_score:.2f}"
```

- [ ] **Step 3: Create Level 5 eval test**

Create `backend/tests/evals/test_level5.py`:

```python
"""Level 5: Stress Test — state tracking under compounding mutations.

Requires Ollama running locally for LLM-judged dimensions.
Run: cd backend && python -m pytest tests/evals/test_level5.py -v -s
"""

from __future__ import annotations

from pathlib import Path

import pytest

from app.evals.judge import LLMJudge
from app.evals.rubric import load_rubric
from app.evals.runner import evaluate_level, format_level_result
from app.evals.types import AgentTrace
from tests.evals.conftest import SequentialMockAgent

STEP_OUTPUTS = [
    # Step 1: loans summary
    "## Loans Summary\n| loan_type | count | avg_principal | default_rate |\n"
    "|-----------|-------|--------------|-------------|\n"
    "| personal | 24 | $17,500 | 20.8% |\n"
    "| auto | 20 | $30,000 | 15.0% |\n"
    "| mortgage | 20 | $300,000 | 10.0% |\n"
    "| business | 16 | $112,500 | 18.8% |",
    # Step 2: remove auto, add credit score
    "## Loans Summary v2 (auto removed, credit score added)\n"
    "| loan_type | count | avg_principal | default_rate | avg_credit_score |\n"
    "|-----------|-------|--------------|-------------|------------------|\n"
    "| personal | 24 | $17,500 | 20.8% | 665 |\n"
    "| mortgage | 20 | $300,000 | 10.0% | 738 |\n"
    "| business | 16 | $112,500 | 18.8% | 690 |",
    # Step 3: Q4 transactions by category
    "## Q4 2025 Transactions by Category\n| month | payroll | utilities | transfer "
    "| merchant | atm | wire |\n|-------|---------|-----------|----------|"
    "----------|-----|------|\n| Oct | $82K | -$12K | $5K | -$45K | -$8K | $15K |\n"
    "| Nov | $85K | -$13K | $7K | -$68K | -$9K | $12K |\n"
    "| Dec | $88K | -$14K | $3K | -$72K | -$10K | $18K |",
    # Step 4: combine atm+merchant
    "## Q4 2025 (atm+merchant → cash_and_retail)\n| month | payroll | utilities "
    "| transfer | cash_and_retail | wire |\n|-------|---------|-----------|"
    "----------|----------------|------|\n| Oct | $82K | -$12K | $5K | -$53K | $15K |\n"
    "| Nov | $85K | -$13K | $7K | -$77K | $12K |\n"
    "| Dec | $88K | -$14K | $3K | -$82K | $18K |",
    # Step 5: combined view
    "## Combined View — Loans + Q4 Transactions\n"
    "| loan_type | count | avg_principal | default_rate | avg_credit_score "
    "| oct_total | nov_total | dec_total |\n"
    "Joined on customer segment where applicable.",
    # Step 6: ratio calculation
    "## Transaction-to-Loan Ratio by Segment\n"
    "| segment | monthly_txn_volume | outstanding_principal | ratio |\n"
    "|---------|-------------------|-----------------------|-------|\n"
    "| retail | $45K | $420K | 0.107 |\n"
    "| business | $89K | $1.8M | 0.049 |\n"
    "| premium | $120K | $3.5M | 0.034 |",
    # Step 7: filter ratio > 0.5
    "## Filtered: Segments with ratio > 0.5\n\nNo segments exceed the 0.5 "
    "threshold. The highest ratio is retail at 0.107. This suggests loan "
    "principals significantly outweigh monthly transaction volumes across "
    "all segments.",
    # Step 8: comparison
    "## Comparison: Final vs Original (Step 1)\n\n"
    "**Changes from Step 1:**\n"
    "1. Auto loans removed — they represented 25% of loans\n"
    "2. Credit scores added — reveals mortgage holders have highest scores (738)\n"
    "3. Transaction context added — shows spending patterns alongside loan risk\n"
    "4. Ratio analysis shows all segments have low txn/principal ratios (<0.11)\n\n"
    "**Key Insight:** The filtering in step 7 revealed that no segment's monthly "
    "transaction volume is particularly high relative to outstanding loan principal. "
    "This means the bank's loan book is well-collateralized relative to transaction "
    "activity — a sign of conservative lending.",
]


@pytest.fixture
def level5_traces() -> list[AgentTrace]:
    return [
        AgentTrace(
            queries=[f"SELECT ... -- step {i + 1}"],
            intermediate=[],
            final_output=output,
            token_count=450,
            duration_ms=3000,
            errors=[],
        )
        for i, output in enumerate(STEP_OUTPUTS)
    ]


@pytest.mark.asyncio
async def test_level5_grading(
    rubrics_path: Path,
    eval_db: str,
    llm_judge: LLMJudge,
    level5_traces: list[AgentTrace],
) -> None:
    """Verify Level 5 grading pipeline handles sequential prompts."""
    rubric = load_rubric(rubrics_path / "level5_stress.yaml")

    mock = SequentialMockAgent(level5_traces)

    # Run all 8 prompts sequentially
    all_traces: list[AgentTrace] = []
    for prompt in rubric.prompt_sequence:
        trace = await mock.run(prompt, eval_db)
        all_traces.append(trace)

    # Combine into single trace for grading
    combined = AgentTrace(
        queries=[q for t in all_traces for q in t.queries],
        intermediate=[item for t in all_traces for item in t.intermediate],
        final_output=all_traces[-1].final_output,
        token_count=sum(t.token_count for t in all_traces),
        duration_ms=sum(t.duration_ms for t in all_traces),
        errors=[e for t in all_traces for e in t.errors],
    )

    optimal = rubric.token_budget_optimal or 4000
    total_tokens = combined.token_count

    checks = {
        "step_completion": [
            lambda t, _i=i: len(all_traces) > _i
            for i in range(8)
        ],
        "state_correctness": [
            lambda t: "v2" in t.final_output or "step 1" in t.final_output.lower(),
        ],
        "efficiency": [
            lambda t, _tt=total_tokens, _o=optimal: _tt <= _o * 2.0,
            lambda t, _tt=total_tokens, _o=optimal: _tt <= _o * 1.5,
            lambda t, _tt=total_tokens, _o=optimal: _tt <= _o * 1.2,
        ],
    }

    result = await evaluate_level(rubric, combined, llm_judge, checks)
    print("\n" + format_level_result(result))
    for d in result.dimensions:
        print(f"  {d.name}: {d.grade} — {d.justification}")
    print(f"  token_budget: {total_tokens}/{optimal} ({total_tokens/optimal:.1f}x)")
    assert result.grade != "F", f"Level 5 failed: score={result.weighted_score:.2f}"
```

- [ ] **Step 4: Update Makefile with eval targets**

Add the following targets to the Makefile. Insert after the `seed-data` target:

```makefile
# Eval framework
seed-eval:
	cd backend && python -m scripts.seed_eval_data

eval:
ifdef level
	cd backend && python -m pytest tests/evals/test_level$(level).py -v -s
else
	cd backend && python -m pytest tests/evals/ -v -s
endif
```

Also update the `.PHONY` line to include `seed-eval eval`.

- [ ] **Step 5: Run all unit tests to verify nothing is broken**

Run: `cd backend && python -m pytest tests/unit/ -v`
Expected: All unit tests pass.

- [ ] **Step 6: Run seed-eval to verify Makefile target works**

Run: `make seed-eval`
Expected:

```
Eval dataset seeded successfully:
  customers: 200 rows
  accounts: ~400 rows
  transactions: ~5000 rows
  loans: 80 rows
  daily_rates: 365 rows
  flagged anomalies: 27 transactions
```

- [ ] **Step 7: Commit**

```bash
git add backend/tests/evals/test_level3.py backend/tests/evals/test_level4.py backend/tests/evals/test_level5.py Makefile
git commit -m "feat: add eval test levels 3-5 and Makefile integration"
```

---

## Running the Eval Suite

After all tasks are complete:

```bash
# Seed the eval database
make seed-eval

# Run all 5 levels (requires Ollama running)
make eval

# Run a specific level
make eval level=3

# Run just unit tests (no Ollama needed)
cd backend && python -m pytest tests/unit/ -v
```

Expected output format:

```
Level 1 — Basic Rendering:      B  (chart_correctness:B  table_correctness:A  mermaid_erd:A  process_quality:C)
Level 2 — Multi-Step Explore:   A  (logical_chain:A  correctness:A  error_recovery:B  communication:A)
Level 3 — Anomaly Detection:    B  (detection_recall:A  false_positive_handling:B  methodology:B  final_report:C)
Level 4 — Free Exploration:     B  (breadth:B  depth:B  discovery_quality:A  presentation:C)
Level 5 — Stress Test:          C  (step_completion:B  state_correctness:C  efficiency:C  final_comparison:B)
Overall:                        B
```
