/**
 * TweaksPanel — runtime UI knobs (theme, accent, density, dock, msg style,
 * think mode, font, rail, agent run/pause). Opens as a Radix Dialog anchored
 * to the bottom-left, near the IconRail gear that triggers it.
 */
import * as Dialog from '@radix-ui/react-dialog'
import { useTheme } from '@/components/layout/ThemeProvider'
import {
  useUiStore,
  selectAccent,
  selectDensity,
  selectDockPosition,
  selectMsgStyle,
  selectThinkMode,
  selectUiFont,
  selectRailMode,
  selectAgentRunning,
} from '@/lib/ui-store'
import { Seg2 } from './Seg2'
import { TweakRow } from './TweakRow'
import { AccentSwatches } from './AccentSwatches'

const THEME_OPTS = [
  { value: 'dark' as const, label: 'Dark' },
  { value: 'light' as const, label: 'Light' },
]
const DENSITY_OPTS = [
  { value: 'compact' as const, label: 'Compact' },
  { value: 'default' as const, label: 'Default' },
]
const DOCK_OPTS = [
  { value: 'right' as const, label: 'Right' },
  { value: 'bottom' as const, label: 'Bottom' },
  { value: 'off' as const, label: 'Off' },
]
const MSG_OPTS = [
  { value: 'flat' as const, label: 'Flat' },
  { value: 'bordered' as const, label: 'Bordered' },
]
const THINK_OPTS = [
  { value: 'tab' as const, label: 'Tab' },
  { value: 'inline' as const, label: 'Inline' },
]
const FONT_OPTS = [
  { value: 'mono' as const, label: 'Mono' },
  { value: 'sans' as const, label: 'Sans' },
]
const RAIL_OPTS = [
  { value: 'icon' as const, label: 'Icons' },
  { value: 'expand' as const, label: 'Labels' },
]
const AGENT_OPTS = [
  { value: 'running' as const, label: 'Run' },
  { value: 'paused' as const, label: 'Pause' },
]

export function TweaksPanel() {
  const open = useUiStore((s) => s.tweaksOpen)
  const setOpen = useUiStore((s) => s.setTweaksOpen)

  const { theme, setTheme } = useTheme()
  const accent = useUiStore(selectAccent)
  const setAccent = useUiStore((s) => s.setAccent)
  const density = useUiStore(selectDensity)
  const setDensity = useUiStore((s) => s.setDensity)
  const dockPosition = useUiStore(selectDockPosition)
  const setDockPosition = useUiStore((s) => s.setDockPosition)
  const msgStyle = useUiStore(selectMsgStyle)
  const setMsgStyle = useUiStore((s) => s.setMsgStyle)
  const thinkMode = useUiStore(selectThinkMode)
  const setThinkMode = useUiStore((s) => s.setThinkMode)
  const uiFont = useUiStore(selectUiFont)
  const setUiFont = useUiStore((s) => s.setUiFont)
  const railMode = useUiStore(selectRailMode)
  const setRailMode = useUiStore((s) => s.setRailMode)
  const agentRunning = useUiStore(selectAgentRunning)
  const setAgentRunning = useUiStore((s) => s.setAgentRunning)

  const themeValue = theme === 'system' ? 'dark' : theme

  return (
    <Dialog.Root open={open} onOpenChange={setOpen}>
      <Dialog.Portal>
        <Dialog.Overlay
          className="fixed inset-0 z-40 bg-black/40 backdrop-blur-[2px] data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0"
        />
        <Dialog.Content
          aria-label="Tweaks"
          className="fixed bottom-4 left-[64px] z-50 w-[280px] rounded-[12px] p-3 shadow-2xl data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:slide-out-to-left-2 data-[state=open]:slide-in-from-left-2"
          style={{
            background: 'var(--bg-1)',
            border: '1px solid var(--line)',
          }}
        >
          <Dialog.Title className="font-mono text-[11px] uppercase tracking-wider mb-2" style={{ color: 'var(--fg-2)' }}>
            Tweaks
          </Dialog.Title>
          <Dialog.Description className="sr-only">
            Adjust runtime UI preferences: theme, density, accent color, dock position, and more.
          </Dialog.Description>
          <div className="flex flex-col">
            <TweakRow label="Theme">
              <Seg2
                ariaLabel="Theme"
                options={THEME_OPTS}
                value={themeValue as 'light' | 'dark'}
                onChange={(v) => setTheme(v)}
              />
            </TweakRow>
            <TweakRow label="Accent">
              <AccentSwatches value={accent} onChange={setAccent} />
            </TweakRow>
            <TweakRow label="Density">
              <Seg2 ariaLabel="Density" options={DENSITY_OPTS} value={density === 'cozy' ? 'default' : density} onChange={setDensity} />
            </TweakRow>
            <TweakRow label="Dock">
              <Seg2 ariaLabel="Dock position" options={DOCK_OPTS} value={dockPosition} onChange={setDockPosition} />
            </TweakRow>
            <TweakRow label="Msg style">
              <Seg2 ariaLabel="Message style" options={MSG_OPTS} value={msgStyle} onChange={setMsgStyle} />
            </TweakRow>
            <TweakRow label="Think">
              <Seg2 ariaLabel="Thinking display" options={THINK_OPTS} value={thinkMode} onChange={setThinkMode} />
            </TweakRow>
            <TweakRow label="Font">
              <Seg2 ariaLabel="UI font" options={FONT_OPTS} value={uiFont} onChange={setUiFont} />
            </TweakRow>
            <TweakRow label="Rail">
              <Seg2 ariaLabel="Icon rail mode" options={RAIL_OPTS} value={railMode} onChange={setRailMode} />
            </TweakRow>
            <TweakRow label="Agent">
              <Seg2
                ariaLabel="Agent state"
                options={AGENT_OPTS}
                value={agentRunning ? 'running' : 'paused'}
                onChange={(v) => setAgentRunning(v === 'running')}
              />
            </TweakRow>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  )
}
