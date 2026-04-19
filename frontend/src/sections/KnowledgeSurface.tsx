import { Download, Upload } from 'lucide-react'
import { SurfacePage } from '@/components/surface/SurfacePage'
import { DrawerSlot } from '@/components/surface/DrawerSlot'
import { GraphPanel } from '@/components/graph/GraphPanel'
import { IngestPanel } from '@/components/ingest/IngestPanel'
import { DigestPanel } from '@/components/digest/DigestPanel'
import { useSurfacesStore } from '@/lib/surfaces-store'
import { cn } from '@/lib/utils'

export function KnowledgeSurface() {
  const drawer = useSurfacesStore((s) => s.knowledgeDrawer)
  const setDrawer = useSurfacesStore((s) => s.setKnowledgeDrawer)
  const closeDrawer = () => setDrawer(null)

  const toolbar = (
    <>
      <ToolbarButton
        active={drawer === 'ingest'}
        onClick={() => setDrawer(drawer === 'ingest' ? null : 'ingest')}
        icon={<Upload size={13} aria-hidden />}
        label="Ingest"
      />
      <ToolbarButton
        active={drawer === 'digest'}
        onClick={() => setDrawer(drawer === 'digest' ? null : 'digest')}
        icon={<Download size={13} aria-hidden />}
        label="Digest"
      />
    </>
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
    ) : undefined

  return (
    <SurfacePage
      eyebrow="WIKI"
      title="Knowledge"
      toolbar={toolbar}
      drawer={drawerContent}
      drawerOpen={drawer !== null}
    >
      <GraphPanel open onClose={closeDrawer} embedded />
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
