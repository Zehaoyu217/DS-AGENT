import React, { useState } from 'react'
import { ChevronDown, ChevronRight, Bot, CheckCircle, XCircle, Clock } from 'lucide-react'
import type { A2aContent } from '@/lib/types'
import { cn } from '@/lib/utils'

interface SubagentCardProps {
  entry: A2aContent
}

function StatusIcon({ status }: { status: A2aContent['status'] }) {
  if (status === 'complete') return <CheckCircle className="w-3.5 h-3.5 text-success" />
  if (status === 'error') return <XCircle className="w-3.5 h-3.5 text-error" />
  return <Clock className="w-3.5 h-3.5 text-surface-400 animate-pulse" />
}

export function SubagentCard({ entry }: SubagentCardProps): React.ReactElement {
  const [expanded, setExpanded] = useState(false)

  return (
    <div
      className={cn(
        'rounded border text-sm',
        entry.status === 'error'
          ? 'border-error/30 bg-error-bg'
          : 'border-surface-700/60 bg-surface-850/60',
      )}
    >
      <button
        type="button"
        onClick={() => setExpanded((v) => !v)}
        className="flex items-center gap-2 w-full px-3 py-2 text-left"
        aria-expanded={expanded}
      >
        <Bot className="w-3.5 h-3.5 text-brand-400 flex-shrink-0" aria-hidden />
        <span className="text-[11px] font-mono font-semibold text-surface-500 uppercase tracking-wider flex-shrink-0">
          Sub-agent
        </span>
        <span className="flex-1 min-w-0 text-xs text-surface-300 truncate">
          {entry.task || '(delegated task)'}
        </span>
        <StatusIcon status={entry.status} />
        {expanded ? (
          <ChevronDown className="w-3.5 h-3.5 text-surface-500 flex-shrink-0" aria-hidden />
        ) : (
          <ChevronRight className="w-3.5 h-3.5 text-surface-500 flex-shrink-0" aria-hidden />
        )}
      </button>

      {expanded && (
        <div className="border-t border-surface-700/50 px-3 pb-3 pt-2 space-y-2">
          {entry.summary ? (
            <p className="text-xs text-surface-300 leading-relaxed">{entry.summary}</p>
          ) : entry.status === 'pending' ? (
            <p className="text-xs text-surface-500 italic animate-pulse">Running…</p>
          ) : null}

          {entry.artifactId && (
            <p className="text-[10px] font-mono text-surface-600">
              artifact: {entry.artifactId}
            </p>
          )}
        </div>
      )}
    </div>
  )
}
