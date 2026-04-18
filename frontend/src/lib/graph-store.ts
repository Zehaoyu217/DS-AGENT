import { create } from 'zustand'

export type GraphNodeKind = 'claim' | 'source' | 'wiki'

export interface GraphNode {
  id: string
  kind: GraphNodeKind
  label: string
}

export interface GraphEdge {
  src: string
  dst: string
  kind: string
}

interface GraphResponse {
  ok: boolean
  center?: string | null
  nodes?: GraphNode[]
  edges?: GraphEdge[]
  note?: string
}

interface GraphState {
  loading: boolean
  error: string | null
  center: string | null
  nodes: GraphNode[]
  edges: GraphEdge[]
  note: string | null
  refresh: () => Promise<void>
  setCenter: (id: string | null) => Promise<void>
}

const DEFAULT_LIMIT = 50

export const useGraphStore = create<GraphState>((set, get) => ({
  loading: false,
  error: null,
  center: null,
  nodes: [],
  edges: [],
  note: null,

  async refresh() {
    const { center } = get()
    set({ loading: true, error: null })
    try {
      const qs = new URLSearchParams({ limit: String(DEFAULT_LIMIT) })
      if (center) qs.set('center', center)
      const res = await fetch(`/api/sb/graph?${qs.toString()}`)
      if (res.status === 404) {
        set({
          loading: false,
          nodes: [],
          edges: [],
          note: 'knowledge base disabled',
        })
        return
      }
      if (!res.ok) {
        throw new Error(`graph ${res.status}`)
      }
      const body = (await res.json()) as GraphResponse
      set({
        loading: false,
        nodes: body.nodes ?? [],
        edges: body.edges ?? [],
        note: body.note ?? null,
      })
    } catch (err: unknown) {
      set({
        loading: false,
        error: err instanceof Error ? err.message : 'Unexpected error',
      })
    }
  },

  async setCenter(id) {
    set({ center: id })
    await get().refresh()
  },
}))

export interface LayoutNode extends GraphNode {
  x: number
  y: number
}

interface LayoutOptions {
  width: number
  height: number
  iterations?: number
  seed?: number
}

/** Hand-rolled spring-repulsion layout. Deterministic with optional seed. */
export function computeLayout(
  nodes: GraphNode[],
  edges: GraphEdge[],
  opts: LayoutOptions,
): LayoutNode[] {
  const { width, height } = opts
  const iterations = opts.iterations ?? 120
  if (nodes.length === 0) return []

  // Seeded PRNG for deterministic initial positions.
  let s = (opts.seed ?? 1) >>> 0
  const rand = () => {
    s = (s * 1664525 + 1013904223) >>> 0
    return s / 0x1_0000_0000
  }

  const pts = nodes.map<LayoutNode>((n) => ({
    ...n,
    x: rand() * width,
    y: rand() * height,
  }))
  const idx = new Map(pts.map((p, i) => [p.id, i]))

  const k = Math.sqrt((width * height) / Math.max(nodes.length, 1))
  const repulse = k * k
  const attract = 1 / k

  for (let iter = 0; iter < iterations; iter++) {
    const t = 1 - iter / iterations
    const fx = new Array(pts.length).fill(0) as number[]
    const fy = new Array(pts.length).fill(0) as number[]

    // Repulsion: all-pairs (ok for n <= 50).
    for (let i = 0; i < pts.length; i++) {
      for (let j = i + 1; j < pts.length; j++) {
        const dx = pts[i].x - pts[j].x
        const dy = pts[i].y - pts[j].y
        const dist2 = Math.max(dx * dx + dy * dy, 0.01)
        const dist = Math.sqrt(dist2)
        const f = repulse / dist2
        const ux = (dx / dist) * f
        const uy = (dy / dist) * f
        fx[i] += ux
        fy[i] += uy
        fx[j] -= ux
        fy[j] -= uy
      }
    }

    // Attraction along edges.
    for (const e of edges) {
      const i = idx.get(e.src)
      const j = idx.get(e.dst)
      if (i === undefined || j === undefined) continue
      const dx = pts[i].x - pts[j].x
      const dy = pts[i].y - pts[j].y
      const dist = Math.max(Math.sqrt(dx * dx + dy * dy), 0.01)
      const f = dist * attract
      const ux = (dx / dist) * f
      const uy = (dy / dist) * f
      fx[i] -= ux
      fy[i] -= uy
      fx[j] += ux
      fy[j] += uy
    }

    const step = 8 * t + 1
    for (let i = 0; i < pts.length; i++) {
      const mag = Math.sqrt(fx[i] * fx[i] + fy[i] * fy[i])
      if (mag > 0) {
        pts[i].x += (fx[i] / mag) * Math.min(mag, step)
        pts[i].y += (fy[i] / mag) * Math.min(mag, step)
      }
      pts[i].x = Math.max(10, Math.min(width - 10, pts[i].x))
      pts[i].y = Math.max(10, Math.min(height - 10, pts[i].y))
    }
  }

  return pts
}
