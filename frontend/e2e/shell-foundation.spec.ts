/**
 * E2E — Shell Foundation (Phase 8.3)
 *
 * Validates the four-pane AppShell structure and the new keyboard shortcuts
 * introduced with the DS-Agent handoff. Runs UI-only (no backend asserts) and
 * uses the `loadApp` pattern from smoke.spec.ts — backend request failures are
 * swallowed so the suite is green without the Python API running.
 *
 * Visual-regression baselines (4 breakpoints × 2 themes × sections) are
 * deferred until we stand up a baseline-image review flow in CI; this spec
 * focuses on structural and keyboard-driven behavior that is deterministic.
 */

import { test, expect, type Page } from '@playwright/test'

async function loadApp(page: Page): Promise<void> {
  page.on('requestfailed', () => {
    /* swallow backend failures */
  })
  await page.goto('/', { waitUntil: 'domcontentloaded', timeout: 15_000 })
}

async function resetTheme(page: Page): Promise<void> {
  await page.evaluate(() => {
    localStorage.removeItem('ds:theme')
    localStorage.removeItem('theme')
  })
}

test.describe('Shell Foundation', () => {
  test('renders the four-pane shell with IconRail + main region', async ({
    page,
  }) => {
    await resetTheme(page)
    await loadApp(page)

    const shell = page.locator('[data-app-shell]')
    await expect(shell).toBeVisible({ timeout: 10_000 })

    const nav = page.locator('nav[aria-label="Main navigation"]')
    await expect(nav).toBeVisible()

    const main = page.locator('main[aria-label="Main content"]')
    await expect(main).toBeVisible()
  })

  test('IconRail surfaces 9 sections + theme toggle + settings', async ({
    page,
  }) => {
    await loadApp(page)

    const nav = page.locator('nav[aria-label="Main navigation"]')
    const labels = [
      'Chat',
      'Agents',
      'Skills',
      'Prompts',
      'Context',
      'Health',
      'Graph',
      'Digest',
      'Ingest',
      'Settings',
    ]
    for (const label of labels) {
      await expect(
        nav.locator(`button[aria-label="${label}"]`),
      ).toBeVisible({ timeout: 5_000 })
    }
  })

  test('theme toggle flips data-theme attribute + persists ds:theme', async ({
    page,
  }) => {
    await resetTheme(page)
    await loadApp(page)

    const html = page.locator('html')
    // Default is light — absence of data-theme or explicit "light"
    const initial = (await html.getAttribute('data-theme')) ?? 'light'
    expect(initial).toBe('light')

    const toggle = page.locator(
      'nav[aria-label="Main navigation"] button[aria-label*="mode"]',
    )
    await toggle.click()

    await expect(html).toHaveAttribute('data-theme', 'dark', { timeout: 3_000 })
    const stored = await page.evaluate(() => localStorage.getItem('ds:theme'))
    expect(stored).toBe('dark')
  })

  test('mod+shift+7 jumps to the Graph section (OPEN_SECTION_*)', async ({
    page,
  }) => {
    await loadApp(page)

    const nav = page.locator('nav[aria-label="Main navigation"]')
    await expect(
      nav.locator('button[aria-label="Chat"]'),
    ).toHaveAttribute('aria-current', 'page')

    const mod = process.platform === 'darwin' ? 'Meta' : 'Control'
    await page.keyboard.press(`${mod}+Shift+Digit7`)

    await expect(
      nav.locator('button[aria-label="Graph"]'),
    ).toHaveAttribute('aria-current', 'page', { timeout: 3_000 })
  })

  test('mod+j toggles the dock visibility on the chat section', async ({
    page,
  }) => {
    await loadApp(page)

    // Ensure chat section is active so the dock is eligible to mount
    await page
      .locator('nav[aria-label="Main navigation"] button[aria-label="Chat"]')
      .click()

    const mod = process.platform === 'darwin' ? 'Meta' : 'Control'

    // Read dockOpen from the ui-store directly since the persist layer wires it
    const initialDockOpen = await page.evaluate(() => {
      const raw = localStorage.getItem('ds:ui')
      if (!raw) return true // default
      try {
        const state = JSON.parse(raw)?.state
        return state?.dockOpen ?? true
      } catch {
        return true
      }
    })

    await page.keyboard.press(`${mod}+KeyJ`)

    await expect
      .poll(
        async () =>
          page.evaluate(() => {
            const raw = localStorage.getItem('ds:ui')
            if (!raw) return null
            try {
              return JSON.parse(raw)?.state?.dockOpen ?? null
            } catch {
              return null
            }
          }),
        { timeout: 3_000 },
      )
      .toBe(!initialDockOpen)
  })
})
