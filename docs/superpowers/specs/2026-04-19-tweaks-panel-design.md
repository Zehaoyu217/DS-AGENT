# Tweaks Panel — Design Spec (sub-project 5 of 5)

**Date:** 2026-04-19
**Status:** Approved (auto)
**Predecessors:** SP1 shell foundation, SP2 chat surface, SP3 dock+artifact, SP4 thread list+palette polish

## Goal

Land the handoff's **Tweaks panel** — a runtime UI knob popover that supersedes the overlapping rows in the existing `SettingsSection`. Full handoff parity (9 controls) including a real `dock-bottom` layout. Client-only persistence via `useUiStore`.

## Decisions

| Q | A |
|---|---|
| Scope | **A** — full handoff parity (9 controls) |
| Dock-position | **A1** — right / bottom / off |
| Tweaks vs Settings | Tweaks **supersedes** the overlapping Settings rows (theme, density, accent). Settings keeps model/prompt/api fields. |

## Controls

| Knob | Values | Default | Source of truth |
|---|---|---|---|
| Theme | `light` / `dark` / `system` | `light` | `ThemeProvider` (`ds:theme`) |
| Accent | 5 hex swatches | `#e0733a` (Claude orange) | `useUiStore.accent` |
| Density | `compact` / `default` | `default` | `useUiStore.density` |
| Dock | `right` / `bottom` / `off` | `right` | `useUiStore.dockPosition` |
| Msg style | `flat` / `bordered` | `flat` | `useUiStore.msgStyle` |
| Think | `tab` / `inline` | `tab` | `useUiStore.thinkMode` |
| Font | `mono` / `sans` | `mono` | `useUiStore.uiFont` |
| Rail | `icon` / `expand` | `icon` | `useUiStore.railMode` |
| Agent | `run` / `pause` | `run` | `useUiStore.agentRunning` |

Accent swatches: `#e0733a` (orange — default), `#a3e635` (lime), `#22d3ee` (cyan), `#c084fc` (violet), `#f472b6` (pink). The orange-default invariant is preserved.

## Architecture

```
IconRail
  └─ gear button (bottom) ──► opens TweaksPanel (Radix Popover, anchored to gear)

TweaksPanel
  ├─ TweakRow × 9 (label + Seg2/SwatchRow)
  └─ writes through to: useUiStore (accent/dockPosition/msgStyle/thinkMode/uiFont/railMode/agentRunning/density)
                        ThemeProvider.setTheme (theme)

TweaksEffects (mounted in App.tsx, no DOM)
  └─ subscribes to ui-store, applies side-effects:
      - accent → document.documentElement.style.setProperty('--acc', …) + --acc-dim, --acc-line
      - uiFont → document.documentElement.dataset.font = uiFont
      - railMode → handled inside IconRail
      - msgStyle/thinkMode → consumed by Message renderer + ThinkingBlock
      - agentRunning → consumed by header running pulse + composer Send/Stop default

AppShell
  └─ branches on dockPosition:
       'right'  → existing flex-row layout
       'bottom' → grid-rows: [main / dock]
       'off'    → no Dock pane

SettingsTab
  └─ strips theme + density rows; gains "Manage in Tweaks (⌘,)" hint card
```

## Persistence

`useUiStore` schema bumps `v: 2 → v: 3` adding 7 fields. Migration backfills defaults. Tweaks panel is opened by:
- gear icon click in `IconRail`
- ⌘, keyboard shortcut (registered as `tweaks.open` command)
- palette: `Open Tweaks` (category Navigation)

## Side-effects map (CSS layer)

`tokens.css` gains:
- `:root[data-font="sans"] { --font-ui: var(--font-sans); }` — default `mono`
- `[data-msg-style="bordered"]` selectors on the message bubble
- `[data-think-mode="inline"]` selectors on the thinking block

Accent overrides go through inline style on `:root` (cleaner than data-attrs since the value is dynamic hex).

## Out of scope

- Server-side persistence of these knobs (client-only by design)
- "Reset to defaults" button (deferred — easy follow-up)
- Custom-hex accent picker (5 fixed swatches only, per handoff)
- Mobile-specific layout for `dock=bottom` (desktop-first)

## Testing

- `useUiStore` v3 migration test (v2 payload → v3 with backfilled defaults)
- `TweaksPanel` renders 9 rows, fires correct setters, persists across reload
- `AppShell` renders dock at `right` / `bottom` / not-at-all per `dockPosition`
- `IconRail` `expand` mode shows labels next to icons
- Accent change writes `--acc` inline style
- SettingsTab no longer renders theme/density rows (regression guard)

## Files

**Create:**
- `frontend/src/components/tweaks/TweaksPanel.tsx`
- `frontend/src/components/tweaks/TweakRow.tsx`
- `frontend/src/components/tweaks/Seg2.tsx`
- `frontend/src/components/tweaks/AccentSwatches.tsx`
- `frontend/src/components/tweaks/TweaksEffects.tsx`
- `frontend/src/components/tweaks/__tests__/TweaksPanel.test.tsx`

**Modify:**
- `frontend/src/lib/ui-store.ts` (v3 schema + 7 new fields + setters)
- `frontend/src/components/shell/AppShell.tsx` (dock-position branch)
- `frontend/src/components/layout/IconRail.tsx` (gear trigger + expand mode)
- `frontend/src/styles/tokens.css` (font-ui data-attr, msg-style, think-mode)
- `frontend/src/components/sidebar/SettingsTab.tsx` (strip overlapping rows)
- `frontend/src/App.tsx` (mount `TweaksEffects`)
- `frontend/src/hooks/useCommandRegistry.tsx` or shortcuts (register `tweaks.open` ⌘,)
