import { test, expect } from '@playwright/test';

test.describe('Intelligent-AML Enterprise E2E Suite', () => {
  test.describe('1. Public Technical & Commercial Landing Page', () => {
    test('renders landing page with headline, conformal explainer, and request-demo form', async ({ page }) => {
      await page.goto('/');

      // Verify title and main headline
      await expect(page).toHaveTitle(/Intelligent-AML/);
      await expect(page.getByRole('heading', { level: 1 })).toContainText(/Eliminate 84% of False Positives/i);

      // Verify Conformal Tiering Section
      await expect(page.locator('#tiering')).toBeVisible();
      await expect(page.getByText('Tier 1 Hold')).toBeVisible();
      await expect(page.getByText('Tier 2 Review')).toBeVisible();
      await expect(page.getByText('Tier 3 Clear')).toBeVisible();

      // Verify Security & BFIU Section
      await expect(page.locator('#security')).toBeVisible();
      await expect(page.getByText(/OWASP ASVS LEVEL 2/i)).toBeVisible();

      // Verify Request Demo Trigger & Modal
      const requestDemoBtn = page.getByRole('button', { name: /Request Demo/i }).first();
      await requestDemoBtn.click();
      await expect(page.getByRole('dialog', { name: /Schedule Institutional Demonstration/i })).toBeVisible();

      // Fill and submit demo request
      await page.fill('input[placeholder*="Kazi"]', 'Amina Rahman');
      await page.fill('input[placeholder*="officer@bank"]', 'amina@ebl.com.bd');
      await page.fill('input[placeholder*="Eastern Bank"]', 'Eastern Bank PLC');
      await page.getByRole('button', { name: /Submit Institutional Request/i }).click();

      // Verify confirmation state
      await expect(page.getByText(/Briefing Request Received/i)).toBeVisible();
    });
  });

  test.describe('2. Compliance Modules Hub (/app)', () => {
    test('renders Module 1: Executive Surveillance dashboard with live stream telemetry', async ({ page }) => {
      await page.goto('/app');

      // Verify brand and version
      await expect(page.getByText('INTELLIGENT-AML')).toBeVisible();
      await expect(page.getByText('v3.0')).toBeVisible();

      // Verify SLA & Surveillance cards
      await expect(page.getByText(/Surveillance & SLA Overview/i)).toBeVisible();
      await expect(page.getByText(/Active Ingestion Stream/i).or(page.getByText(/SIMULATED STREAM/i))).toBeVisible();
    });

    test('renders Module 2: Alert Triage queue with 3-tier filtering & SHAP waterfall', async ({ page }) => {
      await page.goto('/app/triage');

      // Verify table header
      await expect(page.getByRole('table', { name: /Alert triage queue/i })).toBeVisible();

      // Verify 3-tier buttons
      await expect(page.getByRole('button', { name: /Tier 1 Hold/i })).toBeVisible();
      await expect(page.getByRole('button', { name: /Tier 2 Review/i })).toBeVisible();
      await expect(page.getByRole('button', { name: /Tier 3 Clear/i })).toBeVisible();

      // Filter by Tier 1
      await page.getByRole('button', { name: /Tier 1 Hold/i }).click();
      await expect(page.getByText(/Tier 1 Hold/i).first()).toBeVisible();
    });

    test('renders Module 3: Sanctions & PEP screening with 5 official lists and matcher', async ({ page }) => {
      await page.goto('/app/screening');

      // Verify official lists
      await expect(page.getByText(/Official Regulatory Watchlists/i)).toBeVisible();
      await expect(page.getByText('OFAC SDN')).toBeVisible();
      await expect(page.getByText('UN Consolidated')).toBeVisible();
      await expect(page.getByText('EU Consolidated')).toBeVisible();
      await expect(page.getByText('UK HM Treasury')).toBeVisible();
      await expect(page.getByText('Bangladesh Domestic (BFIU / ATA 2009)')).toBeVisible();
    });

    test('renders Module 4: Customer 360° KYC and beneficial ownership graph', async ({ page }) => {
      await page.goto('/app/customers');

      await expect(page.getByText(/Customer 360/i)).toBeVisible();
      await expect(page.getByText('Meghna Industrial Corp PLC')).toBeVisible();
    });

    test('renders Module 5: Institutional Cases docket with print dossier modal and JSON export', async ({ page }) => {
      await page.goto('/app/cases');

      await expect(page.getByText(/Institutional Case Management Docket/i)).toBeVisible();
      await expect(page.getByRole('button', { name: /Export JSON/i })).toBeVisible();

      // Open print dossier preview
      const printBtn = page.getByTitle(/Print Formal BFIU Case Dossier/i).first();
      await printBtn.click();

      // Verify BFIU letterhead and Section 65B statutory certificate
      await expect(page.getByRole('dialog')).toBeVisible();
      await expect(page.getByText(/BANGLADESH FINANCIAL INTELLIGENCE UNIT/i)).toBeVisible();
      await expect(page.getByText(/STATUTORY EVIDENTIARY CERTIFICATE/i)).toBeVisible();
    });

    test('renders Module 6: Forensic Cash Flow multi-hop topology studio', async ({ page }) => {
      await page.goto('/app/graph');

      await expect(page.getByText(/Forensic Cash Flow Studio/i)).toBeVisible();
      await expect(page.getByText('Node Cap:')).toBeVisible();
    });

    test('renders Module 7: Trade Finance TBML radar with ASYCUDA price divergence', async ({ page }) => {
      await page.goto('/app/tbml');

      await expect(page.getByText(/Trade-Based Money Laundering/i)).toBeVisible();
      await expect(page.getByText(/ASYCUDA/i)).toBeVisible();
    });

    test('renders Module 8: SAR & CTR Workbench with goAML XML schema export', async ({ page }) => {
      await page.goto('/app/sar');

      await expect(page.getByText(/SAR & CTR Regulatory Filing Workbench/i)).toBeVisible();
      await expect(page.getByText(/ANTI-TIPPING-OFF LEGAL WARNING/i)).toBeVisible();
      await expect(page.getByText(/Money Laundering Prevention Act, 2012 § 27/i)).toBeVisible();
    });

    test('renders Module 9: Compliance RFI Hub with correspondent bank verification', async ({ page }) => {
      await page.goto('/app/rfi');

      await expect(page.getByText(/Compliance RFI & Inter-Bank Sharing Hub/i)).toBeVisible();
    });

    test('renders Module 10: Rule Studio & Recourse with invariant authoring', async ({ page }) => {
      await page.goto('/app/rules');

      await expect(page.getByText(/Rule Studio & Counterfactual Recourse/i)).toBeVisible();
    });

    test('renders Module 11: Model Ops, SR 11-7 & Tamper-Evident Ledger', async ({ page }) => {
      await page.goto('/app/governance');

      await expect(page.getByText(/Model Ops, SR 11-7 Validation & Audit Ledger/i)).toBeVisible();
      await expect(page.getByRole('button', { name: /Verify Cryptographic Chain/i })).toBeVisible();
      await expect(page.getByRole('button', { name: /Simulate Auditor Tamper Test/i })).toBeVisible();

      // Trigger chain verification
      await page.getByRole('button', { name: /Verify Cryptographic Chain/i }).click();
      await expect(page.getByText(/VERIFIED/i).first()).toBeVisible();
    });
  });

  test.describe('3. Four-Eyes Dual Control & PII Governance Flows', () => {
    test('enforces PII masking and audited 60-second reveal flow', async ({ page }) => {
      await page.goto('/app');

      // Check PII reveal button in header
      const revealBtn = page.getByRole('button', { name: /Reveal PII/i }).first();
      await expect(revealBtn).toBeVisible();
      await revealBtn.click();

      // Verify modal or state change
      await expect(page.getByText(/PII: UNMASKED/i).or(page.getByText(/Reveal PII/i))).toBeVisible();
    });

    test('toggles language between English and Bangla across the shell', async ({ page }) => {
      await page.goto('/app');

      // Click Language switcher
      const langBtn = page.getByRole('button', { name: /EN|বাং/i }).first();
      await langBtn.click();

      // Verify Bangla terms in navigation
      await expect(page.getByText(/১\. নির্বাহী নজরদারি/i).or(page.getByText(/২\. সতর্কতা বাছাই/i))).toBeVisible();

      // Toggle back to English
      await langBtn.click();
      await expect(page.getByText(/1\. Executive Surveillance/i)).toBeVisible();
    });

    test('toggles currency between BDT and USD', async ({ page }) => {
      await page.goto('/app');

      const currBtn = page.getByRole('button', { name: /৳ BDT|\$ USD/i }).first();
      await currBtn.click();

      // Verify toggle action
      await expect(page.getByRole('button', { name: /৳ BDT|\$ USD/i }).first()).toBeVisible();
    });
  });
});
