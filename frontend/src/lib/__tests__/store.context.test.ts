import { describe, it, expect, beforeEach } from 'vitest'
import { useChatStore } from '@/lib/store'

describe('setConversationContext', () => {
  beforeEach(() => {
    useChatStore.setState({ conversations: [], activeConversationId: null })
  })

  it('attaches ContextShape to the conversation', () => {
    const id = useChatStore.getState().createConversation()
    useChatStore.getState().setConversationContext(id, {
      layers: [{ id: 'sys', label: 'system', tokens: 8_000, maxTokens: 16_000 }],
      loadedFiles: [],
      scratchpad: '',
      totalTokens: 8_000,
      budgetTokens: 200_000,
    })
    const conv = useChatStore.getState().conversations.find((c) => c.id === id)!
    expect(conv.context?.totalTokens).toBe(8_000)
    expect(conv.context?.layers[0].label).toBe('system')
  })

  it('unloadFile removes the file by id', () => {
    const id = useChatStore.getState().createConversation()
    useChatStore.getState().setConversationContext(id, {
      layers: [],
      loadedFiles: [
        { id: 'a', name: 'x.csv', size: 1, kind: 'csv' },
        { id: 'b', name: 'y.csv', size: 1, kind: 'csv' },
      ],
      scratchpad: '',
      totalTokens: 0,
      budgetTokens: 200_000,
    })
    useChatStore.getState().unloadFile(id, 'a')
    const conv = useChatStore.getState().conversations.find((c) => c.id === id)!
    expect(conv.context?.loadedFiles.map((f) => f.id)).toEqual(['b'])
  })
})
