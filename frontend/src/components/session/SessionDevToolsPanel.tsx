import { useEffect, useState } from 'react'
import { cn } from '@/lib/utils'
import { SessionHeader } from '@/components/monitor/SessionHeader'
import { TraceTimeline } from '@/components/monitor/TraceTimeline'
import { ContextInspector } from '@/devtools/ContextInspector'

type DevToolsSubTab = 'timeline' | 'context' | 'prompt' | 'events'

interface SubTabDef {
  id: DevToolsSubTab
  label: string
}

const SUB_TABS: SubTabDef[] = [
  { id: 'timeline', label: 'Timeline' },
  { id: 'context', label: 'Context' },
  { id: 'prompt', label: 'Prompt' },
  { id: 'events', label: 'Events' },
]

interface PromptSection {
  source: string
  lines?: string
  text: string
}

interface PromptAssembly {
  sections: PromptSection[]
  conflicts?: unknown[]
}

function joinSectionsBySource(sections: PromptSection[], source: string): string {
  return sections
    .filter((s) => s.source === source)
    .map((s) => s.text)
    .join('\n\n')
}

interface TimelineEvent {
  turn: number
  kind: string
  detail: string
}

interface SessionDevToolsPanelProps {
  sessionId: string | null
}

// ── empty state ───────────────────────────────────────────────────────────────

function EmptyState({ reason }: { reason: string }): React.ReactElement {
  return (
    <div className="flex flex-col h-full items-center justify-center gap-3 px-6">
      <span className="text-[9px] font-mono tracking-[0.3em] text-surface-700 uppercase">
        {reason}
      </span>
      <div className="w-32 h-px bg-surface-800" />
      <span className="text-[10px] font-mono text-surface-600 text-center leading-relaxed max-w-xs">
        Session telemetry — tool calls, context layers, prompt assembly, and compaction events —
        will appear here once a turn is recorded.
      </span>
    </div>
  )
}

// ── prompt inspector ──────────────────────────────────────────────────────────

function PromptInspectorPanel({ sessionId }: { sessionId: string }): React.ReactElement {
  const [state, setState] = useState<
    | { status: 'loading' }
    | { status: 'error'; message: string }
    | { status: 'empty' }
    | { status: 'ok'; data: PromptAssembly; stepId: string }
  >({ status: 'loading' })

  useEffect(() => {
    let cancelled = false
    setState({ status: 'loading' })

    async function load() {
      try {
        const timelineRes = await fetch(`/api/trace/traces/${sessionId}/timeline`)
        if (!timelineRes.ok) throw new Error(`HTTP ${timelineRes.status}`)
        const timeline = (await timelineRes.json()) as { turns: { turn: number }[] }
        if (timeline.turns.length === 0) {
          if (!cancelled) setState({ status: 'empty' })
          return
        }
        const lastTurn = timeline.turns[timeline.turns.length - 1].turn
        const stepId = `s${lastTurn}`
        const promptRes = await fetch(
          `/api/trace/traces/${sessionId}/prompt/${stepId}`,
        )
        if (!promptRes.ok) throw new Error(`HTTP ${promptRes.status}`)
        const data = (await promptRes.json()) as PromptAssembly
        if (!cancelled) setState({ status: 'ok', data, stepId })
      } catch (err) {
        if (!cancelled) {
          setState({
            status: 'error',
            message: err instanceof Error ? err.message : 'Failed to load prompt',
          })
        }
      }
    }

    load()
    return () => {
      cancelled = true
    }
  }, [sessionId])

  if (state.status === 'loading') {
    return (
      <div className="flex h-full items-center justify-center">
        <span className="text-[10px] font-mono text-surface-600 uppercase tracking-widest">
          loading prompt…
        </span>
      </div>
    )
  }

  if (state.status === 'empty') {
    return <EmptyState reason="No prompt recorded yet" />
  }

  if (state.status === 'error') {
    return (
      <div className="flex h-full items-center justify-center px-6">
        <span className="text-[10px] font-mono text-red-400">{state.message}</span>
      </div>
    )
  }

  const { data, stepId } = state
  const sections = data.sections ?? []
  const systemText = joinSectionsBySource(sections, 'system_prompt')
  const userText = joinSectionsBySource(sections, 'user_query')
  return (
    <div className="flex flex-col h-full gap-4 p-4 overflow-y-auto">
      <div className="flex items-baseline gap-3">
        <span className="text-[9px] font-mono tracking-[0.25em] text-surface-500 uppercase">
          Step
        </span>
        <span className="text-[11px] font-mono text-brand-accent">{stepId}</span>
        <span className="ml-auto text-[9px] font-mono tracking-[0.25em] text-surface-600 uppercase">
          {sections.length} sections
        </span>
      </div>

      <section>
        <div className="flex items-center gap-2 mb-2">
          <span className="text-[9px] font-mono tracking-[0.25em] text-surface-500 uppercase">
            System
          </span>
          <div className="flex-1 h-px bg-surface-800" />
        </div>
        <pre className="text-[10px] font-mono text-surface-300 leading-relaxed whitespace-pre-wrap break-words bg-surface-900/40 border border-surface-800 rounded p-3 max-h-[40vh] overflow-y-auto">
          {systemText || '(no system_prompt section recorded)'}
        </pre>
      </section>

      <section>
        <div className="flex items-center gap-2 mb-2">
          <span className="text-[9px] font-mono tracking-[0.25em] text-surface-500 uppercase">
            User
          </span>
          <div className="flex-1 h-px bg-surface-800" />
        </div>
        <pre className="text-[10px] font-mono text-surface-300 leading-relaxed whitespace-pre-wrap break-words bg-surface-900/40 border border-surface-800 rounded p-3 max-h-[40vh] overflow-y-auto">
          {userText || '(no user_query section recorded)'}
        </pre>
      </section>
    </div>
  )
}

// ── raw events ────────────────────────────────────────────────────────────────

function EventsPanel({ sessionId }: { sessionId: string }): React.ReactElement {
  const [state, setState] = useState<
    | { status: 'loading' }
    | { status: 'error'; message: string }
    | { status: 'ok'; events: TimelineEvent[] }
  >({ status: 'loading' })

  useEffect(() => {
    let cancelled = false
    setState({ status: 'loading' })
    fetch(`/api/trace/traces/${sessionId}/timeline`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        return res.json() as Promise<{ events: TimelineEvent[] }>
      })
      .then((data) => {
        if (!cancelled) setState({ status: 'ok', events: data.events ?? [] })
      })
      .catch((err) => {
        if (!cancelled) {
          setState({
            status: 'error',
            message: err instanceof Error ? err.message : 'Failed to load events',
          })
        }
      })
    return () => {
      cancelled = true
    }
  }, [sessionId])

  if (state.status === 'loading') {
    return (
      <div className="flex h-full items-center justify-center">
        <span className="text-[10px] font-mono text-surface-600 uppercase tracking-widest">
          loading events…
        </span>
      </div>
    )
  }
  if (state.status === 'error') {
    return (
      <div className="flex h-full items-center justify-center px-6">
        <span className="text-[10px] font-mono text-red-400">{state.message}</span>
      </div>
    )
  }
  if (state.events.length === 0) {
    return <EmptyState reason="No events yet" />
  }

  return (
    <div className="flex flex-col h-full overflow-y-auto p-3 gap-1.5">
      {state.events.map((ev, i) => (
        <div
          key={i}
          className={cn(
            'flex items-center gap-3 px-2.5 py-1.5 rounded border',
            ev.kind === 'compaction'
              ? 'border-amber-900/50 bg-amber-950/20'
              : 'border-surface-800 bg-surface-900/40',
          )}
        >
          <span className="text-[9px] font-mono tracking-widest text-surface-600 uppercase shrink-0 w-8">
            T{ev.turn}
          </span>
          <span
            className={cn(
              'text-[10px] font-mono uppercase tracking-widest shrink-0 w-20',
              ev.kind === 'compaction' ? 'text-amber-400' : 'text-surface-400',
            )}
          >
            {ev.kind}
          </span>
          <span className="text-[10px] font-mono text-surface-500 truncate">
            {ev.detail}
          </span>
        </div>
      ))}
    </div>
  )
}

// ── main panel ────────────────────────────────────────────────────────────────

export function SessionDevToolsPanel({
  sessionId,
}: SessionDevToolsPanelProps): React.ReactElement {
  const [activeTab, setActiveTab] = useState<DevToolsSubTab>('timeline')

  if (!sessionId) {
    return (
      <div className="flex flex-col h-full bg-canvas">
        <div className="flex items-center gap-3 px-4 h-11 border-b border-surface-800 shrink-0">
          <span className="font-mono text-[10px] text-surface-500 uppercase tracking-widest">
            Session DevTools
          </span>
        </div>
        <div className="flex-1 min-h-0">
          <EmptyState reason="No active session" />
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full bg-canvas">
      {/* Top: session header (id, level, duration, outcome) */}
      <div className="flex items-center h-11 shrink-0 border-b border-surface-800 bg-[#09090b]">
        <div className="flex-1 min-w-0 h-full">
          <SessionHeader sessionId={sessionId} />
        </div>
      </div>

      {/* Sub-tab row — caps mono, orange underline when active */}
      <div
        role="tablist"
        aria-label="Session DevTools sections"
        className="flex items-center border-b border-surface-800 bg-surface-900/60 shrink-0"
      >
        {SUB_TABS.map((tab) => {
          const isActive = activeTab === tab.id
          return (
            <button
              key={tab.id}
              role="tab"
              aria-selected={isActive}
              onClick={() => setActiveTab(tab.id)}
              className={cn(
                'flex items-center px-4 py-2.5',
                'text-[10px] font-mono font-semibold tracking-[0.2em] uppercase',
                'border-b transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-brand-accent/50',
                isActive
                  ? 'border-brand-accent/80 text-surface-200'
                  : 'border-transparent text-surface-600 hover:text-surface-400',
              )}
            >
              {tab.label}
            </button>
          )
        })}
      </div>

      {/* Active panel content */}
      <div className="flex-1 min-h-0 overflow-hidden">
        {activeTab === 'timeline' && <TraceTimeline sessionId={sessionId} />}
        {activeTab === 'context' && (
          <div className="h-full overflow-hidden">
            <ContextInspector />
          </div>
        )}
        {activeTab === 'prompt' && <PromptInspectorPanel sessionId={sessionId} />}
        {activeTab === 'events' && <EventsPanel sessionId={sessionId} />}
      </div>
    </div>
  )
}
