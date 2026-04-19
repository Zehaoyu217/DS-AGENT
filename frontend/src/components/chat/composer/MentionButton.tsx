import { AtSign } from 'lucide-react'

interface MentionButtonProps {
  onInsert: (token: string) => void
}

export function MentionButton({ onInsert }: MentionButtonProps) {
  return (
    <button
      type="button"
      aria-label="Mention file"
      onClick={() => onInsert('@')}
      className="flex h-7 w-7 items-center justify-center rounded-md"
      style={{ color: 'var(--fg-2)' }}
    >
      <AtSign size={14} />
    </button>
  )
}
