/**
 * api-skills.ts — typed wrapper around the skills manifest API.
 *
 * Mirrors fields from backend/app/api/skills_api.py SkillEntry.
 */

const BASE_URL = ''

export interface SkillEntry {
  name: string
  version: string
  description: string
  level: number
  requires: string[]
  used_by: string[]
}

export interface SkillSourceFile {
  path: string
  content: string
}

export interface SkillDetail {
  name: string
  level: number
  version: string
  description: string
  requires: string[]
  required_by: string[]
  skill_md: string
  source_files: SkillSourceFile[]
}

interface SkillsManifestResponse {
  skills: SkillEntry[]
}

export async function listSkills(): Promise<SkillEntry[]> {
  const res = await fetch(`${BASE_URL}/api/skills/manifest`)
  if (!res.ok) {
    throw new Error(`Failed to fetch skills: ${res.status} ${res.statusText}`)
  }
  const data = (await res.json()) as SkillsManifestResponse
  return data.skills ?? []
}

export async function getSkillDetail(name: string): Promise<SkillDetail> {
  const res = await fetch(`${BASE_URL}/api/skills/${encodeURIComponent(name)}/detail`)
  if (!res.ok) {
    throw new Error(`Failed to fetch skill detail: ${res.status} ${res.statusText}`)
  }
  return (await res.json()) as SkillDetail
}
