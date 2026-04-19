import { useState } from 'react'
import { Download } from 'lucide-react'
import { useChatStore } from '@/lib/store'
import { toMarkdown, toJson, toHtml } from './export-formatters'

interface ExportMenuProps {
  conversationId: string
}

function download(filename: string, body: string, mime: string) {
  const blob = new Blob([body], { type: mime })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}

export function ExportMenu({ conversationId }: ExportMenuProps) {
  const [open, setOpen] = useState(false)
  const conv = useChatStore((s) => s.conversations.find((c) => c.id === conversationId))

  const handle = (format: 'md' | 'json' | 'html') => {
    if (!conv) return
    const base = conv.title.replace(/[^\w-]+/g, '_') || 'conversation'
    try {
      if (format === 'md') download(`${base}.md`, toMarkdown(conv), 'text/markdown')
      if (format === 'json') download(`${base}.json`, toJson(conv), 'application/json')
      if (format === 'html') download(`${base}.html`, toHtml(conv), 'text/html')
    } finally {
      setOpen(false)
    }
  }

  return (
    <div className="relative">
      <button
        type="button"
        aria-label="Export"
        onClick={() => setOpen((v) => !v)}
        className="flex items-center gap-1.5 rounded-md border px-2.5 py-1 text-[12px]"
        style={{ borderColor: 'var(--line-2)', color: 'var(--fg-1)' }}
      >
        <Download size={12} /> Export
      </button>
      {open && (
        <div
          role="menu"
          className="absolute right-0 top-full mt-1 overflow-hidden rounded-md border shadow-[var(--shadow-2)]"
          style={{ borderColor: 'var(--line)', background: 'var(--bg-1)' }}
        >
          <button
            type="button"
            role="menuitem"
            className="block w-full px-3 py-1.5 text-left text-[12px]"
            style={{ color: 'var(--fg-1)' }}
            onClick={() => handle('md')}
          >
            Markdown (.md)
          </button>
          <button
            type="button"
            role="menuitem"
            className="block w-full px-3 py-1.5 text-left text-[12px]"
            style={{ color: 'var(--fg-1)' }}
            onClick={() => handle('json')}
          >
            JSON (.json)
          </button>
          <button
            type="button"
            role="menuitem"
            className="block w-full px-3 py-1.5 text-left text-[12px]"
            style={{ color: 'var(--fg-1)' }}
            onClick={() => handle('html')}
          >
            HTML (.html)
          </button>
        </div>
      )}
    </div>
  )
}
