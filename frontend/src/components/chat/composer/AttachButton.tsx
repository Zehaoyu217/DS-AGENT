import { useRef } from 'react'
import { nanoid } from 'nanoid'
import { Paperclip } from 'lucide-react'
import { useChatStore } from '@/lib/store'

const ICON_BTN = 'flex h-7 w-7 items-center justify-center rounded-md transition-colors'

interface AttachButtonProps {
  conversationId: string
}

export function AttachButton({ conversationId }: AttachButtonProps) {
  const inputRef = useRef<HTMLInputElement>(null)
  const addAttachedFile = useChatStore((s) => s.addAttachedFile)

  const onPick = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    addAttachedFile(conversationId, {
      id: nanoid(),
      name: file.name,
      size: file.size,
      mimeType: file.type || 'application/octet-stream',
    })
    e.target.value = ''
  }

  return (
    <>
      <input ref={inputRef} type="file" className="hidden" onChange={onPick} />
      <button
        type="button"
        title="Attach file"
        aria-label="Attach file"
        onClick={() => inputRef.current?.click()}
        className={ICON_BTN}
        style={{ color: 'var(--fg-2)' }}
      >
        <Paperclip size={14} />
      </button>
    </>
  )
}
