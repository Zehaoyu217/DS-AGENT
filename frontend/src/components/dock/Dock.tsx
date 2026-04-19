import { ChevronRight } from 'lucide-react'
import {
  useUiStore,
  DOCK_W_MIN,
  DOCK_W_MAX,
  selectDockW,
  selectDockTab,
  type DockTab,
} from '@/lib/ui-store'
import { cn } from '@/lib/utils'
import { Resizer } from '@/components/shell/Resizer'
import { DockProgress } from './DockProgress'
import { DockContext } from './DockContext'
import { DockArtifacts } from './DockArtifacts'

interface TabDef {
  id: DockTab
  label: string
}

const TABS: readonly TabDef[] = [
  { id: 'progress', label: 'Progress' },
  { id: 'context', label: 'Context' },
  { id: 'artifacts', label: 'Artifacts' },
] as const

export function Dock() {
  const dockW = useUiStore(selectDockW)
  const setDockW = useUiStore((s) => s.setDockW)
  const dockTab = useUiStore(selectDockTab)
  const setDockTab = useUiStore((s) => s.setDockTab)
  const toggleDock = useUiStore((s) => s.toggleDock)

  return (
    <aside
      className="relative flex h-full flex-col border-l border-line-2 bg-bg-1"
      style={{ width: dockW, minWidth: DOCK_W_MIN, maxWidth: DOCK_W_MAX }}
      aria-label="Agent dock"
    >
      <div
        className="absolute top-0 left-0 h-full"
        style={{ transform: 'translateX(-2px)' }}
      >
        <Resizer
          axis="x"
          min={DOCK_W_MIN}
          max={DOCK_W_MAX}
          value={dockW}
          onChange={setDockW}
          invert
          ariaLabel="Resize dock"
          className="h-full"
        />
      </div>

      <div
        className="flex h-9 items-center border-b border-line-2 px-2"
        role="tablist"
        aria-label="Dock sections"
      >
        {TABS.map((tab) => {
          const on = dockTab === tab.id
          return (
            <button
              key={tab.id}
              type="button"
              role="tab"
              aria-selected={on}
              aria-controls={`dock-panel-${tab.id}`}
              onClick={() => setDockTab(tab.id)}
              className={cn(
                'relative inline-flex items-center px-3 py-2',
                'text-[11.5px] transition-colors focus-ring rounded-sm',
                on ? 'text-fg-0 font-medium' : 'text-fg-2 hover:text-fg-0',
              )}
            >
              {tab.label}
              {on && (
                <span
                  aria-hidden
                  className="pointer-events-none absolute -bottom-px left-2 right-2 h-0.5 bg-acc"
                />
              )}
            </button>
          )
        })}
        <div className="flex-1" />
        <button
          type="button"
          onClick={toggleDock}
          aria-label="Collapse dock"
          className={cn(
            'inline-flex h-6 w-6 items-center justify-center rounded',
            'text-fg-3 hover:text-fg-0 hover:bg-bg-2 focus-ring',
          )}
        >
          <ChevronRight className="h-3.5 w-3.5" aria-hidden />
        </button>
      </div>

      <div
        id={`dock-panel-${dockTab}`}
        role="tabpanel"
        aria-labelledby={`dock-tab-${dockTab}`}
        className="flex-1 min-h-0 overflow-hidden"
      >
        {dockTab === 'progress' && <DockProgress />}
        {dockTab === 'context' && <DockContext />}
        {dockTab === 'artifacts' && <DockArtifacts />}
      </div>
    </aside>
  )
}
