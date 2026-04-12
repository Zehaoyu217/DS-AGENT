import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { useDevtoolsStore } from '../../stores/devtools'
import { SessionReplay } from './SessionReplay'

const mockSessions = [
  {
    session_id: 's-001',
    date: '2026-04-12',
    level: 3,
    overall_grade_before: 'F' as const,
    preflight: { verdict: 'pass' as const },
    triage: { bucket: 'context-management' },
    fix: { name: 'reduce-compaction', evidence: null },
    outcome: { grade_after: null },
    trace_links: { trace_id: 's-001' },
  },
  {
    session_id: 's-002',
    date: '2026-04-12',
    level: 3,
    overall_grade_before: 'F' as const,
    preflight: { verdict: 'pass' as const },
    triage: { bucket: 'other' },
    fix: { name: null, evidence: null },
    outcome: { grade_after: null },
    trace_links: { trace_id: null },
  },
]

beforeEach(() => {
  useDevtoolsStore.setState({ selectedTraceId: null })
  vi.stubGlobal('fetch', vi.fn(async () =>
    new Response(JSON.stringify({ sessions: mockSessions }), { status: 200 }),
  ))
})

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('SessionReplay', () => {
  it('row click with trace_id sets selectedTraceId', async () => {
    render(<SessionReplay />)
    const row = await screen.findByRole('button', { name: /s-001/i })
    fireEvent.click(row)
    await waitFor(() => {
      expect(useDevtoolsStore.getState().selectedTraceId).toBe('s-001')
    })
  })

  it('row without trace_id is disabled and shows (no trace) label', async () => {
    render(<SessionReplay />)
    const noTraceRow = await screen.findByText(/s-002/i)
    expect(noTraceRow.parentElement).toHaveTextContent(/no trace/i)
  })

  it('selected row has aria-selected true', async () => {
    useDevtoolsStore.setState({ selectedTraceId: 's-001' })
    render(<SessionReplay />)
    const row = await screen.findByRole('button', { name: /s-001/i })
    expect(row).toHaveAttribute('aria-selected', 'true')
  })
})
