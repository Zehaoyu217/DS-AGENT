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
- **Changelog:** every main update lands an entry in `docs/log.md` under `[Unreleased]` — see that file's header for the policy and entry shape.

## Changelog Policy

`docs/log.md` is the single source of truth for notable changes. **You must update it** before marking a task complete whenever the change is one of:

- A `feat:` commit that touches user-visible behavior or adds a capability
- A breaking change to a public interface (skill signature, tool registration, API schema, config schema)
- A migration, rename, or removal that affects existing callers
- A security, correctness, or data-loss fix on a critical path

Pure refactors, test-only commits, and doc-only commits do not require an entry unless they change observable behavior.

## Current State

Read `knowledge/wiki/working.md` for what's in progress.

## Deeper Context

- Architecture decisions: `knowledge/adr/`
- Development setup: `docs/dev-setup.md`
- Testing guide: `docs/testing.md`
- Skill creation: `docs/skill-creation.md`
- Known gotchas: `docs/gotchas.md`
- Changelog: `docs/log.md`
