import { describe, it, expect } from 'vitest'
import { selectProgressSteps } from '../progressSteps'
import type { ToolCallEntry } from '@/lib/store'

function entry(p: Partial<ToolCallEntry>): ToolCallEntry {
  return {
    id: p.id ?? 'x',
    step: p.step ?? 0,
    name: p.name ?? 'tool',
    inputPreview: p.inputPreview ?? '',
    status: p.status ?? 'pending',
    startedAt: p.startedAt ?? 1,
    ...p,
  } as ToolCallEntry
}

describe('selectProgressSteps', () => {
  it('returns empty for empty log', () => {
    expect(selectProgressSteps([])).toEqual([])
  })

  it('maps tool calls to running/ok/err steps', () => {
    const steps = selectProgressSteps([
      entry({ id: 'a', step: 1, name: 'fetch', status: 'pending' }),
      entry({ id: 'b', step: 2, name: 'save', status: 'ok', finishedAt: 5 }),
      entry({ id: 'c', step: 3, name: 'x', status: 'error', finishedAt: 7 }),
    ])
    expect(steps).toHaveLength(3)
    expect(steps[0].status).toBe('running')
    expect(steps[1].status).toBe('ok')
    expect(steps[2].status).toBe('err')
  })

  it('tags compact entries with kind=compact', () => {
    const steps = selectProgressSteps([
      entry({ id: 'c', step: 4, name: '__compact__', status: 'ok', finishedAt: 9 }),
    ])
    expect(steps[0].kind).toBe('compact')
  })

  it('is referentially stable for the same log identity', () => {
    const log: ToolCallEntry[] = [entry({ id: 'a', step: 1, name: 'fetch', status: 'ok' })]
    const a = selectProgressSteps(log)
    const b = selectProgressSteps(log)
    expect(a).toBe(b)
  })
})
