/**
 * Tests for the Plan Mode toggle affordance on <ChatInput/>.
 *
 * Scope: the UI control and the request payload. The backend gate itself
 * (filtering tools, rewriting the system prompt) is tested in backend
 * pytest and is out of scope here — this test pins ONLY that:
 *
 *   1. The toggle renders as a switch with the correct aria-checked state.
 *   2. Clicking toggles the Zustand `planMode` flag.
 *   3. When plan mode is ON, the POST /api/chat/stream body carries
 *      `"plan_mode": true` (so the two-layer gate is actually armed).
 *   4. When plan mode is OFF, the body carries `"plan_mode": false` (and
 *      never omits it — the backend field defaults to false, but making
 *      the value explicit prevents a future default flip from silently
 *      altering behavior).
 */
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { ChatInput } from '../ChatInput'
import { useChatStore } from '@/lib/store'

type ParsedBody = Record<string, unknown> | undefined

function installStreamCaptureFetch() {
  const calls: Array<{ url: string; method: string; body: ParsedBody }> = []
  const impl = (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
    const url = typeof input === 'string' ? input : input.toString()
    const method = init?.method ?? 'GET'
    const bodyRaw = init?.body as string | undefined
    const body = bodyRaw ? (JSON.parse(bodyRaw) as Record<string, unknown>) : undefined
    calls.push({ url, method, body })

    // Chat stream: return a minimal SSE body with a single turn_end frame so
    // the component exits the "streaming" state cleanly instead of hanging.
    if (url.endsWith('/api/chat/stream')) {
      const payload =
        'data: ' +
        JSON.stringify({ type: 'turn_start', session_id: 's-1' }) +
        '\n\n' +
        'data: ' +
        JSON.stringify({ type: 'turn_end', final_text: 'ok', charts: [] }) +
        '\n\n'
      const bytes = new TextEncoder().encode(payload)
      let delivered = false
      const reader = {
        read: () => {
          if (!delivered) {
            delivered = true
            return Promise.resolve({ done: false, value: bytes })
          }
          return Promise.resolve({ done: true, value: undefined })
        },
      }
      return Promise.resolve({
        ok: true,
        status: 200,
        headers: { get: () => 'text/event-stream' },
        body: { getReader: () => reader },
        text: () => Promise.resolve(payload),
        json: () => Promise.resolve({}),
      } as unknown as Response)
    }

    // Conversation appendTurn and anything else — fire-and-forget, ok body.
    return Promise.resolve({
      ok: true,
      status: 200,
      headers: { get: () => 'application/json' },
      text: () => Promise.resolve('{}'),
      json: () => Promise.resolve({}),
    } as unknown as Response)
  }
  vi.stubGlobal('fetch', vi.fn(impl))
  return calls
}

function bootstrapConversation() {
  useChatStore.setState({
    conversations: [
      {
        id: 'conv-1',
        title: 'T',
        messages: [],
        createdAt: Date.now(),
        updatedAt: Date.now(),
      },
    ],
    activeConversationId: 'conv-1',
    planMode: false,
  })
}

describe('<ChatInput> Plan Mode toggle', () => {
  beforeEach(() => {
    bootstrapConversation()
  })
  afterEach(() => {
    vi.unstubAllGlobals()
    vi.restoreAllMocks()
    useChatStore.setState({ planMode: false })
  })

  it('renders as a switch reflecting the current store state', () => {
    installStreamCaptureFetch()
    useChatStore.setState({ planMode: false })

    render(<ChatInput conversationId="conv-1" />)

    const toggle = screen.getByRole('switch', { name: /plan mode/i })
    expect(toggle).toHaveAttribute('aria-checked', 'false')

    act(() => {
      useChatStore.setState({ planMode: true })
    })

    // Re-reading the DOM reflects the store update because ChatInput
    // subscribes to the slice.
    expect(screen.getByRole('switch', { name: /plan mode/i })).toHaveAttribute(
      'aria-checked',
      'true',
    )
  })

  it('toggles planMode on click', () => {
    installStreamCaptureFetch()

    render(<ChatInput conversationId="conv-1" />)
    const toggle = screen.getByRole('switch', { name: /plan mode/i })

    expect(useChatStore.getState().planMode).toBe(false)

    fireEvent.click(toggle)
    expect(useChatStore.getState().planMode).toBe(true)

    fireEvent.click(toggle)
    expect(useChatStore.getState().planMode).toBe(false)
  })

  it('sends plan_mode=true when the toggle is ON', async () => {
    const calls = installStreamCaptureFetch()
    useChatStore.setState({ planMode: true })

    render(<ChatInput conversationId="conv-1" />)
    const textarea = screen.getByLabelText('Message') as HTMLTextAreaElement

    await act(async () => {
      fireEvent.change(textarea, { target: { value: 'analyze this' } })
    })
    await act(async () => {
      fireEvent.keyDown(textarea, { key: 'Enter' })
    })

    const streamCall = await waitFor(() => {
      const hit = calls.find((c) => c.url.endsWith('/api/chat/stream'))
      if (!hit) throw new Error('stream call not issued yet')
      return hit
    })

    expect(streamCall.method).toBe('POST')
    expect(streamCall.body).toMatchObject({
      message: 'analyze this',
      plan_mode: true,
    })
  })

  it('sends plan_mode=false explicitly when the toggle is OFF', async () => {
    const calls = installStreamCaptureFetch()
    useChatStore.setState({ planMode: false })

    render(<ChatInput conversationId="conv-1" />)
    const textarea = screen.getByLabelText('Message') as HTMLTextAreaElement

    await act(async () => {
      fireEvent.change(textarea, { target: { value: 'hello' } })
    })
    await act(async () => {
      fireEvent.keyDown(textarea, { key: 'Enter' })
    })

    const streamCall = await waitFor(() => {
      const hit = calls.find((c) => c.url.endsWith('/api/chat/stream'))
      if (!hit) throw new Error('stream call not issued yet')
      return hit
    })

    // Explicit false, not missing — see the test preamble for why.
    expect(streamCall.body).toMatchObject({
      message: 'hello',
      plan_mode: false,
    })
  })
})
