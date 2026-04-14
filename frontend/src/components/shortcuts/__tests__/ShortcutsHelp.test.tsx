import { act, render, screen } from '@testing-library/react'
import { useEffect } from 'react'
import { describe, expect, it } from 'vitest'
import {
  CommandRegistryProvider,
  useCommandRegistry,
} from '@/hooks/useCommandRegistry'
import { ShortcutsHelp } from '../ShortcutsHelp'

function Harness() {
  const { registerCommand, openHelp } = useCommandRegistry()

  useEffect(() => {
    const disposers = [
      registerCommand({
        id: 'test.toggle-sidebar',
        keys: ['mod+b'],
        label: 'Toggle sidebar',
        description: 'Show or hide the sidebar',
        category: 'View',
        action: () => {},
      }),
      registerCommand({
        id: 'test.new-conversation',
        keys: ['mod+n'],
        label: 'New conversation',
        description: 'Start a new chat',
        category: 'Chat',
        action: () => {},
      }),
    ]
    return () => {
      for (const dispose of disposers) dispose()
    }
  }, [registerCommand])

  return (
    <button type="button" onClick={openHelp}>
      open help
    </button>
  )
}

describe('<ShortcutsHelp>', () => {
  it('renders shortcuts grouped by category when opened', async () => {
    render(
      <CommandRegistryProvider>
        <Harness />
        <ShortcutsHelp />
      </CommandRegistryProvider>,
    )

    await act(async () => {
      await Promise.resolve()
    })

    act(() => {
      screen.getByText('open help').click()
    })

    await act(async () => {
      await Promise.resolve()
    })

    const heading = document.querySelector('h2, [role="heading"]')
    expect(heading).not.toBeNull()
    expect(document.body.textContent).toContain('Keyboard Shortcuts')

    // Category headers appear (rendered as <h3>)
    const categoryHeadings = Array.from(document.querySelectorAll('h3')).map((el) =>
      el.textContent?.trim(),
    )
    expect(categoryHeadings).toEqual(expect.arrayContaining(['Chat', 'View']))

    // Both registered commands are visible
    expect(document.body.textContent).toContain('Toggle sidebar')
    expect(document.body.textContent).toContain('New conversation')
  })
})
