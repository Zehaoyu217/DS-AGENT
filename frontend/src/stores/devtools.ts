import { create } from 'zustand'
import type { ContextSnapshot } from '../lib/api'

interface DevtoolsState {
  isOpen: boolean
  activeTab: 'events' | 'skills' | 'config' | 'wiki' | 'evals' | 'context'
          | 'sop-sessions' | 'sop-judge' | 'sop-prompt' | 'sop-timeline'
  contextSnapshot: ContextSnapshot | null
  toggle: () => void
  setActiveTab: (tab: DevtoolsState['activeTab']) => void
  setContextSnapshot: (snapshot: ContextSnapshot) => void
}

export const useDevtoolsStore = create<DevtoolsState>((set) => ({
  isOpen: false,
  activeTab: 'context',
  contextSnapshot: null,
  toggle: () => set((s) => ({ isOpen: !s.isOpen })),
  setActiveTab: (tab) => set({ activeTab: tab }),
  setContextSnapshot: (snapshot) => set({ contextSnapshot: snapshot }),
}))
