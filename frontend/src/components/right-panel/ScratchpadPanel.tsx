import React from 'react'
import { useChatStore } from '../../lib/store'

export function ScratchpadPanel(): React.ReactElement {
  const scratchpad = useChatStore((s) => s.scratchpad)

  return (
    <div className="flex flex-col flex-1 min-h-0 p-3">
      <p className="text-[10px] font-mono font-semibold tracking-widest text-surface-500 uppercase mb-2">
        Scratchpad
      </p>
      <div className="border-t border-surface-800 mb-3" />
      {scratchpad ? (
        <div className="flex-1 min-h-0 overflow-y-auto">
          <pre className="text-xs font-mono text-surface-300 leading-relaxed whitespace-pre-wrap break-words">
            {scratchpad}
          </pre>
        </div>
      ) : (
        <div>
          <p className="text-xs font-mono text-surface-500">No scratchpad content yet.</p>
          <p className="text-xs font-mono text-surface-600 mt-1 leading-relaxed">
            Agent reasoning and findings will appear here when the agent calls{' '}
            <span className="text-surface-400">write_working</span>.
          </p>
        </div>
      )}
    </div>
  )
}
