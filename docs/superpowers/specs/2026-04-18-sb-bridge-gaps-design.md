# Second Brain ↔ claude-code-agent bridge gaps — design spec

**Date:** 2026-04-18
**Status:** Draft (awaiting implementation plan)
**Scope:** Post-v2 refinement. Close the bridge gap between `claude-code-agent` (the analytical platform) and `second-brain` v2 (the digest-based KB). Today only `sb_search`, `sb_load`, `sb_reason`, `sb_ingest`, `sb_promote_claim` are exposed. None of the v2 digest surface reaches the agent or the frontend. This spec adds that layer — additively, without rewrites.

## 0. One-paragraph summary

The agent gains 7 new tool handlers covering the v2 digest surface plus `sb_stats`; a pre-turn hook injects a short "you have N pending KB decisions" summary into the system prompt at session start; the frontend gains a right-rail `DigestPanel` with apply/skip/mark-read controls. Proposals flow through a new `sb_digest_propose` tool that appends to `digests/pending.jsonl`, which the next `sb digest build` merges with its 5 LLM passes. Nothing auto-mutates the KB. All existing tools, contracts, and the sb CLI stay unchanged.

## 1. Goals and non-goals

### Goals
- The agent is aware of today's digest without burning a tool call (pre-turn injection).
- The user can triage the digest from the frontend without leaving the app.
- The agent can apply, skip, and propose digest entries via tools when asked in conversation.
- Every new surface gracefully degrades when `SECOND_BRAIN_ENABLED=False`.

### Non-goals
- Editing digest entries (actions are opaque — approve or skip).
- Multi-user conflict resolution.
- Undo UI — applied actions remain replayable via git history.
- New sb CLI commands (CLI already covers everything; bridge wraps it).
- Mobile layout (project is desktop-only).

## 2. Scenarios

| Label | Scenario | Surfaces used |
|---|---|---|
| A1 | Agent mentions pending digest at conversation start when relevant | Pre-turn hook |
| A3 | User opens right-rail panel, applies/skips entries without chat | Frontend panel + REST API |
| B1 | Agent notices a KB-relevant finding during analysis and proposes a digest entry | `sb_digest_propose` tool |
| C1 | User tells agent "apply r01 r02" or "what does my KB look like" | `sb_digest_*` + `sb_stats` tools |

## 3. New tool catalog

All handlers live in `backend/app/tools/sb_tools.py`, follow `{ok: bool, ...}` envelope, and call `_disabled()` when `SECOND_BRAIN_ENABLED=False`.

| Tool | Args | Returns |
|---|---|---|
| `sb_digest_today` | `{}` | `{ok, date, entry_count, unread, entries: [...]}` — today's digest summary |
| `sb_digest_list` | `{limit?: int = 10}` | `{ok, digests: [{date, entry_count, read, applied_count}]}` — newest-first |
| `sb_digest_show` | `{date: "YYYY-MM-DD"}` | `{ok, date, markdown, entries: [{id, section, line, action, applied, skipped}]}` |
| `sb_digest_apply` | `{date?: str, ids: list[str] \| "all"}` | `{ok, applied, skipped, failed}` |
| `sb_digest_skip` | `{date?: str, id: str, ttl_days?: int}` | `{ok, signature, expires_at}` |
| `sb_digest_propose` | `{section: str, action: dict}` | `{ok, pending_id, file}` |
| `sb_stats` | `{}` | `{ok, stats: {...}, health: {score, breakdown}}` |

### Propose action validation

`sb_digest_propose` accepts all 7 action types used by the nightly passes:
1. `upgrade_confidence {claim_id, from, to, rationale}`
2. `resolve_contradiction {left_id, right_id, rationale}`
3. `promote_wiki_to_claim {wiki_path, proposed_taxonomy}`
4. `backlink_claim_to_wiki {claim_id, wiki_path}`
5. `add_taxonomy_root {root, example_claim_ids}`
6. `re_abstract_batch {claim_ids, taxonomy}`
7. `drop_edge {src_id, dst_id, relation}`

Re-validated at the bridge (fail-fast). Unknown action types return `{ok: false, error: "invalid_action_type"}`.

### Pending-proposal flow

`sb_digest_propose` appends `{id: pending_id, section, action, proposed_at}` to `~/second-brain/digests/pending.jsonl`. Builder (in sb) gains a new pre-pass step that reads this file, wraps each line as a `DigestEntry` (id rewritten during renumbering), merges with pass output, and truncates `pending.jsonl` on successful build. `pending.jsonl` lives in the digests directory so it travels with the rest of the surface.

### Concurrency

Applier is per-entry transactional. Two simultaneous `sb_digest_apply` calls for the same id: second call observes the `.applied.jsonl` line and returns `{applied: [], skipped: ["r01"], failed: []}`. Good enough — no file locks.

## 4. Pre-turn hook (A1)

New module `backend/app/hooks/sb_digest_hook.py`.

**Trigger:** session start (first turn), before system prompt is finalized.

**Algorithm:**
1. If `SECOND_BRAIN_ENABLED=False` → return None.
2. If `SB_DIGEST_HOOK_ENABLED=False` (env var, default true) → return None.
3. Read today's digest path; if missing → return None.
4. Read `digests/.read_marks`; if today's ISO date present → return None.
5. Diff `digests/YYYY-MM-DD.actions.jsonl` against `.applied.jsonl`; unread_count = lines not yet applied.
6. If unread_count == 0 → return None.
7. Return injection string:

```text
## Pending knowledge base digest (YYYY-MM-DD)
You have N pending KB decisions. Tools: sb_digest_show, sb_digest_apply, sb_digest_skip.
Section summary: 3 Reconciliation, 1 Wiki↔KB drift, 2 Taxonomy.
Offer to review only if relevant to the conversation.
```

**Integration point:** identify where system prompt is composed (likely `backend/app/harness/loop.py` or `backend/app/harness/wiring.py`). Hook returns either `None` or a string to append. System-prompt composition stays a pure function.

**Failure mode:** any exception in the hook → log and return None. Never block a conversation.

## 5. Frontend panel (A3)

New component tree: `frontend/src/components/digest/` — `DigestPanel.tsx`, `DigestEntry.tsx`, `DigestHeader.tsx`, `digest.css`.

**Behaviour:**
- Right-rail drawer, collapsed by default. Topbar icon shows unread-entry badge.
- On open: renders today's digest grouped by section (Reconciliation, Wiki ↔ KB drift, Taxonomy, Stale, Edge audit).
- Each entry = one-line `line` text + `[apply]` and `[skip]` buttons.
- Applied entries: strikethrough, grey, timestamp suffix `applied HH:MM`.
- Skipped entries: hidden.
- `[mark read]` action writes to `digests/.read_marks`.

**Style:** Swiss/terminal — JetBrains Mono for entry ids `[r01]`, subtle borders between sections, orange accent on active section. No cards, no shadows.

**State:** Zustand store at `frontend/src/lib/digest-store.ts` — `{date, entries, loading, error}`. Invalidated on apply/skip. No optimistic updates — backend returns the post-mutation state, store replaces.

**REST API** — new routes in `backend/app/api/sb_api.py`:

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/sb/digest/today` | Today's structured digest + read status |
| POST | `/api/sb/digest/apply` | `{date, ids}` → `DigestApplier.apply` |
| POST | `/api/sb/digest/skip` | `{date, id, ttl_days?}` → `SkipRegistry.skip_by_id` |
| POST | `/api/sb/digest/read` | `{date}` → write to `digests/.read_marks` |

API handlers are thin shells around the same `second_brain.digest` modules the tool handlers use. Returns 404 when `SECOND_BRAIN_ENABLED=False`.

## 6. Repository deltas

```
claude-code-agent/
├── backend/
│   ├── app/
│   │   ├── api/sb_api.py                 # NEW — 4 digest routes
│   │   ├── hooks/
│   │   │   ├── sb_digest_hook.py         # NEW — pre-turn injection
│   │   │   └── tests/test_sb_digest_hook.py  # NEW
│   │   └── tools/
│   │       ├── sb_tools.py               # MODIFIED — +7 handlers
│   │       └── tests/test_sb_digest_tools.py # NEW
│   └── tests/api/test_sb_api.py          # NEW
└── frontend/
    └── src/
        ├── components/digest/            # NEW — Panel/Entry/Header + css
        │   └── __tests__/                # NEW — vitest
        └── lib/digest-store.ts           # NEW — Zustand store

second-brain/
└── src/second_brain/digest/
    └── builder.py                        # MODIFIED — merge pending.jsonl
    └── tests/test_digest_pending_merge.py # NEW
```

## 7. Data flow examples

### Apply from chat
```
User: "apply r01"
Agent → sb_digest_apply({ids: ["r01"]})
Bridge → DigestApplier.apply(cfg, today, ["r01"])
Applier → writes digests/YYYY-MM-DD.applied.jsonl
Bridge → returns {applied: ["r01"], skipped: [], failed: []}
Agent → "Applied r01 (upgrade confidence clm_foo low→medium)."
Frontend panel (next poll) → sees applied row → greys entry
```

### Propose during analysis
```
Agent is analysing a PR about auth middleware; notices it refutes clm_auth_x.
Agent → sb_digest_propose({
  section: "Reconciliation",
  action: {action: "resolve_contradiction", left_id: "clm_auth_x", right_id: "clm_auth_y", rationale: "new PR..."}
})
Bridge → appends to digests/pending.jsonl with proposed_id="pend_0001"
Returns → {ok: true, pending_id: "pend_0001", file: "~/second-brain/digests/pending.jsonl"}
(Tomorrow's builder merges this into the next digest as r03 or similar.)
```

## 8. Testing

| Layer | Path | Notes |
|---|---|---|
| Unit — tool handlers | `backend/app/tools/tests/test_sb_digest_tools.py` | All 7 handlers × (happy path, disabled, invalid args, invalid action) |
| Unit — hook | `backend/app/hooks/tests/test_sb_digest_hook.py` | Injection, read-mark, missing file, never-raise |
| Integration — API | `backend/tests/api/test_sb_api.py` | 4 routes via FastAPI TestClient |
| Unit — frontend | `frontend/src/components/digest/__tests__/` | vitest + RTL; entry states, panel empty/loading |
| Integration — sb | `tests/test_digest_pending_merge.py` (in sb repo) | Builder merges `pending.jsonl` into next digest |
| E2E | `frontend/tests/e2e/digest.spec.ts` | Playwright smoke — open, apply one, confirm strikethrough |

Coverage targets: ≥80% backend, ≥70% new frontend components.

## 9. Success criteria

1. Session start with unread digest → hook injects summary (trace-recorder observable).
2. `sb_digest_show` returns structured JSON, not raw markdown.
3. `sb_digest_apply` round-trips: chat call → `.applied.jsonl` line → panel greys entry.
4. `sb_digest_propose` → `pending.jsonl` line → next `sb digest build` absorbs it (integration test against real builder).
5. All 7 tools return `{ok: false, error: "second_brain_disabled"}` when flag off.
6. Panel renders 20 entries in <100ms with no layout shift.

## 10. Migration & rollout

- All additive; no schema migrations.
- Ships behind `SECOND_BRAIN_ENABLED` flag (already enforced).
- Pre-turn hook ships behind `SB_DIGEST_HOOK_ENABLED` (default true).
- Frontend panel hidden when `/api/sb/digest/today` returns 404.

## 11. Open questions (resolved for v1)

- **Propose timing:** pending entries merge into the *next* scheduled build, not the current day's. (Simpler; one concurrent write path per file.)
- **Hook injection frequency:** once per session, not per turn. Context drift would be annoying.
- **Panel poll interval:** 10 seconds while open, paused when hidden.

## Appendix — tool count

After v2-bridge ships:

| Existing | New | Total |
|---|---|---|
| sb_search, sb_load, sb_reason, sb_ingest, sb_promote_claim (5) | sb_digest_today, sb_digest_list, sb_digest_show, sb_digest_apply, sb_digest_skip, sb_digest_propose, sb_stats (7) | 12 |

12 is a lot. All live in `sb_tools.py`; if it grows past ~600 lines, split into `sb_tools/core.py` + `sb_tools/digest.py`.
