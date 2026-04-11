# Project Restructure & Harness Design

**Date:** 2026-04-11
**Status:** Draft
**Scope:** Sub-project 1 — File structure reorganization + project harness

---

## 1. Context

claude-code-agent contains Anthropic's leaked Claude Code CLI source (~512K lines TypeScript) as read-only study material. The goal is to build a full-stack analytical platform on top of this repo — targeting MLE, data scientists, and quants — with a Python/FastAPI backend, React+Vite frontend, and a comprehensive developer harness for transparency and control.

### Decisions made

| Decision | Rationale | ADR |
|----------|-----------|-----|
| Python/FastAPI backend | Native sandbox for data science code, LangGraph ecosystem, target users think in Python | 001 |
| React+Vite frontend (new) | Existing `web/` is a different product; 4-zone analytical layout needs purpose-built UI | 002 |
| `src/` as study material only | Read-only reference for agent patterns; not modified or extended | — |
| Analytical-chatbot as reference only | Different agent framework; patterns and ideas borrowed, code not merged | — |

### What this spec covers

1. File structure (hybrid monorepo layout)
2. Project harness (CLAUDE.md, docs, knowledge system)
3. Skills system (instruction layer + Python packages + sealed evals)
4. Devtools UI (6-tab developer workbench)
5. Context window inspector (full transparency into LLM context management)
6. Migration mapping (existing files → new structure)

### What this spec does NOT cover (future sub-projects)

- Backend agent implementation (LangGraph graph, tool loop)
- Frontend analytical UI (4-zone layout, artifact rendering)
- Sandbox implementation
- Data ingestion pipeline
- Wiki engine implementation

---

## 2. File Structure

Hybrid layout: layer separation at top level, domain organization within layers.

```
claude-code-agent/
│
├── CLAUDE.md                    # Harness entry point
├── Makefile                     # Unified commands
├── docker-compose.yml           # Local dev orchestration
├── .env.example                 # Environment template
│
├── backend/                     # Python/FastAPI
│   ├── pyproject.toml
│   ├── app/
│   │   ├── main.py              # FastAPI app factory
│   │   ├── config.py            # Pydantic settings (env-based)
│   │   ├── agent/               # LangGraph agent
│   │   │   ├── graph.py         # Agent graph definition
│   │   │   ├── state.py         # Agent state schema
│   │   │   ├── tools/           # Tool implementations
│   │   │   │   ├── query_duckdb.py
│   │   │   │   ├── run_python.py
│   │   │   │   ├── scratchpad.py
│   │   │   │   └── save_artifact.py
│   │   │   └── prompts/         # System prompts, tool descriptions
│   │   ├── sandbox/             # Python code execution
│   │   │   ├── runner.py        # Subprocess executor
│   │   │   ├── policy.py        # Allowed imports, resource limits
│   │   │   └── builtins.py      # Pre-injected globals (df, alt, np)
│   │   ├── data/                # Data layer
│   │   │   ├── ingest.py        # File upload + parsing
│   │   │   ├── duckdb.py        # DuckDB connection manager
│   │   │   └── registry.py      # Dataset metadata registry
│   │   ├── api/                 # HTTP layer
│   │   │   ├── chat.py          # POST /chat, SSE streaming
│   │   │   ├── datasets.py      # CRUD /datasets
│   │   │   ├── artifacts.py     # GET /artifacts
│   │   │   ├── config_api.py    # GET/PUT /config (devtools)
│   │   │   ├── context_api.py   # GET /context (context inspector)
│   │   │   └── health.py        # Health + readiness
│   │   ├── skills/              # Skills system
│   │   │   ├── registry.py      # Skill discovery + dependency resolver
│   │   │   ├── base.py          # SkillError, SkillResult, SkillContext
│   │   │   ├── manifest.py      # Closed-loop dependency tracker
│   │   │   ├── eda/             # EDA skill
│   │   │   ├── timeseries/      # Time series skill
│   │   │   ├── modeling/        # ML modeling skill
│   │   │   └── query_data/      # DuckDB query skill
│   │   ├── wiki/                # LLM wiki engine
│   │   │   ├── engine.py        # Ingest, query, lint operations
│   │   │   ├── index.py         # index.md manager
│   │   │   └── search.py        # Full-text search over wiki pages
│   │   ├── context/             # Context window management
│   │   │   ├── manager.py       # Layer tracking, token counting
│   │   │   ├── compaction.py    # Multi-layer compaction engine
│   │   │   └── events.py        # Context change event emitter
│   │   ├── sessions/            # Session management
│   │   │   └── store.py         # Session state, artifact store
│   │   └── observability/       # Telemetry + logging
│   │       ├── events.py        # Structured event emitter
│   │       └── metrics.py       # Timing, token counting
│   └── tests/
│       ├── unit/
│       ├── integration/
│       └── conftest.py
│
├── frontend/                    # React+Vite
│   ├── package.json
│   ├── vite.config.ts
│   ├── index.html
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── panels/              # 4-zone analytical layout
│       │   ├── LeftPanel.tsx     # Datasets, model selector, metrics
│       │   ├── ChatPanel.tsx     # Conversation + thinking stream
│       │   ├── RightPanel.tsx    # Tabs: artifacts, trace, scratchpad
│       │   └── StatusBar.tsx     # Bottom: model, turn, tokens, timing
│       ├── devtools/            # Developer mode (Cmd+Shift+D)
│       │   ├── DevToolsPanel.tsx # Main container + tab routing
│       │   ├── EventStream.tsx   # Tab 1: real-time event log
│       │   ├── SkillBrowser.tsx  # Tab 2: skill registry + health
│       │   ├── ConfigEditor.tsx  # Tab 3: live config editor
│       │   ├── WikiBrowser.tsx   # Tab 4: wiki page browser
│       │   ├── EvalDashboard.tsx # Tab 5: skill eval results
│       │   └── ContextInspector.tsx # Tab 6: context window transparency
│       ├── components/          # Shared UI atoms
│       ├── lib/                 # API client, utils
│       └── stores/              # Zustand state management
│
├── reference/                   # Read-only — study material
│   ├── README.md                # "What this is and how to use it"
│   ├── src/                     # Original 512K TS source
│   ├── web/                     # Original Next.js frontend
│   ├── docs/                    # CLI architecture docs
│   ├── scripts/                 # CLI build scripts
│   ├── tests/                   # CLI test suite
│   ├── prompts/                 # CLI prompt templates
│   ├── agent.md
│   ├── Skill.md
│   ├── package.json
│   ├── tsconfig.json
│   └── biome.json
│
├── mcp/                         # MCP server (renamed from mcp-server/)
│
├── infra/                       # Deployment + local services
│   ├── docker/                  # Dockerfiles
│   ├── helm/                    # K8s charts
│   ├── grafana/                 # Dashboards
│   ├── ollama/                  # Local model scripts
│   └── nginx/                   # Reverse proxy config
│
├── knowledge/                   # Project intelligence (persistent, growing)
│   ├── wiki/                    # LLM wiki content (Karpathy pattern)
│   │   ├── index.md             # Catalog of all pages
│   │   ├── log.md               # Append-only changelog
│   │   ├── working.md           # Current focus
│   │   ├── entities/            # Concept/component pages
│   │   ├── findings/            # Confirmed discoveries
│   │   ├── hypotheses/          # Tested/rejected ideas
│   │   └── meta/                # Synthesis, coverage maps
│   ├── graphs/                  # Graphify output
│   │   ├── architecture.json
│   │   ├── dependencies.json
│   │   └── data-flow.json
│   └── adr/                     # Architecture decision records
│       ├── 000-initial-vision.md
│       ├── 001-python-over-typescript.md
│       ├── 002-vite-over-nextjs.md
│       └── template.md
│
├── docs/                        # SOPs, guides, operational docs
│   ├── architecture.md          # System overview + diagrams
│   ├── testing.md               # How to write and run tests
│   ├── deployment.md            # How to deploy
│   ├── data-handling.md         # Data formats, ingestion, DuckDB
│   ├── git-workflow.md          # Branching, commits, PRs
│   ├── model-guide.md           # Ollama models, config, performance
│   ├── skill-creation.md        # How to create and test skills
│   ├── gotchas.md               # Known pitfalls, workarounds
│   └── dev-setup.md             # Getting started from zero
│
└── scripts/                     # Dev tooling
    ├── dev.sh                   # Start everything for local dev
    ├── wiki-lint.sh             # Run wiki lint cycle
    ├── graphify-run.sh          # Regenerate graphify output
    └── seed-data.sh             # Load sample datasets
```

---

## 3. Project Harness

### 3.1 CLAUDE.md (entry point)

The root CLAUDE.md is the first thing any Claude session reads. It contains:

- **Project identity** — one paragraph: what this is, who it's for
- **Structure map** — which directories, what's in them, what's read-only
- **Quick commands** — `make dev`, `make test`, `make lint`, `make wiki-lint`
- **Architecture summary** — backend→frontend→mcp data flow
- **Active conventions** — coding style, commit format, test expectations
- **Pointers** — "For deeper context, see docs/ and knowledge/"
- **Current state** — "Read knowledge/wiki/working.md for what's in progress"

### 3.2 docs/ (operational knowledge)

| File | Purpose |
|------|---------|
| `dev-setup.md` | Zero-to-running. Prerequisites, env vars, first run. |
| `architecture.md` | System overview with diagrams. Updated by graphify. Links to ADRs. |
| `testing.md` | How to write tests, run them, coverage targets. Backend (pytest) + frontend (vitest/playwright). |
| `deployment.md` | Docker build, compose up, Helm deploy. |
| `data-handling.md` | Supported formats, ingestion pipeline, DuckDB schema conventions. |
| `git-workflow.md` | Branch naming, commit format, PR process. |
| `model-guide.md` | Ollama models, performance, how to add new models. |
| `skill-creation.md` | How to create skills, write SKILL.md, build packages, write evals, run tests. |
| `gotchas.md` | Living document. Things that bit you, workarounds. Append-only with dates. |

### 3.3 knowledge/ (project intelligence)

Three-file invariant — always in system prompt:

| File | Budget | Content |
|------|--------|---------|
| `working.md` | ~800 tokens | What the agent is doing RIGHT NOW |
| `index.md` | ~600 tokens | One-line per wiki page — full catalog |
| `log.md` | ~200 tokens | Last 10 operations (grep-parseable) |

Total: ~1,600 tokens. Everything else retrieved on demand.

### 3.4 ADR format

```markdown
# ADR-NNN: Title

Status: Proposed | Accepted | Superseded | Rejected
Date: YYYY-MM-DD
Supersedes: ADR-NNN (if applicable)

## Context
What is the issue? What forces are at play?

## Decision
What did we decide?

## Consequences
What are the trade-offs? What becomes easier/harder?
```

---

## 4. Skills System

### 4.1 Two-layer architecture

**Layer 1: SKILL.md** (<200 lines) — instruction file the agent reads. Tells it WHAT functions are available, WHEN to use them, and common error recovery patterns. Written in markdown with YAML frontmatter.

**Layer 2: Python packages** (unlimited) — importable libraries the agent uses inside the sandbox. Well-documented functions with type hints, docstrings, parameter validation, and actionable error messages. The agent imports and calls these like any library — it does not rewrite functionality the package already provides.

### 4.2 Skill directory structure

```
backend/app/skills/<skill_name>/
├── SKILL.md                  # Agent reads this (<200 lines)
├── skill.yaml                # Metadata, triggers, dependencies
├── pkg/                      # Agent imports this in sandbox
│   ├── __init__.py           # Public API surface
│   ├── <module>.py           # Implementation (unlimited length)
│   └── viz.py                # Pre-built Altair chart templates
├── references/               # Loaded by agent on demand
│   └── <topic>.md
├── tests/                    # Developer unit tests (pytest)
│   └── test_<module>.py
└── evals/                    # SEALED — never loaded to agent
    ├── eval.yaml             # Eval definitions + assertions
    ├── fixtures/             # Sample datasets
    └── judge.py              # LLM-graded response evaluator
```

### 4.3 skill.yaml

```yaml
name: timeseries
version: "1.0"
description: "Time series analysis, decomposition, forecasting, and diagnostics"
level: 2                     # 1=leaf, 2=composed, 3=orchestrator

parameters:
  <param_name>:
    type: string | int | float | boolean
    required: true | false
    default: <value>
    description: "Clear, self-documenting description"
    examples: ["example1", "example2"]

errors:
  <ERROR_CODE>:
    message: "Template with {placeholders}"
    guidance: "What to do about it with {context}"
    recovery: "Concrete next step"

dependencies:
  requires: [<other_skills>]
  used_by: [<dependent_skills>]
  packages: [<pip_packages>]

observability:
  emit_events: [<event_types>]
  track_metrics: [<metric_names>]
```

### 4.4 SkillError — actionable errors

Every error declared in `skill.yaml` with a template. At runtime:

```python
raise SkillError(
    code="COLUMN_NOT_FOUND",
    context={
        "column": "price",
        "table": "sales",
        "available_columns": ["date", "revenue", "quantity"],
        "suggestions": ["price_usd"]  # difflib.get_close_matches
    }
)
```

The error handler looks up the template from `skill.yaml`, fills it in, and returns:

```
Column 'price' not found in table 'sales'.
Available columns: ['date', 'revenue', 'quantity']. Did you mean: 'price_usd'?
Fix: Change the column name and retry.
```

No raw tracebacks reach the agent. Every error is actionable.

### 4.5 @skill_function decorator

```python
@skill_function(
    name="decompose_seasonal",
    description="Decompose time series into trend, seasonal, and residual",
    emit_events=True,
)
def decompose_seasonal(
    df: pl.DataFrame,
    date_col: str,
    value_col: str,
    period: int | None = None,
    method: Literal["additive", "multiplicative"] = "additive",
) -> DecomposeResult:
```

The decorator handles:
- Wrapping all exceptions into SkillError with context
- Emitting start/end/error events to the event bus
- Recording metrics (duration, input size)
- Validating parameter types before execution

### 4.6 Hierarchy levels

| Level | Role | Example | Can invoke |
|-------|------|---------|-----------|
| 1 | Leaf function | `decompose_seasonal` | Nothing |
| 2 | Composed skill | `timeseries` | Level 1 functions |
| 3 | Orchestrator | `full_analysis` | Level 2 skills |

Never skip levels.

### 4.7 Closed-loop manifest

`manifest.py` tracks the dependency graph. When a skill's interface changes:

```
$ make skill-check

BREAKING: timeseries/pkg/decompose.py
  Function decompose_seasonal: parameter 'period' renamed to 'seasonal_period'
  
  Impact:
  ├── SKILL.md references 'period' (line 34) → update
  ├── tests/test_decompose.py uses 'period=' (lines 12, 28) → update
  ├── modeling/SKILL.md references decompose_seasonal (line 52) → review
  └── wiki/entities/timeseries.md mentions period (line 7) → update

  Run: make skill-fix skill=timeseries
```

### 4.8 Sealed evals

The `evals/` directory is never loaded into the agent's context. The registry explicitly excludes it.

**eval.yaml** defines test cases with:

- **Behavioral assertions** — did the agent call the right functions with right params?
- **Output quality** — does the result contain expected metrics/artifacts?
- **Guardrail assertions** — agent must NOT write code the package already provides
- **Error recovery** — agent must handle errors and retry correctly
- **Qualitative grading** — LLM-judged criteria (explanation quality, workflow coherence)

**Running evals:**

```
$ make skill-eval skill=timeseries

Running evals for: timeseries (4 cases)
[1/4] decompose_basic        PASS (8/8 assertions)
[2/4] decompose_error_recovery PASS (3/3)
[3/4] insufficient_data       PASS (3/3)
[4/4] skill_package_used      PASS (2/2)

RESULT: 16/16 passed · Qualitative: 0.90 avg (threshold: 0.85) ✓
```

**Gate:** CI blocks merge if skill evals fail.

---

## 5. Devtools UI

### 5.1 Overview

Developer mode is a workbench overlay toggled with `Cmd+Shift+D`. It provides full transparency into the agent's operation without leaving the analytical UI.

### 5.2 Tabs

| # | Tab | Purpose | Read/Write |
|---|-----|---------|-----------|
| 1 | **Events** | Real-time stream: tool calls, skill events, sandbox execution, LLM responses, wiki writes, artifact saves | Read-only |
| 2 | **Skills** | Skill registry tree, health indicators, eval pass rates, dependency graph. Quick actions: run evals, reload, check manifest, create new skill | Read + actions |
| 3 | **Config** | Live config editor: model, sandbox limits, packages, wiki settings. Changes take effect immediately. Diff from defaults. Change history. | Read/Write |
| 4 | **Wiki** | Browse LLM wiki pages. Status (confirmed/testing/rejected), cross-references, index. Trigger lint. View working.md. | Read + lint action |
| 5 | **Evals** | Skill eval dashboard. Run evals, see pass/fail per assertion, LLM-judged scores. Compare across iterations. Drill into test transcripts. | Read + run action |
| 6 | **Context** | Context window inspector. Live layer breakdown, token counts, compaction history, timeline chart. | Read-only |

### 5.3 Status bar (always visible)

Even when devtools is closed, the bottom status bar shows:
- DuckDB connection status + table count
- Ollama model status + loaded model
- Wiki page count
- Skills health (N/M passing)
- Context utilization %

---

## 6. Context Window Inspector

### 6.1 Context layers

The agent's context window is divided into layers with different compaction behaviors:

| Layer | Content | Token budget | Compaction |
|-------|---------|-------------|-----------|
| **System** | Role, tools, safety | ~1,640t | Never |
| **L1: Always** | working.md + index.md + log.md | ~1,600t | Never |
| **L2: Skill** | Active SKILL.md | ~500-900t | Swapped when skill changes |
| **Memory** | Wiki entities by relevance | Variable | Rotated — least relevant out |
| **Knowledge** | Skill reference docs | Variable | Evicted first — re-loadable |
| **Conversation** | Messages + tool results | Growing | Oldest summarized first |

### 6.2 Compaction priority

When context utilization hits 80%, compaction runs in this order:

1. **Knowledge references** — evicted first, agent can re-load on demand
2. **Old tool results** — summarized (gist kept, detail lost)
3. **Old conversation turns** — summarized (context preserved)
4. **Memory (wiki pages)** — rotated by relevance score

**Never compacted:**
- System prompt
- L1 (working.md, index.md, log.md)
- L2 (active SKILL.md)
- Current turn

### 6.3 Inspector UI

**Left panel — Live snapshot:** Every layer with token counts, expandable to see individual items.

**Right panel — Compaction history:** Every compaction event showing trigger %, what was removed (with token counts freed), what survived, and before/after totals.

**Bottom — Timeline chart:** Stacked area chart showing context composition over time, with compaction events marked. Layers color-coded to match the snapshot view.

### 6.4 Backend API

```
GET /api/context/{session_id}

Response:
{
  "total_tokens": 12847,
  "max_tokens": 32768,
  "utilization": 0.392,
  "layers": [
    {
      "name": "system",
      "tokens": 1640,
      "chars": 6412,
      "compactable": false,
      "items": [{"name": "system_prompt", "tokens": 1640}]
    },
    {
      "name": "l1_always",
      "tokens": 1612,
      "chars": 6290,
      "compactable": false,
      "items": [
        {"name": "working.md", "tokens": 812},
        {"name": "index.md", "tokens": 588},
        {"name": "log.md", "tokens": 212}
      ]
    },
    ...
  ],
  "compaction_history": [
    {
      "id": 2,
      "timestamp": "2026-04-11T08:38:12Z",
      "trigger_utilization": 0.812,
      "tokens_before": 26607,
      "tokens_after": 12847,
      "tokens_freed": 13760,
      "removed": [...],
      "survived": [...]
    }
  ]
}
```

---

## 7. Migration Mapping

### Files to move

| Current | New | Action |
|---------|-----|--------|
| `src/` | `reference/src/` | Move |
| `web/` | `reference/web/` | Move |
| `mcp-server/` | `mcp/` | Rename |
| `ollama/` | `infra/ollama/` | Move |
| `docker/` | `infra/docker/` | Move |
| `helm/` | `infra/helm/` | Move |
| `grafana/` | `infra/grafana/` | Move |
| `docs/` | `reference/docs/` | Move (CLI docs) |
| `scripts/` | `reference/scripts/` | Move (CLI scripts) |
| `tests/` | `reference/tests/` | Move (CLI tests) |
| `prompts/` | `reference/prompts/` | Move |
| `plans.md` | `knowledge/adr/000-initial-vision.md` | Convert to ADR |
| `agent.md` | `reference/agent.md` | Move |
| `Skill.md` | `reference/Skill.md` | Move |
| `graphify-out/` | `knowledge/graphs/` | Move |
| `package.json` | `reference/package.json` | Move |
| `bun.lock` | `reference/bun.lock` | Move |
| `biome.json` | `reference/biome.json` | Move |
| `tsconfig.json` | `reference/tsconfig.json` | Move |
| `.env.example` | `.env.example` | Keep, update for new structure |

### New directories to create

| Directory | Purpose |
|-----------|---------|
| `backend/` | FastAPI Python backend |
| `frontend/` | React+Vite analytical UI |
| `knowledge/wiki/` | LLM wiki (Karpathy pattern) |
| `knowledge/adr/` | Architecture decision records |
| `docs/` | Project SOPs and guides |
| `scripts/` | Project dev tooling |
| `infra/` | Consolidated infrastructure |
| `reference/` | All read-only material consolidated |

### Root files after migration

```
CLAUDE.md                    # Rewritten for new structure
Makefile                     # Unified commands (make dev, make test, etc.)
docker-compose.yml           # Local dev: backend + frontend + DuckDB + Ollama
.env.example                 # Updated environment template
.gitignore                   # Updated for new structure
```

---

## 8. Makefile Commands

```makefile
# Development
make dev              # Start backend + frontend + Ollama
make backend          # Start backend only
make frontend         # Start frontend only

# Quality
make lint             # Ruff (backend) + ESLint (frontend)
make typecheck        # Mypy (backend) + tsc (frontend)
make test             # Pytest (backend) + vitest (frontend)
make test-backend     # Backend tests only
make test-frontend    # Frontend tests only

# Skills
make skill-check      # Run manifest dependency check
make skill-eval       # Run all skill evals
make skill-eval skill=timeseries  # Run specific skill eval
make skill-fix skill=timeseries   # Auto-fix dependency breakage
make skill-new name=<name>        # Scaffold new skill directory

# Knowledge
make wiki-lint        # Run wiki lint cycle
make graphify         # Regenerate graphify output

# Data
make seed-data        # Load sample datasets into DuckDB

# Infrastructure
make docker-build     # Build Docker images
make docker-up        # Start via docker-compose
```

---

## 9. Future Sub-Projects

These are explicitly out of scope for this spec but will follow as separate design cycles:

1. **Backend agent implementation** — LangGraph graph, tool loop, model integration
2. **Frontend analytical UI** — 4-zone layout, artifact rendering, thinking stream
3. **Sandbox implementation** — Subprocess executor, policy engine, pre-loaded globals
4. **Data pipeline** — Ingestion, DuckDB schemas, dataset registry
5. **Wiki engine** — Ingest/query/lint operations, search
6. **Context management engine** — Token counting, compaction strategies, layer management (directory scaffolded in this spec at `backend/app/context/`, implementation in future spec)
7. **Enterprise features** — Multi-user, sharing, collaboration (future)
