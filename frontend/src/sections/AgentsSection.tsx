import { useCallback, useEffect, useRef, useState } from 'react'
import { listTraces, type TraceListItem } from '@/lib/api'
import { cn } from '@/lib/utils'

type FilterTab = 'all' | 'done' | 'failed'

const REFRESH_INTERVAL_MS = 5_000

function formatDuration(ms: number): string {
  if (ms < 1000) return `${ms}ms`
  if (ms < 60_000) return `${(ms / 1000).toFixed(1)}s`
  const m = Math.floor(ms / 60_000)
  const s = Math.round((ms % 60_000) / 1000)
  return `${m}m ${s}s`
}

function formatTokens(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}k`
  return String(n)
}

function formatTimestamp(iso: string): string {
  try {
    const d = new Date(iso)
    return d.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit', second: '2-digit' })
  } catch {
    return iso
  }
}

function truncateId(id: string): string {
  if (id.length <= 16) return id
  return `${id.slice(0, 8)}…${id.slice(-6)}`
}

function outcomeToStatus(outcome: string): 'running' | 'done' | 'failed' {
  if (outcome === 'running') return 'running'
  if (outcome === 'pass' || outcome === 'ok') return 'done'
  return 'failed'
}

interface AgentCardProps {
  trace: TraceListItem
  compact?: boolean
}

function AgentCard({ trace, compact = false }: AgentCardProps) {
  const status = outcomeToStatus(trace.outcome)
  const totalTokens = trace.total_input_tokens + trace.total_output_tokens

  function handleClick() {
    window.location.hash = `#/monitor/${trace.session_id}`
  }

  return (
    <button
      type="button"
      onClick={handleClick}
      className={cn(
        'flex flex-col gap-2.5 rounded-md border bg-surface-900 text-left transition-colors',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500',
        'w-full',
        compact ? 'p-3 border-surface-700/80' : 'p-4 border-surface-800',
        status === 'running'
          ? 'hover:border-emerald-700/60 hover:bg-surface-850 border-emerald-900/60'
          : 'hover:border-surface-700 hover:bg-surface-850',
      )}
      title={`Session ${trace.session_id}`}
    >
      {/* Header row */}
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0 flex flex-col gap-0.5">
          <span className="font-mono text-xs font-semibold text-surface-200 truncate">
            {truncateId(trace.session_id)}
          </span>
          {trace.started_at && (
            <span className="font-mono text-[10px] text-surface-600">
              {formatTimestamp(trace.started_at)}
            </span>
          )}
        </div>

        <div className="flex items-center gap-1.5 flex-shrink-0">
          {/* Grade badge */}
          {trace.final_grade && (
            <span
              className={cn(
                'text-[10px] font-mono font-semibold px-1 py-0.5',
                trace.final_grade === 'A'
                  ? 'text-emerald-400'
                  : trace.final_grade === 'B'
                    ? 'text-brand-400'
                    : trace.final_grade === 'C'
                      ? 'text-amber-400'
                      : 'text-red-400',
              )}
            >
              {trace.final_grade}
            </span>
          )}

          {/* Status badge */}
          <span
            className={cn(
              'flex-shrink-0 text-[10px] font-mono font-semibold uppercase tracking-wider px-1.5 py-0.5 rounded border flex items-center gap-1',
              status === 'running'
                ? 'bg-emerald-950/60 text-emerald-400 border-emerald-900/60'
                : status === 'done'
                  ? 'bg-surface-800/60 text-surface-400 border-surface-700/60'
                  : 'bg-red-950/60 text-red-400 border-red-900/60',
            )}
          >
            {status === 'running' && (
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" aria-hidden />
            )}
            {status === 'running' ? 'RUNNING' : status === 'done' ? '✓ DONE' : '✗ FAILED'}
          </span>
        </div>
      </div>

      {/* Metrics row */}
      <div className="flex items-center gap-4 text-[11px] font-mono text-surface-500">
        <span title="Duration" className="flex items-center gap-1">
          <span className="text-surface-700">dur</span>
          <span className="text-surface-400">{formatDuration(trace.duration_ms)}</span>
        </span>
        <span title="Turns" className="flex items-center gap-1">
          <span className="text-surface-700">turns</span>
          <span className="text-surface-400">{trace.turn_count}</span>
        </span>
        <span title="Tokens" className="flex items-center gap-1">
          <span className="text-surface-700">tok</span>
          <span className="text-surface-400">{formatTokens(totalTokens)}</span>
        </span>
        {trace.llm_call_count > 0 && (
          <span title="LLM calls" className="flex items-center gap-1">
            <span className="text-surface-700">llm</span>
            <span className="text-surface-400">{trace.llm_call_count}</span>
          </span>
        )}
      </div>

      {/* View link */}
      <div className="flex items-center justify-end">
        <span className="text-[10px] font-mono text-brand-500/70 hover:text-brand-400 transition-colors">
          View →
        </span>
      </div>
    </button>
  )
}

const FILTER_TABS: Array<{ id: FilterTab; label: string }> = [
  { id: 'all', label: 'All' },
  { id: 'done', label: 'Done' },
  { id: 'failed', label: 'Failed' },
]

export function AgentsSection() {
  const [traces, setTraces] = useState<TraceListItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [filter, setFilter] = useState<FilterTab>('all')
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null)
  const [secondsAgo, setSecondsAgo] = useState(0)
  const tickRef = useRef<ReturnType<typeof setInterval> | null>(null)

  const fetchData = useCallback(async () => {
    try {
      const data = await listTraces()
      setTraces(data)
      setError(null)
      setLastUpdated(new Date())
      setSecondsAgo(0)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load traces'
      setError(message)
    } finally {
      setLoading(false)
    }
  }, [])

  // Data refresh every 5s
  useEffect(() => {
    void fetchData()
    const interval = setInterval(() => void fetchData(), REFRESH_INTERVAL_MS)
    return () => clearInterval(interval)
  }, [fetchData])

  // "X seconds ago" ticker
  useEffect(() => {
    tickRef.current = setInterval(() => {
      if (lastUpdated) {
        setSecondsAgo(Math.floor((Date.now() - lastUpdated.getTime()) / 1000))
      }
    }, 1000)
    return () => {
      if (tickRef.current) clearInterval(tickRef.current)
    }
  }, [lastUpdated])

  const running = traces.filter((t) => outcomeToStatus(t.outcome) === 'running')
  const completed = traces.filter((t) => outcomeToStatus(t.outcome) !== 'running')

  const filtered = completed.filter((t) => {
    if (filter === 'all') return true
    return outcomeToStatus(t.outcome) === filter
  })

  function formatSecondsAgo(s: number): string {
    if (s < 5) return 'just now'
    if (s < 60) return `${s}s ago`
    return `${Math.floor(s / 60)}m ago`
  }

  return (
    <div className="flex flex-col h-full bg-surface-950 text-surface-100 overflow-hidden">
      {/* Header */}
      <header className="flex items-center gap-4 px-6 py-4 border-b border-surface-800 flex-shrink-0">
        <h1 className="font-mono text-xs font-semibold text-surface-300 uppercase tracking-widest">
          MONITORING
        </h1>

        {/* Filter tabs */}
        <div
          role="tablist"
          aria-label="Filter agent sessions"
          className="flex items-center gap-0.5"
        >
          {FILTER_TABS.map(({ id, label }) => (
            <button
              key={id}
              role="tab"
              aria-selected={filter === id}
              type="button"
              onClick={() => setFilter(id)}
              className={cn(
                'px-3 py-1 rounded text-xs font-mono font-medium transition-colors',
                'focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-brand-500',
                filter === id
                  ? 'bg-surface-800 text-surface-100'
                  : 'text-surface-500 hover:text-surface-300 hover:bg-surface-800/40',
              )}
            >
              {label}
              {id === 'all' && traces.length > 0 && (
                <span className="ml-1 text-surface-600">{traces.length}</span>
              )}
              {id === 'failed' && completed.filter((t) => outcomeToStatus(t.outcome) === 'failed').length > 0 && (
                <span className="ml-1 text-red-500/70">
                  {completed.filter((t) => outcomeToStatus(t.outcome) === 'failed').length}
                </span>
              )}
            </button>
          ))}
        </div>

        <div className="flex-1" />

        {/* Last updated */}
        {lastUpdated && (
          <span className="text-[10px] font-mono text-surface-600">
            Updated {formatSecondsAgo(secondsAgo)}
          </span>
        )}

        {/* Live indicator */}
        <span className="flex items-center gap-1.5 text-[10px] font-mono text-surface-600">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" aria-hidden />
          LIVE
        </span>
      </header>

      {/* Body */}
      <main className="flex-1 min-h-0 overflow-y-auto px-6 py-5 space-y-6">
        {loading && (
          <p className="text-xs font-mono text-surface-500 text-center py-12">
            Loading agent sessions…
          </p>
        )}

        {!loading && error && (
          <div
            role="alert"
            className="rounded-md border border-red-900/60 bg-red-950/40 px-4 py-3 text-xs font-mono text-red-300"
          >
            {error}
          </div>
        )}

        {!loading && !error && (
          <>
            {/* Running now section */}
            {running.length > 0 && (
              <section aria-labelledby="running-heading">
                <div className="flex items-center gap-2 mb-3">
                  <span
                    id="running-heading"
                    className="text-[10px] font-mono font-semibold text-emerald-400 uppercase tracking-widest"
                  >
                    RUNNING NOW
                  </span>
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" aria-hidden />
                  <span className="text-[10px] font-mono text-surface-600">{running.length}</span>
                </div>
                <div className="grid gap-3 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
                  {running.map((trace) => (
                    <AgentCard key={trace.session_id} trace={trace} compact />
                  ))}
                </div>
              </section>
            )}

            {/* Completed sessions grid */}
            {filtered.length === 0 ? (
              <p className="text-xs font-mono text-surface-500 text-center py-12">
                {filter === 'all'
                  ? running.length > 0
                    ? 'No completed sessions yet.'
                    : 'No agent sessions recorded yet.'
                  : `No ${filter} sessions.`}
              </p>
            ) : (
              <section aria-label="Completed sessions">
                {running.length > 0 && (
                  <div className="flex items-center gap-2 mb-3">
                    <span className="text-[10px] font-mono font-semibold text-surface-500 uppercase tracking-widest">
                      COMPLETED
                    </span>
                    <span className="text-[10px] font-mono text-surface-600">{filtered.length}</span>
                  </div>
                )}
                <div className="grid gap-3 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
                  {filtered.map((trace) => (
                    <AgentCard key={trace.session_id} trace={trace} />
                  ))}
                </div>
              </section>
            )}
          </>
        )}
      </main>
    </div>
  )
}
