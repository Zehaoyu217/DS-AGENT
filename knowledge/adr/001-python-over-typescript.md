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
