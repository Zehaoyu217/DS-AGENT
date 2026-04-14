import { useRef, useEffect, useState } from 'react'
import embed, { type Result } from 'vega-embed'

interface VegaChartProps {
  spec: string | Record<string, unknown>
}

const FONT = 'JetBrains Mono, ui-monospace, monospace'

const DARK_THEME_CONFIG = {
  background: 'transparent',
  font: FONT,
  title: {
    color: '#f4f4f5',
    fontSize: 13,
    fontWeight: 600 as const,
    font: FONT,
    anchor: 'start' as const,
    offset: 8,
  },
  axis: {
    labelColor: '#a1a1aa',
    titleColor: '#a1a1aa',
    gridColor: 'rgba(255,255,255,0.05)',
    domainColor: '#3f3f46',
    tickColor: '#3f3f46',
    labelFontSize: 11,
    titleFontSize: 12,
    labelFont: FONT,
    titleFont: FONT,
    labelPadding: 6,
  },
  legend: {
    labelColor: '#a1a1aa',
    titleColor: '#f4f4f5',
    labelFontSize: 11,
    titleFontSize: 12,
    labelFont: FONT,
    titleFont: FONT,
    orient: 'bottom' as const,
    padding: 10,
  },
  view: {
    strokeWidth: 0,
  },
  range: {
    category: [
      '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444',
      '#3b82f6', '#ec4899', '#14b8a6', '#f97316', '#6366f1',
    ],
  },
}

const TOOLTIP_OPTS = {
  theme: 'dark' as const,
  style: {
    'background-color': '#18181b',
    'border': '1px solid rgba(255,255,255,0.1)',
    'border-radius': '6px',
    'padding': '6px 10px',
    'font-family': FONT,
    'font-size': '11px',
    'color': '#f4f4f5',
    'box-shadow': '0 4px 16px rgba(0,0,0,0.6)',
  },
}

function enhanceMarkTooltip(spec: Record<string, unknown>): Record<string, unknown> {
  if (!spec || typeof spec !== 'object') return spec
  if (!spec.mark && !spec.encoding) return spec
  const result = { ...spec }
  if (result.encoding && !(result.encoding as Record<string, unknown>).tooltip) {
    result.encoding = {
      ...(result.encoding as Record<string, unknown>),
      tooltip: { content: 'data' },
    }
  }
  return result
}

function enhanceSpec(spec: Record<string, unknown>): Record<string, unknown> {
  if (!spec || typeof spec !== 'object') return spec

  if (Array.isArray(spec.layer)) {
    return { ...spec, layer: (spec.layer as Record<string, unknown>[]).map(enhanceMarkTooltip) }
  }
  if (Array.isArray(spec.hconcat)) {
    return { ...spec, hconcat: (spec.hconcat as Record<string, unknown>[]).map(enhanceSpec) }
  }
  if (Array.isArray(spec.vconcat)) {
    return { ...spec, vconcat: (spec.vconcat as Record<string, unknown>[]).map(enhanceSpec) }
  }

  const enhanced = enhanceMarkTooltip(spec)
  if (!enhanced.params && !enhanced.selection && enhanced.mark) {
    const markType = typeof enhanced.mark === 'string' ? enhanced.mark : (enhanced.mark as Record<string, unknown>)?.type
    if (markType && ['bar', 'point', 'circle', 'line', 'area', 'rect'].includes(markType as string)) {
      enhanced.params = [
        { name: 'hover', select: { type: 'point', on: 'pointerover', clear: 'pointerout' } },
      ]
      const enc = enhanced.encoding as Record<string, unknown> | undefined
      if (enc && !enc.opacity) {
        enhanced.encoding = {
          ...enc,
          opacity: { condition: { param: 'hover', value: 1 }, value: 0.7 },
        }
      }
    }
  }
  return enhanced
}

export function VegaChart({ spec }: VegaChartProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const resultRef = useRef<Result | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!containerRef.current || !spec) return

    let cancelled = false

    async function render() {
      try {
        setError(null)
        const parsed: Record<string, unknown> =
          typeof spec === 'string' ? JSON.parse(spec) : (spec as Record<string, unknown>)
        const enhanced = enhanceSpec(parsed)
        const specWidth = enhanced.width
        const specHeight = enhanced.height
        const hasFixedDimensions =
          typeof specWidth === 'number' && typeof specHeight === 'number'

        const themed: Record<string, unknown> = {
          ...enhanced,
          config: {
            ...DARK_THEME_CONFIG,
            ...((enhanced.config as Record<string, unknown>) ?? {}),
          },
        }

        if (hasFixedDimensions) {
          themed.width = specWidth
          themed.height = specHeight
          themed.autosize = { type: 'pad', contains: 'padding' }
        } else {
          themed.width = 'container'
          themed.autosize = { type: 'fit', contains: 'padding' }
        }

        if (cancelled) return

        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const result = await embed(containerRef.current!, themed as any, {
          actions: { export: true, source: false, compiled: false, editor: false },
          renderer: 'svg',
          tooltip: TOOLTIP_OPTS,
        })

        if (!cancelled) {
          resultRef.current = result
        } else {
          result.finalize()
        }
      } catch (e: unknown) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : 'Failed to render chart')
        }
      }
    }

    render()

    return () => {
      cancelled = true
      if (resultRef.current) {
        resultRef.current.finalize()
        resultRef.current = null
      }
      if (containerRef.current) {
        containerRef.current.innerHTML = ''
      }
    }
  }, [spec])

  if (error) {
    return (
      <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-red-950/40 border border-red-800/40 text-xs text-red-400 font-mono">
        Chart error: {error}
      </div>
    )
  }

  let aspectStyle: React.CSSProperties = {}
  try {
    const parsed =
      typeof spec === 'string' ? JSON.parse(spec) : (spec as Record<string, unknown>)
    if (typeof parsed.width === 'number' && typeof parsed.height === 'number') {
      aspectStyle = {
        aspectRatio: `${parsed.width} / ${parsed.height}`,
        maxWidth: `${parsed.width}px`,
        width: '100%',
      }
    }
  } catch {
    // ignore
  }

  return (
    <div
      style={aspectStyle}
      className="my-2 rounded-lg overflow-hidden bg-surface-850 border border-surface-700/60"
    >
      <div ref={containerRef} className="w-full h-full [&_svg]:w-full [&_svg]:h-full" />
    </div>
  )
}
