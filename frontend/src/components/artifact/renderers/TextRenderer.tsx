import { useState } from 'react'
import { cn } from '@/lib/utils'

interface TextRendererProps {
  content: string
}

export function TextRenderer({ content }: TextRendererProps) {
  const [wrap, setWrap] = useState(true)
  return (
    <div className="flex h-full flex-col">
      <div className="flex justify-end border-b border-line-2 px-3 py-1">
        <button
          type="button"
          onClick={() => setWrap((v) => !v)}
          className="mono text-[10.5px] text-fg-2 hover:text-fg-0 focus-ring rounded"
        >
          {wrap ? 'no wrap' : 'wrap'}
        </button>
      </div>
      <pre
        className={cn(
          'mono flex-1 overflow-auto p-3 text-[12px] text-fg-0',
          wrap ? 'whitespace-pre-wrap break-words' : 'whitespace-pre',
        )}
      >
        {content}
      </pre>
    </div>
  )
}
