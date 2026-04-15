import { useEffect, useState } from 'react'
import { useDevtoolsStore } from '../../stores/devtools'
import { listSessions, type SOPSession } from './api'

export function SessionReplay() {
  const [sessions, setSessions] = useState<SOPSession[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const selectedTraceId = useDevtoolsStore((s) => s.selectedTraceId)
  const setSelectedTrace = useDevtoolsStore((s) => s.setSelectedTrace)

  useEffect(() => {
    listSessions()
      .then(setSessions)
      .catch((e: unknown) => setError(e instanceof Error ? e.message : 'error'))
  }, [])

  if (error) return <div className="sop-empty">Failed to load sessions: {error}</div>
  if (sessions === null) return <div className="sop-empty">Loading…</div>
  if (sessions.length === 0) {
    return (
      <div className="sop-empty">
        No sessions yet. Run eval with <code>TRACE_MODE=always make eval</code> to populate.
      </div>
    )
  }

  return (
    <div className="sop-session-list">
      {sessions.map((s) => {
        const traceId = s.trace_links.trace_id
        const selected = traceId !== null && traceId === selectedTraceId
        const disabled = traceId === null
        return (
          <button
            key={s.session_id}
            type="button"
            role="button"
            aria-selected={selected}
            disabled={disabled}
            onClick={() => { if (traceId) setSelectedTrace(traceId) }}
            className={`sop-row ${selected ? 'sop-row--selected' : ''}`}
            style={{
              display: 'flex',
              flexDirection: 'column',
              padding: '8px 12px',
              background: 'transparent',
              border: 'none',
              borderLeft: selected ? '2px solid #818cf8' : '2px solid transparent',
              color: '#e0e0e8',
              textAlign: 'left',
              cursor: disabled ? 'not-allowed' : 'pointer',
              opacity: disabled ? 0.5 : 1,
              fontFamily: 'monospace',
              fontSize: 11,
            }}
          >
            <span>
              <strong>{s.session_id}</strong> — level {s.level} — {s.triage.bucket ?? '—'}
              {disabled ? ' (no trace)' : ''}
            </span>
            <span style={{ color: '#94a3b8' }}>
              {s.overall_grade_before ?? '—'} → {s.outcome.grade_after ?? '—'} · {s.fix.name ?? 'no-fix'}
            </span>
          </button>
        )
      })}
    </div>
  )
}
