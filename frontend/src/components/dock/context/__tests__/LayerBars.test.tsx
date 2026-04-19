import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { LayerBars } from '../LayerBars'

describe('LayerBars', () => {
  it('renders one bar per layer with label and token count', () => {
    render(
      <LayerBars
        layers={[
          { id: '0', label: 'system', tokens: 12_000, maxTokens: 16_000 },
          { id: '1', label: 'history', tokens: 8_000, maxTokens: 16_000 },
        ]}
      />,
    )
    expect(screen.getByText('system')).toBeInTheDocument()
    expect(screen.getByText('history')).toBeInTheDocument()
    expect(screen.getAllByRole('progressbar')).toHaveLength(2)
  })
})
