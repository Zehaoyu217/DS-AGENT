const BASE_URL = '/api'

export async function fetchHealth(): Promise<{ status: string; version: string }> {
  const res = await fetch(`${BASE_URL}/health`)
  return res.json()
}

export interface ContextSnapshot {
  total_tokens: number
  max_tokens: number
  utilization: number
  compaction_needed: boolean
  layers: Array<{
    name: string
    tokens: number
    compactable: boolean
    items: Array<{ name: string; tokens: number }>
  }>
  compaction_history: Array<{
    id: number
    timestamp: string
    tokens_before: number
    tokens_after: number
    tokens_freed: number
    trigger_utilization: number
    removed: Array<{ name: string; tokens: number }>
    survived: string[]
  }>
}

export async function fetchContext(): Promise<ContextSnapshot> {
  const res = await fetch(`${BASE_URL}/context`)
  return res.json()
}
