import { test, expect, type Page } from '@playwright/test';

// Skip the one-time cookie notice so it never covers a control under test.
test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => {
    try { localStorage.setItem('aml_cookie_consent', 'acknowledged'); } catch { /* ignore */ }
  });
});

const openSettings = async (page: Page) => {
  await page.getByRole('button', { name: 'Settings' }).click();
  await expect(page.getByRole('dialog', { name: 'Workspace settings' })).toBeVisible();
};

test.describe('Landing page', () => {
  test('shows the offer, honest metric caption and working navigation', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/Intelligent-AML/);
    await expect(page.getByRole('heading', { level: 1 })).toContainText('Eliminate 84% of False Positives');
    await expect(page.getByText(/synthetic Bangladesh banking data/i)).toBeVisible();
    for (const id of ['how', 'tiering', 'security', 'pricing']) {
      await expect(page.locator(`#${id}`)).toBeAttached();
    }
    await expect(page.getByText(/OWASP ASVS Level 2/i)).toBeVisible();
    await expect(page.getByText(/Air-Gap Verified|0 EXTERNAL EGRESS/i)).toHaveCount(0);
  });

  test('request demo form validates, submits and confirms', async ({ page }) => {
    await page.goto('/');
    await page.getByRole('button', { name: /Request demo/i }).first().click();
    const dialog = page.getByRole('dialog');
    await expect(dialog).toBeVisible();
    await page.fill('input[placeholder*="Kazi"]', 'Amina Rahman');
    await page.fill('input[placeholder*="officer@bank"]', 'amina@ebl.com.bd');
    await page.fill('input[placeholder*="Eastern Bank"]', 'Eastern Bank PLC');
    await dialog.getByRole('button', { name: /Submit/i }).click();
    await expect(page.getByText(/Architecture Brief Generated/i)).toBeVisible();
  });

  test('launch app opens the workspace and language toggle works', async ({ page }) => {
    await page.goto('/');
    await page.getByRole('button', { name: 'Switch language' }).click();
    await expect(page.getByRole('button', { name: 'Switch language' })).toHaveText('English');
    await page.getByRole('link', { name: /Launch app/i }).first().click();
    await expect(page).toHaveURL(/\/app$/);
  });

  test('privacy and terms dialogs open and close with Escape', async ({ page }) => {
    await page.goto('/');
    await page.getByRole('button', { name: 'Privacy' }).click();
    await expect(page.getByRole('dialog')).toBeVisible();
    await page.keyboard.press('Escape');
    await expect(page.getByRole('dialog')).toHaveCount(0);
    await page.getByRole('button', { name: 'Terms' }).click();
    await expect(page.getByRole('dialog')).toBeVisible();
  });
});

test.describe('Shell and settings', () => {
  test('theme, currency and language settings take effect', async ({ page }) => {
    await page.goto('/triage');
    await openSettings(page);

    await page.getByRole('group', { name: 'Theme' }).getByRole('button', { name: 'Light' }).click();
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'light');
    await page.getByRole('group', { name: 'Theme' }).getByRole('button', { name: 'Dark' }).click();
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');

    const firstAmount = page.locator('[role=row]').nth(1);
    await page.getByRole('group', { name: 'Currency' }).getByRole('button', { name: '$ USD' }).click();
    await expect(firstAmount).toContainText('$');

    await page.getByRole('group', { name: 'Language' }).getByRole('button', { name: 'বাংলা' }).click();
    await expect(page.getByText(/নির্বাহী নজরদারি/).first()).toBeVisible();
    await page.getByRole('group', { name: 'Language' }).getByRole('button', { name: 'English' }).click();
    await expect(page.getByText(/Executive Surveillance/).first()).toBeVisible();
  });

  test('settings choices survive a reload', async ({ page }) => {
    await page.goto('/triage');
    await openSettings(page);
    await page.getByRole('group', { name: 'Row density' }).getByRole('button', { name: 'Roomy' }).click();
    await page.reload();
    await openSettings(page);
    await expect(page.getByRole('group', { name: 'Row density' }).getByRole('button', { name: 'Roomy' })).toHaveAttribute('aria-pressed', 'true');
  });

  test('command palette opens with the keyboard and navigates', async ({ page }) => {
    await page.goto('/app');
    await page.keyboard.press('Control+k');
    const box = page.getByPlaceholder(/Search alerts/);
    await expect(box).toBeVisible();
    await box.fill('graph');
    await page.keyboard.press('Enter');
    await expect(page).toHaveURL(/graph/);
  });

  test('number keys jump between modules', async ({ page }) => {
    await page.goto('/app');
    await page.locator('body').click({ position: { x: 5, y: 300 } });
    await page.keyboard.press('2');
    await expect(page).toHaveURL(/triage/);
    await page.keyboard.press('6');
    await expect(page).toHaveURL(/graph/);
  });

  test('feed can be paused and resumed from the header', async ({ page }) => {
    await page.goto('/app');
    await page.getByRole('button', { name: 'Pause simulated feed' }).click();
    await expect(page.getByRole('button', { name: 'Resume simulated feed' })).toBeVisible();
    await page.getByRole('button', { name: 'Resume simulated feed' }).click();
    await expect(page.getByRole('button', { name: 'Pause simulated feed' })).toBeVisible();
  });

  test('personal data stays masked until revealed', async ({ page }) => {
    await page.goto('/triage');
    await expect(page.getByText(/BD22-\*\*\*\*/).first()).toBeVisible();
    await openSettings(page);
    await page.getByRole('button', { name: /Reveal personal data/i }).click();
  });
});

test.describe('Modules', () => {
  test('1 dashboard: KPIs link to the filtered queues', async ({ page }) => {
    await page.goto('/app');
    await expect(page.getByText(/Evaluation workspace/)).toBeVisible();
    await expect(page.getByText(/Air-Gap Ready/i)).toHaveCount(0);
    await page.getByRole('link', { name: /View Tier 1 Queue/i }).click();
    await expect(page).toHaveURL(/triage/);
  });

  test('2 triage: filter, search, inspect and export', async ({ page }) => {
    await page.goto('/triage');
    await expect(page.getByRole('table', { name: /Alert triage queue/i })).toBeVisible();
    await page.getByRole('button', { name: /Tier 2 Review/ }).click();
    await expect(page.getByText('Tier 2 · Review').first()).toBeVisible();
    await expect(page.getByText('Tier 1 · Hold')).toHaveCount(0);
    await page.getByRole('button', { name: /All Alerts/ }).click();
    await page.getByPlaceholder(/Search by ID/).fill('Meghna');
    await expect(page.getByText('Meghna Industrial & Agro Processing Ltd').first()).toBeVisible();
    await page.getByRole('button', { name: /Inspect Raw SWIFT/ }).first().click();
    await expect(page.getByRole('dialog', { name: 'Raw wire inspector' })).toBeVisible();
    await page.keyboard.press('Escape');
    await expect(page.getByRole('dialog', { name: 'Raw wire inspector' })).toHaveCount(0);
    const [csv] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'CSV' }).click()]);
    expect(csv.suggestedFilename()).toMatch(/\.csv$/);
    const [json] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'JSON' }).click()]);
    expect(json.suggestedFilename()).toMatch(/\.json$/);
  });

  test('3 screening: run a name check and filter the hits', async ({ page }) => {
    await page.goto('/screening');
    await page.getByPlaceholder(/Gulf Star Commodities/).fill('Gulf Star Trading');
    await page.getByRole('button', { name: /^Screen$/ }).click();
    await page.getByRole('button', { name: /True Hits/ }).click();
    await expect(page.getByRole('button', { name: /Confirm True Hit/ }).first()).toBeVisible();
  });

  test('4 customers: search and risk filter', async ({ page }) => {
    await page.goto('/customers');
    await page.getByPlaceholder('Search entities...').fill('Meghna');
    await expect(page.getByText(/Meghna/).first()).toBeVisible();
    await page.getByRole('button', { name: /High \(EDD\)/ }).click();
    await expect(page.getByRole('button', { name: /Execute EDD Sign-Off/ })).toBeVisible();
  });

  test('5 cases: switch view and export', async ({ page }) => {
    await page.goto('/cases');
    await page.getByRole('button', { name: 'Table' }).click();
    await page.getByRole('button', { name: 'Grid' }).click();
    const [dl] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Export JSON' }).click()]);
    expect(dl.suggestedFilename()).toMatch(/\.json$/);
  });

  test('6 graph: renders and responds to hop and cap controls', async ({ page }) => {
    await page.goto('/graph');
    await expect(page.getByRole('heading', { level: 1 })).toContainText('Forensic Cash Flow Studio');
    await page.getByRole('button', { name: '3-Hop' }).click();
    await page.getByRole('button', { name: '250' }).click();
    await page.getByRole('button', { name: 'Fit' }).click();
    await expect(page.getByText(/Loading Forensic/)).toHaveCount(0);
    await expect(page.locator('canvas, svg').first()).toBeVisible();
  });

  test('7 TBML: document packet and benchmark tabs', async ({ page }) => {
    await page.goto('/tbml');
    await expect(page.getByText(/ASYCUDA/).first()).toBeVisible();
    await page.getByRole('button', { name: /AIS Vessel Route Tracking/ }).click();
    await page.getByRole('button', { name: /ASYCUDA World Price Benchmark/ }).click();
  });

  test('8 SAR: tabs, checker sign-off and goAML export', async ({ page }) => {
    await page.goto('/sar');
    await expect(page.getByText(/Tipping-Off/i).first()).toBeVisible();
    await page.getByRole('button', { name: /CTR\) Aggregator|Cash Transaction Reports/ }).click();
    await page.getByRole('button', { name: /Suspicious Transaction Report/ }).click();
    await page.getByRole('button', { name: /Authorize as CCO/ }).click();
    const [xml] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: /Export Official BFIU goAML XML/ }).click()]);
    expect(xml.suggestedFilename()).toMatch(/\.xml$/);
  });

  test('9 RFI: issue a notice', async ({ page }) => {
    await page.goto('/rfi');
    const texts = page.locator('main input[type=text], main input:not([type])');
    await texts.nth(0).fill('Meghna Industrial & Agro Processing Ltd');
    await texts.nth(1).fill('Please provide the commercial invoice and bill of lading.');
    await page.locator('main textarea').first().fill('Documents required within 5 working days.');
    await page.getByRole('button', { name: /Issue Customer RFI Notice/ }).click();
    await expect(page.getByRole('button', { name: /Send Reminder/ }).first()).toBeVisible();
  });

  test('10 rules: tabs and promotion needs four-eyes', async ({ page }) => {
    await page.goto('/rules');
    await page.getByRole('button', { name: /Internal Sensitivity Calibration/ }).click();
    await page.getByRole('button', { name: /Time-Bound Whitelisting/ }).click();
    await page.getByRole('button', { name: /Champion vs Challenger/ }).click();
    await page.getByRole('button', { name: /Promote to Production/ }).click();
    await expect(page.getByRole('dialog', { name: 'Four-eyes approval' })).toBeVisible();
  });

  test('11 governance: ledger verification and compliance pack', async ({ page }) => {
    await page.goto('/governance');
    await page.getByRole('button', { name: /Tamper-Evident Ledger/ }).click();
    await page.getByRole('button', { name: /Verify Cryptographic Chain/ }).click();
    await expect(page.getByText(/Chain 100% Valid/)).toBeVisible();
    await page.getByRole('button', { name: /Model Operations/ }).click();
    const [pack] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: /Download Governance Compliance Pack/ }).click()]);
    expect(pack.suggestedFilename()).toMatch(/\.json$/);
  });
});

test.describe('Every route', () => {
  for (const route of ['/', '/app', '/triage', '/screening', '/customers', '/cases', '/graph', '/tbml', '/sar', '/rfi', '/rules', '/governance']) {
    test(`${route} renders without a stuck loader or page error`, async ({ page }) => {
      const errors: string[] = [];
      page.on('pageerror', (e) => errors.push(String(e)));
      await page.goto(route);
      await page.waitForTimeout(1500);
      await expect(page.locator('body')).not.toContainText(/Loading .*\.\.\./);
      await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
      expect(errors).toEqual([]);
    });
  }
});
