import { useState } from 'react'
import { useDevtoolsStore } from '../stores/devtools'
import { ContextInspector } from './ContextInspector'
import { SessionReplay } from './sop/SessionReplay'
import { JudgeVariance } from './sop/JudgeVariance'
import { PromptInspector } from './sop/PromptInspector'
import { CompactionTimeline } from './sop/CompactionTimeline'

const TABS = [
  'events', 'skills', 'config', 'wiki', 'evals', 'context',
  'sop-sessions', 'sop-judge', 'sop-prompt', 'sop-timeline',
] as const

function Placeholder({ name }: { name: string }) {
  return (
    <div style={{ color: '#4a4a5a', padding: 16, fontSize: 12 }}>
      {name} tab — not yet implemented
    </div>
  )
}

export function DevToolsPanel() {
  const { isOpen, activeTab, setActiveTab } = useDevtoolsStore()
  // v1: trace selection is not wired — Session Replay does not yet expose a
  // selection callback. The three dependent tabs show a placeholder until a
  // future task adds selection state and threads it through SessionReplay.
  const [selectedTraceId] = useState<string | null>(null)
  const [selectedStepId] = useState<string | null>(null)

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
        {activeTab === 'sop-sessions' && <SessionReplay />}
        {activeTab === 'sop-judge' && (
          selectedTraceId
            ? <JudgeVariance traceId={selectedTraceId} />
            : <div className="sop-empty">Select a trace from the Session Replay tab.</div>
        )}
        {activeTab === 'sop-prompt' && (
          selectedTraceId && selectedStepId
            ? <PromptInspector traceId={selectedTraceId} stepId={selectedStepId} />
            : <div className="sop-empty">Select a trace+step from the Session Replay tab.</div>
        )}
        {activeTab === 'sop-timeline' && (
          selectedTraceId
            ? <CompactionTimeline traceId={selectedTraceId} />
            : <div className="sop-empty">Select a trace from the Session Replay tab.</div>
        )}
        {!['context', 'sop-sessions', 'sop-judge', 'sop-prompt', 'sop-timeline'].includes(activeTab) && (
          <Placeholder name={activeTab} />
        )}
      </div>
    </div>
  )
}
