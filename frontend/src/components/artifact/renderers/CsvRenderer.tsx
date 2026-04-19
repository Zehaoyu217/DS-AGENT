import { useEffect, useState } from 'react'
import { TableRenderer } from './TableRenderer'
import { TextRenderer } from './TextRenderer'

interface CsvRendererProps {
  content: string
}

export function CsvRenderer({ content }: CsvRendererProps) {
  const [tableJson, setTableJson] = useState<string | null>(null)
  const [failed, setFailed] = useState(false)

  useEffect(() => {
    let mounted = true
    import('papaparse')
      .then((mod) => {
        const parsed = mod.parse<string[]>(content.trim(), { skipEmptyLines: true })
        if (!mounted) return
        const rows = parsed.data as string[][]
        if (!rows.length) {
          setFailed(true)
          return
        }
        const [header, ...body] = rows
        setTableJson(JSON.stringify({ columns: header, rows: body }))
      })
      .catch(() => {
        if (mounted) setFailed(true)
      })
    return () => {
      mounted = false
    }
  }, [content])

  if (failed) return <TextRenderer content={content} />
  if (!tableJson) return <TextRenderer content="Parsing CSV…" />
  return <TableRenderer content={tableJson} />
}
