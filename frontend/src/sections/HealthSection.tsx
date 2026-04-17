import { useEffect, useState } from 'react'
import { MarkdownContent } from '@/components/chat/MarkdownContent'

interface AutofixArtifact {
  date?: string
  mode?: string
  fix_classes_run?: string[]
  fix_classes_skipped?: string[]
  diffs_by_class?: Record<string, unknown[]>
  pr_results?: Record<string, unknown>
}

function AutofixTile({ artifact }: { artifact: AutofixArtifact | null }) {
  if (!artifact) return null
  const openPrs = artifact.pr_results ? Object.keys(artifact.pr_results).length : 0
  const disabled = artifact.fix_classes_skipped?.length ?? 0
  const lastRun = artifact.date ?? '—'
  const mode = artifact.mode ?? '—'
  return (
    <section
      aria-labelledby="autofix-heading"
      className="mt-6 border-t border-surface-800 pt-4"
    >
      <h3 id="autofix-heading" className="text-xs font-mono uppercase tracking-wider text-surface-400 mb-2">
        AUTOFIX
      </h3>
      <dl className="grid grid-cols-4 gap-4 text-sm">
        <div>
          <dt className="text-surface-500 text-xs">Mode</dt>
          <dd className="font-mono">{mode}</dd>
        </div>
        <div>
          <dt className="text-surface-500 text-xs">Open PRs</dt>
          <dd className="font-mono">{openPrs}</dd>
        </div>
        <div>
          <dt className="text-surface-500 text-xs">Disabled classes</dt>
          <dd className="font-mono">{disabled}</dd>
        </div>
        <div>
          <dt className="text-surface-500 text-xs">Last run</dt>
          <dd className="font-mono">{lastRun}</dd>
        </div>
      </dl>
    </section>
  )
}

export function HealthSection() {
  const [markdown, setMarkdown] = useState<string | null>(null)
  const [missing, setMissing] = useState(false)
  const [autofix, setAutofix] = useState<AutofixArtifact | null>(null)

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

  useEffect(() => {
    let cancelled = false
    fetch('/static/health/autofix.json')
      .then(async (r) => {
        if (!r.ok || cancelled) return
        const data = (await r.json()) as AutofixArtifact
        if (!cancelled) setAutofix(data)
      })
      .catch(() => {
        // Silently ignore — autofix is a secondary signal.
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
      <AutofixTile artifact={autofix} />
    </div>
  )
}
