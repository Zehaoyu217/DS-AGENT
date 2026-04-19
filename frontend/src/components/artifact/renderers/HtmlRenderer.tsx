interface HtmlRendererProps {
  content: string
}

export function HtmlRenderer({ content }: HtmlRendererProps) {
  return (
    <iframe
      title="artifact-html"
      srcDoc={content}
      sandbox="allow-same-origin"
      className="h-full w-full border-0 bg-bg-0"
    />
  )
}
