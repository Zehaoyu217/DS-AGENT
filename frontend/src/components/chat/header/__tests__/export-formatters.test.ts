import { describe, it, expect } from 'vitest'
import { toMarkdown, toJson, toHtml } from '../export-formatters'
import type { Conversation } from '@/lib/store'

const conv: Conversation = {
  id: 'c1',
  title: 'Q3 churn',
  createdAt: 0,
  updatedAt: 0,
  messages: [
    { id: 'm1', role: 'user', content: 'hello', status: 'complete', timestamp: 0 },
    { id: 'm2', role: 'assistant', content: 'hi', status: 'complete', timestamp: 0 },
  ],
}

describe('export-formatters', () => {
  it('markdown renders title + role sections', () => {
    const out = toMarkdown(conv)
    expect(out).toContain('# Q3 churn')
    expect(out).toContain('**user**')
    expect(out).toContain('hello')
    expect(out).toContain('**assistant**')
  })

  it('json round-trips', () => {
    const out = toJson(conv)
    const parsed = JSON.parse(out)
    expect(parsed.title).toBe('Q3 churn')
    expect(parsed.messages).toHaveLength(2)
  })

  it('html escapes dangerous chars', () => {
    const hostile: Conversation = {
      ...conv,
      messages: [{ ...conv.messages[0], content: '<script>x</script>' }],
    }
    const out = toHtml(hostile)
    expect(out).not.toContain('<script>x')
    expect(out).toContain('&lt;script&gt;')
  })
})
