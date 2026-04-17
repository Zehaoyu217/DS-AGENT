import { render, screen, waitFor } from '@testing-library/react'
import { describe, expect, it, vi, beforeEach, afterEach } from 'vitest'
import { HealthSection } from '../HealthSection'

describe('HealthSection', () => {
  const originalFetch = global.fetch

  beforeEach(() => {
    global.fetch = vi.fn()
  })

  afterEach(() => {
    global.fetch = originalFetch
  })

  it('renders the markdown when fetch succeeds', async () => {
    ;(global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      text: () => Promise.resolve('# Hello health\n\nbody'),
    })
    render(<HealthSection />)
    await waitFor(() => {
      expect(screen.getByText(/Hello health/)).toBeInTheDocument()
    })
  })

  it('shows empty state when fetch returns 404', async () => {
    ;(global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: false,
      status: 404,
      text: () => Promise.resolve(''),
    })
    render(<HealthSection />)
    await waitFor(() => {
      expect(screen.getByText(/No integrity report yet/i)).toBeInTheDocument()
    })
  })
})
