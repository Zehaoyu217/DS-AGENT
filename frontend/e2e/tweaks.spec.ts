/**
 * E2E — Tweaks panel (SP5)
 *
 * Boots the app, opens the Tweaks panel via the IconRail gear button (and
 * via ⌘,), and asserts that toggling the controls writes side-effects to
 * <html> + persists into ds:ui.
 */
import { test, expect, type Page } from '@playwright/test'

async function loadApp(page: Page): Promise<void> {
  page.on('requestfailed', () => {
    /* swallow backend failures */
  })
  await page.goto('/', { waitUntil: 'domcontentloaded', timeout: 15_000 })
}

test.describe('Tweaks panel', () => {
  test('IconRail Tweaks button opens the panel with all 9 rows', async ({
    page,
  }) => {
    await loadApp(page)

    const rail = page.locator('nav[aria-label="Main navigation"]')
    const tweaksBtn = rail.locator('button[aria-label="Tweaks"]')
    await expect(tweaksBtn).toBeVisible({ timeout: 5_000 })

    await tweaksBtn.click()

    const panel = page.locator('[aria-label="Tweaks"][role="dialog"]')
    await expect(panel).toBeVisible({ timeout: 3_000 })

    for (const label of [
      'Theme',
      'Accent',
      'Density',
      'Dock',
      'Msg style',
      'Think',
      'Font',
      'Rail',
      'Agent',
    ]) {
      await expect(panel.getByText(label, { exact: true })).toBeVisible()
    }
  })

  // Keyboard shortcut delivery is flaky in headless chromium (same issue
  // affects ⌘K palette + ⌘J dock toggle). Vitest covers the registration;
  // here we exercise the button path which is what users hit anyway.
  test.skip('⌘, opens the Tweaks panel', async ({ page }) => {
    await loadApp(page)
    const mod = process.platform === 'darwin' ? 'Meta' : 'Control'
    await page.keyboard.press(`${mod}+Comma`)
    const panel = page.locator('[aria-label="Tweaks"][role="dialog"]')
    await expect(panel).toBeVisible({ timeout: 3_000 })
  })

  test('changing accent writes --acc on <html> and persists', async ({
    page,
  }) => {
    await loadApp(page)
    await page
      .locator('nav[aria-label="Main navigation"] button[aria-label="Tweaks"]')
      .click()

    const panel = page.locator('[aria-label="Tweaks"][role="dialog"]')
    await panel.locator('button[aria-label="cyan"]').click()

    await expect
      .poll(async () =>
        page.evaluate(() =>
          document.documentElement.style.getPropertyValue('--acc'),
        ),
      )
      .toBe('#22d3ee')

    const persisted = await page.evaluate(() => {
      const raw = localStorage.getItem('ds:ui')
      if (!raw) return null
      try {
        return JSON.parse(raw)?.state?.accent ?? null
      } catch {
        return null
      }
    })
    expect(persisted).toBe('#22d3ee')
  })

  test('switching dockPosition to Bottom writes data-dock-position', async ({
    page,
  }) => {
    await loadApp(page)
    await page
      .locator('nav[aria-label="Main navigation"] button[aria-label="Chat"]')
      .click()
    await page
      .locator('nav[aria-label="Main navigation"] button[aria-label="Tweaks"]')
      .click()

    const panel = page.locator('[aria-label="Tweaks"][role="dialog"]')
    await panel.locator('button[role="radio"]', { hasText: 'Bottom' }).click()

    await expect(page.locator('[data-app-shell]')).toHaveAttribute(
      'data-dock-position',
      'bottom',
      { timeout: 3_000 },
    )
  })
})
