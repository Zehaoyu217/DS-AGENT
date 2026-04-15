import { beforeEach, describe, expect, it } from 'vitest'
import { useDevtoolsStore } from '../devtools'

describe('devtools store selection', () => {
  beforeEach(() => {
    useDevtoolsStore.setState({
      selectedTraceId: null,
      selectedStepId: null,
    })
  })

  it('setSelectedTrace updates traceId and clears stepId', () => {
    useDevtoolsStore.setState({ selectedStepId: 's3' })
    useDevtoolsStore.getState().setSelectedTrace('trace-abc')
    const s = useDevtoolsStore.getState()
    expect(s.selectedTraceId).toBe('trace-abc')
    expect(s.selectedStepId).toBeNull()
  })

  it('setSelectedTrace(null) clears both', () => {
    useDevtoolsStore.setState({ selectedTraceId: 'x', selectedStepId: 's1' })
    useDevtoolsStore.getState().setSelectedTrace(null)
    const s = useDevtoolsStore.getState()
    expect(s.selectedTraceId).toBeNull()
    expect(s.selectedStepId).toBeNull()
  })

  it('setSelectedStep updates stepId without touching traceId', () => {
    useDevtoolsStore.setState({ selectedTraceId: 'trace-xyz' })
    useDevtoolsStore.getState().setSelectedStep('s2')
    const s = useDevtoolsStore.getState()
    expect(s.selectedTraceId).toBe('trace-xyz')
    expect(s.selectedStepId).toBe('s2')
  })
})
