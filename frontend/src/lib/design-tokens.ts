/**
 * Design token constants for third-party visualization libraries (Vega, Mermaid, etc.)
 * that can't consume Tailwind classes or CSS custom properties directly.
 *
 * Values must stay in sync with globals.css / tailwind.config.ts.
 */
export const TOKENS = {
  bgPrimary: '#09090b',
  bgSecondary: '#18181b',
  bgElevated: '#27272a',
  textPrimary: '#fafafa',
  textSecondary: '#a1a1aa',
  textMuted: '#52525b',
  accent: '#e0733a',
  success: '#22c55e',
  warning: '#f59e0b',
  error: '#ef4444',
  info: '#3b82f6',
  border: '#27272a',
  borderHover: '#3f3f46',
} as const

/** Ordered color palette for chart series — accent-led, no violet. */
export const CHART_COLOR_SCALE = [
  '#e0733a', // accent orange
  '#3b82f6', // info blue
  '#22c55e', // success green
  '#f59e0b', // warning amber
  '#ef4444', // error red
  '#0ea5e9', // sky
  '#ec4899', // pink
  '#14b8a6', // teal
  '#f97316', // orange
  '#6366f1', // indigo
] as const
