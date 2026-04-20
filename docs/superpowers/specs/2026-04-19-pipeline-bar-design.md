# Pipeline Bar — Knowledge Page Execution Surface

**Status:** approved (user-authorized auto-implementation)
**Date:** 2026-04-19
**Sub-project:** 4 of 5 (DS-Agent shell rebuild)

## Goal

Replace the three drawer-toggle buttons on the Knowledge page toolbar with three primary **execution** actions along the page footer: **INGEST**, **DIGEST**, **MAINTAIN**. Each button runs its backend pipeline phase in-place, shows last-run metadata inline, and opens a review drawer only when human attention is warranted (ingest upload dialog, digest proposals queue, maintain lint report).

This consolidates the knowledge-base lifecycle into a single, glanceable command surface matching the power-user aesthetic: structure, density, visible state.

## Non-Goals

- SSE progress streaming (use synchronous POST + toast; add SSE later if needed)
- Auto-apply safe digest actions (still require human approval; button reports count)
- Checkpoint / replay of partial pipeline state
- Removing the Graph viewer — it stays reachable via the top toolbar

## Users & Context

Power users (MLE / data scientists / quants) operating the DS-Agent. They want to:
1. Drop a file/URL and watch it land.
2. Trigger cleanup passes on demand and see how much the graph moved.
3. Run nightly housekeeping when they feel the KB getting stale.

Today's three drawer-toggle buttons conflate *viewing* (opening a panel) with *executing* (running work). The new bar separates the two: execution is primary and footer-placed; drawers open contextually on completion.

## Surface

```
┌─ KNOWLEDGE ─────────────────────────────────────────────┐
│ [Graph]                                          (top toolbar)
│                                                          │
│  ┌──────────────────────┬───────────────────────────┐   │
│  │ WikiTree             │ WikiArticle               │   │
│  │ (260px)              │                           │   │
│  └──────────────────────┴───────────────────────────┘   │
│                                                          │
│ ┌─── PIPELINE ──────────────────────────────────────┐   │
│ │  ⬆ INGEST         ⟳ DIGEST         ✓ MAINTAIN    │   │
│ │  2m ago · 14 new  17m ago · 3 new   1h ago · 0 err│   │
│ └───────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

Footer height: `56px` fixed, aligned to design tokens. Monospace label, sans status line.

## Component Design

### `PipelineBar`
Footer component with three buttons (`PipelineAction`). Fetches `/api/sb/pipeline/status` on mount + after each execution.

### `PipelineAction`
Props:
```ts
interface PipelineActionProps {
  phase: 'ingest' | 'digest' | 'maintain'
  label: string
  icon: ReactNode
  status: PipelinePhaseStatus
  onClick: () => void | Promise<void>
}
```
States:
- **idle** — shows last-run timestamp + last-run count summary
- **running** — shows spinner, disabled, label changes to `RUNNING…`
- **done** — flashes last result for 2s, then falls back to idle with fresh counts

### `pipeline-store.ts` (Zustand)
```ts
interface PipelineStore {
  ingest: PhaseState
  digest: PhaseState
  maintain: PhaseState
  refreshStatus: () => Promise<void>
  runIngest: (payload: IngestPayload) => Promise<IngestResult>
  runDigest: () => Promise<DigestResult>
  runMaintain: () => Promise<MaintainResult>
}

interface PhaseState {
  status: 'idle' | 'running' | 'done' | 'error'
  lastRunAt: string | null          // ISO timestamp
  lastResult: PhaseResultSummary | null
  errorMessage: string | null
}
```

Per-phase result summaries, all narrow typed:
```ts
interface IngestResultSummary { sourcesAdded: number }
interface DigestResultSummary { entries: number; emitted: boolean; pending: number }
interface MaintainResultSummary { lintErrors: number; lintWarnings: number; openContradictions: number; staleAbstracts: number }
```

## Backend Changes

### New routes

**`GET /api/sb/pipeline/status`**
Returns aggregate last-run metadata. Response schema:
```json
{
  "ok": true,
  "ingest": { "last_run_at": "...", "result": { "sources_added": 14 } | null },
  "digest": { "last_run_at": "...", "result": { "entries": 3, "emitted": true, "pending": 5 } | null },
  "maintain": { "last_run_at": "...", "result": { "lint_errors": 0, "lint_warnings": 2, ... } | null }
}
```

**`POST /api/sb/maintain/run`**
Invokes `MaintainRunner(cfg).run(build_digest=False)` and returns the report as JSON:
```json
{
  "ok": true,
  "result": {
    "lint_errors": 0, "lint_warnings": 2, "lint_info": 0,
    "open_contradictions": 0,
    "stale_abstracts": [],
    "analytics_rebuilt": true,
    "habit_proposals": 0,
    "fts_bytes_before": 123, "fts_bytes_after": 120,
    "duck_bytes_before": 456, "duck_bytes_after": 450
  }
}
```

### State file
All three phase endpoints write their outcome to `{cfg.sb_dir}/.state/pipeline.json`:
```json
{
  "ingest": { "last_run_at": "2026-04-19T20:44:10Z", "result": {...} },
  "digest": { "last_run_at": "2026-04-19T20:50:02Z", "result": {...} },
  "maintain": { "last_run_at": "2026-04-19T21:00:15Z", "result": {...} }
}
```
`pipeline/status` reads this file. Writes are best-effort; failures don't mask the phase outcome.

### Touchpoints on existing routes
- `POST /api/sb/ingest` + `/ingest/upload` — on success, update `.state/pipeline.json` ingest slot.
- `POST /api/sb/digest/build` — on success, update digest slot (append `pending` by reading pending queue after build).

## Files Touched

### New
- `backend/app/api/sb_pipeline.py` — new router for `/pipeline/status` + `/maintain/run`
- `backend/app/tools/sb_pipeline_state.py` — helpers for reading/writing `.state/pipeline.json`
- `backend/tests/api/test_sb_pipeline.py`
- `frontend/src/lib/pipeline-store.ts`
- `frontend/src/lib/__tests__/pipeline-store.test.ts`
- `frontend/src/components/pipeline/PipelineBar.tsx`
- `frontend/src/components/pipeline/PipelineAction.tsx`
- `frontend/src/components/pipeline/__tests__/PipelineBar.test.tsx`

### Modified
- `backend/app/api/sb_api.py` — add state-write hooks on ingest + digest routes
- `backend/app/main.py` (or wherever routers register) — mount new pipeline router
- `frontend/src/sections/KnowledgeSurface.tsx` — replace Ingest/Digest toolbar toggles with Graph-only toolbar; add `PipelineBar` as footer; existing drawers still open on completion
- `frontend/src/lib/surfaces-store.ts` — drop ingest/digest from `KnowledgeDrawer` union (keep graph); drawers now triggered by pipeline store on completion

## Interaction Flow

**INGEST** — click opens the existing `IngestPanel` drawer (path/URL/upload form). Submit posts to `/api/sb/ingest/upload`; pipeline store updates ingest slot; drawer closes on success; button flashes `+1 source`.

**DIGEST** — click directly posts `/api/sb/digest/build` (no prior drawer). On response, if `entries > 0`, opens the `DigestPanel` drawer showing the new pending entries. Button flashes `N entries`.

**MAINTAIN** — click directly posts `/api/sb/maintain/run`. No drawer unless `lint_errors > 0`, in which case a `MaintainReportDrawer` opens showing the rule violations. Button flashes `✓ clean` or `N errors`.

## Keyboard

- `G I` → Ingest (same mnemonic family as existing `G G` graph-shortcuts pattern)
- `G D` → Digest
- `G M` → Maintain
- Registered via existing `lib/shortcuts.ts` global map.

## Telemetry

Each phase endpoint already writes a `meta.json` sidecar. Extend:
- Maintain writes `{cfg.sb_dir}/maintain/YYYY-MM-DD.meta.json` with `duration_ms`, outcome, report summary.

## Error Handling

- Backend: each phase endpoint catches top-level exceptions and returns a structured error envelope `{ok: false, phase: "...", error: "..."}` with HTTP 500 for server failures; 400 for validation.
- Frontend: phase store sets `status: 'error'`, surfaces `errorMessage` as a destructive toast; button enters `error` visual state (red ring) for 10s before reverting to `idle`.

## Testing

Backend:
- `test_sb_pipeline.py::test_status_empty_state` — fresh KB, all phases `null`
- `test_sb_pipeline.py::test_status_after_ingest` — seed ingest state, verify slot
- `test_sb_pipeline.py::test_maintain_run_ok` — invokes runner with a fake cfg, asserts shape
- `test_sb_pipeline.py::test_maintain_run_handles_exception` — ensures 500 envelope

Frontend:
- `pipeline-store.test.ts` — mocks fetch for each phase, verifies state transitions
- `PipelineBar.test.tsx` — renders three buttons, disables during `running`, shows last-run

No visual-regression E2E until the component lands; Playwright flow can follow.

## Open Questions — resolved

- **Should digest auto-apply safe entries?** → No, not yet. Button only builds; user still approves in drawer. Revisit after three-button UX settles.
- **Should Graph move to the footer too?** → No. Graph is a *viewer*, not a *pipeline stage*. It stays as a top toolbar toggle (currently on `KnowledgeSurface`).
- **SSE for progress?** → Deferred. Synchronous POST is fine for now; maintain typically completes in under 10 seconds on a mid-size KB.

## Accessibility

- Footer is a `<nav aria-label="Pipeline">` landmark with three `<button>` elements.
- Each button's accessible name includes phase + status (e.g., "Digest, last run 17 minutes ago, 3 new entries").
- `aria-busy="true"` during `running`; `role="status"` live region announces phase completion.
- Kbd hints rendered as `<kbd>` with `aria-hidden`; action name in the accessible label.
- Focus ring follows existing `focus-ring` token.

## Visual Spec

- Footer row: `h-14`, `border-t border-line`, `bg-bg-0`
- Each action: `flex-1`, vertical padding `py-2`, horizontal `px-4`, divider `border-l border-line` between actions
- Icon `size={16}`, label `font-mono uppercase tracking-wide text-[12px]`, status line `text-[11px] text-fg-2`
- Running state uses existing `animate-pulse` keyframe and disabled opacity token
- Done-state flash uses accent color `text-acc` for 2000ms before decay
