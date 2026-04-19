import { useUiStore } from '@/lib/ui-store'

export function ProgressToggle() {
  const dockOpen = useUiStore((s) => s.dockOpen)
  const setDockOpen = useUiStore((s) => s.setDockOpen)
  if (dockOpen) return null
  return (
    <button
      type="button"
      aria-label="Progress"
      onClick={() => setDockOpen(true)}
      className="fade-in flex items-center gap-1.5 rounded-md border px-2.5 py-1 text-[12px]"
      style={{ borderColor: 'var(--line-2)', color: 'var(--fg-1)' }}
    >
      <span
        className="pulse h-1.5 w-1.5 flex-shrink-0 rounded-full"
        style={{ background: 'var(--acc)' }}
      />
      Progress
    </button>
  )
}
