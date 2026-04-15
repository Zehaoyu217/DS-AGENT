import { useEffect, useState } from 'react'
import { useChatStore } from '@/lib/store'
import { fetchSessionContext, fetchContext } from '@/lib/api'
import type { ContextSnapshot } from '@/lib/api'
import { cn } from '@/lib/utils'

// Matches the color map used in ContextSection to stay consistent.
// Semantically distinct colors so each layer is identifiable at small bar sizes
const LAYER_COLORS: Record<string, string> = {
  'System Prompt': '#3b82f6',    // info blue  (--color-info)
  'User Message': '#22c55e',     // success green (--color-success)
  'Assistant Turns': '#e0733a',  // brand orange (--color-accent)
  'Tool Results': '#f59e0b',     // warning amber (--color-warning)
  'Dataset Context': '#2563eb',  // deeper info blue — distinct from System Prompt at small sizes
}

function layerColor(name: string): string {
  for (const [key, color] of Object.entries(LAYER_COLORS)) {
    if (name.includes(key)) return color
  }
  return '#3f3f46' // surface-700
}

function layerShort(name: string): string {
  return name
    .replace('System Prompt', 'SYS')
    .replace('Assistant Turns', 'ASST')
    .replace('User Message', 'USR')
    .replace('Tool Results', 'TOOLS')
    .replace('Dataset Context', 'DATA')
    .toUpperCase()
}

function fmtTokens(n: number): string {
  if (n >= 1000) return `${(n / 1000).toFixed(0)}k`
  return `${n}`
}

export function ContextBar() {
  const conversations = useChatStore((s) => s.conversations)
  const activeConversationId = useChatStore((s) => s.activeConversationId)
  const [snapshot, setSnapshot] = useState<ContextSnapshot | null>(null)

  const sessionId =
    conversations.find((c) => c.id === activeConversationId)?.sessionId ?? null

  useEffect(() => {
    let cancelled = false

    async function poll() {
      if (cancelled) return
      try {
        const data = sessionId
          ? await fetchSessionContext(sessionId)
          : await fetchContext()
        if (!cancelled) setSnapshot(data)
      } catch {
        // backend unreachable — keep showing last snapshot
      }
    }

    poll()
    const timer = sessionId !== null ? setInterval(poll, 5000) : null
    return () => {
      cancelled = true
      if (timer !== null) clearInterval(timer)
    }
  }, [sessionId])

  const hasData = snapshot !== null && snapshot.max_tokens > 0 && snapshot.total_tokens > 0
  const utilization = snapshot?.utilization ?? 0
  const isWarning = utilization > 0.8
  const isCritical = utilization > 0.95

  return (
    <div className="px-4 pt-3 pb-4 border-t border-surface-800/60">
      <p className="text-[10px] font-mono font-semibold tracking-[0.18em] text-surface-500 uppercase mb-2.5">
        Context
      </p>

      {hasData && snapshot ? (
        <>
          {/* Layered stack bar */}
          <div
            className="h-1.5 w-full rounded-sm overflow-hidden flex bg-surface-800/60 mb-2"
            role="img"
            aria-label={`Context window ${Math.round(utilization * 100)}% used`}
          >
            {snapshot.layers.map((layer) => {
              const pct = (layer.tokens / snapshot.max_tokens) * 100
              if (pct < 0.3) return null
              return (
                <div
                  key={layer.name}
                  title={`${layer.name}: ${fmtTokens(layer.tokens)}`}
                  style={{
                    width: `${pct}%`,
                    backgroundColor: layerColor(layer.name),
                    flexShrink: 0,
                    opacity: isCritical ? 1 : isWarning ? 0.9 : 0.75,
                  }}
                />
              )
            })}
            {/* Available remainder */}
            <div className="flex-1 bg-brand-accent/10" />
          </div>

          {/* Token count + percentage */}
          <div className="flex items-center justify-between mb-2">
            <span
              className={cn(
                'text-[10px] font-mono tabular-nums',
                isCritical
                  ? 'text-red-400'
                  : isWarning
                    ? 'text-amber-400'
                    : 'text-surface-700',
              )}
            >
              {fmtTokens(snapshot.total_tokens)} / {fmtTokens(snapshot.max_tokens)}
            </span>
            <span
              className={cn(
                'text-[10px] font-mono font-semibold tabular-nums',
                isCritical
                  ? 'text-red-400'
                  : isWarning
                    ? 'text-amber-400'
                    : 'text-surface-500',
              )}
            >
              {Math.round(utilization * 100)}%
            </span>
          </div>

          {/* Per-layer legend */}
          <div className="space-y-1">
            {snapshot.layers
              .filter((l) => l.tokens > 0)
              .map((layer) => (
                <div key={layer.name} className="flex items-center gap-1.5">
                  <span
                    className="w-1.5 h-1.5 rounded-sm flex-shrink-0"
                    style={{ backgroundColor: layerColor(layer.name) }}
                  />
                  <span className="text-[10px] font-mono text-surface-600 flex-1 truncate">
                    {layerShort(layer.name)}
                  </span>
                  <span className="text-[10px] font-mono text-surface-700 tabular-nums">
                    {fmtTokens(layer.tokens)}
                  </span>
                </div>
              ))}
          </div>
        </>
      ) : (
        /* No session or no data yet */
        <>
          <div className="h-1.5 w-full rounded-sm bg-surface-800/50" />
          <p className="mt-1.5 text-[9px] font-mono text-surface-700 italic">active after first message</p>
        </>
      )}
    </div>
  )
}
