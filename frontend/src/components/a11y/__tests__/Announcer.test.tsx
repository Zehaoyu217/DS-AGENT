import { act, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { AnnouncerProvider, useAnnouncer } from '../Announcer'

function PoliteAnnouncer({ message }: { message: string }) {
  const { announce } = useAnnouncer()
  return (
    <button
      type="button"
      onClick={() => announce(message)}
      aria-label={`announce ${message}`}
    />
  )
}

function AssertiveAnnouncer({ message }: { message: string }) {
  const { announce } = useAnnouncer()
  return (
    <button
      type="button"
      onClick={() => announce(message, 'assertive')}
      aria-label={`announce urgent ${message}`}
    />
  )
}

describe('<AnnouncerProvider>', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('renders a polite message into the polite live region', () => {
    render(
      <AnnouncerProvider>
        <PoliteAnnouncer message="hello world" />
      </AnnouncerProvider>,
    )

    act(() => {
      screen.getByLabelText('announce hello world').click()
    })

    act(() => {
      vi.advanceTimersByTime(60)
    })

    const polite = document.querySelector('[aria-live="polite"]')
    const assertive = document.querySelector('[aria-live="assertive"]')
    expect(polite?.textContent).toBe('hello world')
    expect(assertive?.textContent).toBe('')
  })

  it('renders an assertive message into the assertive live region', () => {
    render(
      <AnnouncerProvider>
        <AssertiveAnnouncer message="boom" />
      </AnnouncerProvider>,
    )

    act(() => {
      screen.getByLabelText('announce urgent boom').click()
    })

    act(() => {
      vi.advanceTimersByTime(60)
    })

    const polite = document.querySelector('[aria-live="polite"]')
    const assertive = document.querySelector('[aria-live="assertive"]')
    expect(assertive?.textContent).toBe('boom')
    expect(polite?.textContent).toBe('')
  })

  it('throws when useAnnouncer is called outside the provider', () => {
    // Silence the React error boundary noise for this expected throw
    const errSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
    const Broken = () => {
      useAnnouncer()
      return null
    }
    expect(() => render(<Broken />)).toThrow(/AnnouncerProvider/)
    errSpy.mockRestore()
  })
})
