/**
 * Tests for the Prompt sub-tab of SessionDevToolsPanel.
 *
 * Background: P22 surfaced that the trace YAML now carries a structured
 * `sections` array per llm_call, and the frontend DevTools Prompt tab splits
 * those sections by `source` to render the system prompt and the user query
 * separately. This is the regression suite for that path.
 *
 * Why test through `SessionDevToolsPanel`: the inner `PromptInspectorPanel`
 * component is a private function inside the module and isn't exported, so
 * the contract we actually ship is the one reachable by clicking the
 * "Prompt" sub-tab. Testing at that boundary protects us from accidentally
 * breaking the user-visible flow even if the internal function is renamed
 * or reshaped.
 *
 * Mocked endpoints:
 *   GET /api/trace/summary/{id}       — consumed by <SessionHeader/>
 *   GET /api/trace/traces/{id}/timeline
 *   GET /api/trace/traces/{id}/prompt/{stepId}
 */
import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { SessionDevToolsPanel } from '../SessionDevToolsPanel'

type Handler = {
  status?: number
  body: unknown
  contentType?: string
}

/**
 * TraceTimeline renders by default on the Timeline sub-tab, and it crashes
 * if turns omit `layers`. We don't want timeline-shape leakage to mask real
 * prompt-panel failures, so every timeline mock returned to the panel has
 * the fully-shaped turns. Tests that care about prompt behavior use
 * `makeTurns()` to stay focused on what matters — the `turn` number.
 */
function makeTurns(turnNumbers: number[]): { turn: number; layers: { input: number; tool_calls: number } }[] {
  return turnNumbers.map((t) => ({
    turn: t,
    layers: { input: 0, tool_calls: 0 },
  }))
}

function installFetch(handlers: Record<string, Handler>) {
  const calls: Array<{ url: string; method: string }> = []
  const impl = (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
    const url = typeof input === 'string' ? input : input.toString()
    const method = init?.method ?? 'GET'
    calls.push({ url, method })
    const key = `${method} ${url.split('?')[0]}`
    const handler = handlers[key]
    if (!handler) {
      return Promise.resolve({
        ok: false,
        status: 404,
        headers: { get: () => 'text/plain' },
        text: () => Promise.resolve('no handler'),
        json: () => Promise.resolve({}),
      } as unknown as Response)
    }
    const status = handler.status ?? 200
    const ok = status >= 200 && status < 300
    return Promise.resolve({
      ok,
      status,
      headers: {
        get: (name: string) =>
          name.toLowerCase() === 'content-type'
            ? handler.contentType ?? 'application/json'
            : null,
      },
      json: () => Promise.resolve(handler.body),
      text: () =>
        Promise.resolve(
          typeof handler.body === 'string' ? handler.body : JSON.stringify(handler.body),
        ),
    } as unknown as Response)
  }
  vi.stubGlobal('fetch', vi.fn(impl))
  return calls
}

/** Click the "Prompt" sub-tab so the inner PromptInspectorPanel mounts. */
async function selectPromptTab(): Promise<void> {
  const tab = await screen.findByRole('tab', { name: /prompt/i })
  fireEvent.click(tab)
}

/** Reasonable defaults for the two unrelated endpoints the panel calls. */
function baseHandlers(sessionId: string): Record<string, Handler> {
  return {
    [`GET /api/trace/summary/${sessionId}`]: {
      body: {
        summary: {
          session_id: sessionId,
          level: 1,
          level_label: 'L1',
          outcome: 'success',
          turn_count: 1,
          duration_ms: 123,
          started_at: '2026-04-15T00:00:00Z',
        },
      },
    },
  }
}

describe('SessionDevToolsPanel — Prompt tab', () => {
  beforeEach(() => {
    vi.useRealTimers()
  })
  afterEach(() => {
    vi.unstubAllGlobals()
    vi.restoreAllMocks()
  })

  it('renders the empty state when no sessionId is provided', () => {
    render(<SessionDevToolsPanel sessionId={null} />)
    expect(screen.getByText(/no active session/i)).toBeInTheDocument()
  })

  it('renders system and user text from the matching sections on the last turn', async () => {
    const sessionId = 'sess-abc'
    installFetch({
      ...baseHandlers(sessionId),
      [`GET /api/trace/traces/${sessionId}/timeline`]: {
        body: { turns: makeTurns([1, 2]), events: [] },
      },
      [`GET /api/trace/traces/${sessionId}/prompt/s2`]: {
        body: {
          sections: [
            { source: 'system_prompt', text: 'SYSTEM_BASE', lines: '1-5' },
            { source: 'system_prompt', text: 'SYSTEM_EXTRA' },
            { source: 'user_query', text: 'analyze this thing' },
            { source: 'wiki', text: 'ignored' },
          ],
          conflicts: [],
        },
      },
    })

    render(<SessionDevToolsPanel sessionId={sessionId} />)
    await selectPromptTab()

    // joinSectionsBySource glues multiple entries per source with \n\n —
    // both system chunks must appear and nothing else from the array should
    // leak into the system/user panes.
    const systemText = await screen.findByText(/SYSTEM_BASE/)
    expect(systemText.textContent).toContain('SYSTEM_EXTRA')
    expect(screen.getByText(/analyze this thing/)).toBeInTheDocument()
    expect(screen.queryByText(/^ignored$/)).not.toBeInTheDocument()

    // The step label comes from the last turn in the timeline (s2).
    expect(screen.getByText('s2')).toBeInTheDocument()
    expect(screen.getByText(/4 sections/i)).toBeInTheDocument()
  })

  it('falls back to placeholder text when a source is missing', async () => {
    const sessionId = 'sess-nosys'
    installFetch({
      ...baseHandlers(sessionId),
      [`GET /api/trace/traces/${sessionId}/timeline`]: {
        body: { turns: makeTurns([1]), events: [] },
      },
      [`GET /api/trace/traces/${sessionId}/prompt/s1`]: {
        body: {
          sections: [{ source: 'user_query', text: 'only the user asked' }],
          conflicts: [],
        },
      },
    })

    render(<SessionDevToolsPanel sessionId={sessionId} />)
    await selectPromptTab()

    await screen.findByText(/only the user asked/)
    // Without a system_prompt entry the panel must still render — and it
    // must make the absence legible rather than silently showing an empty
    // <pre> block.
    expect(
      screen.getByText(/no system_prompt section recorded/i),
    ).toBeInTheDocument()
  })

  it('renders the empty state when the timeline has no turns', async () => {
    const sessionId = 'sess-empty'
    installFetch({
      ...baseHandlers(sessionId),
      [`GET /api/trace/traces/${sessionId}/timeline`]: {
        body: { turns: makeTurns([]), events: [] },
      },
    })

    render(<SessionDevToolsPanel sessionId={sessionId} />)
    await selectPromptTab()

    await screen.findByText(/no prompt recorded yet/i)
  })

  it('surfaces the error message when the prompt endpoint 404s', async () => {
    const sessionId = 'sess-404'
    installFetch({
      ...baseHandlers(sessionId),
      [`GET /api/trace/traces/${sessionId}/timeline`]: {
        body: { turns: makeTurns([1]), events: [] },
      },
      [`GET /api/trace/traces/${sessionId}/prompt/s1`]: {
        status: 404,
        body: { detail: 'not found' },
      },
    })

    render(<SessionDevToolsPanel sessionId={sessionId} />)
    await selectPromptTab()

    // The Prompt panel should not render pre blocks full of blanks on
    // error; it should explicitly say HTTP 404 so operators can correlate
    // with the backend log.
    await waitFor(() => {
      expect(screen.getByText(/HTTP 404/)).toBeInTheDocument()
    })
  })

  it('requests the prompt for the LAST turn in the timeline', async () => {
    const sessionId = 'sess-many-turns'
    const calls = installFetch({
      ...baseHandlers(sessionId),
      [`GET /api/trace/traces/${sessionId}/timeline`]: {
        body: { turns: makeTurns([1, 2, 3]), events: [] },
      },
      [`GET /api/trace/traces/${sessionId}/prompt/s3`]: {
        body: {
          sections: [
            { source: 'system_prompt', text: 'sys' },
            { source: 'user_query', text: 'third-turn query' },
          ],
          conflicts: [],
        },
      },
    })

    render(<SessionDevToolsPanel sessionId={sessionId} />)
    await selectPromptTab()

    await screen.findByText(/third-turn query/)
    // We only want to pin the URL we care about; everything else (header,
    // etc.) is incidental.
    const promptCall = calls.find((c) => c.url.endsWith('/prompt/s3'))
    expect(promptCall).toBeDefined()
    // And no call to an off-by-one step id.
    const wrongCall = calls.find((c) => c.url.endsWith('/prompt/s2'))
    expect(wrongCall).toBeUndefined()
  })
})
