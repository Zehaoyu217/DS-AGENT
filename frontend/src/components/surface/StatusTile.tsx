import type { ReactNode } from 'react'
import { cn } from '@/lib/utils'

export type TileStatus = 'ok' | 'warn' | 'err' | 'info' | 'idle'

interface StatusTileProps {
  label: string
  value: ReactNode
  status: TileStatus
  hint?: string
  onClick?: () => void
  className?: string
}

const STATUS_BORDER: Record<TileStatus, string> = {
  ok: 'border-b-ok',
  warn: 'border-b-warn',
  err: 'border-b-err',
  info: 'border-b-acc',
  idle: 'border-b-line',
}

const STATUS_LABEL_COLOR: Record<TileStatus, string> = {
  ok: 'text-ok',
  warn: 'text-warn',
  err: 'text-err',
  info: 'text-acc',
  idle: 'text-fg-3',
}

export function StatusTile({
  label,
  value,
  status,
  hint,
  onClick,
  className,
}: StatusTileProps) {
  const Tag = onClick ? 'button' : 'div'
  return (
    <Tag
      type={onClick ? 'button' : undefined}
      onClick={onClick}
      title={hint}
      className={cn(
        'flex h-[88px] flex-col justify-between rounded-md',
        'border border-line bg-bg-1 px-3 py-2 text-left',
        'border-b-2',
        STATUS_BORDER[status],
        onClick && 'transition-colors hover:bg-bg-2 focus-ring',
        className,
      )}
    >
      <span
        className={cn(
          'mono uppercase tracking-[0.06em]',
          STATUS_LABEL_COLOR[status],
        )}
        style={{ fontSize: 10 }}
      >
        {label}
      </span>
      <span className="text-[18px] font-semibold text-fg-0">{value}</span>
    </Tag>
  )
}
