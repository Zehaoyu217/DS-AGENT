import type { ReactNode } from 'react'
import { cn } from '@/lib/utils'

interface SurfacePageProps {
  title: string
  eyebrow?: string
  toolbar?: ReactNode
  drawer?: ReactNode
  drawerOpen?: boolean
  children: ReactNode
  bodyClassName?: string
}

export function SurfacePage({
  title,
  eyebrow,
  toolbar,
  drawer,
  drawerOpen = false,
  children,
  bodyClassName,
}: SurfacePageProps) {
  const showDrawer = Boolean(drawer && drawerOpen)
  return (
    <div className="flex h-full w-full flex-col bg-bg-0 text-fg-0">
      <header
        className={cn(
          'flex h-14 flex-shrink-0 items-center justify-between',
          'border-b border-line px-5',
        )}
      >
        <div className="flex flex-col leading-tight">
          {eyebrow && (
            <span
              className="mono uppercase tracking-[0.06em] text-fg-3"
              style={{ fontSize: 10.5 }}
            >
              {eyebrow}
            </span>
          )}
          <h1 className="text-[18px] font-semibold text-fg-0">{title}</h1>
        </div>
        {toolbar && <div className="flex items-center gap-2">{toolbar}</div>}
      </header>
      <div
        className={cn(
          'grid flex-1 overflow-hidden',
          showDrawer ? 'grid-cols-[1fr_384px]' : 'grid-cols-[1fr]',
        )}
      >
        <main className={cn('overflow-auto', bodyClassName)}>{children}</main>
        {showDrawer && (
          <aside
            className="overflow-auto border-l border-line bg-bg-1"
            aria-label="Surface drawer"
          >
            {drawer}
          </aside>
        )}
      </div>
    </div>
  )
}
