import { Database, X } from 'lucide-react'
import { useChatStore } from '@/lib/store'

interface AttachedFilesPreviewProps {
  conversationId: string
}

function formatRows(n: number): string {
  if (n < 1_000) return `${n} rows`
  if (n < 1_000_000) return `${(n / 1_000).toFixed(n < 10_000 ? 1 : 0)}K rows`
  return `${(n / 1_000_000).toFixed(1)}M rows`
}

export function AttachedFilesPreview({ conversationId }: AttachedFilesPreviewProps) {
  const datasets = useChatStore(
    (s) => s.conversations.find((c) => c.id === conversationId)?.datasets,
  )
  const deleteDataset = useChatStore((s) => s.deleteDataset)
  if (!datasets || datasets.length === 0) return null

  return (
    <div className="mb-2 flex flex-wrap gap-1.5">
      {datasets.map((d) => (
        <span
          key={d.tableName}
          className="inline-flex items-center gap-1.5 rounded-md border px-2 py-0.5 text-[11.5px]"
          style={{
            borderColor: 'var(--line-2)',
            background: 'var(--bg-2)',
            color: 'var(--fg-1)',
          }}
          title={`${d.filename} — ${d.columns.length} cols, ${d.rowCount.toLocaleString()} rows`}
        >
          <Database size={11} style={{ color: 'var(--acc)' }} />
          <span className="mono">user_data.{d.tableName}</span>
          <span style={{ color: 'var(--fg-3)' }}>· {formatRows(d.rowCount)}</span>
          <button
            type="button"
            aria-label={`remove ${d.tableName}`}
            onClick={() => {
              if (window.confirm(`Remove dataset "${d.tableName}"?`)) {
                deleteDataset(conversationId, d.tableName).catch((err) => {
                  window.alert(
                    `Failed to delete: ${err instanceof Error ? err.message : String(err)}`,
                  )
                })
              }
            }}
            className="ml-0.5 flex h-3 w-3 items-center justify-center rounded-[2px]"
            style={{ color: 'var(--fg-3)' }}
          >
            <X size={9} />
          </button>
        </span>
      ))}
    </div>
  )
}
