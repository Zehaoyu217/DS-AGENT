export interface WikiNode {
  name: string
  path: string
  kind: 'dir' | 'file'
  size: number
  modified: number
  children: WikiNode[]
  pinned: boolean
}

export interface WikiTreeResponse {
  root: string
  nodes: WikiNode[]
}

export interface WikiPageResponse {
  path: string
  content: string
  size: number
  modified: number
  outbound_links: string[]
}

export interface WikiBacklink {
  path: string
  label: string
}

export interface WikiBacklinksResponse {
  path: string
  backlinks: WikiBacklink[]
}

async function getJson<T>(url: string): Promise<T> {
  const res = await fetch(url)
  if (!res.ok) {
    throw new Error(`${res.status} ${res.statusText}`)
  }
  return (await res.json()) as T
}

export function fetchWikiTree(): Promise<WikiTreeResponse> {
  return getJson<WikiTreeResponse>('/api/wiki/tree')
}

export function fetchWikiPage(path: string): Promise<WikiPageResponse> {
  const q = encodeURIComponent(path)
  return getJson<WikiPageResponse>(`/api/wiki/page?path=${q}`)
}

export function fetchWikiBacklinks(path: string): Promise<WikiBacklinksResponse> {
  const q = encodeURIComponent(path)
  return getJson<WikiBacklinksResponse>(`/api/wiki/backlinks?path=${q}`)
}

// ── Tree filter helpers ──────────────────────────────────────────────────────
export function filterTree(nodes: WikiNode[], query: string): WikiNode[] {
  if (!query) return nodes
  const q = query.toLowerCase()
  const visit = (n: WikiNode): WikiNode | null => {
    if (n.kind === 'file') {
      return n.name.toLowerCase().includes(q) || n.path.toLowerCase().includes(q)
        ? n
        : null
    }
    const kept: WikiNode[] = []
    for (const c of n.children) {
      const m = visit(c)
      if (m) kept.push(m)
    }
    if (kept.length === 0 && !n.name.toLowerCase().includes(q)) return null
    return { ...n, children: kept }
  }
  const out: WikiNode[] = []
  for (const n of nodes) {
    const m = visit(n)
    if (m) out.push(m)
  }
  return out
}

export function countFiles(nodes: WikiNode[]): number {
  let n = 0
  const walk = (xs: WikiNode[]) => {
    for (const x of xs) {
      if (x.kind === 'file') n += 1
      else walk(x.children)
    }
  }
  walk(nodes)
  return n
}

export function formatRelative(modified: number): string {
  if (!modified) return '—'
  const ms = Date.now() - modified * 1000
  if (ms < 60_000) return 'just now'
  if (ms < 3_600_000) return `${Math.floor(ms / 60_000)}m ago`
  if (ms < 86_400_000) return `${Math.floor(ms / 3_600_000)}h ago`
  if (ms < 30 * 86_400_000) return `${Math.floor(ms / 86_400_000)}d ago`
  return new Date(modified * 1000).toLocaleDateString()
}

export function extractToc(content: string): { id: string; depth: number; text: string }[] {
  const out: { id: string; depth: number; text: string }[] = []
  const lines = content.split('\n')
  let inFence = false
  for (const line of lines) {
    if (/^```/.test(line)) {
      inFence = !inFence
      continue
    }
    if (inFence) continue
    const m = /^(#{2,4})\s+(.+?)\s*$/.exec(line)
    if (!m) continue
    const depth = m[1].length
    const text = m[2].replace(/`([^`]+)`/g, '$1').trim()
    const id = text
      .toLowerCase()
      .replace(/[^a-z0-9\s-]/g, '')
      .trim()
      .replace(/\s+/g, '-')
    out.push({ id, depth, text })
  }
  return out
}
