import { fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { ThreadList } from "../ThreadList";
import { useChatStore, type Conversation, type Message } from "@/lib/store";
import { useUiStore } from "@/lib/ui-store";

const MS_PER_DAY = 24 * 60 * 60 * 1000;

function makeConv(
  id: string,
  title: string,
  updatedAgoMs: number,
  messages: Message[] = [],
): Conversation {
  const t = Date.now() - updatedAgoMs;
  return {
    id,
    title,
    messages,
    createdAt: t,
    updatedAt: t,
  };
}

function resetStores(conversations: Conversation[] = []): void {
  useChatStore.setState({
    conversations,
    activeConversationId: conversations[0]?.id ?? null,
    draftInput: "",
    toolCallLog: [],
    scratchpad: "",
    todos: [],
    artifacts: [],
    planMode: false,
    searchPanelOpen: false,
  });
  useUiStore.setState({
    v: 1,
    threadW: 240,
    dockW: 320,
    threadsOpen: true,
    dockOpen: true,
    dockTab: "progress",
    density: "default",
    threadsOverridden: false,
    dockOverridden: false,
  });
}

beforeEach(() => {
  vi.useFakeTimers().setSystemTime(new Date("2026-04-18T12:00:00Z"));
});

afterEach(() => {
  vi.useRealTimers();
  vi.restoreAllMocks();
});

describe("ThreadList", () => {
  it("renders Today / This week / Older section labels", () => {
    resetStores([
      makeConv("a", "Today chat", 60 * 60_000),
      makeConv("b", "Week chat", 3 * MS_PER_DAY),
      makeConv("c", "Old chat", 30 * MS_PER_DAY),
    ]);
    render(<ThreadList />);
    expect(screen.getByText("Today")).toBeInTheDocument();
    expect(screen.getByText("This week")).toBeInTheDocument();
    expect(screen.getByText("Older")).toBeInTheDocument();
  });

  it("hides Pinned section when no pinned conversations exist", () => {
    resetStores([makeConv("a", "Only chat", 10 * 60_000)]);
    render(<ThreadList />);
    expect(screen.queryByText("Pinned")).not.toBeInTheDocument();
  });

  it("marks the active conversation with aria-current='true'", () => {
    resetStores([
      makeConv("a", "First", 10 * 60_000),
      makeConv("b", "Second", 20 * 60_000),
    ]);
    useChatStore.setState({ activeConversationId: "b" });
    render(<ThreadList />);
    const activeRow = screen
      .getAllByRole("listitem")
      .find((el) => el.getAttribute("aria-current") === "true");
    expect(activeRow).toBeDefined();
    expect(within(activeRow!).getByText("Second")).toBeInTheDocument();
  });

  it("clicking a row sets it as the active conversation", () => {
    resetStores([
      makeConv("a", "First", 10 * 60_000),
      makeConv("b", "Second", 20 * 60_000),
    ]);
    useChatStore.setState({ activeConversationId: "a" });
    render(<ThreadList />);
    fireEvent.click(screen.getByText("Second"));
    expect(useChatStore.getState().activeConversationId).toBe("b");
  });

  it("collapse chevron calls toggleThreads", () => {
    resetStores([makeConv("a", "First", 5 * 60_000)]);
    render(<ThreadList />);
    expect(useUiStore.getState().threadsOpen).toBe(true);
    fireEvent.click(
      screen.getByRole("button", { name: /collapse thread list/i }),
    );
    expect(useUiStore.getState().threadsOpen).toBe(false);
    expect(useUiStore.getState().threadsOverridden).toBe(true);
  });

  it("shows an empty-state message when there are no conversations", () => {
    resetStores([]);
    render(<ThreadList />);
    expect(screen.getByText(/no chats yet/i)).toBeInTheDocument();
  });

  it("filters conversations by title (case-insensitive substring)", () => {
    resetStores([
      makeConv("a", "Pipeline debug", 10 * 60_000),
      makeConv("b", "Quarterly report", 20 * 60_000),
      makeConv("c", "Pipeline rewrite", 30 * 60_000),
    ]);
    render(<ThreadList />);
    fireEvent.change(screen.getByLabelText(/filter conversations/i), {
      target: { value: "pipe" },
    });
    expect(screen.getByText("Pipeline debug")).toBeInTheDocument();
    expect(screen.getByText("Pipeline rewrite")).toBeInTheDocument();
    expect(screen.queryByText("Quarterly report")).not.toBeInTheDocument();
  });

  it("shows Checkpoints section for frozen conversations and hides them from active sections", () => {
    const frozen = makeConv("f", "Frozen ref", 60 * 60_000);
    frozen.frozenAt = Date.now() - 30 * 60_000;
    const active = makeConv("a", "Active chat", 5 * 60_000);
    resetStores([frozen, active]);
    render(<ThreadList />);
    expect(screen.getByText("Checkpoints")).toBeInTheDocument();
    expect(screen.getByText("Frozen ref")).toBeInTheDocument();
    expect(screen.getByText("Active chat")).toBeInTheDocument();
    expect(screen.getByLabelText("Frozen")).toBeInTheDocument();
  });

  it("Pinned section appears for pinned (non-frozen) conversations", () => {
    const pinned = makeConv("p", "Pinned chat", 10 * 60_000);
    pinned.pinned = true;
    resetStores([pinned, makeConv("o", "Other", 20 * 60_000)]);
    render(<ThreadList />);
    expect(screen.getByText("Pinned")).toBeInTheDocument();
    expect(screen.getByLabelText("Pinned")).toBeInTheDocument();
  });

  it("MoreMenu opens and triggers setConversationPinned action", async () => {
    resetStores([makeConv("a", "Target", 10 * 60_000)]);
    const setConversationPinned = vi
      .fn<(id: string, pinned: boolean) => Promise<void>>()
      .mockResolvedValue();
    useChatStore.setState({ setConversationPinned });
    render(<ThreadList />);
    fireEvent.click(screen.getByLabelText(/more options for target/i));
    fireEvent.click(screen.getByRole("menuitem", { name: /^pin$/i }));
    expect(setConversationPinned).toHaveBeenCalledWith("a", true);
  });
});
