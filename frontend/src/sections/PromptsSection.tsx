import { useCallback, useEffect, useState } from 'react'
import { Check, Copy, FileText } from 'lucide-react'
import { listPrompts, type PromptEntry } from '@/lib/api-prompts'
import { cn } from '@/lib/utils'

const CATEGORY_LABELS: Record<PromptEntry['category'], string> = {
  system: 'SYSTEM',
  skill_injection: 'SKILL INJECTIONS',
  tool_description: 'TOOL DESCRIPTIONS',
  injector_template: 'INJECTOR TEMPLATES',
}

const CATEGORY_ORDER: PromptEntry['category'][] = [
  'system',
  'skill_injection',
  'tool_description',
  'injector_template',
]

function formatTokens(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M tok`
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}k tok`
  return `${n} tok`
}

interface LayerBadgeProps {
  layer: PromptEntry['layer']
}

function LayerBadge({ layer }: LayerBadgeProps) {
  return (
    <span
      className={cn(
        'text-[10px] font-mono font-semibold uppercase tracking-wider px-1.5 py-0.5 rounded border flex-shrink-0',
        layer === 'L1'
          ? 'bg-brand-950/40 text-brand-400 border-brand-900/60'
          : layer === 'L2'
            ? 'bg-emerald-950/40 text-emerald-400 border-emerald-900/60'
            : 'bg-surface-800/60 text-surface-500 border-surface-700/60',
      )}
    >
      {layer}
    </span>
  )
}

interface PromptListItemProps {
  entry: PromptEntry
  isSelected: boolean
  onSelect: (id: string) => void
}

function PromptListItem({ entry, isSelected, onSelect }: PromptListItemProps) {
  return (
    <button
      type="button"
      onClick={() => onSelect(entry.id)}
      className={cn(
        'w-full flex flex-col gap-0.5 px-3 py-2 text-left transition-colors',
        'focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-brand-500',
        isSelected
          ? 'bg-brand-950/30 border-l-2 border-brand-500 pl-2.5'
          : 'hover:bg-surface-800/50 border-l-2 border-transparent',
      )}
      aria-selected={isSelected}
    >
      <div className="flex items-center gap-2 min-w-0">
        <span className="flex-1 min-w-0 font-mono text-xs text-surface-300 truncate">
          {entry.label}
        </span>
        <LayerBadge layer={entry.layer} />
      </div>
      {entry.description && (
        <p className="text-[10px] text-surface-600 truncate leading-relaxed">
          {entry.description}
        </p>
      )}
    </button>
  )
}

interface PromptDetailPanelProps {
  entry: PromptEntry
}

function PromptDetailPanel({ entry }: PromptDetailPanelProps) {
  const [copied, setCopied] = useState(false)

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(entry.text)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch {
      // clipboard not available
    }
  }

  return (
    <div className="flex flex-col h-full min-h-0">
      {/* Header */}
      <div className="px-6 py-4 border-b border-surface-800 flex-shrink-0">
        <div className="flex items-center gap-2 flex-wrap">
          <h2 className="font-mono text-sm font-semibold text-surface-100">{entry.label}</h2>
          <LayerBadge layer={entry.layer} />
          {entry.compactable && (
            <span className="text-[10px] font-mono text-surface-600 bg-surface-800 px-1.5 py-0.5 rounded border border-surface-700">
              compactable
            </span>
          )}
          <span className="text-[10px] font-mono text-surface-600 bg-surface-800 px-1.5 py-0.5 rounded border border-surface-700">
            ~{formatTokens(entry.approx_tokens)}
          </span>
        </div>
        {entry.description && (
          <p className="mt-2 text-xs text-surface-400 leading-relaxed">{entry.description}</p>
        )}
      </div>

      {/* Prompt text */}
      <div className="flex-1 min-h-0 flex flex-col relative">
        {/* Copy button */}
        <div className="absolute top-3 right-4 z-10">
          <button
            type="button"
            onClick={() => void handleCopy()}
            title={copied ? 'Copied!' : 'Copy prompt'}
            aria-label={copied ? 'Copied' : 'Copy prompt'}
            className={cn(
              'flex items-center gap-1.5 px-2 py-1 rounded text-[10px] font-mono transition-colors',
              'border border-surface-700 bg-surface-900',
              copied
                ? 'text-green-400 border-green-900/60'
                : 'text-surface-500 hover:text-surface-300 hover:border-surface-600',
            )}
          >
            {copied ? (
              <>
                <Check className="w-3 h-3" />
                COPIED
              </>
            ) : (
              <>
                <Copy className="w-3 h-3" />
                COPY
              </>
            )}
          </button>
        </div>

        {/* Scrollable text area */}
        <div className="flex-1 min-h-0 overflow-y-auto p-4 pt-12">
          <pre
            className={cn(
              'font-mono text-xs text-surface-300 whitespace-pre-wrap break-words leading-relaxed',
              'bg-surface-900/40 rounded-md p-4 border border-surface-800',
            )}
          >
            {entry.text}
          </pre>
        </div>
      </div>
    </div>
  )
}

function PromptDetailEmpty() {
  return (
    <div className="flex-1 flex items-center justify-center">
      <div className="text-center space-y-1">
        <p className="text-xs font-mono text-surface-600 uppercase tracking-widest">
          Select a prompt
        </p>
        <p className="text-[11px] text-surface-700">
          Click any entry to view its full content
        </p>
      </div>
    </div>
  )
}

export function PromptsSection() {
  const [entries, setEntries] = useState<PromptEntry[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedId, setSelectedId] = useState<string | null>(null)

  const fetchEntries = useCallback(async () => {
    try {
      const data = await listPrompts()
      setEntries(data)
      setError(null)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load prompts'
      setError(message)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    void fetchEntries()
  }, [fetchEntries])

  const selectedEntry = entries.find((e) => e.id === selectedId) ?? null

  // Group by category, in defined order
  const grouped = new Map<PromptEntry['category'], PromptEntry[]>()
  for (const entry of entries) {
    const existing = grouped.get(entry.category)
    if (existing) {
      existing.push(entry)
    } else {
      grouped.set(entry.category, [entry])
    }
  }

  const orderedCategories = CATEGORY_ORDER.filter((cat) => grouped.has(cat))

  return (
    <div className="flex flex-col h-full bg-surface-950 text-surface-100 overflow-hidden">
      {/* Header */}
      <header className="flex items-center gap-3 px-6 py-4 border-b border-surface-800 flex-shrink-0">
        <FileText className="w-4 h-4 text-surface-500" aria-hidden />
        <h1 className="font-mono text-xs font-semibold text-surface-300 uppercase tracking-widest">
          PROMPTS
        </h1>
        <span className="text-[10px] font-mono text-surface-600">
          {entries.length > 0 ? `${entries.length} entries` : ''}
        </span>
      </header>

      {/* Two-column layout */}
      <div className="flex flex-1 min-h-0 overflow-hidden">
        {/* Left: categorized list */}
        <aside
          className="w-[260px] flex-shrink-0 flex flex-col border-r border-surface-800 overflow-hidden"
          aria-label="Prompt list"
        >
          <div className="flex-1 min-h-0 overflow-y-auto" role="listbox" aria-label="Prompts by category">
            {loading && (
              <p className="px-3 py-6 text-xs text-surface-500 text-center">Loading prompts…</p>
            )}

            {error && (
              <div
                role="alert"
                className="mx-2 my-2 rounded border border-red-900/60 bg-red-950/40 px-2 py-1.5 text-[11px] font-mono text-red-300"
              >
                {error}
              </div>
            )}

            {!loading && !error && entries.length === 0 && (
              <p className="px-3 py-6 text-xs text-surface-500 text-center">No prompts found.</p>
            )}

            {orderedCategories.map((category) => {
              const categoryEntries = grouped.get(category) ?? []
              const label = CATEGORY_LABELS[category]

              return (
                <div key={category} role="group" aria-label={label}>
                  {/* Section header */}
                  <div className="px-3 py-1.5 flex items-center gap-2 border-b border-surface-800/60 bg-surface-900/40">
                    <span className="text-[10px] font-mono font-semibold text-surface-600 uppercase tracking-widest">
                      {label}
                    </span>
                    <span className="text-[10px] font-mono text-surface-700">
                      {categoryEntries.length}
                    </span>
                  </div>

                  <div className="py-0.5">
                    {categoryEntries.map((entry) => (
                      <PromptListItem
                        key={entry.id}
                        entry={entry}
                        isSelected={selectedId === entry.id}
                        onSelect={setSelectedId}
                      />
                    ))}
                  </div>
                </div>
              )
            })}
          </div>
        </aside>

        {/* Right: detail panel */}
        <main className="flex-1 min-w-0 flex flex-col overflow-hidden">
          {selectedEntry ? (
            <PromptDetailPanel entry={selectedEntry} />
          ) : (
            <PromptDetailEmpty />
          )}
        </main>
      </div>
    </div>
  )
}
