import { useCallback, useEffect, useMemo, useState } from 'react'
import type { ReactNode } from 'react'
import { Circle, Loader2, Save, Settings } from 'lucide-react'
import { backend, type FullConfigResponse } from '@/lib/api-backend'
import { SettingsTab as GeneralTab } from '@/components/sidebar/SettingsTab'
import { cn } from '@/lib/utils'

type TabId =
  | 'general'
  | 'models'
  | 'second-brain'
  | 'runtime'
  | 'env'
  | 'prompts'

interface TabDef {
  id: TabId
  label: string
  enabledWhen?: (cfg: FullConfigResponse | null) => boolean
  disabledHint?: string
}

const TABS: TabDef[] = [
  { id: 'general', label: 'General' },
  { id: 'models', label: 'Models' },
  {
    id: 'second-brain',
    label: 'Second Brain',
    enabledWhen: (c) => Boolean(c?.habits_yaml?.enabled),
    disabledHint: 'Second Brain disabled — set SECOND_BRAIN_HOME',
  },
  { id: 'runtime', label: 'Runtime' },
  { id: 'env', label: 'Environment' },
  { id: 'prompts', label: 'Prompts' },
]

export function SettingsSection() {
  const [tab, setTab] = useState<TabId>('general')
  const [cfg, setCfg] = useState<FullConfigResponse | null>(null)
  const [cfgError, setCfgError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  const reload = useCallback(async () => {
    setLoading(true)
    try {
      const r = await backend.settings.fullConfig()
      setCfg(r)
      setCfgError(null)
    } catch (err) {
      setCfgError(err instanceof Error ? err.message : String(err))
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    void reload()
  }, [reload])

  return (
    <div className="flex flex-col h-full bg-surface-950 text-surface-100 overflow-hidden">
      <header className="flex items-center gap-3 px-6 py-4 border-b border-surface-800 flex-shrink-0">
        <Settings className="w-4 h-4 text-surface-500" aria-hidden />
        <h1 className="font-mono text-xs font-semibold text-surface-300 uppercase tracking-widest">
          Settings
        </h1>
        {loading && (
          <Loader2
            className="w-3 h-3 animate-spin text-surface-500"
            aria-label="loading config"
          />
        )}
      </header>

      <nav
        role="tablist"
        aria-label="Settings tabs"
        className="flex items-center gap-0 border-b border-surface-800 flex-shrink-0 overflow-x-auto"
      >
        {TABS.map((t) => {
          const enabled = t.enabledWhen ? t.enabledWhen(cfg) : true
          return (
            <button
              key={t.id}
              role="tab"
              aria-selected={tab === t.id}
              aria-disabled={!enabled || undefined}
              title={enabled ? undefined : t.disabledHint}
              onClick={() => enabled && setTab(t.id)}
              disabled={!enabled}
              className={cn(
                'px-4 py-2 text-[12px] font-mono uppercase tracking-wider border-r border-surface-800',
                'transition-colors focus-ring',
                tab === t.id
                  ? 'bg-surface-900 text-fg-0 border-b-2 border-b-acc'
                  : 'text-fg-2 hover:text-fg-0 hover:bg-surface-900',
                !enabled && 'cursor-not-allowed opacity-50',
              )}
            >
              {t.label}
            </button>
          )
        })}
      </nav>

      <div className="flex-1 min-h-0 overflow-y-auto">
        {cfgError && (
          <div className="px-6 py-3 text-[12px] text-err">
            Failed to load config: {cfgError}
          </div>
        )}
        {tab === 'general' && <GeneralTab />}
        {tab === 'models' && <ModelsTabBody cfg={cfg} onSaved={reload} />}
        {tab === 'second-brain' && cfg?.habits_yaml?.enabled && (
          <SecondBrainTabBody cfg={cfg} onSaved={reload} />
        )}
        {tab === 'runtime' && <RuntimeTabBody cfg={cfg} />}
        {tab === 'env' && <EnvTabBody cfg={cfg} />}
        {tab === 'prompts' && <PromptsTabBody cfg={cfg} />}
      </div>
    </div>
  )
}

// ── shared primitives ──────────────────────────────────────────────────────

function Field({
  label,
  hint,
  readOnly,
  children,
}: {
  label: string
  hint?: string
  readOnly?: boolean
  children: ReactNode
}) {
  return (
    <label className="block">
      <div className="flex items-baseline gap-2 mb-1">
        <span className="text-[11px] font-mono uppercase tracking-wider text-fg-2">
          {label}
        </span>
        {readOnly && (
          <span className="text-[10px] font-mono text-fg-3">
            (read-only — restart required)
          </span>
        )}
      </div>
      {children}
      {hint && <div className="mt-1 text-[11px] text-fg-3">{hint}</div>}
    </label>
  )
}

function Code({ children }: { children: ReactNode }) {
  return (
    <pre className="overflow-auto rounded border border-surface-800 bg-surface-900 px-3 py-2 text-[11.5px] font-mono text-fg-1 whitespace-pre-wrap break-all">
      {children}
    </pre>
  )
}

function SaveButton({
  onClick,
  dirty,
  saving,
  error,
}: {
  onClick: () => void
  dirty: boolean
  saving: boolean
  error: string | null
}) {
  return (
    <div className="flex items-center gap-3 pt-2">
      <button
        type="button"
        onClick={onClick}
        disabled={!dirty || saving}
        className={cn(
          'inline-flex items-center gap-1.5 rounded border px-3 py-1.5 text-[12px]',
          'focus-ring transition-colors',
          dirty && !saving
            ? 'border-acc-line bg-acc-dim text-acc hover:bg-acc-dim/80'
            : 'border-surface-700 bg-surface-900 text-fg-3 cursor-not-allowed',
        )}
      >
        {saving ? (
          <Loader2 size={12} className="animate-spin" />
        ) : (
          <Save size={12} />
        )}
        Save
      </button>
      {error && <span className="text-[11px] text-err">{error}</span>}
      {!dirty && !saving && !error && (
        <span className="text-[11px] text-fg-3">No changes</span>
      )}
    </div>
  )
}

function InputBox({
  value,
  readOnly,
}: {
  value: string
  readOnly?: boolean
}) {
  return (
    <input
      type="text"
      value={value}
      readOnly={readOnly}
      className={cn(
        'w-full rounded border px-2.5 py-1.5 text-[12.5px] font-mono focus-ring',
        readOnly
          ? 'border-surface-800 bg-surface-900/60 text-fg-2 cursor-not-allowed'
          : 'border-surface-800 bg-surface-900 text-fg-1',
      )}
    />
  )
}

// ── Models tab ─────────────────────────────────────────────────────────────

function ModelsTabBody({
  cfg,
  onSaved,
}: {
  cfg: FullConfigResponse | null
  onSaved: () => void
}) {
  const initial = useMemo(
    () => JSON.stringify(cfg?.models_yaml?.content ?? {}, null, 2),
    [cfg],
  )
  const [text, setText] = useState(initial)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => setText(initial), [initial])
  const dirty = text !== initial

  const save = useCallback(async () => {
    setError(null)
    let parsed: Record<string, unknown>
    try {
      parsed = JSON.parse(text) as Record<string, unknown>
    } catch (e) {
      setError(`invalid JSON: ${e instanceof Error ? e.message : String(e)}`)
      return
    }
    setSaving(true)
    try {
      await backend.settings.patchModelsYaml(parsed)
      onSaved()
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
    } finally {
      setSaving(false)
    }
  }, [text, onSaved])

  if (!cfg) return <div className="px-6 py-4 text-fg-3">Loading…</div>

  return (
    <div className="px-6 py-4 space-y-4 max-w-4xl">
      <div>
        <h2 className="text-[13px] font-semibold mb-1">Model routing</h2>
        <p className="text-[12px] text-fg-2">
          <code className="font-mono">{cfg.models_yaml.path}</code> — edit as
          JSON. Validated against the harness loader before writing; bad
          providers, unknown role targets, etc. reject with a 400.
        </p>
      </div>
      <Field
        label="config/models.yaml (as JSON)"
        hint="Deep-merged on save. Unchanged keys are preserved."
      >
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={22}
          spellCheck={false}
          className="w-full rounded border border-surface-800 bg-surface-900 px-3 py-2 text-[12px] font-mono text-fg-1 focus-ring"
        />
      </Field>
      <SaveButton onClick={save} dirty={dirty} saving={saving} error={error} />
    </div>
  )
}

// ── Second Brain tab ───────────────────────────────────────────────────────

function SecondBrainTabBody({
  cfg,
  onSaved,
}: {
  cfg: FullConfigResponse | null
  onSaved: () => void
}) {
  const initial = useMemo(
    () => JSON.stringify(cfg?.habits_yaml?.content ?? {}, null, 2),
    [cfg],
  )
  const [text, setText] = useState(initial)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => setText(initial), [initial])
  const dirty = text !== initial

  const save = useCallback(async () => {
    setError(null)
    let parsed: Record<string, unknown>
    try {
      parsed = JSON.parse(text) as Record<string, unknown>
    } catch (e) {
      setError(`invalid JSON: ${e instanceof Error ? e.message : String(e)}`)
      return
    }
    setSaving(true)
    try {
      await backend.settings.patchHabitsYaml(parsed)
      onSaved()
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
    } finally {
      setSaving(false)
    }
  }, [text, onSaved])

  if (!cfg) return <div className="px-6 py-4 text-fg-3">Loading…</div>

  return (
    <div className="px-6 py-4 space-y-4 max-w-4xl">
      <div>
        <h2 className="text-[13px] font-semibold mb-1">Second Brain habits</h2>
        <p className="text-[12px] text-fg-2">
          <code className="font-mono">{cfg.habits_yaml.path}</code> — autonomy
          levels, digest/gardener passes, extraction density, taxonomy,
          retrieval. Writes are deep-merged (unchanged keys preserved).
        </p>
      </div>
      <Field label="habits.yaml (as JSON)">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={22}
          spellCheck={false}
          className="w-full rounded border border-surface-800 bg-surface-900 px-3 py-2 text-[12px] font-mono text-fg-1 focus-ring"
        />
      </Field>
      <SaveButton onClick={save} dirty={dirty} saving={saving} error={error} />
    </div>
  )
}

// ── Runtime tab (read-only) ────────────────────────────────────────────────

function RuntimeTabBody({ cfg }: { cfg: FullConfigResponse | null }) {
  if (!cfg) return <div className="px-6 py-4 text-fg-3">Loading…</div>
  const app = cfg.app
  const readonly = new Set(app._readonly)
  return (
    <div className="px-6 py-4 space-y-5 max-w-3xl">
      <h2 className="text-[13px] font-semibold">Harness runtime</h2>
      <div className="grid grid-cols-2 gap-x-6 gap-y-4">
        <Field label="Environment" readOnly={readonly.has('environment')}>
          <InputBox value={app.environment} readOnly />
        </Field>
        <Field label="Host" readOnly={readonly.has('host')}>
          <InputBox value={app.host} readOnly />
        </Field>
        <Field label="Port" readOnly={readonly.has('port')}>
          <InputBox value={String(app.port)} readOnly />
        </Field>
        <Field label="Debug" readOnly>
          <InputBox value={String(app.debug)} readOnly />
        </Field>
        <Field label="Default model">
          <InputBox value={app.default_model} readOnly />
        </Field>
        <Field label="OpenRouter key set">
          <InputBox value={app.openrouter_api_key_set ? 'yes' : 'no'} readOnly />
        </Field>
        <Field label="Sandbox timeout (s)">
          <InputBox value={String(app.sandbox_timeout_seconds)} readOnly />
        </Field>
        <Field label="Sandbox memory (MB)">
          <InputBox value={String(app.sandbox_max_memory_mb)} readOnly />
        </Field>
        <Field
          label="Context max tokens"
          readOnly={readonly.has('context_max_tokens')}
        >
          <InputBox value={String(app.context_max_tokens)} readOnly />
        </Field>
        <Field
          label="Compaction threshold"
          readOnly={readonly.has('context_compaction_threshold')}
        >
          <InputBox value={String(app.context_compaction_threshold)} readOnly />
        </Field>
      </div>

      <h2 className="text-[13px] font-semibold pt-2">Branding</h2>
      <div className="grid grid-cols-2 gap-x-6 gap-y-4">
        <Field label="Agent name" readOnly>
          <InputBox value={cfg.branding.agent_name} readOnly />
        </Field>
        <Field label="UI title" readOnly>
          <InputBox value={cfg.branding.ui_title} readOnly />
        </Field>
        <Field label="Accent color" readOnly>
          <InputBox value={cfg.branding.ui_accent_color} readOnly />
        </Field>
      </div>
    </div>
  )
}

// ── Env tab (read-only) ────────────────────────────────────────────────────

function EnvTabBody({ cfg }: { cfg: FullConfigResponse | null }) {
  if (!cfg) return <div className="px-6 py-4 text-fg-3">Loading…</div>
  return (
    <div className="px-6 py-4 space-y-4 max-w-3xl">
      <div>
        <h2 className="text-[13px] font-semibold">Environment variables</h2>
        <p className="text-[12px] text-fg-2">
          Read-only. Secrets are masked — edit <code>.env</code> on the host
          and restart to change values. An empty circle means the key isn't
          set.
        </p>
      </div>
      <div className="rounded border border-surface-800 divide-y divide-surface-800">
        {cfg.env.map((e) => (
          <div
            key={e.key}
            className="flex items-center gap-3 px-3 py-2 text-[12px]"
          >
            <Circle
              size={8}
              className={cn(
                'flex-shrink-0',
                e.set ? 'fill-acc text-acc' : 'text-fg-3',
              )}
              aria-hidden
            />
            <span className="font-mono text-fg-1 w-56 flex-shrink-0">
              {e.key}
            </span>
            <span className="font-mono text-fg-3 truncate">
              {e.set ? e.value : '—'}
            </span>
            {e.secret && (
              <span className="text-[10px] uppercase tracking-wider text-fg-3 ml-auto flex-shrink-0">
                secret
              </span>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

// ── Prompts tab (read-only) ────────────────────────────────────────────────

function PromptsTabBody({ cfg }: { cfg: FullConfigResponse | null }) {
  const [selected, setSelected] = useState<string | null>(null)
  const [content, setContent] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!selected) return
    let cancelled = false
    setLoading(true)
    setError(null)
    backend.settings
      .prompt(selected)
      .then((r) => {
        if (!cancelled) setContent(r.content)
      })
      .catch((e: unknown) => {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : String(e))
          setContent(null)
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [selected])

  if (!cfg) return <div className="px-6 py-4 text-fg-3">Loading…</div>

  return (
    <div className="px-6 py-4 space-y-4 max-w-4xl">
      <div>
        <h2 className="text-[13px] font-semibold">System prompts</h2>
        <p className="text-[12px] text-fg-2">
          Read-only viewer. Edit the files directly on disk — no write
          endpoint (yet).
        </p>
      </div>
      <div className="flex gap-2 flex-wrap">
        {cfg.prompts.length === 0 && (
          <span className="text-[12px] text-fg-3">No prompts found.</span>
        )}
        {cfg.prompts.map((p) => (
          <button
            key={p.name}
            type="button"
            onClick={() => setSelected(p.name)}
            className={cn(
              'rounded border px-2.5 py-1 text-[12px] font-mono',
              selected === p.name
                ? 'border-acc-line bg-acc-dim text-acc'
                : 'border-surface-800 bg-surface-900 text-fg-1 hover:bg-surface-800',
            )}
          >
            {p.name}{' '}
            <span className="text-fg-3">({(p.size / 1024).toFixed(1)}k)</span>
          </button>
        ))}
      </div>
      {loading && <div className="text-[12px] text-fg-3">Loading…</div>}
      {error && <div className="text-[12px] text-err">{error}</div>}
      {content !== null && !loading && !error && <Code>{content}</Code>}
    </div>
  )
}
