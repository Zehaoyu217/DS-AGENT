import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { MoreMenu } from '../MoreMenu'
import { useChatStore } from '@/lib/store'

describe('MoreMenu', () => {
  beforeEach(() => {
    useChatStore.setState({ conversations: [], activeConversationId: null })
  })

  it('opens menu and deletes conversation', () => {
    const id = useChatStore.getState().createConversation()
    render(<MoreMenu conversationId={id} onRename={() => {}} />)
    fireEvent.click(screen.getByRole('button', { name: /more/i }))
    fireEvent.click(screen.getByText(/delete/i))
    expect(useChatStore.getState().conversations.length).toBe(0)
  })

  it('fires onRename', () => {
    const id = useChatStore.getState().createConversation()
    const spy = vi.fn()
    render(<MoreMenu conversationId={id} onRename={spy} />)
    fireEvent.click(screen.getByRole('button', { name: /more/i }))
    fireEvent.click(screen.getByText(/rename/i))
    expect(spy).toHaveBeenCalled()
  })
})
