import { useEffect } from 'react'
import { fetchContext } from '../lib/api'
import { useDevtoolsStore } from '../stores/devtools'

const LAYER_COLORS: Record<string, string> = {
  system: '#ef4444',
  l1_always: '#f97316',
  l2_skill: '#f59e0b',
  memory: '#eab308',
  knowledge: '#22c55e',
  conversation: '#818cf8',
}

export function ContextInspector() {
  const { contextSnapshot, setContextSnapshot } = useDevtoolsStore()

  useEffect(() => {
    fetchContext().then(setContextSnapshot).catch(() => {})
    const interval = setInterval(() => {
      fetchContext().then(setContextSnapshot).catch(() => {})
    }, 2000)
    return () => clearInterval(interval)
  }, [setContextSnapshot])

  if (!contextSnapshot) {
    return <div style={{ color: '#94a3b8', padding: 16 }}>Loading context...</div>
  }

  const { total_tokens, max_tokens, utilization, layers, compaction_history } = contextSnapshot

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', height: '100%', overflow: 'hidden' }}>
      {/* Left: layers */}
      <div style={{ overflowY: 'auto', padding: 8, borderRight: '1px solid #2a2a3a' }}>
        <div style={{ color: '#818cf8', fontSize: 10, textTransform: 'uppercase', marginBottom: 8, letterSpacing: 1 }}>
          Context Layers — {total_tokens.toLocaleString()} / {max_tokens.toLocaleString()} tokens ({(utilization * 100).toFixed(1)}%)
        </div>
        {layers.map((layer) => (
          <div
            key={layer.name}
            style={{
              background: '#14141f',
              border: '1px solid #2a2a3a',
              borderLeft: `3px solid ${LAYER_COLORS[layer.name] ?? '#64748b'}`,
              borderRadius: 4,
              padding: 8,
              marginBottom: 6,
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 10 }}>
              <span style={{ color: LAYER_COLORS[layer.name] ?? '#64748b', fontWeight: 600 }}>
                {layer.name.toUpperCase()}
              </span>
              <span style={{ color: '#4a4a5a' }}>{layer.tokens.toLocaleString()} tok</span>
            </div>
            {layer.items.length > 0 && (
              <div style={{ marginTop: 4, fontSize: 9, color: '#94a3b8', lineHeight: 1.5 }}>
                {layer.items.map((item, i) => (
                  <div key={i} style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>{i === layer.items.length - 1 ? '└' : '├'} {item.name}</span>
                    <span>{item.tokens}t</span>
                  </div>
                ))}
              </div>
            )}
            <div style={{ color: '#4a4a5a', fontSize: 9, marginTop: 4 }}>
              {layer.compactable ? 'Compactable' : 'Never compacted'}
            </div>
          </div>
        ))}
      </div>

      {/* Right: compaction history */}
      <div style={{ overflowY: 'auto', padding: 8 }}>
        <div style={{ color: '#818cf8', fontSize: 10, textTransform: 'uppercase', marginBottom: 8, letterSpacing: 1 }}>
          Compaction History
        </div>
        {compaction_history.length === 0 ? (
          <div style={{ color: '#4a4a5a', fontSize: 10 }}>No compactions yet</div>
        ) : (
          compaction_history.map((event) => (
            <div
              key={event.id}
              style={{
                background: '#14141f',
                border: '1px solid #2a2a3a',
                borderLeft: '3px solid #f59e0b',
                borderRadius: 4,
                padding: 8,
                marginBottom: 8,
                fontSize: 9,
                color: '#94a3b8',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                <span style={{ color: '#f59e0b', fontWeight: 600, fontSize: 10 }}>
                  COMPACTION #{event.id}
                </span>
                <span style={{ color: '#4a4a5a' }}>{new Date(event.timestamp).toLocaleTimeString()}</span>
              </div>
              <div>Trigger: {(event.trigger_utilization * 100).toFixed(1)}%</div>
              <div>Before: {event.tokens_before.toLocaleString()}t → After: {event.tokens_after.toLocaleString()}t</div>
              <div style={{ color: '#4ade80' }}>Freed: {event.tokens_freed.toLocaleString()} tokens</div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
