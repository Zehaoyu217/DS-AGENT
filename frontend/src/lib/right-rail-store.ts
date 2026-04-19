import { create } from 'zustand'
import { createJSONStorage, persist } from 'zustand/middleware'

export type TraceTab = 'timeline' | 'context' | 'raw'

interface RightRailState {
  traceTab: TraceTab
  setTraceTab: (tab: TraceTab) => void
}

// Persists trace-tab selection only; the old `mode`/cycle/toggle state
// belonged to the retired right-rail drawer and now lives in the Dock shell.
export const useRightRailStore = create<RightRailState>()(
  persist(
    (set) => ({
      traceTab: 'timeline',
      setTraceTab: (traceTab) => set({ traceTab }),
    }),
    {
      name: 'cc-right-rail',
      storage: createJSONStorage(() => localStorage),
    },
  ),
)
