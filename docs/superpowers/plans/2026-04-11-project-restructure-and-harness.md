# Project Restructure & Harness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize claude-code-agent into a hybrid monorepo with clear backend/frontend/reference separation, scaffold the Python backend and React frontend, establish the project harness (docs, wiki, ADRs), and create the skills system foundation.

**Architecture:** Existing CLI source moves to `reference/`. New Python/FastAPI backend in `backend/`, new React+Vite frontend in `frontend/`. Infrastructure consolidates under `infra/`. Knowledge system (wiki + graphify + ADRs) lives in `knowledge/`. SOPs and guides in `docs/`.

**Tech Stack:** Python 3.12+, FastAPI, Pydantic, pytest / React 19, Vite, TypeScript, Zustand, vitest / DuckDB, Ollama, Docker Compose

**Spec:** `docs/superpowers/specs/2026-04-11-project-restructure-and-harness-design.md`

---

## File Map

### Files to move (git mv)

| Current | New |
|---------|-----|
| `src/` | `reference/src/` |
| `web/` | `reference/web/` |
| `mcp-server/` | `mcp/` |
| `ollama/` | `infra/ollama/` |
| `docker/` | `infra/docker/` |
| `helm/` | `infra/helm/` |
| `grafana/` | `infra/grafana/` |
| `docs/` | `reference/docs/` |
| `scripts/` | `reference/scripts/` |
| `tests/` | `reference/tests/` |
| `prompts/` | `reference/prompts/` |
| `agent.md` | `reference/agent.md` |
| `Skill.md` | `reference/Skill.md` |
| `README.md` | `reference/README.md` |
| `CONTRIBUTING.md` | `reference/CONTRIBUTING.md` |
| `graphify-out/` | `knowledge/graphs/` |
| `package.json` | `reference/package.json` |
| `package-lock.json` | `reference/package-lock.json` |
| `bun.lock` | `reference/bun.lock` |
| `biome.json` | `reference/biome.json` |
| `tsconfig.json` | `reference/tsconfig.json` |
| `bunfig.toml` | `reference/bunfig.toml` |
| `vitest.config.ts` | `reference/vitest.config.ts` |
| `drizzle.config.ts` | `reference/drizzle.config.ts` |
| `server.json` | `reference/server.json` |
| `renovate.json` | `reference/renovate.json` |
| `vercel.json` | `reference/vercel.json` |
| `.lighthouserc.json` | `reference/.lighthouserc.json` |
| `Dockerfile` | `infra/docker/Dockerfile.cli` |

### Files to create

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Rewritten project entry point |
| `Makefile` | Unified commands |
| `docker-compose.yml` | Local dev orchestration |
| `.env.example` | Updated env template |
| `README.md` | New project README |
| `reference/README.md` | Explains reference material |
| `backend/pyproject.toml` | Python project config |
| `backend/app/main.py` | FastAPI app factory |
| `backend/app/config.py` | Pydantic settings |
| `backend/app/api/health.py` | Health endpoint |
| `backend/app/skills/base.py` | SkillError, SkillResult, SkillContext |
| `backend/app/skills/registry.py` | Skill discovery |
| `backend/app/skills/manifest.py` | Dependency tracker |
| `backend/app/context/manager.py` | Context layer tracker |
| `backend/tests/conftest.py` | Pytest fixtures |
| `backend/tests/unit/test_config.py` | Config tests |
| `backend/tests/unit/test_health.py` | Health endpoint tests |
| `backend/tests/unit/test_skill_base.py` | SkillError tests |
| `backend/tests/unit/test_skill_registry.py` | Registry tests |
| `backend/tests/unit/test_context_manager.py` | Context manager tests |
| `frontend/package.json` | Frontend deps |
| `frontend/vite.config.ts` | Vite config |
| `frontend/tsconfig.json` | TypeScript config |
| `frontend/index.html` | Entry HTML |
| `frontend/src/main.tsx` | React entry |
| `frontend/src/App.tsx` | Root component |
| `frontend/src/panels/StatusBar.tsx` | Status bar |
| `frontend/src/devtools/DevToolsPanel.tsx` | Devtools container |
| `frontend/src/devtools/ContextInspector.tsx` | Context inspector |
| `frontend/src/lib/api.ts` | API client |
| `frontend/src/stores/devtools.ts` | Devtools state |
| `knowledge/wiki/index.md` | Wiki catalog |
| `knowledge/wiki/log.md` | Wiki changelog |
| `knowledge/wiki/working.md` | Current focus |
| `knowledge/adr/template.md` | ADR template |
| `knowledge/adr/000-initial-vision.md` | Vision from plans.md |
| `knowledge/adr/001-python-over-typescript.md` | Backend choice |
| `knowledge/adr/002-vite-over-nextjs.md` | Frontend choice |
| `docs/dev-setup.md` | Getting started |
| `docs/architecture.md` | System overview |
| `docs/testing.md` | Test guide |
| `docs/skill-creation.md` | Skill authoring guide |
| `docs/git-workflow.md` | Git conventions |
| `docs/gotchas.md` | Known issues |
| `scripts/dev.sh` | Start local dev |

---

## Task 1: Migrate existing files to reference/

**Files:**
- Move: all existing directories and root config files → `reference/`
- Move: `mcp-server/` → `mcp/`
- Move: infrastructure dirs → `infra/`
- Create: `reference/README.md`

- [ ] **Step 1: Create target directories**

```bash
mkdir -p reference infra
```

- [ ] **Step 2: Move CLI source and related files to reference/**

```bash
git mv src reference/src
git mv web reference/web
git mv tests reference/tests
git mv scripts reference/scripts
git mv prompts reference/prompts
git mv docs reference/docs
git mv agent.md reference/agent.md
git mv Skill.md reference/Skill.md
git mv README.md reference/README.md
git mv CONTRIBUTING.md reference/CONTRIBUTING.md
git mv package.json reference/package.json
git mv package-lock.json reference/package-lock.json
git mv bun.lock reference/bun.lock
git mv biome.json reference/biome.json
git mv tsconfig.json reference/tsconfig.json
git mv bunfig.toml reference/bunfig.toml
git mv vitest.config.ts reference/vitest.config.ts
git mv drizzle.config.ts reference/drizzle.config.ts
git mv server.json reference/server.json
git mv renovate.json reference/renovate.json
git mv vercel.json reference/vercel.json
git mv .lighthouserc.json reference/.lighthouserc.json
```

- [ ] **Step 3: Move infrastructure to infra/**

```bash
git mv docker infra/docker
git mv helm infra/helm
git mv grafana infra/grafana
git mv ollama infra/ollama
git mv Dockerfile infra/docker/Dockerfile.cli
git mv .dockerignore infra/docker/.dockerignore
```

- [ ] **Step 4: Rename mcp-server to mcp**

```bash
git mv mcp-server mcp
```

- [ ] **Step 5: Move graphify output to knowledge/**

```bash
mkdir -p knowledge/graphs
git mv graphify-out knowledge/graphs
```

Note: Also move any `src/*/graphify-out/` directories. These are untracked so use regular `mv`:

```bash
find reference/src -name "graphify-out" -type d -exec rm -rf {} + 2>/dev/null
```

- [ ] **Step 6: Move plans.md to knowledge/adr/**

```bash
mkdir -p knowledge/adr
git mv plans.md knowledge/adr/000-initial-vision.md
```

- [ ] **Step 7: Write reference/README.md**

Create `reference/README.md`:

```markdown
# Reference Material

This directory contains the original Claude Code CLI source code (published 2026-03-31) and related files. All contents are **read-only study material** — do not modify these files.

## What's here

| Directory | Contents |
|-----------|----------|
| `src/` | Original 512K-line TypeScript CLI source |
| `web/` | Original Next.js web frontend |
| `docs/` | CLI architecture documentation |
| `scripts/` | CLI build and deployment scripts |
| `tests/` | CLI test suite |
| `prompts/` | CLI prompt templates |

## How to use

Read these files to understand Claude Code's agent patterns:
- **Tool pattern:** `src/tools/{ToolName}/` — `buildTool()` factory
- **Skill system:** `src/skills/` — bundled workflows
- **Permission model:** `src/hooks/toolPermission/`
- **Query engine:** `src/QueryEngine.ts` — LLM streaming + tool loop

See the parent project's `docs/architecture.md` for how these patterns inform our design.
```

- [ ] **Step 8: Commit migration**

```bash
git add -A
git commit -m "refactor: migrate existing files to reference/ and infra/

Move CLI source, web frontend, and config files to reference/ (read-only).
Consolidate docker/helm/grafana/ollama under infra/.
Rename mcp-server/ to mcp/.
Move graphify output to knowledge/graphs/."
```

---

## Task 2: Backend scaffold — project config and app factory

**Files:**
- Create: `backend/pyproject.toml`
- Create: `backend/app/__init__.py`
- Create: `backend/app/main.py`
- Create: `backend/app/config.py`
- Create: `backend/app/api/__init__.py`
- Create: `backend/app/api/health.py`
- Test: `backend/tests/conftest.py`
- Test: `backend/tests/unit/test_config.py`
- Test: `backend/tests/unit/test_health.py`

- [ ] **Step 1: Create pyproject.toml**

Create `backend/pyproject.toml`:

```toml
[project]
name = "analytical-agent"
version = "0.1.0"
description = "Full-stack analytical platform for MLE, data scientists, and quants"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.34.0",
    "pydantic>=2.10.0",
    "pydantic-settings>=2.7.0",
    "duckdb>=1.2.0",
    "polars>=1.20.0",
    "httpx>=0.28.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.25.0",
    "pytest-cov>=6.0.0",
    "httpx>=0.28.0",
    "ruff>=0.9.0",
    "mypy>=1.14.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
pythonpath = ["."]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "A", "SIM"]

[tool.mypy]
python_version = "3.12"
strict = true
```

- [ ] **Step 2: Write the failing config test**

Create `backend/tests/__init__.py` (empty file).
Create `backend/tests/unit/__init__.py` (empty file).
Create `backend/tests/conftest.py`:

```python
import os

import pytest


@pytest.fixture(autouse=True)
def _test_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set minimal env vars for all tests."""
    monkeypatch.setenv("ENVIRONMENT", "test")
```

Create `backend/tests/unit/test_config.py`:

```python
from app.config import AppConfig, get_config


def test_config_loads_defaults() -> None:
    config = get_config()
    assert config.environment == "test"
    assert config.host == "127.0.0.1"
    assert config.port == 8000


def test_config_sandbox_defaults() -> None:
    config = get_config()
    assert config.sandbox_timeout_seconds == 30
    assert config.sandbox_max_memory_mb == 2048


def test_config_model_default() -> None:
    config = get_config()
    assert config.default_model == "qwen3.5:9b"
```

- [ ] **Step 3: Run test to verify it fails**

```bash
cd backend && pip install -e ".[dev]" && pytest tests/unit/test_config.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'app'`

- [ ] **Step 4: Write config implementation**

Create `backend/app/__init__.py` (empty file).
Create `backend/app/config.py`:

```python
from functools import lru_cache

from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    """Application configuration loaded from environment variables."""

    environment: str = "development"
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = False

    # Model
    default_model: str = "qwen3.5:9b"
    ollama_base_url: str = "http://localhost:11434"
    litellm_base_url: str = "http://localhost:4000"

    # Sandbox
    sandbox_timeout_seconds: int = 30
    sandbox_max_memory_mb: int = 2048
    sandbox_state_root: str = "./data/sandbox_sessions"

    # DuckDB
    duckdb_path: str = "./data/duckdb/analytical.db"

    # Wiki
    wiki_root: str = "../knowledge/wiki"
    wiki_auto_write: bool = True

    # Context window
    context_max_tokens: int = 32768
    context_compaction_threshold: float = 0.80

    model_config = {"env_prefix": "", "env_file": "../.env", "extra": "ignore"}


@lru_cache
def get_config() -> AppConfig:
    return AppConfig()
```

- [ ] **Step 5: Run config tests**

```bash
cd backend && pytest tests/unit/test_config.py -v
```

Expected: PASS (3 tests)

- [ ] **Step 6: Write the failing health endpoint test**

Create `backend/app/api/__init__.py` (empty file).
Create `backend/tests/unit/test_health.py`:

```python
from fastapi.testclient import TestClient

from app.main import create_app


def test_health_returns_ok() -> None:
    app = create_app()
    client = TestClient(app)
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"


def test_health_includes_version() -> None:
    app = create_app()
    client = TestClient(app)
    response = client.get("/api/health")
    body = response.json()
    assert "version" in body
```

- [ ] **Step 7: Run test to verify it fails**

```bash
cd backend && pytest tests/unit/test_health.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'app.main'`

- [ ] **Step 8: Write app factory and health endpoint**

Create `backend/app/api/health.py`:

```python
from fastapi import APIRouter

router = APIRouter()


@router.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "version": "0.1.0"}
```

Create `backend/app/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Analytical Agent",
        version="0.1.0",
        description="Full-stack analytical platform for MLE, data scientists, and quants",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)

    return app
```

- [ ] **Step 9: Run tests**

```bash
cd backend && pytest tests/unit/test_config.py tests/unit/test_health.py -v
```

Expected: PASS (5 tests)

- [ ] **Step 10: Commit**

```bash
git add backend/
git commit -m "feat: scaffold backend with FastAPI app factory, config, and health endpoint"
```

---

## Task 3: Skills system foundation — base types

**Files:**
- Create: `backend/app/skills/__init__.py`
- Create: `backend/app/skills/base.py`
- Test: `backend/tests/unit/test_skill_base.py`

- [ ] **Step 1: Write the failing SkillError test**

Create `backend/app/skills/__init__.py` (empty file).
Create `backend/tests/unit/test_skill_base.py`:

```python
from app.skills.base import SkillError, SkillResult


def test_skill_error_formats_message() -> None:
    error_templates = {
        "COLUMN_NOT_FOUND": {
            "message": "Column '{column}' not found in table '{table}'",
            "guidance": "Available columns: {available_columns}. Did you mean: {suggestions}?",
            "recovery": "Fix the column name and retry",
        }
    }
    err = SkillError(
        code="COLUMN_NOT_FOUND",
        context={
            "column": "price",
            "table": "sales",
            "available_columns": ["date", "revenue"],
            "suggestions": ["price_usd"],
        },
        templates=error_templates,
    )
    formatted = err.format()
    assert "Column 'price' not found in table 'sales'" in formatted
    assert "Available columns: ['date', 'revenue']" in formatted
    assert "Did you mean: ['price_usd']" in formatted
    assert "Fix the column name and retry" in formatted


def test_skill_error_without_template_falls_back() -> None:
    err = SkillError(
        code="UNKNOWN_ERROR",
        context={"detail": "something broke"},
        templates={},
    )
    formatted = err.format()
    assert "UNKNOWN_ERROR" in formatted
    assert "something broke" in formatted


def test_skill_result_with_data() -> None:
    result = SkillResult(data={"rows": 10, "columns": ["a", "b"]})
    assert result.data["rows"] == 10
    assert result.artifacts == []
    assert result.events == []


def test_skill_result_with_artifacts() -> None:
    result = SkillResult(
        data=None,
        artifacts=[{"type": "chart", "title": "My Chart", "spec": {}}],
    )
    assert len(result.artifacts) == 1
    assert result.artifacts[0]["type"] == "chart"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd backend && pytest tests/unit/test_skill_base.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'app.skills.base'`

- [ ] **Step 3: Write SkillError and SkillResult**

Create `backend/app/skills/base.py`:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class SkillError(Exception):
    """Actionable error with template-based formatting.

    Every error code maps to a template in skill.yaml with message,
    guidance, and recovery fields. Context values fill the placeholders.
    """

    def __init__(
        self,
        code: str,
        context: dict[str, Any],
        templates: dict[str, dict[str, str]] | None = None,
    ) -> None:
        self.code = code
        self.context = context
        self.templates = templates or {}
        super().__init__(self.format())

    def format(self) -> str:
        template = self.templates.get(self.code)
        if template is None:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            return f"{self.code}: {context_str}"

        parts: list[str] = []
        for key in ("message", "guidance", "recovery"):
            raw = template.get(key, "")
            if raw:
                try:
                    parts.append(raw.format(**self.context))
                except KeyError:
                    parts.append(raw)
        return "\n".join(parts)


@dataclass(frozen=True)
class SkillResult:
    """Return type for all skill function executions."""

    data: Any = None
    artifacts: list[dict[str, Any]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class SkillMetadata:
    """Parsed metadata from skill.yaml."""

    name: str
    version: str
    description: str
    level: int
    dependencies_requires: list[str] = field(default_factory=list)
    dependencies_used_by: list[str] = field(default_factory=list)
    dependencies_packages: list[str] = field(default_factory=list)
    error_templates: dict[str, dict[str, str]] = field(default_factory=dict)
```

- [ ] **Step 4: Run tests**

```bash
cd backend && pytest tests/unit/test_skill_base.py -v
```

Expected: PASS (4 tests)

- [ ] **Step 5: Commit**

```bash
git add backend/app/skills/ backend/tests/unit/test_skill_base.py
git commit -m "feat: add SkillError, SkillResult, and SkillMetadata base types"
```

---

## Task 4: Skills system — registry and manifest

**Files:**
- Create: `backend/app/skills/registry.py`
- Create: `backend/app/skills/manifest.py`
- Test: `backend/tests/unit/test_skill_registry.py`

- [ ] **Step 1: Write the failing registry test**

Create `backend/tests/unit/test_skill_registry.py`:

```python
from pathlib import Path

from app.skills.registry import SkillRegistry


def test_registry_discovers_skills(tmp_path: Path) -> None:
    skill_dir = tmp_path / "test_skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: test_skill\n---\n# Test Skill\n")
    (skill_dir / "skill.yaml").write_text(
        "name: test_skill\nversion: '1.0'\ndescription: A test\nlevel: 1\n"
        "errors: {}\ndependencies:\n  requires: []\n  used_by: []\n  packages: []\n"
    )
    (skill_dir / "pkg").mkdir()
    (skill_dir / "pkg" / "__init__.py").write_text("")

    registry = SkillRegistry(skills_root=tmp_path)
    registry.discover()
    assert "test_skill" in registry.list_skills()


def test_registry_loads_skill_instructions(tmp_path: Path) -> None:
    skill_dir = tmp_path / "eda"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: eda\n---\n# EDA\nExploratory analysis.\n")
    (skill_dir / "skill.yaml").write_text(
        "name: eda\nversion: '1.0'\ndescription: EDA\nlevel: 1\n"
        "errors: {}\ndependencies:\n  requires: []\n  used_by: []\n  packages: []\n"
    )
    (skill_dir / "pkg").mkdir()
    (skill_dir / "pkg" / "__init__.py").write_text("")

    registry = SkillRegistry(skills_root=tmp_path)
    registry.discover()
    instructions = registry.get_instructions("eda")
    assert "Exploratory analysis" in instructions


def test_registry_excludes_evals(tmp_path: Path) -> None:
    skill_dir = tmp_path / "query_data"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: query_data\n---\n# Query\n")
    (skill_dir / "skill.yaml").write_text(
        "name: query_data\nversion: '1.0'\ndescription: Query\nlevel: 1\n"
        "errors: {}\ndependencies:\n  requires: []\n  used_by: []\n  packages: []\n"
    )
    (skill_dir / "pkg").mkdir()
    (skill_dir / "pkg" / "__init__.py").write_text("")
    evals_dir = skill_dir / "evals"
    evals_dir.mkdir()
    (evals_dir / "eval.yaml").write_text("cases: []")

    registry = SkillRegistry(skills_root=tmp_path)
    registry.discover()
    skill = registry.get_skill("query_data")
    assert skill is not None
    assert skill.evals_path is None  # evals are excluded from loaded skill


def test_registry_returns_none_for_unknown_skill(tmp_path: Path) -> None:
    registry = SkillRegistry(skills_root=tmp_path)
    registry.discover()
    assert registry.get_skill("nonexistent") is None
    assert registry.get_instructions("nonexistent") is None
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd backend && pytest tests/unit/test_skill_registry.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'app.skills.registry'`

- [ ] **Step 3: Write registry implementation**

Create `backend/app/skills/registry.py`:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from app.skills.base import SkillMetadata


@dataclass
class LoadedSkill:
    """A discovered and loaded skill (evals excluded)."""

    metadata: SkillMetadata
    instructions: str
    package_path: Path
    references_path: Path | None
    evals_path: None = None  # deliberately excluded — never exposed to agent


class SkillRegistry:
    """Discovers and loads skills from a directory tree."""

    def __init__(self, skills_root: Path) -> None:
        self._root = skills_root
        self._skills: dict[str, LoadedSkill] = {}

    def discover(self) -> None:
        """Scan skills_root for valid skill directories and load them."""
        self._skills.clear()
        if not self._root.exists():
            return

        for skill_dir in sorted(self._root.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_yaml = skill_dir / "skill.yaml"
            skill_md = skill_dir / "SKILL.md"
            if not skill_yaml.exists() or not skill_md.exists():
                continue

            raw = yaml.safe_load(skill_yaml.read_text())
            deps = raw.get("dependencies", {})
            metadata = SkillMetadata(
                name=raw["name"],
                version=raw.get("version", "0.0"),
                description=raw.get("description", ""),
                level=raw.get("level", 1),
                dependencies_requires=deps.get("requires", []),
                dependencies_used_by=deps.get("used_by", []),
                dependencies_packages=deps.get("packages", []),
                error_templates=raw.get("errors", {}),
            )

            instructions = skill_md.read_text()
            pkg_path = skill_dir / "pkg"
            refs_path = skill_dir / "references"

            self._skills[metadata.name] = LoadedSkill(
                metadata=metadata,
                instructions=instructions,
                package_path=pkg_path,
                references_path=refs_path if refs_path.exists() else None,
                # evals_path deliberately not set — sealed from agent
            )

    def list_skills(self) -> list[str]:
        return list(self._skills.keys())

    def get_skill(self, name: str) -> LoadedSkill | None:
        return self._skills.get(name)

    def get_instructions(self, name: str) -> str | None:
        skill = self._skills.get(name)
        return skill.instructions if skill else None

    def get_dependency_graph(self) -> dict[str, list[str]]:
        """Return {skill_name: [required_skills]} mapping."""
        return {
            name: skill.metadata.dependencies_requires
            for name, skill in self._skills.items()
        }
```

- [ ] **Step 4: Run tests**

```bash
cd backend && pip install pyyaml && pytest tests/unit/test_skill_registry.py -v
```

Expected: PASS (4 tests)

Note: Add `pyyaml>=6.0` to `backend/pyproject.toml` dependencies.

- [ ] **Step 5: Update pyproject.toml with pyyaml**

Edit `backend/pyproject.toml`, add to dependencies:

```toml
    "pyyaml>=6.0",
```

- [ ] **Step 6: Write manifest stub**

Create `backend/app/skills/manifest.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.skills.registry import SkillRegistry


@dataclass(frozen=True)
class ManifestIssue:
    """A detected breaking change or inconsistency."""

    skill: str
    severity: str  # "breaking", "warning", "info"
    message: str
    affected: list[str]


class SkillManifest:
    """Tracks skill dependency graph and detects breaking changes."""

    def __init__(self, registry: SkillRegistry) -> None:
        self._registry = registry

    def check(self) -> list[ManifestIssue]:
        """Check for dependency issues. Returns list of issues found."""
        issues: list[ManifestIssue] = []
        graph = self._registry.get_dependency_graph()
        all_skills = set(self._registry.list_skills())

        for skill_name, requires in graph.items():
            for dep in requires:
                if dep not in all_skills:
                    issues.append(
                        ManifestIssue(
                            skill=skill_name,
                            severity="breaking",
                            message=f"Required skill '{dep}' not found",
                            affected=[skill_name],
                        )
                    )
        return issues
```

- [ ] **Step 7: Commit**

```bash
git add backend/app/skills/ backend/tests/unit/test_skill_registry.py backend/pyproject.toml
git commit -m "feat: add skill registry with discovery, loading, and manifest checking"
```

---

## Task 5: Context manager — layer tracking

**Files:**
- Create: `backend/app/context/__init__.py`
- Create: `backend/app/context/manager.py`
- Test: `backend/tests/unit/test_context_manager.py`

- [ ] **Step 1: Write the failing context manager test**

Create `backend/app/context/__init__.py` (empty file).
Create `backend/tests/unit/test_context_manager.py`:

```python
from app.context.manager import ContextLayer, ContextManager


def test_add_layer() -> None:
    mgr = ContextManager(max_tokens=32768)
    mgr.add_layer(ContextLayer(
        name="system",
        tokens=1640,
        compactable=False,
        items=[{"name": "system_prompt", "tokens": 1640}],
    ))
    assert mgr.total_tokens == 1640
    assert mgr.utilization < 0.1


def test_utilization_calculation() -> None:
    mgr = ContextManager(max_tokens=10000)
    mgr.add_layer(ContextLayer(name="system", tokens=5000, compactable=False, items=[]))
    assert mgr.utilization == 0.5


def test_snapshot_returns_all_layers() -> None:
    mgr = ContextManager(max_tokens=32768)
    mgr.add_layer(ContextLayer(name="system", tokens=1640, compactable=False, items=[]))
    mgr.add_layer(ContextLayer(name="l1_always", tokens=1600, compactable=False, items=[]))
    mgr.add_layer(ContextLayer(name="conversation", tokens=3000, compactable=True, items=[]))
    snapshot = mgr.snapshot()
    assert snapshot["total_tokens"] == 6240
    assert len(snapshot["layers"]) == 3
    assert snapshot["max_tokens"] == 32768


def test_compaction_needed() -> None:
    mgr = ContextManager(max_tokens=10000, compaction_threshold=0.8)
    mgr.add_layer(ContextLayer(name="system", tokens=2000, compactable=False, items=[]))
    assert not mgr.compaction_needed
    mgr.add_layer(ContextLayer(name="conversation", tokens=7000, compactable=True, items=[]))
    assert mgr.compaction_needed


def test_compaction_history() -> None:
    mgr = ContextManager(max_tokens=10000, compaction_threshold=0.8)
    mgr.record_compaction(
        tokens_before=8500,
        tokens_after=4200,
        removed=[{"name": "old_ref.md", "tokens": 1200}],
        survived=["system", "l1_always"],
    )
    history = mgr.compaction_history
    assert len(history) == 1
    assert history[0]["tokens_freed"] == 4300
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd backend && pytest tests/unit/test_context_manager.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'app.context.manager'`

- [ ] **Step 3: Write ContextManager**

Create `backend/app/context/manager.py`:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class ContextLayer:
    """A named layer in the context window."""

    name: str
    tokens: int
    compactable: bool
    items: list[dict[str, Any]]


class ContextManager:
    """Tracks context window composition across layers.

    Provides live snapshots for the devtools Context Inspector tab
    and records compaction history for the timeline chart.
    """

    def __init__(
        self,
        max_tokens: int = 32768,
        compaction_threshold: float = 0.80,
    ) -> None:
        self._max_tokens = max_tokens
        self._compaction_threshold = compaction_threshold
        self._layers: list[ContextLayer] = []
        self._compaction_history: list[dict[str, Any]] = []

    @property
    def total_tokens(self) -> int:
        return sum(layer.tokens for layer in self._layers)

    @property
    def utilization(self) -> float:
        if self._max_tokens == 0:
            return 0.0
        return self.total_tokens / self._max_tokens

    @property
    def compaction_needed(self) -> bool:
        return self.utilization >= self._compaction_threshold

    @property
    def compaction_history(self) -> list[dict[str, Any]]:
        return list(self._compaction_history)

    def add_layer(self, layer: ContextLayer) -> None:
        existing = [i for i, l in enumerate(self._layers) if l.name == layer.name]
        if existing:
            self._layers[existing[0]] = layer
        else:
            self._layers.append(layer)

    def remove_layer(self, name: str) -> None:
        self._layers = [l for l in self._layers if l.name != name]

    def snapshot(self) -> dict[str, Any]:
        """Return current context state for the devtools inspector."""
        return {
            "total_tokens": self.total_tokens,
            "max_tokens": self._max_tokens,
            "utilization": round(self.utilization, 4),
            "compaction_needed": self.compaction_needed,
            "layers": [
                {
                    "name": layer.name,
                    "tokens": layer.tokens,
                    "compactable": layer.compactable,
                    "items": layer.items,
                }
                for layer in self._layers
            ],
            "compaction_history": self._compaction_history,
        }

    def record_compaction(
        self,
        tokens_before: int,
        tokens_after: int,
        removed: list[dict[str, Any]],
        survived: list[str],
    ) -> None:
        self._compaction_history.append({
            "id": len(self._compaction_history) + 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tokens_before": tokens_before,
            "tokens_after": tokens_after,
            "tokens_freed": tokens_before - tokens_after,
            "trigger_utilization": round(tokens_before / self._max_tokens, 4),
            "removed": removed,
            "survived": survived,
        })
```

- [ ] **Step 4: Run tests**

```bash
cd backend && pytest tests/unit/test_context_manager.py -v
```

Expected: PASS (5 tests)

- [ ] **Step 5: Wire context API endpoint**

Create `backend/app/api/context_api.py`:

```python
from fastapi import APIRouter

from app.context.manager import ContextManager

router = APIRouter()

# In-memory context manager (will be per-session in future)
_context_manager = ContextManager()


def get_context_manager() -> ContextManager:
    return _context_manager


@router.get("/api/context")
async def get_context() -> dict:
    return get_context_manager().snapshot()
```

Add to `backend/app/main.py` — add import and include_router:

```python
from app.api.context_api import router as context_router
```

Add after `app.include_router(health_router)`:

```python
    app.include_router(context_router)
```

- [ ] **Step 6: Commit**

```bash
git add backend/app/context/ backend/app/api/context_api.py backend/tests/unit/test_context_manager.py backend/app/main.py
git commit -m "feat: add context window manager with layer tracking and compaction history"
```

---

## Task 6: Knowledge system — wiki scaffold and ADRs

**Files:**
- Create: `knowledge/wiki/index.md`
- Create: `knowledge/wiki/log.md`
- Create: `knowledge/wiki/working.md`
- Create: `knowledge/wiki/entities/.gitkeep`
- Create: `knowledge/wiki/findings/.gitkeep`
- Create: `knowledge/wiki/hypotheses/.gitkeep`
- Create: `knowledge/wiki/meta/.gitkeep`
- Create: `knowledge/adr/template.md`
- Create: `knowledge/adr/001-python-over-typescript.md`
- Create: `knowledge/adr/002-vite-over-nextjs.md`

- [ ] **Step 1: Create wiki directory structure**

```bash
mkdir -p knowledge/wiki/{entities,findings,hypotheses,meta}
touch knowledge/wiki/entities/.gitkeep
touch knowledge/wiki/findings/.gitkeep
touch knowledge/wiki/hypotheses/.gitkeep
touch knowledge/wiki/meta/.gitkeep
```

- [ ] **Step 2: Write wiki seed files**

Create `knowledge/wiki/index.md`:

```markdown
# Wiki Index

> This file is always in the agent's context (~600 tokens budget).
> One line per page. Updated on every wiki write.

## Entities

_(no pages yet)_

## Findings

_(no findings yet)_

## Hypotheses

_(no hypotheses yet)_

## Meta

_(no meta pages yet)_
```

Create `knowledge/wiki/log.md`:

```markdown
# Wiki Log

> Append-only. Last 10 operations. Always in agent's context (~200 tokens budget).
> Format: `## [YYYY-MM-DD] action | details`

## [2026-04-11] init | Wiki created with empty index
```

Create `knowledge/wiki/working.md`:

```markdown
# Working

> What the agent is doing RIGHT NOW. Always in context (~800 tokens budget).
> Updated at start and end of each session.

## Current Focus

Project restructure — migrating to hybrid monorepo layout with backend/frontend/reference separation.

## Active Decisions

- Backend: Python/FastAPI (ADR-001)
- Frontend: React+Vite (ADR-002)
- Skills: Two-layer architecture (SKILL.md + Python packages)

## Next Steps

1. Complete file migration
2. Scaffold backend and frontend
3. Set up skills system foundation
```

- [ ] **Step 3: Write ADR template**

Create `knowledge/adr/template.md`:

```markdown
# ADR-NNN: Title

**Status:** Proposed | Accepted | Superseded | Rejected
**Date:** YYYY-MM-DD
**Supersedes:** _(ADR number if applicable)_

## Context

What is the issue? What forces are at play?

## Decision

What did we decide?

## Consequences

What are the trade-offs? What becomes easier/harder?
```

- [ ] **Step 4: Write ADR-001**

Create `knowledge/adr/001-python-over-typescript.md`:

```markdown
# ADR-001: Python/FastAPI for Backend

**Status:** Accepted
**Date:** 2026-04-11

## Context

The platform targets MLE, data scientists, and quants who work primarily in Python. The agent needs to execute Python data science code in a sandbox (polars, numpy, scipy, altair, duckdb). The existing CLI source in `reference/src/` is TypeScript/Bun, but serves only as study material.

Two options considered:
1. **TypeScript/Bun** — same language as the CLI source, strong types, fast runtime
2. **Python/FastAPI** — native to the data science ecosystem, LangGraph agent framework, zero cross-language serialization for sandbox

## Decision

Use Python/FastAPI. The sandbox runs Python code — keeping the backend in Python eliminates cross-language serialization overhead. LangGraph for agent orchestration is Python-native. Target users think in Python and will want to extend the platform.

## Consequences

- **Easier:** Sandbox integration, data science library access, user contributions
- **Harder:** Type safety requires discipline (Pydantic + mypy), deployment is heavier than a single JS bundle
- **Mitigated:** Pydantic models provide runtime validation; Docker handles deployment
```

- [ ] **Step 5: Write ADR-002**

Create `knowledge/adr/002-vite-over-nextjs.md`:

```markdown
# ADR-002: React+Vite Frontend (New) Over Existing Next.js

**Status:** Accepted
**Date:** 2026-04-11

## Context

The existing `reference/web/` is a Next.js frontend built for Claude Code's web interface — chat-centric, Radix UI, CodeMirror. Our platform needs a fundamentally different UI: a 4-zone analytical layout with artifacts panel, trace viewer, scratchpad, and developer mode workbench.

## Decision

Build a new React+Vite frontend purpose-built for the analytical platform. The existing Next.js frontend stays in `reference/web/` as study material for component patterns.

## Consequences

- **Easier:** Full control over dependencies, lighter build, faster HMR, no legacy constraints
- **Harder:** No pre-built components to inherit (must build from scratch)
- **Mitigated:** Can borrow component patterns from `reference/web/` as needed
```

- [ ] **Step 6: Commit**

```bash
git add knowledge/
git commit -m "feat: set up knowledge system with wiki scaffold and initial ADRs"
```

---

## Task 7: Harness docs — SOPs and guides

**Files:**
- Create: `docs/dev-setup.md`
- Create: `docs/architecture.md`
- Create: `docs/testing.md`
- Create: `docs/skill-creation.md`
- Create: `docs/git-workflow.md`
- Create: `docs/gotchas.md`

Note: `docs/superpowers/` already exists from the spec. The new docs go alongside it.

- [ ] **Step 1: Write dev-setup.md**

Create `docs/dev-setup.md`:

```markdown
# Development Setup

## Prerequisites

- Python 3.12+
- Node.js 20+ (for frontend)
- Docker + Docker Compose (for local services)
- Ollama (for local models)

## Quick Start

```bash
# 1. Clone and enter
git clone https://github.com/Zehaoyu217/analytical-agent.git
cd analytical-agent

# 2. Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cd ..

# 3. Frontend
cd frontend
npm install
cd ..

# 4. Environment
cp .env.example .env
# Edit .env with your settings

# 5. Start everything
make dev
```

## Individual Services

```bash
make backend          # Backend only (uvicorn on :8000)
make frontend         # Frontend only (vite on :5173)
```

## Running Tests

```bash
make test             # All tests
make test-backend     # Backend only (pytest)
make test-frontend    # Frontend only (vitest)
```

## Ollama Setup

```bash
# Install Ollama: https://ollama.ai
ollama pull qwen3.5:9b
source infra/ollama/start.sh
```
```

- [ ] **Step 2: Write architecture.md**

Create `docs/architecture.md`:

```markdown
# Architecture

## System Overview

```
┌─────────────────────────────────────────────┐
│  Frontend (React+Vite, :5173)               │
│  ├── Analytical UI (4-zone layout)          │
│  └── Devtools (Cmd+Shift+D overlay)         │
└──────────────┬──────────────────────────────┘
               │ REST + SSE
┌──────────────▼──────────────────────────────┐
│  Backend (FastAPI, :8000)                    │
│  ├── Agent (LangGraph)                      │
│  ├── Skills (registry + packages)           │
│  ├── Sandbox (subprocess Python execution)  │
│  ├── Wiki Engine (Karpathy pattern)         │
│  ├── Context Manager (layer tracking)       │
│  └── Data Layer (DuckDB)                    │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│  Infrastructure                              │
│  ├── Ollama + LiteLLM (local models)        │
│  ├── DuckDB (analytical database)           │
│  └── Docker Compose (orchestration)         │
└─────────────────────────────────────────────┘
```

## Directory Structure

See `CLAUDE.md` for the full directory map.

## Key Design Decisions

See `knowledge/adr/` for Architecture Decision Records.

## Context Window Management

The agent's context is divided into layers — see spec section 6 for details.
L1 (working.md, index.md, log.md) is always in context. Everything else is managed.
```

- [ ] **Step 3: Write testing.md**

Create `docs/testing.md`:

```markdown
# Testing Guide

## Backend (pytest)

```bash
cd backend
pytest                           # all tests
pytest tests/unit/               # unit only
pytest tests/integration/        # integration only
pytest -v -k "test_config"      # specific test
pytest --cov=app --cov-report=term-missing  # coverage
```

Target: 80% coverage minimum.

## Frontend (vitest)

```bash
cd frontend
npm test                         # all tests
npm run test:watch               # watch mode
```

## Skill Evals

```bash
make skill-eval                  # all skills
make skill-eval skill=timeseries # specific skill
```

Skill evals test agent behavior against sealed assertions — see `docs/skill-creation.md`.

## Writing Tests

Follow the AAA pattern (Arrange-Act-Assert):

```python
def test_config_loads_defaults() -> None:
    # Arrange
    # (config auto-loads from env)

    # Act
    config = get_config()

    # Assert
    assert config.environment == "test"
```
```

- [ ] **Step 4: Write skill-creation.md**

Create `docs/skill-creation.md`:

```markdown
# Skill Creation Guide

## Anatomy of a Skill

```
backend/app/skills/<name>/
├── SKILL.md          # Agent reads this (<200 lines)
├── skill.yaml        # Metadata, triggers, dependencies
├── pkg/              # Python package (agent imports in sandbox)
│   ├── __init__.py   # Public API
│   └── <modules>.py  # Implementations (unlimited length)
├── references/       # Agent loads on demand
├── tests/            # Unit tests (pytest)
└── evals/            # SEALED — never loaded to agent
    ├── eval.yaml     # Test cases + assertions
    └── fixtures/     # Sample data
```

## Step-by-Step

1. **Scaffold:** `make skill-new name=my_skill`
2. **Write skill.yaml:** Define name, level, errors, dependencies
3. **Write pkg/:** Implement functions with `@skill_function` decorator
4. **Write SKILL.md:** Agent instructions (<200 lines)
5. **Write tests/:** Unit tests for pkg functions
6. **Write evals/:** Sealed behavioral tests
7. **Validate:** `make skill-check` then `make skill-eval skill=my_skill`

## Key Rules

- SKILL.md < 200 lines — it's instructions, not implementation
- Python packages have no line limit — they're libraries
- Every error must be declared in skill.yaml with message + guidance + recovery
- Parameter names must be self-documenting
- evals/ is never loaded into the agent's context
- Level 1 skills are leaf functions, level 2 compose level 1, level 3 orchestrates level 2
```

- [ ] **Step 5: Write git-workflow.md and gotchas.md**

Create `docs/git-workflow.md`:

```markdown
# Git Workflow

## Branch Naming

```
feat/<feature-name>
fix/<bug-description>
refactor/<what>
docs/<what>
```

## Commit Format

```
<type>: <description>

<optional body>
```

Types: feat, fix, refactor, docs, test, chore, perf

## Pull Requests

1. Branch from `main`
2. Make changes, commit with conventional commits
3. Push with `git push -u origin <branch>`
4. Create PR: `gh pr create --title "..." --body "..."`
5. Ensure all checks pass before merge
```

Create `docs/gotchas.md`:

```markdown
# Gotchas

Known pitfalls, workarounds, and things that will bite you. Append-only with dates.

---

## [2026-04-11] reference/ is read-only

The `reference/` directory contains the original Claude Code CLI source. Do not modify files there. If you need to study a pattern, read it and reimplement in `backend/` or `frontend/`.

## [2026-04-11] Skill evals are sealed

The `evals/` directory inside each skill is never loaded into the agent's context. This is by design — the agent must not know what the eval assertions check for.
```

- [ ] **Step 6: Commit**

```bash
git add docs/dev-setup.md docs/architecture.md docs/testing.md docs/skill-creation.md docs/git-workflow.md docs/gotchas.md
git commit -m "docs: add SOPs for dev setup, architecture, testing, skills, git, and gotchas"
```

---

## Task 8: Rewrite CLAUDE.md and create root files

**Files:**
- Rewrite: `CLAUDE.md`
- Create: `Makefile`
- Create: `.env.example`
- Create: `README.md`
- Modify: `.gitignore`

- [ ] **Step 1: Rewrite CLAUDE.md**

Replace the contents of `CLAUDE.md` with:

```markdown
# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## What This Is

Analytical Agent — a full-stack analytical platform for MLE, data scientists, and quants. AI-powered data analysis with transparent agent operations, a skills system for composable analytical capabilities, and a developer workbench for full observability.

## Project Structure

| Directory | What | Modify? |
|-----------|------|---------|
| `backend/` | Python/FastAPI backend (agent, skills, sandbox, API) | Yes |
| `frontend/` | React+Vite analytical UI + devtools | Yes |
| `mcp/` | MCP explorer server | Yes |
| `infra/` | Docker, Helm, Grafana, Ollama | Yes |
| `knowledge/` | Wiki, graphify graphs, ADRs | Yes |
| `docs/` | SOPs, guides, gotchas | Yes |
| `scripts/` | Dev tooling scripts | Yes |
| `reference/` | Original Claude Code CLI source (read-only) | **No** |

## Commands

```bash
# Development
make dev              # Start backend + frontend + Ollama
make backend          # Backend only (uvicorn :8000)
make frontend         # Frontend only (vite :5173)

# Quality
make lint             # Ruff (backend) + ESLint (frontend)
make typecheck        # Mypy (backend) + tsc (frontend)
make test             # All tests
make test-backend     # pytest
make test-frontend    # vitest

# Skills
make skill-check      # Dependency manifest check
make skill-eval       # Run all skill evals
make skill-new name=X # Scaffold new skill

# Knowledge
make wiki-lint        # Run wiki lint cycle
make graphify         # Regenerate graphify output
```

## Architecture

```
Frontend (React+Vite :5173)
    ↕ REST + SSE
Backend (FastAPI :8000)
    ├── Agent (LangGraph) → Tools → Sandbox (subprocess Python)
    ├── Skills (registry + packages, importable in sandbox)
    ├── Wiki Engine (Karpathy pattern, knowledge/wiki/)
    ├── Context Manager (layer tracking, compaction)
    └── Data (DuckDB, dataset registry)
```

## Conventions

- **Backend:** Python 3.12+, Ruff formatter, type hints everywhere, Pydantic for schemas
- **Frontend:** TypeScript strict, Vite, Zustand for state
- **Tests:** pytest (backend), vitest (frontend), 80% coverage target
- **Commits:** `<type>: <description>` (feat, fix, refactor, docs, test, chore)
- **Skills:** SKILL.md < 200 lines, Python packages unlimited, errors must be actionable

## Current State

Read `knowledge/wiki/working.md` for what's in progress.

## Deeper Context

- Architecture decisions: `knowledge/adr/`
- Development setup: `docs/dev-setup.md`
- Testing guide: `docs/testing.md`
- Skill creation: `docs/skill-creation.md`
- Known gotchas: `docs/gotchas.md`
```

- [ ] **Step 2: Create Makefile**

Create `Makefile`:

```makefile
.PHONY: dev backend frontend test test-backend test-frontend lint typecheck \
        skill-check skill-eval skill-new wiki-lint graphify seed-data \
        docker-build docker-up

# Development
dev:
	@echo "Starting backend and frontend..."
	$(MAKE) -j2 backend frontend

backend:
	cd backend && uvicorn app.main:create_app --factory --reload --host 127.0.0.1 --port 8000

frontend:
	cd frontend && npm run dev

# Quality
lint:
	cd backend && ruff check . --fix
	cd frontend && npm run lint 2>/dev/null || true

typecheck:
	cd backend && mypy app/
	cd frontend && npx tsc --noEmit 2>/dev/null || true

test: test-backend test-frontend

test-backend:
	cd backend && pytest -v --tb=short

test-frontend:
	cd frontend && npm test 2>/dev/null || echo "No frontend tests yet"

# Skills
skill-check:
	cd backend && python -m app.skills.manifest

skill-eval:
ifdef skill
	cd backend && python -m pytest tests/evals/test_$(skill).py -v
else
	cd backend && python -m pytest tests/evals/ -v 2>/dev/null || echo "No skill evals yet"
endif

skill-new:
ifndef name
	$(error Usage: make skill-new name=<skill_name>)
endif
	@mkdir -p backend/app/skills/$(name)/{pkg,references,tests,evals/fixtures}
	@touch backend/app/skills/$(name)/pkg/__init__.py
	@echo "---\nname: $(name)\n---\n# $(name)\n" > backend/app/skills/$(name)/SKILL.md
	@echo "name: $(name)\nversion: '0.1'\ndescription: ''\nlevel: 1\nerrors: {}\ndependencies:\n  requires: []\n  used_by: []\n  packages: []" > backend/app/skills/$(name)/skill.yaml
	@echo "Skill scaffolded at backend/app/skills/$(name)/"

# Knowledge
wiki-lint:
	cd backend && python -m app.wiki.lint 2>/dev/null || echo "Wiki lint not yet implemented"

graphify:
	@echo "Running graphify..." && echo "Not yet implemented"

# Data
seed-data:
	@echo "Seeding sample data..." && echo "Not yet implemented"

# Infrastructure
docker-build:
	docker compose build

docker-up:
	docker compose up -d
```

- [ ] **Step 3: Create .env.example**

Create `.env.example`:

```bash
# Application
ENVIRONMENT=development
DEBUG=true

# Model
DEFAULT_MODEL=qwen3.5:9b
OLLAMA_BASE_URL=http://localhost:11434
LITELLM_BASE_URL=http://localhost:4000

# Sandbox
SANDBOX_TIMEOUT_SECONDS=30
SANDBOX_MAX_MEMORY_MB=2048

# DuckDB
DUCKDB_PATH=./data/duckdb/analytical.db

# Wiki
WIKI_ROOT=../knowledge/wiki
WIKI_AUTO_WRITE=true

# Context
CONTEXT_MAX_TOKENS=32768
CONTEXT_COMPACTION_THRESHOLD=0.80
```

- [ ] **Step 4: Create README.md**

Create `README.md`:

```markdown
# Analytical Agent

Full-stack analytical platform for MLE, data scientists, and quants. AI-powered data analysis with transparent agent operations.

## Quick Start

```bash
cd backend && pip install -e ".[dev]"
cd frontend && npm install
make dev
```

Open http://localhost:5173

## Documentation

- [Development Setup](docs/dev-setup.md)
- [Architecture](docs/architecture.md)
- [Testing Guide](docs/testing.md)
- [Skill Creation](docs/skill-creation.md)

## Project Structure

```
backend/       Python/FastAPI backend
frontend/      React+Vite analytical UI
reference/     Claude Code CLI source (read-only study material)
knowledge/     Wiki, ADRs, graphify graphs
docs/          SOPs and guides
infra/         Docker, Helm, Grafana, Ollama
mcp/           MCP explorer server
```

## License

See [LICENSE](LICENSE).
```

- [ ] **Step 5: Update .gitignore**

Replace `.gitignore` with:

```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/
*.egg
dist/
build/

# Node
node_modules/
.next/

# Build output
dist/
out/
*.tsbuildinfo

# Environment
.env
.env.local
.env.*.local

# Data
data/
*.db
*.duckdb

# OS
.DS_Store
Thumbs.db

# Editor / IDE
.idea/
*.swp
*.swo
*~
.vscode/settings.json
.vscode/launch.json

# Debug & logs
*.log
debug-logs/
coverage/
htmlcov/
.coverage

# Bun (reference/)
bun.lockb

# MCP registry
.mcpregistry_*

# Temporary
tmp/
temp/

# Superpowers brainstorm sessions
.superpowers/

# Sandbox sessions
data/sandbox_sessions/

# Graphify working files (output lives in knowledge/graphs/)
**/graphify-out/
```

- [ ] **Step 6: Commit**

```bash
git add CLAUDE.md Makefile .env.example README.md .gitignore
git commit -m "feat: rewrite CLAUDE.md, add Makefile, README, env template, and updated gitignore"
```

---

## Task 9: Frontend scaffold

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.ts`
- Create: `frontend/tsconfig.json`
- Create: `frontend/index.html`
- Create: `frontend/src/main.tsx`
- Create: `frontend/src/App.tsx`
- Create: `frontend/src/panels/StatusBar.tsx`
- Create: `frontend/src/devtools/DevToolsPanel.tsx`
- Create: `frontend/src/devtools/ContextInspector.tsx`
- Create: `frontend/src/lib/api.ts`
- Create: `frontend/src/stores/devtools.ts`

- [ ] **Step 1: Create package.json**

Create `frontend/package.json`:

```json
{
  "name": "analytical-agent-frontend",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview",
    "test": "vitest run",
    "test:watch": "vitest",
    "lint": "eslint ."
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "zustand": "^5.0.0"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "@vitejs/plugin-react": "^4.3.0",
    "typescript": "~5.7.0",
    "vite": "^6.0.0",
    "vitest": "^3.0.0"
  }
}
```

- [ ] **Step 2: Create vite.config.ts**

Create `frontend/vite.config.ts`:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

- [ ] **Step 3: Create tsconfig.json**

Create `frontend/tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "skipLibCheck": true,
    "outDir": "./dist"
  },
  "include": ["src"]
}
```

- [ ] **Step 4: Create index.html**

Create `frontend/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Analytical Agent</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

- [ ] **Step 5: Create API client**

Create `frontend/src/lib/api.ts`:

```typescript
const BASE_URL = '/api'

export async function fetchHealth(): Promise<{ status: string; version: string }> {
  const res = await fetch(`${BASE_URL}/health`)
  return res.json()
}

export interface ContextSnapshot {
  total_tokens: number
  max_tokens: number
  utilization: number
  compaction_needed: boolean
  layers: Array<{
    name: string
    tokens: number
    compactable: boolean
    items: Array<{ name: string; tokens: number }>
  }>
  compaction_history: Array<{
    id: number
    timestamp: string
    tokens_before: number
    tokens_after: number
    tokens_freed: number
    trigger_utilization: number
    removed: Array<{ name: string; tokens: number }>
    survived: string[]
  }>
}

export async function fetchContext(): Promise<ContextSnapshot> {
  const res = await fetch(`${BASE_URL}/context`)
  return res.json()
}
```

- [ ] **Step 6: Create devtools store**

Create `frontend/src/stores/devtools.ts`:

```typescript
import { create } from 'zustand'
import type { ContextSnapshot } from '../lib/api'

interface DevtoolsState {
  isOpen: boolean
  activeTab: 'events' | 'skills' | 'config' | 'wiki' | 'evals' | 'context'
  contextSnapshot: ContextSnapshot | null
  toggle: () => void
  setActiveTab: (tab: DevtoolsState['activeTab']) => void
  setContextSnapshot: (snapshot: ContextSnapshot) => void
}

export const useDevtoolsStore = create<DevtoolsState>((set) => ({
  isOpen: false,
  activeTab: 'context',
  contextSnapshot: null,
  toggle: () => set((s) => ({ isOpen: !s.isOpen })),
  setActiveTab: (tab) => set({ activeTab: tab }),
  setContextSnapshot: (snapshot) => set({ contextSnapshot: snapshot }),
}))
```

- [ ] **Step 7: Create StatusBar component**

Create `frontend/src/panels/StatusBar.tsx`:

```tsx
import { useDevtoolsStore } from '../stores/devtools'

export function StatusBar() {
  const { isOpen, toggle, contextSnapshot } = useDevtoolsStore()
  const utilization = contextSnapshot
    ? `${(contextSnapshot.utilization * 100).toFixed(1)}%`
    : '—'

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '4px 12px',
      background: '#14141f',
      borderTop: '1px solid #2a2a3a',
      fontSize: '10px',
      color: '#64748b',
      fontFamily: 'monospace',
    }}>
      <div style={{ display: 'flex', gap: 16 }}>
        <span>DuckDB: <span style={{ color: '#94a3b8' }}>—</span></span>
        <span>Ollama: <span style={{ color: '#94a3b8' }}>—</span></span>
        <span>Context: <span style={{ color: '#94a3b8' }}>{utilization}</span></span>
      </div>
      <button
        onClick={toggle}
        style={{
          background: 'none',
          border: 'none',
          color: isOpen ? '#818cf8' : '#64748b',
          cursor: 'pointer',
          fontSize: '10px',
          fontFamily: 'monospace',
        }}
      >
        {isOpen ? '⚙ DEV MODE ON' : '⚙ Cmd+Shift+D'}
      </button>
    </div>
  )
}
```

- [ ] **Step 8: Create ContextInspector component**

Create `frontend/src/devtools/ContextInspector.tsx`:

```tsx
import { useEffect } from 'react'
import { fetchContext } from '../lib/api'
import { useDevtoolsStore } from '../stores/devtools'

const LAYER_COLORS: Record<string, string> = {
  system: '#ef4444',
  l1_always: '#f97316',
  l2_skill: '#f59e0b',
  memory: '#eab308',
  knowledge: '#22c55e',
  conversation: '#818cf8',
}

export function ContextInspector() {
  const { contextSnapshot, setContextSnapshot } = useDevtoolsStore()

  useEffect(() => {
    fetchContext().then(setContextSnapshot).catch(() => {})
    const interval = setInterval(() => {
      fetchContext().then(setContextSnapshot).catch(() => {})
    }, 2000)
    return () => clearInterval(interval)
  }, [setContextSnapshot])

  if (!contextSnapshot) {
    return <div style={{ color: '#94a3b8', padding: 16 }}>Loading context...</div>
  }

  const { total_tokens, max_tokens, utilization, layers, compaction_history } = contextSnapshot

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', height: '100%', overflow: 'hidden' }}>
      {/* Left: layers */}
      <div style={{ overflowY: 'auto', padding: 8, borderRight: '1px solid #2a2a3a' }}>
        <div style={{ color: '#818cf8', fontSize: 10, textTransform: 'uppercase', marginBottom: 8, letterSpacing: 1 }}>
          Context Layers — {total_tokens.toLocaleString()} / {max_tokens.toLocaleString()} tokens ({(utilization * 100).toFixed(1)}%)
        </div>
        {layers.map((layer) => (
          <div
            key={layer.name}
            style={{
              background: '#14141f',
              border: '1px solid #2a2a3a',
              borderLeft: `3px solid ${LAYER_COLORS[layer.name] ?? '#64748b'}`,
              borderRadius: 4,
              padding: 8,
              marginBottom: 6,
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 10 }}>
              <span style={{ color: LAYER_COLORS[layer.name] ?? '#64748b', fontWeight: 600 }}>
                {layer.name.toUpperCase()}
              </span>
              <span style={{ color: '#4a4a5a' }}>{layer.tokens.toLocaleString()} tok</span>
            </div>
            {layer.items.length > 0 && (
              <div style={{ marginTop: 4, fontSize: 9, color: '#94a3b8', lineHeight: 1.5 }}>
                {layer.items.map((item, i) => (
                  <div key={i} style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>{i === layer.items.length - 1 ? '└' : '├'} {item.name}</span>
                    <span>{item.tokens}t</span>
                  </div>
                ))}
              </div>
            )}
            <div style={{ color: '#4a4a5a', fontSize: 9, marginTop: 4 }}>
              {layer.compactable ? 'Compactable' : 'Never compacted'}
            </div>
          </div>
        ))}
      </div>

      {/* Right: compaction history */}
      <div style={{ overflowY: 'auto', padding: 8 }}>
        <div style={{ color: '#818cf8', fontSize: 10, textTransform: 'uppercase', marginBottom: 8, letterSpacing: 1 }}>
          Compaction History
        </div>
        {compaction_history.length === 0 ? (
          <div style={{ color: '#4a4a5a', fontSize: 10 }}>No compactions yet</div>
        ) : (
          compaction_history.map((event) => (
            <div
              key={event.id}
              style={{
                background: '#14141f',
                border: '1px solid #2a2a3a',
                borderLeft: '3px solid #f59e0b',
                borderRadius: 4,
                padding: 8,
                marginBottom: 8,
                fontSize: 9,
                color: '#94a3b8',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                <span style={{ color: '#f59e0b', fontWeight: 600, fontSize: 10 }}>
                  COMPACTION #{event.id}
                </span>
                <span style={{ color: '#4a4a5a' }}>{new Date(event.timestamp).toLocaleTimeString()}</span>
              </div>
              <div>Trigger: {(event.trigger_utilization * 100).toFixed(1)}%</div>
              <div>Before: {event.tokens_before.toLocaleString()}t → After: {event.tokens_after.toLocaleString()}t</div>
              <div style={{ color: '#4ade80' }}>Freed: {event.tokens_freed.toLocaleString()} tokens</div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
```

- [ ] **Step 9: Create DevToolsPanel**

Create `frontend/src/devtools/DevToolsPanel.tsx`:

```tsx
import { useDevtoolsStore } from '../stores/devtools'
import { ContextInspector } from './ContextInspector'

const TABS = ['events', 'skills', 'config', 'wiki', 'evals', 'context'] as const

function Placeholder({ name }: { name: string }) {
  return (
    <div style={{ color: '#4a4a5a', padding: 16, fontSize: 12 }}>
      {name} tab — not yet implemented
    </div>
  )
}

export function DevToolsPanel() {
  const { isOpen, activeTab, setActiveTab } = useDevtoolsStore()
  if (!isOpen) return null

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 32,
      background: '#0a0a0f',
      color: '#e0e0e8',
      fontFamily: 'monospace',
      fontSize: 11,
      zIndex: 1000,
      display: 'flex',
      flexDirection: 'column',
    }}>
      {/* Tab bar */}
      <div style={{
        display: 'flex',
        gap: 16,
        padding: '8px 12px',
        borderBottom: '1px solid #2a2a3a',
        background: '#14141f',
      }}>
        <span style={{ color: '#818cf8', fontWeight: 600 }}>⚙ DEV MODE</span>
        {TABS.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            style={{
              background: 'none',
              border: 'none',
              color: activeTab === tab ? '#818cf8' : '#94a3b8',
              borderBottom: activeTab === tab ? '1px solid #818cf8' : 'none',
              cursor: 'pointer',
              fontSize: 11,
              fontFamily: 'monospace',
              textTransform: 'capitalize',
              padding: '0 4px 4px',
            }}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div style={{ flex: 1, overflow: 'hidden' }}>
        {activeTab === 'context' && <ContextInspector />}
        {activeTab !== 'context' && <Placeholder name={activeTab} />}
      </div>
    </div>
  )
}
```

- [ ] **Step 10: Create App.tsx and main.tsx**

Create `frontend/src/App.tsx`:

```tsx
import { useEffect } from 'react'
import { StatusBar } from './panels/StatusBar'
import { DevToolsPanel } from './devtools/DevToolsPanel'
import { useDevtoolsStore } from './stores/devtools'

export default function App() {
  const toggle = useDevtoolsStore((s) => s.toggle)

  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.shiftKey && e.key === 'D') {
        e.preventDefault()
        toggle()
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [toggle])

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100vh',
      background: '#0a0a0f',
      color: '#e0e0e8',
    }}>
      {/* Main content area (placeholder for analytical UI) */}
      <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ textAlign: 'center', color: '#4a4a5a' }}>
          <h1 style={{ fontSize: 24, fontWeight: 300, marginBottom: 8 }}>Analytical Agent</h1>
          <p style={{ fontSize: 12 }}>Press Cmd+Shift+D to open developer tools</p>
        </div>
      </div>

      {/* Devtools overlay */}
      <DevToolsPanel />

      {/* Status bar (always visible) */}
      <StatusBar />
    </div>
  )
}
```

Create `frontend/src/main.tsx`:

```tsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
```

- [ ] **Step 11: Install and verify build**

```bash
cd frontend && npm install && npx tsc --noEmit
```

Expected: No errors.

- [ ] **Step 12: Commit**

```bash
git add frontend/
git commit -m "feat: scaffold frontend with devtools shell, context inspector, and status bar"
```

---

## Task 10: Dev script and final verification

**Files:**
- Create: `scripts/dev.sh`
- Verify: full test suite passes
- Push to remote

- [ ] **Step 1: Create dev.sh**

Create `scripts/dev.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "=== Analytical Agent — Local Development ==="
echo ""

# Check prerequisites
command -v python3 >/dev/null 2>&1 || { echo "Python 3 required"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "Node.js required"; exit 1; }

# Backend
if [ ! -d "backend/.venv" ]; then
    echo "Setting up backend virtualenv..."
    cd backend && python3 -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]" && cd ..
else
    source backend/.venv/bin/activate
fi

# Frontend
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing frontend dependencies..."
    cd frontend && npm install && cd ..
fi

echo ""
echo "Starting services..."
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:5173"
echo "  Health:   http://localhost:8000/api/health"
echo ""

make dev
```

```bash
chmod +x scripts/dev.sh
```

- [ ] **Step 2: Run full backend test suite**

```bash
cd backend && pip install -e ".[dev]" && pytest -v --tb=short
```

Expected: All tests pass (config: 3, health: 2, skill_base: 4, skill_registry: 4, context_manager: 5 = **18 tests total**).

- [ ] **Step 3: Verify frontend builds**

```bash
cd frontend && npm install && npx tsc --noEmit
```

Expected: No TypeScript errors.

- [ ] **Step 4: Commit and push**

```bash
git add scripts/
git commit -m "feat: add dev script for local development setup"
git push origin main
```

- [ ] **Step 5: Final verification — test full flow**

```bash
# Start backend
cd backend && uvicorn app.main:create_app --factory --host 127.0.0.1 --port 8000 &

# Test health
curl http://localhost:8000/api/health
# Expected: {"status":"ok","version":"0.1.0"}

# Test context endpoint
curl http://localhost:8000/api/context
# Expected: {"total_tokens":0,"max_tokens":32768,"utilization":0.0,...}

# Kill backend
kill %1
```

---

## Summary

| Task | What | Tests |
|------|------|-------|
| 1 | Migrate files to reference/, infra/, mcp/ | — (structural) |
| 2 | Backend scaffold: app factory, config, health | 5 tests |
| 3 | Skills base types: SkillError, SkillResult | 4 tests |
| 4 | Skills registry + manifest | 4 tests |
| 5 | Context manager with layer tracking | 5 tests |
| 6 | Knowledge system: wiki scaffold + ADRs | — (content) |
| 7 | Harness docs: SOPs and guides | — (content) |
| 8 | CLAUDE.md rewrite, Makefile, root files | — (config) |
| 9 | Frontend scaffold with devtools shell | TypeScript check |
| 10 | Dev script + final verification | Integration check |

**Total: 10 tasks, 18 backend tests, TypeScript compilation check, integration verification.**
