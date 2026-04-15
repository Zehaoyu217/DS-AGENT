import { useEffect, useRef, useState } from 'react'
import { Moon, Sun, SquarePen, ChevronDown } from 'lucide-react'
import * as DropdownMenu from '@radix-ui/react-dropdown-menu'
import { useTheme } from './ThemeProvider'
import { useChatStore } from '@/lib/store'
import { backend } from '@/lib/api-backend'
import type { ModelGroup, UserSettings, DataInfo } from '@/lib/api-backend'
import { ContextBar } from './ContextBar'
import { cn } from '@/lib/utils'

/** Strip the `provider/` prefix from a model ID for compact display. */
function shortModelName(id: string): string {
  const slash = id.lastIndexOf('/')
  return slash !== -1 ? id.slice(slash + 1) : id
}

export function LeftPanel() {
  const { theme, setTheme } = useTheme()
  const settings = useChatStore((s) => s.settings)
  const updateSettings = useChatStore((s) => s.updateSettings)
  const createConversationRemote = useChatStore((s) => s.createConversationRemote)
  const createConversation = useChatStore((s) => s.createConversation)
  const clearToolCallLog = useChatStore((s) => s.clearToolCallLog)
  const clearScratchpad = useChatStore((s) => s.clearScratchpad)
  const clearArtifacts = useChatStore((s) => s.clearArtifacts)
  const conversations = useChatStore((s) => s.conversations)
  const activeConversationId = useChatStore((s) => s.activeConversationId)
  const scratchpad = useChatStore((s) => s.scratchpad)
  const [modelGroups, setModelGroups] = useState<ModelGroup[]>([])
  const [backendSettings, setBackendSettings] = useState<UserSettings | null>(null)
  const [dataInfo, setDataInfo] = useState<DataInfo | null>(null)
  const [confirmNew, setConfirmNew] = useState(false)
  const confirmTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  useEffect(() => {
    // Load backend settings, models, and data info in parallel
    backend.settings
      .get()
      .then((s) => {
        setBackendSettings(s)
        updateSettings({ model: s.model }) // sync Zustand with what backend has
      })
      .catch(() => {})

    backend.models
      .list()
      .then((r) => setModelGroups(r.groups))
      .catch(() => {})

    backend.data
      .info()
      .then((d) => setDataInfo(d))
      .catch(() => {})
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  const isDark = theme !== 'light'
  const activeModel = backendSettings?.model ?? settings.model

  function handleNewSession() {
    const activeConv = conversations.find((c) => c.id === activeConversationId)
    const hasContent = (activeConv?.messages?.length ?? 0) > 0 || scratchpad.length > 0

    if (hasContent && !confirmNew) {
      setConfirmNew(true)
      if (confirmTimerRef.current) clearTimeout(confirmTimerRef.current)
      confirmTimerRef.current = setTimeout(() => setConfirmNew(false), 3000)
      return
    }

    if (confirmTimerRef.current) {
      clearTimeout(confirmTimerRef.current)
      confirmTimerRef.current = null
    }
    setConfirmNew(false)
    clearToolCallLog()
    clearScratchpad()
    clearArtifacts()
    createConversationRemote('New Conversation').catch(() => createConversation())
  }

  function handleCancelNew() {
    if (confirmTimerRef.current) {
      clearTimeout(confirmTimerRef.current)
      confirmTimerRef.current = null
    }
    setConfirmNew(false)
  }

  function handleModelChange(newModel: string) {
    updateSettings({ model: newModel })
    const updated: UserSettings = {
      theme: backendSettings?.theme ?? 'dark',
      model: newModel,
      send_on_enter: backendSettings?.send_on_enter ?? true,
    }
    setBackendSettings(updated)
    backend.settings.put(updated).catch(() => {})
  }

  return (
    <aside
      className="flex flex-col w-full bg-canvas"
      aria-label="Session configuration"
    >
      {/* ── Logo + New Session ────────────────────────────── */}
      <div className="px-4 pt-5 pb-3">
        <div className="flex items-start justify-between mb-1">
          <div className="flex flex-col gap-[2px]">
            <span className="text-[10px] font-mono tracking-[0.3em] text-surface-600 uppercase">
              Analytical
            </span>
            <span className="text-[11px] font-mono font-bold tracking-[0.12em] text-surface-100 uppercase">
              Agent
            </span>
          </div>
          {confirmNew ? (
            <div className="flex items-center gap-1">
              <button
                onClick={handleNewSession}
                aria-label="Confirm new session"
                className={cn(
                  'px-2 py-1 rounded',
                  'text-[10px] font-mono text-error',
                  'hover:bg-error-bg transition-colors',
                )}
              >
                confirm
              </button>
              <button
                onClick={handleCancelNew}
                aria-label="Cancel new session"
                className={cn(
                  'px-2 py-1 rounded',
                  'text-[10px] font-mono text-surface-600',
                  'hover:text-surface-300 hover:bg-surface-800/60',
                  'transition-colors',
                )}
              >
                cancel
              </button>
            </div>
          ) : (
            <button
              onClick={handleNewSession}
              aria-label="New session"
              className={cn(
                'flex items-center gap-1.5 px-2 py-1 rounded',
                'text-[10px] font-mono text-surface-400',
                'hover:text-surface-100 hover:bg-surface-800/60',
                'transition-colors',
              )}
            >
              <SquarePen className="w-3 h-3 flex-shrink-0" aria-hidden="true" />
              <span className="tracking-wide">New</span>
            </button>
          )}
        </div>
        {dataInfo && (
          <div className="flex items-center gap-1.5 mt-2">
            <span className={cn(
              'w-1.5 h-1.5 rounded-full flex-shrink-0',
              dataInfo.tables.length > 0 ? 'bg-brand-accent' : 'bg-surface-700',
            )} />
            <span className="text-[10px] font-mono text-surface-600 uppercase tracking-[0.15em] truncate">
              {dataInfo.db_name}
              {dataInfo.tables.length > 0 && (
                <span className="text-surface-700"> · {dataInfo.tables.length} tables</span>
              )}
            </span>
          </div>
        )}
      </div>

      {/* ── Controls ──────────────────────────────────────── */}
      <div className="px-4 py-3 space-y-3.5">
        {/* Model selector */}
        <div>
          <div className="text-[10px] font-mono font-semibold tracking-[0.18em] text-surface-600 uppercase mb-1.5">
            Model
          </div>
          <DropdownMenu.Root>
            <DropdownMenu.Trigger asChild>
              <button
                aria-label="Select LLM model"
                className={cn(
                  'w-full flex items-center justify-between gap-1 px-2 py-1.5',
                  'text-[11px] font-mono text-surface-300 text-left truncate',
                  'bg-surface-900 border border-surface-700/60 rounded',
                  'hover:border-surface-600 hover:text-surface-200',
                  'focus:outline-none focus:ring-1 focus:ring-brand-accent/60',
                  'transition-colors cursor-pointer',
                )}
              >
                <span className="truncate flex-1" title={activeModel}>{shortModelName(activeModel)}</span>
                <ChevronDown className="w-3 h-3 text-surface-600 flex-shrink-0" aria-hidden />
              </button>
            </DropdownMenu.Trigger>

            <DropdownMenu.Portal>
              <DropdownMenu.Content
                sideOffset={4}
                align="start"
                className={cn(
                  'z-50 w-48 max-h-72 overflow-y-auto',
                  'bg-surface-900 border border-surface-700/60',
                  'py-1 shadow-2xl',
                )}
              >
                {modelGroups.length > 0 ? (
                  modelGroups.map((group) => (
                    <DropdownMenu.Group key={group.provider}>
                      <DropdownMenu.Label className="px-3 pt-2 pb-1 text-[10px] font-mono font-bold tracking-[0.2em] text-surface-700 uppercase">
                        {group.available ? group.label : `${group.label} (pending)`}
                      </DropdownMenu.Label>
                      {group.models.map((m) => (
                        <DropdownMenu.Item
                          key={m.id}
                          disabled={!group.available}
                          onSelect={() => handleModelChange(m.id)}
                          className={cn(
                            'flex items-center gap-2 px-3 py-1.5 cursor-pointer outline-none select-none',
                            'text-[11px] font-mono transition-colors',
                            activeModel === m.id
                              ? 'text-brand-400 bg-surface-800'
                              : 'text-surface-400 data-[highlighted]:text-surface-200 data-[highlighted]:bg-surface-800',
                            !group.available && 'opacity-40 cursor-not-allowed pointer-events-none',
                          )}
                        >
                          <span className={cn('w-3 text-[9px] text-brand-400 flex-shrink-0', activeModel !== m.id && 'invisible')}>
                            ✓
                          </span>
                          <span className="truncate">{m.label}</span>
                        </DropdownMenu.Item>
                      ))}
                    </DropdownMenu.Group>
                  ))
                ) : (
                  <DropdownMenu.Item
                    className="px-3 py-1.5 text-[11px] font-mono text-surface-400 outline-none"
                    disabled
                  >
                    {activeModel}
                  </DropdownMenu.Item>
                )}
              </DropdownMenu.Content>
            </DropdownMenu.Portal>
          </DropdownMenu.Root>
        </div>

        {/* Theme toggle — icon-only, low prominence */}
        <div className="flex justify-end">
          <button
            onClick={() => setTheme(isDark ? 'light' : 'dark')}
            aria-label={`Switch to ${isDark ? 'light' : 'dark'} theme`}
            className="p-1 rounded text-surface-700 hover:text-surface-400 hover:bg-surface-800/40 transition-colors"
          >
            {isDark ? (
              <Moon className="w-3 h-3" aria-hidden="true" />
            ) : (
              <Sun className="w-3 h-3" aria-hidden="true" />
            )}
          </button>
        </div>
      </div>

      {/* Spacer */}
      <div className="flex-1" />

      {/* ── Context bar ───────────────────────────────────── */}
      <ContextBar />
    </aside>
  )
}
