# Secondary Surfaces — Umbrella Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement each sub-plan task-by-task.

**Goal:** Ship the 4 secondary surfaces (Knowledge, Memory, Integrity, Library) plus a Settings overlay, replacing the existing dump-style sections from sub-projects 1–3.

**Architecture:** Five sequential sub-plans. Plan A delivers shared primitives (`<SurfacePage>`, `<SearchBar>`, `<StatusTile>`, `<DrawerSlot>`, `<SettingsOverlay>`) that all subsequent plans consume. Plans B–E each build one surface end-to-end (UI + thin API) and ship green.

**Tech Stack:** React + Vite + TypeScript + Tailwind + Zustand + Zod (existing). Backend: FastAPI (existing).

**Spec:** `docs/superpowers/specs/2026-04-19-secondary-surfaces-design.md`

---

## Sub-plans

| # | Name | File | Status |
|---|---|---|---|
| A | Shared primitives + Settings overlay | `2026-04-19-secondary-surfaces-plan-a-primitives.md` | TBD |
| B | Knowledge surface (Wiki + Ingest + Digest) | `2026-04-19-secondary-surfaces-plan-b-knowledge.md` | TBD |
| C | Memory surface (live + durable) | `2026-04-19-secondary-surfaces-plan-c-memory.md` | TBD |
| D | Integrity surface (rename Health) | `2026-04-19-secondary-surfaces-plan-d-integrity.md` | TBD |
| E | Library surfaces (Agents · Skills · Prompts) | `2026-04-19-secondary-surfaces-plan-e-library.md` | TBD |

Execute in order. Each plan ends with `pnpm build` + `pnpm test` green and a single feature commit.

---

## Cross-cutting tasks (do these once, before Plan A)

### Task X1: Update `SectionId` and IconRail
**Files:**
- Modify: `frontend/src/lib/store.ts:90-100`
- Modify: `frontend/src/components/layout/IconRail.tsx:32-42`
- Modify: `frontend/src/App.tsx:280-303`

- [ ] Add `'knowledge' | 'memory' | 'integrity'` to `SectionId`
- [ ] Update `SECTIONS` in `IconRail.tsx`: replace Health/Graph/Digest/Ingest/Context with Knowledge / Memory / Integrity; reorder to spec
- [ ] Add legacy alias mapping in `setActiveSection`: `graph|digest|ingest → knowledge`, `health → integrity`, `context → chat`, `settings → chat + open overlay`
- [ ] Update `App.tsx` switch to route new sections to placeholder components (real components land in subsequent plans)
- [ ] Commit: `feat(shell): rename secondary section ids and IconRail entries`

### Task X2: Add `surfaces-store.ts` skeleton
**Files:** Create `frontend/src/lib/surfaces-store.ts`

- [ ] Implement Zustand store per spec
- [ ] Persist (localStorage `ds:surfaces`): `memorySplitFrac`, `memoryFilter`, `knowledgeDrawer`, `selectedWikiPath`, `settingsActiveSection`
- [ ] Unit test for default state + persistence
- [ ] Commit: `feat(shell): add surfaces-store for secondary-surface UI state`

---

## Self-review (run after all plans done)

1. Every spec section maps to a task in some plan.
2. No "TODO" / "TBD" left in shipped code (only in clearly-marked stub endpoints).
3. All five surfaces use `<SurfacePage>` — no ad-hoc page chrome.
4. Settings overlay opens with ⌘, from any surface.
5. Legacy section IDs still navigate correctly via aliases.
6. `pnpm build` + `pnpm test` green on the umbrella merge commit.
