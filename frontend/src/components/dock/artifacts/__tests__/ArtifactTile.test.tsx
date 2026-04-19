import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { ArtifactTile } from '../ArtifactTile'
import type { Artifact } from '@/lib/store'

const artifact: Artifact = {
  id: 'a1',
  type: 'chart',
  title: 'Revenue',
  content: '{}',
  format: 'vega-lite',
  session_id: 's',
  created_at: Date.now() / 1000,
  metadata: {},
}

describe('ArtifactTile', () => {
  it('renders kind label and title', () => {
    render(<ArtifactTile artifact={artifact} />)
    expect(screen.getByText('Revenue')).toBeInTheDocument()
    expect(screen.getByText(/chart/i)).toBeInTheDocument()
  })

  it('dispatches focusArtifact on click', () => {
    const handler = vi.fn()
    window.addEventListener('focusArtifact', handler as EventListener)
    render(<ArtifactTile artifact={artifact} />)
    fireEvent.click(screen.getByRole('button'))
    expect(handler).toHaveBeenCalled()
    const ev = handler.mock.calls[0][0] as CustomEvent
    expect((ev.detail as { id: string }).id).toBe('a1')
    window.removeEventListener('focusArtifact', handler as EventListener)
  })
})
