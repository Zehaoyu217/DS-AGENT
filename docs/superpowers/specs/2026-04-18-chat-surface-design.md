# DS-Agent Chat Surface Rebuild — Design Spec

**Sub-project 2 of 5** (Shell Foundation → **Chat Surface** → Dock Progress Tab → ThreadList/Palette → Tweaks Panel)
**Status:** approved (auto-approved 2026-04-18)
**Source:** `design_handoff_ds_agent/chat.jsx` + `tokens.css`
**Prior:** `docs/superpowers/specs/2026-04-18-shell-foundation-design.md` (step 1 — shipped)

## Goal

Bring the conversation pane to full pixel parity with the handoff `chat.jsx`:

- A thread-header toolbar with sidebar toggle, inline-editable session title, Search / Fork / Export / Progress-dock toggle / More.
- A card-style composer with attach / @ / # / mic icon row, inline model picker, Extended-thinking toggle, Plan toggle, ⌘↵ hint, Send / Stop.
- Avatar-bubble message rendering with name + timestamp + copy/more hover actions, markdown body, inline tool chips, artifact pills, callouts, subagent cards, attached-file chips.

Replaces the TopHUD + SessionDropdown affordances that were retired in sub-project 1, and refactors the chat surface into small, testable files (≤200 lines each).

## Non-goals

- Dock Progress tab redesign (sub-project 3).
- ThreadList refinements / Command Palette rewrite (sub-project 4).
- Tweaks / density panel (sub-project 5).
- Backend changes to agent streaming or tool-call schema, except the minimal additions listed under **Data model changes**.

## Users & success criteria

DS power users expect:

- **Title-rename without leaving the keyboard** — click title, type, Enter.
- **Model switching in ≤2 clicks** — composer-footer picker, keyboard-navigable.
- **Visible progress without scrolling** — tool chips inline in the current turn; full Trace in the Dock when they want it.
- **No dropped state** — per-conversation model, extended-thinking, and plan-mode persist across reloads and session switches.
- **Light + dark first-class** — every new surface reads from the oklch token system already in `tokens.css`; no hard-coded hex.

Ship criteria:

- `pnpm typecheck` + `pnpm test` green.
- E2E shell-foundation spec extended with ≥6 new assertions covering header, composer, and message rendering.
- No individual new file exceeds 200 lines. No single file exceeds the 800-line project guard.
- Visual snapshots at 1100px and 1440px × (light, dark) captured for `ChatPane` empty state and a thread with tools+artifacts+callouts. (Baselines land; CI review flow still deferred per sub-project 1.)

---

## Architecture

```
AppShell (from sub-project 1)
└── SectionContent
    └── [activeSection === 'chat'] → ChatPane  ← NEW entry point
         ├── ChatHeader
         │    ├── SidebarToggle          (ui-store: threadsOpen)
         │    ├── NewChatButton          (fades in when threadsOpen===false)
         │    ├── divider
         │    ├── TitleEditor            (inline-edit; writes conversation.title)
         │    └── HeaderActions
         │         ├── SearchButton       (opens palette; ⌘K hint)
         │         ├── ForkButton         (duplicate-conversation)
         │         ├── ExportMenuButton   (.md · .json · .html)
         │         ├── ProgressToggle     (shows only if dockOpen===false; pulse dot)
         │         └── MoreMenuButton     (rename · archive · duplicate · delete)
         ├── ChatWindow (existing, lightly refactored)
         │    ├── empty → SuggestedPrompts (restyled)
         │    └── VirtualMessageList
         │         └── Message              ← NEW, replaces MessageBubble
         │              ├── Avatar           (gradient for user, --acc solid for agent)
         │              ├── MessageHeader    (name · timestamp · copy · more)
         │              ├── MarkdownContent  (existing; inline `code` → acc pill; **bold**)
         │              ├── Callout[]        (derived from tool err + callout blocks)
         │              ├── ToolChipRow      (filter toolCallLog by messageId)
         │              ├── ArtifactPillRow  (filter artifacts by message.artifactIds)
         │              ├── SubagentCard[]   (existing a2a)
         │              └── AttachedFileChip[] (user messages only)
         └── Composer
              ├── SlashMenu (keep behavior, restyle to card)
              ├── AttachedFilesPreview
              ├── textarea (auto-resize, existing)
              └── ComposerActions
                   ├── IconRow: AttachButton · MentionButton · SkillButton · VoiceButton
                   ├── divider
                   ├── ModelPicker
                   ├── ExtendedToggle
                   ├── PlanToggle (existing behavior)
                   ├── ⌘↵ hint
                   └── SendButton / StopButton
```

### File layout

```
frontend/src/components/chat/
├── ChatPane.tsx                    ← rendered by AppShell "chat" section
├── ChatWindow.tsx                  ← existing; lightly refactored (remove empty-state heading)
├── VirtualMessageList.tsx          ← existing; now renders <Message>, not <MessageBubble>
├── SuggestedPrompts.tsx            ← existing; restyled via tokens
├── MarkdownContent.tsx             ← existing
├── SubagentCard.tsx                ← existing
├── VegaChart.tsx                   ← existing
├── MermaidDiagram.tsx              ← existing
├── ScrollToBottom.tsx              ← existing
│
├── header/
│   ├── ChatHeader.tsx
│   ├── TitleEditor.tsx
│   ├── HeaderActions.tsx
│   ├── SearchButton.tsx
│   ├── ForkButton.tsx
│   ├── ExportMenu.tsx
│   ├── ProgressToggle.tsx
│   └── MoreMenu.tsx
│
├── composer/
│   ├── Composer.tsx
│   ├── ComposerActions.tsx
│   ├── IconRow.tsx
│   ├── AttachButton.tsx
│   ├── MentionButton.tsx
│   ├── SkillButton.tsx
│   ├── VoiceButton.tsx
│   ├── ModelPicker.tsx
│   ├── ExtendedToggle.tsx
│   ├── PlanToggle.tsx           ← split out of ChatInput
│   ├── SlashMenu.tsx            ← split out of ChatInput
│   ├── AttachedFilesPreview.tsx
│   └── useComposerSubmit.ts     ← handleSubmit logic, extracted hook
│
└── message/
    ├── Message.tsx
    ├── Avatar.tsx
    ├── MessageHeader.tsx
    ├── ToolChip.tsx
    ├── ToolChipRow.tsx
    ├── ArtifactPill.tsx
    ├── ArtifactPillRow.tsx
    ├── Callout.tsx
    └── AttachedFileChip.tsx
```

**Retired:**

- `components/cockpit/ChatMain.tsx` — replaced by `components/chat/ChatPane.tsx`.
- `components/chat/ChatInput.tsx` — logic migrated to `composer/` sub-modules + `useComposerSubmit`.
- `components/chat/MessageBubble.tsx` — replaced by `message/Message.tsx` tree.
- `components/chat/ChatLayout.tsx` — unused after ChatPane lands (verify via grep before delete).

**Kept (no API changes):** `MarkdownContent`, `SubagentCard`, `VegaChart`, `MermaidDiagram`, `ScrollToBottom`, `VirtualMessageList` (consumer swap only), `SuggestedPrompts`, `CodeBlock`, `ThinkingBlock`, `FileAttachment` (if referenced).

---

## Data model changes

Minimal, additive. No breaking store migrations.

### `ToolCallLogEntry` (in `lib/store.ts`)

```ts
interface ToolCallLogEntry {
  id: string
  step: number
  name: string
  inputPreview: string
  status: 'pending' | 'ok' | 'err' | 'warn'
  preview?: string
  stdout?: string
  startedAt: number
  finishedAt?: number
  artifactIds?: string[]
  rows?: string               // NEW — e.g. "248,913 × 42", displayed on the chip
  messageId?: string          // NEW — assistant message that caused this tool call
}
```

`ChatInput.handleSubmit` (migrated into `useComposerSubmit`) sets `messageId: assistantId` when calling `pushToolCall(...)`. `ToolChipRow` filters `toolCallLog` by `messageId`.

### `Conversation` (in `lib/store.ts`)

```ts
interface Conversation {
  // existing fields …
  model?: string              // NEW — active OpenRouter model id
  extendedThinking?: boolean  // NEW — reasoning-tokens toggle
  attachedFiles?: AttachedFile[] // NEW — pending attachments for next turn
}

interface AttachedFile {
  id: string
  name: string
  size: number
  mimeType: string
  contextRefId?: string        // assigned after context-endpoint upload
}
```

New store actions:

- `updateConversationTitle(id, title)` — trims, caps at 200 chars; persists in the Zustand-persisted store only. Backend has no conversation-update endpoint; rename is client-side today and will sync automatically when one lands (no schema change required).
- `updateConversationModel(id, modelId)` — persists choice per conv.
- `setConversationExtendedThinking(id, enabled)` — persists.
- `addAttachedFile(convId, file)` / `removeAttachedFile(convId, fileId)` / `clearAttachedFiles(convId)` — managed by `AttachButton` + `useComposerSubmit`.
- `forkConversation(convId, throughMessageId?)` — creates new conversation; copies messages up to `throughMessageId` (or all); appends " (fork)" to title; returns new id.

### `Message` (in `lib/store.ts`)

No schema change; existing `artifactIds` + `content: ContentBlock[]` covers the new surfaces. `callout` is added as a ContentBlock variant:

```ts
type ContentBlock =
  | { type: 'text'; text: string }
  | { type: 'tool_use'; id?: string; name: string; input?: unknown }
  | { type: 'chart'; spec: unknown }
  | { type: 'a2a'; task: string; artifactId: string; summary: string; status: 'pending' | 'complete' | 'error' }
  | { type: 'callout'; kind: 'warn' | 'err' | 'info'; label: string; text: string }  // NEW
```

Callouts are also auto-derived at render-time from any preceding `tool_result` with `status === 'err'` that has no surrounding assistant text — the Message tree injects an ephemeral warn/err callout from the tool result's `preview` + name. Server emission is forward-compat.

### `ui-store` (existing)

`dockOpen`, `dockOverridden`, `threadsOpen` — already exist. No additions.

### `right-rail-store` (existing)

`traceTab` — already exists. Scroll-to-entry uses a new `scrollToTrace(entryId: string)` action (dispatched via custom event so the Dock can listen without importing Message components).

---

## API surface (backend)

No new endpoints. Consumed:

- `GET /api/models` — consumed via existing `backend.models.list()`. **Read-only consumption, `models_api.py` is untouched.** Returns a `ModelsResponse` whose shape the picker already renders.
- `POST /api/context/upload` — existing context upload endpoint; `AttachButton` calls this and stores the returned `contextRefId` in `AttachedFile`. If the endpoint is absent in a given deployment the attach button is still functional for text-only flows but the attach ref is `undefined` and the backend's streaming endpoint receives the raw file contents inline (size-capped).
- Streaming endpoint — `streamChatMessage` already accepts `planMode`. Extend its options type with `model?: string; extendedThinking?: boolean`; the backend reads these from the request body if present and ignores them otherwise (backward compatible).

If `/api/models` is unreachable, `ModelPicker` falls back to a static default:

```ts
const FALLBACK_MODELS = [{ id: 'claude-sonnet-4-6', label: 'Sonnet 4.6', capabilities: ['thinking', 'tools'] }]
```

---

## Keyboard shortcuts

Additive. No conflicts with existing `mod+k / n / b / , / l / / / shift+[ / shift+] / shift+f / 1..9`.

| Combo | Action |
|-------|--------|
| `Enter` (composer) | Send (existing) |
| `Shift+Enter` (composer) | Newline (existing) |
| `mod+Enter` (composer) | Send (mirrors handoff ⌘↵ hint — idempotent w/ `Enter`) |
| `Esc` (TitleEditor) | Cancel edit, revert |
| `Enter` (TitleEditor) | Commit edit |
| `mod+Shift+M` | Cycle model in ModelPicker |
| `mod+Shift+E` | Toggle Extended thinking |

`mod+Shift+M` and `mod+Shift+E` register via `useKeyboardShortcuts` + `useCommandRegistry`, alongside existing commands. No conflicts with the `OPEN_SECTION_*` / `TOGGLE_DOCK` shortcuts added in sub-project 1.

---

## Styling

- All colors read from `tokens.css` CSS vars (`--bg-0/1/2`, `--fg-0/1/2/3`, `--line`, `--line-2`, `--acc`, `--acc-dim`, `--acc-fg`, `--ok`, `--warn`, `--err`, `--info`, `--shadow-1`, `--shadow-2`).
- No hard-coded hex. No legacy `.light`-class branches.
- Monospace for: timestamps, tool-chip args, file sizes, keyboard hint labels, model pill (mono micro-caps).
- Sans (Inter) for: message body, callout text, title, button labels.
- Font feature flags inherited from `globals.css` (`cv11, ss01, ss03` sans; `zero, ss01, cv01` mono).
- Motion: rely on the handoff keyframes already in `tokens.css` (`pulse`, `pulseRing`, `fadeIn`, `scaleIn`, `caret`, `drawCheck`) — **no new keyframes**.
- Density: Messages use `html[data-density="compact|cozy"]`-aware spacing, already wired in sub-project 1.

---

## Error handling

| Failure | Behavior |
|---------|----------|
| Model list fetch fails | Fall back to static list; muted `!` warning under picker; retry on next open. |
| Context upload fails | Attached-file chip shows red border + tooltip; removed on retry or manual dismiss. No blocking of text-only send. |
| Fork backend-sync fails | Client-side new conversation persists; toast "Saved locally — will sync on reconnect." |
| Export fails | Toast with `err.message`; no partial download written. |
| Voice unsupported | `VoiceButton` hidden on mount (feature-detect `window.SpeechRecognition \|\| window.webkitSpeechRecognition`). |
| Voice permission denied | Button stays visible but styled `disabled`; tooltip explains. |
| Title edit empty | Revert to previous title on blur / Enter. |
| Title edit > 200 chars | Truncate on commit; flash the input once. |
| Tool chip has no matching trace entry | Click still opens dock; log a dev warning; no user-facing error. |
| Artifact pill refers to missing artifact | Render as disabled pill with `— removed` suffix. |

---

## Testing

### Unit (Vitest + RTL)

- `TitleEditor` — enters edit mode on click, commits on Enter, reverts on Esc, truncates >200.
- `ModelPicker` — renders list, selects, persists via store action, fallback when fetch throws.
- `ExtendedToggle` — disabled when model lacks 'thinking' capability.
- `PlanToggle` — keeps existing `togglePlanMode` contract.
- `VoiceButton` — hides when SpeechRecognition undefined; starts/stops on tap; writes transcript.
- `AttachButton` — uploads file, writes to `attachedFiles`, surfaces error state.
- `SlashMenu` — preserves existing keyboard navigation + selection lock.
- `ToolChip` — dot color by status; click dispatches `scrollToTrace` event.
- `ArtifactPill` — click sets `dockOpen=true` + `traceTab='context'` (upgrades to `artifacts` in sub-project 3); hover shows preview for images.
- `Callout` — renders warn/err/info variants with correct `color-mix` borders.
- `forkConversation` store action — copies messages up through target; appends " (fork)".

### Integration

- `Composer` end-to-end: slash menu → pick → lock → Enter submits message; attach file → shown as chip → cleared on submit.
- `Message` with tools + artifacts + callouts renders in correct order: `markdown → callouts → tools → artifacts → subagents → attached`.
- `ChatHeader` fork + export: fork creates new conv and switches to it; export markdown matches reference fixture.

### E2E (Playwright)

Extend `frontend/e2e/shell-foundation.spec.ts` (or add `chat-surface.spec.ts`):

- Header renders 6 actions after load.
- Title click → editable → Enter commits + persists across reload.
- `mod+Shift+M` cycles model; selection persists across reload.
- `mod+Shift+E` toggles Extended badge.
- Composer shows model picker with fallback list when backend unavailable.
- Sending a turn shows streaming cursor, then tool chips, then artifact pill; clicking artifact pill opens dock artifacts tab.
- Visual snapshots: empty state + rich thread, light + dark, 1100 + 1440.

---

## Rollout

One branch, one PR. No feature flag — the chat pane is rebuilt in place. Deleted files are removed in the same commit as their replacements land. Tests are updated in the same commit.

## Open questions (deferred)

None for this sub-project. Items punted to later steps:

- Sub-project 3 — Dock Progress tab redesign; the `ArtifactPillRow`'s `traceTab` target switches from `'context'` to `'artifacts'` when that tab lands.
- Sub-project 4 — Palette rewrite may introduce a richer Search affordance; Header's `SearchButton` then calls into the new palette API instead of the current `openHelp`-style open.
- Sub-project 5 — Tweaks panel will expose density controls surfaced today only via `html[data-density]`.
