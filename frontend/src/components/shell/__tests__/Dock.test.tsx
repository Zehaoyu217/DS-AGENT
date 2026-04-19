import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { Dock } from "../Dock";
import { useUiStore } from "@/lib/ui-store";
import { useChatStore } from "@/lib/store";

// TraceRail pulls from right-rail-store + renders mode children; stub it so
// this test stays focused on the Dock shell (tabs, resizer, close).
vi.mock("@/components/cockpit/TraceRail", () => ({
  TraceRail: () => <div data-testid="trace-rail">TraceRail</div>,
}));

function resetUi(): void {
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
  useChatStore.setState({
    toolCallLog: [],
    conversations: [],
    activeConversationId: null,
  });
}

beforeEach(() => {
  resetUi();
});

describe("Dock", () => {
  it("renders three tabs with Progress selected by default", () => {
    render(<Dock />);
    expect(
      screen.getByRole("tab", { name: "Progress", selected: true }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("tab", { name: "Context", selected: false }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("tab", { name: "Artifacts", selected: false }),
    ).toBeInTheDocument();
  });

  it("clicking Context switches the active tab", async () => {
    const user = userEvent.setup();
    render(<Dock />);
    await user.click(screen.getByRole("tab", { name: "Context" }));
    expect(useUiStore.getState().dockTab).toBe("context");
  });

  it("mounts TraceRail when dockTab=progress", () => {
    render(<Dock />);
    expect(screen.getByTestId("trace-rail")).toBeInTheDocument();
  });

  it("renders Context stub when dockTab=context", () => {
    useUiStore.setState({ dockTab: "context" });
    render(<Dock />);
    expect(screen.getByText(/context snapshot/i)).toBeInTheDocument();
  });

  it("collapse chevron calls toggleDock", async () => {
    const user = userEvent.setup();
    render(<Dock />);
    expect(useUiStore.getState().dockOpen).toBe(true);
    await user.click(screen.getByRole("button", { name: /collapse dock/i }));
    expect(useUiStore.getState().dockOpen).toBe(false);
    expect(useUiStore.getState().dockOverridden).toBe(true);
  });

  it("includes a resizer with inverted drag semantics", () => {
    render(<Dock />);
    const sep = screen.getByRole("separator", { name: /resize dock/i });
    expect(sep).toHaveAttribute("aria-valuemin", "240");
    expect(sep).toHaveAttribute("aria-valuemax", "480");
  });
});
