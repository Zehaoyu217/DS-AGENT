import { useEffect, type JSX } from 'react'
import { CheckCircle2, Download, Upload } from 'lucide-react'
import { usePipelineStore } from '@/lib/pipeline-store'
import { PipelineAction } from './PipelineAction'

interface PipelineBarProps {
  onOpenIngest?: () => void
  onDigestComplete?: (entries: number) => void
  onMaintainComplete?: (lintErrors: number) => void
}

export function PipelineBar({
  onOpenIngest,
  onDigestComplete,
  onMaintainComplete,
}: PipelineBarProps): JSX.Element {
  const ingest = usePipelineStore((s) => s.ingest)
  const digest = usePipelineStore((s) => s.digest)
  const maintain = usePipelineStore((s) => s.maintain)
  const refreshStatus = usePipelineStore((s) => s.refreshStatus)
  const runDigest = usePipelineStore((s) => s.runDigest)
  const runMaintain = usePipelineStore((s) => s.runMaintain)

  useEffect(() => {
    void refreshStatus()
  }, [refreshStatus])

  const handleDigest = async (): Promise<void> => {
    const result = await runDigest()
    if (result && result.entries > 0) onDigestComplete?.(result.entries)
  }

  const handleMaintain = async (): Promise<void> => {
    const result = await runMaintain()
    if (result) onMaintainComplete?.(result.lint_errors)
  }

  return (
    <nav
      aria-label="Pipeline"
      className="flex h-14 shrink-0 items-stretch border-t border-line bg-bg-0"
    >
      <PipelineAction
        phase="ingest"
        label="Ingest"
        icon={<Upload size={16} aria-hidden />}
        state={ingest}
        onClick={() => onOpenIngest?.()}
      />
      <PipelineAction
        phase="digest"
        label="Digest"
        icon={<Download size={16} aria-hidden />}
        state={digest}
        onClick={handleDigest}
      />
      <PipelineAction
        phase="maintain"
        label="Maintain"
        icon={<CheckCircle2 size={16} aria-hidden />}
        state={maintain}
        onClick={handleMaintain}
      />
    </nav>
  )
}
