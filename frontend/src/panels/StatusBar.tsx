import { useDevtoolsStore } from '../stores/devtools'

export function StatusBar() {
  const { isOpen, toggle, contextSnapshot } = useDevtoolsStore()
  const utilization = contextSnapshot
    ? `${(contextSnapshot.utilization * 100).toFixed(1)}%`
    : '—'

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '4px 12px',
      background: '#14141f',
      borderTop: '1px solid #2a2a3a',
      fontSize: '10px',
      color: '#64748b',
      fontFamily: 'monospace',
    }}>
      <div style={{ display: 'flex', gap: 16 }}>
        <span>DuckDB: <span style={{ color: '#94a3b8' }}>—</span></span>
        <span>Ollama: <span style={{ color: '#94a3b8' }}>—</span></span>
        <span>Context: <span style={{ color: '#94a3b8' }}>{utilization}</span></span>
      </div>
      <button
        onClick={toggle}
        style={{
          background: 'none',
          border: 'none',
          color: isOpen ? '#818cf8' : '#64748b',
          cursor: 'pointer',
          fontSize: '10px',
          fontFamily: 'monospace',
        }}
      >
        {isOpen ? '⚙ DEV MODE ON' : '⚙ Cmd+Shift+D'}
      </button>
    </div>
  )
}
