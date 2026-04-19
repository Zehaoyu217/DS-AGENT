import { describe, it, expect, beforeEach } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { StepCard } from '../StepCard'
import { useUiStore } from '@/lib/ui-store'
import type { ProgressStep } from '@/lib/selectors/progressSteps'

const step: ProgressStep = {
  id: 's1',
  index: 1,
  title: 'fetch_data',
  kind: 'tool',
  status: 'ok',
  startedAt: 1_000,
  finishedAt: 1_250,
  toolCallIds: ['t1'],
  artifactIds: [],
}

describe('StepCard', () => {
  beforeEach(() => {
    useUiStore.setState({ progressExpanded: [] } as never)
  })

  it('renders title and elapsed', () => {
    render(<StepCard step={step} />)
    expect(screen.getByText('fetch_data')).toBeInTheDocument()
    expect(screen.getByText(/250\s*ms/)).toBeInTheDocument()
  })

  it('toggles expanded on click', () => {
    render(<StepCard step={step} />)
    fireEvent.click(screen.getByRole('button', { name: /fetch_data/i }))
    expect(useUiStore.getState().progressExpanded).toContain('s1')
  })
})
