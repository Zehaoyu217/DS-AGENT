import { beforeEach, describe, expect, it } from 'vitest'
import { useRightRailStore } from '../right-rail-store'

describe('rightRailStore', () => {
  beforeEach(() => {
    useRightRailStore.setState({ traceTab: 'timeline' })
  })

  it('defaults to timeline', () => {
    expect(useRightRailStore.getState().traceTab).toBe('timeline')
  })

  it('setTraceTab switches tabs', () => {
    useRightRailStore.getState().setTraceTab('raw')
    expect(useRightRailStore.getState().traceTab).toBe('raw')

    useRightRailStore.getState().setTraceTab('context')
    expect(useRightRailStore.getState().traceTab).toBe('context')
  })
})
