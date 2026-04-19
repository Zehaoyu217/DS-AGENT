import type { ReactNode } from 'react'
import { X } from 'lucide-react'
import { cn } from '@/lib/utils'

interface DrawerSlotProps {
  title: string
  eyebrow?: string
  onClose: () => void
  children: ReactNode
  footer?: ReactNode
  className?: string
}

export function DrawerSlot({
  title,
  eyebrow,
  onClose,
  children,
  footer,
  className,
}: DrawerSlotProps) {
  return (
    <div className={cn('flex h-full w-full flex-col bg-bg-1', className)}>
      <header
        className={cn(
          'flex h-12 flex-shrink-0 items-center justify-between',
          'border-b border-line px-4',
        )}
      >
        <div className="flex flex-col leading-tight">
          {eyebrow && (
            <span
              className="mono uppercase tracking-[0.06em] text-fg-3"
              style={{ fontSize: 10 }}
            >
              {eyebrow}
            </span>
          )}
          <span className="text-[13px] font-semibold text-fg-0">{title}</span>
        </div>
        <button
          type="button"
          aria-label="Close drawer"
          onClick={onClose}
          className={cn(
            'flex h-7 w-7 items-center justify-center rounded-md',
            'text-fg-2 hover:bg-bg-2 hover:text-fg-0 focus-ring',
          )}
        >
          <X size={14} aria-hidden />
        </button>
      </header>
      <div className="flex-1 overflow-auto px-4 py-3">{children}</div>
      {footer && (
        <footer className="flex-shrink-0 border-t border-line px-4 py-2">
          {footer}
        </footer>
      )}
    </div>
  )
}
