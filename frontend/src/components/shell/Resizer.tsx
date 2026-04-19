/**
 * Resizer — a 4px-thick drag handle used between shell panes.
 *
 * Behavior:
 *  - Pointer drag: on pointerdown, captures pointer and registers move/up
 *    handlers on `window`. Move fires onChange with clamped new value.
 *  - Keyboard: Arrow keys ±10; Shift+Arrow ±50; Home/End snap to bounds.
 *  - `invert` reverses the drag delta direction (for a left-edge handle such
 *    as the Dock's, where dragging left should *increase* the dock width).
 *  - ARIA: `role="separator"` with `aria-orientation`, `aria-valuenow`,
 *    `aria-valuemin`, `aria-valuemax`, and `aria-label`.
 */

import { useCallback, useRef, type KeyboardEvent, type PointerEvent } from "react";

export type ResizerAxis = "x" | "y";

export interface ResizerProps {
  axis: ResizerAxis;
  min: number;
  max: number;
  value: number;
  onChange: (next: number) => void;
  ariaLabel: string;
  /** For left-edge handles where dragging towards the parent edge should grow. */
  invert?: boolean;
  className?: string;
}

const clamp = (n: number, min: number, max: number): number =>
  Math.min(max, Math.max(min, n));

export function Resizer({
  axis,
  min,
  max,
  value,
  onChange,
  ariaLabel,
  invert = false,
  className,
}: ResizerProps) {
  const startRef = useRef<{ coord: number; value: number } | null>(null);

  const handlePointerDown = useCallback(
    (event: PointerEvent<HTMLDivElement>): void => {
      event.preventDefault();
      const coord = axis === "x" ? event.clientX : event.clientY;
      startRef.current = { coord, value };
      const target = event.currentTarget;
      target.setPointerCapture(event.pointerId);

      const direction = invert ? -1 : 1;
      const onMove = (e: globalThis.PointerEvent): void => {
        if (!startRef.current) return;
        const current = axis === "x" ? e.clientX : e.clientY;
        const delta = (current - startRef.current.coord) * direction;
        onChange(clamp(Math.round(startRef.current.value + delta), min, max));
      };
      const onUp = (e: globalThis.PointerEvent): void => {
        startRef.current = null;
        try {
          target.releasePointerCapture(e.pointerId);
        } catch {
          /* pointer already released */
        }
        window.removeEventListener("pointermove", onMove);
        window.removeEventListener("pointerup", onUp);
        window.removeEventListener("pointercancel", onUp);
      };

      window.addEventListener("pointermove", onMove);
      window.addEventListener("pointerup", onUp);
      window.addEventListener("pointercancel", onUp);
    },
    [axis, invert, max, min, onChange, value],
  );

  const handleKeyDown = useCallback(
    (event: KeyboardEvent<HTMLDivElement>): void => {
      const step = event.shiftKey ? 50 : 10;
      const direction = invert ? -1 : 1;
      const primaryDec = axis === "x" ? "ArrowLeft" : "ArrowUp";
      const primaryInc = axis === "x" ? "ArrowRight" : "ArrowDown";

      if (event.key === primaryDec) {
        event.preventDefault();
        onChange(clamp(value - step * direction, min, max));
      } else if (event.key === primaryInc) {
        event.preventDefault();
        onChange(clamp(value + step * direction, min, max));
      } else if (event.key === "Home") {
        event.preventDefault();
        onChange(min);
      } else if (event.key === "End") {
        event.preventDefault();
        onChange(max);
      }
    },
    [axis, invert, max, min, onChange, value],
  );

  const baseClass =
    axis === "x"
      ? "w-1 cursor-col-resize hover:bg-acc-line active:bg-acc"
      : "h-1 cursor-row-resize hover:bg-acc-line active:bg-acc";

  return (
    <div
      role="separator"
      tabIndex={0}
      aria-orientation={axis === "x" ? "vertical" : "horizontal"}
      aria-valuenow={value}
      aria-valuemin={min}
      aria-valuemax={max}
      aria-label={ariaLabel}
      onPointerDown={handlePointerDown}
      onKeyDown={handleKeyDown}
      className={[
        baseClass,
        "bg-transparent transition-colors focus-ring",
        "touch-none select-none",
        className ?? "",
      ]
        .filter(Boolean)
        .join(" ")}
    />
  );
}
