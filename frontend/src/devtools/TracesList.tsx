import { useEffect, useMemo, useRef, useState } from 'react'
import { listTraces, type TraceListItem } from '../lib/api'
import { useDevtoolsStore } from '../stores/devtools'

const POLL_INTERVAL_MS = 2000

function formatDateTime(iso: string): string {
  if (!iso) return ''
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return ''
  const date = d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
  const time = d.toLocaleTimeString(undefined, { hour12: false })
  return `${date} ${time}`
}

function outcomeColor(outcome: string): string {
  if (outcome === 'ok') return '#4ade80'
  if (outcome === 'error') return '#f87171'
  return '#94a3b8'
}

function fmtTokens(n: number): string {
  if (n >= 1000) return `${(n / 1000).toFixed(1)}k`
  return String(n)
}

// ── Types ─────────────────────────────────────────────────────────────────────

type SortKey = 'started_at' | 'llm_call_count' | 'total_input_tokens' | 'total_output_tokens' | 'turn_count' | 'outcome' | 'level'
type SortDir = 'asc' | 'desc'

interface FilterState {
  search: string        // matches session_id substring
  level: string         // '' = all, or label substring
  outcome: string       // '' = all, 'ok' | 'error' | 'pending'
  minTokens: string     // input+output combined minimum
}

// ── Sub-components ────────────────────────────────────────────────────────────

function SortArrow({ col, sortKey, sortDir }: { col: SortKey; sortKey: SortKey; sortDir: SortDir }) {
  if (col !== sortKey) {
    return <span style={{ color: '#3f3f46', marginLeft: 3 }}>↕</span>
  }
  return (
    <span style={{ color: '#e0733a', marginLeft: 3 }}>
      {sortDir === 'desc' ? '↓' : '↑'}
    </span>
  )
}

// ── Main component ────────────────────────────────────────────────────────────

export function TracesList() {
  const selectedTraceId = useDevtoolsStore((s) => s.selectedTraceId)
  const setSelectedTrace = useDevtoolsStore((s) => s.setSelectedTrace)

  const [traces, setTraces] = useState<TraceListItem[]>([])
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  // Sort state — click to toggle desc; click active column again to toggle to asc
  const [sortKey, setSortKey] = useState<SortKey>('started_at')
  const [sortDir, setSortDir] = useState<SortDir>('desc')

  // Filter state
  const [filters, setFilters] = useState<FilterState>({
    search: '',
    level: '',
    outcome: '',
    minTokens: '',
  })
  const [showFilters, setShowFilters] = useState(false)

  // Track previous click for column to toggle direction
  const lastSortKeyRef = useRef<SortKey>(sortKey)

  function handleSort(col: SortKey) {
    if (lastSortKeyRef.current === col) {
      setSortDir((d) => (d === 'desc' ? 'asc' : 'desc'))
    } else {
      setSortKey(col)
      setSortDir('desc') // always start descending on new column
      lastSortKeyRef.current = col
    }
    lastSortKeyRef.current = col
  }

  useEffect(() => {
    let cancelled = false

    async function poll() {
      try {
        const next = await listTraces()
        if (cancelled) return
        setTraces(next)
        setError(null)
      } catch (err: unknown) {
        if (cancelled) return
        setError(err instanceof Error ? err.message : 'listTraces failed')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    poll()
    const handle = window.setInterval(poll, POLL_INTERVAL_MS)
    return () => {
      cancelled = true
      window.clearInterval(handle)
    }
  }, [])

  // Apply filters + sort
  const displayed = useMemo(() => {
    let out = [...traces]

    // Filter
    if (filters.search) {
      const q = filters.search.toLowerCase()
      out = out.filter((t) => t.session_id.toLowerCase().includes(q))
    }
    if (filters.level) {
      const q = filters.level.toLowerCase()
      out = out.filter((t) => t.level_label.toLowerCase().includes(q))
    }
    if (filters.outcome) {
      out = out.filter((t) => t.outcome === filters.outcome)
    }
    if (filters.minTokens) {
      const min = Number(filters.minTokens)
      if (!Number.isNaN(min)) {
        out = out.filter((t) => t.total_input_tokens + t.total_output_tokens >= min)
      }
    }

    // Sort
    out.sort((a, b) => {
      let va: number | string
      let vb: number | string

      switch (sortKey) {
        case 'started_at':      va = a.started_at;      vb = b.started_at;      break
        case 'llm_call_count':  va = a.llm_call_count;  vb = b.llm_call_count;  break
        case 'turn_count':      va = a.turn_count;      vb = b.turn_count;      break
        case 'total_input_tokens':  va = a.total_input_tokens + a.total_output_tokens;  vb = b.total_input_tokens + b.total_output_tokens; break
        case 'total_output_tokens': va = a.total_output_tokens; vb = b.total_output_tokens; break
        case 'outcome':         va = a.outcome;         vb = b.outcome;         break
        case 'level':           va = a.level;           vb = b.level;           break
        default:                va = a.started_at;      vb = b.started_at;
      }

      if (va < vb) return sortDir === 'desc' ? 1 : -1
      if (va > vb) return sortDir === 'desc' ? -1 : 1
      return 0
    })

    return out
  }, [traces, filters, sortKey, sortDir])

  const activeFiltersCount = [
    filters.search, filters.level, filters.outcome, filters.minTokens,
  ].filter(Boolean).length

  // ── Render ─────────────────────────────────────────────────────────────────

  if (loading && traces.length === 0) {
    return <div style={{ padding: 16, color: '#4a4a5a', fontSize: 11 }}>Loading traces…</div>
  }

  if (error && traces.length === 0) {
    return (
      <div style={{ padding: 16, color: '#f87171', fontSize: 11, fontFamily: 'monospace' }}>
        {error}
      </div>
    )
  }

  if (traces.length === 0) {
    return (
      <div style={{ padding: 16, color: '#4a4a5a', fontSize: 11 }}>
        No traces yet. Send a chat message to produce one.
      </div>
    )
  }

  const thStyle: React.CSSProperties = {
    padding: '5px 8px',
    fontWeight: 600,
    cursor: 'pointer',
    whiteSpace: 'nowrap',
    userSelect: 'none',
    color: '#64748b',
    fontSize: 10,
    textTransform: 'uppercase',
    letterSpacing: '0.08em',
  }

  const tdStyle: React.CSSProperties = {
    padding: '4px 8px',
    borderBottom: '1px solid #1c1c24',
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden' }}>
      {/* ── Toolbar ───────────────────────────────────────────────────────── */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 8,
          padding: '6px 8px',
          borderBottom: '1px solid #1c1c24',
          flexShrink: 0,
        }}
      >
        <span style={{ color: '#4a4a5a', fontSize: 10, fontFamily: 'monospace' }}>
          {displayed.length}/{traces.length} traces
        </span>

        {error && (
          <span style={{ color: '#f59e0b', fontSize: 10, fontFamily: 'monospace' }}>
            · polling error
          </span>
        )}

        <div style={{ flex: 1 }} />

        {/* Quick outcome filter */}
        {(['', 'ok', 'error'] as const).map((val) => (
          <button
            key={val}
            onClick={() => setFilters((f) => ({ ...f, outcome: f.outcome === val ? '' : val }))}
            style={{
              padding: '2px 7px',
              fontSize: 10,
              fontFamily: 'monospace',
              background: filters.outcome === val ? (val === 'ok' ? '#052e16' : val === 'error' ? '#1c0606' : '#1e1b4b') : 'transparent',
              color: filters.outcome === val ? (val === 'ok' ? '#4ade80' : val === 'error' ? '#f87171' : '#a5b4fc') : '#4a4a5a',
              border: '1px solid',
              borderColor: filters.outcome === val ? (val === 'ok' ? '#166534' : val === 'error' ? '#7f1d1d' : '#312e81') : '#27272a',
              borderRadius: 3,
              cursor: 'pointer',
            }}
          >
            {val === '' ? 'all' : val}
          </button>
        ))}

        {/* Filter toggle */}
        <button
          onClick={() => setShowFilters((v) => !v)}
          style={{
            padding: '2px 7px',
            fontSize: 10,
            fontFamily: 'monospace',
            background: showFilters || activeFiltersCount > 0 ? '#27272a' : 'transparent',
            color: activeFiltersCount > 0 ? '#e0733a' : '#4a4a5a',
            border: `1px solid ${activeFiltersCount > 0 ? '#7c3010' : '#27272a'}`,
            borderRadius: 3,
            cursor: 'pointer',
          }}
        >
          filter{activeFiltersCount > 0 ? ` (${activeFiltersCount})` : ''}
        </button>
      </div>

      {/* ── Filter row ────────────────────────────────────────────────────── */}
      {showFilters && (
        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: 6,
            padding: '6px 8px',
            borderBottom: '1px solid #1c1c24',
            background: '#0f0f16',
            flexShrink: 0,
          }}
        >
          {(
            [
              { key: 'search',    label: 'session id', placeholder: 'abc123…' },
              { key: 'level',     label: 'level',      placeholder: 'e.g. query' },
              { key: 'minTokens', label: 'min tokens', placeholder: 'e.g. 500' },
            ] as const
          ).map(({ key, label, placeholder }) => (
            <label key={key} style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
              <span style={{ fontSize: 9, fontFamily: 'monospace', color: '#4a4a5a', textTransform: 'uppercase', letterSpacing: '0.1em' }}>
                {label}
              </span>
              <input
                type={key === 'minTokens' ? 'number' : 'text'}
                placeholder={placeholder}
                value={filters[key as keyof FilterState]}
                onChange={(e) => setFilters((f) => ({ ...f, [key]: e.target.value }))}
                style={{
                  background: '#14141f',
                  border: '1px solid #27272a',
                  borderRadius: 3,
                  color: '#a1a1aa',
                  fontFamily: 'monospace',
                  fontSize: 10,
                  padding: '2px 6px',
                  width: key === 'minTokens' ? 80 : 120,
                  outline: 'none',
                }}
              />
            </label>
          ))}

          {activeFiltersCount > 0 && (
            <button
              onClick={() => setFilters({ search: '', level: '', outcome: '', minTokens: '' })}
              style={{
                fontSize: 10,
                fontFamily: 'monospace',
                color: '#f87171',
                background: 'transparent',
                border: 'none',
                cursor: 'pointer',
                padding: '2px 4px',
              }}
            >
              clear
            </button>
          )}
        </div>
      )}

      {/* ── Table ─────────────────────────────────────────────────────────── */}
      <div style={{ flex: 1, overflowY: 'auto', overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 11 }}>
          <thead>
            <tr style={{ position: 'sticky', top: 0, background: '#09090b', zIndex: 1 }}>
              {(
                [
                  { col: 'started_at' as SortKey,         label: 'date / time' },
                  { col: 'total_input_tokens' as SortKey, label: 'tokens in+out' },
                  { col: 'llm_call_count' as SortKey,     label: 'llm calls' },
                  { col: 'turn_count' as SortKey,         label: 'turns' },
                  { col: 'level' as SortKey,              label: 'level' },
                  { col: 'outcome' as SortKey,            label: 'outcome' },
                ]
              ).map(({ col, label }) => (
                <th
                  key={col}
                  style={thStyle}
                  onClick={() => handleSort(col)}
                  title={`Sort by ${label}. Click once for descending, again for ascending.`}
                >
                  {label}
                  <SortArrow col={col} sortKey={sortKey} sortDir={sortDir} />
                </th>
              ))}
              <th style={{ ...thStyle, cursor: 'default' }}>session</th>
            </tr>
          </thead>
          <tbody>
            {displayed.length === 0 ? (
              <tr>
                <td
                  colSpan={7}
                  style={{ padding: '16px 8px', color: '#4a4a5a', fontSize: 11, fontFamily: 'monospace', textAlign: 'center' }}
                >
                  no traces match filters
                </td>
              </tr>
            ) : (
              displayed.map((trace) => {
                const isSelected = trace.session_id === selectedTraceId
                const totalTok = trace.total_input_tokens + trace.total_output_tokens
                return (
                  <tr
                    key={trace.session_id}
                    onClick={() => setSelectedTrace(trace.session_id)}
                    style={{
                      background: isSelected ? '#1a1a2e' : 'transparent',
                      color: isSelected ? '#e0e0e8' : '#94a3b8',
                      cursor: 'pointer',
                      fontFamily: 'monospace',
                    }}
                  >
                    <td style={tdStyle}>{formatDateTime(trace.started_at)}</td>
                    <td style={tdStyle}>
                      {fmtTokens(trace.total_input_tokens)}
                      <span style={{ color: '#3f3f46', margin: '0 2px' }}>/</span>
                      {fmtTokens(trace.total_output_tokens)}
                      <span style={{ color: '#3f3f46', fontSize: 9, marginLeft: 4 }}>
                        ({fmtTokens(totalTok)})
                      </span>
                    </td>
                    <td style={tdStyle}>{trace.llm_call_count}</td>
                    <td style={tdStyle}>{trace.turn_count}</td>
                    <td style={tdStyle}>{trace.level_label}</td>
                    <td style={{ ...tdStyle, color: outcomeColor(trace.outcome) }}>{trace.outcome}</td>
                    <td style={{ ...tdStyle, color: '#3f3f46', fontSize: 10, maxWidth: 120, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {trace.session_id.slice(0, 16)}…
                    </td>
                  </tr>
                )
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
