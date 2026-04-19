import { useEffect, useMemo, useState } from 'react'
import { ChevronRight, Clock, ExternalLink, FileText, Hash, Link2 } from 'lucide-react'
import {
  type WikiBacklink,
  type WikiPageResponse,
  extractToc,
  fetchWikiBacklinks,
  fetchWikiPage,
  formatRelative,
} from '@/lib/api-wiki'
import { MarkdownContent } from '@/components/chat/MarkdownContent'
import { cn } from '@/lib/utils'

interface WikiArticleProps {
  path: string | null
  onNavigate: (path: string) => void
}

export function WikiArticle({ path, onNavigate }: WikiArticleProps) {
  const [page, setPage] = useState<WikiPageResponse | null>(null)
  const [backlinks, setBacklinks] = useState<WikiBacklink[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!path) {
      setPage(null)
      setBacklinks([])
      return
    }
    let cancelled = false
    setLoading(true)
    setError(null)
    Promise.all([fetchWikiPage(path), fetchWikiBacklinks(path)])
      .then(([p, b]) => {
        if (cancelled) return
        setPage(p)
        setBacklinks(b.backlinks)
      })
      .catch((e: unknown) => {
        if (!cancelled) setError(e instanceof Error ? e.message : String(e))
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [path])

  const toc = useMemo(() => (page ? extractToc(page.content) : []), [page])
  const wordCount = useMemo(
    () => (page ? page.content.trim().split(/\s+/).filter(Boolean).length : 0),
    [page],
  )

  if (!path) return <EmptyState />
  if (error)
    return (
      <div className="flex h-full items-center justify-center px-6">
        <div className="rounded-md border border-err/40 bg-err/10 px-4 py-3 text-[13px] text-err">
          {error}
        </div>
      </div>
    )
  if (loading || !page) return <ArticleSkeleton />

  return (
    <div className="grid h-full grid-cols-[1fr_220px] overflow-hidden">
      <article className="overflow-auto">
        <ArticleHeader
          page={page}
          wordCount={wordCount}
          backlinkCount={backlinks.length}
        />
        <div className="px-8 pb-16 pt-2">
          <div className="max-w-[760px]">
            <MarkdownContent content={page.content} />
          </div>
          <BacklinksFooter backlinks={backlinks} onNavigate={onNavigate} />
          <OutboundFooter
            links={page.outbound_links}
            currentPath={page.path}
            onNavigate={onNavigate}
          />
        </div>
      </article>
      <TocRail toc={toc} />
    </div>
  )
}

function ArticleHeader({
  page,
  wordCount,
  backlinkCount,
}: {
  page: WikiPageResponse
  wordCount: number
  backlinkCount: number
}) {
  const segments = page.path.split('/')
  const filename = segments[segments.length - 1]
  const title = filename.replace(/\.md$/, '').replace(/[-_]/g, ' ')
  return (
    <header className="sticky top-0 z-10 border-b border-line bg-bg-0 px-8 py-4">
      <Breadcrumb segments={segments} />
      <h1 className="mt-1 text-[24px] font-semibold capitalize text-fg-0">
        {title}
      </h1>
      <dl
        className="mt-2 flex flex-wrap items-center gap-4 text-fg-3"
        style={{ fontSize: 11 }}
      >
        <Meta icon={<Clock size={11} aria-hidden />}>
          {formatRelative(page.modified)}
        </Meta>
        <Meta icon={<FileText size={11} aria-hidden />}>
          {wordCount.toLocaleString()} words
        </Meta>
        <Meta icon={<Link2 size={11} aria-hidden />}>
          {page.outbound_links.length} out
        </Meta>
        <Meta icon={<Link2 size={11} aria-hidden className="rotate-180" />}>
          {backlinkCount} in
        </Meta>
      </dl>
    </header>
  )
}

function Meta({ icon, children }: { icon: React.ReactNode; children: React.ReactNode }) {
  return (
    <span className="mono inline-flex items-center gap-1 uppercase tracking-[0.06em]">
      {icon}
      {children}
    </span>
  )
}

function Breadcrumb({ segments }: { segments: string[] }) {
  return (
    <nav
      aria-label="Breadcrumb"
      className="flex items-center gap-1 text-fg-3 mono uppercase tracking-[0.06em]"
      style={{ fontSize: 10 }}
    >
      <span>WIKI</span>
      {segments.slice(0, -1).map((s, i) => (
        <span key={i} className="flex items-center gap-1">
          <ChevronRight size={10} aria-hidden />
          <span>{s}</span>
        </span>
      ))}
    </nav>
  )
}

function TocRail({ toc }: { toc: { id: string; depth: number; text: string }[] }) {
  if (toc.length === 0) {
    return <aside className="border-l border-line bg-bg-1" aria-label="Table of contents" />
  }
  return (
    <aside
      className="overflow-auto border-l border-line bg-bg-1 px-3 py-4"
      aria-label="Table of contents"
    >
      <div
        className="mono uppercase tracking-[0.06em] text-fg-3 mb-2"
        style={{ fontSize: 10 }}
      >
        On this page
      </div>
      <ul className="flex flex-col gap-0.5">
        {toc.map((t, i) => (
          <li key={`${t.id}-${i}`}>
            <a
              href={`#${t.id}`}
              className={cn(
                'flex items-center gap-1 rounded-sm px-1.5 py-0.5 text-fg-2',
                'text-[12px] hover:bg-bg-2 hover:text-fg-0 focus-ring',
              )}
              style={{ paddingLeft: 6 + (t.depth - 2) * 10 }}
            >
              <Hash size={10} className="text-fg-3" aria-hidden />
              <span className="truncate">{t.text}</span>
            </a>
          </li>
        ))}
      </ul>
    </aside>
  )
}

function BacklinksFooter({
  backlinks,
  onNavigate,
}: {
  backlinks: WikiBacklink[]
  onNavigate: (path: string) => void
}) {
  if (backlinks.length === 0) return null
  return (
    <section className="mt-12 border-t border-line pt-4 max-w-[760px]">
      <div
        className="mono uppercase tracking-[0.06em] text-fg-3 mb-2"
        style={{ fontSize: 10 }}
      >
        Backlinks
      </div>
      <ul className="flex flex-col gap-1">
        {backlinks.map((b) => (
          <li key={b.path}>
            <button
              type="button"
              onClick={() => onNavigate(b.path)}
              className={cn(
                'flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-left',
                'text-[13px] text-fg-1 hover:bg-bg-1 hover:text-fg-0 focus-ring',
              )}
            >
              <Link2 size={12} className="text-fg-3" aria-hidden />
              <span className="truncate">{b.label}</span>
              <span
                className="mono text-fg-3"
                style={{ fontSize: 10 }}
              >
                {b.path}
              </span>
            </button>
          </li>
        ))}
      </ul>
    </section>
  )
}

function OutboundFooter({
  links,
  currentPath,
  onNavigate,
}: {
  links: string[]
  currentPath: string
  onNavigate: (path: string) => void
}) {
  if (links.length === 0) return null
  const base = currentPath.split('/').slice(0, -1).join('/')
  const resolveLink = (l: string): string => {
    if (l.startsWith('/')) return l.slice(1)
    if (!base) return l
    const parts = (base + '/' + l).split('/')
    const stack: string[] = []
    for (const p of parts) {
      if (p === '..') stack.pop()
      else if (p !== '.' && p !== '') stack.push(p)
    }
    return stack.join('/')
  }
  return (
    <section className="mt-8 border-t border-line pt-4 max-w-[760px]">
      <div
        className="mono uppercase tracking-[0.06em] text-fg-3 mb-2"
        style={{ fontSize: 10 }}
      >
        Outbound
      </div>
      <ul className="flex flex-col gap-1">
        {links.map((l) => (
          <li key={l}>
            <button
              type="button"
              onClick={() => onNavigate(resolveLink(l))}
              className={cn(
                'flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-left',
                'text-[13px] text-fg-1 hover:bg-bg-1 hover:text-fg-0 focus-ring',
              )}
            >
              <ExternalLink size={12} className="text-fg-3" aria-hidden />
              <span className="truncate">{l}</span>
            </button>
          </li>
        ))}
      </ul>
    </section>
  )
}

function EmptyState() {
  return (
    <div className="flex h-full flex-col items-center justify-center gap-2 px-6 text-center text-fg-3">
      <FileText size={28} aria-hidden />
      <p className="text-[13px]">Pick a page from the tree to start reading.</p>
    </div>
  )
}

function ArticleSkeleton() {
  return (
    <div className="px-8 py-6">
      <div className="h-3 w-32 animate-pulse rounded bg-bg-2" />
      <div className="mt-3 h-7 w-2/3 animate-pulse rounded bg-bg-2" />
      <div className="mt-2 h-3 w-48 animate-pulse rounded bg-bg-2" />
      <div className="mt-8 flex flex-col gap-2">
        {Array.from({ length: 8 }).map((_, i) => (
          <div
            key={i}
            className="h-3 animate-pulse rounded bg-bg-2"
            style={{ width: `${50 + ((i * 23) % 50)}%` }}
          />
        ))}
      </div>
    </div>
  )
}
