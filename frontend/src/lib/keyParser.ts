/**
 * Keyboard shortcut parser.
 * Supports modifier strings like "mod+shift+k" where `mod` maps to Cmd on Mac
 * and Ctrl on Win/Linux. Ported from reference/web/lib/keyParser.ts.
 */

// Detected once at module load; safe for SSR because Vite runs in the browser.
export const isMac =
  typeof navigator !== 'undefined' &&
  /Mac|iPhone|iPad|iPod/i.test(navigator.platform || navigator.userAgent || '')

export interface ParsedKey {
  mod: boolean
  ctrl: boolean
  shift: boolean
  alt: boolean
  key: string
}

/**
 * Parse a shortcut string like "mod+shift+k" into a structured object.
 * Supports modifiers: mod, ctrl, shift, alt.
 * `mod` = Cmd on Mac, Ctrl on Win/Linux.
 */
export function parseKey(keyString: string): ParsedKey {
  const parts = keyString.toLowerCase().split('+')
  const key = parts[parts.length - 1]
  return {
    mod: parts.includes('mod'),
    ctrl: parts.includes('ctrl'),
    shift: parts.includes('shift'),
    alt: parts.includes('alt'),
    key,
  }
}

/**
 * Test whether a KeyboardEvent matches a parsed key definition.
 */
export function matchesEvent(parsed: ParsedKey, e: KeyboardEvent): boolean {
  // On Mac, `mod` maps to metaKey; on Win/Linux it maps to ctrlKey.
  const expectedMeta = isMac ? parsed.mod : false
  const expectedCtrl = isMac ? parsed.ctrl : parsed.mod || parsed.ctrl

  if (e.metaKey !== expectedMeta) return false
  if (e.ctrlKey !== expectedCtrl) return false
  if (e.altKey !== parsed.alt) return false

  // For alphanumeric keys, require shift to match. For symbol characters
  // (?, /, comma, etc.) shift is implicit in the key value itself, so skip
  // the shift check.
  const keyIsAlphanumeric = /^[a-z0-9]$/.test(parsed.key)
  if (keyIsAlphanumeric && e.shiftKey !== parsed.shift) return false

  return e.key.toLowerCase() === parsed.key
}

/**
 * Format a key combo string for display, returning an array of display
 * segments, e.g. ["⌘", "K"] on Mac or ["Ctrl", "K"] elsewhere.
 */
export function formatKeyCombo(keyString: string): string[] {
  const parts = keyString.split('+')
  return parts.map((part) => {
    switch (part.toLowerCase()) {
      case 'mod':
        return isMac ? '⌘' : 'Ctrl'
      case 'shift':
        return isMac ? '⇧' : 'Shift'
      case 'alt':
        return isMac ? '⌥' : 'Alt'
      case 'ctrl':
        return isMac ? '⌃' : 'Ctrl'
      case 'enter':
        return '↵'
      case 'escape':
        return 'Esc'
      case 'backspace':
        return '⌫'
      case 'tab':
        return 'Tab'
      case 'arrowup':
        return '↑'
      case 'arrowdown':
        return '↓'
      case 'arrowleft':
        return '←'
      case 'arrowright':
        return '→'
      default:
        return part.toUpperCase()
    }
  })
}
