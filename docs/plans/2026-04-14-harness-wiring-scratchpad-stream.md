# Plan: Full Harness Wiring + Scratchpad Streaming

**Created:** 2026-04-14  
**Branch:** feat/harness-wiring-scratchpad

---

## Goal

Replace `chat_api.py`'s standalone `_agent_loop` / `_stream_agent_loop` with the full harness `AgentLoop`, and emit live `scratchpad_delta` SSE events so `ScratchpadPanel.tsx` shows the agent's reasoning in real time.

Two sub-goals:
1. **Full harness wiring** — all analytical skills, guardrails, artifact store, wiki, A2A
2. **Scratchpad streaming** — `write_working` tool emits `scratchpad_delta` SSE; panel subscribes

---

## Background

### Current state

`chat_api.py` has a standalone mini-loop (`_agent_loop`, `_stream_agent_loop`) that only supports `execute_python`. The full `AgentLoop` in `harness/loop.py` has guardrails, A2A delegation, artifact tracking, and all analytical skills — but it is not wired to any HTTP endpoint.

`ScratchpadPanel.tsx` is a stub: "No scratchpad content yet."

### Why it matters

- Users can't access `data_profiler`, `correlate`, `stat_validate`, etc. through the chat UI yet
- Guardrails (blocked tools, pre/post gates) never fire
- Scratchpad reasoning is invisible to the user

---

## Architecture

### Scratchpad data flow

The agent writes to `working.md` via the `write_working` tool:
```
agent → write_working(content) → WikiEngine.write_working()
```

Currently `TurnState.scratchpad` is seeded at turn start from `working.md` but never updated mid-turn. We fix this:
- `_write_working` handler returns `{"ok": True, "content": content}` (adds content to payload)
- `AgentLoop.run()` / `run_stream()` detect `write_working` calls and update `state.scratchpad` from the result
- `run_stream()` additionally emits `StreamEvent(type="scratchpad_delta", payload={"content": ...})`

### chat_api.py changes

Replace `_stream_agent_loop` body with:
```python
artifact_store = ArtifactStore()
wiki = WikiEngine(...)
sandbox = SandboxExecutor(...)
dispatcher = ToolDispatcher()
register_core_tools(dispatcher, artifact_store, wiki, sandbox, session_id)
client = _make_client(model_id, http)
loop = AgentLoop(dispatcher)
for event in loop.run_stream(client, system, message, ...):
    yield event.to_sse()
```

The synchronous `_agent_loop` (used by `POST /api/chat`) can similarly delegate to `AgentLoop.run()`.

### SSE event additions

`run_stream()` already emits: `turn_start`, `tool_call`, `tool_result`, `a2a_start`, `a2a_end`, `turn_end`

We add: `scratchpad_delta` — payload `{"content": "<full markdown>"}` — emitted after each `write_working` tool result.

### Frontend store additions

```ts
// store.ts additions
scratchpad: string          // current working.md content
setScratchpad(c: string): void
clearScratchpad(): void
```

`ChatInput.tsx` handles `scratchpad_delta` → `setScratchpad(event.content ?? '')`

`ScratchpadPanel.tsx` subscribes to `scratchpad` from store and renders markdown.

---

## Phases

### Phase 1 — Backend: scratchpad_delta event (loop.py + skill_tools.py)

**Files:** `backend/app/harness/skill_tools.py`, `backend/app/harness/loop.py`, `backend/app/harness/stream_events.py`

1. **`skill_tools.py`**: Update `_write_working` to return `{"ok": True, "content": content}` so the result carries the new scratchpad body.

2. **`loop.py`**: In both `run()` and `run_stream()`, after dispatching any tool whose `call.name == "write_working"`, extract `result.payload.get("content")` and assign it to `state.scratchpad`. In `run_stream()`, additionally yield:
   ```python
   StreamEvent(type="scratchpad_delta", payload={"content": content})
   ```

3. No changes to `stream_events.py` needed (generic `StreamEvent` handles any type).

**Tests:** `backend/app/harness/tests/test_loop.py` — add test that `write_working` call in `run_stream()` produces a `scratchpad_delta` event with the expected content.

---

### Phase 2 — Backend: wire chat_api.py to full harness

**Files:** `backend/app/api/chat_api.py`

Replace the standalone loop bodies. Key details:

- `WikiEngine` needs a `data/wiki/{session_id}/` directory (create on first use)
- `ArtifactStore` uses `data/artifacts/{session_id}/`  
- `SandboxExecutor` needs the session's DuckDB bootstrap globals
- System prompt: use `PreTurnInjector.build()` if wiki/skills are available, else fall back to `_SYSTEM_PROMPT`
- The harness `AgentLoop` uses `tools=()` in `CompletionRequest` (tools are registered on the dispatcher, not passed directly) — wait, no: looking at the harness loop, it passes `tools=()` to `CompletionRequest`... but how does the client know what tools to advertise?

**Critical gap to resolve:** The `CompletionRequest.tools` field is what tells the LLM what tools are available. Currently `_stream_agent_loop` passes `tools=(_EXECUTE_PYTHON,)`. In the full harness `run()`, it passes `tools=()`. We need to either:
- Pass `ToolSchema` tuples derived from the dispatcher's registered tools, OR
- Keep the existing `tools` pattern but have the dispatcher's registered handlers matched by name when the LLM calls them

Looking at the harness router:

```python
# harness/router.py — need to read this
```

Actually the dispatcher's registered handlers are matched by name when the LLM calls a tool by name in its response. The `tools` in `CompletionRequest` is what the API advertises to the model. These two need to be in sync.

**Resolution:** `chat_api.py`'s new `_stream_agent_loop` should:
1. Build the dispatcher with handlers registered
2. Build the `tools` tuple from `dispatcher.tool_schemas()` (add this method to `ToolDispatcher`)
3. Pass these to `AgentLoop.run_stream(client, system, message, tools=tool_schemas, ...)`

This requires `AgentLoop.run_stream()` to accept a `tools` parameter instead of always using `()`.

**Simpler alternative:** Since the dispatcher already has registered schemas (see `dispatcher.py`), add `dispatcher.tool_schemas() -> tuple[ToolSchema, ...]` that returns all registered schemas. Pass these in `CompletionRequest`. This is already needed but currently missing.

---

### Phase 3 — Frontend: scratchpad store + panel

**Files:** `frontend/src/lib/store.ts`, `frontend/src/lib/api.ts`, `frontend/src/components/chat/ChatInput.tsx`, `frontend/src/components/right-panel/ScratchpadPanel.tsx`

1. **`store.ts`**: Add `scratchpad: string`, `setScratchpad`, `clearScratchpad` to `useChatStore`.

2. **`api.ts`**: Add `content?: string` to `ChatStreamEvent` (for `scratchpad_delta` payload).

3. **`ChatInput.tsx`**: In the `for await` event loop, handle `scratchpad_delta`:
   ```ts
   } else if (ev.type === 'scratchpad_delta') {
     setScratchpad(ev.content ?? '')
   }
   ```
   Also call `clearScratchpad()` at the start of each new message submission.

4. **`ScratchpadPanel.tsx`**: Rewrite to subscribe to store and render markdown:
   ```tsx
   const scratchpad = useChatStore((s) => s.scratchpad)
   // render MarkdownContent or pre-formatted monospace text
   ```

---

### Phase 4 — Read dispatcher.py and verify tool_schemas

**Files:** `backend/app/harness/dispatcher.py`

Add `tool_schemas() -> tuple[ToolSchema, ...]` method that returns the schemas registered on the dispatcher. This allows `AgentLoop` to advertise all registered tools to the LLM without the caller having to maintain a separate list.

---

## File Change Summary

| File | Change |
|------|--------|
| `backend/app/harness/skill_tools.py` | `_write_working` returns `content` in payload |
| `backend/app/harness/loop.py` | detect `write_working` results → update `state.scratchpad`; emit `scratchpad_delta` in `run_stream` |
| `backend/app/harness/dispatcher.py` | add `tool_schemas()` method |
| `backend/app/api/chat_api.py` | replace standalone loops with `AgentLoop` backed by full dispatcher |
| `frontend/src/lib/store.ts` | add `scratchpad`, `setScratchpad`, `clearScratchpad` |
| `frontend/src/lib/api.ts` | add `content?` to `ChatStreamEvent` |
| `frontend/src/components/chat/ChatInput.tsx` | handle `scratchpad_delta` event |
| `frontend/src/components/right-panel/ScratchpadPanel.tsx` | subscribe to store, render markdown |

---

## Open Questions

1. **System prompt**: Should chat_api use `PreTurnInjector` (wiki + skills) or keep the simple `_SYSTEM_PROMPT`? Recommendation: use `PreTurnInjector` for full harness, keep simple prompt as fallback when injector is unavailable.

2. **Wiki persistence**: Should each chat session get its own wiki directory? Recommendation: yes — `data/wiki/{session_id}/` — isolated per session.

3. **Backward compat for `POST /api/chat` (sync)**: Keep the sync endpoint working. Wire it to `AgentLoop.run()` with same dispatcher setup.

4. **`tools` in `AgentLoop`**: Currently `run()` / `run_stream()` hardcode `tools=()` in `CompletionRequest`. They need to accept `tools: tuple[ToolSchema, ...]` — add this parameter.

---

## Build Order

1. `dispatcher.py` — add `tool_schemas()` (10 min, no deps)
2. `skill_tools.py` — return `content` from `_write_working` (5 min)
3. `loop.py` — scratchpad state update + `scratchpad_delta` event (20 min)
4. `chat_api.py` — wire to full harness (45 min, most complex)
5. `store.ts` — add scratchpad slice (5 min)
6. `api.ts` — add `content?` field (2 min)
7. `ChatInput.tsx` — handle `scratchpad_delta` (5 min)
8. `ScratchpadPanel.tsx` — render from store (10 min)

---

## Success Criteria

- `POST /api/chat/stream` returns `scratchpad_delta` events when the agent calls `write_working`
- `ScratchpadPanel` shows live scratchpad content during a streaming response
- `data_profiler`, `correlate`, `stat_validate` tools are available via the chat endpoint
- All existing tests still pass
- `POST /api/chat` (sync) still returns a valid response
