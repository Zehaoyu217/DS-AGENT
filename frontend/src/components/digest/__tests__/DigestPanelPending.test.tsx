import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { DigestPanel } from '../DigestPanel'
import { useDigestStore } from '@/lib/digest-store'

function seedStore(partial: Partial<ReturnType<typeof useDigestStore.getState>>) {
  useDigestStore.setState({
    date: '2026-04-18',
    entries: [],
    unread: 0,
    loading: false,
    error: null,
    pending: [],
    pendingLoading: false,
    ...partial,
  })
}

beforeEach(() => {
  global.fetch = vi.fn(async (url: string | URL | Request) => {
    const u = url.toString()
    if (u.endsWith('/api/sb/digest/today')) {
      return new Response(
        JSON.stringify({ ok: true, date: '2026-04-18', entries: [], unread: 0 }),
        { status: 200 },
      )
    }
    if (u.endsWith('/api/sb/digest/pending')) {
      return new Response(
        JSON.stringify({
          ok: true,
          count: 1,
          proposals: [
            {
              id: 'pend_0001',
              section: 'Reconciliation',
              line: 'upgrade foo',
              action: { action: 'upgrade_confidence' },
            },
          ],
        }),
        { status: 200 },
      )
    }
    if (u.endsWith('/api/sb/digest/build')) {
      return new Response(JSON.stringify({ ok: true, emitted: true, entries: 2 }), {
        status: 200,
      })
    }
    return new Response('{}', { status: 200 })
  }) as typeof fetch
  seedStore({})
})

describe('DigestPanel pending tab', () => {
  it('switches to pending tab and renders proposals', async () => {
    seedStore({
      pending: [
        {
          id: 'pend_0001',
          section: 'Reconciliation',
          line: 'upgrade foo',
          action: { action: 'upgrade_confidence' },
        },
      ],
    })
    render(<DigestPanel open onClose={() => {}} />)
    fireEvent.click(screen.getByRole('tab', { name: /PENDING/i }))
    await waitFor(() => {
      expect(screen.getByTestId('digest-pending-entry')).toBeInTheDocument()
    })
    expect(screen.getByText('[pend_0001]')).toBeInTheDocument()
    expect(screen.getByText(/upgrade foo/)).toBeInTheDocument()
  })

  it('fires build endpoint on BUILD NOW click', async () => {
    seedStore({
      pending: [
        {
          id: 'pend_0001',
          section: 'Reconciliation',
          line: 'upgrade foo',
          action: { action: 'upgrade_confidence' },
        },
      ],
    })
    render(<DigestPanel open onClose={() => {}} />)
    fireEvent.click(screen.getByRole('tab', { name: /PENDING/i }))
    fireEvent.click(screen.getByRole('button', { name: /BUILD NOW/i }))
    await waitFor(() => {
      const fetchMock = global.fetch as unknown as ReturnType<typeof vi.fn>
      const called = fetchMock.mock.calls.some((c) =>
        c[0].toString().endsWith('/api/sb/digest/build'),
      )
      expect(called).toBe(true)
    })
  })

  it('shows empty state when no proposals', () => {
    seedStore({ pending: [] })
    render(<DigestPanel open onClose={() => {}} />)
    fireEvent.click(screen.getByRole('tab', { name: /PENDING/i }))
    expect(screen.getByText(/no pending proposals/i)).toBeInTheDocument()
  })
})
