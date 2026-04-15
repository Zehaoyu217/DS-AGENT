import { useState } from 'react'
import { BarChart2, Table2, GitGraph, FileText, Check, Copy } from 'lucide-react'
import { useChatStore } from '@/lib/store'
import { VegaChart } from '@/components/chat/VegaChart'
import { MermaidDiagram } from '@/components/chat/MermaidDiagram'
import { DataTable } from './DataTable'
import type { Artifact } from '@/lib/store'

const TYPE_ICON: Record<string, React.ComponentType<{ className?: string }>> = {
  chart: BarChart2,
  table: Table2,
  diagram: GitGraph,
}

const FORMAT_BADGE: Record<string, string> = {
  'vega-lite': 'vega-lite',
  'mermaid': 'mermaid',
  'table-json': 'table',
  'html': 'html',
}

function ArtifactCard({ artifact }: { artifact: Artifact }) {
  const [expanded, setExpanded] = useState(true)
  const [copied, setCopied] = useState(false)

  const Icon = TYPE_ICON[artifact.type] ?? FileText

  const handleCopySpec = async () => {
    try {
      await navigator.clipboard.writeText(artifact.content)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch {
      // clipboard unavailable
    }
  }

  return (
    <div className="rounded border border-surface-700/50 bg-surface-900/50 overflow-hidden">
      {/* Header */}
      <div className="flex items-center gap-2 px-2.5 py-1.5 border-b border-surface-700/50">
        <button
          onClick={() => setExpanded(!expanded)}
          className="flex-1 flex items-center gap-2 min-w-0"
        >
          <Icon className="w-3.5 h-3.5 text-brand-400 shrink-0" aria-hidden />
          <span className="text-[11px] font-mono font-medium text-surface-300 truncate text-left">
            {artifact.title || `${artifact.type} ${artifact.id}`}
          </span>
          <span className="text-[9px] font-mono uppercase tracking-widest text-surface-600 shrink-0 px-1.5 py-0.5 rounded bg-surface-800">
            {FORMAT_BADGE[artifact.format] ?? artifact.format}
          </span>
        </button>

        {/* Copy spec button for charts */}
        {(artifact.format === 'vega-lite' || artifact.format === 'table-json') && (
          <button
            onClick={handleCopySpec}
            aria-label={copied ? 'Copied' : 'Copy spec'}
            className="p-1 rounded text-surface-600 hover:text-surface-300 hover:bg-surface-800 transition-colors shrink-0"
          >
            {copied ? (
              <Check className="w-3 h-3 text-green-400" />
            ) : (
              <Copy className="w-3 h-3" />
            )}
          </button>
        )}
      </div>

      {/* Content */}
      {expanded && (
        <div className="p-2.5">
          {artifact.format === 'vega-lite' ? (
            <VegaChart spec={artifact.content} />
          ) : artifact.format === 'mermaid' ? (
            <MermaidDiagram code={artifact.content} />
          ) : artifact.format === 'table-json' ? (
            <DataTable content={artifact.content} />
          ) : (
            <div
              className="text-xs text-surface-400 overflow-auto max-h-64"
              dangerouslySetInnerHTML={{ __html: artifact.content }}
            />
          )}
        </div>
      )}
    </div>
  )
}

export function ArtifactsPanel(): React.ReactElement {
  const artifacts = useChatStore((s) => s.artifacts)
  const activeId = useChatStore((s) => s.activeConversationId)
  const conversation = useChatStore((s) =>
    s.conversations.find((c) => c.id === activeId),
  )

  // Filter artifacts by current conversation's session_id, fall back to all if no session yet
  const sessionId = conversation?.sessionId
  const filtered = sessionId
    ? artifacts.filter((a) => a.session_id === sessionId || a.session_id === '')
    : artifacts

  return (
    <div className="flex flex-col flex-1 min-h-0 p-3">
      <p className="text-[10px] font-mono font-semibold tracking-widest text-surface-500 uppercase mb-2">
        Artifacts
      </p>
      <div className="border-t border-surface-700/50 mb-3" />

      {filtered.length === 0 ? (
        <div>
          <p className="text-[10px] font-mono text-surface-600 italic">no artifacts yet</p>
          <p className="text-[9px] font-mono text-surface-700 italic mt-1 leading-relaxed">
            charts, tables, and diagrams appear here as the agent generates them
          </p>
        </div>
      ) : (
        <div className="flex flex-col gap-3 overflow-y-auto flex-1 min-h-0">
          {filtered.map((artifact) => (
            <ArtifactCard key={artifact.id} artifact={artifact} />
          ))}
        </div>
      )}
    </div>
  )
}
