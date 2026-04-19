import type { Conversation, Message } from '@/lib/store'
import { extractTextContent } from '@/lib/utils'

function escapeHtml(input: string): string {
  return input
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

function messageText(msg: Message): string {
  return extractTextContent(msg.content)
}

export function toMarkdown(conv: Conversation): string {
  const lines: string[] = [`# ${conv.title}`, '']
  for (const msg of conv.messages) {
    lines.push(`**${msg.role}**`, '')
    lines.push(messageText(msg), '')
  }
  return lines.join('\n')
}

export function toJson(conv: Conversation): string {
  const payload = {
    id: conv.id,
    title: conv.title,
    createdAt: conv.createdAt,
    updatedAt: conv.updatedAt,
    model: conv.model,
    messages: conv.messages.map((m) => ({
      id: m.id,
      role: m.role,
      content: messageText(m),
      timestamp: m.timestamp,
    })),
  }
  return JSON.stringify(payload, null, 2)
}

export function toHtml(conv: Conversation): string {
  const body = conv.messages
    .map(
      (m) =>
        `<section><h2>${escapeHtml(m.role)}</h2><pre>${escapeHtml(messageText(m))}</pre></section>`,
    )
    .join('\n')
  return `<!doctype html>
<html><head><meta charset="utf-8"><title>${escapeHtml(conv.title)}</title></head>
<body><h1>${escapeHtml(conv.title)}</h1>${body}</body></html>`
}
