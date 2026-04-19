import { describe, it, expect, beforeEach } from 'vitest'
import { useChatStore } from '@/lib/store'

describe('updateConversationTitle', () => {
  beforeEach(() => {
    useChatStore.setState({ conversations: [], activeConversationId: null })
  })

  it('trims and persists', () => {
    const id = useChatStore.getState().createConversation()
    useChatStore.getState().updateConversationTitle(id, '  new title  ')
    const conv = useChatStore.getState().conversations.find((c) => c.id === id)!
    expect(conv.title).toBe('new title')
  })

  it('caps at 200 chars', () => {
    const id = useChatStore.getState().createConversation()
    useChatStore.getState().updateConversationTitle(id, 'a'.repeat(300))
    const conv = useChatStore.getState().conversations.find((c) => c.id === id)!
    expect(conv.title.length).toBe(200)
  })

  it('ignores empty strings (keeps previous)', () => {
    const id = useChatStore.getState().createConversation()
    useChatStore.getState().updateConversationTitle(id, 'Kept')
    useChatStore.getState().updateConversationTitle(id, '   ')
    const conv = useChatStore.getState().conversations.find((c) => c.id === id)!
    expect(conv.title).toBe('Kept')
  })
})
