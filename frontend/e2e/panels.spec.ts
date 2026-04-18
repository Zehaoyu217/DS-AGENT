/**
 * E2E Panel Tests — right-rail drawers shipped during the post-v2
 * coherence sweep (DIGEST, HEALTH, SKILLS, GRAPH, INGEST).
 *
 * Scope: UI scaffolding only. Backend may be unavailable — network
 * failures to :8000 are swallowed. See `smoke.spec.ts` for the
 * helper precedent.
 */

import { test, expect, type Page } from '@playwright/test'

async function loadApp(page: Page) {
  page.on('requestfailed', () => {/* intentionally swallowed */})
  await page.goto('/', { waitUntil: 'domcontentloaded', timeout: 15_000 })
}

// Panels declared in the order they appear as topbar slots.
const PANELS: ReadonlyArray<{
  label: string
  panelSelector: string
  ariaLabel: string
}> = [
  {
    label: 'DIGEST',
    panelSelector: '.digest-panel',
    ariaLabel: 'Toggle second-brain digest panel',
  },
  {
    label: 'HEALTH',
    panelSelector: '.health-panel',
    ariaLabel: 'Toggle second-brain health panel',
  },
  {
    label: 'SKILLS',
    panelSelector: '.skills-panel',
    ariaLabel: 'Toggle skills usage panel',
  },
  {
    label: 'GRAPH',
    panelSelector: '.graph-panel',
    ariaLabel: 'Toggle knowledge graph panel',
  },
  {
    label: 'INGEST',
    panelSelector: '.ingest-panel',
    ariaLabel: 'Toggle ingest drop-zone panel',
  },
]

// ────────────────────────────────────────────────────────────────────
// Test 1: all five topbar buttons render with the expected labels
// ────────────────────────────────────────────────────────────────────

test('topbar stack renders all panel buttons', async ({ page }) => {
  await loadApp(page)

  const buttons = page.locator('.topbar-btn')
  await expect(buttons.first()).toBeVisible({ timeout: 10_000 })
  const count = await buttons.count()
  expect(count).toBeGreaterThanOrEqual(PANELS.length)

  const texts = await buttons.allTextContents()
  for (const p of PANELS) {
    const found = texts.some((t) => t.includes(p.label))
    expect(found, `expected topbar button for ${p.label}`).toBe(true)
  }

  await page.screenshot({ path: 'e2e-panels-topbar.png' })
})

// ────────────────────────────────────────────────────────────────────
// Test 2: every panel opens on click and closes via its × button
// ────────────────────────────────────────────────────────────────────

test('each topbar button opens and closes its drawer', async ({ page }) => {
  await loadApp(page)

  for (const panel of PANELS) {
    const btn = page.locator(`button[aria-label="${panel.ariaLabel}"]`)
    await expect(btn).toBeVisible({ timeout: 10_000 })

    // Open
    await btn.click()
    const drawer = page.locator(panel.panelSelector)
    await expect(drawer).toBeVisible({ timeout: 5_000 })

    // Close — the close button is scoped to the drawer
    const closeBtn = drawer.locator('button[aria-label="close"]')
    await expect(closeBtn).toBeVisible()
    await closeBtn.click()
    await expect(drawer).toBeHidden({ timeout: 5_000 })
  }

  await page.screenshot({ path: 'e2e-panels-open-close.png' })
})

// ────────────────────────────────────────────────────────────────────
// Test 3: GRAPH panel shows an empty-state string when the backend
//          has no graph data (the common case without a live store)
// ────────────────────────────────────────────────────────────────────

test('graph panel renders empty-state when no data', async ({ page }) => {
  await loadApp(page)

  await page
    .locator('button[aria-label="Toggle knowledge graph panel"]')
    .click()

  const panel = page.locator('.graph-panel')
  await expect(panel).toBeVisible({ timeout: 5_000 })

  // The empty-state block is rendered when `nodes.length === 0`. We
  // accept either the default copy or the backend-supplied `note`
  // (e.g. "no graph data").
  const empty = panel.locator('.graph-panel__empty')
  await expect(empty.first()).toBeVisible({ timeout: 5_000 })
  const text = (await empty.first().textContent()) ?? ''
  expect(text.toLowerCase()).toMatch(/no graph data|disabled|error|knowledge/i)

  await page.screenshot({ path: 'e2e-panels-graph-empty.png' })
})

// ────────────────────────────────────────────────────────────────────
// Test 4: INGEST panel renders the dropzone + focusable input
// ────────────────────────────────────────────────────────────────────

test('ingest panel renders dropzone and focusable input', async ({ page }) => {
  await loadApp(page)

  await page
    .locator('button[aria-label="Toggle ingest drop-zone panel"]')
    .click()

  const panel = page.locator('.ingest-panel')
  await expect(panel).toBeVisible({ timeout: 5_000 })

  const dropzone = panel.locator('[data-testid="ingest-dropzone"]')
  await expect(dropzone).toBeVisible()
  const dropzoneText = (await dropzone.textContent()) ?? ''
  expect(dropzoneText.toUpperCase()).toContain('DROP')

  const input = panel.locator('[data-testid="ingest-input"]')
  await expect(input).toBeVisible()
  await input.click()
  await expect(input).toBeFocused()
  await input.fill('/tmp/test.md')
  const val = await input.inputValue()
  expect(val).toBe('/tmp/test.md')

  await page.screenshot({ path: 'e2e-panels-ingest.png' })
})

// ────────────────────────────────────────────────────────────────────
// Test 5: HEALTH panel renders its header + DIGEST BUILD subsection
// ────────────────────────────────────────────────────────────────────

test('health panel renders header and digest-build subsection', async ({
  page,
}) => {
  await loadApp(page)

  await page
    .locator('button[aria-label="Toggle second-brain health panel"]')
    .click()

  const panel = page.locator('.health-panel')
  await expect(panel).toBeVisible({ timeout: 5_000 })

  // Primary header
  await expect(panel.locator('.health-panel__title')).toHaveText('HEALTH')

  // Digest-build subsection renders even when the backend has no data —
  // the HealthPanel always mounts the "Digest Build · today" title with
  // either the metrics block or an inline empty-state underneath.
  const digestTitle = panel.locator('[data-testid="health-digest-build-title"]')
  await expect(digestTitle).toBeVisible({ timeout: 5_000 })

  await page.screenshot({ path: 'e2e-panels-health.png' })
})
