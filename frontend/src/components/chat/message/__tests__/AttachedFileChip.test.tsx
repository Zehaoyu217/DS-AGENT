import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { AttachedFileChip } from '../AttachedFileChip'

describe('AttachedFileChip', () => {
  it('renders file name', () => {
    render(<AttachedFileChip name="q3-brief.md" />)
    expect(screen.getByText('q3-brief.md')).toBeInTheDocument()
  })
})
