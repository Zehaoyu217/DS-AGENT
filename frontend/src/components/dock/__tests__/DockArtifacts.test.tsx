import { describe, it, expect, beforeEach } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { DockArtifacts } from '../DockArtifacts'
import { useChatStore, type Artifact } from '@/lib/store'
import { useUiStore } from '@/lib/ui-store'

const art: Artifact = {
  id: 'x',
  type: 'chart',
  title: 'Chart A',
  content: '{}',
  format: 'vega-lite',
  session_id: 's',
  created_at: 1,
  metadata: {},
}

describe('DockArtifacts', () => {
  beforeEach(() => {
    useChatStore.setState({ artifacts: [] } as never)
    useUiStore.setState({ artifactView: 'grid' } as never)
  })

  it('empty state', () => {
    render(<DockArtifacts />)
    expect(screen.getByText(/no artifacts yet/i)).toBeInTheDocument()
  })

  it('renders tiles and toggles view', () => {
    useChatStore.setState({ artifacts: [art] } as never)
    render(<DockArtifacts />)
    expect(screen.getByText('Chart A')).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: /list view/i }))
    expect(useUiStore.getState().artifactView).toBe('list')
  })
})
