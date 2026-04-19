import { useChatStore } from '@/lib/store'
import { ContextBudgetBar } from './context/ContextBudgetBar'
import { LayerBars } from './context/LayerBars'
import { LoadedFileChip } from './context/LoadedFileChip'
import { AttachedFileList } from './context/AttachedFileList'
import { TodoList } from './context/TodoList'
import { ScratchpadPreview } from './context/ScratchpadPreview'

export function DockContext() {
  const conversationId = useChatStore((s) => s.activeConversationId)
  const conv = useChatStore((s) => s.conversations.find((c) => c.id === conversationId))
  const todos = useChatStore((s) => s.todos)
  const scratchpad = useChatStore((s) => s.scratchpad)
  const unloadFile = useChatStore((s) => s.unloadFile)

  if (!conv?.context) {
    return (
      <div className="flex h-full flex-col gap-3 p-4">
        <div className="label-cap">Context snapshot</div>
        <div className="stripe-ph h-40" aria-label="No context snapshot yet">
          No context snapshot yet
        </div>
      </div>
    )
  }

  const { layers, loadedFiles, totalTokens, budgetTokens } = conv.context

  return (
    <div className="flex h-full flex-col gap-4 overflow-y-auto p-4">
      <div>
        <div className="label-cap mb-2">Budget</div>
        <ContextBudgetBar totalTokens={totalTokens} budgetTokens={budgetTokens} />
      </div>
      {layers.length > 0 && (
        <div>
          <div className="label-cap mb-2">Layers</div>
          <LayerBars layers={layers} />
        </div>
      )}
      {loadedFiles.length > 0 && (
        <div>
          <div className="label-cap mb-2">Loaded files</div>
          <div className="flex flex-col gap-1">
            {loadedFiles.map((f) => (
              <LoadedFileChip key={f.id} file={f} onUnload={(id) => unloadFile(conv.id, id)} />
            ))}
          </div>
        </div>
      )}
      {(conv.attachedFiles?.length ?? 0) > 0 && (
        <div>
          <div className="label-cap mb-2">Attached</div>
          <AttachedFileList files={conv.attachedFiles ?? []} />
        </div>
      )}
      <div>
        <div className="label-cap mb-2">Todos</div>
        <TodoList todos={todos} />
      </div>
      <div>
        <div className="label-cap mb-2">Scratchpad</div>
        <ScratchpadPreview content={scratchpad} />
      </div>
    </div>
  )
}
