import { describe, it, expect, beforeEach } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { AttachedFilesPreview } from '../AttachedFilesPreview'
import { useChatStore } from '@/lib/store'

describe('AttachedFilesPreview', () => {
  beforeEach(() => {
    useChatStore.setState({ conversations: [], activeConversationId: null })
  })

  it('renders a chip per attached file', () => {
    const id = useChatStore.getState().createConversation()
    useChatStore
      .getState()
      .addAttachedFile(id, { id: 'a', name: 'q.csv', size: 1024, mimeType: 'text/csv' })
    useChatStore
      .getState()
      .addAttachedFile(id, { id: 'b', name: 'r.md', size: 512, mimeType: 'text/markdown' })
    render(<AttachedFilesPreview conversationId={id} />)
    expect(screen.getByText('q.csv')).toBeInTheDocument()
    expect(screen.getByText('r.md')).toBeInTheDocument()
  })

  it('removes on X click', () => {
    const id = useChatStore.getState().createConversation()
    useChatStore
      .getState()
      .addAttachedFile(id, { id: 'a', name: 'q.csv', size: 1024, mimeType: 'text/csv' })
    render(<AttachedFilesPreview conversationId={id} />)
    fireEvent.click(screen.getByRole('button', { name: /remove q\.csv/i }))
    const conv = useChatStore.getState().conversations.find((c) => c.id === id)!
    expect(conv.attachedFiles).toEqual([])
  })
})
