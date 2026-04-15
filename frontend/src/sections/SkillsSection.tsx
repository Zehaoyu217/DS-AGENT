import { useCallback, useEffect, useState } from 'react'
import { Check, Copy, Puzzle } from 'lucide-react'
import { CodeBlock } from '@/components/chat/CodeBlock'
import { listSkills, getSkillDetail, type SkillEntry, type SkillDetail } from '@/lib/api-skills'
import { cn } from '@/lib/utils'

const LEVEL_LABELS: Record<number, string> = {
  1: 'PRIMITIVES',
  2: 'ANALYTICAL',
  3: 'COMPOSITION',
}

function getLevelLabel(level: number): string {
  return LEVEL_LABELS[level] ?? `LEVEL ${level}`
}

function guessLanguage(path: string): string {
  if (path.endsWith('.py')) return 'python'
  if (path.endsWith('.md')) return 'markdown'
  if (path.endsWith('.yaml') || path.endsWith('.yml')) return 'yaml'
  if (path.endsWith('.toml')) return 'toml'
  if (path.endsWith('.json')) return 'json'
  return 'plaintext'
}

interface LevelBadgeProps {
  level: number
}

function LevelBadge({ level }: LevelBadgeProps) {
  return (
    <span
      className={cn(
        'text-[10px] font-mono font-semibold uppercase tracking-wider px-1.5 py-0.5 rounded border flex-shrink-0',
        level === 1
          ? 'bg-brand-950/40 text-brand-400 border-brand-900/60'
          : level === 2
            ? 'bg-emerald-950/40 text-emerald-400 border-emerald-900/60'
            : 'bg-amber-950/40 text-amber-400 border-amber-900/60',
      )}
    >
      L{level}
    </span>
  )
}

interface SkillListItemProps {
  skill: SkillEntry
  isSelected: boolean
  onSelect: (name: string) => void
}

function SkillListItem({ skill, isSelected, onSelect }: SkillListItemProps) {
  const isAlwaysLoaded = skill.level === 1

  return (
    <button
      type="button"
      onClick={() => onSelect(skill.name)}
      className={cn(
        'w-full flex items-center gap-2 px-2 py-1.5 rounded text-left transition-colors',
        'focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-brand-500',
        isSelected
          ? 'bg-brand-950/40 border-l-2 border-brand-500 pl-1.5'
          : 'hover:bg-surface-800/60 border-l-2 border-transparent',
      )}
      aria-selected={isSelected}
    >
      {/* Circle icon */}
      <span
        className={cn(
          'w-4 h-4 flex-shrink-0 rounded-full border flex items-center justify-center',
          isSelected ? 'border-brand-500 bg-brand-950/60' : 'border-surface-600',
        )}
        aria-hidden
      >
        <span
          className={cn(
            'w-1.5 h-1.5 rounded-full',
            isSelected ? 'bg-brand-400' : 'bg-surface-600',
          )}
        />
      </span>

      <span className="flex-1 min-w-0 font-mono text-xs text-surface-300 truncate">
        {skill.name}
      </span>

      <span
        className={cn(
          'flex-shrink-0 text-[9px] font-mono uppercase tracking-wider px-1 py-0.5 rounded',
          isAlwaysLoaded
            ? 'text-brand-500/70'
            : 'text-surface-600',
        )}
      >
        {isAlwaysLoaded ? 'always' : 'on-demand'}
      </span>
    </button>
  )
}

interface SkillDetailPanelProps {
  detail: SkillDetail
}

function SkillDetailPanel({ detail }: SkillDetailPanelProps) {
  const [activeTab, setActiveTab] = useState(0)
  const [copied, setCopied] = useState(false)

  // Reset tab when skill changes
  useEffect(() => {
    setActiveTab(0)
  }, [detail.name])

  const activeFile = detail.source_files[activeTab]

  async function handleCopy() {
    if (!activeFile) return
    try {
      await navigator.clipboard.writeText(activeFile.content)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch {
      // clipboard not available
    }
  }

  return (
    <div className="flex flex-col h-full min-h-0">
      {/* Skill header */}
      <div className="px-6 py-4 border-b border-surface-800 flex-shrink-0">
        <div className="flex items-center gap-2 flex-wrap">
          <h2 className="font-mono text-sm font-semibold text-surface-100">{detail.name}</h2>
          <span className="text-[10px] font-mono text-surface-600 bg-surface-800 px-1.5 py-0.5 rounded border border-surface-700">
            v{detail.version}
          </span>
          <LevelBadge level={detail.level} />
        </div>
        {detail.description && (
          <p className="mt-2 text-xs text-surface-400 leading-relaxed">{detail.description}</p>
        )}
      </div>

      {/* Dependencies */}
      {(detail.requires.length > 0 || detail.required_by.length > 0) && (
        <div className="px-6 py-3 border-b border-surface-800 flex-shrink-0 space-y-2">
          {detail.requires.length > 0 && (
            <div className="flex items-start gap-2">
              <span className="text-[10px] font-mono text-surface-600 uppercase tracking-wider pt-0.5 flex-shrink-0 w-20">
                requires
              </span>
              <div className="flex flex-wrap gap-1">
                {detail.requires.map((dep) => (
                  <span key={dep} className="text-[10px] font-mono text-surface-400 bg-surface-800 px-1.5 py-0.5 rounded border border-surface-700 flex items-center gap-1">
                    <span className="text-surface-600">→</span> {dep}
                  </span>
                ))}
              </div>
            </div>
          )}
          {detail.required_by.length > 0 && (
            <div className="flex items-start gap-2">
              <span className="text-[10px] font-mono text-surface-600 uppercase tracking-wider pt-0.5 flex-shrink-0 w-20">
                required by
              </span>
              <div className="flex flex-wrap gap-1">
                {detail.required_by.map((dep) => (
                  <span key={dep} className="text-[10px] font-mono text-surface-400 bg-surface-800 px-1.5 py-0.5 rounded border border-surface-700">
                    {dep}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Source files */}
      {detail.source_files.length > 0 && (
        <div className="flex flex-col flex-1 min-h-0">
          {/* Tab bar */}
          <div className="flex items-center gap-0 border-b border-surface-800 px-2 flex-shrink-0 overflow-x-auto">
            {detail.source_files.map((file, idx) => (
              <button
                key={file.path}
                type="button"
                onClick={() => setActiveTab(idx)}
                className={cn(
                  'px-3 py-2 text-[11px] font-mono whitespace-nowrap transition-colors flex-shrink-0',
                  'focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-brand-500',
                  'border-b-2',
                  activeTab === idx
                    ? 'text-surface-100 border-brand-500'
                    : 'text-surface-500 border-transparent hover:text-surface-300 hover:border-surface-600',
                )}
              >
                {file.path}
              </button>
            ))}
            <div className="flex-1" />
            <button
              type="button"
              onClick={() => void handleCopy()}
              title={copied ? 'Copied!' : 'Copy file'}
              aria-label={copied ? 'Copied' : 'Copy file'}
              className="flex-shrink-0 ml-2 p-1.5 text-surface-500 hover:text-surface-300 transition-colors"
            >
              {copied ? (
                <Check className="w-3.5 h-3.5 text-green-400" />
              ) : (
                <Copy className="w-3.5 h-3.5" />
              )}
            </button>
          </div>

          {/* File content — overflow-y-auto on the wrapper; CodeBlock must NOT
              clip with overflow-hidden so its natural height feeds the scroll. */}
          {activeFile && (
            <div className="flex-1 min-h-0 overflow-y-auto overflow-x-hidden">
              <CodeBlock
                code={activeFile.content}
                language={guessLanguage(activeFile.path)}
                className="!rounded-none !border-none !my-0 !overflow-visible"
              />
            </div>
          )}
        </div>
      )}

      {detail.source_files.length === 0 && (
        <div className="flex-1 flex items-center justify-center">
          <p className="text-xs font-mono text-surface-600">No source files found</p>
        </div>
      )}
    </div>
  )
}

function SkillDetailLoading() {
  return (
    <div className="flex-1 flex items-center justify-center">
      <p className="text-xs font-mono text-surface-500">Loading detail…</p>
    </div>
  )
}

function SkillDetailEmpty() {
  return (
    <div className="flex-1 flex items-center justify-center">
      <div className="text-center space-y-1">
        <p className="text-xs font-mono text-surface-600 uppercase tracking-widest">
          Select a skill
        </p>
        <p className="text-[11px] text-surface-700">
          Click any skill in the list to view its detail
        </p>
      </div>
    </div>
  )
}

export function SkillsSection() {
  const [skills, setSkills] = useState<SkillEntry[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [search, setSearch] = useState('')
  const [selectedSkill, setSelectedSkill] = useState<string | null>(null)
  const [detail, setDetail] = useState<SkillDetail | null>(null)
  const [detailLoading, setDetailLoading] = useState(false)
  const [detailError, setDetailError] = useState<string | null>(null)

  const fetchSkills = useCallback(async () => {
    try {
      const data = await listSkills()
      setSkills(data)
      setError(null)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load skills'
      setError(message)
    } finally {
      setLoading(false)
    }
  }, [])

  const fetchDetail = useCallback(async (name: string) => {
    setDetailLoading(true)
    setDetailError(null)
    setDetail(null)
    try {
      const data = await getSkillDetail(name)
      setDetail(data)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load skill detail'
      setDetailError(message)
    } finally {
      setDetailLoading(false)
    }
  }, [])

  useEffect(() => {
    void fetchSkills()
  }, [fetchSkills])

  function handleSelect(name: string) {
    setSelectedSkill(name)
    void fetchDetail(name)
  }

  const q = search.trim().toLowerCase()
  const filteredSkills = q
    ? skills.filter((s) => s.name.toLowerCase().includes(q))
    : skills

  const levelGroups = new Map<number, SkillEntry[]>()
  for (const skill of filteredSkills) {
    const existing = levelGroups.get(skill.level)
    if (existing) {
      existing.push(skill)
    } else {
      levelGroups.set(skill.level, [skill])
    }
  }
  const sortedLevels = [...levelGroups.keys()].sort((a, b) => a - b)

  return (
    <div className="flex flex-col h-full bg-surface-950 text-surface-100 overflow-hidden">
      {/* Header */}
      <header className="flex items-center gap-3 px-6 py-4 border-b border-surface-800 flex-shrink-0">
        <Puzzle className="w-4 h-4 text-surface-500" aria-hidden />
        <h1 className="font-mono text-xs font-semibold text-surface-300 uppercase tracking-widest">
          SKILLS
        </h1>
        <span className="text-[10px] font-mono text-surface-600">
          {skills.length > 0 ? `${skills.length} discovered` : ''}
        </span>
      </header>

      {/* Two-column layout */}
      <div className="flex flex-1 min-h-0 overflow-hidden">
        {/* Left: skill list (260px) */}
        <aside
          className="w-[260px] flex-shrink-0 flex flex-col border-r border-surface-800 overflow-hidden"
          aria-label="Skill list"
        >
          {/* Search */}
          <div className="px-3 py-2 border-b border-surface-800 flex-shrink-0">
            <input
              type="search"
              placeholder="Search skills…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className={cn(
                'w-full bg-surface-800 border border-surface-700 rounded px-2 py-1',
                'text-xs font-mono text-surface-200 placeholder:text-surface-600',
                'focus:outline-none focus:border-brand-500',
              )}
              aria-label="Search skills"
            />
          </div>

          {/* Error */}
          {error && (
            <div
              role="alert"
              className="mx-2 my-2 rounded border border-red-900/60 bg-red-950/40 px-2 py-1.5 text-[11px] font-mono text-red-300"
            >
              {error}
            </div>
          )}

          {/* Skill list */}
          <div className="flex-1 min-h-0 overflow-y-auto" role="listbox" aria-label="Skills by level">
            {loading && (
              <p className="px-3 py-6 text-xs text-surface-500 text-center">Loading skills…</p>
            )}

            {!loading && filteredSkills.length === 0 && (
              <p className="px-3 py-6 text-xs text-surface-500 text-center">No skills found.</p>
            )}

            {sortedLevels.map((level) => {
              const levelSkills = levelGroups.get(level) ?? []
              const label = getLevelLabel(level)

              return (
                <div key={level} role="group" aria-label={`Level ${level} — ${label}`}>
                  {/* Section header */}
                  <div className="px-3 py-1.5 flex items-center gap-2 border-b border-surface-800/60 bg-surface-900/40">
                    <span className="text-[10px] font-mono font-semibold text-surface-600 uppercase tracking-widest">
                      Level {level} — {label}
                    </span>
                  </div>

                  <div className="px-1 py-0.5">
                    {levelSkills.map((skill) => (
                      <SkillListItem
                        key={skill.name}
                        skill={skill}
                        isSelected={selectedSkill === skill.name}
                        onSelect={handleSelect}
                      />
                    ))}
                  </div>
                </div>
              )
            })}
          </div>
        </aside>

        {/* Right: detail panel */}
        <main className="flex-1 min-w-0 flex flex-col overflow-hidden">
          {detailLoading && <SkillDetailLoading />}
          {!detailLoading && detailError && (
            <div className="p-6">
              <div
                role="alert"
                className="rounded border border-red-900/60 bg-red-950/40 px-4 py-3 text-xs font-mono text-red-300"
              >
                {detailError}
              </div>
            </div>
          )}
          {!detailLoading && !detailError && detail && <SkillDetailPanel detail={detail} />}
          {!detailLoading && !detailError && !detail && <SkillDetailEmpty />}
        </main>
      </div>
    </div>
  )
}
