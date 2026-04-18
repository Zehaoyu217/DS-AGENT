# Post-v2 Coherence Umbrella

**Date:** 2026-04-18
**Status:** Active
**Scope:** 10 post-v2 improvements shipped as a single coherent sweep, reusing patterns established by the sb-bridge work rather than as 10 isolated bolt-ons.

## Theme

The v2 digest pipeline + bridge shipped the plumbing. This wave makes the product **legible, observable, and extensible** — you can see what the agent is doing, what it costs, where it fails, and where the knowledge is drifting.

## Shared conventions

Every item below MUST reuse these patterns.

### 1. Right-rail drawer pattern

All new panels follow `frontend/src/components/digest/DigestPanel.tsx` exactly:
- `position: fixed; right: 0; top: 0; bottom: 0; width: 360px`
- `background: #09090b`, `border-left: 1px solid #27272a`
- `font-family: 'JetBrains Mono'`, `font-size: 12px`
- Header with small-caps 10px title + meta line + close button
- Orange (`#e0733a`) reserved for active-state and unread/error counts
- Zustand store per panel at `frontend/src/lib/<name>-store.ts`

### 2. Topbar badge pattern

Each panel toggle lives in the fixed top-right stack under the DIGEST button:
- `.topbar-btn` class (monospace, 10px caps, `#09090b` bg, `#27272a` border)
- `·` separator + count when unread > 0
- Hover/active: `border-color: #e0733a; color: #e0733a`

One component (`TopbarButton.tsx`) — defined in Wave A, reused everywhere.

### 3. `/api/sb/*` route prefix

All second-brain-touching routes live under `/api/sb/…`. New routes from this sweep:
- `POST /api/sb/digest/build` (Wave A, item #2)
- `GET /api/sb/digest/pending` (Wave A)
- `GET /api/sb/memory/session/{id}` (Wave A, item #6)
- `GET /api/sb/stats` (Wave A, item #7 — wraps sb_stats handler)
- `GET /api/sb/digest/costs?date=…` (Wave B, item #3)
- `GET /api/skills/telemetry` (Wave B, item #9 — non-sb prefix)
- `GET /api/sb/graph?center=…` (Wave C, item #1)
- `POST /api/sb/ingest` (Wave C, item #5)
- `GET /api/sb/drift` (Wave D, item #10)

Every route returns `404` when `SECOND_BRAIN_ENABLED=False` (except skills telemetry).

### 4. Telemetry sidecar format

Digest passes and skill invocations write to identically-shaped sidecars:

```
{repo}/digests/YYYY-MM-DD.meta.json     # pass metrics
{repo}/telemetry/skills.jsonl           # skill invocations (append-only)
{repo}/telemetry/drift/YYYY-MM-DD.json  # drift snapshot
```

Shape for per-record telemetry:

```json
{
  "timestamp": "2026-04-18T12:00:00Z",
  "actor": "reconciliation_pass | skill:time_series_methodology | ...",
  "duration_ms": 1234,
  "input_tokens": 8000,
  "output_tokens": 420,
  "cost_usd": 0.0321,
  "outcome": "ok | error",
  "detail": { ... }  // per-actor payload
}
```

### 5. Failure mode — gate and degrade

New code never fatally depends on the KB. If `SECOND_BRAIN_ENABLED=False`:
- Routes return 404
- Panels render empty state with muted subtitle ("knowledge base disabled")
- Hooks return None
- Telemetry writes still work (they're local disk, not KB-dependent)

### 6. TDD + conventional commits

Every task: failing test → minimal impl → commit. Commit prefix `feat(coherence):` for this sweep so the roll-up is filterable.

## Item → wave mapping

| # | Item | Wave | Shared infra used |
|---|------|------|-------------------|
| 2 | Pending proposals UX | A | drawer pattern, sb route prefix |
| 6 | Memory panel in devtools | A | ContextInspector extension |
| 7 | Health widget | A | drawer + topbar badge |
| 3 | Digest pass cost/latency | B | telemetry sidecar |
| 9 | Skills usage dashboard | B | telemetry sidecar + drawer |
| 1 | Graph viz UI | C | drawer + sb route |
| 5 | Ingest UX | C | drawer + sb route |
| 4 | Playwright E2E harness | D | — |
| 8 | GAN loop ↔ trace corpus | D | — |
| 10 | Graph↔wiki drift detection | D | telemetry sidecar + sb route |

## Non-goals for this sweep

- Any v3 retrieval rework.
- Multi-user / auth.
- Mobile layout.
- Net-new skill creation beyond instrumenting existing skills.
- Rebuilding the chat surface.

## Success criterion

After all 10 items ship, a user opening the app cold should be able to, without leaving the right rail:
1. See pending KB decisions with unread count.
2. See last session's memory recall layer.
3. See today's digest cost + health score.
4. See which skills have been used today and their latencies.
5. Browse the knowledge graph from any claim.
6. Drop a file/URL to ingest without using the CLI.

That is "ties together" operationalized.
