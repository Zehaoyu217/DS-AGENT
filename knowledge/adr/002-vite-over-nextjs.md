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
