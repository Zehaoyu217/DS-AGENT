import { useMemo } from 'react'

interface TableRendererProps {
  content: string
}

interface TableData {
  columns: string[]
  rows: Array<Array<string | number | null>>
}

function parse(content: string): TableData {
  try {
    const data = JSON.parse(content) as TableData
    return {
      columns: Array.isArray(data.columns) ? data.columns : [],
      rows: Array.isArray(data.rows) ? data.rows : [],
    }
  } catch {
    return { columns: [], rows: [] }
  }
}

export function TableRenderer({ content }: TableRendererProps) {
  const { columns, rows } = useMemo(() => parse(content), [content])
  return (
    <div className="flex-1 overflow-auto">
      <table className="min-w-full border-collapse">
        <thead className="sticky top-0 bg-bg-1">
          <tr>
            {columns.map((c) => (
              <th
                key={c}
                className="mono border-b border-line-2 px-3 py-1.5 text-left text-[10.5px] uppercase text-fg-2"
              >
                {c}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={i} className="border-b border-line-2">
              {r.map((cell, j) => (
                <td key={j} className="mono px-3 py-1 text-[12px] text-fg-0">
                  {cell === null ? '—' : String(cell)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
