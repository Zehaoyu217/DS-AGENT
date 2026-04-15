import { useCallback, useEffect, useState } from 'react'
import { ChevronRight, Layers, RefreshCw, X } from 'lucide-react'
import {
  type CompactionDiff,
  type SessionContextSnapshot,
  fetchCompactionDiff,
  fetchSessionContext,
  listContextSessions,
} from '@/lib/api'
import { useChatStore } from '@/lib/store'
import { cn } from '@/lib/utils'

// ── Layer color palette by layer name keyword ─────────────────────────────────
const LAYER_COLORS: Record<string, string> = {
  'System Prompt': '#8b5cf6',   // brand purple — L1, never compacted
  'User Message': '#3b82f6',    // blue — incoming user turn
  'Assistant Turns': '#10b981', // green — model output
  'Tool Results': '#f59e0b',    // amber — tool call outputs
  'Dataset Context': '#06b6d4', // cyan — loaded dataset
}

function layerColor(name: string): string {
  for (const [key, color] of Object.entries(LAYER_COLORS)) {
    if (name.includes(key)) return color
  }
  return '#6b7280'
}

// ── Stacked token bar ─────────────────────────────────────────────────────────
function StackedBar({ snapshot }: { snapshot: SessionContextSnapshot }) {
  const { layers, total_tokens, max_tokens } = snapshot
  if (total_tokens === 0 || max_tokens === 0) {
    return (
      <div className="h-5 w-full rounded bg-surface-800 flex items-center justify-center">
        <span className="font-mono text-[10px] text-surface-600">no data</span>
      </div>
    )
  }

  // Each layer's share of the total bar width = (layer.tokens / max_tokens) * 100%
  return (
    <div className="space-y-1">
      <div
        className="h-5 w-full rounded overflow-hidden flex"
        role="img"
        aria-label="Token budget breakdown"
      >
        {layers.map((layer) => {
          const pct = (layer.tokens / max_tokens) * 100
          if (pct < 0.1) return null
          return (
            <div
              key={layer.name}
              title={`${layer.name}: ${layer.tokens.toLocaleString()} tokens`}
              style={{ width: `${pct}%`, backgroundColor: layerColor(layer.name) }}
              className="transition-all duration-300 opacity-80 hover:opacity-100"
            />
          )
        })}
        {/* Remaining budget in gray */}
        {total_tokens < max_tokens && (
          <div
            className="flex-1 bg-surface-800"
            title={`Free: ${(max_tokens - total_tokens).toLocaleString()} tokens`}
          />
        )}
      </div>
      {/* Legend */}
      <div className="flex flex-wrap gap-x-4 gap-y-1">
        {layers.filter((l) => l.tokens > 0).map((layer) => (
          <div key={layer.name} className="flex items-center gap-1.5">
            <span
              className="w-2 h-2 rounded-sm flex-shrink-0"
              style={{ backgroundColor: layerColor(layer.name) }}
            />
            <span className="font-mono text-[10px] text-surface-400">{layer.name}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

// ── Layer breakdown table ─────────────────────────────────────────────────────
function LayerTable({ snapshot }: { snapshot: SessionContextSnapshot }) {
  const { layers, max_tokens } = snapshot
  const sorted = [...layers].sort((a, b) => b.tokens - a.tokens)

  return (
    <div className="rounded border border-surface-800 overflow-hidden">
      <table className="w-full text-xs font-mono">
        <thead>
          <tr className="border-b border-surface-800 bg-surface-900">
            <th className="text-left px-3 py-2 text-[10px] text-surface-500 uppercase tracking-wider font-semibold">
              Layer
            </th>
            <th className="text-right px-3 py-2 text-[10px] text-surface-500 uppercase tracking-wider font-semibold">
              Tokens
            </th>
            <th className="text-right px-3 py-2 text-[10px] text-surface-500 uppercase tracking-wider font-semibold">
              Share
            </th>
            <th className="text-center px-3 py-2 text-[10px] text-surface-500 uppercase tracking-wider font-semibold">
              Compactable
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-surface-800/50">
          {sorted.map((layer) => {
            const share = max_tokens > 0 ? (layer.tokens / max_tokens) * 100 : 0
            return (
              <tr
                key={layer.name}
                className="bg-surface-950 hover:bg-surface-900 transition-colors"
              >
                <td className="px-3 py-2">
                  <div className="flex items-center gap-2">
                    <span
                      className="w-1.5 h-1.5 rounded-full flex-shrink-0"
                      style={{ backgroundColor: layerColor(layer.name) }}
                    />
                    <span className="text-surface-200">{layer.name}</span>
                  </div>
                </td>
                <td className="px-3 py-2 text-right text-surface-300">
                  {layer.tokens.toLocaleString()}
                </td>
                <td className="px-3 py-2 text-right text-surface-500">
                  {share.toFixed(1)}%
                </td>
                <td className="px-3 py-2 text-center">
                  {layer.compactable ? (
                    <span className="text-amber-500/80">yes</span>
                  ) : (
                    <span className="text-surface-600">—</span>
                  )}
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

// ── Compaction history list ───────────────────────────────────────────────────
interface CompactionRowProps {
  entry: SessionContextSnapshot['compaction_history'][number]
  onSelect: (id: number) => void
  selected: boolean
}

function CompactionRow({ entry, onSelect, selected }: CompactionRowProps) {
  const lossPct =
    entry.tokens_before > 0
      ? ((entry.tokens_freed / entry.tokens_before) * 100).toFixed(1)
      : '0.0'
  const severity =
    Number(lossPct) >= 40 ? 'HIGH' : Number(lossPct) >= 20 ? 'MEDIUM' : 'LOW'
  const severityColor =
    severity === 'HIGH'
      ? 'text-red-400'
      : severity === 'MEDIUM'
        ? 'text-amber-400'
        : 'text-green-400'

  return (
    <button
      type="button"
      onClick={() => onSelect(entry.id)}
      className={cn(
        'w-full text-left px-3 py-2.5 transition-colors hover:bg-surface-800 flex items-center gap-3',
        selected && 'bg-surface-800 border-l-2 border-brand-500',
      )}
    >
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <span className="font-mono text-[10px] text-surface-500">
            #{entry.id}
          </span>
          <span className="font-mono text-[10px] text-surface-400">
            {new Date(entry.timestamp).toLocaleTimeString()}
          </span>
          <span className={cn('font-mono text-[10px] font-semibold', severityColor)}>
            {severity}
          </span>
        </div>
        <div className="flex items-center gap-3 mt-0.5">
          <span className="font-mono text-xs text-surface-300">
            {entry.tokens_before.toLocaleString()} → {entry.tokens_after.toLocaleString()}
          </span>
          <span className="font-mono text-[10px] text-red-400">
            −{entry.tokens_freed.toLocaleString()} ({lossPct}%)
          </span>
        </div>
      </div>
      <ChevronRight className="w-3 h-3 text-surface-600 flex-shrink-0" />
    </button>
  )
}

// ── Compaction diff panel ─────────────────────────────────────────────────────
function CompactionDiffPanel({
  diff,
  onClose,
}: {
  diff: CompactionDiff
  onClose: () => void
}) {
  const severityColor =
    diff.loss_severity === 'HIGH'
      ? 'text-red-400 bg-red-950/40 border-red-900/60'
      : diff.loss_severity === 'MEDIUM'
        ? 'text-amber-400 bg-amber-950/40 border-amber-900/60'
        : 'text-green-400 bg-green-950/40 border-green-900/60'

  return (
    <div className="space-y-4">
      {/* Header metrics */}
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="font-mono text-[10px] text-surface-500 uppercase tracking-wider mb-1">
            Compaction #{diff.compaction_id} — {new Date(diff.timestamp).toLocaleString()}
          </p>
          <div className="flex items-center gap-4">
            <span className="font-mono text-xs text-surface-300">
              {diff.tokens_before.toLocaleString()} → {diff.tokens_after.toLocaleString()} tok
            </span>
            <span className="font-mono text-xs text-red-400">
              −{diff.tokens_freed.toLocaleString()} freed
            </span>
            <span className="font-mono text-xs text-surface-500">
              trigger: {(diff.trigger_utilization * 100).toFixed(1)}%
            </span>
          </div>
        </div>
        <button
          type="button"
          onClick={onClose}
          className="p-1 rounded hover:bg-surface-800 text-surface-500 hover:text-surface-300"
          aria-label="Close diff"
        >
          <X className="w-3 h-3" />
        </button>
      </div>

      {/* Information loss badge */}
      <div
        className={cn(
          'inline-flex items-center gap-2 px-3 py-1.5 rounded border font-mono text-xs',
          severityColor,
        )}
      >
        <span className="font-semibold">{diff.loss_severity}</span>
        <span>information loss</span>
        <span className="opacity-80">{diff.information_loss_pct}%</span>
      </div>

      {/* Side-by-side diff */}
      <div className="grid grid-cols-2 gap-3">
        {/* Removed */}
        <div className="space-y-2">
          <h3 className="font-mono text-[10px] text-red-400 uppercase tracking-wider">
            Removed ({diff.removed.length})
          </h3>
          <div className="rounded border border-red-900/40 bg-red-950/20 overflow-hidden">
            {diff.removed.length === 0 ? (
              <p className="px-3 py-2 font-mono text-[10px] text-surface-600">none</p>
            ) : (
              diff.removed.map((item, i) => (
                <div
                  key={i}
                  className="flex items-center justify-between px-3 py-1.5 border-b border-red-900/20 last:border-0"
                >
                  <span className="font-mono text-[10px] text-red-300 truncate">
                    {typeof item === 'string' ? item : item.name ?? String(item)}
                  </span>
                  {typeof item === 'object' && item.tokens != null && (
                    <span className="font-mono text-[10px] text-red-500 flex-shrink-0 ml-2">
                      {(item.tokens as number).toLocaleString()} tok
                    </span>
                  )}
                </div>
              ))
            )}
          </div>
        </div>

        {/* Survived */}
        <div className="space-y-2">
          <h3 className="font-mono text-[10px] text-green-400 uppercase tracking-wider">
            Survived ({diff.survived.length})
          </h3>
          <div className="rounded border border-green-900/40 bg-green-950/20 overflow-hidden">
            {diff.survived.length === 0 ? (
              <p className="px-3 py-2 font-mono text-[10px] text-surface-600">none</p>
            ) : (
              diff.survived.map((name, i) => (
                <div
                  key={i}
                  className="px-3 py-1.5 border-b border-green-900/20 last:border-0"
                >
                  <span className="font-mono text-[10px] text-green-300">{name}</span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

// ── Session picker ────────────────────────────────────────────────────────────
function SessionPicker({
  sessions,
  selected,
  onSelect,
}: {
  sessions: string[]
  selected: string
  onSelect: (s: string) => void
}) {
  if (sessions.length === 0) return null
  return (
    <div className="flex items-center gap-2">
      <span className="font-mono text-[10px] text-surface-500 uppercase tracking-wider">
        Session
      </span>
      <select
        value={selected}
        onChange={(e) => onSelect(e.target.value)}
        className="flex-1 bg-surface-900 border border-surface-700 rounded px-2 py-1 font-mono text-[10px] text-surface-300 focus:outline-none focus:border-brand-500"
      >
        {sessions.map((s) => (
          <option key={s} value={s}>
            {s.length > 40 ? `…${s.slice(-38)}` : s}
          </option>
        ))}
      </select>
    </div>
  )
}

// ── Main section ──────────────────────────────────────────────────────────────
export function ContextSection() {
  const activeConversationId = useChatStore((s) => s.activeConversationId)
  const conversations = useChatStore((s) => s.conversations)

  // Derive the backend session_id for the active conversation
  const activeConv = conversations.find((c) => c.id === activeConversationId)
  const derivedSessionId = activeConv?.sessionId ?? null

  const [sessions, setSessions] = useState<string[]>([])
  const [selectedSession, setSelectedSession] = useState<string>('')
  const [snapshot, setSnapshot] = useState<SessionContextSnapshot | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedCompaction, setSelectedCompaction] = useState<number | null>(null)
  const [diff, setDiff] = useState<CompactionDiff | null>(null)
  const [diffLoading, setDiffLoading] = useState(false)

  // Fetch available sessions
  const loadSessions = useCallback(async () => {
    try {
      const { sessions: list } = await listContextSessions()
      setSessions(list)
      // Auto-select the active conversation's session if available
      if (derivedSessionId && list.includes(derivedSessionId)) {
        setSelectedSession(derivedSessionId)
      } else if (list.length > 0 && !selectedSession) {
        setSelectedSession(list[0])
      }
    } catch {
      // Non-fatal — just leave sessions empty
    }
  }, [derivedSessionId, selectedSession])

  // Fetch snapshot for selected session
  const loadSnapshot = useCallback(async (sessionId: string) => {
    if (!sessionId) return
    setLoading(true)
    try {
      const data = await fetchSessionContext(sessionId)
      setSnapshot(data)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load context')
    } finally {
      setLoading(false)
    }
  }, [])

  // Load compaction diff when selected
  const loadDiff = useCallback(async (sessionId: string, compactionId: number) => {
    setDiffLoading(true)
    try {
      const data = await fetchCompactionDiff(sessionId, compactionId)
      setDiff(data)
    } catch {
      setDiff(null)
    } finally {
      setDiffLoading(false)
    }
  }, [])

  useEffect(() => {
    void loadSessions()
  }, [loadSessions])

  // Auto-update selected session when active chat changes
  useEffect(() => {
    if (derivedSessionId && sessions.includes(derivedSessionId)) {
      setSelectedSession(derivedSessionId)
    }
  }, [derivedSessionId, sessions])

  useEffect(() => {
    if (!selectedSession) return
    void loadSnapshot(selectedSession)
    const interval = setInterval(() => void loadSnapshot(selectedSession), 10_000)
    return () => clearInterval(interval)
  }, [selectedSession, loadSnapshot])

  useEffect(() => {
    if (selectedCompaction !== null && selectedSession) {
      void loadDiff(selectedSession, selectedCompaction)
    } else {
      setDiff(null)
    }
  }, [selectedCompaction, selectedSession, loadDiff])

  const pct =
    snapshot && snapshot.max_tokens > 0
      ? Math.min(100, (snapshot.total_tokens / snapshot.max_tokens) * 100)
      : 0

  const utilizationColor =
    pct >= 80 ? 'text-red-400' : pct >= 60 ? 'text-amber-400' : 'text-brand-400'

  return (
    <div className="flex flex-col h-full bg-surface-950 text-surface-100 overflow-hidden">
      {/* Header */}
      <header className="flex items-center gap-3 px-6 py-4 border-b border-surface-800 flex-shrink-0">
        <Layers className="w-4 h-4 text-surface-500" aria-hidden />
        <h1 className="font-mono text-xs font-semibold text-surface-300 uppercase tracking-widest">
          CONTEXT
        </h1>
        {snapshot && (
          <span className={cn('ml-2 font-mono text-xs font-semibold', utilizationColor)}>
            {pct.toFixed(1)}%
          </span>
        )}
        <button
          type="button"
          onClick={() => selectedSession && void loadSnapshot(selectedSession)}
          className="ml-auto p-1.5 rounded hover:bg-surface-800 text-surface-500 hover:text-surface-300 transition-colors"
          aria-label="Refresh context"
        >
          <RefreshCw className="w-3.5 h-3.5" />
        </button>
      </header>

      <main className="flex-1 min-h-0 overflow-y-auto px-6 py-5 space-y-6">
        {/* Session picker */}
        <SessionPicker
          sessions={sessions}
          selected={selectedSession}
          onSelect={(s) => {
            setSelectedSession(s)
            setSelectedCompaction(null)
            setDiff(null)
          }}
        />

        {!selectedSession && !loading && (
          <p className="font-mono text-xs text-surface-500 text-center py-12">
            No sessions tracked yet — send a chat message to populate context data.
          </p>
        )}

        {loading && selectedSession && (
          <p className="font-mono text-xs text-surface-500 text-center py-12">
            Loading context snapshot…
          </p>
        )}

        {!loading && error && (
          <div
            role="alert"
            className="rounded border border-red-900/60 bg-red-950/40 px-4 py-3 font-mono text-xs text-red-300"
          >
            {error}
          </div>
        )}

        {!loading && !error && snapshot && (
          <>
            {/* Token budget summary */}
            <section className="space-y-3">
              <div className="flex items-baseline justify-between">
                <h2 className="font-mono text-[10px] text-surface-500 uppercase tracking-widest">
                  Token Budget
                </h2>
                <span className="font-mono text-xs text-surface-300">
                  {snapshot.total_tokens.toLocaleString()} / {snapshot.max_tokens.toLocaleString()}
                </span>
              </div>
              <StackedBar snapshot={snapshot} />
              {snapshot.compaction_needed && (
                <p className="font-mono text-[10px] text-amber-400">
                  ⚠ Compaction recommended ({pct.toFixed(1)}% utilization)
                </p>
              )}
            </section>

            {/* Layer breakdown */}
            {snapshot.layers.length > 0 && (
              <section className="space-y-2">
                <h2 className="font-mono text-[10px] text-surface-500 uppercase tracking-widest">
                  Layer Breakdown
                </h2>
                <LayerTable snapshot={snapshot} />
              </section>
            )}

            {/* Compaction history */}
            <section className="space-y-3">
              <div className="flex items-center justify-between">
                <h2 className="font-mono text-[10px] text-surface-500 uppercase tracking-widest">
                  Compaction History
                </h2>
                {snapshot.compaction_history.length > 0 && (
                  <span className="font-mono text-[10px] text-surface-600">
                    {snapshot.compaction_history.length} event
                    {snapshot.compaction_history.length !== 1 ? 's' : ''}
                  </span>
                )}
              </div>

              {snapshot.compaction_history.length === 0 ? (
                <p className="font-mono text-[10px] text-surface-600">
                  No compaction events recorded yet.
                </p>
              ) : (
                <div className="rounded border border-surface-800 divide-y divide-surface-800 overflow-hidden">
                  {[...snapshot.compaction_history].reverse().map((entry) => (
                    <CompactionRow
                      key={entry.id}
                      entry={entry}
                      selected={selectedCompaction === entry.id}
                      onSelect={(id) =>
                        setSelectedCompaction((prev) => (prev === id ? null : id))
                      }
                    />
                  ))}
                </div>
              )}

              {/* Diff panel */}
              {selectedCompaction !== null && (
                <div className="rounded border border-surface-800 bg-surface-900 p-4">
                  {diffLoading ? (
                    <p className="font-mono text-xs text-surface-500">Loading diff…</p>
                  ) : diff ? (
                    <CompactionDiffPanel
                      diff={diff}
                      onClose={() => {
                        setSelectedCompaction(null)
                        setDiff(null)
                      }}
                    />
                  ) : (
                    <p className="font-mono text-xs text-red-400">Failed to load diff.</p>
                  )}
                </div>
              )}
            </section>

            {/* Layer items detail */}
            {snapshot.layers.some((l) => l.items.length > 0) && (
              <section className="space-y-2">
                <h2 className="font-mono text-[10px] text-surface-500 uppercase tracking-widest">
                  Layer Detail
                </h2>
                <div className="space-y-2">
                  {snapshot.layers
                    .filter((l) => l.items.length > 0)
                    .map((layer) => (
                      <details key={layer.name} className="group rounded border border-surface-800">
                        <summary className="flex items-center gap-2 px-3 py-2 cursor-pointer hover:bg-surface-800 transition-colors list-none">
                          <ChevronRight className="w-3 h-3 text-surface-600 group-open:rotate-90 transition-transform" />
                          <span
                            className="w-1.5 h-1.5 rounded-full"
                            style={{ backgroundColor: layerColor(layer.name) }}
                          />
                          <span className="font-mono text-xs text-surface-300">{layer.name}</span>
                          <span className="ml-auto font-mono text-[10px] text-surface-500">
                            {layer.items.length} item{layer.items.length !== 1 ? 's' : ''}
                          </span>
                        </summary>
                        <div className="border-t border-surface-800 divide-y divide-surface-800/50">
                          {layer.items.map((item, i) => (
                            <div
                              key={i}
                              className="flex items-center justify-between px-4 py-1.5 bg-surface-950"
                            >
                              <span className="font-mono text-[10px] text-surface-400">
                                {item.name}
                              </span>
                              <span className="font-mono text-[10px] text-surface-600">
                                {item.tokens.toLocaleString()} tok
                              </span>
                            </div>
                          ))}
                        </div>
                      </details>
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
