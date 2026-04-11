import { useEffect } from 'react'
import { StatusBar } from './panels/StatusBar'
import { DevToolsPanel } from './devtools/DevToolsPanel'
import { useDevtoolsStore } from './stores/devtools'

export default function App() {
  const toggle = useDevtoolsStore((s) => s.toggle)

  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.shiftKey && e.key === 'D') {
        e.preventDefault()
        toggle()
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [toggle])

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100vh',
      background: '#0a0a0f',
      color: '#e0e0e8',
    }}>
      {/* Main content area (placeholder for analytical UI) */}
      <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ textAlign: 'center', color: '#4a4a5a' }}>
          <h1 style={{ fontSize: 24, fontWeight: 300, marginBottom: 8 }}>Analytical Agent</h1>
          <p style={{ fontSize: 12 }}>Press Cmd+Shift+D to open developer tools</p>
        </div>
      </div>

      {/* Devtools overlay */}
      <DevToolsPanel />

      {/* Status bar (always visible) */}
      <StatusBar />
    </div>
  )
}
