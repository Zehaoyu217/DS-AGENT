import React from 'react'
import { useChatStore, type TodoItem, type TodoStatus } from '../../lib/store'
import { cn } from '../../lib/utils'

function statusLabel(status: TodoStatus): string {
  switch (status) {
    case 'pending': return '○'
    case 'in_progress': return '◑'
    case 'completed': return '●'
  }
}

function statusClass(status: TodoStatus): string {
  switch (status) {
    case 'pending': return 'text-surface-500'
    case 'in_progress': return 'text-brand-accent'
    case 'completed': return 'text-surface-600 line-through'
  }
}

function TodoRow({ item }: { item: TodoItem }): React.ReactElement {
  return (
    <div className="flex items-start gap-2 py-1.5 border-b border-surface-800/50 last:border-0">
      <span
        className={cn('text-[11px] font-mono mt-px flex-shrink-0', statusClass(item.status))}
        aria-label={item.status}
      >
        {statusLabel(item.status)}
      </span>
      <span
        className={cn(
          'text-[11px] font-mono leading-snug flex-1',
          item.status === 'completed' ? 'text-surface-600 line-through' : 'text-surface-300',
        )}
      >
        {item.content}
      </span>
    </div>
  )
}

export function TodosPanel(): React.ReactElement {
  const todos = useChatStore((s) => s.todos)

  const pending = todos.filter((t) => t.status === 'pending').length
  const inProgress = todos.filter((t) => t.status === 'in_progress').length
  const completed = todos.filter((t) => t.status === 'completed').length

  return (
    <div className="flex flex-col flex-1 min-h-0 p-3">
      <div className="flex items-center justify-between mb-2">
        <p className="text-[10px] font-mono font-semibold tracking-widest text-surface-500 uppercase">
          Tasks
        </p>
        {todos.length > 0 && (
          <span className="text-[9px] font-mono text-surface-600 tracking-widest uppercase">
            {completed}/{todos.length} done
          </span>
        )}
      </div>
      <div className="border-t border-surface-800 mb-3" />
      {todos.length > 0 ? (
        <div className="flex-1 min-h-0 overflow-y-auto">
          {/* in-progress first, then pending, then completed */}
          {[
            ...todos.filter((t) => t.status === 'in_progress'),
            ...todos.filter((t) => t.status === 'pending'),
            ...todos.filter((t) => t.status === 'completed'),
          ].map((item) => (
            <TodoRow key={item.id} item={item} />
          ))}
          {inProgress > 0 && (
            <p className="text-[9px] font-mono text-brand-accent/60 mt-2 tracking-widest uppercase">
              {inProgress} in progress · {pending} pending · {completed} done
            </p>
          )}
        </div>
      ) : (
        <div>
          <p className="text-[10px] font-mono text-surface-600 italic">no tasks yet</p>
          <p className="text-[9px] font-mono text-surface-700 italic mt-1 leading-relaxed">
            agent task list surfaces when the agent uses{' '}
            <span className="text-surface-600 not-italic">todo_write</span>
          </p>
        </div>
      )}
    </div>
  )
}
