import { act, fireEvent, render, screen } from '@testing-library/react'
import { useEffect } from 'react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import {
  CommandRegistryProvider,
  useCommandRegistry,
} from '@/hooks/useCommandRegistry'
import { CommandPalette } from '../CommandPalette'
import { useChatStore, type Conversation } from '@/lib/store'

function makeConv(id: string, title: string, frozenAt: number | null = null): Conversation {
  const t = Date.now()
  return {
    id,
    title,
    messages: [],
    createdAt: t,
    updatedAt: t,
    pinned: false,
    frozenAt,
  }
}

beforeEach(() => {
  useChatStore.setState({
    conversations: [],
    activeConversationId: null,
  })
})

interface HarnessProps {
  action: () => void
}

function Harness({ action }: HarnessProps) {
  const { registerCommand, openPalette } = useCommandRegistry()

  useEffect(() => {
    return registerCommand({
      id: 'test.create-chat',
      keys: ['mod+n'],
      label: 'Create new chat',
      description: 'Start a fresh conversation',
      category: 'Chat',
      action,
    })
  }, [registerCommand, action])

  return (
    <button type="button" onClick={openPalette}>
      open palette
    </button>
  )
}

describe('<CommandPalette>', () => {
  it('opens on command, lists the registered command, and runs it on Enter', async () => {
    const action = vi.fn()

    render(
      <CommandRegistryProvider>
        <Harness action={action} />
        <CommandPalette />
      </CommandRegistryProvider>,
    )

    // Let the registerCommand effect flush before opening.
    await act(async () => {
      await Promise.resolve()
    })

    // Open the palette
    act(() => {
      screen.getByText('open palette').click()
    })

    // Let focus + layout effects run
    await act(async () => {
      await Promise.resolve()
    })

    // Radix Dialog portals — query whole document
    expect(document.body.textContent).toContain('Create new chat')

    // Press Enter on the dialog content. Since the input auto-focuses,
    // fire the key event from document-level via the input that was focused.
    const input = document.querySelector<HTMLInputElement>('#command-palette-input')
    expect(input).not.toBeNull()

    act(() => {
      fireEvent.keyDown(input!, { key: 'Enter' })
    })

    expect(action).toHaveBeenCalledTimes(1)
  })

  it('shows Conversations group with non-frozen conversations only', async () => {
    useChatStore.setState({
      conversations: [
        makeConv('a', 'Alpha'),
        makeConv('b', 'Bravo', Date.now()),
        makeConv('c', 'Charlie'),
      ],
      activeConversationId: null,
    })

    render(
      <CommandRegistryProvider>
        <Harness action={vi.fn()} />
        <CommandPalette />
      </CommandRegistryProvider>,
    )
    await act(async () => {
      await Promise.resolve()
    })
    act(() => {
      screen.getByText('open palette').click()
    })
    await act(async () => {
      await Promise.resolve()
    })

    expect(document.body.textContent).toContain('Conversations')
    expect(document.body.textContent).toContain('Alpha')
    expect(document.body.textContent).toContain('Charlie')
    expect(document.body.textContent).not.toContain('Bravo')
  })

  it('shows This conversation group only when a conversation is active; hides Freeze when frozen', async () => {
    useChatStore.setState({
      conversations: [makeConv('a', 'Alpha', Date.now())],
      activeConversationId: 'a',
    })

    render(
      <CommandRegistryProvider>
        <Harness action={vi.fn()} />
        <CommandPalette />
      </CommandRegistryProvider>,
    )
    await act(async () => {
      await Promise.resolve()
    })
    act(() => {
      screen.getByText('open palette').click()
    })
    await act(async () => {
      await Promise.resolve()
    })

    expect(document.body.textContent).toContain('This conversation')
    expect(document.body.textContent).toContain('Pin conversation')
    // Freeze hidden when already frozen.
    expect(document.body.textContent).not.toContain('Freeze conversation')
    expect(document.body.textContent).toContain('Duplicate conversation')
  })
})
