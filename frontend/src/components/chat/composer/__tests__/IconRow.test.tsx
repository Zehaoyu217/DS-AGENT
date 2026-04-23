import { describe, it, expect, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import { IconRow } from '../IconRow'
import { useChatStore } from '@/lib/store'

describe('IconRow', () => {
  beforeEach(() => {
    useChatStore.setState({ conversations: [], activeConversationId: null })
  })

  it('renders only the upload button (mention/skill/voice were removed)', () => {
    const id = useChatStore.getState().createConversation()
    render(<IconRow conversationId={id} />)
    expect(screen.getByRole('button', { name: /upload/i })).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /mention/i })).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /skill/i })).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /voice/i })).not.toBeInTheDocument()
  })
})
