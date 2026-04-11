import { useDevtoolsStore } from '../stores/devtools'
import { ContextInspector } from './ContextInspector'

const TABS = ['events', 'skills', 'config', 'wiki', 'evals', 'context'] as const

function Placeholder({ name }: { name: string }) {
  return (
    <div style={{ color: '#4a4a5a', padding: 16, fontSize: 12 }}>
      {name} tab — not yet implemented
    </div>
  )
}

export function DevToolsPanel() {
  const { isOpen, activeTab, setActiveTab } = useDevtoolsStore()
  if (!isOpen) return null

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 32,
      background: '#0a0a0f',
      color: '#e0e0e8',
      fontFamily: 'monospace',
      fontSize: 11,
      zIndex: 1000,
      display: 'flex',
      flexDirection: 'column',
    }}>
      {/* Tab bar */}
      <div style={{
        display: 'flex',
        gap: 16,
        padding: '8px 12px',
        borderBottom: '1px solid #2a2a3a',
        background: '#14141f',
      }}>
        <span style={{ color: '#818cf8', fontWeight: 600 }}>⚙ DEV MODE</span>
        {TABS.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            style={{
              background: 'none',
              border: 'none',
              color: activeTab === tab ? '#818cf8' : '#94a3b8',
              borderBottom: activeTab === tab ? '1px solid #818cf8' : 'none',
              cursor: 'pointer',
              fontSize: 11,
              fontFamily: 'monospace',
              textTransform: 'capitalize',
              padding: '0 4px 4px',
            }}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div style={{ flex: 1, overflow: 'hidden' }}>
        {activeTab === 'context' && <ContextInspector />}
        {activeTab !== 'context' && <Placeholder name={activeTab} />}
      </div>
    </div>
  )
}
