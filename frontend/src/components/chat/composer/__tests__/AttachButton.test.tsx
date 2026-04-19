import { describe, it, expect, beforeEach } from 'vitest'
import { render, fireEvent } from '@testing-library/react'
import { AttachButton } from '../AttachButton'
import { useChatStore } from '@/lib/store'

describe('AttachButton', () => {
  beforeEach(() => {
    useChatStore.setState({ conversations: [], activeConversationId: null })
  })

  it('opens file picker and adds attached file on success', async () => {
    const id = useChatStore.getState().createConversation()
    const { container } = render(<AttachButton conversationId={id} />)
    const input = container.querySelector('input[type="file"]')!
    const file = new File(['hi'], 'note.md', { type: 'text/markdown' })
    Object.defineProperty(input, 'files', { value: [file] })
    fireEvent.change(input)
    const conv = useChatStore.getState().conversations.find((c) => c.id === id)!
    expect(conv.attachedFiles?.[0].name).toBe('note.md')
  })
})
