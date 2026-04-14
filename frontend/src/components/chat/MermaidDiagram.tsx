import { useRef, useEffect, useState } from 'react'
import mermaid from 'mermaid'

mermaid.initialize({
  startOnLoad: false,
  theme: 'base',
  themeVariables: {
    background: '#09090b',
    primaryColor: '#18181b',
    primaryTextColor: '#f4f4f5',
    primaryBorderColor: '#8b5cf6',
    lineColor: '#52525b',
    secondaryColor: '#27272a',
    secondaryTextColor: '#a1a1aa',
    secondaryBorderColor: '#8b5cf6',
    tertiaryColor: '#09090b',
    tertiaryTextColor: '#a1a1aa',
    tertiaryBorderColor: '#52525b',
    edgeLabelBackground: '#18181b',
    titleColor: '#f4f4f5',
    textColor: '#a1a1aa',
    clusterBkg: '#09090b',
    clusterBorder: 'rgba(139,92,246,0.2)',
    fontFamily: 'JetBrains Mono, ui-monospace, monospace',
    noteTextColor: '#f4f4f5',
    noteBkgColor: '#18181b',
    noteBorderColor: 'rgba(139,92,246,0.3)',
    actorBkg: '#18181b',
    actorBorder: 'rgba(139,92,246,0.4)',
    actorTextColor: '#f4f4f5',
    actorLineColor: '#52525b',
    signalColor: '#a1a1aa',
    signalTextColor: '#f4f4f5',
    labelBoxBkgColor: '#18181b',
    labelBoxBorderColor: 'rgba(139,92,246,0.3)',
    labelTextColor: '#f4f4f5',
    loopTextColor: '#a1a1aa',
    activationBorderColor: '#8b5cf6',
    activationBkgColor: 'rgba(139,92,246,0.12)',
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
      <div className="flex items-start gap-2 px-3 py-2 rounded-lg bg-red-950/40 border border-red-800/40">
        <div>
          <p className="text-xs font-mono font-semibold text-red-400 mb-0.5">Diagram error</p>
          <p className="text-[10px] font-mono text-red-400/70 leading-relaxed break-words">{error}</p>
        </div>
      </div>
    )
  }

  if (!svg) return null

  return (
    <div
      ref={containerRef}
      className="flex justify-center overflow-auto my-2 rounded-lg bg-surface-850 border border-surface-700/60 p-3"
      dangerouslySetInnerHTML={{ __html: svg }}
    />
  )
}
