import { ACCENT_SWATCHES, type AccentColor } from '@/lib/ui-store'

interface AccentSwatchesProps {
  value: AccentColor
  onChange: (next: AccentColor) => void
}

const SWATCH_LABELS: Record<AccentColor, string> = {
  '#e0733a': 'orange',
  '#a3e635': 'lime',
  '#22d3ee': 'cyan',
  '#c084fc': 'violet',
  '#f472b6': 'pink',
}

export function AccentSwatches({ value, onChange }: AccentSwatchesProps) {
  return (
    <div role="radiogroup" aria-label="Accent color" className="flex items-center gap-[5px]">
      {ACCENT_SWATCHES.map((c) => {
        const active = c === value
        return (
          <button
            key={c}
            type="button"
            role="radio"
            aria-checked={active}
            aria-label={SWATCH_LABELS[c]}
            onClick={() => onChange(c)}
            className="rounded-full transition-transform hover:scale-110"
            style={{
              width: 16,
              height: 16,
              background: c,
              border: active ? '2px solid var(--fg-0)' : '1px solid var(--line)',
              outlineOffset: 2,
            }}
          />
        )
      })}
    </div>
  )
}
