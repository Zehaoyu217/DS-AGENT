import { useState } from 'react'
import { MoreHorizontal } from 'lucide-react'
import { useChatStore } from '@/lib/store'

interface MoreMenuProps {
  conversationId: string
  onRename: () => void
}

export function MoreMenu({ conversationId, onRename }: MoreMenuProps) {
  const [open, setOpen] = useState(false)
  const fork = useChatStore((s) => s.forkConversation)
  const del = useChatStore((s) => s.deleteConversation)

  const handleDuplicate = () => {
    fork(conversationId)
    setOpen(false)
  }
  const handleDelete = () => {
    del(conversationId)
    setOpen(false)
  }
  const handleRename = () => {
    onRename()
    setOpen(false)
  }

  return (
    <div className="relative">
      <button
        type="button"
        aria-label="More"
        onClick={() => setOpen((v) => !v)}
        className="rounded-md p-1.5"
        style={{ color: 'var(--fg-2)' }}
      >
        <MoreHorizontal size={15} />
      </button>
      {open && (
        <div
          role="menu"
          className="absolute right-0 top-full mt-1 min-w-[140px] overflow-hidden rounded-md border shadow-[var(--shadow-2)]"
          style={{ borderColor: 'var(--line)', background: 'var(--bg-1)' }}
        >
          <button
            type="button"
            role="menuitem"
            className="block w-full px-3 py-1.5 text-left text-[12px]"
            style={{ color: 'var(--fg-1)' }}
            onClick={handleRename}
          >
            Rename
          </button>
          <button
            type="button"
            role="menuitem"
            className="block w-full px-3 py-1.5 text-left text-[12px]"
            style={{ color: 'var(--fg-1)' }}
            onClick={handleDuplicate}
          >
            Duplicate
          </button>
          <button
            type="button"
            role="menuitem"
            className="block w-full px-3 py-1.5 text-left text-[12px]"
            style={{ color: 'var(--err)' }}
            onClick={handleDelete}
          >
            Delete
          </button>
        </div>
      )}
    </div>
  )
}
