import { useState, useMemo } from 'react'
import { ArrowUp, ArrowDown, ChevronsUpDown } from 'lucide-react'

interface TableData {
  columns: string[]
  rows: (string | number | boolean | null)[][]
  total_rows?: number
}

interface DataTableProps {
  content: string  // JSON string of TableData
}

export function DataTable({ content }: DataTableProps) {
  const [sortCol, setSortCol] = useState<number | null>(null)
  const [sortDir, setSortDir] = useState<'asc' | 'desc'>('asc')
  const [filter, setFilter] = useState('')

  let columns: string[] = []
  let rows: (string | number | boolean | null)[][] = []
  let totalRows = 0

  try {
    const parsed = JSON.parse(content) as TableData
    columns = parsed.columns ?? []
    rows = parsed.rows ?? []
    totalRows = parsed.total_rows ?? rows.length
  } catch {
    return (
      <p className="text-xs font-mono text-red-400 p-2">Failed to parse table data.</p>
    )
  }

  const handleSort = (colIdx: number) => {
    if (sortCol === colIdx) {
      setSortDir((d) => (d === 'asc' ? 'desc' : 'asc'))
    } else {
      setSortCol(colIdx)
      setSortDir('asc')
    }
  }

  // eslint-disable-next-line react-hooks/rules-of-hooks
  const displayRows = useMemo(() => {
    let result = rows

    if (filter.trim()) {
      const q = filter.toLowerCase()
      result = result.filter((row) =>
        row.some((cell) => String(cell ?? '').toLowerCase().includes(q)),
      )
    }

    if (sortCol !== null) {
      result = [...result].sort((a, b) => {
        const av = a[sortCol]
        const bv = b[sortCol]
        const isNum =
          av !== null && bv !== null && !isNaN(Number(av)) && !isNaN(Number(bv))
        const cmp = isNum
          ? Number(av) - Number(bv)
          : String(av ?? '').localeCompare(String(bv ?? ''))
        return sortDir === 'asc' ? cmp : -cmp
      })
    }

    return result
  }, [rows, filter, sortCol, sortDir])

  const isTruncated = totalRows > rows.length
  const isFiltered = filter.trim().length > 0

  return (
    <div className="flex flex-col gap-1.5">
      {rows.length > 5 && (
        <div className="relative">
          <input
            type="text"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            placeholder="Filter rows…"
            className="w-full pl-3 pr-2 py-1 text-[11px] font-mono bg-surface-900 border border-surface-700 rounded text-surface-300 placeholder:text-surface-600 focus:outline-none focus:border-brand-500 transition-colors"
          />
        </div>
      )}

      <div className="overflow-x-auto rounded border border-surface-700">
        <table className="w-full border-collapse">
          <thead>
            <tr className="border-b border-surface-700">
              {columns.map((col, i) => (
                <th
                  key={i}
                  onClick={() => handleSort(i)}
                  className="px-3 py-1.5 text-left text-[10px] font-mono font-bold uppercase tracking-widest text-surface-500 bg-surface-900 whitespace-nowrap cursor-pointer select-none hover:text-surface-300 transition-colors"
                >
                  <span className="flex items-center gap-1">
                    {col}
                    {sortCol === i ? (
                      sortDir === 'asc' ? (
                        <ArrowUp className="w-2.5 h-2.5 text-brand-400" />
                      ) : (
                        <ArrowDown className="w-2.5 h-2.5 text-brand-400" />
                      )
                    ) : (
                      <ChevronsUpDown className="w-2.5 h-2.5 opacity-20" />
                    )}
                  </span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {displayRows.map((row, i) => (
              <tr
                key={i}
                className="border-b border-surface-800 last:border-b-0 hover:bg-surface-800/50 transition-colors duration-75"
              >
                {row.map((cell, j) => (
                  <td
                    key={j}
                    className="px-3 py-1.5 text-[11px] font-mono tabular-nums text-surface-300 whitespace-nowrap"
                  >
                    {cell === null ? (
                      <span className="text-surface-600 italic">null</span>
                    ) : (
                      String(cell)
                    )}
                  </td>
                ))}
              </tr>
            ))}
            {displayRows.length === 0 && (
              <tr>
                <td
                  colSpan={columns.length}
                  className="px-3 py-4 text-center text-[11px] font-mono text-surface-600"
                >
                  {isFiltered ? 'No rows match filter' : 'No data'}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="flex items-center gap-2 text-[10px] font-mono text-surface-600">
        {isFiltered ? (
          <span>{displayRows.length} of {rows.length} rows match</span>
        ) : (
          <span>{displayRows.length} rows</span>
        )}
        {isTruncated && !isFiltered && (
          <span className="text-amber-500/60">· {totalRows} total — showing first {rows.length}</span>
        )}
        {sortCol !== null && (
          <>
            <span>·</span>
            <button
              onClick={() => { setSortCol(null); setSortDir('asc') }}
              className="text-surface-600 hover:text-surface-400 transition-colors"
            >
              clear sort
            </button>
          </>
        )}
      </div>
    </div>
  )
}
