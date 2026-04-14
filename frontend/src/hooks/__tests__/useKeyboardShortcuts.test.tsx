import { act, fireEvent, render } from '@testing-library/react'
import { useEffect } from 'react'
import { describe, expect, it, vi } from 'vitest'
import {
  CommandRegistryProvider,
  useCommandRegistry,
} from '@/hooks/useCommandRegistry'
import { useKeyboardShortcuts } from '@/hooks/useKeyboardShortcuts'

interface TestShortcutProps {
  action: () => void
}

function TestShortcut({ action }: TestShortcutProps) {
  const { registerCommand } = useCommandRegistry()
  useKeyboardShortcuts()

  useEffect(() => {
    return registerCommand({
      id: 'test.open-palette',
      keys: ['mod+k'],
      label: 'Open palette (test)',
      description: 'Test',
      category: 'Navigation',
      action,
      global: true,
    })
  }, [registerCommand, action])

  return <div data-testid="host" />
}

describe('useKeyboardShortcuts', () => {
  it('fires the registered command when mod+k is pressed', async () => {
    const action = vi.fn()

    render(
      <CommandRegistryProvider>
        <TestShortcut action={action} />
      </CommandRegistryProvider>,
    )

    // Allow commands to register
    await act(async () => {
      await Promise.resolve()
    })

    act(() => {
      // On macOS matchesEvent treats `mod` as metaKey; on other platforms as ctrlKey.
      // Fire both — the one matching the host will trigger. Extras are no-ops.
      fireEvent.keyDown(document, { key: 'k', metaKey: true })
      fireEvent.keyDown(document, { key: 'k', ctrlKey: true })
    })

    expect(action).toHaveBeenCalledTimes(1)
  })

  it('does not fire the command for unrelated keystrokes', async () => {
    const action = vi.fn()

    render(
      <CommandRegistryProvider>
        <TestShortcut action={action} />
      </CommandRegistryProvider>,
    )

    await act(async () => {
      await Promise.resolve()
    })

    act(() => {
      fireEvent.keyDown(document, { key: 'j', metaKey: true })
    })

    expect(action).not.toHaveBeenCalled()
  })
})
