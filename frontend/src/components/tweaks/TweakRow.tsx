import type { ReactNode } from 'react'

interface TweakRowProps {
  label: string
  children: ReactNode
}

export function TweakRow({ label, children }: TweakRowProps) {
  return (
    <div className="flex items-center justify-between py-[6px]">
      <div
        className="font-mono text-[11px] uppercase tracking-wider"
        style={{ color: 'var(--fg-2)', width: 80 }}
      >
        {label}
      </div>
      <div className="flex items-center justify-end">{children}</div>
    </div>
  )
}
