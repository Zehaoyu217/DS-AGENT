import { useEffect, useState } from 'react'
import { SurfacePage } from '@/components/surface/SurfacePage'
import { StatusTile } from '@/components/surface/StatusTile'
import { HealthSection } from '@/sections/HealthSection'

interface HealthSummary {
  lint?: 'ok' | 'warn' | 'err'
  drift?: 'ok' | 'warn' | 'err'
  autofix?: 'ok' | 'warn' | 'err'
  test?: 'ok' | 'warn' | 'err'
  loaded: boolean
}

async function fetchHealthSummary(): Promise<HealthSummary> {
  try {
    const res = await fetch('/api/health/summary')
    if (!res.ok) return { loaded: true }
    const j = (await res.json()) as Partial<HealthSummary>
    return { ...j, loaded: true }
  } catch {
    return { loaded: true }
  }
}

export function IntegritySurface() {
  const [summary, setSummary] = useState<HealthSummary>({ loaded: false })

  useEffect(() => {
    let cancelled = false
    void fetchHealthSummary().then((s) => {
      if (!cancelled) setSummary(s)
    })
    return () => {
      cancelled = true
    }
  }, [])

  const strip = (
    <div className="grid grid-cols-4 gap-3 px-5 py-3 border-b border-line bg-bg-1">
      <StatusTile
        label="LINT"
        value={summary.lint ?? '—'}
        status={summary.lint ?? 'idle'}
      />
      <StatusTile
        label="DRIFT"
        value={summary.drift ?? '—'}
        status={summary.drift ?? 'idle'}
      />
      <StatusTile
        label="AUTOFIX"
        value={summary.autofix ?? '—'}
        status={summary.autofix ?? 'idle'}
      />
      <StatusTile
        label="TESTS"
        value={summary.test ?? '—'}
        status={summary.test ?? 'idle'}
      />
    </div>
  )

  return (
    <SurfacePage eyebrow="HEALTH PIPELINE" title="Integrity">
      {strip}
      <HealthSection />
    </SurfacePage>
  )
}
