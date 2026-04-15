import { useEffect, useState } from 'react'
import { useChatStore } from '@/lib/store'
import { LeftPanel } from '@/components/layout/LeftPanel'
import { ChatWindow } from '@/components/chat/ChatWindow'
import { ChatInput } from '@/components/chat/ChatInput'
import { SessionRightPanel } from '@/components/right-panel/SessionRightPanel'
import { ResizeHandle } from '@/components/layout/ResizeHandle'
import { useResizablePanel } from '@/hooks/useResizablePanel'
import { SessionDevToolsPanel } from '@/components/session/SessionDevToolsPanel'
import { cn } from '@/lib/utils'

type MiddleTab = 'conversation' | 'devtools'

export function SessionLayout() {
  const conversations = useChatStore((s) => s.conversations)
  const activeConversationId = useChatStore((s) => s.activeConversationId)
  const createConversation = useChatStore((s) => s.createConversation)
  const createConversationRemote = useChatStore((s) => s.createConversationRemote)

  const left = useResizablePanel(192, 140, 300, 'horizontal')
  const right = useResizablePanel(320, 240, 520, 'horizontal', true)

  const [middleTab, setMiddleTab] = useState<MiddleTab>('conversation')

  // Active conversation drives session-scoped telemetry.
  const activeConversation = conversations.find((c) => c.id === activeConversationId)
  const activeSessionId = activeConversation?.sessionId ?? null

  // Ensure there is always an active conversation so the input is usable.
  // Remote-first: server id becomes source of truth for appendTurn calls.
  useEffect(() => {
    if (conversations.length === 0) {
      createConversationRemote('New Conversation').catch(() => {
        createConversation()
      })
    } else if (
      !activeConversationId ||
      !conversations.some((c) => c.id === activeConversationId)
    ) {
      useChatStore.getState().setActiveConversation(conversations[0].id)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <div className="flex h-full bg-canvas text-surface-100 overflow-hidden">
      {/* Left panel — resizable, hidden on narrow viewports */}
      <div style={{ width: left.size, minWidth: left.size }} className="hidden md:flex flex-shrink-0">
        <LeftPanel />
      </div>

      <ResizeHandle onMouseDown={left.onMouseDown} direction="horizontal" className="hidden md:flex" />

      <main
        id="main-content"
        className="flex flex-col flex-1 min-w-0 min-h-0"
        aria-label="Chat"
      >
        {/* ── Middle tab bar: Conversation | DevTools ─────────────── */}
        <div
          role="tablist"
          aria-label="Middle panel view"
          className="flex items-center h-9 shrink-0 border-b border-surface-800 bg-surface-900/30"
        >
          {(['conversation', 'devtools'] as MiddleTab[]).map((tab) => {
            const isActive = middleTab === tab
            const label = tab === 'conversation' ? 'Conversation' : 'DevTools'
            const hasSession = tab !== 'devtools' || activeSessionId !== null
            return (
              <button
                key={tab}
                role="tab"
                aria-selected={isActive}
                onClick={() => setMiddleTab(tab)}
                className={cn(
                  'flex items-center gap-2 px-4 h-full',
                  'text-[10px] font-mono font-semibold tracking-[0.22em] uppercase',
                  'border-b transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-brand-accent/50',
                  isActive
                    ? 'border-brand-accent/80 text-surface-200'
                    : 'border-transparent text-surface-600 hover:text-surface-400',
                )}
              >
                {label}
                {tab === 'devtools' && !hasSession && (
                  <span
                    className="w-1 h-1 rounded-full bg-surface-700 flex-shrink-0"
                    aria-label="no active session"
                  />
                )}
                {tab === 'devtools' && hasSession && (
                  <span
                    className="w-1 h-1 rounded-full bg-brand-accent/70 flex-shrink-0"
                    aria-label="session ready"
                  />
                )}
              </button>
            )
          })}
          <div className="flex-1" />
          {activeSessionId && middleTab === 'devtools' && (
            <span className="text-[9px] font-mono text-surface-700 tracking-widest uppercase pr-4">
              {activeSessionId.slice(0, 12)}
            </span>
          )}
        </div>

        {/* ── Conversation tab ─────────────────────────────────── */}
        {middleTab === 'conversation' &&
          (activeConversationId ? (
            <>
              <ChatWindow conversationId={activeConversationId} />
              <ChatInput conversationId={activeConversationId} />
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center">
              <span className="text-[11px] font-mono text-surface-700 tracking-widest uppercase">
                initializing session...
              </span>
            </div>
          ))}

        {/* ── DevTools tab — session-scoped telemetry ──────────── */}
        {middleTab === 'devtools' && (
          <div className="flex-1 min-h-0 overflow-hidden">
            <SessionDevToolsPanel sessionId={activeSessionId} />
          </div>
        )}
      </main>

      <ResizeHandle onMouseDown={right.onMouseDown} direction="horizontal" className="hidden md:flex" />

      {/* Right panel — resizable, hidden on narrow viewports */}
      <div style={{ width: right.size, minWidth: right.size }} className="hidden md:flex flex-shrink-0">
        <SessionRightPanel />
      </div>
    </div>
  )
}
