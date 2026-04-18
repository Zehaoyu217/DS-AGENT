import { create } from 'zustand'

export interface DigestEntry {
  id: string
  section: string
  line: string
  action: string
  applied: boolean
}

export interface PendingProposal {
  id: string
  section: string
  line: string
  action: Record<string, unknown>
}

interface BuildResult {
  emitted: boolean
  entries: number
}

interface DigestState {
  date: string
  entries: DigestEntry[]
  unread: number
  loading: boolean
  error: string | null
  pending: PendingProposal[]
  pendingLoading: boolean
  refresh: () => Promise<void>
  apply: (ids: string[]) => Promise<void>
  skip: (id: string, ttlDays?: number) => Promise<void>
  markRead: () => Promise<void>
  refreshPending: () => Promise<void>
  triggerBuild: () => Promise<BuildResult>
}

export const useDigestStore = create<DigestState>((set, get) => ({
  date: '',
  entries: [],
  unread: 0,
  loading: false,
  error: null,
  pending: [],
  pendingLoading: false,

  async refresh() {
    set({ loading: true, error: null })
    try {
      const response = await fetch('/api/sb/digest/today')
      if (response.status === 404) {
        // Second-brain disabled — present as empty state.
        set({ date: '', entries: [], unread: 0, loading: false })
        return
      }
      const body = (await response.json()) as {
        date?: string
        entries?: DigestEntry[]
        unread?: number
      }
      set({
        date: body.date ?? '',
        entries: body.entries ?? [],
        unread: body.unread ?? 0,
        loading: false,
      })
    } catch (err: unknown) {
      set({
        error: err instanceof Error ? err.message : 'Unexpected error',
        loading: false,
      })
    }
  },

  async apply(ids) {
    try {
      await fetch('/api/sb/digest/apply', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ ids }),
      })
    } catch (err: unknown) {
      set({ error: err instanceof Error ? err.message : 'Unexpected error' })
    }
    await get().refresh()
  },

  async skip(id, ttlDays = 30) {
    try {
      await fetch('/api/sb/digest/skip', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ id, ttl_days: ttlDays }),
      })
    } catch (err: unknown) {
      set({ error: err instanceof Error ? err.message : 'Unexpected error' })
    }
    await get().refresh()
  },

  async markRead() {
    const { date } = get()
    if (!date) return
    try {
      await fetch('/api/sb/digest/read', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ date }),
      })
    } catch (err: unknown) {
      set({ error: err instanceof Error ? err.message : 'Unexpected error' })
    }
  },

  async refreshPending() {
    set({ pendingLoading: true })
    try {
      const res = await fetch('/api/sb/digest/pending')
      if (res.status === 404) {
        set({ pending: [], pendingLoading: false })
        return
      }
      const body = (await res.json()) as { proposals?: PendingProposal[] }
      set({ pending: body.proposals ?? [], pendingLoading: false })
    } catch (err: unknown) {
      set({
        pendingLoading: false,
        error: err instanceof Error ? err.message : 'Unexpected error',
      })
    }
  },

  async triggerBuild() {
    try {
      const res = await fetch('/api/sb/digest/build', { method: 'POST' })
      if (res.status === 404) return { emitted: false, entries: 0 }
      const body = (await res.json()) as BuildResult
      return { emitted: Boolean(body.emitted), entries: body.entries ?? 0 }
    } catch (err: unknown) {
      set({ error: err instanceof Error ? err.message : 'Unexpected error' })
      return { emitted: false, entries: 0 }
    }
  },
}))
