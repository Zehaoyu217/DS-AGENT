/**
 * AppShell — the four-pane chrome that every section lives inside:
 *
 *   [ IconRail | ThreadList? | Conversation (children) | Dock? ]
 *
 * ThreadList and Dock only mount when `activeSection === 'chat'` AND the
 * corresponding open flag is true. Auto-collapse at narrow widths is driven
 * by `useAutoCollapse` mounted here once for the whole app.
 */

import type { ReactNode } from "react";
import { IconRail } from "@/components/layout/IconRail";
import { useAutoCollapse } from "@/hooks/useAutoCollapse";
import { useChatStore } from "@/lib/store";
import {
  useUiStore,
  selectThreadsOpen,
  selectDockOpen,
} from "@/lib/ui-store";
import { ThreadList } from "./ThreadList";
import { Dock } from "./Dock";

interface AppShellProps {
  children: ReactNode;
}

export function AppShell({ children }: AppShellProps) {
  useAutoCollapse();

  const activeSection = useChatStore((s) => s.activeSection);
  const threadsOpen = useUiStore(selectThreadsOpen);
  const dockOpen = useUiStore(selectDockOpen);

  const isChat = activeSection === "chat";
  const showThreads = isChat && threadsOpen;
  const showDock = isChat && dockOpen;

  return (
    <div
      className="flex h-dvh overflow-hidden bg-bg-0 text-fg-0"
      data-app-shell
    >
      <IconRail />
      {showThreads && <ThreadList />}
      <main
        className="flex-1 min-w-0 overflow-hidden"
        aria-label="Main content"
      >
        {children}
      </main>
      {showDock && <Dock />}
    </div>
  );
}
