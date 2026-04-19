# Secondary Surfaces Pass — Design Spec

> Step 4 of the 5-part DS-Agent shell rebuild. Brings the four secondary IconRail surfaces (Knowledge, Memory, Library, Integrity) and a Settings overlay up to the same shell-foundation quality as the chat surface. Replaces the existing dump-style `HealthSection`, the placeholder `GraphPanel`/`DigestPanel`/`IngestPanel`, and the bare-bones `AgentsSection`/`SkillsSection`/`PromptsSection` with intentional, opinionated, controllable surfaces.

**Date:** 2026-04-19
**Sub-project:** 4 of 5
**Predecessors:** sub-project 1 (shell foundation, shipped) · 2 (chat surface, shipped) · 3 (dock + artifact viewer, shipped)
**Brainstorm decisions:** Q1=2 (Library = 3 IconRail siblings) · Q2=2 (Knowledge = wiki-first w/ drawers) · Q3=3 (Memory = two-pane live+durable) · Q4=3 (Integrity = top strip + agent self-report) · Q5=hybrid (Settings = subsystem groups + persistent search) · Q6=1 (umbrella + sequential sub-plans)

---

## Goals

1. **Replace dumps with dashboards.** The existing `HealthSection` reads a markdown blob; replace with a real surface that surfaces what's actionable. The existing `GraphPanel`/`IngestPanel`/`DigestPanel` are isolated drawers; merge into one Knowledge surface with a coherent lifecycle.
2. **Expose every knob.** A Settings overlay (⌘,) lets the user mutate runtime behavior without editing YAML — model routing, auto-dream cadence, ingest sources, integrity schedule, theme, hotkeys.
3. **Make memory and knowledge feel like different systems.** They are. Memory is the agent's working/episodic store with consolidation and forgetting; Knowledge is the curated, durable second brain.
4. **Establish a `<SurfacePage>` primitive.** All five surfaces share a header + body shape. Building it once keeps every surface coherent and saves churn for sub-project 5.
5. **Land a green build at every plan boundary.** No "in-progress" plans left half-merged.

---

## Non-Goals

- Memory backend implementation. The memory store already exists in `~/.claude/projects/.../memory/`; this spec only wires UI to read it. Live "auto-dream" is implemented if the backend endpoint exists; otherwise the button is wired to a stub that POSTs to a clearly-marked TODO endpoint.
- Wiki authoring UX (rich editor, slash commands, inline embeds). Wiki content is rendered read-only; edits open the underlying markdown file in the user's editor via a `vscode://` link or copy-path button.
- New skill or agent runtime semantics. Library surfaces existing API responses; it doesn't change what an agent or skill is.
- Mobile layout. Desktop only, matching predecessor scope.

---

## IconRail (final)

```
[Chat]                ⌘⇧1
[Knowledge]           ⌘⇧2     // replaces Graph + folds in Ingest, Digest
[Memory]              ⌘⇧3     // new
[Library: Agents]     ⌘⇧4
[Library: Skills]     ⌘⇧5
[Library: Prompts]    ⌘⇧6
[Integrity]           ⌘⇧7     // renamed from Health
                              // Context section retired (was redundant with dock)
                              // Digest, Ingest, Graph removed as standalone entries
─── (spacer) ───
[Theme toggle]
[Settings ⌘,]                 // overlay, not a destination
```

`SectionId` becomes:
```ts
export type SectionId =
  | 'chat'
  | 'knowledge'
  | 'memory'
  | 'agents'
  | 'skills'
  | 'prompts'
  | 'integrity'
  // legacy IDs kept as aliases for one release for migration:
  | 'graph' | 'digest' | 'ingest' | 'health' | 'context' | 'settings'
```

The `settings` activeSection becomes a no-op; the Settings overlay (`SettingsOverlay`) opens via Zustand state `settingsOverlayOpen` instead. Aliases route `graph→knowledge`, `digest→knowledge`, `ingest→knowledge`, `health→integrity`, `context→chat`, `settings→chat + open overlay`.

---

## Shared primitives (Plan A)

Built in `frontend/src/components/surface/`:

### `<SurfacePage>`

```tsx
interface SurfacePageProps {
  title: string                 // e.g. "Knowledge"
  eyebrow?: string              // small caps label above title, e.g. "SECOND BRAIN"
  toolbar?: ReactNode           // right-aligned actions
  drawer?: ReactNode            // optional right drawer slot (Knowledge)
  drawerOpen?: boolean
  onDrawerClose?: () => void
  children: ReactNode           // body
}
```

- Fixed header (sticky, 56px, `border-b border-line`, JetBrains Mono eyebrow, Inter title at `--text-2xl`).
- Body fills remaining height with internal scroll.
- Drawer slides in from the right at 384px; pushes body width via grid template, doesn't overlay (matches Dock pattern).

### `<SearchBar>`

```tsx
interface SearchBarProps {
  value: string
  onChange: (v: string) => void
  placeholder?: string
  hotkey?: string               // e.g. "/"
  ariaLabel: string
}
```

JBM 12.5px caret label, focus ring on focus, listens for `hotkey` to focus from anywhere within the surface. Used in Settings, Knowledge, Library.

### `<StatusTile>`

```tsx
interface StatusTileProps {
  label: string                 // "LINT"
  value: string | number        // "0 errors"
  status: 'ok' | 'warn' | 'err' | 'info' | 'idle'
  hint?: string                 // tooltip
  href?: string                 // optional click-through (anchor-style)
  onClick?: () => void
}
```

- 88px tall, full-width-of-cell tiles.
- `ok` = `--status-ok` border-bottom 2px, `warn` = amber, `err` = `--status-err`, `info` = `--acc-dim`, `idle` = `--line`.
- JBM uppercase label, Inter SemiBold value.

### `<DrawerSlot>`

Reused for Knowledge ingest/digest drawers and Memory detail. Same animation as Dock auto-collapse from sub-project 1 (`useAutoCollapse`).

### `<SettingsOverlay>`

```tsx
interface SettingsOverlayProps {
  open: boolean
  onClose: () => void
}
```

- ⌘, opens. Esc closes. Overlay scrim + centered panel, max-w 960px, max-h 80vh.
- Persistent search at top (focuses on open).
- Subsystem sections in scrollable left rail (Models, Sandbox, Memory, Ingest, Integrity, Theme, Hotkeys, Hooks).
- Right pane: settings for active section, OR (when search non-empty) flat list of matching settings across all sections, each with its `[group]` tag.
- Each setting row: label · current value · control · "Reset" inline · description text below in `--fg-2`.

---

## Per-surface designs

### Knowledge (Plan B)

**Layout.** Wiki-first with Ingest queue + Digest stream as drawers (Q2 decision = 2).

```
┌─────────────────────────────────────────────────────────────────┐
│  KNOWLEDGE  ▸  Wiki                          [Ingest 3] [Digest]│  ← SurfacePage header
├──────────┬───────────────────────────────────────┬──────────────┤
│  TREE    │  ARTICLE                              │ DRAWER (opt) │
│          │                                        │              │
│  • index │   # working.md                         │ Ingest queue │
│  • work… │                                        │  ─ pending 3 │
│  ▾ findi │   …rendered markdown…                  │  • file.csv  │
│    f-001 │                                        │  • email-12  │
│  ▾ adr   │                                        │  • web-abc   │
│  ▾ gotch │                                        │              │
└──────────┴───────────────────────────────────────┴──────────────┘
```

**Components:**
- `KnowledgeSurface` — owns drawer state (`'ingest' | 'digest' | null`), search, selected article path.
- `WikiTree` — left rail, 280px, `<aside>` with `role="tree"`. Reads from `/api/wiki/tree`. Folder nodes expand/collapse.
- `WikiArticle` — center, renders markdown via existing `MarkdownRenderer`. Header has article path + "Open in editor" link (`vscode://file/...`).
- `IngestDrawer` — drawer panel showing pending ingest items, source toggles (`docs/`, `email`, `urls`), "Trigger ingest" button.
- `DigestDrawer` — chronological list of digests (existing `DigestPanel` content, restyled into drawer).
- `<SearchBar>` in header filters tree.

**Backend touchpoints:**
- New: `GET /api/wiki/tree` → `[{path, name, type: 'file'|'dir', children}]` recursive
- New: `GET /api/wiki/article?path=...` → `{path, content, last_modified}`
- Existing: `/api/digest/*` (already wired in `chat_api.py` and `DigestPanel`)
- New stub: `GET /api/ingest/pending` → `[{id, source, name, queued_at}]`
- New stub: `POST /api/ingest/trigger` → fire-and-forget, returns 202

### Memory (Plan C)

**Layout.** Two-pane: live working memory (top, ~40% height) + durable store (bottom, ~60%) (Q3 decision = 3).

```
┌─────────────────────────────────────────────────────────────────┐
│  MEMORY                                  [Auto-dream] [Configure]│
├─────────────────────────────────────────────────────────────────┤
│  WORKING MEMORY   (this session)                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ recalled · user_role.md         · 2 min ago · "data sci…"   ││
│  │ recalled · feedback_testing.md  · 5 min ago · "no mocks…"   ││
│  │ pending  · proj_X_status.md     · just now  · candidate     ││
│  └─────────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────────┤
│  DURABLE STORE                       [filter: all ▾]  [search /] │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ feedback · accent_color · 2026-04-12 · "Claude orange…"     ││
│  │ project  · theme_dir    · 2026-04-18 · "light-default…"     ││
│  │ user     · role         · 2026-04-10 · "data scientist…"    ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

**Components:**
- `MemorySurface` — owns top/bottom split (resizable via existing `Resizer`).
- `WorkingMemoryPane` — list of in-session recalls + pending consolidation candidates. Each row: type badge · file name · age · snippet.
- `DurableStorePane` — list of all memory files. Filter dropdown by type (`all|user|feedback|project|reference`), search box, click row → detail drawer with full markdown + "Edit", "Delete", "Promote to wiki".
- Toolbar: "Auto-dream" button (POST `/api/memory/dream`) and "Configure" (opens Settings overlay scrolled to Memory section).

**Backend touchpoints:**
- New: `GET /api/memory/working` → `[{type, name, recalled_at, snippet, source: 'recalled'|'pending'}]`
- New: `GET /api/memory/durable` → `[{type, name, path, modified_at, snippet, content?}]`
- New: `GET /api/memory/durable/{name}` → full content
- New: `POST /api/memory/dream` → triggers consolidation (stub if backend doesn't exist; UI shows "queued" toast)

### Integrity (Plan D)

**Layout.** Top strip = pipeline tiles. Body = agent self-report (Q4 decision = 3, scope corrected to codebase integrity).

```
┌─────────────────────────────────────────────────────────────────┐
│  INTEGRITY  ·  2026-04-19          [Run integrity now] [History▾]│
├─────────────────────────────────────────────────────────────────┤
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌──────┐ ┌────────┐ │
│  │ A  │ │ B  │ │ C  │ │ D  │ │ E  │ │ F  │ │ LINT │ │AUTOFIX │ │
│  │ ok │ │ ok │ │warn│ │ ok │ │ ok │ │info│ │ 0 err│ │ 3 pend │ │
│  └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └──────┘ └────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  AGENT SELF-REPORT                                               │
│  ┌──────────────┬──────────────┬──────────────┬──────────────┐  │
│  │ TOKENS 7d    │ SKILLS USED  │ VALIDATIONS  │ GOTCHAS HIT  │  │
│  │ ▁▂▃▅▇▆▄ 240k │ 18 / 32      │ 92% pass     │ 2 today      │  │
│  └──────────────┴──────────────┴──────────────┴──────────────┘  │
│                                                                   │
│  RECENT ISSUES                                                   │
│  ─────────────────────────────────────────────────────────────  │
│  WARN  graph.drift.no_baseline · integrity-out/snapshots/       │
│        Yesterday's snapshot missing — drift evaluation skipped. │
│        [Apply autofix] [Dismiss]                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Components:**
- `IntegritySurface` — fetches `docs/health/latest.md` + `integrity-out/<latest>/{report.json,autofix.json}`.
- `PipelineStrip` — 8 `<StatusTile>` cells: A (graphify), B (graph_lint), C (config_registry), D (doc_audit), E (hooks_check), F (autofix), LINT, AUTOFIX-PENDING.
- `SelfReportGrid` — 4 tiles with sparklines/values (uses MCP/telemetry data; if not yet exposed, mock with TODO comment).
- `IssuesList` — paginated list of `report.json` issues with severity badge, rule, message, location, action buttons (only "Apply autofix" if a `fix_class` exists).
- Toolbar: "Run integrity now" (POST `/api/integrity/run`, stub if not wired) + "History" dropdown listing snapshot dates from `integrity-out/`.

**Backend touchpoints:**
- New: `GET /api/integrity/latest` → `{date, report, autofix, latest_md}`
- New: `GET /api/integrity/dates` → `["2026-04-19", "2026-04-17", ...]`
- New: `GET /api/integrity/by-date/{date}` → same shape as `/latest`
- New stub: `POST /api/integrity/run` → 202
- Optional: `GET /api/telemetry/agent-self-report` (skip if not available; tile shows "—")

### Library: Agents · Skills · Prompts (Plan E)

**Layout.** Each is `<SurfacePage>` with the same shape — list + detail.

```
┌─────────────────────────────────────────────────────────────────┐
│  AGENTS                                              [search /]  │
├──────────────────────┬──────────────────────────────────────────┤
│  LIST                │  DETAIL                                  │
│  ─────────           │  ──────                                  │
│  • code-reviewer     │  ## code-reviewer                         │
│  • planner           │  Reviews recent changes for quality…      │
│  • tdd-guide   (★)   │                                            │
│  • build-resolver    │  Recent invocations: 12 this week         │
│                       │  [Invoke] [Edit] [View full prompt]       │
└──────────────────────┴──────────────────────────────────────────┘
```

**Per-surface specifics:**

| Surface | Data source | Detail actions |
|---|---|---|
| Agents | `GET /api/agents` (existing or new — see below) | Invoke, Edit prompt, View invocation history |
| Skills | `GET /api/skills` (exists in `skills_api.py`) | Enable/disable, View source, Run eval, See usage telemetry |
| Prompts | `GET /api/prompts` (exists in `prompts_api.py`) | Edit, View version diff, Set as active |

If any of these APIs don't exist yet, ship the surface with read-only data from `~/.claude/agents/`, `backend/app/skills/registry`, `prompts/`. Mutations are stubbed (UI shows "Not yet implemented" toast).

**Components:**
- `LibrarySurface` (one component, parameterized by `kind: 'agents' | 'skills' | 'prompts'`).
- `LibraryList` — left rail, 320px, search-filterable.
- `LibraryDetail` — right pane, kind-specific.

---

## Settings overlay (Plan A, ships with primitives)

**Sections** (subsystem groups):

| Section | Settings (initial) |
|---|---|
| **Models** | `default_model`, `fallback_models`, `temperature_default`, `max_tokens_default` |
| **Sandbox** | `python_timeout_s`, `python_memory_mb`, `auto_capture_charts` (bool) |
| **Memory** | `auto_dream_cadence` (off / hourly / daily), `consolidation_threshold` (slider 0–1), `forgetting_age_days` |
| **Ingest** | per-source toggles (`docs/`, `email`, `urls`), `ingest_schedule` (off / hourly / daily) |
| **Integrity** | `integrity_schedule` (off / on commit / daily), `auto_apply_safe_fixes` (bool) |
| **Theme** | `theme` (light / dark / system), `density` (compact / comfy) |
| **Hotkeys** | view-only list of all hotkeys with rebind UI (rebind = stretch goal) |
| **Hooks** | enabled/disabled toggle per registered hook (read from `~/.claude/settings.json`) |

**Behavior:**
- Search filters across all sections; flat list view replaces tabbed view when search has 1+ char.
- Each setting POSTs to `/api/config/{section}/{key}` with `{value}`.
- Optimistic update; revert on 4xx/5xx with toast.
- "Reset to default" per setting; "Reset section" per section.

**Backend touchpoints:**
- New: `GET /api/config` → `{models: {...}, sandbox: {...}, memory: {...}, ...}`
- New: `PUT /api/config/{section}/{key}` body `{value}` → `{ok: true, value}`
- New: `POST /api/config/reset?scope=section&name=memory` (or `scope=key`)

If backend isn't wired, ship with localStorage-backed values + clear "(client-only)" badge per setting.

---

## State management

New Zustand store `frontend/src/lib/surfaces-store.ts`:

```ts
interface SurfacesStore {
  // Knowledge
  knowledgeDrawer: 'ingest' | 'digest' | null
  setKnowledgeDrawer: (d: 'ingest' | 'digest' | null) => void
  selectedWikiPath: string | null
  setSelectedWikiPath: (p: string | null) => void
  knowledgeSearch: string
  setKnowledgeSearch: (q: string) => void

  // Memory
  memorySplitFrac: number          // 0.4 default
  setMemorySplitFrac: (f: number) => void
  memoryFilter: 'all' | 'user' | 'feedback' | 'project' | 'reference'
  setMemoryFilter: (f: ...) => void
  memorySearch: string
  setMemorySearch: (q: string) => void
  selectedMemoryName: string | null

  // Integrity
  integrityDate: string | null     // ISO date or null = latest
  setIntegrityDate: (d: string | null) => void

  // Library
  selectedLibraryItemId: string | null
  setSelectedLibraryItemId: (id: string | null) => void

  // Settings overlay
  settingsOverlayOpen: boolean
  openSettings: () => void
  closeSettings: () => void
  settingsSearch: string
  setSettingsSearch: (q: string) => void
  settingsActiveSection: SettingsSection
  setSettingsActiveSection: (s: SettingsSection) => void
}
```

Persisted (localStorage `ds:surfaces`): `memorySplitFrac`, `memoryFilter`, `knowledgeDrawer`, `selectedWikiPath`, `settingsActiveSection`. Everything else session-scoped.

---

## File structure (created)

```
frontend/src/
├── components/
│   ├── surface/
│   │   ├── SurfacePage.tsx                    NEW (Plan A)
│   │   ├── SearchBar.tsx                      NEW (Plan A)
│   │   ├── StatusTile.tsx                     NEW (Plan A)
│   │   ├── DrawerSlot.tsx                     NEW (Plan A)
│   │   ├── surface.css                        NEW (Plan A)
│   │   └── __tests__/
│   ├── settings/
│   │   ├── SettingsOverlay.tsx                NEW (Plan A)
│   │   ├── SettingRow.tsx                     NEW (Plan A)
│   │   ├── sections/
│   │   │   ├── ModelsSection.tsx              NEW (Plan A)
│   │   │   ├── SandboxSection.tsx             NEW (Plan A)
│   │   │   ├── MemorySettingsSection.tsx      NEW (Plan A)
│   │   │   ├── IngestSettingsSection.tsx      NEW (Plan A)
│   │   │   ├── IntegritySettingsSection.tsx   NEW (Plan A)
│   │   │   ├── ThemeSection.tsx               NEW (Plan A)
│   │   │   ├── HotkeysSection.tsx             NEW (Plan A)
│   │   │   └── HooksSection.tsx               NEW (Plan A)
│   │   └── __tests__/
│   ├── knowledge/
│   │   ├── KnowledgeSurface.tsx               NEW (Plan B)
│   │   ├── WikiTree.tsx                       NEW (Plan B)
│   │   ├── WikiArticle.tsx                    NEW (Plan B)
│   │   ├── IngestDrawer.tsx                   NEW (Plan B)
│   │   ├── DigestDrawer.tsx                   NEW (Plan B)
│   │   └── __tests__/
│   ├── memory/
│   │   ├── MemorySurface.tsx                  NEW (Plan C)
│   │   ├── WorkingMemoryPane.tsx              NEW (Plan C)
│   │   ├── DurableStorePane.tsx               NEW (Plan C)
│   │   ├── MemoryDetailDrawer.tsx             NEW (Plan C)
│   │   └── __tests__/
│   ├── integrity/
│   │   ├── IntegritySurface.tsx               NEW (Plan D)
│   │   ├── PipelineStrip.tsx                  NEW (Plan D)
│   │   ├── SelfReportGrid.tsx                 NEW (Plan D)
│   │   ├── IssuesList.tsx                     NEW (Plan D)
│   │   └── __tests__/
│   └── library/
│       ├── LibrarySurface.tsx                 NEW (Plan E)
│       ├── LibraryList.tsx                    NEW (Plan E)
│       ├── LibraryDetail.tsx                  NEW (Plan E)
│       ├── kinds/
│       │   ├── AgentDetail.tsx                NEW (Plan E)
│       │   ├── SkillDetail.tsx                NEW (Plan E)
│       │   └── PromptDetail.tsx               NEW (Plan E)
│       └── __tests__/
├── lib/
│   ├── surfaces-store.ts                      NEW (Plan A)
│   └── api/
│       ├── wiki.ts                            NEW (Plan B)
│       ├── memory.ts                          NEW (Plan C)
│       ├── integrity.ts                       NEW (Plan D)
│       └── library.ts                         NEW (Plan E)
└── App.tsx                                    EDIT — route to new sections
```

Backend (only the read endpoints needed to unblock the frontend; mutation endpoints can land later as stubs):

```
backend/app/api/
├── wiki_api.py                                NEW (Plan B)
├── memory_api.py                              NEW (Plan C)
├── integrity_api.py                           NEW (Plan D)
├── ingest_api.py                              NEW (Plan B) — pending list + trigger stub
└── config_api.py                              EDIT — extend with /api/config CRUD
```

Sections to retire (after migration aliases hold for one release):
```
frontend/src/sections/HealthSection.tsx          → IntegritySurface
frontend/src/sections/ContextSection.tsx         → removed (dock covers it)
frontend/src/sections/AgentsSection.tsx          → LibrarySurface
frontend/src/sections/SkillsSection.tsx          → LibrarySurface
frontend/src/sections/PromptsSection.tsx         → LibrarySurface
frontend/src/sections/SettingsSection.tsx        → SettingsOverlay
frontend/src/components/panels/GraphPanel.tsx    → KnowledgeSurface
frontend/src/components/panels/IngestPanel.tsx   → IngestDrawer (content port)
frontend/src/components/panels/DigestPanel.tsx   → DigestDrawer (content port)
```

---

## Visual / typographic rules (carried from sub-project 1)

- All eyebrows, status labels, tile labels: JetBrains Mono uppercase, `--text-xs`, `letter-spacing: 0.06em`, `--fg-2`.
- All page titles: Inter SemiBold, `--text-2xl`, `--fg-0`.
- Tile values: Inter SemiBold, `--text-xl`, `--fg-0`.
- Metadata (timestamps, paths, sizes): JBM, `--text-xs`, `--fg-3`.
- Single accent color (Claude orange `--acc`) used only for active state, primary action buttons, focus ring.
- No purple anywhere. No gradients. Borders are 1px `--line`.

---

## Build order (sequential plans)

1. **Plan A — Shared primitives + Settings overlay** (Plan file: `2026-04-19-secondary-surfaces-plan-a-primitives.md`)
2. **Plan B — Knowledge surface** (Plan file: `2026-04-19-secondary-surfaces-plan-b-knowledge.md`)
3. **Plan C — Memory surface** (Plan file: `2026-04-19-secondary-surfaces-plan-c-memory.md`)
4. **Plan D — Integrity surface** (Plan file: `2026-04-19-secondary-surfaces-plan-d-integrity.md`)
5. **Plan E — Library surfaces** (Plan file: `2026-04-19-secondary-surfaces-plan-e-library.md`)

Each plan ends green: `pnpm build` passes, vitest passes, no TS errors. The umbrella plan file (`2026-04-19-secondary-surfaces-plan.md`) is the index pointing to the five sub-plans.

---

## Risks / open questions

- **Backend endpoint scope.** Frontend needs ~10 new endpoints. If full implementation takes too long, ship with read-only stubs that return mocked data so the surfaces are usable; mark mutations clearly. Captured in each plan.
- **Memory backend semantics.** The `~/.claude/projects/.../memory/` files are owned by the Claude Code memory subsystem, not this app. The Memory surface reads these directly (filesystem) or via a new `memory_api.py` that resolves the path. Writes (auto-dream, edit) require backend cooperation — defer to stubs if unclear.
- **Integrity self-report data.** The "tokens used / skills run / validations passed" tiles depend on telemetry that may not be wired through `/api/telemetry`. If unavailable, tiles show "—" with a tooltip explaining and a TODO comment in code.
- **Hotkey conflicts.** Adding ⌘⇧4–7 conflicts with browser tab nav; verify in Chrome/Safari and reassign if needed.
