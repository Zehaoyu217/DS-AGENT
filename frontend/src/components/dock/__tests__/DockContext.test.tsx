import { describe, it, expect, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import { DockContext } from '../DockContext'
import { useChatStore } from '@/lib/store'

describe('DockContext', () => {
  beforeEach(() => {
    useChatStore.setState({ conversations: [], activeConversationId: null } as never)
  })

  it('shows empty state when no context snapshot yet', () => {
    const id = useChatStore.getState().createConversation()
    useChatStore.setState({ activeConversationId: id } as never)
    render(<DockContext />)
    expect(screen.getByText(/no context snapshot yet/i)).toBeInTheDocument()
  })

  it('renders budget bar + layers when context present', () => {
    const id = useChatStore.getState().createConversation()
    useChatStore.getState().setConversationContext(id, {
      layers: [{ id: '0', label: 'system', tokens: 12_000, maxTokens: 16_000 }],
      loadedFiles: [{ id: 'a', name: 'x.csv', size: 1024, kind: 'csv' }],
      scratchpad: '',
      totalTokens: 12_000,
      budgetTokens: 200_000,
    })
    useChatStore.setState({ activeConversationId: id } as never)
    render(<DockContext />)
    expect(screen.getByLabelText(/context budget/i)).toBeInTheDocument()
    expect(screen.getByText('system')).toBeInTheDocument()
    expect(screen.getByText('x.csv')).toBeInTheDocument()
  })
})
