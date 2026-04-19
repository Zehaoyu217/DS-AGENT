/**
 * Dock — the 240–480px tertiary column on the far right, tabbed into
 * Progress / Context / Artifacts. Progress hosts the live TraceRail. Context
 * and Artifacts are handoff-styled stubs for step 1 — the full panels land
 * in later steps.
 *
 * Width + tab selection + visibility are persisted via `ui-store`. The left
 * edge has an inverted Resizer (dragging left grows the dock).
 */

import { ChevronRight } from "lucide-react";
import {
  useUiStore,
  DOCK_W_MIN,
  DOCK_W_MAX,
  selectDockW,
  selectDockTab,
  type DockTab,
} from "@/lib/ui-store";
import { cn } from "@/lib/utils";
import { TraceRail } from "@/components/cockpit/TraceRail";
import { Resizer } from "./Resizer";

interface TabDef {
  id: DockTab;
  label: string;
}

const TABS: readonly TabDef[] = [
  { id: "progress", label: "Progress" },
  { id: "context", label: "Context" },
  { id: "artifacts", label: "Artifacts" },
] as const;

function DockContextStub() {
  return (
    <div className="flex h-full flex-col gap-3 p-4">
      <div className="label-cap">Context snapshot</div>
      <div
        className="stripe-ph h-40"
        aria-label="Context panel coming in step 3"
      >
        context layers · 48.2k / 200k
      </div>
      <div className="mono text-[10.5px] text-fg-3">
        coming in step 3 · full layer-by-layer breakdown
      </div>
    </div>
  );
}

function DockArtifactsStub() {
  const tiles = ["report", "chart", "data", "model", "code", "file"];
  return (
    <div className="flex h-full flex-col gap-3 p-4">
      <div className="label-cap">Artifacts</div>
      <div className="grid grid-cols-3 gap-2">
        {tiles.map((t) => (
          <div
            key={t}
            className="stripe-ph aspect-square text-[10.5px]"
            aria-label={`${t} placeholder`}
          >
            {t}
          </div>
        ))}
      </div>
      <div className="mono text-[10.5px] text-fg-3">
        coming in step 4 · previews + drawer
      </div>
    </div>
  );
}

export function Dock() {
  const dockW = useUiStore(selectDockW);
  const setDockW = useUiStore((s) => s.setDockW);
  const dockTab = useUiStore(selectDockTab);
  const setDockTab = useUiStore((s) => s.setDockTab);
  const toggleDock = useUiStore((s) => s.toggleDock);

  return (
    <aside
      className="relative flex h-full flex-col border-l border-line-2 bg-bg-1"
      style={{ width: dockW, minWidth: DOCK_W_MIN, maxWidth: DOCK_W_MAX }}
      aria-label="Agent dock"
    >
      {/* Left-edge resizer (invert: drag toward the center grows dock) */}
      <div
        className="absolute top-0 left-0 h-full"
        style={{ transform: "translateX(-2px)" }}
      >
        <Resizer
          axis="x"
          min={DOCK_W_MIN}
          max={DOCK_W_MAX}
          value={dockW}
          onChange={setDockW}
          invert
          ariaLabel="Resize dock"
          className="h-full"
        />
      </div>

      {/* Tab bar */}
      <div
        className="flex h-9 items-center border-b border-line-2 px-2"
        role="tablist"
        aria-label="Dock sections"
      >
        {TABS.map((tab) => {
          const on = dockTab === tab.id;
          return (
            <button
              key={tab.id}
              type="button"
              role="tab"
              aria-selected={on}
              aria-controls={`dock-panel-${tab.id}`}
              onClick={() => setDockTab(tab.id)}
              className={cn(
                "relative inline-flex items-center px-3 py-2",
                "text-[11.5px] transition-colors focus-ring rounded-sm",
                on
                  ? "text-fg-0 font-medium"
                  : "text-fg-2 hover:text-fg-0",
              )}
            >
              {tab.label}
              {on && (
                <span
                  aria-hidden
                  className="pointer-events-none absolute -bottom-px left-2 right-2 h-0.5 bg-acc"
                />
              )}
            </button>
          );
        })}
        <div className="flex-1" />
        <button
          type="button"
          onClick={toggleDock}
          aria-label="Collapse dock"
          className={cn(
            "inline-flex h-6 w-6 items-center justify-center rounded",
            "text-fg-3 hover:text-fg-0 hover:bg-bg-2 focus-ring",
          )}
        >
          <ChevronRight className="h-3.5 w-3.5" aria-hidden />
        </button>
      </div>

      {/* Tab body */}
      <div
        id={`dock-panel-${dockTab}`}
        role="tabpanel"
        aria-labelledby={`dock-tab-${dockTab}`}
        className="flex-1 min-h-0 overflow-hidden"
      >
        {dockTab === "progress" && (
          <div className="h-full overflow-hidden">
            <TraceRail />
          </div>
        )}
        {dockTab === "context" && <DockContextStub />}
        {dockTab === "artifacts" && <DockArtifactsStub />}
      </div>
    </aside>
  );
}
