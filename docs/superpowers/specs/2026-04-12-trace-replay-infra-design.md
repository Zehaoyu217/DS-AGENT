# Trace-Replay Infrastructure & DevTools Selection — Design

**Date:** 2026-04-12
**Status:** Approved (brainstorm complete)
**Related:** `docs/superpowers/specs/2026-04-12-eval-failure-sop-design.md`, `docs/superpowers/plans/2026-04-12-eval-failure-sop.md`

---

## Problem

The Eval-Failure SOP ships with three DevTools surfaces — **Judge Variance**, **Prompt Inspector**, **Compaction Timeline** — but they render against stub endpoints. The DevTools panel has `selectedTraceId` and `selectedStepId` hardcoded to `null`, so the tabs only show "Select a trace from the Session Replay tab" placeholders. There is no machinery that captures what actually happened during an agent run, and no way to select a captured run from the UI.

This spec defines the **trace-replay infrastructure**: a capture pipeline that records the irreducible events of an agent run into a per-session YAML file, a set of REST endpoints that serve derived diagnostic views from that file, and the frontend wiring (row-click selection + URL deep-links + step dropdown) that makes the three stub tabs functional.

## Goals

- Every agent run can optionally produce a self-contained trace file that is sufficient to reconstruct Judge Variance, Prompt Inspector, and Compaction Timeline views without re-running the agent.
- Trace capture is **configurable** (`always` vs `on_failure`), has **zero perf impact on the happy path**, and **never breaks the agent** even if the recorder fails.
- Trace format is **versioned, immutable, and self-describing**, so old traces remain readable as capture points evolve.
- DevTools has a working trace selection flow: click a row in Session Replay to activate a trace across all dependent tabs; URL deep-links survive reload and are shareable.
- Architecture is **future-proof**: an event bus lets future consumers (Scope C diagnostic harness, live-tail DevTools, metrics collectors) subscribe without further refactoring.

## Non-Goals

- Full-replay determinism (deterministic re-play of exact LLM responses). Judge variance uses cached N runs with a live-refresh escape hatch; other views are served from captured data.
- Cross-session correlation or aggregate analytics (each trace is a self-contained artifact).
- Retention automation (trace accumulation is cleaned manually via a CLI / Make target).
- Scope C diagnostic harness that mutates the agent to find root causes — separate brainstorm.

---

## Scope

- **Trace subsystem** — event bus, event models, recorder, store, retention CLI
- **REST API** — `/api/trace/*` endpoints replacing the stub endpoints in `sop_api.py`
- **DevTools wiring** — selection store + URL sync + row-click + step dropdown + timeline bar click

---

## Architecture

Trace capture is an **event-bus subsystem** decoupled from the SOP module. The agent's `LlmClient`, `ToolRunner`, and `ContextManager` publish events to a sync in-process bus. A `TraceRecorder` subscriber buffers events in-memory during a run and writes a single YAML file atomically at finalize. DevTools reads derived views from that file through a dedicated REST router.

```
┌─── Agent Loop ──────────────────────────────────────────────┐
│                                                             │
│  LlmClient ───────┐       ToolRunner ──┐    ContextMgr ──┐  │
│   wraps Anthropic │        dispatches  │     compaction, │  │
│   messages.create │        tool calls  │     scratchpad  │  │
│                   ▼                    ▼                 ▼  │
│                   ─────── trace.emit(event) ──────────────  │
│                                  │                          │
└──────────────────────────────────┼──────────────────────────┘
                                   │ (event bus, sync pub/sub)
                                   ▼
                        ┌─────────────────┐
                        │  TraceRecorder  │   (subscriber)
                        │  buffers events │
                        └─────────────────┘
                                   │ on session end
                                   │ (always OR on_failure per TRACE_MODE)
                                   ▼
                         traces/<session_id>.yaml
                         (summary + judge_runs + events,
                          trace_schema_version: 1)

DevTools  ───  GET /api/trace/traces/<id>/...  ───▶  TraceStore (read-only load)
                                                      │
                                                      ▼
                                                  JudgeReplayer   (cached N=5 + live ?refresh=1)
                                                  PromptAssembler (reads captured sections)
                                                  TimelineBuilder (groups events by turn)
```

**Key architectural properties:**

- **Sync, in-process pub/sub.** No threads, no async, no queue — the agent loop is synchronous and publish is a direct list append under a module-level subscriber list. Future consumers can subscribe without changing publishers.
- **Finalize-time write only.** The recorder never touches disk mid-session. If the process crashes, no trace is written (acceptable — crashes are rare and SOP already captures them via error reports).
- **Trace package has zero dependency on `sop/`.** The SOP session record links outward via `trace_id` only; traces are a standalone diagnostic asset.
- **Trace files are immutable once written.** Atomic write through tempfile + rename; no partial files.
- **Schema is versioned.** `trace_schema_version: 1` on every file; future shape changes bump the version and add a reader adapter rather than rewriting old files.

---

## Data Contracts

### Event model

All events are Pydantic v2 models with `ConfigDict(frozen=True)`. Every event has `seq: int` (monotonic, assigned by bus), `timestamp: str` (ISO8601), and `kind: str`. Event-specific fields:

| Kind | Fields |
|---|---|
| `session_start` | `session_id`, `started_at`, `level`, `level_label`, `input_query` |
| `llm_call` | `step_id` (e.g. `s1`), `turn`, `model`, `temperature`, `max_tokens`, `prompt_text`, `sections: list[PromptSection]`, `response_text`, `tool_calls: list[dict]`, `stop_reason`, `input_tokens`, `output_tokens`, `cache_read_tokens`, `cache_creation_tokens`, `latency_ms` |
| `tool_call` | `turn`, `tool_name`, `tool_input: dict[str, object]`, `tool_output: str`, `duration_ms`, `error: str \| None` |
| `compaction` | `turn`, `before_token_count`, `after_token_count`, `dropped_layers: list[str]`, `kept_layers: list[str]` |
| `scratchpad_write` | `turn`, `key`, `value_preview: str` (truncated) |
| `final_output` | `output_text`, `final_grade: Grade \| None`, `judge_dimensions: dict[str, float]` |
| `session_end` | `ended_at`, `duration_ms`, `outcome: Literal["ok", "error"]`, `error: str \| None` |

`PromptSection` is `{source: str, lines: str, text: str}` — matches the existing frontend `PromptInspector` contract.

**Type provenance.** `Grade` (`Literal["A", "B", "C", "F"]`) is currently defined in `backend/app/sop/types.py`. Since the trace package has zero dependency on `sop/`, the trace module defines its own local `Grade` alias with identical definition. The duplication is trivial; if the SOP type later moves to a shared `backend/app/common/` module, both sides import from there.

`step_id` is `s{n}` where n is the 1-based LLM-call sequence number. The `LlmClient` wrapper authors and attaches the step_id immediately before publishing the `llm_call` event, so step_ids are monotonic and gap-free.

### Trace file format

```yaml
trace_schema_version: 1
summary:
  session_id: 2026-04-12-eval-level3-001
  started_at: "2026-04-12T08:42:13Z"
  ended_at:   "2026-04-12T08:42:55Z"
  duration_ms: 42300
  level: 3
  level_label: eval-level3
  turn_count: 7
  llm_call_count: 9
  total_input_tokens: 48210
  total_output_tokens: 3104
  outcome: ok
  final_grade: F
  step_ids: [s1, s2, s3, s4, s5, s6, s7, s8, s9]
  trace_mode: on_failure
  judge_runs_cached: 5

judge_runs:
  - {dim_accuracy: 0.80, dim_completeness: 0.70, dim_reasoning: 0.85, ...}
  - {dim_accuracy: 0.65, dim_completeness: 0.75, dim_reasoning: 0.80, ...}
  - ... (N=5 total)

events:
  - {seq: 1, timestamp: "2026-04-12T08:42:13Z", kind: session_start, ...}
  - {seq: 2, timestamp: "2026-04-12T08:42:15Z", kind: llm_call, step_id: s1, turn: 1,
     prompt_text: "...", sections: [{source: SYSTEM_PROMPT, lines: "1-50", text: "..."}, ...],
     response_text: "...", input_tokens: 2314, output_tokens: 412, ...}
  - {seq: 3, timestamp: "2026-04-12T08:42:17Z", kind: tool_call, turn: 1,
     tool_name: read_file, ...}
  - ...
  - {seq: N, timestamp: "2026-04-12T08:42:55Z", kind: session_end, outcome: ok}
```

**Summary provenance:** written once by the recorder at finalize — not recomputed on read. Events are the source of truth; summary is authoritative derived data captured at the moment the run completed. If a summary and events ever disagree, events win (DevTools detail views read events directly; summary is only used for list views and fast filtering).

**Truncation:** fields larger than `TRACE_MAX_EVENT_SIZE_BYTES` (default 10KB) are truncated with a `__truncated: true` marker at write time. In-memory values stay full during the run so the finalize-time judge replay sees complete `final_output`; truncation only affects on-disk storage and post-run DevTools views.

**Conflicts** (for `PromptInspector`): computed on read by `PromptAssembler` using a byte-range overlap heuristic — two sections that share a `source` and have overlapping `lines` ranges are flagged as a conflict. Semantic duplication detection is deferred.

---

## Backend Implementation

### File layout

```
backend/app/trace/
  __init__.py
  bus.py                # sync pub/sub singleton
  events.py             # Pydantic event models + PromptSection
  recorder.py           # subscriber, buffers events, finalizes to disk
  store.py              # read-only load/list traces with path-traversal guard
  assembler.py          # PromptAssembler — reads sections, detects conflicts
  timeline.py           # TimelineBuilder — groups events by turn
  judge_replay.py       # JudgeReplayer — cached + live
  retention.py          # CLI: --clear-all, --older-than, --grade

backend/app/api/trace_api.py   # FastAPI router, prefix=/api/trace

backend/tests/trace/
  test_bus.py
  test_events.py
  test_recorder.py
  test_store.py
  test_assembler.py
  test_timeline.py
  test_judge_replay.py
  test_retention.py
  test_trace_api.py
  test_integration.py            # synthetic agent run → trace file round-trip
```

### Event bus

Module-level singleton. Sync `publish(event)` assigns `seq` via a monotonic counter, then calls each subscriber in order. `subscribe(fn)` appends a callback. `reset()` clears subscribers and counter (test-only). No thread safety required — agent loop is synchronous.

Publish is a no-op when there are no subscribers (tracing disabled).

### Recorder

Constructed at session start with `(session_id, trace_mode, output_dir, judge_runner=None)`. Subscribes to the bus. `on_event` appends to an in-memory list.

`finalize(final_grade)` decides whether to write based on `trace_mode`:
- `always` → write unconditionally
- `on_failure` → write iff `final_grade not in {"A", "B"}` (treating None and error outcomes as failure too)

Finalize writes `{trace_schema_version, summary, judge_runs, events}` to `traces/<session_id>.yaml` via atomic tempfile + rename. If the write raises, finalize catches the exception, logs it to stderr, and returns `None` — tracing failures never raise into the agent loop.

### Wiring points

- `backend/app/agent/llm_client.py` — wrap `messages.create`, emit `llm_call` with assembled prompt + section metadata (context manager provides sections alongside the assembled text).
- `backend/app/agent/tool_runner.py` — wrap dispatch, emit `tool_call`.
- `backend/app/agent/context_manager.py` — two explicit `bus.publish(...)` sites for `compaction` and `scratchpad_write` events.
- Agent loop entry/exit — emit `session_start`, `final_output`, `session_end`.

### Store

`list_traces(traces_dir)` reads the `summary` block from each YAML and returns `list[TraceSummary]`. `load_trace(traces_dir, trace_id)` loads the full file. Both validate `trace_id` against `_TRACE_ID_RE = r"^[A-Za-z0-9_-]+$"` before touching the filesystem.

### Retention CLI

```bash
uv run python -m app.trace.retention --clear-all
uv run python -m app.trace.retention --older-than 30d
uv run python -m app.trace.retention --grade A,B     # keep only failures
```

Exposed via `make clean-traces` in the root Makefile.

---

## API

**Router:** `backend/app/api/trace_api.py`, `prefix="/api/trace"`, mounted in `backend/app/api/__init__.py`.

### `GET /api/trace/traces`

List trace summaries. Returns `{"traces": [TraceSummary, ...]}`.

### `GET /api/trace/traces/{trace_id}`

Full trace (`summary + judge_runs + events`). 400 on invalid id, 404 on missing.

### `GET /api/trace/traces/{trace_id}/prompt/{step_id}`

```json
{"sections": [{"source": "SYSTEM_PROMPT", "lines": "1-50", "text": "..."}, ...],
 "conflicts": [{"source_a": "rules.md", "source_b": "rules.md", "overlap": "100-150"}]}
```

Backend finds the `llm_call` event with matching `step_id`, returns its captured sections, runs conflict detection. 404 if `step_id` not in the trace. `step_id` validated against `_STEP_ID_RE = r"^s\d+$"`.

### `GET /api/trace/traces/{trace_id}/timeline`

```json
{"turns": [{"turn": 1, "layers": {"system": 2400, "scratchpad": 0, "tools": 800}}, ...],
 "events": [{"turn": 1, "kind": "compaction", "detail": "dropped 3 layers, -4200 tokens"}, ...]}
```

Grouped by `turn` from event stream. 200 with empty arrays if the trace has no turn events (edge, not an error).

### `GET /api/trace/traces/{trace_id}/judge-variance?refresh=0&n=5`

Default (`refresh=0`): serves cached `judge_runs` from the trace file.

With `refresh=1`: re-runs the judge live against captured `final_output`, `temperature=0.7`, N runs. Requires `ANTHROPIC_API_KEY` — returns 503 if missing.

```json
{"variance": {"accuracy": 0.12, "completeness": 0.08, ...},
 "threshold_exceeded": ["accuracy"],
 "n": 5,
 "source": "cached" | "live"}
```

Threshold default `0.10` (`JUDGE_VARIANCE_THRESHOLD` env).

### `GET /api/trace/traces/{trace_id}/events?kind=llm_call`

Raw filtered event stream. Optional `kind` query param. Returned unmodified — no derivation. Escape hatch for Scope C and custom DevTools views. Query params that fail validation return 400.

### Error model

- 400 — invalid `trace_id` or `step_id` pattern
- 404 — trace or step not found
- 500 — caught `ValueError` / `pydantic.ValidationError` / `FileNotFoundError` with clean body (no traceback leak, same hardening pattern as `sop_api.py`)
- 503 — live judge replay requested without API key

### Migration from existing SOP endpoints

Phased, backward-compatible:
1. Ship the trace subsystem and new `/api/trace/*` endpoints; existing `sop_api.py` stubs keep working untouched.
2. Replace the three stub handlers in `sop_api.py` with thin forwarding shims that call the `trace_api` handlers directly (same URL, same response shape, new backing).
3. Flip `frontend/src/devtools/sop/api.ts` to hit `/api/trace/*` directly.
4. Delete the SOP shims; old URLs no longer served.

---

## DevTools Wiring

### Store (`frontend/src/stores/devtools.ts`)

```ts
interface DevtoolsState {
  isOpen: boolean
  activeTab: /* existing union */ | 'sop-sessions' | 'sop-judge' | 'sop-prompt' | 'sop-timeline'
  selectedTraceId: string | null
  selectedStepId: string | null
  setActiveTab: (t: ActiveTab) => void
  setSelectedTrace: (traceId: string | null) => void   // also clears selectedStepId
  setSelectedStep: (stepId: string | null) => void
}
```

### URL sync (`frontend/src/devtools/sop/useSelectionUrlSync.ts`)

Custom hook:
- On mount: parses `?trace=<id>&step=<id>` and calls `setSelectedTrace/Step`.
- Subscribes to the store; on change calls `history.replaceState(null, '', url)` — `replaceState` (not `pushState`) to avoid bloating browser history during debugging sessions.
- Invoked once from `DevToolsPanel` so the sync is active whenever DevTools is open.

### `SessionReplay.tsx` — row click wires selection

- Each row gets `onClick={() => setSelectedTrace(session.trace_id)}` and `onKeyDown` for Enter/Space (keyboard accessibility).
- Selected row: `aria-selected="true"`, accent left-border (`.sop-row--selected`, accent color `#818cf8`).
- Empty state: `"No sessions yet. Run eval with TRACE_MODE=always make eval to populate."`
- If `session.trace_id` is absent (old session, pre-trace-subsystem), the row is non-interactive and shows a `(no trace)` label next to the bucket.

### `PromptInspector.tsx` — step selection via dropdown

- New top row: `<select>` populated from `trace.summary.step_ids`. The component fetches `GET /api/trace/traces/{id}` once on mount and caches the summary locally.
- `onChange={e => setSelectedStep(e.target.value)}`.
- If the store already has a `selectedStepId` matching one of the step_ids, dropdown defaults to it; otherwise it defaults to the first step and calls `setSelectedStep` so the URL stays in sync.
- Below the dropdown: existing section rendering, unchanged.

### `CompactionTimeline.tsx` — bars become clickable

- Each turn's bar stack wraps in `<button>` with `aria-label="Select turn N"`. `onClick` picks the first step_id whose `llm_call` event has that `turn` number and calls `setSelectedStep(stepId)`.
- If the turn has no `llm_call` events (e.g. a compaction-only turn), the button is rendered with `disabled` and a dimmed cursor — user falls back to the dropdown.
- Selected turn: accent outline.
- Secondary selection path — dropdown stays the primary step picker.

### `DevToolsPanel.tsx` — remove hardcoded nulls

```tsx
// BEFORE:
const [selectedTraceId] = useState<string | null>(null)
const [selectedStepId] = useState<string | null>(null)

// AFTER:
const { selectedTraceId, selectedStepId } = useDevtoolsStore()
useSelectionUrlSync()
```

Existing placeholder branches (`<div className="sop-empty">Select a trace...</div>`) stay — they fire correctly when selection is null.

### Deep-link example

`https://localhost:5173/?trace=2026-04-12-eval-level3-001&step=s4` opens DevTools → `sop-prompt` tab auto-populated with step 4's prompt assembly. (`activeTab` is still store-only; URL sync is scoped to trace + step.)

### Styling

Add `.sop-row--selected` (accent left-border). Keep existing `.sop-empty`. No new global styles.

---

## Error Handling (design-level rules)

- **Recorder finalize failure** — caught, logged to stderr, `finalize` returns `None`. Never raises into the agent loop.
- **Bus publish with no subscribers** — no-op.
- **Corrupted trace YAML** — store raises `ValueError`; API catches and returns 500 with clean body.
- **Invalid IDs** — regex validation, 400 response.
- **Missing trace file** — 404.
- **Live judge replay without API key** — 503.
- **Oversize fields** — truncated at write with `__truncated: true` marker.
- **Empty trace** (no events) — list endpoints return empty arrays with 200; individual-step endpoints return 404 if the requested step_id isn't present.

---

## Configuration

All env vars documented in `.env.example` and `README.md`.

| Var | Default | Purpose |
|---|---|---|
| `TRACE_ENABLED` | `1` | Master off-switch for prod/CI |
| `TRACE_MODE` | `on_failure` | `always` or `on_failure` |
| `TRACE_DIR` | `traces/` | Output directory for trace YAML files |
| `TRACE_MAX_EVENT_SIZE_BYTES` | `10240` | Truncation threshold for large fields |
| `JUDGE_VARIANCE_THRESHOLD` | `0.10` | Flag dimensions with variance above this |
| `JUDGE_VARIANCE_N` | `5` | Number of judge runs at finalize |

---

## Testing Strategy

| Layer | Framework | Coverage | Approach |
|---|---|---|---|
| Event models | pytest | 100% | Pydantic validation, frozen, schema versioning round-trip |
| Bus | pytest | 100% | Pub/sub fan-out, seq monotonicity, subscriber reset |
| Recorder | pytest + `tmp_path` | ≥95% | `trace_mode` gating (always/on_failure × grade), atomic write, truncation, finalize idempotency, exception swallowing |
| Store | pytest + `tmp_path` | ≥95% | list + load, path-traversal regex, corrupted YAML → clean error |
| Assembler | pytest | ≥90% | Section pass-through, conflict detection heuristic (overlapping ranges) |
| Timeline builder | pytest | ≥90% | Turn grouping, event classification, empty trace edge |
| Judge replayer | pytest + monkeypatched judge | ≥90% | Cached path, live path with mocked Anthropic, missing-key 503 |
| `trace_api.py` | pytest + `TestClient` + env overrides | ≥90% | Every endpoint × every error code (400/404/500/503) |
| Retention CLI | pytest + `tmp_path` | ≥90% | Each flag (`--clear-all`, `--older-than`, `--grade`) |
| Agent wire-up integration | pytest | critical path | Synthetic agent run publishes expected event sequence; recorder produces a trace file that round-trips through store and assembler |
| Frontend store | vitest | ≥90% | `setSelectedTrace` clears stepId; URL sync hook reads and writes `?trace`/`?step` |
| Frontend components | vitest + RTL | ≥85% | Row click → store update; dropdown → store update; URL deep-link hydrates store on mount; `.sop-row--selected` applied on selection |
| Frontend api.ts | vitest | 100% | Fetch contract against mocked `/api/trace/*` endpoints |

Overall 80% minimum per project rule. TDD throughout — each task writes the failing test first.

---

## Integration

- `backend/app/sop/types.py` — add `trace_id: str | None = None` to `SOPSession`. **ID convention:** when an SOP session runs alongside trace capture, the `session_id` assigned by the SOP log is reused as the trace filename and as the trace's `summary.session_id`, so `SOPSession.trace_id == SOPSession.session_id` on linked rows. `trace_id` remains a separate nullable field (rather than just using `session_id`) so DevTools can distinguish "session with no trace captured" from "session with trace missing from disk". Already-written sessions remain valid with `trace_id = None`.
- `Makefile` — `make eval` default unchanged (`TRACE_MODE=on_failure` inherited); add `make eval-trace` (`TRACE_MODE=always make eval`) and `make clean-traces` (retention CLI).
- `.gitignore` — add `traces/` (matches existing pattern for `backend/tests/evals/reports/`).
- Backend lib deps — none new (Pydantic, PyYAML, FastAPI already present).
- Frontend lib deps — none new.

---

## Migration Sequence

1. **Ship trace subsystem + new `/api/trace/*`.** Existing SOP stubs untouched.
2. **Replace SOP stub handlers with forwarding shims** that call the trace handlers. Same URLs, same response shapes, new backing.
3. **Flip frontend `api.ts`** to hit `/api/trace/*` directly.
4. **Delete SOP shims.** Old URLs no longer served. Complete.

Each step keeps the app shippable. No mandatory sequencing between backend capture and frontend display work — capture can be built and merged before any frontend change lands.

---

## Open Questions / Future Work

- **Trace indexing.** With enough traces, grepping summaries becomes slow. Deferred — a SQLite index over summary fields is easy to add later without touching the trace file format.
- **Cross-session diff.** Comparing two traces (e.g., before/after a fix) is a natural DevTools feature. Out of scope for v1; the data contract supports it.
- **Live-tail events via WebSocket.** The event bus is future-proof for this — just add a WS subscriber. Deferred until a real use case.
- **Scope C diagnostic harness.** Separate brainstorm after this ships. Scope C will subscribe to the bus to drive controlled mutations and capture differential traces.
