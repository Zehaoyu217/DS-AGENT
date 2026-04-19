import { describe, it, expect, beforeEach } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { TitleEditor } from '../TitleEditor'
import { useChatStore } from '@/lib/store'

describe('TitleEditor', () => {
  beforeEach(() => {
    useChatStore.setState({ conversations: [], activeConversationId: null })
  })

  it('enters edit mode on click', () => {
    const id = useChatStore.getState().createConversation()
    useChatStore.getState().updateConversationTitle(id, 'Churn')
    render(<TitleEditor conversationId={id} />)
    fireEvent.click(screen.getByText('Churn'))
    expect(screen.getByRole('textbox')).toHaveValue('Churn')
  })

  it('commits on Enter', () => {
    const id = useChatStore.getState().createConversation()
    useChatStore.getState().updateConversationTitle(id, 'Old')
    render(<TitleEditor conversationId={id} />)
    fireEvent.click(screen.getByText('Old'))
    const input = screen.getByRole('textbox')
    fireEvent.change(input, { target: { value: 'New' } })
    fireEvent.keyDown(input, { key: 'Enter' })
    expect(useChatStore.getState().conversations[0].title).toBe('New')
  })

  it('reverts on Esc', () => {
    const id = useChatStore.getState().createConversation()
    useChatStore.getState().updateConversationTitle(id, 'Keep')
    render(<TitleEditor conversationId={id} />)
    fireEvent.click(screen.getByText('Keep'))
    const input = screen.getByRole('textbox')
    fireEvent.change(input, { target: { value: 'Lose' } })
    fireEvent.keyDown(input, { key: 'Escape' })
    expect(useChatStore.getState().conversations[0].title).toBe('Keep')
  })
})
