import { useEffect, useState } from 'react'
import { MarkdownContent } from '@/components/chat/MarkdownContent'

export function HealthSection() {
  const [markdown, setMarkdown] = useState<string | null>(null)
  const [missing, setMissing] = useState(false)

  useEffect(() => {
    let cancelled = false
    fetch('/static/health/latest.md')
      .then(async (r) => {
        if (cancelled) return
        if (!r.ok) {
          setMissing(true)
          return
        }
        const text = await r.text()
        if (!cancelled) setMarkdown(text)
      })
      .catch(() => {
        if (!cancelled) setMissing(true)
      })
    return () => {
      cancelled = true
    }
  }, [])

  if (missing) {
    return (
      <div className="p-6 text-surface-300">
        <p className="text-sm">
          No integrity report yet. Run <code>make integrity</code> to generate one.
        </p>
      </div>
    )
  }
  if (markdown == null) {
    return <div className="p-6 text-surface-500 text-sm">Loading health report…</div>
  }
  return (
    <div className="p-6 max-w-4xl mx-auto overflow-y-auto h-full">
      <MarkdownContent content={markdown} />
    </div>
  )
}
