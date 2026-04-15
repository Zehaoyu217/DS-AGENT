import { useEffect, useMemo, useState } from 'react'
import { useDevtoolsStore } from '../../stores/devtools'
import { fetchTimeline, type Timeline } from './api'

interface Props {
  traceId: string
}

interface FullTrace {
  events: Array<{ kind: string; turn?: number; step_id?: string }>
}

export function CompactionTimeline({ traceId }: Props) {
  const [timeline, setTimeline] = useState<Timeline | null>(null)
  const [trace, setTrace] = useState<FullTrace | null>(null)
  const setSelectedStep = useDevtoolsStore((s) => s.setSelectedStep)

  useEffect(() => {
    fetchTimeline(traceId).then(setTimeline)
    fetch(`/api/trace/traces/${encodeURIComponent(traceId)}`)
      .then((r) => r.json())
      .then((body: FullTrace) => setTrace(body))
  }, [traceId])

  const firstStepByTurn = useMemo(() => {
    const m = new Map<number, string>()
    if (!trace) return m
    for (const e of trace.events) {
      if (e.kind === 'llm_call' && e.turn !== undefined && e.step_id !== undefined) {
        if (!m.has(e.turn)) m.set(e.turn, e.step_id)
      }
    }
    return m
  }, [trace])

  if (!timeline) return <div className="sop-empty">Loading…</div>

  return (
    <div style={{ padding: 12, color: '#e0e0e8', fontFamily: 'monospace', fontSize: 11 }}>
      <div style={{ display: 'flex', gap: 8, alignItems: 'flex-end', marginBottom: 16 }}>
        {timeline.turns.map((t) => {
          const stepId = firstStepByTurn.get(t.turn)
          const disabled = stepId === undefined
          return (
            <button
              key={t.turn}
              type="button"
              role="button"
              aria-label={`Select turn ${t.turn}`}
              disabled={disabled}
              onClick={() => { if (stepId) setSelectedStep(stepId) }}
              style={{
                background: 'transparent',
                border: '1px solid #2a2a3a',
                color: '#e0e0e8',
                padding: 8,
                cursor: disabled ? 'not-allowed' : 'pointer',
                opacity: disabled ? 0.5 : 1,
                fontFamily: 'monospace',
                fontSize: 11,
              }}
            >
              <div>Turn {t.turn}</div>
              <div style={{ color: '#818cf8' }}>in: {t.layers.input ?? 0}</div>
              <div style={{ color: '#94a3b8' }}>tools: {t.layers.tool_calls ?? 0}</div>
            </button>
          )
        })}
      </div>
      <ul style={{ margin: 0, padding: 0, listStyle: 'none' }}>
        {timeline.events.map((e, i) => (
          <li key={i} style={{ marginBottom: 4 }}>
            t{e.turn}: <span style={{ color: '#f59e0b' }}>[{e.kind}]</span> {e.detail}
          </li>
        ))}
      </ul>
    </div>
  )
}
