import { create } from 'zustand'

export type PipelineStatus = 'idle' | 'running' | 'done' | 'error'

export interface IngestResultSummary {
  sources_added: number
  source_id?: string | null
}

export interface DigestResultSummary {
  entries: number
  emitted: boolean
  pending: number
}

export interface MaintainResultSummary {
  lint_errors: number
  lint_warnings: number
  lint_info: number
  open_contradictions: number
  stale_count: number
  stale_abstracts: string[]
  analytics_rebuilt: boolean
  habit_proposals: number
  fts_bytes_before: number
  fts_bytes_after: number
  duck_bytes_before: number
  duck_bytes_after: number
}

export type PhaseResultSummary =
  | IngestResultSummary
  | DigestResultSummary
  | MaintainResultSummary

export interface PhaseState<T extends PhaseResultSummary = PhaseResultSummary> {
  status: PipelineStatus
  lastRunAt: string | null
  lastResult: T | null
  errorMessage: string | null
}

interface StatusResponse {
  ok: boolean
  ingest: { last_run_at: string | null; result: IngestResultSummary | null }
  digest: { last_run_at: string | null; result: DigestResultSummary | null }
  maintain: { last_run_at: string | null; result: MaintainResultSummary | null }
}

export interface PipelineStore {
  ingest: PhaseState<IngestResultSummary>
  digest: PhaseState<DigestResultSummary>
  maintain: PhaseState<MaintainResultSummary>
  refreshStatus: () => Promise<void>
  runDigest: () => Promise<DigestResultSummary | null>
  runMaintain: () => Promise<MaintainResultSummary | null>
}

const DONE_FLASH_MS = 2000

const emptyPhase = <T extends PhaseResultSummary>(): PhaseState<T> => ({
  status: 'idle',
  lastRunAt: null,
  lastResult: null,
  errorMessage: null,
})

function scheduleRevert(setStatus: (s: PipelineStatus) => void): void {
  if (typeof window === 'undefined') return
  window.setTimeout(() => setStatus('idle'), DONE_FLASH_MS)
}

export const usePipelineStore = create<PipelineStore>((set, get) => ({
  ingest: emptyPhase(),
  digest: emptyPhase(),
  maintain: emptyPhase(),

  async refreshStatus() {
    try {
      const res = await fetch('/api/sb/pipeline/status')
      if (!res.ok) return
      const body = (await res.json()) as StatusResponse
      set((s) => ({
        ingest: {
          ...s.ingest,
          lastRunAt: body.ingest.last_run_at,
          lastResult: body.ingest.result,
        },
        digest: {
          ...s.digest,
          lastRunAt: body.digest.last_run_at,
          lastResult: body.digest.result,
        },
        maintain: {
          ...s.maintain,
          lastRunAt: body.maintain.last_run_at,
          lastResult: body.maintain.result,
        },
      }))
    } catch {
      // status is best-effort; stale display is fine
    }
  },

  async runDigest() {
    set((s) => ({ digest: { ...s.digest, status: 'running', errorMessage: null } }))
    try {
      const res = await fetch('/api/sb/digest/build', { method: 'POST' })
      if (!res.ok) {
        const detail = await res.text()
        set((s) => ({
          digest: {
            ...s.digest,
            status: 'error',
            errorMessage: detail || `HTTP ${res.status}`,
          },
        }))
        return null
      }
      const body = (await res.json()) as {
        ok: boolean
        entries: number
        emitted: boolean
      }
      await get().refreshStatus()
      const result = get().digest.lastResult ?? {
        entries: body.entries,
        emitted: body.emitted,
        pending: 0,
      }
      set((s) => ({ digest: { ...s.digest, status: 'done', lastResult: result } }))
      scheduleRevert((status) =>
        set((s) => ({ digest: { ...s.digest, status } })),
      )
      return result
    } catch (err: unknown) {
      set((s) => ({
        digest: {
          ...s.digest,
          status: 'error',
          errorMessage: err instanceof Error ? err.message : 'Unexpected error',
        },
      }))
      return null
    }
  },

  async runMaintain() {
    set((s) => ({
      maintain: { ...s.maintain, status: 'running', errorMessage: null },
    }))
    try {
      const res = await fetch('/api/sb/maintain/run', { method: 'POST' })
      if (!res.ok) {
        const detail = await res.text()
        set((s) => ({
          maintain: {
            ...s.maintain,
            status: 'error',
            errorMessage: detail || `HTTP ${res.status}`,
          },
        }))
        return null
      }
      const body = (await res.json()) as {
        ok: boolean
        result: MaintainResultSummary
      }
      await get().refreshStatus()
      set((s) => ({
        maintain: { ...s.maintain, status: 'done', lastResult: body.result },
      }))
      scheduleRevert((status) =>
        set((s) => ({ maintain: { ...s.maintain, status } })),
      )
      return body.result
    } catch (err: unknown) {
      set((s) => ({
        maintain: {
          ...s.maintain,
          status: 'error',
          errorMessage: err instanceof Error ? err.message : 'Unexpected error',
        },
      }))
      return null
    }
  },
}))

export function formatAgo(iso: string | null, now: number = Date.now()): string {
  if (!iso) return 'never'
  const ts = Date.parse(iso)
  if (Number.isNaN(ts)) return 'never'
  const sec = Math.max(0, Math.round((now - ts) / 1000))
  if (sec < 60) return `${sec}s ago`
  const min = Math.round(sec / 60)
  if (min < 60) return `${min}m ago`
  const hr = Math.round(min / 60)
  if (hr < 24) return `${hr}h ago`
  return `${Math.round(hr / 24)}d ago`
}
