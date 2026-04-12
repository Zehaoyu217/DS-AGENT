import { create } from 'zustand'
import type { ContextSnapshot } from '../lib/api'

interface DevtoolsState {
  isOpen: boolean
  activeTab: 'events' | 'skills' | 'config' | 'wiki' | 'evals' | 'context'
          | 'sop-sessions' | 'sop-judge' | 'sop-prompt' | 'sop-timeline'
  contextSnapshot: ContextSnapshot | null
  selectedTraceId: string | null
  selectedStepId: string | null
  toggle: () => void
  setActiveTab: (tab: DevtoolsState['activeTab']) => void
  setContextSnapshot: (snapshot: ContextSnapshot) => void
  setSelectedTrace: (traceId: string | null) => void
  setSelectedStep: (stepId: string | null) => void
}

export const useDevtoolsStore = create<DevtoolsState>((set) => ({
  isOpen: false,
  activeTab: 'context',
  contextSnapshot: null,
  selectedTraceId: null,
  selectedStepId: null,
  toggle: () => set((s) => ({ isOpen: !s.isOpen })),
  setActiveTab: (tab) => set({ activeTab: tab }),
  setContextSnapshot: (snapshot) => set({ contextSnapshot: snapshot }),
  setSelectedTrace: (traceId) =>
    set({ selectedTraceId: traceId, selectedStepId: null }),
  setSelectedStep: (stepId) => set({ selectedStepId: stepId }),
}))
