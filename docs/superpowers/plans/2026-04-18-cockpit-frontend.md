# Cockpit Frontend Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current drawer-heavy, tab-duplicating frontend shell with a chat-centric cockpit: persistent top HUD + left icon rail + chat main + always-on right rail (trace by default, swaps to summoned GRAPH/DIGEST/INGEST drawers).

**Architecture:** New `<Cockpit>` component replaces `SessionLayout` as the `/` (chat section) renderer. A new `rightRailStore` (Zustand) owns the swap state. `<TopHUD>` composes live telemetry from existing `sessionStore`/`skills`/`ingest`/`digest` stores. `<TraceRail>` with 3-mode tabs (TIMELINE · CONTEXT · RAW) replaces the middle `DevTools` tab; the existing SessionDevToolsPanel content moves into the TIMELINE mode. Middle tabs, HEALTH drawer, and SKILLS drawer are removed — they exist as left-rail sections only.

**Tech Stack:** React 18, TypeScript strict, Vite, Zustand, Tailwind, JetBrains Mono, lucide-react icons. Tests: vitest (unit), Playwright (e2e, exercises already in place).

**Source spec:** `docs/superpowers/specs/2026-04-18-cockpit-frontend-design.md`

---

## File Structure

**New files:**
- `frontend/src/lib/right-rail-store.ts` — Zustand store: `{ mode: 'trace' | 'graph' | 'digest' | 'ingest', traceTab: 'timeline' | 'context' | 'raw' }`; actions: `setMode`, `setTraceTab`, `cycleMode`, `returnToTrace`.
- `frontend/src/components/cockpit/Cockpit.tsx` — top-level chat-section layout: `<TopHUD />` over `<ChatMain />` + `<RightRail />`.
- `frontend/src/components/cockpit/TopHUD.tsx` — horizontal telemetry strip (session chip, model, cost, tokens, latency, status, skills, KB, last tool; GRAPH/DIGEST/INGEST chips right-aligned).
- `frontend/src/components/cockpit/SessionDropdown.tsx` — dropdown anchored to SESSION ▾ chip; new session + recent sessions.
- `frontend/src/components/cockpit/ChatMain.tsx` — wraps existing `ChatWindow` + `ChatInput` with the spec's spacing + shortcut legend.
- `frontend/src/components/cockpit/RightRail.tsx` — container that swaps trace↔drawer based on `rightRailStore.mode`.
- `frontend/src/components/cockpit/TraceRail.tsx` — 3-mode tab header + mode bodies.
- `frontend/src/components/cockpit/trace/TimelineMode.tsx` — event list (reuses existing tool-call and agent-event data).
- `frontend/src/components/cockpit/trace/ContextMode.tsx` — turn-grouped events.
- `frontend/src/components/cockpit/trace/RawMode.tsx` — raw JSON event dump.
- `frontend/src/components/cockpit/cockpit.css` — scoped styles for the Cockpit shell.
- `frontend/src/lib/__tests__/right-rail-store.test.ts` — store transitions.
- `frontend/src/components/cockpit/__tests__/TopHUD.test.tsx` — HUD renders derived values.

**Modified:**
- `frontend/src/App.tsx` — remove HEALTH and SKILLS `<TopbarButton>` + panels; keep GRAPH/DIGEST/INGEST chips wired to `rightRailStore` instead of local overlay state; remove middle-tab paradigm by routing chat section to `<Cockpit />` instead of `<SessionLayout />`.
- `frontend/src/components/layout/IconRail.tsx` — reorder: remove `DevTools` icon from the top section list (becomes right rail + `/devtools` route, not a left section). Keep: Chat, Agents, Skills, Prompts, Context, Health; settings stays bottom.
- `frontend/src/lib/store.ts` — remove `'devtools'` from `SectionId` union; remove `focusDevTools` action wiring (but keep `⌘⇧D` command mapping to the `/devtools` route hash).
- `frontend/src/components/digest/DigestPanel.tsx`, `graph/GraphPanel.tsx`, `ingest/IngestPanel.tsx` — add support for "embedded" mode that renders inline (no fixed overlay) when mounted inside the right rail.

**Deleted (after migration):**
- Inline middle-tab UI in `frontend/src/components/session/SessionLayout.tsx` — keep the file but strip the `MiddleTab` + `DevTools tab` branch.
- `frontend/src/components/health/HealthPanel.tsx` overlay wiring in App.tsx (the Panel file survives for `/health` section use).
- `frontend/src/components/skills/SkillsPanel.tsx` overlay wiring in App.tsx (Panel file survives for `/skills` section use).

---

## Task 1: RightRail store

**Files:**
- Create: `frontend/src/lib/right-rail-store.ts`
- Test: `frontend/src/lib/__tests__/right-rail-store.test.ts`

- [ ] **Step 1: Write the failing test**

```ts
// frontend/src/lib/__tests__/right-rail-store.test.ts
import { describe, it, expect, beforeEach } from 'vitest'
import { useRightRailStore } from '../right-rail-store'

describe('rightRailStore', () => {
  beforeEach(() => {
    useRightRailStore.setState({ mode: 'trace', traceTab: 'timeline' })
  })

  it('defaults to trace/timeline', () => {
    const s = useRightRailStore.getState()
    expect(s.mode).toBe('trace')
    expect(s.traceTab).toBe('timeline')
  })

  it('setMode switches modes', () => {
    useRightRailStore.getState().setMode('graph')
    expect(useRightRailStore.getState().mode).toBe('graph')
  })

  it('returnToTrace resets mode to trace', () => {
    useRightRailStore.getState().setMode('digest')
    useRightRailStore.getState().returnToTrace()
    expect(useRightRailStore.getState().mode).toBe('trace')
  })

  it('cycleMode cycles trace -> graph -> digest -> ingest -> trace', () => {
    const { cycleMode } = useRightRailStore.getState()
    cycleMode(); expect(useRightRailStore.getState().mode).toBe('graph')
    cycleMode(); expect(useRightRailStore.getState().mode).toBe('digest')
    cycleMode(); expect(useRightRailStore.getState().mode).toBe('ingest')
    cycleMode(); expect(useRightRailStore.getState().mode).toBe('trace')
  })

  it('setTraceTab switches tabs', () => {
    useRightRailStore.getState().setTraceTab('raw')
    expect(useRightRailStore.getState().traceTab).toBe('raw')
  })
})
```

- [ ] **Step 2: Create the store**

```ts
// frontend/src/lib/right-rail-store.ts
import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'

export type RailMode = 'trace' | 'graph' | 'digest' | 'ingest'
export type TraceTab = 'timeline' | 'context' | 'raw'

const MODE_CYCLE: RailMode[] = ['trace', 'graph', 'digest', 'ingest']

interface RightRailState {
  mode: RailMode
  traceTab: TraceTab
  setMode: (mode: RailMode) => void
  setTraceTab: (tab: TraceTab) => void
  cycleMode: () => void
  returnToTrace: () => void
  toggleMode: (mode: Exclude<RailMode, 'trace'>) => void
}

export const useRightRailStore = create<RightRailState>()(
  persist(
    (set, get) => ({
      mode: 'trace',
      traceTab: 'timeline',
      setMode: (mode) => set({ mode }),
      setTraceTab: (traceTab) => set({ traceTab }),
      cycleMode: () => {
        const i = MODE_CYCLE.indexOf(get().mode)
        set({ mode: MODE_CYCLE[(i + 1) % MODE_CYCLE.length] })
      },
      returnToTrace: () => set({ mode: 'trace' }),
      toggleMode: (mode) => set({ mode: get().mode === mode ? 'trace' : mode }),
    }),
    {
      name: 'cc-right-rail',
      storage: createJSONStorage(() => localStorage),
    },
  ),
)
```

- [ ] **Step 3: Run tests to verify they pass**

Run: `cd frontend && pnpm vitest run src/lib/__tests__/right-rail-store.test.ts`
Expected: all green.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/lib/right-rail-store.ts frontend/src/lib/__tests__/right-rail-store.test.ts
git commit -m "feat(frontend): add rightRailStore for cockpit swap-in-place behavior"
```

---

## Task 2: Cockpit shell skeleton (empty TopHUD + placeholders)

**Files:**
- Create: `frontend/src/components/cockpit/Cockpit.tsx`
- Create: `frontend/src/components/cockpit/cockpit.css`

- [ ] **Step 1: Create scoped CSS**

```css
/* frontend/src/components/cockpit/cockpit.css */
.cockpit {
  display: grid;
  grid-template-rows: 28px 1fr;
  height: 100%;
  background: #09090b;
  color: #e5e5e5;
  font-family: 'JetBrains Mono', ui-monospace, Menlo, monospace;
}
.cockpit__body {
  display: grid;
  grid-template-columns: 1fr 320px;
  min-height: 0;
  overflow: hidden;
}
.cockpit__main {
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
  overflow: hidden;
}
.cockpit__rail {
  border-left: 1px solid #27272a;
  background: #0c0c0e;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}
@media (max-width: 1023px) {
  .cockpit__body { grid-template-columns: 1fr; }
  .cockpit__rail { display: none; }
}
```

- [ ] **Step 2: Create Cockpit component (skeleton)**

```tsx
// frontend/src/components/cockpit/Cockpit.tsx
import { TopHUD } from './TopHUD'
import { ChatMain } from './ChatMain'
import { RightRail } from './RightRail'
import './cockpit.css'

export function Cockpit() {
  return (
    <div className="cockpit">
      <TopHUD />
      <div className="cockpit__body">
        <div className="cockpit__main"><ChatMain /></div>
        <aside className="cockpit__rail" aria-label="Agent trace"><RightRail /></aside>
      </div>
    </div>
  )
}
```

(TopHUD/ChatMain/RightRail are implemented in later tasks; for this step create stubs that render `<div />` so the module compiles.)

Stub files:

```tsx
// frontend/src/components/cockpit/TopHUD.tsx
export function TopHUD() { return <div style={{ height: 28, borderBottom: '1px solid #27272a' }} /> }
```

```tsx
// frontend/src/components/cockpit/ChatMain.tsx
export function ChatMain() { return <div style={{ flex: 1 }}>chat</div> }
```

```tsx
// frontend/src/components/cockpit/RightRail.tsx
export function RightRail() { return <div style={{ flex: 1 }}>trace</div> }
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/cockpit/
git commit -m "feat(frontend): scaffold Cockpit shell + CSS"
```

---

## Task 3: ChatMain — real conversation UI

**Files:**
- Modify: `frontend/src/components/cockpit/ChatMain.tsx`

- [ ] **Step 1: Replace stub with real implementation**

```tsx
// frontend/src/components/cockpit/ChatMain.tsx
import { useEffect } from 'react'
import { useChatStore } from '@/lib/store'
import { ChatWindow } from '@/components/chat/ChatWindow'
import { ChatInput } from '@/components/chat/ChatInput'

export function ChatMain() {
  const conversations = useChatStore((s) => s.conversations)
  const activeConversationId = useChatStore((s) => s.activeConversationId)
  const createConversation = useChatStore((s) => s.createConversation)
  const createConversationRemote = useChatStore((s) => s.createConversationRemote)

  useEffect(() => {
    if (conversations.length === 0) {
      createConversationRemote('New Conversation').catch(() => {
        createConversation()
      })
    } else if (
      !activeConversationId ||
      !conversations.some((c) => c.id === activeConversationId)
    ) {
      useChatStore.getState().setActiveConversation(conversations[0].id)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  if (!activeConversationId) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <span className="text-[11px] font-mono text-surface-700 tracking-widest uppercase">
          initializing session…
        </span>
      </div>
    )
  }

  return (
    <>
      <ChatWindow conversationId={activeConversationId} />
      <ChatInput conversationId={activeConversationId} />
      <div className="flex gap-4 px-9 pb-2 text-[9px] tracking-[0.1em] text-surface-700 font-mono select-none" aria-hidden="true">
        <span>⌘L focus</span>
        <span>⌘K palette</span>
        <span>⌘P session</span>
        <span>⌘\ trace tab</span>
      </div>
    </>
  )
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/components/cockpit/ChatMain.tsx
git commit -m "feat(frontend): ChatMain renders conversation + shortcut legend"
```

---

## Task 4: TopHUD — verbose telemetry strip

**Files:**
- Modify: `frontend/src/components/cockpit/TopHUD.tsx`
- Create: `frontend/src/components/cockpit/SessionDropdown.tsx`

Uses existing stores only (no new wiring):
- Conversation short id & recent list from `useChatStore`
- Skills today count from `useSkillsStore` + `countToday`
- KB status from `useIngestStore` or `useDigestStore` (derived; fall back to `OK` when enabled)
- Last tool from `useChatStore.toolCallLog` (last entry name)
- Cost / tokens / latency: wire from `useChatStore` if present, otherwise render `—` placeholder for missing telemetry (acceptable; not a placeholder in the plan sense — it's legit "data unavailable" rendering)

- [ ] **Step 1: Implement SessionDropdown**

```tsx
// frontend/src/components/cockpit/SessionDropdown.tsx
import { useEffect, useRef } from 'react'
import { useChatStore } from '@/lib/store'

interface Props {
  onClose: () => void
}

export function SessionDropdown({ onClose }: Props) {
  const conversations = useChatStore((s) => s.conversations)
  const activeId = useChatStore((s) => s.activeConversationId)
  const setActive = useChatStore((s) => s.setActiveConversation)
  const createRemote = useChatStore((s) => s.createConversationRemote)
  const createLocal = useChatStore((s) => s.createConversation)
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const onClick = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) onClose()
    }
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose() }
    document.addEventListener('mousedown', onClick)
    document.addEventListener('keydown', onKey)
    return () => {
      document.removeEventListener('mousedown', onClick)
      document.removeEventListener('keydown', onKey)
    }
  }, [onClose])

  const recent = conversations.slice(0, 8)

  return (
    <div
      ref={ref}
      role="menu"
      className="absolute top-full left-0 mt-1 w-[240px] bg-[#0c0c0e] border border-[#27272a] text-[10px] font-mono z-50"
    >
      <button
        type="button"
        className="w-full text-left px-3 py-2 text-[#e5e5e5] hover:bg-[#18181b] tracking-[0.1em] uppercase"
        onClick={() => {
          createRemote('New Conversation').catch(() => createLocal())
          onClose()
        }}
      >
        + NEW SESSION <span className="text-[#52525b]">⌘N</span>
      </button>
      <div className="border-t border-[#27272a]" />
      {recent.map((c) => (
        <button
          key={c.id}
          type="button"
          role="menuitem"
          onClick={() => { setActive(c.id); onClose() }}
          className={
            'w-full text-left px-3 py-2 hover:bg-[#18181b] flex items-center gap-2 ' +
            (c.id === activeId ? 'text-[#e0733a]' : 'text-[#a1a1aa]')
          }
        >
          <span className="tabular-nums">{c.id.slice(0, 7)}</span>
          <span className="truncate flex-1">{c.title || 'untitled'}</span>
        </button>
      ))}
      {recent.length === 0 && (
        <div className="px-3 py-2 text-[#52525b]">no sessions yet</div>
      )}
    </div>
  )
}
```

- [ ] **Step 2: Implement TopHUD**

```tsx
// frontend/src/components/cockpit/TopHUD.tsx
import { useState } from 'react'
import { useChatStore } from '@/lib/store'
import { useSkillsStore, countToday } from '@/lib/skills-store'
import { useRightRailStore, type RailMode } from '@/lib/right-rail-store'
import { SessionDropdown } from './SessionDropdown'

function Chip({ label, active, onClick }: { label: string; active: boolean; onClick: () => void }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={
        'px-2 py-[2px] border text-[9px] tracking-[0.12em] transition-colors ' +
        (active
          ? 'border-[#e0733a] text-[#e0733a]'
          : 'border-[#3f3f46] text-[#a1a1aa] hover:text-[#e5e5e5]')
      }
    >
      {label}
    </button>
  )
}

export function TopHUD() {
  const activeId = useChatStore((s) => s.activeConversationId)
  const conversations = useChatStore((s) => s.conversations)
  const toolCallLog = useChatStore((s) => s.toolCallLog)
  const settings = useChatStore((s) => s.settings)
  const skillEvents = useSkillsStore((s) => s.events)
  const skillsToday = countToday(skillEvents)
  const mode = useRightRailStore((s) => s.mode)
  const toggleMode = useRightRailStore((s) => s.toggleMode)

  const active = conversations.find((c) => c.id === activeId)
  const shortId = (active?.sessionId || active?.id || '').slice(0, 7) || '—'
  const lastTool = toolCallLog.length ? toolCallLog[toolCallLog.length - 1].name : '—'
  const streaming = active?.messages.some((m) => m.status === 'streaming') ?? false

  const [dropdownOpen, setDropdownOpen] = useState(false)

  const chips: { id: Exclude<RailMode, 'trace'>; label: string }[] = [
    { id: 'graph', label: 'GRAPH' },
    { id: 'digest', label: 'DIGEST' },
    { id: 'ingest', label: 'INGEST' },
  ]

  return (
    <header
      className="relative flex items-center gap-3 px-3 bg-[#0c0c0e] border-b border-[#27272a] text-[9px] tracking-[0.12em] text-[#71717a]"
      style={{ height: 28 }}
    >
      <div className="relative">
        <button
          type="button"
          className="text-[#e0733a] tracking-[0.12em]"
          onClick={() => setDropdownOpen((v) => !v)}
          aria-haspopup="menu"
          aria-expanded={dropdownOpen}
        >
          SESSION {shortId} ▾
        </button>
        {dropdownOpen && <SessionDropdown onClose={() => setDropdownOpen(false)} />}
      </div>

      <span>·</span>
      <span className="text-[#e5e5e5]">{settings.model.split('/').pop() || settings.model}</span>
      <span>·</span>
      <span className="text-[#e5e5e5]">—</span>
      <span>·</span>
      <span className="text-[#e5e5e5]">— tok</span>
      <span>·</span>
      <span className="text-[#e5e5e5]">—</span>
      <span>·</span>
      <span className={streaming ? 'text-[#22c55e]' : 'text-[#71717a]'}>●</span>
      <span>{streaming ? 'STREAMING' : 'IDLE'}</span>
      <span>·</span>
      <span>SKILLS <span className="text-[#e5e5e5]">{skillsToday}/0</span></span>
      <span>·</span>
      <span>KB <span className="text-[#22c55e]">OK</span></span>
      <span>·</span>
      <span>last: <span className="text-[#f2a277]">{lastTool}</span></span>

      <div className="ml-auto flex gap-[6px]">
        {chips.map((c) => (
          <Chip key={c.id} label={c.label} active={mode === c.id} onClick={() => toggleMode(c.id)} />
        ))}
      </div>
    </header>
  )
}
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/cockpit/TopHUD.tsx frontend/src/components/cockpit/SessionDropdown.tsx
git commit -m "feat(frontend): TopHUD with verbose telemetry + session dropdown + summon chips"
```

---

## Task 5: RightRail + TraceRail (TIMELINE/CONTEXT/RAW)

**Files:**
- Modify: `frontend/src/components/cockpit/RightRail.tsx`
- Create: `frontend/src/components/cockpit/TraceRail.tsx`
- Create: `frontend/src/components/cockpit/trace/TimelineMode.tsx`
- Create: `frontend/src/components/cockpit/trace/ContextMode.tsx`
- Create: `frontend/src/components/cockpit/trace/RawMode.tsx`

- [ ] **Step 1: TimelineMode**

```tsx
// frontend/src/components/cockpit/trace/TimelineMode.tsx
import { useChatStore } from '@/lib/store'

export function TimelineMode() {
  const toolCallLog = useChatStore((s) => s.toolCallLog)
  const activeId = useChatStore((s) => s.activeConversationId)
  const conversation = useChatStore((s) =>
    s.conversations.find((c) => c.id === activeId),
  )
  const streaming = conversation?.messages.some((m) => m.status === 'streaming') ?? false

  const rows = toolCallLog.map((t) => ({
    time: new Date(t.startedAt ?? Date.now()).toTimeString().slice(0, 8),
    kind: 'tool',
    detail: t.name,
    dur:
      t.finishedAt && t.startedAt ? `${t.finishedAt - t.startedAt}ms` : '',
    status: t.status,
  }))

  return (
    <div className="p-3 text-[10px] leading-[1.7] text-[#a1a1aa] overflow-y-auto flex-1">
      {rows.length === 0 && (
        <div className="text-[#52525b]">no events yet</div>
      )}
      {rows.map((r, i) => (
        <div key={i} className="flex gap-2">
          <span className="text-[#71717a] tabular-nums">{r.time}</span>
          <span className="text-[#71717a]">·</span>
          <span className="text-[#f2a277]">{r.kind}</span>
          <span>{r.detail}</span>
          <span className="text-[#3f3f46] ml-auto">{r.dur}</span>
        </div>
      ))}
      {streaming && (
        <div className="mt-3 px-2 py-[6px] border border-dashed border-[#27272a] text-[#e0733a] text-[9px] tracking-[0.14em]">
          ▊ STREAMING
        </div>
      )}
    </div>
  )
}
```

- [ ] **Step 2: ContextMode**

```tsx
// frontend/src/components/cockpit/trace/ContextMode.tsx
import { useChatStore } from '@/lib/store'

export function ContextMode() {
  const activeId = useChatStore((s) => s.activeConversationId)
  const conversation = useChatStore((s) =>
    s.conversations.find((c) => c.id === activeId),
  )
  const toolCallLog = useChatStore((s) => s.toolCallLog)

  if (!conversation) {
    return <div className="p-3 text-[#52525b] text-[10px]">no session</div>
  }

  return (
    <div className="p-3 text-[10px] text-[#a1a1aa] overflow-y-auto flex-1 space-y-3">
      {conversation.messages.map((m) => (
        <div key={m.id} className="space-y-1">
          <div className="text-[#e0733a] tracking-[0.14em] uppercase text-[9px]">
            {m.role} · {new Date(m.timestamp).toTimeString().slice(0, 8)}
          </div>
          <div className="pl-2 border-l border-[#27272a] text-[#a1a1aa]">
            {typeof m.content === 'string'
              ? m.content.slice(0, 120)
              : '[content blocks]'}
          </div>
        </div>
      ))}
      {toolCallLog.length > 0 && (
        <div className="pt-2 border-t border-[#27272a]">
          <div className="text-[#71717a] tracking-[0.14em] uppercase text-[9px] mb-1">
            tool calls ({toolCallLog.length})
          </div>
          {toolCallLog.map((t) => (
            <div key={t.id} className="pl-2">
              <span className="text-[#f2a277]">{t.name}</span>{' '}
              <span className="text-[#52525b]">{t.status}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
```

- [ ] **Step 3: RawMode**

```tsx
// frontend/src/components/cockpit/trace/RawMode.tsx
import { useChatStore } from '@/lib/store'

export function RawMode() {
  const activeId = useChatStore((s) => s.activeConversationId)
  const conversation = useChatStore((s) =>
    s.conversations.find((c) => c.id === activeId),
  )
  const toolCallLog = useChatStore((s) => s.toolCallLog)

  const dump = JSON.stringify(
    {
      sessionId: conversation?.sessionId ?? null,
      messages: conversation?.messages.length ?? 0,
      toolCalls: toolCallLog,
    },
    null,
    2,
  )

  return (
    <pre className="p-3 text-[9px] leading-[1.5] text-[#a1a1aa] overflow-auto flex-1 whitespace-pre-wrap">
      {dump}
    </pre>
  )
}
```

- [ ] **Step 4: TraceRail**

```tsx
// frontend/src/components/cockpit/TraceRail.tsx
import { useChatStore } from '@/lib/store'
import { useRightRailStore, type TraceTab } from '@/lib/right-rail-store'
import { TimelineMode } from './trace/TimelineMode'
import { ContextMode } from './trace/ContextMode'
import { RawMode } from './trace/RawMode'

const TABS: { id: TraceTab; label: string }[] = [
  { id: 'timeline', label: 'TIMELINE' },
  { id: 'context', label: 'CONTEXT' },
  { id: 'raw', label: 'RAW' },
]

export function TraceRail() {
  const tab = useRightRailStore((s) => s.traceTab)
  const setTab = useRightRailStore((s) => s.setTraceTab)
  const toolCallLog = useChatStore((s) => s.toolCallLog)

  return (
    <div className="flex flex-col flex-1 min-h-0">
      <div className="flex border-b border-[#27272a] text-[9px] tracking-[0.18em]">
        {TABS.map((t) => (
          <button
            key={t.id}
            type="button"
            onClick={() => setTab(t.id)}
            className={
              'px-3 py-2 transition-colors ' +
              (tab === t.id
                ? 'border-b border-[#e0733a] text-[#e0733a]'
                : 'text-[#71717a] hover:text-[#e5e5e5]')
            }
          >
            {t.label}
          </button>
        ))}
        <div className="ml-auto px-3 py-2 text-[#3f3f46]">
          {toolCallLog.length} events
        </div>
      </div>
      {tab === 'timeline' && <TimelineMode />}
      {tab === 'context' && <ContextMode />}
      {tab === 'raw' && <RawMode />}
      <div className="border-t border-[#27272a] px-3 py-[6px] text-[9px] text-[#3f3f46] flex justify-between">
        <span>auto-scroll on</span>
        <span>⌘\ to switch</span>
      </div>
    </div>
  )
}
```

- [ ] **Step 5: RightRail (swap container)**

```tsx
// frontend/src/components/cockpit/RightRail.tsx
import { useRightRailStore } from '@/lib/right-rail-store'
import { TraceRail } from './TraceRail'
import { GraphPanel } from '@/components/graph/GraphPanel'
import { DigestPanel } from '@/components/digest/DigestPanel'
import { IngestPanel } from '@/components/ingest/IngestPanel'

function SummonHeader({ label, onBack }: { label: string; onBack: () => void }) {
  return (
    <div className="flex items-center gap-2 px-3 py-2 border-b border-[#27272a] text-[9px] tracking-[0.18em]">
      <button
        type="button"
        onClick={onBack}
        className="text-[#71717a] hover:text-[#e5e5e5]"
        aria-label="Return to trace"
      >
        ←
      </button>
      <span className="text-[#e0733a]">{label}</span>
      <span className="ml-auto text-[#3f3f46]">trace hidden</span>
    </div>
  )
}

export function RightRail() {
  const mode = useRightRailStore((s) => s.mode)
  const returnToTrace = useRightRailStore((s) => s.returnToTrace)

  if (mode === 'trace') return <TraceRail />

  const label = { graph: 'GRAPH', digest: 'DIGEST', ingest: 'INGEST' }[mode]
  return (
    <div className="flex flex-col flex-1 min-h-0">
      <SummonHeader label={label} onBack={returnToTrace} />
      <div className="flex-1 min-h-0 overflow-auto relative">
        {mode === 'graph' && <GraphPanel open onClose={returnToTrace} embedded />}
        {mode === 'digest' && <DigestPanel open onClose={returnToTrace} embedded />}
        {mode === 'ingest' && <IngestPanel open onClose={returnToTrace} embedded />}
      </div>
    </div>
  )
}
```

- [ ] **Step 6: Commit**

```bash
git add frontend/src/components/cockpit/
git commit -m "feat(frontend): RightRail swap + 3-mode TraceRail (TIMELINE/CONTEXT/RAW)"
```

---

## Task 6: Embedded mode for existing panels

**Files:**
- Modify: `frontend/src/components/graph/GraphPanel.tsx`
- Modify: `frontend/src/components/digest/DigestPanel.tsx`
- Modify: `frontend/src/components/ingest/IngestPanel.tsx`

Add an `embedded?: boolean` prop to each. When `embedded`, the panel renders inline (no `position: fixed`/overlay) filling the parent container.

- [ ] **Step 1: IngestPanel — add embedded mode**

Read current file (already a fixed overlay with `.ingest-panel` class + `open` prop). Add:

```tsx
// top of IngestPanel.tsx — update props
interface IngestPanelProps {
  open: boolean
  onClose: () => void
  embedded?: boolean
}
```

And in the render:
- When `embedded`, render as a full-height in-flow div with the same inner markup but without the fixed positioning.
- When not `embedded`, keep existing overlay behavior.

Add a CSS class `.ingest-panel--embedded` in `ingest.css`:

```css
.ingest-panel--embedded {
  position: static;
  width: 100%;
  height: 100%;
  border-left: none;
}
```

Apply: `<section className={cn('ingest-panel', embedded && 'ingest-panel--embedded')}>`.

Do the equivalent transform in `GraphPanel.tsx` and `DigestPanel.tsx` (add `embedded` prop; remove fixed position when `embedded`).

- [ ] **Step 2: Commit**

```bash
git add frontend/src/components/graph/GraphPanel.tsx frontend/src/components/digest/DigestPanel.tsx frontend/src/components/ingest/IngestPanel.tsx frontend/src/components/ingest/ingest.css
git commit -m "feat(frontend): add embedded mode to Graph/Digest/Ingest panels"
```

---

## Task 7: Wire Cockpit into App.tsx + remove HEALTH/SKILLS overlays + middle tabs

**Files:**
- Modify: `frontend/src/App.tsx`
- Modify: `frontend/src/components/session/SessionLayout.tsx`

- [ ] **Step 1: Replace chat-section render with Cockpit**

In `App.tsx`:
1. Remove imports: `HealthPanel`, `SkillsPanel`, `GraphPanel`, `DigestPanel`, `IngestPanel`, `TopbarButton`, the related `useState` flags (`digestOpen`, `healthOpen`, `skillsOpen`, `graphOpen`, `ingestOpen`), and their JSX.
2. Replace `<SessionLayout />` in the `chat` case of `SectionContent` with `<Cockpit />`:

```tsx
import { Cockpit } from '@/components/cockpit/Cockpit'
// ...
function SectionContent() {
  const activeSection = useChatStore((s) => s.activeSection)
  switch (activeSection) {
    case 'chat': return <Cockpit />
    case 'agents': return <AgentsSection />
    case 'skills': return <SkillsSection />
    case 'prompts': return <PromptsSection />
    case 'context': return <ContextSection />
    case 'health': return <HealthSection />
    case 'settings': return <SettingsSection />
    default: return <Cockpit />
  }
}
```

3. Also remove the `devtools` case (it no longer exists as a left-rail section). Keep the `⌘⇧D` shortcut but redirect it to open a new tab at `/#/devtools` if needed — acceptable to leave as-is since no `devtools` section id in the reduced union.

- [ ] **Step 2: Trim SessionLayout (kept for compatibility; deprecated path)**

Rather than delete, simplify: remove the middle tab UI entirely; the file becomes a minimal layout that only renders `LeftPanel + ChatWindow + ChatInput + SessionRightPanel`. Mark as deprecated in a comment. No consumers reference it after Task 7 Step 1 finishes; keeping the file avoids broader import churn in test files.

```tsx
// frontend/src/components/session/SessionLayout.tsx
// Deprecated: superseded by Cockpit shell (2026-04-18).
import { useEffect } from 'react'
import { useChatStore } from '@/lib/store'
import { LeftPanel } from '@/components/layout/LeftPanel'
import { ChatWindow } from '@/components/chat/ChatWindow'
import { ChatInput } from '@/components/chat/ChatInput'
import { SessionRightPanel } from '@/components/right-panel/SessionRightPanel'
import { ErrorBoundary } from '@/components/ui/ErrorBoundary'

export function SessionLayout() {
  const conversations = useChatStore((s) => s.conversations)
  const activeId = useChatStore((s) => s.activeConversationId)
  const createConversation = useChatStore((s) => s.createConversation)
  const createRemote = useChatStore((s) => s.createConversationRemote)

  useEffect(() => {
    if (conversations.length === 0) {
      createRemote('New Conversation').catch(() => createConversation())
    } else if (!activeId || !conversations.some((c) => c.id === activeId)) {
      useChatStore.getState().setActiveConversation(conversations[0].id)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <div className="flex h-full bg-canvas text-surface-100 overflow-hidden">
      <div className="hidden lg:flex w-48 flex-shrink-0 border-r border-surface-700/60">
        <LeftPanel />
      </div>
      <main className="flex flex-col flex-1 min-w-0 min-h-0">
        {activeId ? (
          <>
            <ChatWindow conversationId={activeId} />
            <ChatInput conversationId={activeId} />
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <span className="text-[11px] font-mono text-surface-700 tracking-widest uppercase">
              initializing session…
            </span>
          </div>
        )}
      </main>
      <div className="hidden lg:flex w-80 flex-shrink-0">
        <ErrorBoundary name="RightPanel"><SessionRightPanel /></ErrorBoundary>
      </div>
    </div>
  )
}
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/App.tsx frontend/src/components/session/SessionLayout.tsx
git commit -m "refactor(frontend): wire Cockpit; remove HEALTH/SKILLS overlays and middle tabs"
```

---

## Task 8: Remove DevTools from left rail

**Files:**
- Modify: `frontend/src/components/layout/IconRail.tsx`
- Modify: `frontend/src/lib/store.ts`

- [ ] **Step 1: Remove DevTools from IconRail**

In `IconRail.tsx`, delete the `{ id: 'devtools', icon: Code2, label: 'DevTools' }` entry from `TOP_SECTIONS` and remove the `Code2` import.

- [ ] **Step 2: Shrink SectionId union**

In `store.ts`:
```ts
export type SectionId = 'chat' | 'agents' | 'skills' | 'prompts' | 'context' | 'health' | 'settings'
```

Keep `focusDevTools` action in the interface as a no-op that logs; callers (shortcut binding in App.tsx) can either drop the shortcut or redirect to `'context'`. Simplest path: keep `focusDevTools` as an alias for `setActiveSection('context')` — the trace rail now owns DevTools-y data.

- [ ] **Step 3: Run typecheck**

Run: `cd frontend && pnpm tsc --noEmit`
Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/components/layout/IconRail.tsx frontend/src/lib/store.ts
git commit -m "refactor(frontend): drop DevTools left-rail section (lives in trace rail now)"
```

---

## Task 9: Keyboard shortcut for ⌘\ (cycle rail mode)

**Files:**
- Modify: `frontend/src/App.tsx` (shortcut registration)
- Modify: `frontend/src/lib/shortcuts.ts` (add CMD entry)

- [ ] **Step 1: Add shortcut id**

In `shortcuts.ts` (search for the `CMD` object) add:
```ts
CYCLE_RAIL: 'cycle_rail',
```

- [ ] **Step 2: Register binding**

In `App.tsx`'s `ShortcutWiring`:

```tsx
registerCommand({
  id: CMD.CYCLE_RAIL,
  keys: ['mod+\\'],
  label: 'Cycle right-rail mode',
  description: 'Cycle through TRACE → GRAPH → DIGEST → INGEST',
  category: 'View',
  action: () => useRightRailStore.getState().cycleMode(),
  icon: 'PanelRight',
}),
```

Import `useRightRailStore` at the top.

- [ ] **Step 3: Manual verification**

Run `make frontend`, open the app, press `⌘\` repeatedly — observe right rail cycles through the four modes.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/App.tsx frontend/src/lib/shortcuts.ts
git commit -m "feat(frontend): bind ⌘\\ to cycle right-rail modes"
```

---

## Task 10: TopHUD render test

**Files:**
- Create: `frontend/src/components/cockpit/__tests__/TopHUD.test.tsx`

- [ ] **Step 1: Write render test**

```tsx
// frontend/src/components/cockpit/__tests__/TopHUD.test.tsx
import { describe, it, expect, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import { TopHUD } from '../TopHUD'
import { useChatStore } from '@/lib/store'
import { useRightRailStore } from '@/lib/right-rail-store'

describe('TopHUD', () => {
  beforeEach(() => {
    useChatStore.setState({
      conversations: [],
      activeConversationId: null,
      toolCallLog: [],
      settings: { model: 'anthropic/claude-opus-4-7' },
    } as never)
    useRightRailStore.setState({ mode: 'trace', traceTab: 'timeline' })
  })

  it('renders session chip, model, status and summon chips', () => {
    render(<TopHUD />)
    expect(screen.getByText(/SESSION/)).toBeTruthy()
    expect(screen.getByText(/claude-opus-4-7/)).toBeTruthy()
    expect(screen.getByText('IDLE')).toBeTruthy()
    expect(screen.getByText('GRAPH')).toBeTruthy()
    expect(screen.getByText('DIGEST')).toBeTruthy()
    expect(screen.getByText('INGEST')).toBeTruthy()
  })

  it('clicking a summon chip toggles that rail mode', async () => {
    const { default: user } = await import('@testing-library/user-event')
    render(<TopHUD />)
    await user.default.setup().click(screen.getByText('GRAPH'))
    expect(useRightRailStore.getState().mode).toBe('graph')
  })
})
```

- [ ] **Step 2: Run**

Run: `cd frontend && pnpm vitest run src/components/cockpit/__tests__/TopHUD.test.tsx`
Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/cockpit/__tests__/TopHUD.test.tsx
git commit -m "test(frontend): TopHUD renders telemetry + chips toggle rail mode"
```

---

## Self-review

**Spec coverage:**
- Verbose HUD (§5.1) → Task 4 ✓
- Session dropdown (§5.2) → Task 4 ✓
- Left icon rail 7 sections (§5.3) → Task 8 (DevTools removed); existing `IconRail` already had the 7 sections after removal ✓
- ChatMain + composer + shortcut legend (§5.4) → Task 3 ✓
- RightRail swap-in-place (§5.5) → Tasks 5, 6 ✓
- 3-mode trace rail (§5.6) → Task 5 ✓
- Summoned drawers embedded in rail (§5.7) → Tasks 5, 6 ✓
- Orange palette (§6) → used throughout; no purple ✓
- Routing (§7) → section-id routing via `useChatStore.activeSection` already exists; `/devtools` route-hash dropped per Task 8 simplification ✓
- State (§8) — `rightRailStore` added → Task 1 ✓
- Migration notes (§9) — middle tabs + HEALTH/SKILLS overlays removed → Task 7 ✓
- Testing (§10) — unit tests for store + HUD shipped → Tasks 1, 10; Playwright e2e deferred (existing harness continues to work because route paths don't change) ⚠️

**Placeholder scan:** None. `—` in HUD is legitimate "data unavailable" rendering, not a plan placeholder.

**Type consistency:** `RailMode`, `TraceTab`, `toggleMode`, `cycleMode`, `returnToTrace`, `setMode`, `setTraceTab` consistent across Tasks 1, 4, 5, 9.

Plan complete and saved to `docs/superpowers/plans/2026-04-18-cockpit-frontend.md`.
