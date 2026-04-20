import { Network } from 'lucide-react'
import { SurfacePage } from '@/components/surface/SurfacePage'
import { DrawerSlot } from '@/components/surface/DrawerSlot'
import { WikiTree } from '@/components/wiki/WikiTree'
import { WikiArticle } from '@/components/wiki/WikiArticle'
import { GraphPanel } from '@/components/graph/GraphPanel'
import { IngestPanel } from '@/components/ingest/IngestPanel'
import { DigestPanel } from '@/components/digest/DigestPanel'
import { PipelineBar } from '@/components/pipeline/PipelineBar'
import { useSurfacesStore } from '@/lib/surfaces-store'
import { cn } from '@/lib/utils'

export function KnowledgeSurface() {
  const drawer = useSurfacesStore((s) => s.knowledgeDrawer)
  const setDrawer = useSurfacesStore((s) => s.setKnowledgeDrawer)
  const selected = useSurfacesStore((s) => s.selectedWikiPath)
  const setSelected = useSurfacesStore((s) => s.setSelectedWikiPath)
  const closeDrawer = () => setDrawer(null)

  const toolbar = (
    <ToolbarButton
      active={drawer === 'graph'}
      onClick={() => setDrawer(drawer === 'graph' ? null : 'graph')}
      icon={<Network size={13} aria-hidden />}
      label="Graph"
    />
  )

  const drawerContent =
    drawer === 'ingest' ? (
      <DrawerSlot eyebrow="KNOWLEDGE" title="Ingest" onClose={closeDrawer}>
        <IngestPanel open onClose={closeDrawer} embedded />
      </DrawerSlot>
    ) : drawer === 'digest' ? (
      <DrawerSlot eyebrow="KNOWLEDGE" title="Digest" onClose={closeDrawer}>
        <DigestPanel open onClose={closeDrawer} embedded />
      </DrawerSlot>
    ) : drawer === 'graph' ? (
      <DrawerSlot eyebrow="KNOWLEDGE" title="Second-Brain Graph" onClose={closeDrawer}>
        <GraphPanel open onClose={closeDrawer} embedded />
      </DrawerSlot>
    ) : undefined

  return (
    <SurfacePage
      eyebrow="WIKI"
      title="Knowledge"
      toolbar={toolbar}
      drawer={drawerContent}
      drawerOpen={drawer !== null}
      bodyClassName="!overflow-hidden"
    >
      <div className="flex h-full flex-col overflow-hidden">
        <div className="grid flex-1 grid-cols-[260px_1fr] overflow-hidden">
          <div className="overflow-hidden border-r border-line">
            <WikiTree selectedPath={selected} onSelect={setSelected} />
          </div>
          <div className="overflow-hidden">
            <WikiArticle path={selected} onNavigate={setSelected} />
          </div>
        </div>
        <PipelineBar
          onOpenIngest={() => setDrawer('ingest')}
          onDigestComplete={(entries) => {
            if (entries > 0) setDrawer('digest')
          }}
        />
      </div>
    </SurfacePage>
  )
}

interface ToolbarButtonProps {
  active: boolean
  onClick: () => void
  icon: React.ReactNode
  label: string
}

function ToolbarButton({ active, onClick, icon, label }: ToolbarButtonProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={active}
      className={cn(
        'flex h-8 items-center gap-1.5 rounded-md border px-2.5 text-[12px]',
        'transition-colors focus-ring',
        active
          ? 'border-acc-line bg-acc-dim text-acc'
          : 'border-line bg-bg-1 text-fg-1 hover:bg-bg-2 hover:text-fg-0',
      )}
    >
      {icon}
      <span>{label}</span>
    </button>
  )
}
