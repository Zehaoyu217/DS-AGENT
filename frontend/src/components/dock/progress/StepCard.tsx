import { useUiStore, selectProgressExpanded, selectTraceTab } from '@/lib/ui-store'
import type { ProgressStep } from '@/lib/selectors/progressSteps'
import { StatusDot } from './StatusDot'
import { cn } from '@/lib/utils'
import { TimelineMode } from './modes/TimelineMode'
import { ContextMode } from './modes/ContextMode'
import { RawMode } from './modes/RawMode'

interface StepCardProps {
  step: ProgressStep
}

function elapsedLabel(step: ProgressStep): string {
  if (!step.startedAt) return ''
  const end = step.finishedAt ?? Date.now()
  const ms = Math.max(0, end - step.startedAt)
  return ms < 1_000 ? `${ms} ms` : `${(ms / 1_000).toFixed(1)} s`
}

export function StepCard({ step }: StepCardProps) {
  const expanded = useUiStore(selectProgressExpanded)
  const isOpen = expanded.includes(step.id)
  const toggle = useUiStore((s) => s.toggleProgressExpanded)
  const traceTab = useUiStore(selectTraceTab)
  const setTraceTab = useUiStore((s) => s.setTraceTab)

  return (
    <div className="border-b border-line-2 px-3 py-2">
      <button
        type="button"
        onClick={() => toggle(step.id)}
        className={cn(
          'flex w-full items-center gap-2 text-left focus-ring rounded',
          'hover:bg-bg-2',
        )}
        aria-expanded={isOpen}
        aria-label={`Step ${step.index}: ${step.title}`}
      >
        <StatusDot status={step.status} />
        <span className="flex-1 truncate text-[13px] text-fg-0">{step.title}</span>
        <span className="mono text-[11px] text-fg-3">{elapsedLabel(step)}</span>
      </button>
      {isOpen && (
        <div className="mt-2 border-t border-line-2 pt-2">
          <div className="mb-2 flex gap-1">
            {(['timeline', 'context', 'raw'] as const).map((t) => (
              <button
                key={t}
                type="button"
                onClick={() => setTraceTab(t)}
                data-active={traceTab === t}
                className={cn(
                  'mono rounded px-2 py-0.5 text-[10.5px] uppercase',
                  traceTab === t ? 'bg-acc/10 text-acc' : 'text-fg-3 hover:text-fg-0',
                )}
              >
                {t}
              </button>
            ))}
          </div>
          {traceTab === 'timeline' && <TimelineMode />}
          {traceTab === 'context' && <ContextMode />}
          {traceTab === 'raw' && <RawMode />}
        </div>
      )}
    </div>
  )
}
