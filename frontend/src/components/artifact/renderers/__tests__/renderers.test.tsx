import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { TableRenderer } from '../TableRenderer'
import { HtmlRenderer } from '../HtmlRenderer'
import { TextRenderer } from '../TextRenderer'

describe('renderers', () => {
  it('TableRenderer renders headers and rows', () => {
    render(
      <TableRenderer
        content={JSON.stringify({ columns: ['a', 'b'], rows: [[1, 2], [3, 4]] })}
      />,
    )
    expect(screen.getByText('a')).toBeInTheDocument()
    expect(screen.getByText('4')).toBeInTheDocument()
  })

  it('HtmlRenderer uses srcdoc iframe', () => {
    const { container } = render(<HtmlRenderer content="<p>hi</p>" />)
    const iframe = container.querySelector('iframe')
    expect(iframe).not.toBeNull()
    expect(iframe?.getAttribute('srcdoc')).toContain('<p>hi</p>')
  })

  it('TextRenderer renders pre block', () => {
    render(<TextRenderer content="hello" />)
    expect(screen.getByText('hello')).toBeInTheDocument()
  })
})
