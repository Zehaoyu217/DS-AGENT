import { act, fireEvent, render, screen } from '@testing-library/react'
import { useEffect } from 'react'
import { describe, expect, it, vi } from 'vitest'
import {
  CommandRegistryProvider,
  useCommandRegistry,
} from '@/hooks/useCommandRegistry'
import { CommandPalette } from '../CommandPalette'

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
})
