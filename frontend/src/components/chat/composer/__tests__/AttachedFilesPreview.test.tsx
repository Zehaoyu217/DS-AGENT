import { describe, it, expect, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import { AttachedFilesPreview } from '../AttachedFilesPreview'
import { useChatStore, type UploadedDataset } from '@/lib/store'

function seed(conversationId: string, datasets: UploadedDataset[]) {
  useChatStore.setState((state) => ({
    conversations: state.conversations.map((c) =>
      c.id === conversationId ? { ...c, datasets } : c,
    ),
  }))
}

describe('AttachedFilesPreview', () => {
  beforeEach(() => {
    useChatStore.setState({ conversations: [], activeConversationId: null })
  })

  it('renders a chip per uploaded dataset', () => {
    const id = useChatStore.getState().createConversation()
    seed(id, [
      {
        tableName: 'sales',
        filename: 'sales.csv',
        columns: [{ name: 'x', type: 'BIGINT' }],
        rowCount: 1234,
        sizeBytes: 999,
        uploadedAt: Date.now(),
      },
      {
        tableName: 'inventory',
        filename: 'inventory.parquet',
        columns: [{ name: 'sku', type: 'VARCHAR' }],
        rowCount: 50,
        sizeBytes: 1_200,
        uploadedAt: Date.now(),
      },
    ])
    render(<AttachedFilesPreview conversationId={id} />)
    expect(screen.getByText('user_data.sales')).toBeInTheDocument()
    expect(screen.getByText('user_data.inventory')).toBeInTheDocument()
  })

  it('renders nothing when the conversation has no datasets', () => {
    const id = useChatStore.getState().createConversation()
    const { container } = render(<AttachedFilesPreview conversationId={id} />)
    expect(container).toBeEmptyDOMElement()
  })
})
