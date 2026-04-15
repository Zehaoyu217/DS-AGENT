import { useCallback, useRef, useState } from 'react'

type Direction = 'horizontal' | 'vertical'

/**
 * Provides drag-to-resize for a panel measured in pixels.
 *
 * @param defaultSize  Initial size in px
 * @param min          Minimum size in px
 * @param max          Maximum size in px
 * @param direction    'horizontal' (left/right drag) or 'vertical' (up/down drag)
 * @param reverse      When true, delta is subtracted instead of added (for panels
 *                     anchored to the right or bottom edge)
 */
export function useResizablePanel(
  defaultSize: number,
  min: number,
  max: number,
  direction: Direction = 'horizontal',
  reverse = false,
) {
  const [size, setSize] = useState(defaultSize)
  const startPos = useRef(0)
  const startSize = useRef(defaultSize)

  const onMouseDown = useCallback(
    (e: React.MouseEvent) => {
      e.preventDefault()
      startPos.current = direction === 'horizontal' ? e.clientX : e.clientY
      startSize.current = size

      const onMouseMove = (ev: MouseEvent) => {
        const raw = direction === 'horizontal' ? ev.clientX : ev.clientY
        const delta = raw - startPos.current
        const next = startSize.current + (reverse ? -delta : delta)
        setSize(Math.max(min, Math.min(max, next)))
      }

      const onMouseUp = () => {
        document.removeEventListener('mousemove', onMouseMove)
        document.removeEventListener('mouseup', onMouseUp)
        document.body.style.cursor = ''
        document.body.style.userSelect = ''
      }

      document.body.style.cursor = direction === 'horizontal' ? 'col-resize' : 'row-resize'
      document.body.style.userSelect = 'none'
      document.addEventListener('mousemove', onMouseMove)
      document.addEventListener('mouseup', onMouseUp)
    },
    [size, min, max, direction, reverse],
  )

  return { size, onMouseDown }
}
