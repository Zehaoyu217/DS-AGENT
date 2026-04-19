/**
 * ThreadList — the 160–360px secondary column between the IconRail and the
 * Conversation pane. Lists conversations grouped by recency (Pinned / Today /
 * This week / Older), with an active-row indicator, a "+ new" button that
 * calls the backend `createConversationRemote`, and a right-edge drag handle
 * (Resizer) that binds to `ui-store.threadW`.
 *
 * Reads conversations from `useChatStore`. Reads width / visibility controls
 * from `useUiStore`. Keeps its own UI-only local state (the errorless toast
 * after a failed remote create → falls back to local `createConversation`).
 */

import { useMemo, useState, type KeyboardEvent } from "react";
import { ChevronLeft, Pin, Plus, Archive } from "lucide-react";
import { useChatStore, type Conversation } from "@/lib/store";
import { extractTextContent } from "@/lib/utils";
import {
  useUiStore,
  THREAD_W_MIN,
  THREAD_W_MAX,
  selectThreadW,
} from "@/lib/ui-store";
import { cn } from "@/lib/utils";
import { Resizer } from "./Resizer";

interface ThreadSection {
  id: "pinned" | "today" | "week" | "older";
  label: string;
  items: Conversation[];
}

const MS_PER_DAY = 24 * 60 * 60 * 1000;
const WEEK_MS = 7 * MS_PER_DAY;

function startOfDay(ts: number): number {
  const d = new Date(ts);
  d.setHours(0, 0, 0, 0);
  return d.getTime();
}

function relativeTime(ts: number, now: number): string {
  const diff = now - ts;
  if (diff < 60_000) return "now";
  if (diff < 3_600_000) return `${Math.floor(diff / 60_000)}m`;
  if (diff < MS_PER_DAY) return `${Math.floor(diff / 3_600_000)}h`;
  if (diff < 2 * MS_PER_DAY) return "yest";
  if (diff < WEEK_MS) return `${Math.floor(diff / MS_PER_DAY)}d`;
  if (diff < 4 * WEEK_MS) return `${Math.floor(diff / WEEK_MS)}w`;
  return new Date(ts).toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
  });
}

interface PinnedMap {
  [id: string]: boolean;
}

function groupConversations(
  conversations: Conversation[],
  pinned: PinnedMap,
  now: number,
): ThreadSection[] {
  const sod = startOfDay(now);
  const weekCut = sod - 6 * MS_PER_DAY;

  const buckets: Record<ThreadSection["id"], Conversation[]> = {
    pinned: [],
    today: [],
    week: [],
    older: [],
  };

  for (const c of conversations) {
    if (pinned[c.id]) {
      buckets.pinned.push(c);
      continue;
    }
    const t = c.updatedAt;
    if (t >= sod) buckets.today.push(c);
    else if (t >= weekCut) buckets.week.push(c);
    else buckets.older.push(c);
  }

  const sortDesc = (a: Conversation, b: Conversation): number =>
    b.updatedAt - a.updatedAt;
  buckets.pinned.sort(sortDesc);
  buckets.today.sort(sortDesc);
  buckets.week.sort(sortDesc);
  buckets.older.sort(sortDesc);

  return [
    { id: "pinned", label: "Pinned", items: buckets.pinned },
    { id: "today", label: "Today", items: buckets.today },
    { id: "week", label: "This week", items: buckets.week },
    { id: "older", label: "Older", items: buckets.older },
  ];
}

function previewOf(conv: Conversation): string {
  const last = conv.messages[conv.messages.length - 1];
  if (!last) return "no messages yet";
  const text = extractTextContent(last.content).trim().replace(/\s+/g, " ");
  return text.length > 0 ? text : `${last.role} · ${last.status}`;
}

export function ThreadList() {
  const conversations = useChatStore((s) => s.conversations);
  const activeId = useChatStore((s) => s.activeConversationId);
  const setActive = useChatStore((s) => s.setActiveConversation);
  const createLocal = useChatStore((s) => s.createConversation);
  const createRemote = useChatStore((s) => s.createConversationRemote);

  const threadW = useUiStore(selectThreadW);
  const setThreadW = useUiStore((s) => s.setThreadW);
  const toggleThreads = useUiStore((s) => s.toggleThreads);

  // Pinned state is UI-only for step 1 — not persisted to backend yet.
  const [pinned] = useState<PinnedMap>({});
  const [creating, setCreating] = useState(false);

  const sections = useMemo(
    () => groupConversations(conversations, pinned, Date.now()),
    [conversations, pinned],
  );

  async function handleCreate() {
    if (creating) return;
    setCreating(true);
    try {
      await createRemote("New chat");
    } catch {
      // Offline or backend is down — fall back to a local-only conversation
      // so the user can keep working. The backend will pick it up on next sync.
      createLocal();
    } finally {
      setCreating(false);
    }
  }

  function handleRowKey(event: KeyboardEvent<HTMLButtonElement>, id: string) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      setActive(id);
    }
  }

  return (
    <aside
      className="relative flex h-full flex-col border-r border-line-2 bg-bg-1"
      style={{ width: threadW, minWidth: THREAD_W_MIN, maxWidth: THREAD_W_MAX }}
      aria-label="Conversation list"
    >
      {/* Header */}
      <div className="flex items-center gap-2 px-3 pt-3 pb-2">
        <span className="label-cap flex-1">Chats</span>
        <button
          type="button"
          onClick={handleCreate}
          disabled={creating}
          aria-label="New chat"
          className={cn(
            "inline-flex h-6 w-6 items-center justify-center rounded",
            "text-fg-2 hover:text-acc hover:bg-bg-2 focus-ring",
            "disabled:opacity-50 disabled:cursor-not-allowed",
          )}
        >
          <Plus className="h-3.5 w-3.5" aria-hidden />
        </button>
        <button
          type="button"
          onClick={toggleThreads}
          aria-label="Collapse thread list"
          className={cn(
            "inline-flex h-6 w-6 items-center justify-center rounded",
            "text-fg-3 hover:text-fg-0 hover:bg-bg-2 focus-ring",
          )}
        >
          <ChevronLeft className="h-3.5 w-3.5" aria-hidden />
        </button>
      </div>

      {/* Body */}
      <div
        className="flex-1 overflow-y-auto"
        role="list"
        aria-label="Conversations"
      >
        {sections.map((section) => {
          // Pinned stays hidden when empty; the other three always render so
          // the user learns the structure. Empty groups render a single muted
          // line rather than a blank band.
          if (section.id === "pinned" && section.items.length === 0) {
            return null;
          }
          return (
            <div key={section.id} className="pb-1">
              <div className="flex items-center justify-between px-3 pt-2 pb-1">
                <span className="label-cap">{section.label}</span>
                <span className="mono text-[10px] text-fg-3">
                  {section.items.length}
                </span>
              </div>
              {section.items.length === 0 ? (
                <div className="px-3 pb-1 text-[11.5px] text-fg-3 italic">
                  empty
                </div>
              ) : (
                section.items.map((conv) => {
                  const isActive = conv.id === activeId;
                  const isPinned = Boolean(pinned[conv.id]);
                  return (
                    <button
                      key={conv.id}
                      type="button"
                      role="listitem"
                      aria-current={isActive ? "true" : undefined}
                      onClick={() => setActive(conv.id)}
                      onKeyDown={(e) => handleRowKey(e, conv.id)}
                      className={cn(
                        "relative w-full px-3 py-2 text-left transition-colors",
                        "focus-ring",
                        isActive
                          ? "bg-acc-dim text-fg-0"
                          : "text-fg-1 hover:bg-bg-2",
                      )}
                    >
                      {isActive && (
                        <span
                          aria-hidden
                          className="pointer-events-none absolute inset-y-1.5 left-0 w-0.5 bg-acc"
                        />
                      )}
                      <div className="flex items-center gap-1.5">
                        {isPinned && (
                          <Pin
                            className="h-2.5 w-2.5 shrink-0 text-acc"
                            aria-label="Pinned"
                          />
                        )}
                        <span
                          className={cn(
                            "flex-1 truncate text-[12.5px]",
                            isActive ? "font-medium" : "font-normal",
                          )}
                        >
                          {conv.title}
                        </span>
                        <span className="mono text-[10.5px] text-fg-3 shrink-0">
                          {relativeTime(conv.updatedAt, Date.now())}
                        </span>
                      </div>
                      <div className="mt-0.5 truncate text-[11.5px] text-fg-3">
                        {previewOf(conv)}
                      </div>
                    </button>
                  );
                })
              )}
            </div>
          );
        })}
        {conversations.length === 0 && (
          <div className="px-3 py-8 text-center text-[12px] text-fg-3">
            <div className="mb-1">No chats yet</div>
            <div className="mono text-[10.5px]">⌘N to start</div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="flex h-10 items-center gap-2 border-t border-line-2 px-3">
        <button
          type="button"
          className={cn(
            "inline-flex items-center gap-1.5 text-[11.5px] text-fg-2",
            "hover:text-fg-0 focus-ring rounded",
          )}
          aria-label="Archive"
        >
          <Archive className="h-2.5 w-2.5" aria-hidden />
          <span>Archive</span>
        </button>
      </div>

      {/* Right-edge resizer */}
      <div
        className="absolute top-0 right-0 h-full"
        style={{ transform: "translateX(2px)" }}
      >
        <Resizer
          axis="x"
          min={THREAD_W_MIN}
          max={THREAD_W_MAX}
          value={threadW}
          onChange={setThreadW}
          ariaLabel="Resize thread list"
          className="h-full"
        />
      </div>
    </aside>
  );
}
