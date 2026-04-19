# Thread List + Palette Polish — Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add backend-persisted pin + one-way freeze to conversations, ship a polished thread list (filter, sections, MoreMenu, Checkpoints), gate the composer on freeze, and wire two new command-palette groups.

**Architecture:** Backend stores `pinned` + `frozen_at` on the JSON-per-conversation `Conversation` model with a new PATCH endpoint and 409 on frozen append. Frontend store + api client mirror the schema. ThreadList reads state from conversations directly; CommandPalette adds Conversations (jump-to) and This conversation (mutating) groups.

**Tech Stack:** FastAPI + Pydantic frozen models, pytest. React 19 + Zustand v5, vitest.

---

## Task 1 — Backend: pinned + frozen_at fields

**Files:**
- Modify: `backend/app/api/conversations_api.py`
- Test: `backend/tests/test_conversations_api.py`

- [ ] Add `pinned: bool = False` and `frozen_at: float | None = None` to `Conversation`.
- [ ] Add `ConversationPatch` model with optional `pinned`, `frozen_at`, `title`.
- [ ] Add `PATCH /api/conversations/{conv_id}` handler — uses lock, replaces fields via `model_copy(update=...)`, atomic write. Reject `frozen_at: None` if currently frozen (one-way).
- [ ] Modify `POST /api/conversations/{conv_id}/turns` — return `HTTPException(409, "conversation is frozen")` when `frozen_at is not None`.
- [ ] Tests: PATCH pin persists; PATCH freeze persists; append after freeze returns 409; PATCH unfreeze rejected.
- [ ] Run `pytest backend/tests/test_conversations_api.py -v`. Expected: all pass.
- [ ] Commit: `feat(backend): pinned + frozen_at conversations + PATCH endpoint`.

## Task 2 — Frontend store + api client

**Files:**
- Modify: `frontend/src/lib/api-backend.ts`
- Modify: `frontend/src/lib/store.ts`
- Test: `frontend/src/lib/__tests__/store.test.ts` (or new file)

- [ ] In `api-backend.ts`, add `patch(id, payload)` method to the `conversations` client (PATCH, JSON body).
- [ ] In `store.ts`, extend `Conversation` interface with `pinned?: boolean; frozenAt?: number | null`.
- [ ] Add `setPinned(id, value)` and `freezeConversation(id)` actions (optimistic update + revert on error).
- [ ] Ensure `loadConversation` and conversation list hydration map backend `frozen_at` → frontend `frozenAt`.
- [ ] Tests: setPinned calls patch + updates state; freezeConversation sets `frozenAt` and prevents new turns being appended via store actions.
- [ ] Run `pnpm vitest run src/lib/__tests__/store.test.ts`. Expected: pass.
- [ ] Commit: `feat(frontend): store + api client for pin/freeze`.

## Task 3 — ThreadList polish (filter, sections, MoreMenu)

**Files:**
- Modify: `frontend/src/components/shell/ThreadList.tsx`
- Test: `frontend/src/components/shell/__tests__/ThreadList.test.tsx`

- [ ] Remove local `useState<PinnedMap>`. Read pinned/frozenAt from each conversation.
- [ ] Add controlled `<input>` filter at the top (case-insensitive substring on title).
- [ ] Compute four bucketed lists: pinned (not frozen), today, week, older, frozen. Render each section only when non-empty. Show section header in small caps.
- [ ] Add `MoreMenu` component: trigger (lucide MoreHorizontal); items: Pin/Unpin (label flips), Freeze (hidden when frozen), Rename (prompt), Duplicate, Delete, Export (JSON download).
- [ ] Freeze action shows window.confirm with the spec message.
- [ ] Frozen rows render with lock icon and muted style.
- [ ] Tests: filter narrows list; pinned section shows only pinned; checkpoints section shows frozen; MoreMenu fires correct store action; freeze confirm cancels cleanly.
- [ ] Run `pnpm vitest run src/components/shell/__tests__/ThreadList.test.tsx`. Expected: pass.
- [ ] Commit: `feat(frontend): thread list filter, sections, MoreMenu`.

## Task 4 — Composer freeze gating

**Files:**
- Modify: `frontend/src/components/chat/ChatPane.tsx` (or composer file — locate via grep for the textarea)

- [ ] When the active conversation has `frozenAt`, disable the composer input + send button.
- [ ] Render a banner above the composer: "This conversation is frozen. Duplicate it to continue." with a Duplicate button.
- [ ] Run `pnpm vitest run` for any composer test that exists. Add a small test if none exists.
- [ ] Commit: `feat(frontend): gate composer when conversation frozen`.

## Task 5 — Command palette groups

**Files:**
- Modify: `frontend/src/components/command-palette/CommandPalette.tsx`
- Test: `frontend/src/components/command-palette/__tests__/CommandPalette.test.tsx`

- [ ] Build dynamic Conversations group: top 50 by updatedAt desc, exclude frozen. Item action: load + route to that conversation.
- [ ] Build dynamic This conversation group: Pin/Unpin (gated on active + flip label), Freeze (hidden when frozen), Rename, Duplicate, Delete, Export.
- [ ] Tests: Conversations group filters out frozen; This conversation group reflects active conv; Freeze hidden when frozen.
- [ ] Run `pnpm vitest run src/components/command-palette`. Expected: pass.
- [ ] Commit: `feat(frontend): palette Conversations + This conversation groups`.

## Task 6 — Verification + log entry

- [ ] `cd frontend && pnpm typecheck` — must be clean.
- [ ] `cd frontend && pnpm vitest run` — all pass, coverage on touched files ≥80%.
- [ ] `cd frontend && pnpm build` — must succeed.
- [ ] `cd backend && pytest -q` — must be clean (or scoped subset if full suite is heavy).
- [ ] Add Unreleased entry in `docs/log.md` summarizing sub-project 4 with commit hashes.
- [ ] Commit log update: `docs(log): thread list + palette polish (sub-project 4)`.
