/**
 * api-prompts.ts — typed wrapper around the prompts catalog API.
 *
 * Mirrors fields from backend/app/api/prompts_api.py PromptEntry.
 */

const BASE_URL = ''

export interface PromptEntry {
  id: string
  category: 'system' | 'skill_injection' | 'tool_description' | 'injector_template'
  label: string
  description: string
  layer: 'L1' | 'L2' | 'tool'
  compactable: boolean
  approx_tokens: number
  text: string
}

export async function listPrompts(): Promise<PromptEntry[]> {
  const res = await fetch(`${BASE_URL}/api/prompts`)
  if (!res.ok) {
    throw new Error(`Failed to fetch prompts: ${res.status} ${res.statusText}`)
  }
  return (await res.json()) as PromptEntry[]
}
