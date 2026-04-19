import { TrendingUp, Table2, FileText, Workflow, FileBarChart, File } from 'lucide-react'
import type { Artifact } from '@/lib/store'
import { cn } from '@/lib/utils'

const ICONS: Record<Artifact['format'], typeof TrendingUp> = {
  'vega-lite': TrendingUp,
  'table-json': Table2,
  mermaid: Workflow,
  csv: FileBarChart,
  html: FileText,
  text: File,
}

interface ArtifactTileProps {
  artifact: Artifact
  view?: 'grid' | 'list'
}

function focus(id: string) {
  window.dispatchEvent(new CustomEvent('focusArtifact', { detail: { id } }))
}

export function ArtifactTile({ artifact, view = 'grid' }: ArtifactTileProps) {
  const Icon = ICONS[artifact.format] ?? File
  return (
    <button
      type="button"
      onClick={() => focus(artifact.id)}
      className={cn(
        'group relative flex rounded border border-line-2 bg-bg-1 text-left focus-ring',
        'hover:border-acc hover:shadow-sm',
        view === 'grid' ? 'aspect-square flex-col p-2' : 'h-10 items-center gap-2 px-2',
      )}
      aria-label={`Open artifact ${artifact.title}`}
    >
      <div className={cn('flex items-center gap-1', view === 'grid' ? '' : 'flex-1')}>
        <Icon className="h-3 w-3 text-fg-2" aria-hidden />
        <span className="mono text-[9.5px] uppercase text-fg-3">{artifact.type}</span>
      </div>
      <span
        className={cn(
          'truncate text-[12px] text-fg-0',
          view === 'grid' ? 'mt-auto' : 'flex-1',
        )}
        title={artifact.title}
      >
        {artifact.title}
      </span>
    </button>
  )
}
