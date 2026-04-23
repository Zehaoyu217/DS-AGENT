import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, fireEvent, waitFor } from '@testing-library/react'
import { AttachButton } from '../AttachButton'
import { useChatStore } from '@/lib/store'

describe('AttachButton', () => {
  beforeEach(() => {
    useChatStore.setState({ conversations: [], activeConversationId: null })
  })

  it('uploads the picked file via the store uploadDataset action', async () => {
    const id = useChatStore.getState().createConversation()
    const uploadSpy = vi
      .spyOn(useChatStore.getState(), 'uploadDataset')
      .mockResolvedValue({
        tableName: 'sales',
        filename: 'sales.csv',
        columns: [{ name: 'x', type: 'BIGINT' }],
        rowCount: 3,
        sizeBytes: 32,
        uploadedAt: Date.now(),
      })

    const { container } = render(<AttachButton conversationId={id} />)
    const input = container.querySelector('input[type="file"]')!
    const file = new File(['a,b\n1,2'], 'sales.csv', { type: 'text/csv' })
    Object.defineProperty(input, 'files', { value: [file] })
    fireEvent.change(input)

    await waitFor(() => {
      expect(uploadSpy).toHaveBeenCalledWith(id, file)
    })
  })
})
