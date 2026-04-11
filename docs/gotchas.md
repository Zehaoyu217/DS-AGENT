# Gotchas

Known pitfalls, workarounds, and things that will bite you. Append-only with dates.

---

## [2026-04-11] reference/ is read-only

The `reference/` directory contains the original Claude Code CLI source. Do not modify files there. If you need to study a pattern, read it and reimplement in `backend/` or `frontend/`.

## [2026-04-11] Skill evals are sealed

The `evals/` directory inside each skill is never loaded into the agent's context. This is by design — the agent must not know what the eval assertions check for.
