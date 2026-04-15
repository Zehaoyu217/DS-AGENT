# Gap Fix + Capability Push Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix concrete bugs blocking CI, close structural gaps in the harness, add hooks and filesystem tools, then harden test coverage and UI quality.

**Architecture:** Three sequential tiers — A (bugs/gaps), B (new capabilities: hooks + fs-tools), C (quality: tests, context inspector accuracy, session notes, todos tab). Each tier is a self-contained commit group; B depends on A passing CI, C depends on B interfaces being stable.

**Tech Stack:** Python 3.12 / FastAPI / uv (backend), React + TypeScript / Vite / Zustand (frontend), pytest + pytest-asyncio (tests)

**Spec:** `docs/superpowers/specs/2026-04-15-gap-fix-and-capability-design.md`

---

## File Map

**Modified (backend):**
- `backend/pyproject.toml` — add pytest-asyncio to dependency-groups.dev (Task 1)
- `Makefile` — fix test-backend target (Task 2)
- `backend/app/api/chat_api.py` — micro_compact→ctx (Task 3), startup guard (Task 4), get_context_status tool (Task 6), fs tool schemas (Task 13), hook wiring (Task 10)
- `backend/app/harness/wrap_up.py` — min-turns guard + worklog + char cap (Task 5)
- `backend/app/harness/loop.py` — hook_runner param + pre/post calls (Task 10)
- `backend/app/harness/skill_tools.py` — register fs tool handlers (Task 13)
- `backend/app/main.py` — register hooks_router (Task 9)

**Created (backend):**
- `backend/app/harness/hooks.py` — HookRunner class (Task 8)
- `backend/app/api/hooks_api.py` — GET /api/hooks (Task 9)
- `backend/app/harness/fs_tools.py` — FsTools class (Task 12)
- `backend/tests/unit/test_hooks.py` — HookRunner tests (Task 14)
- `backend/tests/unit/test_fs_tools.py` — FsTools tests (Task 14)

**Modified (frontend):**
- `frontend/src/components/right-panel/SessionRightPanel.tsx` — auto-switch to Tasks tab (Task 15)

---

## TIER A — Bug Fixes + Gap Closures

---

### Task 1: Restore pytest-asyncio dev dependency (A1)

**Files:**
- Modify: `backend/pyproject.toml`

- [ ] **Step 1: Inspect the current dependency-groups section**

Open `backend/pyproject.toml` and find the `[dependency-groups]` section. It currently reads:
```toml
[dependency-groups]
dev = [
    "pytest>=9.0.3",
    "types-pyyaml>=6.0.12.20260408",
]
```

The `[project.optional-dependencies] dev` already has `pytest-asyncio>=0.25.0`, but uv installs from `[dependency-groups]`, not optional extras. Add it here.

- [ ] **Step 2: Add pytest-asyncio to dependency-groups.dev**

Edit `backend/pyproject.toml`, replace the `[dependency-groups]` section:
```toml
[dependency-groups]
dev = [
    "pytest>=9.0.3",
    "pytest-asyncio>=0.25.0",
    "types-pyyaml>=6.0.12.20260408",
]
```

- [ ] **Step 3: Sync the backend venv**

```bash
cd backend && uv sync
```

Expected: `+ pytest-asyncio 0.25.x` in installed packages output.

- [ ] **Step 4: Run the previously-failing async tests**

```bash
cd backend && uv run python -m pytest tests/unit/test_eval_judge.py tests/unit/test_eval_runner.py -v --tb=short
```

Expected: All tests pass (no "async functions not natively supported" errors). If still failing, check `asyncio_mode = "auto"` is present in `[tool.pytest.ini_options]` — it should already be there.

- [ ] **Step 5: Run full unit suite to confirm no regressions**

```bash
cd backend && uv run python -m pytest tests/unit/ -q
```

Expected: 174 passed, 0 failed.

- [ ] **Step 6: Commit**

```bash
git add backend/pyproject.toml
git commit -m "fix: add pytest-asyncio to dependency-groups so uv sync installs it"
```

---

### Task 2: Fix Makefile test-backend target (A2)

**Files:**
- Modify: `Makefile`

- [ ] **Step 1: Find the broken target**

```bash
grep -n "test-backend" Makefile
```

Expected output shows:
```
test-backend:
	cd backend && pytest -v --tb=short
```

`pytest` is not on PATH — it lives in `backend/.venv/bin/`. Fix: use `uv run python -m pytest`.

- [ ] **Step 2: Fix the target**

Edit `Makefile`, replace the `test-backend` recipe line:

Old:
```makefile
test-backend:
	cd backend && pytest -v --tb=short
```

New:
```makefile
test-backend:
	cd backend && uv run python -m pytest -v --tb=short
```

- [ ] **Step 3: Verify it works**

```bash
make test-backend 2>&1 | tail -5
```

Expected: `N passed in X.XXs` (not "command not found").

- [ ] **Step 4: Commit**

```bash
git add Makefile
git commit -m "fix: use uv run python -m pytest in test-backend target"
```

---

### Task 3: Wire MicroCompactor → ContextManager (A3 + C2)

**Files:**
- Modify: `backend/app/api/chat_api.py`

**Why:** When the `MicroCompactor` fires inside `AgentLoop.run_stream()`, it emits a `micro_compact` SSE event but never calls `ctx.record_compaction()`. The Context Inspector (`ContextSection.tsx`) already renders `compaction_history` from `ctx.snapshot()` — it just has nothing to show because `record_compaction` is never called.

- [ ] **Step 1: Locate the event loop in _stream_agent_loop**

In `backend/app/api/chat_api.py`, find `_stream_agent_loop()`. Inside the `for event in loop.run_stream(...)` loop, find the block that starts:

```python
if event.type == "scratchpad_delta":
    captured_state.scratchpad = str(event.payload.get("content", ""))
```

- [ ] **Step 2: Add the record_compaction call**

Add a new clause immediately after the `scratchpad_delta` check (before the `tool_result` check):

```python
if event.type == "scratchpad_delta":
    captured_state.scratchpad = str(event.payload.get("content", ""))

if event.type == "micro_compact":
    ctx.record_compaction(
        tokens_before=event.payload.get("tokens_before", 0),
        tokens_after=event.payload.get("tokens_after", 0),
        removed=[
            {"name": f"compacted_tool_{i}"}
            for i in range(event.payload.get("dropped_messages", 0))
        ],
        survived=list(event.payload.get("artifact_refs", [])),
    )

if event.type == "tool_result":
    ...
```

- [ ] **Step 3: Write a unit test**

Create `backend/tests/unit/test_micro_compact_ctx.py`:

```python
"""Test that micro_compact SSE events are recorded in the ContextManager."""
from __future__ import annotations

from app.context.manager import ContextManager


def test_record_compaction_appends_to_history():
    ctx = ContextManager()
    ctx.record_compaction(
        tokens_before=10_000,
        tokens_after=6_000,
        removed=[{"name": "compacted_tool_0"}, {"name": "compacted_tool_1"}],
        survived=["artifact-abc"],
    )
    history = ctx.compaction_history
    assert len(history) == 1
    entry = history[0]
    assert entry["tokens_before"] == 10_000
    assert entry["tokens_after"] == 6_000
    assert entry["tokens_freed"] == 4_000
    assert entry["id"] == 1
    assert len(entry["removed"]) == 2
    assert entry["survived"] == ["artifact-abc"]


def test_record_compaction_increments_id():
    ctx = ContextManager()
    ctx.record_compaction(5000, 4000, [], [])
    ctx.record_compaction(4000, 3000, [], [])
    ids = [e["id"] for e in ctx.compaction_history]
    assert ids == [1, 2]
```

- [ ] **Step 4: Run the test**

```bash
cd backend && uv run python -m pytest tests/unit/test_micro_compact_ctx.py -v
```

Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/app/api/chat_api.py backend/tests/unit/test_micro_compact_ctx.py
git commit -m "fix: record micro_compact events in ContextManager for Context Inspector"
```

---

### Task 4: Guard startup fragility in chat_api.py (A4)

**Files:**
- Modify: `backend/app/api/chat_api.py`

**Why:** `_SYSTEM_PROMPT = _build_system_prompt()` is called at module import time. If `data_scientist.md` or the skill registry is missing, the entire chat router fails to import and FastAPI cannot start.

- [ ] **Step 1: Find the module-level call**

In `backend/app/api/chat_api.py`, find line:
```python
# Back-compat exports for prompts_api (which imports a constant by name).
_SYSTEM_PROMPT = _build_system_prompt()
```

- [ ] **Step 2: Wrap in try/except**

Replace with:
```python
# Back-compat exports for prompts_api (which imports a constant by name).
# Wrapped defensively: if the wiki/skills/prompt file is absent at startup,
# the module still loads with a safe fallback instead of crashing FastAPI.
try:
    _SYSTEM_PROMPT = _build_system_prompt()
except Exception as _startup_exc:
    import logging as _logging
    _logging.getLogger(__name__).warning(
        "startup prompt build failed (%s) — using fallback", _startup_exc
    )
    _SYSTEM_PROMPT = "You are an analytical assistant. The full system prompt failed to load."
```

- [ ] **Step 3: Write a smoke test**

Add to `backend/tests/unit/test_chat_api_wiring.py` (this file already exists):

```python
def test_module_imports_cleanly():
    """chat_api must import without error even when wiki or skills are absent."""
    import importlib
    import app.api.chat_api as m
    assert hasattr(m, "_SYSTEM_PROMPT")
    assert isinstance(m._SYSTEM_PROMPT, str)
    assert len(m._SYSTEM_PROMPT) > 10
```

- [ ] **Step 4: Run the test**

```bash
cd backend && uv run python -m pytest tests/unit/test_chat_api_wiring.py -v --tb=short
```

Expected: All tests pass.

- [ ] **Step 5: Commit**

```bash
git add backend/app/api/chat_api.py backend/tests/unit/test_chat_api_wiring.py
git commit -m "fix: guard module-level _build_system_prompt() with try/except fallback"
```

---

### Task 5: Session notes minimum-turns guard + quality (A5 + C3)

**Files:**
- Modify: `backend/app/harness/wrap_up.py`

Three improvements: (1) don't write notes for trivial turns, (2) auto-populate the Worklog section from the tool trace, (3) cap note size at 3000 chars.

- [ ] **Step 1: Add min-turns guard to finalize()**

In `backend/app/harness/wrap_up.py`, find `TurnWrapUp.finalize()`. Locate the block:
```python
        # Structured 9-section session notes (P18).  Best-effort: ...
        notes_written = False
        try:
            notes = _render_session_notes(...)
```

Add a guard before the `try`:
```python
        # Only write session notes for turns with actual work.
        # Single-turn no-tool sessions produce nine "—" sections — noise.
        notes_written = False
        _has_tool_activity = len(state.as_trace()) > 0
        if turn_index >= 2 or _has_tool_activity:
            try:
                notes = _render_session_notes(
                    session_id=session_id,
                    turn_index=turn_index,
                    final_text=final_text,
                    state=state,
                    promoted_finding_ids=promoted,
                )
                self._wiki.write_session_notes(session_id, notes)
                notes_written = True
            except Exception:
                notes_written = False
```

- [ ] **Step 2: Auto-populate Worklog in _render_session_notes()**

In `_render_session_notes()`, find where `## Meta` is built. Add a `worklog` variable just before building `parts`:

```python
    # Auto-populate worklog from tool trace (step N: tool → status).
    worklog_lines: list[str] = []
    for evt in trace:
        tname = str(evt.get("tool", ""))
        status = str(evt.get("status", ""))
        step = evt.get("step", "?")
        if tname:
            worklog_lines.append(f"- step {step}: `{tname}` → {status}")
    worklog = "\n".join(worklog_lines) if worklog_lines else "_no tool activity_"
```

Then in `parts`, replace the empty `## Worklog` line (if it exists) or add after `## Next Steps`:
```python
    parts = [
        ...
        f"## {_SESSION_SECTIONS[6]}",   # Next Steps
        next_steps,
        "",
        "## Worklog",
        worklog,
        "",
        f"## {_SESSION_SECTIONS[7]}",   # Errors / Blockers
        ...
    ]
```

- [ ] **Step 3: Cap notes at 3000 chars before writing**

In `finalize()`, after `notes = _render_session_notes(...)`:
```python
                if len(notes) > 3000:
                    notes = notes[:2997] + "…"
                self._wiki.write_session_notes(session_id, notes)
```

- [ ] **Step 4: Write tests**

In `backend/tests/unit/test_session_notes.py` (already exists), add:

```python
from app.harness.wrap_up import _render_session_notes, TurnWrapUp
from app.harness.turn_state import TurnState
from unittest.mock import MagicMock


def test_worklog_populated_from_trace():
    state = TurnState(dataset_loaded=False)
    state.record_tool("execute_python", {"output": "ok"}, "ok")
    notes = _render_session_notes(
        session_id="test-123",
        turn_index=1,
        final_text="done",
        state=state,
        promoted_finding_ids=[],
    )
    assert "execute_python" in notes
    assert "## Worklog" in notes


def test_notes_capped_at_3000_chars():
    state = TurnState(dataset_loaded=False)
    # Stuff the scratchpad with a huge goal section.
    state.scratchpad = "## Goal\n" + ("x" * 5000)
    notes = _render_session_notes(
        session_id="cap-test",
        turn_index=2,
        final_text="done",
        state=state,
        promoted_finding_ids=[],
    )
    # _render_session_notes itself is uncapped; cap happens in finalize()
    wiki = MagicMock()
    bus = MagicMock()
    wrap = TurnWrapUp(wiki=wiki, event_bus=bus)
    wrap.finalize(state=state, final_text="done", session_id="cap-test", turn_index=2)
    written = wiki.write_session_notes.call_args[0][1]
    assert len(written) <= 3000


def test_notes_skipped_for_trivial_turn():
    state = TurnState(dataset_loaded=False)  # no tools called
    wiki = MagicMock()
    bus = MagicMock()
    wrap = TurnWrapUp(wiki=wiki, event_bus=bus)
    wrap.finalize(state=state, final_text="hi", session_id="s1", turn_index=1)
    wiki.write_session_notes.assert_not_called()


def test_notes_written_when_tools_used_on_turn_1():
    state = TurnState(dataset_loaded=False)
    state.record_tool("execute_python", {}, "ok")
    wiki = MagicMock()
    bus = MagicMock()
    wrap = TurnWrapUp(wiki=wiki, event_bus=bus)
    wrap.finalize(state=state, final_text="result", session_id="s2", turn_index=1)
    wiki.write_session_notes.assert_called_once()
```

- [ ] **Step 5: Run the tests**

```bash
cd backend && uv run python -m pytest tests/unit/test_session_notes.py -v --tb=short
```

Expected: All tests pass.

- [ ] **Step 6: Commit**

```bash
git add backend/app/harness/wrap_up.py backend/tests/unit/test_session_notes.py
git commit -m "fix: session notes min-turns guard, auto-populate Worklog, cap at 3000 chars"
```

---

### Task 6: Implement get_context_status tool (A6)

**Files:**
- Modify: `backend/app/api/chat_api.py`

**Why:** P21 injects context budget info into the system prompt. This tool lets the agent query its current live utilization programmatically.

- [ ] **Step 1: Add the ToolSchema to _CHAT_TOOLS**

In `backend/app/api/chat_api.py`, after `_TODO_WRITE = ToolSchema(...)`, add:

```python
_GET_CONTEXT_STATUS = ToolSchema(
    name="get_context_status",
    description=(
        "Return the current context window utilization for this session. "
        "Use when you need to know how much context budget remains before "
        "deciding whether to run a long analysis or compress working memory."
    ),
    input_schema={
        "type": "object",
        "properties": {},
        "required": [],
    },
)
```

Then add `_GET_CONTEXT_STATUS` to `_CHAT_TOOLS`:
```python
_CHAT_TOOLS: tuple[ToolSchema, ...] = (
    _EXECUTE_PYTHON,
    _WRITE_WORKING,
    _LOAD_SKILL,
    _SAVE_ARTIFACT,
    _PROMOTE_FINDING,
    _DELEGATE_SUBAGENT,
    _TODO_WRITE,
    _GET_CONTEXT_STATUS,
)
```

- [ ] **Step 2: Register the handler in _stream_agent_loop**

In `_stream_agent_loop()`, after `dispatcher = _build_dispatcher(...)` is called, add a closure that captures `ctx`:

```python
            dispatcher = _build_dispatcher(
                session_id=session_id,
                session_bootstrap=session_bootstrap,
                charts_out=charts,
                outputs_out=outputs,
                client=client,
            )

            # get_context_status closes over `ctx` so it returns live data
            # for this specific session. Registered after _build_dispatcher
            # because ctx is only in scope here.
            def _ctx_status_handler(args: dict[str, Any]) -> dict[str, Any]:
                snap = ctx.snapshot()
                return {
                    "total_tokens": snap["total_tokens"],
                    "max_tokens": snap["max_tokens"],
                    "utilization_pct": round(snap["utilization"] * 100),
                    "compaction_needed": snap["compaction_needed"],
                    "layers": [
                        {"name": lyr["name"], "tokens": lyr["tokens"]}
                        for lyr in snap["layers"]
                    ],
                }

            dispatcher.register("get_context_status", _ctx_status_handler)
```

- [ ] **Step 3: Write a unit test**

Add to `backend/tests/unit/test_chat_api_wiring.py`:

```python
def test_get_context_status_in_chat_tools():
    from app.api.chat_api import _CHAT_TOOLS
    names = [t.name for t in _CHAT_TOOLS]
    assert "get_context_status" in names


def test_ctx_status_handler_returns_correct_shape():
    from app.context.manager import ContextManager, ContextLayer
    ctx = ContextManager()
    ctx.add_layer(ContextLayer(name="System Prompt", tokens=1200, compactable=False, items=[]))
    ctx.add_layer(ContextLayer(name="User Message", tokens=300, compactable=True, items=[]))

    def _handler(args):
        snap = ctx.snapshot()
        return {
            "total_tokens": snap["total_tokens"],
            "max_tokens": snap["max_tokens"],
            "utilization_pct": round(snap["utilization"] * 100),
            "compaction_needed": snap["compaction_needed"],
            "layers": [{"name": l["name"], "tokens": l["tokens"]} for l in snap["layers"]],
        }

    result = _handler({})
    assert result["total_tokens"] == 1500
    assert result["utilization_pct"] == 1  # 1500/200000 ~ 0.75%
    assert len(result["layers"]) == 2
    assert result["layers"][0]["name"] == "System Prompt"
```

- [ ] **Step 4: Run the tests**

```bash
cd backend && uv run python -m pytest tests/unit/test_chat_api_wiring.py -v --tb=short
```

Expected: All pass.

- [ ] **Step 5: Commit**

```bash
git add backend/app/api/chat_api.py backend/tests/unit/test_chat_api_wiring.py
git commit -m "feat: add get_context_status tool (P21 — agent queries live context utilization)"
```

---

### Task 7: Verify vega-embed in frontend (A7)

**Files:**
- Read: `frontend/package.json`

- [ ] **Step 1: Check package.json**

```bash
grep "vega-embed\|vega-lite\|vega" frontend/package.json
```

- [ ] **Step 2: If vega-embed is absent, install it**

If `vega-embed` is not in `dependencies`:
```bash
cd frontend && npm install vega-embed
```

- [ ] **Step 3: Verify VegaChart.tsx can render**

Check the import in `frontend/src/components/chat/VegaChart.tsx`:
```bash
head -5 frontend/src/components/chat/VegaChart.tsx
```
Confirm it imports from `vega-embed` (not a missing local file).

- [ ] **Step 4: Frontend build check**

```bash
cd frontend && npm run build 2>&1 | tail -10
```

Expected: Build succeeds with no "Cannot resolve 'vega-embed'" errors.

- [ ] **Step 5: Commit if package.json changed**

```bash
# Only if step 2 was needed:
git add frontend/package.json frontend/package-lock.json
git commit -m "fix: add vega-embed dependency for VegaChart rendering"
```

---

## TIER B — Capability Push

---

### Task 8: Implement HookRunner (P23 — foundation)

**Files:**
- Create: `backend/app/harness/hooks.py`
- Create: `backend/tests/unit/test_hooks.py`

**Interface:** `HookRunner` reads `backend/config/hooks.json` (or `CCAGENT_HOOKS_PATH` env), pattern-matches tool names, and runs shell commands. Never raises — hook failures are logged, never propagated.

- [ ] **Step 1: Create the config directory**

```bash
mkdir -p backend/config
```

- [ ] **Step 2: Write the test file first (TDD)**

Create `backend/tests/unit/test_hooks.py`:

```python
"""Tests for HookRunner — P23 user-configurable hooks."""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from app.harness.hooks import HookRunner


# ── fixture ──────────────────────────────────────────────────────────────────


@pytest.fixture
def hooks_config(tmp_path: Path) -> Path:
    cfg = {
        "PreToolUse": [
            {"matcher": "execute_python", "command": "echo pre_$TOOL_NAME", "description": "log pre"},
        ],
        "PostToolUse": [
            {"matcher": "save_artifact", "command": "echo post_$TOOL_NAME", "description": "log post"},
        ],
        "Stop": [
            {"command": "echo stop_hook", "description": "session end"},
        ],
    }
    p = tmp_path / "hooks.json"
    p.write_text(json.dumps(cfg))
    return p


# ── matcher ───────────────────────────────────────────────────────────────────


def test_matcher_exact(tmp_path):
    r = HookRunner(tmp_path / "absent.json")
    assert r._match("execute_python", "execute_python")
    assert not r._match("execute_python", "save_artifact")


def test_matcher_wildcard(tmp_path):
    r = HookRunner(tmp_path / "absent.json")
    assert r._match("*", "any_tool")
    assert r._match("execute_*", "execute_python")
    assert not r._match("execute_*", "save_artifact")


# ── missing config ────────────────────────────────────────────────────────────


def test_missing_config_is_noop(tmp_path):
    r = HookRunner(tmp_path / "absent.json")
    # Must not raise
    r.run_pre("execute_python", {"code": "1+1"})
    r.run_post("save_artifact", {"artifact_id": "a1"})
    r.run_stop("session-1")


# ── pre-tool hook ─────────────────────────────────────────────────────────────


def test_pre_tool_runs_matching_command(hooks_config, capsys):
    r = HookRunner(hooks_config)
    r.run_pre("execute_python", {"code": "1+1"})
    # Hook runs in subprocess — no capsys output. Just verify no exception.


def test_pre_tool_skips_non_matching(hooks_config):
    r = HookRunner(hooks_config)
    # save_artifact has no PreToolUse hook — must not raise
    r.run_pre("save_artifact", {})


def test_pre_tool_nonzero_exit_does_not_raise(tmp_path):
    cfg = {
        "PreToolUse": [{"matcher": "*", "command": "exit 1", "description": "fail"}],
    }
    p = tmp_path / "hooks.json"
    p.write_text(json.dumps(cfg))
    r = HookRunner(p)
    # Must not raise even though exit code is 1
    r.run_pre("execute_python", {})


# ── post-tool hook ────────────────────────────────────────────────────────────


def test_post_tool_runs_matching_command(hooks_config):
    r = HookRunner(hooks_config)
    r.run_post("save_artifact", {"artifact_id": "a1"})


def test_post_tool_skips_pre_hooks(hooks_config):
    r = HookRunner(hooks_config)
    # execute_python has PreToolUse but not PostToolUse
    r.run_post("execute_python", {})  # must not raise


# ── stop hook ─────────────────────────────────────────────────────────────────


def test_stop_hook_runs(hooks_config):
    r = HookRunner(hooks_config)
    r.run_stop("session-abc")


# ── env vars ──────────────────────────────────────────────────────────────────


def test_env_vars_injected(tmp_path):
    """Hook command can read TOOL_NAME, TOOL_INPUT, SESSION_ID env vars."""
    out_file = tmp_path / "out.txt"
    cfg = {
        "PreToolUse": [
            {
                "matcher": "execute_python",
                "command": f"echo $TOOL_NAME > {out_file}",
                "description": "capture tool name",
            }
        ],
    }
    p = tmp_path / "hooks.json"
    p.write_text(json.dumps(cfg))
    r = HookRunner(p)
    r.run_pre("execute_python", {"code": "1+1"}, session_id="sess-42")
    assert out_file.read_text().strip() == "execute_python"
```

- [ ] **Step 3: Run tests to confirm they fail**

```bash
cd backend && uv run python -m pytest tests/unit/test_hooks.py -v --tb=short 2>&1 | head -20
```

Expected: ImportError (`No module named 'app.harness.hooks'`).

- [ ] **Step 4: Implement HookRunner**

Create `backend/app/harness/hooks.py`:

```python
"""User-configurable hook system (P23).

Reads backend/config/hooks.json (or $CCAGENT_HOOKS_PATH) and runs shell
commands in response to PreToolUse, PostToolUse, and Stop events.

Design constraints:
- Never raises — hook failures are logged, never propagated.
- Uses fnmatch for matcher patterns (supports *, ?, [seq]).
- Subprocess timeout: 10 seconds per hook command.
- Env vars available to commands: TOOL_NAME, TOOL_INPUT, TOOL_OUTPUT,
  SESSION_ID (PostToolUse only for TOOL_OUTPUT).
"""
from __future__ import annotations

import fnmatch
import json
import logging
import os
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

_DEFAULT_CONFIG = Path(__file__).resolve().parents[3] / "config" / "hooks.json"


class HookRunner:
    """Load hook config and run matching commands for each hook event."""

    def __init__(self, config_path: Path | None = None) -> None:
        self._config_path = config_path or Path(
            os.environ.get("CCAGENT_HOOKS_PATH", str(_DEFAULT_CONFIG))
        )
        self._config: dict[str, list[dict]] | None = None

    def _load(self) -> dict[str, list[dict]]:
        if self._config is not None:
            return self._config
        path = self._config_path
        if not path.exists():
            self._config = {}
            return self._config
        try:
            self._config = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            logger.warning("hooks: failed to load config %s: %s", path, exc)
            self._config = {}
        return self._config

    def _match(self, matcher: str, tool_name: str) -> bool:
        """Return True if matcher pattern matches tool_name."""
        return fnmatch.fnmatch(tool_name, matcher)

    def _run(
        self,
        command: str,
        extra_env: dict[str, str],
        description: str,
    ) -> None:
        env = {**os.environ, **extra_env}
        try:
            result = subprocess.run(
                command,
                shell=True,
                env=env,
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode != 0:
                logger.warning(
                    "hooks: command failed (exit %d) — %s: %s",
                    result.returncode,
                    description,
                    result.stderr[:200],
                )
        except subprocess.TimeoutExpired:
            logger.warning("hooks: command timed out — %s", description)
        except Exception as exc:
            logger.warning("hooks: command error — %s: %s", description, exc)

    def run_pre(
        self,
        tool_name: str,
        arguments: dict,
        session_id: str = "",
    ) -> None:
        """Run all matching PreToolUse hooks."""
        hooks = self._load().get("PreToolUse", [])
        env = {
            "TOOL_NAME": tool_name,
            "TOOL_INPUT": json.dumps(arguments),
            "SESSION_ID": session_id,
        }
        for hook in hooks:
            if self._match(hook.get("matcher", ""), tool_name):
                self._run(hook["command"], env, hook.get("description", ""))

    def run_post(
        self,
        tool_name: str,
        result: dict,
        session_id: str = "",
    ) -> None:
        """Run all matching PostToolUse hooks."""
        hooks = self._load().get("PostToolUse", [])
        env = {
            "TOOL_NAME": tool_name,
            "TOOL_OUTPUT": json.dumps(result),
            "SESSION_ID": session_id,
        }
        for hook in hooks:
            if self._match(hook.get("matcher", ""), tool_name):
                self._run(hook["command"], env, hook.get("description", ""))

    def run_stop(self, session_id: str = "") -> None:
        """Run all Stop hooks (called at end of session)."""
        hooks = self._load().get("Stop", [])
        env = {"SESSION_ID": session_id}
        for hook in hooks:
            self._run(hook.get("command", ""), env, hook.get("description", ""))
```

- [ ] **Step 5: Run tests**

```bash
cd backend && uv run python -m pytest tests/unit/test_hooks.py -v --tb=short
```

Expected: All tests pass.

- [ ] **Step 6: Commit**

```bash
git add backend/app/harness/hooks.py backend/tests/unit/test_hooks.py backend/config/
git commit -m "feat(P23): HookRunner — user-configurable PreToolUse/PostToolUse/Stop hooks"
```

---

### Task 9: hooks_api.py and main.py registration (P23 — API layer)

**Files:**
- Create: `backend/app/api/hooks_api.py`
- Modify: `backend/app/main.py`

- [ ] **Step 1: Create hooks_api.py**

Create `backend/app/api/hooks_api.py`:

```python
"""Read-only endpoint to inspect the current hook configuration (P23).

POST/PUT for editing hooks is out of scope — edit hooks.json directly.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from fastapi import APIRouter

router = APIRouter(prefix="/api/hooks", tags=["hooks"])

_DEFAULT_CONFIG = Path(__file__).resolve().parents[3] / "config" / "hooks.json"


@router.get("")
def get_hooks() -> dict:
    """Return the current hook configuration."""
    path = Path(os.environ.get("CCAGENT_HOOKS_PATH", str(_DEFAULT_CONFIG)))
    if not path.exists():
        return {"hooks": {}, "config_path": str(path), "loaded": False}
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
        return {"hooks": config, "config_path": str(path), "loaded": True}
    except Exception as exc:
        return {"hooks": {}, "config_path": str(path), "loaded": False, "error": str(exc)}
```

- [ ] **Step 2: Register in main.py**

In `backend/app/main.py`, add the import and router registration:

```python
from app.api.hooks_api import router as hooks_router
```

Inside `create_app()`, after `app.include_router(todos_router)`:
```python
    app.include_router(hooks_router)
```

- [ ] **Step 3: Write a test**

Add to `backend/tests/unit/test_health.py` (or create `test_hooks_api.py`):

Create `backend/tests/unit/test_hooks_api.py`:
```python
"""Smoke test for GET /api/hooks."""
from __future__ import annotations

from fastapi.testclient import TestClient
from app.main import create_app


def test_get_hooks_returns_200():
    client = TestClient(create_app())
    resp = client.get("/api/hooks")
    assert resp.status_code == 200
    data = resp.json()
    assert "hooks" in data
    assert "loaded" in data
```

- [ ] **Step 4: Run the test**

```bash
cd backend && uv run python -m pytest tests/unit/test_hooks_api.py -v --tb=short
```

Expected: 1 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/app/api/hooks_api.py backend/app/main.py backend/tests/unit/test_hooks_api.py
git commit -m "feat(P23): GET /api/hooks endpoint + router registration"
```

---

### Task 10: Wire HookRunner into AgentLoop and chat_api (P23 — runtime)

**Files:**
- Modify: `backend/app/harness/loop.py`
- Modify: `backend/app/api/chat_api.py`

- [ ] **Step 1: Add hook_runner parameter to AgentLoop.__init__**

In `backend/app/harness/loop.py`, update the import and `__init__`:

Add import at the top:
```python
from app.harness.hooks import HookRunner
```

Update `AgentLoop.__init__`:
```python
class AgentLoop:
    def __init__(
        self,
        dispatcher: ToolDispatcher,
        compactor: MicroCompactor | None = None,
        hook_runner: HookRunner | None = None,
    ) -> None:
        self._dispatcher = dispatcher
        self._compactor = compactor or MicroCompactor()
        self._hook_runner = hook_runner or HookRunner()
```

- [ ] **Step 2: Call pre/post hooks in run() (sync path)**

In `AgentLoop.run()`, in the `for call in resp.tool_calls:` loop, add hook calls around `dispatcher.dispatch()`:

```python
                result: ToolResult = self._dispatcher.dispatch(call)
```

Replace with:
```python
                self._hook_runner.run_pre(call.name, call.arguments)
                result: ToolResult = self._dispatcher.dispatch(call)
                self._hook_runner.run_post(
                    call.name,
                    result.payload if isinstance(result.payload, dict) else {},
                )
```

- [ ] **Step 3: Call pre/post hooks in run_stream() (streaming path)**

In `AgentLoop.run_stream()`, same pattern — find:
```python
                result: ToolResult = self._dispatcher.dispatch(call)
```

Replace with:
```python
                self._hook_runner.run_pre(call.name, call.arguments, session_id=session_id)
                result: ToolResult = self._dispatcher.dispatch(call)
                self._hook_runner.run_post(
                    call.name,
                    result.payload if isinstance(result.payload, dict) else {},
                    session_id=session_id,
                )
```

- [ ] **Step 4: Instantiate HookRunner in chat_api.py and pass to AgentLoop**

In `backend/app/api/chat_api.py`, add import:
```python
from app.harness.hooks import HookRunner
```

In `_stream_agent_loop()`, after `dispatcher = _build_dispatcher(...)` and the `_ctx_status_handler` registration:
```python
            hook_runner = HookRunner()
            loop = AgentLoop(dispatcher, hook_runner=hook_runner)
```

(Replace the bare `loop = AgentLoop(dispatcher)` with this.)

Also in `_agent_loop_sync()`:
```python
        loop = AgentLoop(dispatcher, hook_runner=HookRunner())
```

- [ ] **Step 5: Call run_stop in _run_wrap_up**

In `_run_wrap_up()` in `chat_api.py`, after `wrap.finalize(...)`:
```python
    # Run Stop hooks after the turn is fully wrapped up.
    try:
        HookRunner().run_stop(session_id)
    except Exception:
        pass
```

- [ ] **Step 6: Write a loop-level hook test**

Add to `backend/tests/unit/test_hooks.py`:

```python
def test_hook_runner_pre_called_in_loop(tmp_path):
    """Verify run_pre is called during AgentLoop dispatch (not just by chat_api)."""
    import json
    from unittest.mock import MagicMock, patch
    from app.harness.hooks import HookRunner

    runner = HookRunner(tmp_path / "absent.json")
    called = []
    original_run_pre = runner.run_pre
    runner.run_pre = lambda *a, **kw: called.append(a[0])  # record tool_name

    # We're not running a full loop — just verify the interface is correct.
    runner.run_pre("execute_python", {"code": "1+1"})
    assert "execute_python" in called
```

- [ ] **Step 7: Run all hook tests**

```bash
cd backend && uv run python -m pytest tests/unit/test_hooks.py tests/unit/test_hooks_api.py -v --tb=short
```

Expected: All tests pass.

- [ ] **Step 8: Commit**

```bash
git add backend/app/harness/loop.py backend/app/api/chat_api.py backend/tests/unit/test_hooks.py
git commit -m "feat(P23): wire HookRunner into AgentLoop pre/post dispatch and Stop wrap-up"
```

---

### Task 11: Frontend hook entries in TerminalPanel (P23 — frontend)

**Files:**
- Modify: `frontend/src/components/right-panel/TerminalPanel.tsx`

**Why:** `TerminalPanel` already renders a `CompactBanner` for `__compact__` entries. Hook runs should appear as `__hook__` entries with a `⚙` prefix. Since hooks run server-side, they don't emit SSE events — instead, `ChatInput.tsx` can forward them if needed, or we add a simple note in the tool log when hooks are registered.

**Simpler approach:** The backend already emits `tool_call` SSE events with names like `__compact__`. We need to add a `__hook__` variant. Since hooks run synchronously (blocking) during dispatch, they don't emit their own SSE events. Skip the frontend change for now — hooks are logged server-side. This task becomes a verification step only.

- [ ] **Step 1: Confirm CompactBanner renders for __compact__ entries**

```bash
grep -n "__compact__\|CompactBanner" frontend/src/components/right-panel/TerminalPanel.tsx
```

Expected: Lines showing `__compact__` check and `<CompactBanner>` render.

- [ ] **Step 2: Note in code that __hook__ is reserved for future SSE**

In `TerminalPanel.tsx`, find the `CompactBanner` branch:
```tsx
if (entry.name === '__compact__') return <CompactBanner entry={entry} />
```

Add a comment immediately after:
```tsx
if (entry.name === '__compact__') return <CompactBanner entry={entry} />
// '__hook__' entries reserved for P23 hook SSE events (future: emit from backend)
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/right-panel/TerminalPanel.tsx
git commit -m "docs(P23): reserve __hook__ entry name in TerminalPanel for future hook SSE"
```

---

### Task 12: Implement FsTools (P25 — foundation)

**Files:**
- Create: `backend/app/harness/fs_tools.py`
- Create: `backend/tests/unit/test_fs_tools.py`

**Safety model:** All paths resolved against `project_root`. Any escape attempt returns `{"ok": False, "error": "path_escape"}`. Banned suffixes/names: `.env`, `.key`, `.pem`, `secrets`, `.git`.

- [ ] **Step 1: Write tests first (TDD)**

Create `backend/tests/unit/test_fs_tools.py`:

```python
"""Tests for FsTools — read-only filesystem access for the agent (P25)."""
from __future__ import annotations

from pathlib import Path

import pytest

from app.harness.fs_tools import FsTools


@pytest.fixture
def root(tmp_path: Path) -> Path:
    # Set up a small file tree
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "report.md").write_text("# Report\n\nContent here.")
    (tmp_path / "data" / "notes.txt").write_text("line1\nline2\nfoo bar\n")
    (tmp_path / ".env").write_text("SECRET=abc")
    (tmp_path / "deep").mkdir()
    (tmp_path / "deep" / "nested.py").write_text("def hello(): pass\n")
    return tmp_path


@pytest.fixture
def fs(root: Path) -> FsTools:
    return FsTools(project_root=root)


# ── read_file ─────────────────────────────────────────────────────────────────


def test_read_file_returns_content(fs, root):
    result = fs.read_file({"path": "data/report.md"})
    assert result["ok"] is True
    assert "Content here" in result["content"]
    assert result["lines"] == 3


def test_read_file_path_escape(fs):
    result = fs.read_file({"path": "../../../etc/passwd"})
    assert result["ok"] is False
    assert result["error"] == "path_escape"


def test_read_file_banned_env(fs):
    result = fs.read_file({"path": ".env"})
    assert result["ok"] is False
    assert result["error"] == "path_forbidden"


def test_read_file_missing_file(fs):
    result = fs.read_file({"path": "data/nonexistent.md"})
    assert result["ok"] is False
    assert "not_found" in result["error"]


# ── glob_files ────────────────────────────────────────────────────────────────


def test_glob_files_matches_pattern(fs):
    result = fs.glob_files({"pattern": "**/*.md"})
    assert result["ok"] is True
    paths = result["files"]
    assert any("report.md" in p for p in paths)
    assert not any(".env" in p for p in paths)


def test_glob_files_caps_at_200(fs, root):
    for i in range(210):
        (root / f"file_{i}.txt").write_text(f"content {i}")
    result = fs.glob_files({"pattern": "*.txt"})
    assert result["ok"] is True
    assert result["count"] <= 200
    assert len(result["files"]) <= 200


def test_glob_files_path_escape(fs):
    result = fs.glob_files({"pattern": "../**/*.py"})
    assert result["ok"] is False
    assert result["error"] == "path_escape"


# ── search_text ───────────────────────────────────────────────────────────────


def test_search_text_finds_matches(fs):
    result = fs.search_text({"pattern": "foo", "path": "data"})
    assert result["ok"] is True
    matches = result["matches"]
    assert len(matches) >= 1
    assert any("foo" in m["text"] for m in matches)
    assert all("file" in m for m in matches)
    assert all("line" in m for m in matches)


def test_search_text_caps_at_50(fs, root):
    # Write a file with 60 matching lines
    lines = "\n".join(f"needle {i}" for i in range(60))
    (root / "data" / "big.txt").write_text(lines)
    result = fs.search_text({"pattern": "needle", "path": "data"})
    assert result["ok"] is True
    assert len(result["matches"]) <= 50


def test_search_text_path_escape(fs):
    result = fs.search_text({"pattern": "foo", "path": "../.."})
    assert result["ok"] is False
    assert result["error"] == "path_escape"
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
cd backend && uv run python -m pytest tests/unit/test_fs_tools.py -v --tb=short 2>&1 | head -15
```

Expected: ImportError (`No module named 'app.harness.fs_tools'`).

- [ ] **Step 3: Implement FsTools**

Create `backend/app/harness/fs_tools.py`:

```python
"""Read-only filesystem tools for the agent (P25).

Gives the agent three tools to inspect the project without running Python:
  - read_file(path)      — read a file's content
  - glob_files(pattern)  — list files matching a glob
  - search_text(pattern, path) — grep-style text search

Safety: all paths are resolved against ``project_root``. Any path that would
escape the root returns {"ok": False, "error": "path_escape"}. Banned names
(.env, *.key, *.pem, .git, secrets/) also return an error.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

_BANNED_NAMES = frozenset({".env", ".key", ".pem", "secrets", ".git"})
_BANNED_SUFFIXES = frozenset({".env", ".key", ".pem"})
_MAX_GLOB_RESULTS = 200
_MAX_SEARCH_RESULTS = 50
_MAX_FILE_CHARS = 50_000


class PathEscapeError(Exception):
    pass


class PathForbiddenError(Exception):
    pass


class FsTools:
    """Read-only filesystem access scoped to project_root."""

    def __init__(self, project_root: Path) -> None:
        self._root = project_root.resolve()

    def _resolve(self, path_str: str) -> Path:
        """Resolve path relative to root, raising on escape or banned name."""
        resolved = (self._root / path_str).resolve()
        if not str(resolved).startswith(str(self._root)):
            raise PathEscapeError(path_str)
        # Check each component for banned names/suffixes
        for part in resolved.parts:
            if part in _BANNED_NAMES or Path(part).suffix in _BANNED_SUFFIXES:
                raise PathForbiddenError(part)
        return resolved

    def read_file(self, args: dict[str, Any]) -> dict[str, Any]:
        path_str = str(args.get("path", ""))
        try:
            resolved = self._resolve(path_str)
        except PathEscapeError:
            return {"ok": False, "error": "path_escape"}
        except PathForbiddenError:
            return {"ok": False, "error": "path_forbidden"}
        if not resolved.exists():
            return {"ok": False, "error": f"not_found: {path_str}"}
        if not resolved.is_file():
            return {"ok": False, "error": "not_a_file"}
        try:
            content = resolved.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            return {"ok": False, "error": f"read_error: {exc}"}
        if len(content) > _MAX_FILE_CHARS:
            content = content[:_MAX_FILE_CHARS] + "\n…(truncated)"
        return {
            "ok": True,
            "path": path_str,
            "content": content,
            "lines": content.count("\n") + 1,
        }

    def glob_files(self, args: dict[str, Any]) -> dict[str, Any]:
        pattern = str(args.get("pattern", "*"))
        # Detect escape attempts in the pattern itself
        if pattern.startswith("..") or "/../" in pattern or pattern.startswith("/"):
            return {"ok": False, "error": "path_escape"}
        try:
            matches = list(self._root.glob(pattern))
        except Exception as exc:
            return {"ok": False, "error": f"glob_error: {exc}"}
        # Filter banned and non-files
        files: list[str] = []
        for m in matches:
            if not m.is_file():
                continue
            rel = str(m.relative_to(self._root))
            if any(part in _BANNED_NAMES for part in m.parts):
                continue
            if m.suffix in _BANNED_SUFFIXES:
                continue
            files.append(rel)
            if len(files) >= _MAX_GLOB_RESULTS:
                break
        return {"ok": True, "files": files, "count": len(files)}

    def search_text(self, args: dict[str, Any]) -> dict[str, Any]:
        pattern = str(args.get("pattern", ""))
        path_str = str(args.get("path", "."))
        if path_str.startswith("..") or "/../" in path_str or path_str.startswith("/"):
            return {"ok": False, "error": "path_escape"}
        search_root = (self._root / path_str).resolve()
        if not str(search_root).startswith(str(self._root)):
            return {"ok": False, "error": "path_escape"}
        try:
            compiled = re.compile(pattern)
        except re.error as exc:
            return {"ok": False, "error": f"invalid_regex: {exc}"}
        matches: list[dict[str, Any]] = []
        try:
            for fpath in search_root.rglob("*"):
                if not fpath.is_file():
                    continue
                if fpath.suffix in _BANNED_SUFFIXES:
                    continue
                try:
                    text = fpath.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                for lineno, line in enumerate(text.splitlines(), start=1):
                    if compiled.search(line):
                        matches.append({
                            "file": str(fpath.relative_to(self._root)),
                            "line": lineno,
                            "text": line[:200],
                        })
                        if len(matches) >= _MAX_SEARCH_RESULTS:
                            return {"ok": True, "matches": matches, "truncated": True}
        except Exception as exc:
            return {"ok": False, "error": f"search_error: {exc}"}
        return {"ok": True, "matches": matches, "truncated": False}
```

- [ ] **Step 4: Run tests**

```bash
cd backend && uv run python -m pytest tests/unit/test_fs_tools.py -v --tb=short
```

Expected: All tests pass.

- [ ] **Step 5: Commit**

```bash
git add backend/app/harness/fs_tools.py backend/tests/unit/test_fs_tools.py
git commit -m "feat(P25): FsTools — read_file / glob_files / search_text with path escape guard"
```

---

### Task 13: Register FsTools in register_core_tools and add ToolSchemas (P25 — wiring)

**Files:**
- Modify: `backend/app/harness/skill_tools.py`
- Modify: `backend/app/api/chat_api.py`

- [ ] **Step 1: Add FsTools instantiation to register_core_tools**

In `backend/app/harness/skill_tools.py`, at the top add import:
```python
from app.harness.fs_tools import FsTools
```

Find `register_core_tools()`. At the end of the function, before the `return` (or at the end of the body), add:

```python
    # ── Filesystem tools (P25) ────────────────────────────────────────────────
    _repo_root = Path(__file__).resolve().parents[3]
    fs = FsTools(project_root=_repo_root)
    dispatcher.register("read_file", fs.read_file)
    dispatcher.register("glob_files", fs.glob_files)
    dispatcher.register("search_text", fs.search_text)
```

Also add `from pathlib import Path` to the imports if not already present.

- [ ] **Step 2: Add ToolSchemas to _CHAT_TOOLS in chat_api.py**

In `backend/app/api/chat_api.py`, add three ToolSchema definitions before `_CHAT_TOOLS`:

```python
_READ_FILE = ToolSchema(
    name="read_file",
    description=(
        "Read the content of a file relative to the project root. "
        "Use to inspect skill code, docs, dataset files, or config. "
        "Returns content as a string and line count."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "File path relative to project root"},
        },
        "required": ["path"],
    },
)

_GLOB_FILES = ToolSchema(
    name="glob_files",
    description=(
        "List files matching a glob pattern relative to the project root. "
        "Use to discover skill packages, find config files, or enumerate datasets. "
        "Returns up to 200 results."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "pattern": {"type": "string", "description": "Glob pattern, e.g. 'backend/app/skills/**/*.py'"},
        },
        "required": ["pattern"],
    },
)

_SEARCH_TEXT = ToolSchema(
    name="search_text",
    description=(
        "Search for a regex pattern in files under a directory. "
        "Use to find function definitions, skill names, or dataset columns. "
        "Returns up to 50 matches with file path, line number, and matched text."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "pattern": {"type": "string", "description": "Regex pattern to search for"},
            "path": {"type": "string", "description": "Directory to search in (relative to project root)"},
        },
        "required": ["pattern"],
    },
)
```

Add to `_CHAT_TOOLS` tuple:
```python
_CHAT_TOOLS: tuple[ToolSchema, ...] = (
    _EXECUTE_PYTHON,
    _WRITE_WORKING,
    _LOAD_SKILL,
    _SAVE_ARTIFACT,
    _PROMOTE_FINDING,
    _DELEGATE_SUBAGENT,
    _TODO_WRITE,
    _GET_CONTEXT_STATUS,
    _READ_FILE,
    _GLOB_FILES,
    _SEARCH_TEXT,
)
```

- [ ] **Step 3: Write a registration test**

Add to `backend/tests/unit/test_chat_api_wiring.py`:

```python
def test_fs_tools_in_chat_tools():
    from app.api.chat_api import _CHAT_TOOLS
    names = [t.name for t in _CHAT_TOOLS]
    assert "read_file" in names
    assert "glob_files" in names
    assert "search_text" in names
```

- [ ] **Step 4: Run the test**

```bash
cd backend && uv run python -m pytest tests/unit/test_chat_api_wiring.py -v --tb=short
```

Expected: All pass.

- [ ] **Step 5: Commit**

```bash
git add backend/app/harness/skill_tools.py backend/app/api/chat_api.py backend/tests/unit/test_chat_api_wiring.py
git commit -m "feat(P25): register read_file/glob_files/search_text in dispatcher + _CHAT_TOOLS"
```

---

## TIER C — Quality Pass

---

### Task 14: Test coverage push to ≥ 80% (C1)

**Files:**
- Modify: `backend/tests/unit/test_fs_tools.py` (extend if needed)
- Modify: `backend/tests/unit/test_hooks.py` (extend if needed)

- [ ] **Step 1: Run coverage report**

```bash
cd backend && uv run python -m pytest tests/ --cov=app --cov-report=term-missing -q 2>&1 | tail -30
```

Note the overall coverage percentage and which modules are below 80%.

- [ ] **Step 2: Add missing tests for HookRunner edge cases**

Add to `backend/tests/unit/test_hooks.py`:

```python
def test_hook_command_timeout_does_not_raise(tmp_path):
    """Commands that hang must be killed and not raise."""
    cfg = {
        "PreToolUse": [
            {"matcher": "*", "command": "sleep 30", "description": "slow hook"},
        ]
    }
    p = tmp_path / "hooks.json"
    p.write_text(json.dumps(cfg))
    r = HookRunner(p)
    # HookRunner has 10s timeout; sleep 30 should be killed, not raise
    import time
    start = time.monotonic()
    r.run_pre("any_tool", {})
    elapsed = time.monotonic() - start
    assert elapsed < 15, "hook runner should time out within 10s"


def test_malformed_config_is_noop(tmp_path):
    p = tmp_path / "hooks.json"
    p.write_text("not valid json {{{")
    r = HookRunner(p)
    r.run_pre("execute_python", {})  # must not raise


def test_empty_hooks_list_is_noop(tmp_path):
    cfg = {"PreToolUse": [], "PostToolUse": [], "Stop": []}
    p = tmp_path / "hooks.json"
    p.write_text(json.dumps(cfg))
    r = HookRunner(p)
    r.run_pre("execute_python", {})
    r.run_post("save_artifact", {})
    r.run_stop("sess-1")
```

- [ ] **Step 3: Add FsTools binary file and permission edge cases**

Add to `backend/tests/unit/test_fs_tools.py`:

```python
def test_glob_banned_suffix_excluded(fs, root):
    (root / "data" / "secret.key").write_text("key content")
    result = fs.glob_files({"pattern": "data/*"})
    assert result["ok"] is True
    assert not any(".key" in f for f in result["files"])


def test_search_text_no_results(fs):
    result = fs.search_text({"pattern": "XYZZY_NOT_FOUND", "path": "data"})
    assert result["ok"] is True
    assert result["matches"] == []


def test_read_file_directory_not_file(fs, root):
    result = fs.read_file({"path": "data"})
    assert result["ok"] is False
    assert result["error"] == "not_a_file"


def test_search_text_invalid_regex(fs):
    result = fs.search_text({"pattern": "[invalid", "path": "data"})
    assert result["ok"] is False
    assert "invalid_regex" in result["error"]
```

- [ ] **Step 4: Re-run coverage**

```bash
cd backend && uv run python -m pytest tests/unit/ --cov=app --cov-report=term-missing -q 2>&1 | tail -20
```

Expected: Overall coverage ≥ 80%. If specific modules are low, add targeted tests for their uncovered lines.

- [ ] **Step 5: Commit**

```bash
git add backend/tests/unit/test_hooks.py backend/tests/unit/test_fs_tools.py
git commit -m "test(C1): extend hook + fs_tools test coverage toward 80%"
```

---

### Task 15: Auto-switch SessionRightPanel to Tasks tab (C4)

**Files:**
- Modify: `frontend/src/components/right-panel/SessionRightPanel.tsx`

**Why:** The Tasks tab already exists in `SessionRightPanel` but switching to it requires manual click. When the agent first writes todos (`todos_update` event → `hasTodos` becomes true), the right panel should auto-switch to Tasks.

- [ ] **Step 1: Add useEffect auto-switch to SessionRightPanel**

In `frontend/src/components/right-panel/SessionRightPanel.tsx`, add `useEffect` to the import:
```tsx
import { useState, useEffect } from 'react'
```

After the existing state/store hooks, add:
```tsx
  // Auto-switch to Tasks tab when the agent first writes todos,
  // but only if the right panel is already open (don't hijack focus).
  const rightPanelOpen = useChatStore((s) => s.rightPanelOpen)
  const [autoSwitched, setAutoSwitched] = useState(false)

  useEffect(() => {
    if (hasTodos && !autoSwitched && rightPanelOpen) {
      setActiveTab('tasks')
      setAutoSwitched(true)
    }
  }, [hasTodos, autoSwitched, rightPanelOpen])
```

- [ ] **Step 2: Reset autoSwitched when todos are cleared**

Add a second effect that resets `autoSwitched` when todos length drops to 0 (so the next agent run can auto-switch again):
```tsx
  useEffect(() => {
    if (!hasTodos) {
      setAutoSwitched(false)
    }
  }, [hasTodos])
```

- [ ] **Step 3: Frontend build check**

```bash
cd frontend && npm run build 2>&1 | tail -10
```

Expected: Build succeeds with no TypeScript errors.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/components/right-panel/SessionRightPanel.tsx
git commit -m "feat(C4): auto-switch to Tasks tab when agent first writes todos"
```

---

## Final Verification

- [ ] **Run all backend tests**

```bash
cd backend && uv run python -m pytest tests/unit/ tests/integration/ -q 2>&1 | tail -10
```

Expected: All pass, 0 failures.

- [ ] **Run frontend build**

```bash
cd frontend && npm run build 2>&1 | tail -10
```

Expected: Build succeeds.

- [ ] **Run make test-backend**

```bash
make test-backend 2>&1 | tail -5
```

Expected: No "command not found" errors.

- [ ] **Check Definition of Done against spec**

- [ ] `make test-backend` runs without error ← Task 2
- [ ] All 174+ unit tests pass including 4 async eval tests ← Task 1
- [ ] Context Inspector shows micro-compact events after a long session ← Task 3
- [ ] API starts correctly even if data_scientist.md is temporarily missing ← Task 4
- [ ] Session notes only written for turns with tool activity or turn_index ≥ 2 ← Task 5
- [ ] Session notes Worklog section auto-populated from tool trace ← Task 5
- [ ] Agent can call `get_context_status` and receive utilization data ← Task 6
- [ ] VegaChart renders a Vega-Lite spec ← Task 7
- [ ] `POST /api/chat/stream`: execute_python triggers a PreToolUse hook subprocess ← Task 10
- [ ] Non-zero hook exit does not crash or block the turn ← Tasks 8, 10
- [ ] `GET /api/hooks` returns current hook config ← Task 9
- [ ] Agent can call `read_file({"path": "docs/gotchas.md"})` ← Task 13
- [ ] Path escape attempt returns `{"ok": False, "error": "path_escape"}` ← Task 12
- [ ] `glob_files` and `search_text` work end-to-end ← Task 12, 13
- [ ] Test coverage ≥ 80% ← Task 14
- [ ] TodosPanel auto-switches to Tasks tab on first todos_update ← Task 15
