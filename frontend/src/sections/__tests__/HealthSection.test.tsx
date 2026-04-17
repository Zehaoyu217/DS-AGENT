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
    ;(global.fetch as ReturnType<typeof vi.fn>).mockImplementation(
      (url: string) => {
        if (url.includes('autofix.json')) {
          return Promise.resolve({ ok: false, json: () => Promise.resolve({}) })
        }
        return Promise.resolve({
          ok: true,
          text: () => Promise.resolve('# Hello health\n\nbody'),
        })
      }
    )
    render(<HealthSection />)
    await waitFor(() => {
      expect(screen.getByText(/Hello health/)).toBeInTheDocument()
    })
  })

  it('shows empty state when fetch returns 404', async () => {
    ;(global.fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
      ok: false,
      status: 404,
      text: () => Promise.resolve(''),
      json: () => Promise.resolve({}),
    })
    render(<HealthSection />)
    await waitFor(() => {
      expect(screen.getByText(/No integrity report yet/i)).toBeInTheDocument()
    })
  })

  it('renders Autofix tile when autofix.json is available', async () => {
    ;(global.fetch as ReturnType<typeof vi.fn>).mockImplementation(
      (url: string) => {
        if (url.includes('autofix.json')) {
          return Promise.resolve({
            ok: true,
            json: () =>
              Promise.resolve({
                date: '2026-04-17',
                mode: 'dry-run',
                fix_classes_run: ['health_dashboard_refresh'],
                fix_classes_skipped: [],
                pr_results: {},
              }),
          })
        }
        return Promise.resolve({
          ok: true,
          text: () => Promise.resolve('# Health\n'),
        })
      }
    )
    render(<HealthSection />)
    await waitFor(() => {
      expect(screen.getByText(/AUTOFIX/i)).toBeInTheDocument()
    })
    expect(screen.getByText(/dry-run/)).toBeInTheDocument()
    expect(screen.getByText(/2026-04-17/)).toBeInTheDocument()
  })
})
