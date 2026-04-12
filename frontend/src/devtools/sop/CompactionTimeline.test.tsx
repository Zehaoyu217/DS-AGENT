import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { useDevtoolsStore } from '../../stores/devtools'
import { CompactionTimeline } from './CompactionTimeline'

const traceBody = {
  trace_schema_version: 1,
  summary: {
    session_id: 'trace-1', level: 3,
    outcome: 'ok', final_grade: 'F',
    turn_count: 2, llm_call_count: 2,
    step_ids: ['s1', 's2'],
  },
  events: [
    {
      kind: 'llm_call', seq: 1, timestamp: 't',
      step_id: 's1', turn: 1, model: 'm',
      temperature: 1, max_tokens: 1, prompt_text: '',
      sections: [], response_text: '', tool_calls: [],
      stop_reason: 'end_turn', input_tokens: 100, output_tokens: 0,
      cache_read_tokens: 0, cache_creation_tokens: 0, latency_ms: 0,
    },
    {
      kind: 'llm_call', seq: 2, timestamp: 't',
      step_id: 's2', turn: 2, model: 'm',
      temperature: 1, max_tokens: 1, prompt_text: '',
      sections: [], response_text: '', tool_calls: [],
      stop_reason: 'end_turn', input_tokens: 200, output_tokens: 0,
      cache_read_tokens: 0, cache_creation_tokens: 0, latency_ms: 0,
    },
  ],
}

const timelineBody = {
  turns: [
    { turn: 1, layers: { input: 100, tool_calls: 0 } },
    { turn: 2, layers: { input: 200, tool_calls: 0 } },
  ],
  events: [
    { turn: 1, kind: 'compaction', detail: 'dropped 2 layers, -500 tokens' },
  ],
}

beforeEach(() => {
  useDevtoolsStore.setState({ selectedTraceId: 'trace-1', selectedStepId: null })
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    if (url.includes('/timeline')) {
      return new Response(JSON.stringify(timelineBody), { status: 200 })
    }
    return new Response(JSON.stringify(traceBody), { status: 200 })
  }))
})

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('CompactionTimeline', () => {
  it('bar click sets selectedStepId to first step in that turn', async () => {
    render(<CompactionTimeline traceId="trace-1" />)
    const btn = await screen.findByRole('button', { name: /select turn 2/i })
    fireEvent.click(btn)
    await waitFor(() => {
      expect(useDevtoolsStore.getState().selectedStepId).toBe('s2')
    })
  })

  it('disables button when turn has no llm_call events', async () => {
    const noStepsBody = {
      ...timelineBody,
      turns: [{ turn: 99, layers: { input: 0, tool_calls: 1 } }],
    }
    const emptyTraceBody = {
      ...traceBody,
      events: [
        {
          kind: 'tool_call', seq: 1, timestamp: 't',
          turn: 99, tool_name: 't', tool_input: {},
          tool_output: '', duration_ms: 0, error: null,
        },
      ],
    }
    vi.stubGlobal('fetch', vi.fn(async (url: string) => {
      if (url.includes('/timeline')) {
        return new Response(JSON.stringify(noStepsBody), { status: 200 })
      }
      return new Response(JSON.stringify(emptyTraceBody), { status: 200 })
    }))
    render(<CompactionTimeline traceId="trace-1" />)
    const btn = await screen.findByRole('button', { name: /select turn 99/i })
    expect(btn).toBeDisabled()
  })
})
