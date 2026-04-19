import { describe, it, expect, beforeEach } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { ProgressToggle } from '../ProgressToggle'
import { useUiStore } from '@/lib/ui-store'

describe('ProgressToggle', () => {
  beforeEach(() => {
    useUiStore.setState({ ...useUiStore.getState(), dockOpen: false })
  })

  it('shows pulse dot + opens dock on click', () => {
    render(<ProgressToggle />)
    fireEvent.click(screen.getByRole('button', { name: /progress/i }))
    expect(useUiStore.getState().dockOpen).toBe(true)
  })

  it('renders null when dockOpen is true', () => {
    useUiStore.setState({ ...useUiStore.getState(), dockOpen: true })
    const { container } = render(<ProgressToggle />)
    expect(container.firstChild).toBeNull()
  })
})
