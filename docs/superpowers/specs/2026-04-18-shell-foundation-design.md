# Shell Foundation — Tokens & 4-Pane App Shell

**Status:** Approved 2026-04-18
**Sub-project:** 1 of 5 in the DS-Agent handoff recreation
**Follow-ups:** Chat view (step 2), Dock bodies (step 3), Thread list + Command Palette polish (step 4), Tweaks panel (step 5)

## Motivation

The `design_handoff_ds_agent/` bundle describes a four-pane analytical-agent workspace with a specific density, typography, and interaction model. The current frontend has a three-region `Cockpit` (`TopHUD | ChatMain | RightRail`) whose chrome conflicts with the target: a top status bar the handoff removes on purpose, a right rail that toggles between `trace / graph / digest / ingest` "summon" modes that don't map to the handoff's Progress / Context / Artifacts Dock, and a TopHUD that owns context the handoff gives to the chat header. Retrofitting section-by-section produces two competing shell designs fighting each other.

Step 1 replaces the shell wholesale — tokens, typography, layout, resize/persist plumbing, IconRail visuals — while leaving chat internals and Dock tab bodies for follow-up sub-projects. The goal is to land a shell that every subsequent step can drop content into without rework.

## Outcome

After step 1 is merged:

- The app uses the handoff's four-pane layout: `IconRail (52px fixed) | ThreadList (200px default, 160–360px range, resizable, hideable) | Conversation (flex) | Dock (320px default, 240–480px range, resizable, hideable)`.
- Light is the default theme. Dark is opt-in via the theme toggle; both palettes are first-class and pixel-faithful to `design_handoff_ds_agent/tokens.css`.
- Typography is the handoff's three-face stack: Inter sans (self-hosted, 400/500/600/700), Charter/Iowan Old Style/Palatino serif (OS-provided fallbacks), JetBrains Mono (self-hosted, 400/500/600). Body 13.5px / 1.5 / -0.003em.
- IconRail adopts handoff visuals (52px, top-aligned, 2px accent left bar + `--acc-dim` wash for active, flyout tooltip with label + keyboard hint, bespoke `sidebar` / `sidebarOn` filled-variant pair for the threads toggle). Eleven sections (Chat, Agents, Skills, Prompts, Context, Health, Graph, Digest, Ingest + Theme toggle + Settings).
- All resize widths and toggle states persist to localStorage under a single `ds:ui` key (plus legacy aliases `ds:threadW` / `ds:dockW` for direct handoff-parity debugging).
- The previous `RightRail` "summon" modes (`graph`, `digest`, `ingest`) are promoted to full IconRail sections; `right-rail-store.ts` is deleted.
- The `TraceRail` content lives inside the Dock's Progress tab (its own body stays untouched in step 1 so trace keeps working; step 3 rewrites it against the handoff Progress-tab spec).
- Narrow-viewport auto-collapse fires at `<1100px` (threads hide) and `<900px` (dock hides), with manual-override precedence until the next resize crossing.
- `TopHUD` is deleted. Chat header responsibilities move to the Conversation pane's own header toolbar (step 2).
- Build is green: `pnpm lint`, `pnpm typecheck`, `pnpm test`, and Playwright visual regression at 320 / 768 / 1100 / 1440 × light / dark all pass.

## Non-Goals

- Rewriting chat internals (messages, tool-call chips, composer, slash-commands). Step 2.
- Real Dock tab bodies for Progress (timeline), Context (vars/df/files), Artifacts (mini-grid + viewer). Step 3. Step 1 ships the Dock shell with tabs wired; Progress wraps existing `TraceRail`; Context + Artifacts render handoff-styled empty stubs.
- Command Palette redesign. Step 4 — palette keeps its current visuals and behavior in step 1.
- Tweaks panel (theme / accent / density / dock-position / message-style / thinking-mode / UI-font). Step 5.
- Changing any backend API, store schema unrelated to UI state, or agent behavior.

## Architecture

### File layout

```
frontend/
├── public/fonts/
│   ├── Inter-Regular.woff2       (new)
│   ├── Inter-Medium.woff2         (new)
│   ├── Inter-SemiBold.woff2       (new)
│   ├── Inter-Bold.woff2           (new)
│   ├── JetBrainsMono-Regular.woff2 (existing)
│   ├── JetBrainsMono-Medium.woff2  (existing)
│   └── JetBrainsMono-SemiBold.woff2 (new)
├── src/
│   ├── components/
│   │   ├── shell/
│   │   │   ├── AppShell.tsx       (new — composes IconRail + ThreadList + Conversation + Dock)
│   │   │   ├── ThreadList.tsx     (new — sectioned list + header toolbar)
│   │   │   ├── Dock.tsx           (new — tab bar + tab body slot + resize edge)
│   │   │   ├── Resizer.tsx        (new — drag + keyboard resize)
│   │   │   ├── shell.css          (new — tokens-only CSS; everything else is Tailwind)
│   │   │   └── __tests__/
│   │   │       ├── Resizer.test.tsx
│   │   │       ├── ThreadList.test.tsx
│   │   │       └── AppShell.test.tsx
│   │   └── layout/
│   │       └── IconRail.tsx       (rewritten — 52px, handoff visuals, 11 sections + theme + settings)
│   ├── hooks/
│   │   ├── useViewportWidth.ts    (new — vw with rAF-throttled resize)
│   │   └── useAutoCollapse.ts     (new — manages threadsOpen/dockOpen based on vw + manual override)
│   ├── lib/
│   │   ├── ui-store.ts            (new — Zustand + persist; UI state only)
│   │   ├── shortcuts.ts           (modified — add OPEN_GRAPH, OPEN_DIGEST, OPEN_INGEST, TOGGLE_DOCK)
│   │   └── store.ts               (modified — SectionId union adds 'graph' | 'digest' | 'ingest')
│   └── styles/
│       ├── tokens.css             (new — full handoff token system, both themes, keyframes, @layer components)
│       └── globals.css            (modified — import tokens.css first; add Inter @font-face; alias legacy --color-* vars)
└── tailwind.config.ts             (modified — darkMode selector, colors, fonts, radii, keyframes/animations)
```

### Files deleted

- `frontend/src/components/cockpit/Cockpit.tsx`
- `frontend/src/components/cockpit/TopHUD.tsx`
- `frontend/src/components/cockpit/RightRail.tsx`
- `frontend/src/components/cockpit/cockpit.css`
- `frontend/src/components/cockpit/__tests__/Cockpit.test.tsx` (if present)
- `frontend/src/lib/right-rail-store.ts`
- `frontend/src/components/cockpit/SessionDropdown.tsx` (audit confirmed: only consumed by TopHUD, which is also deleted)

### Preserved untouched by step 1

- `frontend/src/components/cockpit/ChatMain.tsx` — becomes the Conversation pane body for the `chat` section. Step 2 rewrites its internals.
- `frontend/src/components/cockpit/TraceRail.tsx` — consumed by `Dock` as the Progress tab's body in step 1; step 3 rewrites against the handoff Progress spec.
- `frontend/src/components/cockpit/trace/**` — sub-pieces that TraceRail depends on. Left alone.
- All `sections/*Section.tsx` — render full-bleed inside the Conversation pane when their section is active.
- All `components/monitor/**` — `/#/monitor/:id` route unaffected.

### Component contracts

```tsx
// AppShell.tsx
interface AppShellProps {
  children: ReactNode  // rendered inside the Conversation pane
}
// Responsibilities:
//  - Renders IconRail, ThreadList (chat section only), Conversation (children), Dock (chat section only)
//  - Mounts Resizers between ThreadList/Conversation and Conversation/Dock
//  - Subscribes to ui-store for threadW/dockW/threadsOpen/dockOpen/dockTab
//  - Mounts useAutoCollapse() which reconciles vw against user overrides

// ThreadList.tsx
interface ThreadListProps {
  width: number          // current resolved width from ui-store
  onClose: () => void    // header "x" toggles visibility
}
// Responsibilities:
//  - Renders header (label "Chats" + "+" new-chat button + close chevron)
//  - Sectioned list from useChatStore.conversations, grouped by recency
//  - Active conversation gets --acc-dim wash + 2px left accent border
//  - Archive button at footer

// Dock.tsx
interface DockProps {
  width: number
  onClose: () => void
}
// Responsibilities:
//  - 40px tab bar (Progress / Context / Artifacts) with active underline + accent icon
//  - Close chevron at far right
//  - Tab body:
//      'progress' → <TraceRail /> (existing component)
//      'context'  → <DockContextStub />  (handoff-styled empty state)
//      'artifacts'→ <DockArtifactsStub /> (handoff-styled empty state)

// Resizer.tsx
interface ResizerProps {
  axis: 'x' | 'y'           // x = vertical handle (resize left↔right), y = horizontal (top↔bottom)
  min: number
  max: number
  value: number
  onChange: (next: number) => void
  ariaLabel: string
  invert?: boolean          // true when dragging "right" decreases value (dock edge)
}
// Responsibilities:
//  - 4px hit zone with col-resize/row-resize cursor
//  - Pointer drag → onChange (clamped to [min, max])
//  - Keyboard: ArrowLeft/Right (or Up/Down for axis=y) ±10px, Home/End snap to min/max
//  - Visible focus ring via .focus-ring

// useViewportWidth.ts
function useViewportWidth(): number
// rAF-throttled window.innerWidth; updates on resize + orientationchange

// useAutoCollapse.ts
function useAutoCollapse(): void
// Mounts in AppShell. Watches vw from useViewportWidth + a userOverride flag in ui-store.
// When vw crosses 1100px boundary, reset userOverride-threads and auto-open/close threads.
// Same for vw crossing 900px boundary with dock.
// Manual toggles set userOverride-threads=true (or -dock=true) which freezes auto-collapse
// until vw crosses the boundary again.
```

### UI store (ui-store.ts)

```ts
// Public surface
interface UiStore {
  // Persisted
  threadW: number                // clamped to [160, 360]
  dockW: number                  // clamped to [240, 480]
  threadsOpen: boolean           // visible when chat section is active
  dockOpen: boolean              // visible when chat section is active
  dockTab: 'progress' | 'context' | 'artifacts'
  density: 'compact' | 'default' | 'cozy'

  // Transient (not persisted)
  threadsOverridden: boolean     // user manually toggled; freezes auto-collapse until next boundary crossing
  dockOverridden: boolean

  // Actions
  setThreadW: (n: number) => void
  setDockW: (n: number) => void
  toggleThreads: () => void      // sets threadsOverridden=true
  toggleDock: () => void         // sets dockOverridden=true
  setDockTab: (tab: UiStore['dockTab']) => void
  setDensity: (d: UiStore['density']) => void
  setAutoThreads: (open: boolean) => void       // called by useAutoCollapse; does NOT set override
  setAutoDock: (open: boolean) => void
  resetThreadsOverride: () => void              // called when vw crosses 1100px boundary
  resetDockOverride: () => void                 // called when vw crosses 900px boundary
}
```

- Persistence: Zustand `persist` middleware with a single `ds:ui` localStorage key holding the serialized persisted-subset. Schema version: `v: 1`. A `migrate` function handles missing keys by merging defaults (`threadW = 200`, `dockW = 320`, `threadsOpen = true`, `dockOpen = true`, `dockTab = 'progress'`, `density = 'default'`). Older `ds:threadW` / `ds:dockW` keys are read once on migrate and folded in, then ignored.
- Validation: Every incoming value is clamped via a zod schema before landing in state. Invalid localStorage JSON resets to defaults silently.
- Subscription surface is minimal: selectors read only what they need so components don't re-render on unrelated state changes.

### Section routing (store.ts SectionId expansion)

```ts
type SectionId =
  | 'chat' | 'agents' | 'skills' | 'prompts'
  | 'context' | 'health'
  | 'graph' | 'digest' | 'ingest'   // new
  | 'settings'
```

`App.tsx`'s `SectionContent` switch adds three cases that render the appropriate panel components (`GraphPanel`, `DigestPanel`, `IngestPanel`) full-bleed. Those panels accept an `embedded` prop today; the new renderer passes `embedded={false}` and omits the close button (there's no "back to trace" now — the user clicks another IconRail item).

### Token system (tokens.css)

Full port of `design_handoff_ds_agent/tokens.css` with these adjustments:

- `:root` holds the light palette (already the handoff default). `[data-theme="dark"]` holds dark overrides (handoff uses the same attribute).
- Existing `globals.css` hex tokens (`--color-bg-primary`, `--color-accent`, etc.) are **aliased** at the bottom of tokens.css so untouched components keep rendering:

  ```css
  :root {
    --color-bg-primary: var(--bg-0);
    --color-bg-secondary: var(--bg-1);
    --color-bg-elevated: var(--bg-2);
    --color-text-primary: var(--fg-0);
    --color-text-secondary: var(--fg-1);
    --color-text-muted: var(--fg-2);
    --color-accent: var(--acc);
    --color-accent-hover: color-mix(in oklab, var(--acc) 92%, black);
    --color-accent-active: color-mix(in oklab, var(--acc) 82%, black);
    --color-accent-foreground: var(--acc-fg);
    --color-border: var(--line-2);
    --color-border-hover: var(--line);
  }
  ```

- All handoff keyframes (`march`, `pulse`, `pulseRing`, `blink`, `spin`, `drawCheck`, `scaleIn`, `fadeIn`, `slideInR`, `sheen`) ported verbatim. Tailwind config also registers them under `theme.extend.keyframes` + `animation` so they're reachable as utilities like `animate-march`, `animate-draw-check`, `animate-pulse-ring`.
- Semantic component classes (`.surface`, `.surface-raised`, `.mono`, `.serif`, `.label`, `.label-cap`, `.kbd`, `.dot`, `.btn`, `.btn-primary`, `.btn-ghost`, `.row-hover`, `.ants`, `.pulse`, `.pulse-ring`, `.caret`, `.draw-check`, `.scale-in`, `.fade-in`, `.slide-in-r`, `.shimmer`, `.stripe-ph`, `.focus-ring`) ported under `@layer components` in globals.css (so they're purgeable by Tailwind and compose cleanly with utility classes).
- Density variants: `html[data-density="compact"]` and `html[data-density="cozy"]` override `--row-h`, `--pad-x`, `--pad-y`. Step 5 wires a UI control; step 1 exposes the classes.
- Reduced-motion: `@media (prefers-reduced-motion: reduce)` block zeros the duration of all keyframe animations and disables the hover transition transforms.

### Tailwind config (tailwind.config.ts)

```ts
darkMode: ['selector', '[data-theme="dark"]'],
theme: {
  extend: {
    colors: {
      'bg-0': 'var(--bg-0)', 'bg-1': 'var(--bg-1)', 'bg-2': 'var(--bg-2)', 'bg-3': 'var(--bg-3)',
      'fg-0': 'var(--fg-0)', 'fg-1': 'var(--fg-1)', 'fg-2': 'var(--fg-2)', 'fg-3': 'var(--fg-3)',
      'line':   'var(--line)',
      'line-2': 'var(--line-2)',
      acc:          'var(--acc)',
      'acc-fg':     'var(--acc-fg)',
      'acc-dim':    'var(--acc-dim)',
      'acc-line':   'var(--acc-line)',
      ok: 'var(--ok)', warn: 'var(--warn)', err: 'var(--err)', info: 'var(--info)',
      // ...legacy colors stay for backward compatibility
    },
    fontFamily: {
      sans: ['Inter', 'ui-sans-serif', '-apple-system', 'BlinkMacSystemFont', 'SF Pro Text', 'Helvetica Neue', 'sans-serif'],
      serif: ['Charter', 'Iowan Old Style', 'Palatino', 'ui-serif', 'serif'],
      mono: ['JetBrains Mono', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'Consolas', 'monospace'],
    },
    borderRadius: {
      'xs': 'var(--radius-xs)',
      DEFAULT: 'var(--radius)',
      'lg': 'var(--radius-lg)',
      'xl': 'var(--radius-xl)',
    },
    transitionTimingFunction: {
      'out-expo':   'var(--ease-out)',
      'out-2':      'var(--ease-out-2)',
      'in-out':     'var(--ease-in-out)',
      'spring':     'var(--ease-spring)',
    },
    transitionDuration: { fast: '140ms', base: '220ms', slow: '360ms' },
    keyframes: { march, pulse, pulseRing, drawCheck, scaleIn, fadeIn, slideInR, sheen /* ... */ },
    animation: {
      'march':       'march 1s linear infinite',
      'pulse-soft':  'pulse 1.8s cubic-bezier(0.65,0,0.35,1) infinite',
      'pulse-ring':  'pulseRing 1.8s cubic-bezier(0.16,1,0.3,1) infinite',
      'draw-check':  'drawCheck 420ms cubic-bezier(0.16,1,0.3,1) forwards',
      'scale-in':    'scaleIn 280ms cubic-bezier(0.34,1.56,0.64,1) both',
      'fade-in':     'fadeIn 280ms cubic-bezier(0.16,1,0.3,1) both',
      'slide-in-r':  'slideInR 260ms cubic-bezier(0.16,1,0.3,1) both',
      'sheen':       'sheen 2.4s cubic-bezier(0.65,0,0.35,1) infinite',
    },
  },
}
```

Legacy color palettes (`brand.50..950`, `surface.50..950`, `canvas.*`, `ink.*`, `brand-accent.*`) stay intact so existing components render unchanged.

### Fonts

- `frontend/public/fonts/Inter-{Regular,Medium,SemiBold,Bold}.woff2` — 400/500/600/700. Sourced from the official Inter release (rsms.me/inter) and committed under a public-domain + SIL-OFL permissive license (`fonts/LICENSE` mirrors the upstream OFL notice).
- `frontend/public/fonts/JetBrainsMono-SemiBold.woff2` — 600 added alongside existing 400/500 for labels and keycaps that need extra weight contrast.
- `@font-face` blocks in globals.css with `font-display: swap`, `unicode-range` restricted to Latin + Latin-Extended so the payload stays under ~110KB total gzipped.
- Body style from tokens: `font-family: var(--font-sans); font-size: 13.5px; line-height: 1.5; letter-spacing: -0.003em; font-feature-settings: "cv11", "ss01", "ss03";`

### IconRail (rewritten)

Visual spec:
- 52px wide, full-height, `bg-bg-1`, `border-r border-line-2`.
- 10px top padding, items flush-top (no logo block).
- Each item: 36×36 button, centered icon (18px line height, `stroke-1.5`), active state (color `acc`, background `acc-dim`, 2px `acc` left bar absolutely positioned) driven by `aria-current="page"`.
- Hover: `bg-bg-2`, text `fg-0`.
- Disabled: muted `fg-3` with `cursor-not-allowed` (reserved for future sections that need gating).
- Flyout tooltip: `role="tooltip"`, 8px offset right of button, white-on-near-black (or inverse in dark), shows `label` + optional `hint` in `.kbd`. Appears on hover and focus; keyboard-accessible.

Items (top section):
1. Chat · `MessageSquare` · `⌘⇧1`
2. Agents · `Bot` (Lucide) · `⌘⇧2`
3. Skills · `Puzzle` · `⌘⇧3`
4. Prompts · `FileText` · `⌘⇧4`
5. Context · `Layers` · `⌘⇧5`
6. Health · `Activity` · `⌘⇧6`
7. Graph · `Network` · `⌘⇧7`
8. Digest · `ClipboardList` · `⌘⇧8`
9. Ingest · `Download` · `⌘⇧9`

Separator (1px `line-2` hairline, 24px wide).

Bottom section:
- Theme toggle · `Sun` ↔ `Moon` · no default hotkey (already registered as `TOGGLE_THEME` in command palette)
- Settings · `Settings` · `⌘,`

Custom SVG pair `SidebarIcon` / `SidebarOnIcon` (the "filled-left-pane" variant) lives in IconRail's file or a dedicated `icons/sidebar.tsx`. Used by the chat header's threads toggle (step 2) — step 1 exports the component but does not consume it yet (IconRail itself does not render the threads toggle; that belongs in the chat header).

### ThreadList (initial implementation)

Header (40px):
- Label `Chats` in small-caps mono (`.label-cap` class).
- `+` new-chat icon button (28×28, ghost, accent on hover).
- Close chevron at far right (28×28, ghost, points left to indicate hide).

Body (scrollable):
- Sections: `Pinned` (any conversation with `pinned: true`; default false on migration — schema will be extended in step 4, for now the section is hidden entirely when empty), `Today` (updatedAt within last 24h), `This week` (within last 7d), `Older` (everything else).
- Section header: `.label-cap` style, 8px top padding, 4px bottom padding.
- Row: 56px tall, `.row-hover`, two-line layout (title 13px/500/-0.005em on top, preview 11.5px/`fg-2` below), right-justified relative timestamp (`.mono`, 11px, `fg-3`).
- Active row: `bg-acc-dim`, 2px `acc` left border (absolute).

Footer (40px):
- Archive button (ghost, label `Archive`, icon `Archive`). Click is a no-op stub in step 1 — step 4 wires it.

Resizable: right edge hosts a 4px `Resizer` (axis=x, min=160, max=360).

### Dock (initial implementation)

Tab bar (40px):
- Three tabs: `Progress`, `Context`, `Artifacts`. Active tab gets 2px `acc` bottom border + accent icon.
- Tab style: 12.5px label + 14px leading icon, 12px horizontal padding, gap 6px.
- Close chevron (right-pointing) at far right, 24×24, `row-hover`.

Tab bodies:
- `progress`: renders the existing `<TraceRail />` component inside a `.surface` scroll container.
- `context`: `DockContextStub` — a `stripe-ph` placeholder with the text `"Context tab — variables, dataframes, files. Ships in step 3."`.
- `artifacts`: `DockArtifactsStub` — 3-column `stripe-ph` grid with caption `"Artifacts grid — ships in step 3."`.

Resizable: left edge hosts a 4px `Resizer` (axis=x, min=240, max=480, invert=true — dragging left increases dock width).

Dock hides when active section is not `chat`. When hidden, it does not consume horizontal space.

### ThemeProvider changes

Current behavior: `.light` class on `<html>`, `:root:not(.light)` = dark.
New behavior: `[data-theme="dark"]` on `<html>`, `:root` = light.

Migration path:
- `ThemeProvider` effect on mount reads legacy `localStorage.theme` value. If `'dark'` → sets `[data-theme="dark"]`. If `'light'` → removes attribute. Writes back under the new key `ds:theme`. Old key stays for one release (read but never re-written after first migrate) so downgrade is possible.
- Default theme: `light` (was `dark`).
- `useTheme()` hook's `theme: 'dark' | 'light'` contract unchanged; internal implementation flips.

### Accessibility

- All Resizers are focusable, `role="separator"`, `aria-orientation`, `aria-valuemin`, `aria-valuemax`, `aria-valuenow`, `aria-label`, Arrow/Home/End keyboard support.
- IconRail buttons remain full buttons with `aria-current="page"`, `aria-label`, visible focus ring.
- ThreadList rows: `<button>` with `aria-pressed` for active, `aria-label` including title + "active" when current.
- Dock tabs: `role="tablist"` / `role="tab"` / `role="tabpanel"` with proper ARIA linkage.
- Theme toggle: `aria-label="Switch to dark theme"` / `"Switch to light theme"` dynamically.
- Color contrast: light palette `fg-0` on `bg-0` measured ≥7.2:1 (AAA). Dark palette `fg-0` on `bg-0` ≥14:1. Accent on `bg-0` ≥4.8:1 (AA). Verified against the handoff oklch values.
- Reduced motion: `@media (prefers-reduced-motion: reduce)` overrides all `*-infinite` animations with `animation-duration: 0.01ms` and disables the 3px-rise in `fade-in` / `slide-in-r`.

### Observability

- Dev-only `performance.mark`s at AppShell mount (`shell:mounted`) and first resize (`shell:first-resize`). Stripped in production via `import.meta.env.DEV` guard.
- Console warnings suppressed (no `console.log` in production code per coding-style rule; an `assert` utility throws in dev and no-ops in prod for invariants).
- No feature flags (YAGNI).

### Keyboard shortcuts

Additions registered in `ShortcutWiring` (App.tsx):

| Command                | Keys            | Behavior                                      |
|------------------------|-----------------|-----------------------------------------------|
| `TOGGLE_DOCK`          | `mod+j`         | Toggle dock visibility + set override flag    |
| `OPEN_SECTION_CHAT`    | `mod+shift+1`   | Switch section to `chat`                      |
| `OPEN_SECTION_AGENTS`  | `mod+shift+2`   | Switch section to `agents`                    |
| `OPEN_SECTION_SKILLS`  | `mod+shift+3`   | Switch section to `skills`                    |
| `OPEN_SECTION_PROMPTS` | `mod+shift+4`   | Switch section to `prompts`                   |
| `OPEN_SECTION_CONTEXT` | `mod+shift+5`   | Switch section to `context`                   |
| `OPEN_SECTION_HEALTH`  | `mod+shift+6`   | Switch section to `health`                    |
| `OPEN_SECTION_GRAPH`   | `mod+shift+7`   | Switch section to `graph`                     |
| `OPEN_SECTION_DIGEST`  | `mod+shift+8`   | Switch section to `digest`                    |
| `OPEN_SECTION_INGEST`  | `mod+shift+9`   | Switch section to `ingest`                    |

Existing `CYCLE_RAIL` (`mod+\`) is removed — it cycled right-rail summon modes which no longer exist. Its command palette entry and keybinding unregister in the same change.

Existing `SWITCH_1..9` (`mod+1..9`) continue to switch conversation slots and are unaffected (they carry a `when: conversations.length >= n` predicate). Section-switch shortcuts use the Shift chord so the two scopes never collide. `⌘⇧1..9` is global (works in any section); `⌘1..9` remains conversation-scoped to chat.

### Error handling / edge cases

- **localStorage unavailable** (private mode, SSR in dev): `persist` middleware no-ops; defaults apply. No thrown errors.
- **Corrupt localStorage JSON**: schema validation rejects it, state resets to defaults, a dev-only warning is logged via the assert utility.
- **Viewport <600px**: IconRail stays (52px is fine at that width); ThreadList and Dock are both hidden. Conversation pane gets full remaining width.
- **Very wide viewport (>2400px)**: ThreadList and Dock max out at 360 and 480 respectively; Conversation absorbs the rest. No horizontal scroll anywhere.
- **Missing web fonts**: `font-display: swap` falls back to system sans / OS serif / system mono. Layout stable (font-metric overrides tune fallback to Inter's metrics so CLS stays under 0.05).
- **Resize during active drag**: the drag listener captures the starting viewport width and scales deltas accordingly; mid-drag viewport changes don't desync the handle.
- **Manual toggle then resize crossing boundary**: override flag clears when vw crosses the relevant breakpoint, letting auto-collapse take over on the other side of the boundary.

### Testing

**Unit (vitest):**
- `ui-store` — default hydration, clamp behavior, persist-across-reload (via localStorage mock), migrate from legacy `ds:threadW`/`ds:dockW` keys, reject corrupt JSON, toggle actions set override flags correctly.
- `useViewportWidth` — returns initial width, updates on resize, unsubscribes on unmount, rAF throttle semantics.
- `useAutoCollapse` — crossing 1100 opens/closes threads only when not overridden; crossing 900 does the same for dock; manual toggle sets override until next crossing.
- `Resizer` — pointer drag updates value within clamps; keyboard Arrow nudges ±10; Home/End snap; aria-valuenow tracks value; invert axis flips delta direction.
- `ThreadList` — sectioning groups conversations correctly for Pinned/Today/This week/Older given synthetic `updatedAt` timestamps.
- `IconRail` — renders 11 top-section buttons + theme toggle + settings; active state reflects `activeSection`; click updates store.

**Integration (React Testing Library):**
- `AppShell` renders ThreadList + Dock when `activeSection==='chat'`, hides both when section is not chat.
- Theme toggle updates `[data-theme]` attribute on `<html>` and persists.

**Playwright visual regression:**
- Captures at 320 / 768 / 1100 / 1440 × (light / dark) × (chat / agents / skills sections) — 4 × 2 × 3 = 24 screenshots saved to `frontend/e2e-shell-*.png`.
- Checks no CLS beyond 0.05 during font load.
- Keyboard-only flow: Tab through IconRail → ThreadList → Conversation → Dock tabs without pointer assistance.

**Build verification:**
- `pnpm lint` clean.
- `pnpm typecheck` clean.
- `pnpm test` (unit + integration) green.
- `pnpm build` ships with no chunk larger than 300KB gzipped (landing chat route stays under 150KB).

### Rollout & compatibility

- Single PR, single-step rollout. No feature flag — the entire shell flips at once.
- Backward compat for components that still reference `--color-*` vars is maintained by the alias block. No component edits required beyond the step-1 scope.
- The commit sequence (per implementation plan) is ordered so each commit leaves the build green, allowing bisect if anything regresses.

### Risks

1. **Font loading causes perceptible FOUT.** Mitigation: preload `Inter-Regular.woff2` in `index.html`, use `font-display: swap`, and tune a local metric override (ascent/descent/line-gap) to keep fallback layout identical to Inter.
2. **Tailwind JIT misses new keyframes in purge.** Mitigation: add `safelist` entries in `tailwind.config.ts` for every handoff animation class so they survive content purging.
3. **Resizer keyboard conflicts with in-app shortcuts.** Mitigation: Resizer consumes Arrow/Home/End only while focused; global shortcuts take precedence on any other focused element.
4. **Legacy `--color-*` alias drift.** Mitigation: add a vitest snapshot that verifies the computed color values for the aliased tokens match the handoff's oklch output under both themes.
5. **Section rename cascade.** Adding `graph|digest|ingest` to `SectionId` changes the discriminated union — anything that does an exhaustive switch will type-fail until it handles the new members. Intentional: TypeScript forces us to update every switch, preventing silent misses.

## Success Criteria

Step 1 is done when:
- All files listed above exist, all listed files are deleted.
- `pnpm lint`, `pnpm typecheck`, `pnpm test`, `pnpm build` are all green.
- Playwright visual regression suite passes with reference screenshots captured and committed.
- Manually opening the app at the four breakpoints in both themes matches the handoff bundle's layout within ±2px per pane edge.
- The `docs/log.md` `[Unreleased]` section has a `changed` entry summarizing the shell foundation.
- Saved project memory reflects the new theme direction (already done 2026-04-18).
