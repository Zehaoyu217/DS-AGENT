import { describe, it, expect, beforeEach } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { ExportMenu } from '../ExportMenu'
import { useChatStore } from '@/lib/store'

describe('ExportMenu', () => {
  beforeEach(() => {
    useChatStore.setState({ conversations: [], activeConversationId: null })
  })

  it('opens menu and exposes .md/.json/.html options', () => {
    const id = useChatStore.getState().createConversation()
    render(<ExportMenu conversationId={id} />)
    fireEvent.click(screen.getByRole('button', { name: /export/i }))
    expect(screen.getByText(/markdown/i)).toBeInTheDocument()
    expect(screen.getByText(/json/i)).toBeInTheDocument()
    expect(screen.getByText(/html/i)).toBeInTheDocument()
  })
})
