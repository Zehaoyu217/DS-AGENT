import type { ContextLayer } from '@/lib/store'

interface LayerBarsProps {
  layers: ContextLayer[]
}

function fmtK(n: number): string {
  return n >= 1000 ? `${Math.round(n / 100) / 10}k` : `${n}`
}

export function LayerBars({ layers }: LayerBarsProps) {
  const max = Math.max(1, ...layers.map((l) => l.tokens))
  return (
    <ul className="flex flex-col gap-1.5">
      {layers.map((l) => {
        const pct = Math.round((l.tokens / max) * 100)
        return (
          <li key={l.id} className="flex items-center gap-2">
            <span className="mono w-20 truncate text-[10.5px] text-fg-2">{l.label}</span>
            <div
              className="relative h-2 flex-1 overflow-hidden rounded bg-bg-2"
              role="progressbar"
              aria-valuenow={pct}
              aria-valuemin={0}
              aria-valuemax={100}
              aria-label={`${l.label} tokens`}
            >
              <div className="h-full bg-fg-2" style={{ width: `${pct}%` }} />
            </div>
            <span className="mono w-12 text-right text-[10.5px] text-fg-3">{fmtK(l.tokens)}</span>
          </li>
        )
      })}
    </ul>
  )
}
