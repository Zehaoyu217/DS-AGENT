import { useRef, useEffect, useState } from 'react'
import mermaid from 'mermaid'
import { TOKENS } from '@/lib/design-tokens'

mermaid.initialize({
  startOnLoad: false,
  theme: 'base',
  themeVariables: {
    background: TOKENS.bgPrimary,
    primaryColor: TOKENS.bgSecondary,
    primaryTextColor: TOKENS.textPrimary,
    primaryBorderColor: TOKENS.info,
    lineColor: TOKENS.textMuted,
    secondaryColor: TOKENS.bgElevated,
    secondaryTextColor: TOKENS.textSecondary,
    secondaryBorderColor: TOKENS.info,
    tertiaryColor: TOKENS.bgPrimary,
    tertiaryTextColor: TOKENS.textSecondary,
    tertiaryBorderColor: TOKENS.textMuted,
    edgeLabelBackground: TOKENS.bgSecondary,
    titleColor: TOKENS.textPrimary,
    textColor: TOKENS.textSecondary,
    clusterBkg: TOKENS.bgPrimary,
    clusterBorder: 'rgba(59,130,246,0.2)',
    fontFamily: 'JetBrains Mono, ui-monospace, monospace',
    noteTextColor: TOKENS.textPrimary,
    noteBkgColor: TOKENS.bgSecondary,
    noteBorderColor: 'rgba(59,130,246,0.3)',
    actorBkg: TOKENS.bgSecondary,
    actorBorder: 'rgba(59,130,246,0.4)',
    actorTextColor: TOKENS.textPrimary,
    actorLineColor: TOKENS.textMuted,
    signalColor: TOKENS.textSecondary,
    signalTextColor: TOKENS.textPrimary,
    labelBoxBkgColor: TOKENS.bgSecondary,
    labelBoxBorderColor: 'rgba(59,130,246,0.3)',
    labelTextColor: TOKENS.textPrimary,
    loopTextColor: TOKENS.textSecondary,
    activationBorderColor: TOKENS.info,
    activationBkgColor: 'rgba(59,130,246,0.12)',
  },
})

interface MermaidDiagramProps {
  code: string
}

export function MermaidDiagram({ code }: MermaidDiagramProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [svg, setSvg] = useState<string>('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!code) return

    setLoading(true)
    setError(null)
    setSvg('')

    const id = `mermaid-${Math.random().toString(36).slice(2)}`
    mermaid
      .render(id, code)
      .then(({ svg: rendered }) => {
        setSvg(rendered)
        setLoading(false)
      })
      .catch((err: unknown) => {
        setError(err instanceof Error ? err.message : 'Failed to render diagram')
        setLoading(false)
      })
  }, [code])

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center gap-3 py-8">
        <div className="w-full max-w-sm space-y-2">
          {[80, 60, 90, 50, 70].map((w, i) => (
            <div
              key={i}
              className="h-2.5 rounded-full bg-surface-700 animate-pulse"
              style={{ width: `${w}%`, animationDelay: `${i * 0.1}s` }}
            />
          ))}
        </div>
        <p className="text-[10px] font-mono text-surface-500 mt-1">Rendering diagram…</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-start gap-2 px-3 py-2 rounded bg-error-bg border border-error/40">
        <div>
          <p className="text-xs font-mono font-semibold text-error mb-0.5">Diagram error</p>
          <p className="text-[10px] font-mono text-error/70 leading-relaxed break-words">{error}</p>
        </div>
      </div>
    )
  }

  if (!svg) return null

  return (
    <div
      ref={containerRef}
      className="flex justify-center overflow-auto my-2 rounded bg-surface-850 border border-surface-700/60 p-3"
      dangerouslySetInnerHTML={{ __html: svg }}
    />
  )
}
