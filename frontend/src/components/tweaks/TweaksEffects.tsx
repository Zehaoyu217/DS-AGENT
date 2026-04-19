/**
 * TweaksEffects — invisible component that subscribes to the Tweaks-relevant
 * fields in `useUiStore` and applies their side effects to <html>:
 *   - accent       → inline CSS vars `--acc`, `--acc-dim`, `--acc-line`
 *   - uiFont       → `data-font` attribute (consumed by tokens.css)
 *   - msgStyle     → `data-msg-style` attribute (consumed by message renderer)
 *   - thinkMode    → `data-think-mode` attribute (consumed by thinking blocks)
 *
 * railMode and dockPosition are consumed directly by IconRail/AppShell and
 * don't need a global side effect.
 */
import { useEffect } from 'react'
import {
  useUiStore,
  selectAccent,
  selectUiFont,
  selectMsgStyle,
  selectThinkMode,
} from '@/lib/ui-store'

function withAlpha(hex: string, alphaHex: string): string {
  return `${hex}${alphaHex}`
}

export function TweaksEffects() {
  const accent = useUiStore(selectAccent)
  const uiFont = useUiStore(selectUiFont)
  const msgStyle = useUiStore(selectMsgStyle)
  const thinkMode = useUiStore(selectThinkMode)

  useEffect(() => {
    if (typeof document === 'undefined') return
    const root = document.documentElement
    root.style.setProperty('--acc', accent)
    root.style.setProperty('--acc-dim', withAlpha(accent, '1f'))
    root.style.setProperty('--acc-line', withAlpha(accent, '59'))
  }, [accent])

  useEffect(() => {
    if (typeof document === 'undefined') return
    document.documentElement.dataset.font = uiFont
  }, [uiFont])

  useEffect(() => {
    if (typeof document === 'undefined') return
    document.documentElement.dataset.msgStyle = msgStyle
  }, [msgStyle])

  useEffect(() => {
    if (typeof document === 'undefined') return
    document.documentElement.dataset.thinkMode = thinkMode
  }, [thinkMode])

  return null
}
