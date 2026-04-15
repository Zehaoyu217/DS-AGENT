import { cn } from '@/lib/utils'

interface ResizeHandleProps {
  onMouseDown: (e: React.MouseEvent) => void
  direction?: 'horizontal' | 'vertical'
  className?: string
}

/**
 * Drag handle between resizable panels.
 * Wider hit area (8px) with a subtle visible rest-state indicator
 * so the handle is discoverable before hover.
 */
export function ResizeHandle({
  onMouseDown,
  direction = 'horizontal',
  className,
}: ResizeHandleProps) {
  const isH = direction === 'horizontal'

  return (
    <div
      onMouseDown={onMouseDown}
      role="separator"
      aria-orientation={isH ? 'vertical' : 'horizontal'}
      aria-label={isH ? 'Resize panels horizontally' : 'Resize panels vertically'}
      className={cn(
        'group flex-shrink-0 flex items-center justify-center z-10',
        'transition-colors hover:bg-brand-accent/8 active:bg-brand-accent/12',
        isH ? 'w-2 cursor-col-resize' : 'h-2 cursor-row-resize',
        className,
      )}
    >
      {/* Visible at rest (low-opacity line) → orange on hover */}
      <div
        className={cn(
          'rounded-full transition-all duration-150',
          'bg-surface-600/60 group-hover:bg-brand-accent/70 group-active:bg-brand-accent',
          isH ? 'w-px h-8 group-hover:h-12' : 'h-px w-8 group-hover:w-12',
        )}
      />
    </div>
  )
}
