# Eval Readiness Audit

**Date:** 2026-04-15  
**Branch:** main (merged from feat/v2-os-platform)  
**Auditor:** Claude  

This document records the findings from a pre-eval-run readiness check. It covers the trace recording pipeline, eval framework, LLM judge, and frontend monitoring tools.

---

## Summary

| Area | Status | Blockers |
|------|--------|----------|
| Trace bus + file write | ✅ Working | — |
| Tool-call trace events | ❌ Not published | `publish_tool_call` never called |
| Per-turn LLM trace events | ⚠️ Coarse | 1 record per session, not per turn |
| Compaction trace events | ✅ Working (partially) | MicroCompact → ctx → trace works |
| Eval framework (unit tests) | ✅ 37/37 passing | — |
| Eval data (eval.db) | ✅ Seeded | — |
| Rubric YAMLs | ✅ All 5 present | — |
| LLM judge (qwen3.5:9b) | ❌ Fails to load | Resource contention with Gemma4 models |
| Real agent adapter | ❌ Missing | No `RealAgentAdapter` implementation |
| Frontend TracesList | ✅ Working | Limited by trace gaps above |
| Frontend SessionDevTools | ✅ Working | Events/Timeline panels mostly empty |
| Frontend ContextInspector | ✅ Working | Compaction history works |
| Full test suite (non-eval) | ✅ 410/410 passing | — |

---

## 1. Trace Recording System

### 1.1 What IS recorded

Every `/api/chat/stream` request produces a YAML at `traces/{session_id}.yaml` via `TraceSession` context manager (`backend/app/trace/publishers.py:TraceSession`).

Events written per session:
- `session_start` — session_id, input_query, level, level_label ✅
- `llm_call` (one) — system_prompt + user_query sections, response text, estimated token counts ✅
- `final_output` — last response text ✅
- `session_end` — outcome (ok/error) ✅
- `compaction` — when `ContextManager.record_compaction()` fires via `micro_compact` SSE ✅

### 1.2 Critical gaps

**GAP-T1 — Tool calls never reach the trace bus (CRITICAL)**

`publish_tool_call` exists in `publishers.py:60` but is never called in the production code path.

In `loop.py`, each tool dispatch emits `StreamEvent(type="tool_call")` and `StreamEvent(type="tool_result")` SSE events only. These flow to the frontend UI (`TerminalPanel`) but are never published to the trace bus.

In `chat_api.py`, only `publish_llm_call` and `publish_final_output` are imported. `publish_tool_call` is not imported.

**Impact:** The trace YAML has zero `tool_call` events. The DevTools → Events tab shows nothing for tool calls. The Timeline shows `tool_count=0` for every turn. Evals that check tool call patterns have no data.

**Files to fix:** `backend/app/api/chat_api.py` (emit `publish_tool_call` when processing `tool_result` events from `_stream_agent_loop`)

---

**GAP-T2 — Single coarse LLM record per session (HIGH)**

`publish_llm_call` is called once at the END of the entire agent run in `chat_api.py:950-977` with:
- `step_id="s1"` (hardcoded)
- `turn=1` (hardcoded)
- Token counts from `_estimate_tokens()` (not real API token counts)
- Only the user query and system prompt — not the full multi-turn context

A real agent run may have 6–12 LLM calls (one per tool-use step). Currently they all collapse into one record.

**Impact:** Prompt Inspector always shows step `s1` regardless of how many turns occurred. Timeline turn bar chart is always 1 turn. Per-step latency and token data is lost.

**Files to fix:** Wire the `AnthropicClient.complete()` call to emit `publish_llm_call` with actual response metadata. The client already returns `usage` in `CompletionResponse.usage`.

---

**GAP-T3 — Scratchpad writes not published (LOW)**

`publish_scratchpad_write` defined in `publishers.py:83` is never called.

When the agent calls `write_working`, `loop.py` emits a `scratchpad_delta` SSE event and `chat_api.py` captures the content in `captured_state.scratchpad`. Neither calls `publish_scratchpad_write`.

**Impact:** The `scratchpad_write` event type is handled by `timeline.py` but never appears in traces.

---

**GAP-T4 — MicroCompact token counts are estimated (LOW)**

When the `MicroCompactor` fires, `chat_api.py:691–700` calls `ctx.record_compaction(tokens_before=..., tokens_after=...)` using the `tokens_before/tokens_after` fields from the `micro_compact` SSE payload. Those fields come from `compact_report.tokens_before/tokens_after` in `loop.py:185–197`.

The `MicroCompactor` (`harness/compactor.py`) likely estimates these counts rather than tracking real token usage from the API. **Needs verification** — may be fine.

---

### 1.3 What works correctly

- YAML file write is atomic (tmp file + `os.replace`) ✅
- `_should_write` correctly filters by `trace_mode` ✅
- `TraceRecorder._truncate` caps large event fields at 10KB ✅
- `list_traces` / `load_trace` in `trace/store.py` work ✅
- `assemble_prompt` in `trace/assembler.py` works for the single `s1` step ✅
- `build_timeline` in `trace/timeline.py` correctly handles event types ✅
- Integration test (`tests/integration/test_stream_trace.py`) verifies YAML write + event structure ✅

---

## 2. Eval Framework

### 2.1 What IS ready

| Component | Location | Status |
|-----------|----------|--------|
| Core types (AgentTrace, DimensionGrade, etc.) | `backend/app/evals/types.py` | ✅ |
| Grading logic (score rollup, grade_level) | `backend/app/evals/grading.py` | ✅ |
| Rubric YAML loader | `backend/app/evals/rubric.py` | ✅ |
| LLM judge wrapper | `backend/app/evals/judge.py` | ✅ |
| Eval runner (evaluate_level, format_*) | `backend/app/evals/runner.py` | ✅ |
| Rubric YAMLs (levels 1–5) | `backend/tests/evals/rubrics/` | ✅ |
| Eval level test files (levels 1–5) | `backend/tests/evals/` | ✅ |
| Seed script | `backend/scripts/seed_eval_data.py` | ✅ |
| eval.db seeded | `backend/data/duckdb/eval.db` | ✅ |
| Makefile targets | `seed-eval`, `eval`, `eval-trace`, `eval level=N` | ✅ |
| Unit tests | 37/37 pass | ✅ |

### 2.2 Critical gaps

**GAP-E1 — No real agent adapter (CRITICAL)**

The eval framework is designed around `AgentInterface`:
```python
class AgentInterface(Protocol):
    async def run(self, prompt: str, db_path: str) -> AgentTrace: ...
```

The `conftest.py` only provides `MockAgent` and `SequentialMockAgent` which return pre-constructed `AgentTrace` objects. There is **no concrete implementation** that:
1. Launches the real backend (or connects to a running one)
2. Calls `/api/chat/stream` with the eval prompt and the eval DB path
3. Captures tool calls, SQL queries, token counts, errors
4. Returns a real `AgentTrace`

Without this, all eval runs use synthetic mock data — you cannot measure the real agent's performance.

**Required file:** `backend/tests/evals/real_agent.py` with a `RealAgentAdapter` class.

---

**GAP-E2 — LLM judge fails to load (BLOCKER)**

`qwen3.5:9b` is present in Ollama (`ollama list` shows it), but calling `/api/generate` with it returns HTTP 500:
```
{"error":"model failed to load, this may be due to resource limitations or an internal error"}
```

Root cause: Several large Gemma4 models (gemma4:26b, gemma4:31b, gemma2:27b) are using most available VRAM/RAM, leaving insufficient resources for qwen3.5:9b.

**Confirmed by:** Direct `httpx` call to Ollama with `qwen3.5:9b` returns 500.

**Resolution options:**
1. Free up Ollama models (`ollama stop` for the large Gemma4 instances)
2. Switch judge model to `gemma4:e2b` or `gemma4:e4b` (smaller variants already loaded)
3. Run judge against Anthropic API instead of local Ollama

Currently, the `conftest.py` correctly skips eval tests when the model fails (`_require_ollama` fixture). So `pytest tests/` is still green. But `make eval` will fail.

---

**GAP-E3 — Eval-level tests use mock traces (MEDIUM)**

Even when the judge works, the 5 level tests (`test_level1.py` through `test_level5.py`) use fixture-injected `AgentTrace` objects with synthetic data. They verify the grading pipeline, not the agent.

To run real evals: level tests need to be wired to a `RealAgentAdapter` (GAP-E1), or a separate script needs to be written that drives the agent and grades the result.

---

### 2.3 Suggested real eval execution flow

Until `RealAgentAdapter` exists, the only path to real eval runs is:
1. Start the backend: `make backend`
2. Manually call `POST /api/chat/stream` with each level's prompt
3. Inspect the trace YAML under `traces/` to see what the agent did
4. Grade manually using the rubric YAMLs as reference

This is the "minimum viable eval run" and is feasible today.

---

## 3. Frontend Monitoring

### 3.1 What works

| Component | What it shows | Status |
|-----------|--------------|--------|
| `TracesList` | All trace YAMLs, sortable + filterable, 2s polling | ✅ |
| `SessionDevToolsPanel → Prompt` | System prompt + user query for step s1 | ✅ |
| `SessionDevToolsPanel → Context` | Context layers + compaction history via ContextInspector | ✅ |
| `SessionDevToolsPanel → Timeline` | Turn bars (input tokens, tool_count) | ✅ (empty due to GAP-T1) |
| `SessionDevToolsPanel → Events` | Raw compaction + scratchpad_write events | ✅ (empty due to GAP-T1/T3) |
| `SessionRightPanel → Traces tab` | Tool call log (TerminalPanel) + Artifacts | ✅ |
| `SessionRightPanel → Tasks tab` | TodosPanel, auto-switches on first todo_write | ✅ |
| `SessionRightPanel → Scratchpad tab` | Agent reasoning scratchpad | ✅ |
| `MonitorPage` | Historical trace list navigation | ✅ |

### 3.2 Frontend limitations tied to trace gaps

- **Events tab** will show nothing for tool calls (GAP-T1). The UI is ready but data doesn't exist.
- **Timeline** will always show 1 turn and 0 tool_calls per turn (GAP-T1, GAP-T2).
- **Prompt tab** always shows step `s1` regardless of how many turns the agent took (GAP-T2).

These are not frontend bugs — the UI components work correctly. They're empty because the backend doesn't publish the events.

### 3.3 Uncommitted changes (git status)

Three frontend files have local modifications not yet committed:
- `frontend/src/components/chat/ChatInput.tsx`
- `frontend/src/components/right-panel/SessionRightPanel.tsx`
- `frontend/src/components/session/SessionLayout.tsx`

These appear to implement C4 (Tasks tab) and related UI work from the latest plan. They should be reviewed and committed before starting eval runs to ensure clean state.

---

## 4. Test Coverage

Non-eval tests: **410/410 passing** (98s wall time).

Full run command: `cd backend && uv run python -m pytest tests/ --ignore=tests/evals -q`

Eval-level tests: **0/5 passing** (Ollama judge fails, see GAP-E2). Correctly skipped in CI because `_require_ollama` fixture gates them.

---

## 5. Gap Priority List

### Must Fix Before Real Eval Runs

| ID | Gap | Effort | Files |
|----|-----|--------|-------|
| GAP-E1 | Build `RealAgentAdapter` — connect eval to real backend | Medium | `backend/tests/evals/real_agent.py` (new) |
| GAP-E2 | Fix Ollama judge — free up model memory or switch to smaller model | Low | `backend/app/evals/judge.py` (model name) |
| GAP-T1 | Publish `tool_call` events to trace bus from chat_api | Medium | `backend/app/api/chat_api.py` |

### Should Fix for Complete Eval Observability

| ID | Gap | Effort | Files |
|----|-----|--------|-------|
| GAP-T2 | Per-turn LLM call recording — emit one `LlmCallEvent` per agent step | Medium-High | `backend/app/api/chat_api.py`, `loop.py` |
| GAP-T3 | Publish `scratchpad_write` events | Low | `backend/app/api/chat_api.py` |

### Housekeeping

| Item | Action |
|------|--------|
| Uncommitted frontend changes | Commit or discard before eval runs |
| `knowledge/wiki/working.md` | File contains placeholder "line 0, line 1…" content — needs real content or delete |

---

## 6. Minimum Path to First Real Eval Run

Even with the gaps above, you can run a manual eval today:

1. **Commit or discard** the 3 modified frontend files
2. **Start backend**: `make backend`
3. **Free up Ollama memory** by stopping large models: `ollama stop gemma4:31b` (or similar)
4. **Verify judge**: `curl -X POST http://localhost:11434/api/generate -d '{"model":"qwen3.5:9b","prompt":"Say A","stream":false}'` should return 200
5. **Run Level 1 manually**: send the Level 1 prompt from `tests/evals/rubrics/level1_rendering.yaml` via the chat UI with eval.db loaded
6. **Inspect trace**: `cat traces/<session_id>.yaml` — check that `llm_call` and `final_output` events are present
7. **Grade manually**: compare output against rubric criteria in the YAML
8. **Repeat for levels 2–5**

For automated eval runs against the real agent, GAP-E1 (RealAgentAdapter) must be built first.
