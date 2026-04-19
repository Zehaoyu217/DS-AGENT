/** Two/three-segment toggle used inside Tweaks rows. */
interface Seg2Option<T extends string> {
  value: T
  label: string
}

interface Seg2Props<T extends string> {
  options: ReadonlyArray<Seg2Option<T>>
  value: T
  onChange: (next: T) => void
  ariaLabel?: string
}

export function Seg2<T extends string>({ options, value, onChange, ariaLabel }: Seg2Props<T>) {
  return (
    <div
      role="radiogroup"
      aria-label={ariaLabel}
      className="inline-flex items-center rounded-[8px] p-[2px] text-[11px]"
      style={{ background: 'var(--bg-2)', border: '1px solid var(--line)' }}
    >
      {options.map((opt) => {
        const active = opt.value === value
        return (
          <button
            key={opt.value}
            type="button"
            role="radio"
            aria-checked={active}
            onClick={() => onChange(opt.value)}
            className="rounded-[6px] px-2 py-[3px] font-mono uppercase tracking-wider transition-colors"
            style={{
              background: active ? 'var(--bg-0)' : 'transparent',
              color: active ? 'var(--fg-0)' : 'var(--fg-2)',
              boxShadow: active ? 'var(--shadow-1)' : 'none',
            }}
          >
            {opt.label}
          </button>
        )
      })}
    </div>
  )
}
