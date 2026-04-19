import { SurfacePage } from '@/components/surface/SurfacePage'
import { AgentsSection } from '@/sections/AgentsSection'
import { SkillsSection } from '@/sections/SkillsSection'
import { PromptsSection } from '@/sections/PromptsSection'

export function AgentsSurface() {
  return (
    <SurfacePage eyebrow="LIBRARY" title="Agents">
      <AgentsSection />
    </SurfacePage>
  )
}

export function SkillsSurface() {
  return (
    <SurfacePage eyebrow="LIBRARY" title="Skills">
      <SkillsSection />
    </SurfacePage>
  )
}

export function PromptsSurface() {
  return (
    <SurfacePage eyebrow="LIBRARY" title="Prompts">
      <PromptsSection />
    </SurfacePage>
  )
}
