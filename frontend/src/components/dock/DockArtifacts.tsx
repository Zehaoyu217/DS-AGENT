import { LayoutGrid, List } from 'lucide-react'
import { useChatStore } from '@/lib/store'
import { useUiStore, selectArtifactView } from '@/lib/ui-store'
import { ArtifactTile } from './artifacts/ArtifactTile'
import { cn } from '@/lib/utils'

export function DockArtifacts() {
  const artifacts = useChatStore((s) => s.artifacts)
  const view = useUiStore(selectArtifactView)
  const setView = useUiStore((s) => s.setArtifactView)

  if (artifacts.length === 0) {
    return (
      <div className="flex h-full flex-col gap-2 p-4">
        <div className="label-cap">Artifacts</div>
        <div className="stripe-ph h-40">No artifacts yet</div>
        <div className="mono text-[10.5px] text-fg-3">They appear here as the agent produces them.</div>
      </div>
    )
  }

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b border-line-2 px-3 py-2">
        <div className="label-cap">{artifacts.length} artifacts</div>
        <div className="flex gap-1">
          <button
            type="button"
            onClick={() => setView('grid')}
            aria-label="Grid view"
            aria-pressed={view === 'grid'}
            className={cn(
              'inline-flex h-5 w-5 items-center justify-center rounded focus-ring',
              view === 'grid' ? 'bg-bg-2 text-fg-0' : 'text-fg-3 hover:text-fg-0',
            )}
          >
            <LayoutGrid className="h-3 w-3" aria-hidden />
          </button>
          <button
            type="button"
            onClick={() => setView('list')}
            aria-label="List view"
            aria-pressed={view === 'list'}
            className={cn(
              'inline-flex h-5 w-5 items-center justify-center rounded focus-ring',
              view === 'list' ? 'bg-bg-2 text-fg-0' : 'text-fg-3 hover:text-fg-0',
            )}
          >
            <List className="h-3 w-3" aria-hidden />
          </button>
        </div>
      </div>
      <div className={cn('flex-1 overflow-y-auto p-2', view === 'grid' ? 'grid grid-cols-2 gap-2' : 'flex flex-col gap-1')}>
        {artifacts.map((a) => (
          <ArtifactTile key={a.id} artifact={a} view={view} />
        ))}
      </div>
    </div>
  )
}
