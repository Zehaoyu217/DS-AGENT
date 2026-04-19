import { useEffect, useMemo, useState } from 'react'
import { ChevronDown, ChevronRight, FileText, Folder, FolderOpen, Pin } from 'lucide-react'
import {
  type WikiNode,
  type WikiTreeResponse,
  fetchWikiTree,
  filterTree,
  formatRelative,
} from '@/lib/api-wiki'
import { SearchBar } from '@/components/surface/SearchBar'
import { useSurfacesStore } from '@/lib/surfaces-store'
import { cn } from '@/lib/utils'

interface WikiTreeProps {
  selectedPath: string | null
  onSelect: (path: string) => void
}

export function WikiTree({ selectedPath, onSelect }: WikiTreeProps) {
  const [tree, setTree] = useState<WikiTreeResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const search = useSurfacesStore((s) => s.knowledgeSearch)
  const setSearch = useSurfacesStore((s) => s.setKnowledgeSearch)

  useEffect(() => {
    let cancelled = false
    fetchWikiTree()
      .then((r) => {
        if (!cancelled) setTree(r)
      })
      .catch((e: unknown) => {
        if (!cancelled) setError(e instanceof Error ? e.message : String(e))
      })
    return () => {
      cancelled = true
    }
  }, [])

  const filtered = useMemo(() => {
    if (!tree) return []
    return filterTree(tree.nodes, search)
  }, [tree, search])

  const pinned = useMemo(
    () => (tree?.nodes ?? []).filter((n) => n.kind === 'file' && n.pinned),
    [tree],
  )

  return (
    <div className="flex h-full flex-col bg-bg-1">
      <div className="border-b border-line p-2">
        <SearchBar
          value={search}
          onChange={setSearch}
          placeholder="Filter pages…"
          ariaLabel="Filter wiki pages"
          hotkey="/"
        />
      </div>
      {error && (
        <div className="px-3 py-2 text-[12px] text-err">{error}</div>
      )}
      <div className="flex-1 overflow-auto px-1 py-2">
        {pinned.length > 0 && (
          <div className="mb-2">
            <SectionLabel>Pinned</SectionLabel>
            <ul className="flex flex-col">
              {pinned.map((n) => (
                <FileRow
                  key={n.path}
                  node={n}
                  depth={0}
                  selected={selectedPath === n.path}
                  onSelect={onSelect}
                  pinnedHint
                />
              ))}
            </ul>
          </div>
        )}
        <SectionLabel>{search ? 'Matches' : 'Tree'}</SectionLabel>
        {!tree ? (
          <Skeleton />
        ) : filtered.length === 0 ? (
          <div className="px-3 py-2 text-[12px] text-fg-3">no matches</div>
        ) : (
          <ul className="flex flex-col">
            {filtered.map((n) => (
              <TreeItem
                key={n.path}
                node={n}
                depth={0}
                selectedPath={selectedPath}
                onSelect={onSelect}
                forceOpen={Boolean(search)}
              />
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

function SectionLabel({ children }: { children: React.ReactNode }) {
  return (
    <div
      className="mono uppercase tracking-[0.06em] text-fg-3 px-2 pb-1"
      style={{ fontSize: 10 }}
    >
      {children}
    </div>
  )
}

function Skeleton() {
  return (
    <ul className="flex flex-col gap-1 px-2">
      {Array.from({ length: 6 }).map((_, i) => (
        <li
          key={i}
          className="h-5 animate-pulse rounded bg-bg-2"
          style={{ opacity: 0.6 - i * 0.07 }}
        />
      ))}
    </ul>
  )
}

interface TreeItemProps {
  node: WikiNode
  depth: number
  selectedPath: string | null
  onSelect: (path: string) => void
  forceOpen?: boolean
}

function TreeItem({ node, depth, selectedPath, onSelect, forceOpen }: TreeItemProps) {
  const [open, setOpen] = useState(depth === 0 || Boolean(forceOpen))

  useEffect(() => {
    if (forceOpen) setOpen(true)
  }, [forceOpen])

  if (node.kind === 'file') {
    return (
      <FileRow
        node={node}
        depth={depth}
        selected={selectedPath === node.path}
        onSelect={onSelect}
      />
    )
  }
  const Caret = open ? ChevronDown : ChevronRight
  const FolderIcon = open ? FolderOpen : Folder
  return (
    <li>
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className={cn(
          'flex w-full items-center gap-1 rounded-sm py-0.5 pr-2 text-left',
          'text-[12.5px] text-fg-1 hover:bg-bg-2 hover:text-fg-0 focus-ring',
        )}
        style={{ paddingLeft: 6 + depth * 12 }}
      >
        <Caret size={12} className="text-fg-3" aria-hidden />
        <FolderIcon size={13} className="text-fg-2" aria-hidden />
        <span className="flex-1 truncate">{node.name}</span>
        <span
          className="mono text-fg-3"
          style={{ fontSize: 10 }}
          aria-label={`${node.children.length} entries`}
        >
          {node.children.length}
        </span>
      </button>
      {open && (
        <ul className="flex flex-col">
          {node.children.map((c) => (
            <TreeItem
              key={c.path}
              node={c}
              depth={depth + 1}
              selectedPath={selectedPath}
              onSelect={onSelect}
              forceOpen={forceOpen}
            />
          ))}
        </ul>
      )}
    </li>
  )
}

interface FileRowProps {
  node: WikiNode
  depth: number
  selected: boolean
  onSelect: (path: string) => void
  pinnedHint?: boolean
}

function FileRow({ node, depth, selected, onSelect, pinnedHint }: FileRowProps) {
  return (
    <li>
      <button
        type="button"
        onClick={() => onSelect(node.path)}
        aria-current={selected ? 'page' : undefined}
        className={cn(
          'group flex w-full items-center gap-1 rounded-sm py-0.5 pr-2 text-left',
          'text-[12.5px] focus-ring transition-colors',
          selected
            ? 'bg-acc-dim text-acc'
            : 'text-fg-1 hover:bg-bg-2 hover:text-fg-0',
        )}
        style={{ paddingLeft: 6 + depth * 12 + 14 }}
        title={`${node.path} · ${formatRelative(node.modified)}`}
      >
        <FileText size={12} className={cn(selected ? 'text-acc' : 'text-fg-3')} aria-hidden />
        <span className="flex-1 truncate">{node.name}</span>
        {pinnedHint && (
          <Pin size={10} className="text-fg-3" aria-hidden />
        )}
      </button>
    </li>
  )
}
