import { useEffect } from 'react'
import { X } from 'lucide-react'
import { useSurfacesStore, type SettingsSection } from '@/lib/surfaces-store'
import { SearchBar } from '@/components/surface/SearchBar'
import { cn } from '@/lib/utils'

interface SectionDef {
  id: SettingsSection
  label: string
  hint: string
}

const SECTIONS: SectionDef[] = [
  { id: 'models', label: 'Models', hint: 'OpenRouter / local models' },
  { id: 'sandbox', label: 'Sandbox', hint: 'Python execution env' },
  { id: 'memory', label: 'Memory', hint: 'Working + durable stores' },
  { id: 'ingest', label: 'Ingest', hint: 'Sources, schedule, auto-dream' },
  { id: 'integrity', label: 'Integrity', hint: 'Lint / health pipeline' },
  { id: 'theme', label: 'Theme', hint: 'Light / dark / accent' },
  { id: 'hotkeys', label: 'Hotkeys', hint: 'Keyboard shortcuts' },
  { id: 'hooks', label: 'Hooks', hint: 'Pre / post tool hooks' },
]

export function SettingsOverlay() {
  const open = useSurfacesStore((s) => s.settingsOverlayOpen)
  const close = useSurfacesStore((s) => s.closeSettings)
  const active = useSurfacesStore((s) => s.settingsActiveSection)
  const setActive = useSurfacesStore((s) => s.setSettingsActiveSection)
  const search = useSurfacesStore((s) => s.settingsSearch)
  const setSearch = useSurfacesStore((s) => s.setSettingsSearch)

  useEffect(() => {
    if (!open) return
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        e.preventDefault()
        close()
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [open, close])

  if (!open) return null

  const filtered = search
    ? SECTIONS.filter((s) =>
        `${s.label} ${s.hint}`.toLowerCase().includes(search.toLowerCase()),
      )
    : SECTIONS

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label="Settings"
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-6"
      onClick={close}
    >
      <div
        className={cn(
          'flex h-[640px] w-[960px] max-w-full flex-col overflow-hidden',
          'rounded-lg border border-line bg-bg-0 shadow-ds-2',
        )}
        onClick={(e) => e.stopPropagation()}
      >
        <header className="flex h-12 items-center justify-between border-b border-line px-4">
          <span
            className="mono uppercase tracking-[0.06em] text-fg-2"
            style={{ fontSize: 11 }}
          >
            Settings
          </span>
          <button
            type="button"
            aria-label="Close settings"
            onClick={close}
            className="flex h-7 w-7 items-center justify-center rounded-md text-fg-2 hover:bg-bg-2 hover:text-fg-0 focus-ring"
          >
            <X size={14} aria-hidden />
          </button>
        </header>
        <div className="grid flex-1 grid-cols-[220px_1fr] overflow-hidden">
          <nav
            aria-label="Settings sections"
            className="flex flex-col gap-1 overflow-auto border-r border-line bg-bg-1 p-2"
          >
            <SearchBar
              value={search}
              onChange={setSearch}
              placeholder="Search settings…"
              ariaLabel="Search settings"
              className="mb-2"
            />
            {filtered.map((s) => (
              <button
                key={s.id}
                type="button"
                onClick={() => setActive(s.id)}
                className={cn(
                  'flex flex-col items-start rounded-md px-2 py-1.5 text-left',
                  'transition-colors focus-ring',
                  active === s.id
                    ? 'bg-acc-dim text-acc'
                    : 'text-fg-1 hover:bg-bg-2 hover:text-fg-0',
                )}
              >
                <span className="text-[13px] font-medium">{s.label}</span>
                <span className="text-[11px] text-fg-3">{s.hint}</span>
              </button>
            ))}
          </nav>
          <section className="overflow-auto p-6">
            <SettingsPanel section={active} />
          </section>
        </div>
      </div>
    </div>
  )
}

function SettingsPanel({ section }: { section: SettingsSection }) {
  const meta = SECTIONS.find((s) => s.id === section)
  return (
    <div className="flex flex-col gap-3">
      <div className="flex flex-col leading-tight">
        <span
          className="mono uppercase tracking-[0.06em] text-fg-3"
          style={{ fontSize: 10.5 }}
        >
          {section}
        </span>
        <h2 className="text-[18px] font-semibold text-fg-0">{meta?.label}</h2>
        <p className="text-[13px] text-fg-2">{meta?.hint}</p>
      </div>
      <div
        className={cn(
          'rounded-md border border-dashed border-line bg-bg-1 p-6',
          'text-[13px] text-fg-3',
        )}
      >
        Settings for <span className="text-fg-1">{meta?.label}</span> will land
        in a follow-up. The shell, search, and section navigation are wired.
      </div>
    </div>
  )
}
