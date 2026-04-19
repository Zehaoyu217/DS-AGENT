import { useEffect, useRef } from 'react'
import { Search } from 'lucide-react'
import { cn } from '@/lib/utils'

interface SearchBarProps {
  value: string
  onChange: (v: string) => void
  placeholder?: string
  hotkey?: string
  ariaLabel: string
  className?: string
  autoFocus?: boolean
}

export function SearchBar({
  value,
  onChange,
  placeholder = 'Search…',
  hotkey,
  ariaLabel,
  className,
  autoFocus = false,
}: SearchBarProps) {
  const inputRef = useRef<HTMLInputElement | null>(null)

  useEffect(() => {
    if (autoFocus) inputRef.current?.focus()
  }, [autoFocus])

  useEffect(() => {
    if (!hotkey) return
    const handler = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement | null
      if (target && /^(INPUT|TEXTAREA|SELECT)$/.test(target.tagName)) return
      if (e.key === hotkey) {
        e.preventDefault()
        inputRef.current?.focus()
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [hotkey])

  return (
    <label
      className={cn(
        'flex h-8 items-center gap-2 rounded-md border border-line bg-bg-1 px-2.5',
        'focus-within:border-acc focus-within:ring-1 focus-within:ring-acc/40',
        className,
      )}
    >
      <Search size={13} className="text-fg-3" aria-hidden />
      <input
        ref={inputRef}
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        aria-label={ariaLabel}
        className={cn(
          'flex-1 bg-transparent text-[13px] text-fg-0 placeholder:text-fg-3',
          'focus:outline-none',
        )}
      />
      {hotkey && (
        <kbd
          className="mono rounded bg-bg-2 px-1 text-[10px] text-fg-3"
          aria-hidden
        >
          {hotkey}
        </kbd>
      )}
    </label>
  )
}
