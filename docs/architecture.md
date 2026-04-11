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
