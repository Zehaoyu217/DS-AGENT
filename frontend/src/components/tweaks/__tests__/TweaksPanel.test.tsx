import { act, render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it } from 'vitest'
import { TweaksPanel } from '../TweaksPanel'
import { TweaksEffects } from '../TweaksEffects'
import { ThemeProvider } from '@/components/layout/ThemeProvider'
import { useUiStore } from '@/lib/ui-store'

beforeEach(() => {
  localStorage.clear()
  useUiStore.setState({
    accent: '#e0733a',
    dockPosition: 'right',
    msgStyle: 'flat',
    thinkMode: 'tab',
    uiFont: 'mono',
    railMode: 'icon',
    agentRunning: true,
    density: 'default',
    tweaksOpen: false,
  } as never)
  document.documentElement.removeAttribute('data-font')
  document.documentElement.removeAttribute('data-msg-style')
  document.documentElement.removeAttribute('data-think-mode')
  document.documentElement.style.removeProperty('--acc')
})

describe('<TweaksPanel>', () => {
  it('renders all 9 tweak rows when open', () => {
    render(
      <ThemeProvider>
        <TweaksPanel />
      </ThemeProvider>,
    )
    act(() => {
      useUiStore.getState().setTweaksOpen(true)
    })
    const text = document.body.textContent ?? ''
    for (const label of ['Theme', 'Accent', 'Density', 'Dock', 'Msg style', 'Think', 'Font', 'Rail', 'Agent']) {
      expect(text).toContain(label)
    }
  })

  it('clicking an accent swatch updates the store', () => {
    render(
      <ThemeProvider>
        <TweaksPanel />
      </ThemeProvider>,
    )
    act(() => {
      useUiStore.getState().setTweaksOpen(true)
    })
    const lime = screen.getByLabelText('lime')
    act(() => {
      lime.click()
    })
    expect(useUiStore.getState().accent).toBe('#a3e635')
  })

  it('clicking a Dock segment updates dockPosition', () => {
    render(
      <ThemeProvider>
        <TweaksPanel />
      </ThemeProvider>,
    )
    act(() => {
      useUiStore.getState().setTweaksOpen(true)
    })
    const bottomBtns = screen.getAllByRole('radio', { name: 'Bottom' })
    act(() => {
      bottomBtns[0].click()
    })
    expect(useUiStore.getState().dockPosition).toBe('bottom')
  })
})

describe('<TweaksEffects>', () => {
  it('writes accent + data-* attributes to <html>', () => {
    render(<TweaksEffects />)
    act(() => {
      useUiStore.getState().setAccent('#22d3ee')
      useUiStore.getState().setUiFont('sans')
      useUiStore.getState().setMsgStyle('bordered')
      useUiStore.getState().setThinkMode('inline')
    })
    expect(document.documentElement.style.getPropertyValue('--acc')).toBe('#22d3ee')
    expect(document.documentElement.dataset.font).toBe('sans')
    expect(document.documentElement.dataset.msgStyle).toBe('bordered')
    expect(document.documentElement.dataset.thinkMode).toBe('inline')
  })
})
