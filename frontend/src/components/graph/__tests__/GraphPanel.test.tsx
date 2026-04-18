import { render, screen, fireEvent } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { GraphPanel } from '../GraphPanel'
import { useGraphStore, computeLayout } from '@/lib/graph-store'

function seed(partial: Partial<ReturnType<typeof useGraphStore.getState>>) {
  useGraphStore.setState({
    loading: false,
    error: null,
    center: null,
    nodes: [],
    edges: [],
    note: null,
    ...partial,
  })
}

beforeEach(() => {
  global.fetch = vi.fn(async () =>
    new Response(JSON.stringify({ ok: true, nodes: [], edges: [] }), {
      status: 200,
    }),
  ) as typeof fetch
  seed({})
})

describe('GraphPanel', () => {
  it('returns null when closed', () => {
    const { container } = render(<GraphPanel open={false} onClose={() => {}} />)
    expect(container.firstChild).toBeNull()
  })

  it('renders empty state when no data', () => {
    render(<GraphPanel open onClose={() => {}} />)
    expect(screen.getByText(/no graph data yet/i)).toBeInTheDocument()
  })

  it('renders nodes and edges when populated', () => {
    seed({
      nodes: [
        { id: 'clm_a', kind: 'claim', label: 'a' },
        { id: 'src_b', kind: 'source', label: 'b' },
      ],
      edges: [{ src: 'clm_a', dst: 'src_b', kind: 'supports' }],
    })
    render(<GraphPanel open onClose={() => {}} />)
    expect(screen.getAllByTestId('graph-node')).toHaveLength(2)
    expect(screen.getAllByTestId('graph-edge')).toHaveLength(1)
  })

  it('GO button sets center and refreshes', async () => {
    const fetchSpy = vi.fn(async () =>
      new Response(JSON.stringify({ ok: true, nodes: [], edges: [] }), {
        status: 200,
      }),
    ) as typeof fetch
    global.fetch = fetchSpy

    render(<GraphPanel open onClose={() => {}} />)
    const input = screen.getByTestId('graph-center-input') as HTMLInputElement
    fireEvent.change(input, { target: { value: 'clm_xyz' } })
    fireEvent.click(screen.getByTestId('graph-go'))

    // wait a tick for the async setCenter -> refresh
    await Promise.resolve()
    await Promise.resolve()

    expect(useGraphStore.getState().center).toBe('clm_xyz')
  })
})

describe('computeLayout', () => {
  it('returns empty for no nodes', () => {
    expect(computeLayout([], [], { width: 300, height: 300 })).toEqual([])
  })

  it('places every node within the bounding box', () => {
    const nodes = [
      { id: 'a', kind: 'claim' as const, label: 'a' },
      { id: 'b', kind: 'wiki' as const, label: 'b' },
      { id: 'c', kind: 'source' as const, label: 'c' },
    ]
    const edges = [{ src: 'a', dst: 'b', kind: 'supports' }]
    const laid = computeLayout(nodes, edges, {
      width: 300,
      height: 400,
      iterations: 20,
    })
    expect(laid).toHaveLength(3)
    for (const n of laid) {
      expect(n.x).toBeGreaterThanOrEqual(0)
      expect(n.x).toBeLessThanOrEqual(300)
      expect(n.y).toBeGreaterThanOrEqual(0)
      expect(n.y).toBeLessThanOrEqual(400)
    }
  })
})

describe('graph-store', () => {
  it('refresh handles 404 by clearing data', async () => {
    global.fetch = vi.fn(async () =>
      new Response('not found', { status: 404 }),
    ) as typeof fetch
    await useGraphStore.getState().refresh()
    const state = useGraphStore.getState()
    expect(state.nodes).toEqual([])
    expect(state.note).toBe('knowledge base disabled')
  })

  it('refresh stores nodes and edges on happy path', async () => {
    global.fetch = vi.fn(async () =>
      new Response(
        JSON.stringify({
          ok: true,
          nodes: [{ id: 'clm_x', kind: 'claim', label: 'x' }],
          edges: [],
        }),
        { status: 200 },
      ),
    ) as typeof fetch
    await useGraphStore.getState().refresh()
    const state = useGraphStore.getState()
    expect(state.nodes).toHaveLength(1)
    expect(state.nodes[0].id).toBe('clm_x')
  })
})
