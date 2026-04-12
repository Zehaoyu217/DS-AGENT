export type Grade = 'A' | 'B' | 'C' | 'F'
export type PreflightVerdict = 'pass' | 'fail' | 'skipped'

export interface SOPSession {
  session_id: string
  date: string
  level: number
  overall_grade_before: Grade | null
  preflight: { verdict: PreflightVerdict }
  triage: { bucket: string | null }
  fix: { name: string | null; evidence: string | null }
  outcome: { grade_after: Grade | null }
  trace_links: { trace_id: string | null }
}

export async function listSessions(): Promise<SOPSession[]> {
  const r = await fetch('/api/sop/sessions')
  if (!r.ok) throw new Error(`listSessions failed: ${r.status}`)
  const body = (await r.json()) as { sessions: SOPSession[] }
  return body.sessions
}

export interface JudgeVarianceResponse {
  variance: Record<string, number>
  threshold_exceeded: string[]
  n?: number
  source?: 'cached' | 'live'
}

export async function fetchJudgeVariance(
  traceId: string,
  n = 5,
): Promise<JudgeVarianceResponse> {
  const r = await fetch(
    `/api/trace/traces/${encodeURIComponent(traceId)}/judge-variance?refresh=0&n=${n}`,
  )
  if (!r.ok) throw new Error(`fetchJudgeVariance failed: ${r.status}`)
  return (await r.json()) as JudgeVarianceResponse
}

export interface PromptSection {
  source: string
  lines: string
  text: string
}

export interface PromptConflict {
  source_a: string
  source_b: string
  overlap: string
}

export interface PromptAssembly {
  sections: PromptSection[]
  conflicts: PromptConflict[]
}

export async function fetchPromptAssembly(
  traceId: string,
  stepId: string,
): Promise<PromptAssembly> {
  const r = await fetch(
    `/api/trace/traces/${encodeURIComponent(traceId)}/prompt/${encodeURIComponent(stepId)}`,
  )
  if (!r.ok) throw new Error(`fetchPromptAssembly failed: ${r.status}`)
  return (await r.json()) as PromptAssembly
}

export interface TimelineTurn {
  turn: number
  layers: Record<string, number>
}

export interface TimelineEvent {
  turn: number
  kind: string
  detail: string
}

export interface Timeline {
  turns: TimelineTurn[]
  events: TimelineEvent[]
}

export async function fetchTimeline(traceId: string): Promise<Timeline> {
  const r = await fetch(
    `/api/trace/traces/${encodeURIComponent(traceId)}/timeline`,
  )
  if (!r.ok) throw new Error(`fetchTimeline failed: ${r.status}`)
  return (await r.json()) as Timeline
}

export interface TraceSummary {
  session_id: string
  level: number
  outcome: string
  final_grade: Grade | null
  turn_count: number
  llm_call_count: number
  step_ids: string[]
}

export async function fetchTraceSummary(traceId: string): Promise<TraceSummary> {
  const r = await fetch(`/api/trace/traces/${encodeURIComponent(traceId)}`)
  if (!r.ok) throw new Error(`fetchTraceSummary failed: ${r.status}`)
  const body = (await r.json()) as { summary: TraceSummary }
  return body.summary
}
