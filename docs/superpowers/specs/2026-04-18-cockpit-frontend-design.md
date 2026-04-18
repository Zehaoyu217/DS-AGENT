# Cockpit Frontend Design

**Status:** Locked 2026-04-18
**Replaces:** current `App.tsx` top-level shell (icon rail + drawer stack + middle Conversation|DevTools tabs + right-rail panel)
**Scope:** Frontend shell and navigation only. Backend API surface, agent runtime, and skill registry are unchanged.

---

## 1. Goal

Replace the current drawer-heavy, tab-duplicating frontend shell with a single chat-centric cockpit: one persistent layout where the conversation is the product, live telemetry is always visible, and knowledge surfaces (GRAPH / DIGEST / INGEST) are summoned on demand into the right rail.

## 2. Users and constraints

- **Users:** MLEs, data scientists, quants running pressure-test experiments. Technical power users. Expect information density, keyboard-first interactions, authoritative state surfacing. No hand-holding.
- **Aesthetic:** Swiss / Terminal. JetBrains Mono at the system level. Dark-only. Claude orange `#e0733a` is the one accent; `#f2a277` for the lighter tint. See `.impeccable.md`.
- **Non-goals:** No visual language rewrite. No component-library swap. No light mode. No consumer-y chat UI gestures (floating bubbles, gradient avatars, soft shadows).

## 3. Design decisions (locked)

| Decision | Choice | Rationale |
|---|---|---|
| Top-level paradigm | Cockpit (chat + persistent HUD + always-on right rail) | Chat is the primary surface; every state stays visible without opening drawers |
| HUD density | Verbose | Power users want cost, tokens, latency, streaming, skills count, KB status, and last tool all visible simultaneously |
| Session switcher | Dropdown from the `SESSION ▾` chip in the HUD (⌘P opens) | No dedicated sidebar section for sessions; keeps left rail reserved for domain surfaces |
| Right-rail behavior | Swap-in-place: trace is default, summoned drawers replace it temporarily | Simpler than split or third-rail; maintains focus; ⌘\ or back-arrow returns to trace |
| Trace rail modes | 3-mode tabs: `TIMELINE` · `CONTEXT` · `RAW` | Timeline = event list; Context = current turn's tool/skill calls grouped; Raw = JSON stream for debugging |
| Summoned drawers | `GRAPH`, `DIGEST`, `INGEST` (chips right-aligned in HUD) | The three knowledge surfaces that interrupt flow; HEALTH and SKILLS live as sections, not drawers |
| Left sections (7) | `CHAT` (default), `AGENTS`, `SKILLS`, `PROMPTS`, `CONTEXT`, `HEALTH`, `SETTINGS` | One home per concept; no duplication between section and drawer |
| Removed | Middle `Conversation | DevTools` tabs; `HEALTH` drawer; `SKILLS` drawer | DevTools becomes the right-rail trace + a standalone `/devtools` route; HEALTH and SKILLS are sections only |

## 4. Layout

```
┌────────────────────────────────────────────────────────────────────────────┐
│ TOP HUD (28px · spans all columns)                                         │
│ SESSION abc123f ▾ · opus-4.7 · $0.04 ($0.80/day) · 2,184/200k · 3.2s ·     │
│ ● STREAMING · SKILLS 7/0 · KB OK · last: grep       [GRAPH][DIGEST][INGEST]│
├────┬──────────────────────────────────────────────────┬────────────────────┤
│ 44 │                                                  │ TRACE RAIL (320px) │
│ px │              CHAT MAIN                           │  ┌──────────────┐  │
│    │              (user + agent turns, tool blocks,   │  │TIMELINE CTX R│  │
│ C  │              streaming cursor, input at bottom)  │  ├──────────────┤  │
│ A  │                                                  │  │ event list   │  │
│ S  │                                                  │  │ auto-scroll  │  │
│ P  │                                                  │  │ ● STREAMING  │  │
│ C  │                                                  │  └──────────────┘  │
│ H  │                                                  │                    │
│ S  │                                                  │  swap target for   │
│ ─  │                                                  │  GRAPH/DIGEST/     │
│ ⚙  │                                                  │  INGEST chips      │
└────┴──────────────────────────────────────────────────┴────────────────────┘
```

Fixed dimensions:
- Top HUD: `28px` height
- Left icon rail: `44px` width
- Right rail: `320px` width (fixed, not resizable in v1)
- Chat main: flexes to fill; max-width `~760px` centered within its column for readability on wide screens
- Minimum supported viewport: `1280 × 720`. Below `1024px` wide the right rail collapses behind the summon chips (trace becomes a toggleable overlay) — out of scope for v1 but the layout should not break.

## 5. Component inventory

### 5.1 `<TopHUD>`
Single horizontal strip, JetBrains Mono `9px` uppercase labels, `#71717a` for label copy, `#e5e5e5` for values, `#e0733a` for interactive chips.

Left cluster (session + live state):
- `SESSION <shortId> ▾` — clickable; opens `<SessionDropdown>` (see 5.2). Chip colored `#e0733a`.
- `model` — static text, e.g. `opus-4.7`
- `cost` — `$X.XX ($Y.YY/day)`, where per-day is rolling 24h spend
- `tokens` — `used / budget`, color flips to `#f59e0b` at 80% and `#ef4444` at 95%
- `latency` — last-turn p50 in seconds
- `status` — `● STREAMING` (`#22c55e`), `● IDLE` (`#71717a`), `● ERROR` (`#ef4444`)
- `SKILLS <calls>/<failures>` — today's count; failures in `#ef4444` when > 0
- `KB <status>` — `OK` (green), `DISABLED` (muted), `DEGRADED` (amber)
- `last: <tool>` — most recent tool name

Right cluster (summon chips):
- `GRAPH`, `DIGEST`, `INGEST` — bordered `1px #3f3f46`, active state `1px #e0733a` + `#e0733a` text. Clicking toggles the corresponding drawer in the right rail.

Keyboard: `⌘P` focuses `SESSION ▾` and opens the dropdown.

### 5.2 `<SessionDropdown>`
Anchored to `SESSION ▾` chip, `240px` wide, surfaces `#0c0c0e` with `1px #27272a` border. Rows:
- `+ NEW SESSION` (⌘N)
- separator
- Current session (highlighted, `#e0733a`)
- Recent sessions (up to 8), each row: `<shortId>  <first-user-msg-truncated>  <relative-time>`

Closes on outside click, `Esc`, or selection. Selecting a session fires `sessionStore.switch(id)`.

### 5.3 `<LeftIconRail>`
`44px` wide, `#0c0c0e` background, `1px #27272a` right border. Icons are `32 × 32` glyph squares with `7px` uppercase label beneath each. Sections in order:

1. `CHAT` (`▣`) — default cockpit view (this spec)
2. `AGENTS` (`◇`) — `/agents` route; list of agent definitions
3. `SKILLS` (`◈`) — `/skills` route; skill registry + eval status
4. `PROMPTS` (`¶`) — `/prompts` route; saved prompts
5. `CONTEXT` (`≡`) — `/context` route; layer tracking, compaction view
6. `HEALTH` (`♥`) — `/health` route; system health
7. (separator `1px #27272a`)
8. `SETTINGS` (`⚙`, bottom-anchored) — `/settings`

Active section: `background rgba(224,115,58,0.12)` + `#e0733a` icon + `#e0733a` label. Inactive: `#52525b` icon, `#71717a` label on hover.

### 5.4 `<ChatMain>`
Column: `{ messages, composer }`. Messages area has `padding 18px 36px`, `gap 14px` between turns, max content width `~760px`.

**Turn shape:**
- Role label: `9px` uppercase, `letter-spacing 0.18em`, role color (`#e0733a` for user/agent, `#71717a` for system)
- Timestamp: same line as role label, `#71717a`
- Body: `11px/1.6` prose or monospace tool blocks
- Tool-call block: `padding 6px 10px`, `background #0f0f12`, `border-left 2px solid #e0733a`, content `10px` monospace. Label `› tool` in `#71717a`, then tool name, then args in `#f2a277`
- Streaming cursor: `▊` at the end of the last agent turn while `status === 'streaming'`

**Composer:**
- `padding 10px 36px` on `#0c0c0e` with `1px #27272a` top border
- Input: `1px #27272a` border, no background, `11px`, placeholder `#71717a`
- Shortcut legend below input (`9px`, `#52525b`): `⌘L focus · ⌘K palette · ⌘P session · ⌘\ trace tab`
- Enter submits, Shift+Enter newline, Esc blurs

### 5.5 `<RightRail>`
Container that holds either `<TraceRail>` (default) or one of the summoned drawers (`<GraphDrawer>`, `<DigestDrawer>`, `<IngestDrawer>`). Exactly one is rendered at a time; state lives in `rightRailStore.mode: 'trace' | 'graph' | 'digest' | 'ingest'`.

When a summoned drawer is active:
- Drawer header shows `← GRAPH` (back-arrow returns to trace)
- HUD chip for that drawer gets the active outline (`#e0733a`)
- Trace continues accumulating events silently; when user returns, auto-scroll jumps to latest

Keyboard: `⌘\` cycles `trace → graph → digest → ingest → trace`.

### 5.6 `<TraceRail>` (3-mode)
Header: three tabs — `TIMELINE`, `CONTEXT`, `RAW` — plus right-aligned event count (`N events`, `#3f3f46`).

- **TIMELINE:** flat chronological event list. Each row: `<HH:MM:SS> · <kind> <detail> <duration>`. Kinds: `user`, `tool`, `skill`, `model`, `chunk`, `error`. Streaming stream chunks are grouped after the `model stream` row with a `▊ STREAMING` badge at the bottom. Color mapping: kind in `#f2a277`, detail in `#a1a1aa`, duration in `#3f3f46`.
- **CONTEXT:** groups events by turn. Current turn expanded at top with tool/skill calls indented under the user message. Completed turns collapse to a one-line summary; expand on click.
- **RAW:** raw JSON stream from `/api/agent/events` SSE (or equivalent). Pretty-printed, `9px` monospace, copyable. Used for debugging, not daily driving.

Footer: `auto-scroll on` indicator + `⌘\ to switch`. Auto-scroll disables when user scrolls up; re-enables on arrival at bottom.

### 5.7 Summoned drawers

All three follow the same header pattern (`← <NAME>` + close `×`), then drawer-specific body. They preserve internal state across summon/dismiss within a session.

- `<GraphDrawer>`: graphify output preview. Node/edge count, center node, SVG thumbnail, `OPEN FULL` link to `/graph`.
- `<DigestDrawer>`: pending digest + recent digest snapshot. Expand to see merged entries.
- `<IngestDrawer>`: the existing panel (file + URL modes + recent ingests). Already implemented in `frontend/src/components/ingest/IngestPanel.tsx` — moves into the right rail slot without structural change.

## 6. Color palette (source of truth)

Derived from current codebase usage; all tokens already present in `frontend/src`.

| Token | Value | Use |
|---|---|---|
| `--accent` | `#e0733a` | Primary accent; active chips, focused borders, user/agent role labels, user-visible interactive states |
| `--accent-soft` | `#f2a277` | Secondary accent; tool-call args, hover highlights |
| `--bg-base` | `#09090b` | App background |
| `--bg-elevated` | `#0c0c0e` | HUD, rails, drawer surfaces |
| `--bg-inset` | `#0f0f12` | Tool-call inline blocks |
| `--bg-alt` | `#18181b` | Alternate surface (cards where still used) |
| `--border` | `#27272a` | Primary separator |
| `--border-strong` | `#3f3f46` | Secondary separator, button borders |
| `--text-primary` | `#e5e5e5` | Body text, values |
| `--text-muted` | `#a1a1aa` | Secondary text |
| `--text-subtle` | `#71717a` | Labels, metadata |
| `--text-faint` | `#52525b` | Icon rail inactive, shortcuts |
| `--ok` | `#22c55e` | Streaming, healthy KB |
| `--warn` | `#f59e0b` | Token budget ≥80%, degraded KB |
| `--err` | `#ef4444` | Errors, skill failures, token budget ≥95% |

No purple. No gradients. No decorative color.

## 7. Routing

Cockpit is the default route `/` (or `/session/:id`). Left rail icons deep-link:

| Icon | Route |
|---|---|
| CHAT | `/` or `/session/:id` |
| AGENTS | `/agents` |
| SKILLS | `/skills` |
| PROMPTS | `/prompts` |
| CONTEXT | `/context` |
| HEALTH | `/health` |
| SETTINGS | `/settings` |

`/devtools` exists as a standalone route reachable via `⌘⇧D` or from `SETTINGS → Developer`. It mirrors the TIMELINE/CONTEXT/RAW rail at full viewport width for deep debugging.

## 8. State

Frontend state is Zustand, as today.

- `sessionStore` — active session id, recent sessions, HUD chip data (cost, tokens, latency, streaming status, skills count, KB status, last tool). Subscribes to `/api/session/:id/events` SSE.
- `rightRailStore` — `{ mode: 'trace' | 'graph' | 'digest' | 'ingest', traceTab: 'timeline' | 'context' | 'raw' }`. Persisted per-session to `localStorage`.
- `traceStore` — append-only event buffer, capped at 2,000 events per session with ring buffer eviction.
- Existing stores (`ingest-store`, skill/graph/digest stores) keep their current shape; they just become slices the drawer consumers read.

## 9. Migration notes (what's removed)

1. **Middle `Conversation | DevTools` tabs** — delete `SessionLayout`'s tab strip. DevTools content migrates: the live feed moves to `<TraceRail>`; the deep debug view lives at `/devtools`.
2. **HEALTH topbar drawer** — removed. Health remains a left-rail section at `/health`.
3. **SKILLS topbar drawer** — removed. Skills remain a left-rail section at `/skills`.
4. **`App.tsx`** — top-level shell rewritten. Current structure (IconRail + TopbarButton[] overlay drawers + SessionLayout) collapses into: `<TopHUD />` + `<LeftIconRail />` + `<Routes />` where the `/` route renders `<Cockpit />` which composes `<ChatMain />` + `<RightRail />`.

No backend changes. No store schema changes beyond the new `rightRailStore`.

## 10. Testing

Playwright coverage (the e2e harness already exists):

1. HUD renders all chips with live values within 500ms of session load.
2. `SESSION ▾` click opens dropdown; selecting a different session swaps route to `/session/:newId`.
3. Clicking `GRAPH` chip swaps right rail body; trace is hidden; `← GRAPH` returns to trace.
4. `⌘\` cycles rail state through `trace → graph → digest → ingest → trace`.
5. Trace auto-scroll pauses when user scrolls up and resumes on bottom re-entry.
6. Tokens HUD flips to `#f59e0b` at 80% and `#ef4444` at 95% (visual regression screenshot).
7. Left rail `SKILLS` icon navigates to `/skills`; the old drawer no longer exists.

Vitest coverage:
- `rightRailStore` transitions (trace→graph→trace, cycle, dismiss).
- `traceStore` ring-buffer eviction at 2,000 events.
- HUD selectors return correct derived values from `sessionStore`.

## 11. Out of scope (v1)

- Resizable right rail
- Multi-session tiling
- Light theme polish
- `/devtools` route redesign (ships as a minimal mirror of the trace rail)
- Mobile/narrow-viewport behavior below 1024px
- Drag-and-reorder of left rail sections
