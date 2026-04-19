import { Hash } from 'lucide-react'

interface SkillButtonProps {
  onInsert: (token: string) => void
}

export function SkillButton({ onInsert }: SkillButtonProps) {
  return (
    <button
      type="button"
      aria-label="Skill"
      onClick={() => onInsert('#')}
      className="flex h-7 w-7 items-center justify-center rounded-md"
      style={{ color: 'var(--fg-2)' }}
    >
      <Hash size={14} />
    </button>
  )
}
