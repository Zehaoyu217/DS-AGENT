import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { MentionButton } from '../MentionButton'

describe('MentionButton', () => {
  it('calls onInsert("@") on click', () => {
    const spy = vi.fn()
    render(<MentionButton onInsert={spy} />)
    fireEvent.click(screen.getByRole('button', { name: /mention/i }))
    expect(spy).toHaveBeenCalledWith('@')
  })
})
