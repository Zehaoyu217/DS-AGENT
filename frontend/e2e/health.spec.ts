import { test, expect } from '@playwright/test'

test('health rail entry navigates to health section', async ({ page }) => {
  await page.goto('/')
  await page.getByRole('button', { name: 'Health' }).click()
  // Either the report renders or the empty-state message appears.
  await expect(
    page.locator('text=/No integrity report yet|Health —/i'),
  ).toBeVisible({ timeout: 5000 })
})
