import { Paperclip } from 'lucide-react'

interface AttachedFileChipProps {
  name: string
}

export function AttachedFileChip({ name }: AttachedFileChipProps) {
  return (
    <span
      className="inline-flex items-center gap-1.5 rounded-md border px-2 py-0.5 text-[11.5px]"
      style={{
        borderColor: 'var(--line-2)',
        background: 'var(--bg-2)',
        color: 'var(--fg-1)',
      }}
    >
      <Paperclip size={11} style={{ color: 'var(--fg-2)' }} />
      <span className="mono text-[11px]">{name}</span>
    </span>
  )
}
