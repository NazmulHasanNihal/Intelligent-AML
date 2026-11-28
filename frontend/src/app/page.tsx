"use client";

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  ArrowRight,
  CheckCircle2,
  FileCheck2,
  Layers,
  Lock,
  Menu,
  Moon,
  Scale,
  Shield,
  Sun,
  Users,
  X,
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { useTheme } from '@/lib/theme';
import { ConformalLivePreviewWidget } from '@/components/landing/ConformalLivePreviewWidget';
import { ProductVisualPreview } from '@/components/landing/ProductVisualPreview';
import { InstitutionalInquiryModal } from '@/components/landing/InstitutionalInquiryModal';

type InquiryType = 'EVALUATION' | 'BANK_POC' | 'SOVEREIGN';

const NAV = [
  { href: '#how', label: 'How it works' },
  { href: '#tiering', label: 'Tiering' },
  { href: '#security', label: 'Security' },
  { href: '#pricing', label: 'Pricing' },
];

const METRICS = [
  { label: 'Macro F1', value: '94.5%', note: 'vs. GBDT/TGN baselines' },
  { label: 'Noise reduction', value: '84.2%', note: '7-day replay' },
  { label: 'Scoring latency', value: '< 200 µs', note: 'scorer only, p50' },
  { label: 'Conformal coverage', value: '99.04%', note: 'bounded FNR <= 0.01' },
];

const STEPS = [
  { icon: Layers, title: 'Ingest wires', body: 'Read SWIFT MT700, ISO 20022 pacs.008, and cash flows with 12 graph invariants.' },
  { icon: Scale, title: 'Calibrate sets', body: 'Conformal prediction outputs calibrated Tier 1, Tier 2, or Tier 3 certainty bounds.' },
  { icon: Shield, title: 'Enforce 4-eyes', body: 'Hold certain hits for dual sign-off while clearing low-risk traffic at low latency.' },
  { icon: FileCheck2, title: 'Dispatch goAML', body: 'Export BFIU goAML XML packets sealed to a WebCrypto SHA-256 WORM ledger.' },
];

const SECURITY = [
  { icon: Lock, tone: 'bg-accent-subtle text-accent-text', tKey: 'security_point1' as const, body: 'SHA-256 hash chain over canonical records; admissibility-ready under Bangladesh Evidence Act §§ 65A–65B & 73A.' },
  { icon: Users, tone: 'bg-tier-3-bg text-tier-3-text', tKey: 'security_point2' as const, body: 'Maker and checker roles enforced at API boundaries, preventing self-ratification.' },
  { icon: Shield, tone: 'bg-tier-2-bg text-tier-2-text', tKey: 'security_point3' as const, body: 'Personal data is masked by default. Audited unmasking requires a justification and expires in 60s.' },
  { icon: FileCheck2, tone: 'bg-accent-subtle text-accent-2', tKey: 'security_point4' as const, body: 'UNODC goAML v4.2 STR/CTR export guarded by MLPA 2012 § 6 anti-tipping-off scans.' },
];

const PLANS: {
  key: string;
  tKey: 'plan_starter' | 'plan_bank' | 'plan_fiu';
  price: string;
  unit: string;
  features: string[];
  cta: string;
  featured?: boolean;
  href?: string;
  inquiry?: InquiryType;
}[] = [
  {
    key: 'eval',
    tKey: 'plan_starter',
    price: '$0',
    unit: 'sandbox evaluation',
    features: ['Synthetic Bangladesh dataset', 'All 11 compliance modules', 'Deterministic replay'],
    cta: 'Open the sandbox',
    href: '/app',
  },
  {
    key: 'bank',
    tKey: 'plan_bank',
    price: 'Custom',
    unit: 'annual SLA',
    features: ['On-prem Kubernetes / Helm', 'Core banking & SWIFT webhooks', 'SHA-256 WORM ledger', 'Dedicated onboarding'],
    cta: 'Request a bank PoC',
    featured: true,
    inquiry: 'BANK_POC',
  },
  {
    key: 'fiu',
    tKey: 'plan_fiu',
    price: 'Sovereign',
    unit: 'regulator mandate',
    features: ['Multi-institution graph', 'goAML central gateway', 'HSM-backed signing'],
    cta: 'Schedule a briefing',
    inquiry: 'SOVEREIGN',
  },
];

export default function EnterpriseLandingPage() {
  const { language, toggleLanguage, t } = useBankingStore();
  const { theme, setTheme } = useTheme();
  const dark = theme !== 'light';

  const [inquiryModalOpen, setInquiryModalOpen] = useState(false);
  const [inquiryType, setInquiryType] = useState<InquiryType>('BANK_POC');
  const [isPrivacyModalOpen, setIsPrivacyModalOpen] = useState(false);
  const [isTermsModalOpen, setIsTermsModalOpen] = useState(false);
  const [isMobileNavOpen, setIsMobileNavOpen] = useState(false);
  const [isCookieDismissed, setIsCookieDismissed] = useState(true);

  useEffect(() => {
    try {
      if (!localStorage.getItem('aml_cookie_consent')) setIsCookieDismissed(false);
    } catch {
      /* storage unavailable */
    }
  }, []);

  const handleAcknowledgeCookie = () => {
    try {
      localStorage.setItem('aml_cookie_consent', 'acknowledged');
    } catch {
      /* ignore */
    }
    document.cookie = 'aml_consent=1; path=/; max-age=31536000; SameSite=Strict; Secure';
    setIsCookieDismissed(true);
  };

  const handleOpenInquiry = (type: InquiryType) => {
    setInquiryType(type);
    setInquiryModalOpen(true);
    setIsMobileNavOpen(false);
  };

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setIsMobileNavOpen(false);
        setInquiryModalOpen(false);
        setIsPrivacyModalOpen(false);
        setIsTermsModalOpen(false);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  const btnPrimary =
    'inline-flex items-center justify-center gap-2 rounded-lg bg-accent px-5 py-2.5 text-sm font-semibold text-accent-fg transition-colors hover:bg-accent-hover cursor-pointer';
  const btnGhost =
    'inline-flex items-center justify-center gap-2 rounded-lg border border-line px-5 py-2.5 text-sm font-semibold text-fg transition-colors hover:bg-surface-hover cursor-pointer';

  return (
    <div className="flex min-h-screen flex-col bg-canvas font-sans text-fg selection:bg-accent/25">
      {/* Header */}
      <header className="sticky top-0 z-40 h-16 w-full border-b border-line bg-panel/90 backdrop-blur-md">
        <div className="mx-auto flex h-full max-w-6xl items-center justify-between gap-4 px-4 sm:px-6">
          <Link href="/" className="flex shrink-0 items-center gap-2.5" aria-label="Intelligent-AML home">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg border border-accent/30 bg-accent-subtle">
              <span className="h-2.5 w-2.5 rounded-full bg-accent" />
            </span>
            <span className="text-base font-semibold text-fg">Intelligent-AML</span>
            <span className="hidden rounded border border-line bg-surface px-1.5 py-0.5 text-xs font-mono text-muted sm:inline">
              Platform v3.0
            </span>
          </Link>

          <nav className="hidden items-center gap-7 text-sm text-fg-secondary md:flex" aria-label="Primary">
            {NAV.map((n) => (
              <a key={n.href} href={n.href} className="whitespace-nowrap transition-colors hover:text-fg">
                {n.label}
              </a>
            ))}
            <Link href="/governance" className="whitespace-nowrap transition-colors hover:text-fg">
              Model card
            </Link>
          </nav>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => setTheme(dark ? 'light' : 'dark')}
              className="rounded-lg p-2 text-muted transition-colors hover:bg-surface-hover hover:text-fg cursor-pointer"
              aria-label={dark ? 'Switch to light theme' : 'Switch to dark theme'}
              title={dark ? 'Light theme' : 'Dark theme'}
            >
              {dark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
            </button>
            <button
              type="button"
              onClick={toggleLanguage}
              className="rounded-lg px-2.5 py-1.5 text-sm text-fg-secondary transition-colors hover:bg-surface-hover hover:text-fg cursor-pointer"
              aria-label="Switch language"
            >
              {language === 'en' ? 'বাংলা' : 'English'}
            </button>
            <div className="hidden items-center gap-2 sm:flex">
              <button type="button" onClick={() => handleOpenInquiry('BANK_POC')} className={`${btnGhost} !py-2`}>
                Request demo
              </button>
              <Link href="/app" className={`${btnPrimary} !py-2`}>
                Launch app
                <ArrowRight className="h-4 w-4" aria-hidden="true" />
              </Link>
            </div>
            <button
              type="button"
              onClick={() => setIsMobileNavOpen((v) => !v)}
              className="rounded-lg p-2 text-fg-secondary hover:bg-surface-hover md:hidden cursor-pointer"
              aria-label={isMobileNavOpen ? 'Close menu' : 'Open menu'}
              aria-expanded={isMobileNavOpen}
            >
              {isMobileNavOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </button>
          </div>
        </div>

        {isMobileNavOpen && (
          <div className="absolute inset-x-0 top-16 border-b border-line bg-panel p-4 md:hidden shadow-xl">
            <nav className="flex flex-col gap-1 text-base" aria-label="Mobile">
              {[...NAV, { href: '/governance', label: 'Model card' }].map((n) => (
                <a
                  key={n.href}
                  href={n.href}
                  onClick={() => setIsMobileNavOpen(false)}
                  className="rounded-md px-3 py-2.5 text-fg-secondary hover:bg-surface-hover hover:text-fg"
                >
                  {n.label}
                </a>
              ))}
            </nav>
            <div className="mt-3 grid grid-cols-2 gap-2">
              <button type="button" onClick={() => handleOpenInquiry('BANK_POC')} className={btnGhost}>
                Request demo
              </button>
              <Link href="/app" className={btnPrimary}>
                Launch app
              </Link>
            </div>
          </div>
        )}
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden border-b border-line px-4 pb-14 pt-16 sm:px-6 sm:pt-20">
        <div className="pointer-events-none absolute inset-x-0 top-0 h-[24rem] bg-[radial-gradient(60%_60%_at_50%_0%,rgba(16,185,129,0.12),transparent)]" />
        <div className="relative mx-auto max-w-4xl text-center">
          <p className="mb-4 inline-flex items-center gap-2 rounded-full border border-accent/30 bg-accent-subtle px-3 py-1 text-xs font-mono font-medium text-accent-text">
            Platform v3.0 · C-STGB v3.2 Engine · Cloud Sandbox (Air-Gap Ready)
          </p>
          <h1 className="text-3xl font-bold leading-[1.12] tracking-tight text-fg sm:text-5xl">
            Eliminate 84% of False Positives with Provable Conformal Risk Guarantees.
          </h1>
          <p className="mx-auto mt-5 max-w-2xl text-base sm:text-lg leading-relaxed text-muted">
            {t('landing_subheadline')}
          </p>
          <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
            <Link href="/app" className={`${btnPrimary} w-full sm:w-auto`}>
              Open the live demo
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </Link>
            <button type="button" onClick={() => handleOpenInquiry('BANK_POC')} className={`${btnGhost} w-full sm:w-auto`}>
              Request a bank PoC
            </button>
          </div>
        </div>

        <div className="relative mx-auto mt-12 max-w-5xl">
          <dl className="grid grid-cols-2 gap-px overflow-hidden rounded-2xl border border-line bg-line lg:grid-cols-4">
            {METRICS.map((m) => (
              <div key={m.label} className="bg-panel p-5">
                <dt className="text-xs font-medium text-muted">{m.label}</dt>
                <dd className="mt-1 text-2xl sm:text-3xl font-semibold tabular-aml font-mono text-fg">{m.value}</dd>
                <p className="mt-1 text-xs text-muted">{m.note}</p>
              </div>
            ))}
          </dl>
          <p className="mt-3 text-center text-xs text-muted">
            Evaluated on synthetic Bangladesh banking data (7-day replay; 14-dataset corpus: 68.05% Macro F1, 91.42% Elliptic-v1, 0.45 ms P50), not live customer traffic.{' '}
            <Link href="/governance" className="text-accent-text underline underline-offset-2">
              See the model card
            </Link>
          </p>
        </div>
      </section>

      {/* Product preview */}
      <section className="border-b border-line px-4 py-14 sm:px-6">
        <div className="mx-auto max-w-6xl">
          <div className="mx-auto mb-8 max-w-2xl text-center">
            <h2 className="text-2xl font-semibold text-fg sm:text-3xl">Eleven modules, one workflow</h2>
            <p className="mt-2 text-sm text-muted">From alert triage to BFIU goAML STR dispatch in a single audit-locked ledger.</p>
          </div>
          <ProductVisualPreview />
        </div>
      </section>

      {/* 4-Step Pipeline */}
      <section id="how" className="scroll-mt-20 border-b border-line px-4 py-14 sm:px-6">
        <div className="mx-auto max-w-6xl">
          <h2 className="mx-auto mb-8 max-w-2xl text-center text-2xl font-semibold text-fg sm:text-3xl">Four-stage surveillance pipeline</h2>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {STEPS.map((s, i) => (
              <div key={s.title} className="rounded-2xl border border-line bg-panel p-5">
                <div className="mb-3 flex items-center gap-3">
                  <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-accent-subtle text-accent-text">
                    <s.icon className="h-4 w-4" aria-hidden="true" />
                  </span>
                  <span className="text-xs font-mono text-muted">Stage 0{i + 1}</span>
                </div>
                <h3 className="text-base font-semibold text-fg">{s.title}</h3>
                <p className="mt-1.5 text-sm leading-relaxed text-muted">{s.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Conformal tiering */}
      <section id="tiering" className="scroll-mt-20 border-b border-line px-4 py-14 sm:px-6">
        <div className="mx-auto max-w-6xl">
          <div className="mx-auto mb-8 max-w-2xl text-center">
            <h2 className="text-2xl font-semibold text-fg sm:text-3xl">{t('conformal_title')}</h2>
            <p className="mt-2 text-sm text-muted">
              {t('conformal_desc')} Empirical Missed-Illicit Rate (FNR): 0.76% (bounded FNR &lt;= alpha = 0.01).
            </p>
          </div>
          <ConformalLivePreviewWidget />
        </div>
      </section>

      {/* Security */}
      <section id="security" className="scroll-mt-20 border-b border-line px-4 py-14 sm:px-6">
        <div className="mx-auto max-w-6xl">
          <div className="mx-auto mb-8 max-w-2xl text-center">
            <p className="mb-3 inline-block rounded-full border border-accent/30 bg-accent-subtle px-3 py-1 text-xs font-mono font-medium text-accent-text">
              OWASP ASVS Level 2 Aligned Architecture
            </p>
            <h2 className="text-2xl font-semibold text-fg sm:text-3xl">{t('security_title')}</h2>
            <p className="mt-2 text-xs text-muted">
              Aligned with MLPA 2012 (§§ 6, 25), ATA 2009, MLPR 2019, and BFIU Circulars 24, 26, 31 &amp; 32.
            </p>
          </div>
          <div className="grid gap-4 md:grid-cols-2">
            {SECURITY.map((s) => (
              <div key={s.tKey} className="flex items-start gap-4 rounded-2xl border border-line bg-panel p-5">
                <span className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl ${s.tone}`}>
                  <s.icon className="h-5 w-5" aria-hidden="true" />
                </span>
                <div>
                  <h3 className="font-semibold text-fg">{t(s.tKey)}</h3>
                  <p className="mt-1 text-sm leading-relaxed text-muted">{s.body}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="scroll-mt-20 border-b border-line px-4 py-14 sm:px-6">
        <div className="mx-auto max-w-6xl">
          <div className="mx-auto mb-8 max-w-2xl text-center">
            <h2 className="text-2xl font-semibold text-fg sm:text-3xl">{t('pricing_title')}</h2>
            <p className="mt-2 text-sm text-muted">Evaluate in this public cloud sandbox or deploy inside an air-gapped bank intranet.</p>
          </div>
          <div className="grid gap-5 md:grid-cols-3">
            {PLANS.map((p) => (
              <div
                key={p.key}
                className={`relative flex flex-col rounded-2xl bg-panel p-6 ${
                  p.featured ? 'border-2 border-accent' : 'border border-line'
                }`}
              >
                {p.featured && (
                  <span className="absolute -top-3 left-6 rounded-full bg-accent px-3 py-0.5 text-xs font-semibold text-accent-fg">
                    Recommended
                  </span>
                )}
                <h3 className="text-lg font-semibold text-fg">{t(p.tKey)}</h3>
                <p className="mt-3 text-3xl font-semibold text-fg tabular-aml">
                  {p.price} <span className="text-sm font-normal text-muted">/ {p.unit}</span>
                </p>
                <ul className="mt-5 flex-1 space-y-2.5 text-sm text-fg-secondary">
                  {p.features.map((f) => (
                    <li key={f} className="flex items-start gap-2">
                      <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-accent-text" aria-hidden="true" />
                      <span>{f}</span>
                    </li>
                  ))}
                </ul>
                {p.href ? (
                  <Link href={p.href} className={`${btnGhost} mt-6`}>
                    {p.cta}
                  </Link>
                ) : (
                  <button
                    type="button"
                    onClick={() => handleOpenInquiry(p.inquiry as InquiryType)}
                    className={`${p.featured ? btnPrimary : btnGhost} mt-6`}
                  >
                    {p.cta}
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-canvas px-4 py-10 text-sm text-muted sm:px-6">
        <div className="mx-auto max-w-6xl">
          <div className="flex flex-col items-center justify-between gap-5 md:flex-row">
            <div className="flex items-center gap-2">
              <span className="h-2.5 w-2.5 rounded-full bg-accent" />
              <span className="font-semibold text-fg">Intelligent-AML Platform v3.0 · C-STGB v3.2 Engine</span>
            </div>
            <nav className="flex flex-wrap items-center justify-center gap-x-5 gap-y-2" aria-label="Footer">
              <button type="button" onClick={() => setIsPrivacyModalOpen(true)} className="hover:text-fg cursor-pointer">
                Privacy
              </button>
              <button type="button" onClick={() => setIsTermsModalOpen(true)} className="hover:text-fg cursor-pointer">
                Terms
              </button>
              <Link href="/cookies" className="hover:text-fg">
                Cookies
              </Link>
              <Link href="/governance" className="hover:text-fg">
                Model card
              </Link>
              <Link href="/app" className="font-medium text-accent-text hover:underline">
                Open the app &rarr;
              </Link>
            </nav>
          </div>
          <p className="mt-6 border-t border-line pt-5 text-center text-xs text-muted md:text-left">
            &copy; 2026 Intelligent-AML. Research &amp; evaluation prototype running on synthetic data. Not legal advice or a regulator-certified product.
          </p>
        </div>
      </footer>

      <InstitutionalInquiryModal
        isOpen={inquiryModalOpen}
        onClose={() => setInquiryModalOpen(false)}
        inquiryType={inquiryType}
      />

      {isPrivacyModalOpen && (
        <div role="dialog" aria-modal="true" aria-labelledby="privacy-dialog-title" className="fixed inset-0 z-50 bg-black/75 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="w-full max-w-2xl bg-panel border border-line rounded-xl shadow-2xl p-6 relative text-fg max-h-[80vh] overflow-y-auto">
            <button type="button" onClick={() => setIsPrivacyModalOpen(false)} className="absolute top-4 right-4 p-1.5 rounded-md hover:bg-surface-hover text-muted hover:text-fg cursor-pointer" aria-label="Close dialog">
              <X className="w-5 h-5" />
            </button>
            <h3 id="privacy-dialog-title" className="text-base font-semibold text-fg mb-1">Privacy Policy &amp; Sovereign Data Governance</h3>
            <p className="text-xs font-mono text-accent-text mb-4">Bangladesh Bank ICT Security Guidelines &amp; Banking Companies Act 1991 § 46</p>
            <div className="space-y-3 text-xs text-fg-secondary leading-relaxed">
              <p><strong>1. Sovereign Residency:</strong> In on-premises mode (<code>APP_MODE=onprem</code>), payloads and customer records stay inside the bank&apos;s private perimeter.</p>
              <p><strong>2. Server-Side PII Masking:</strong> Identifiers stay masked by default. Audited unmasking expires automatically in 60 seconds.</p>
              <p><strong>3. Full Draft Page:</strong> View the standalone <Link href="/privacy" className="text-accent-text underline">Privacy Notice</Link>.</p>
            </div>
          </div>
        </div>
      )}

      {isTermsModalOpen && (
        <div role="dialog" aria-modal="true" aria-labelledby="terms-dialog-title" className="fixed inset-0 z-50 bg-black/75 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="w-full max-w-2xl bg-panel border border-line rounded-xl shadow-2xl p-6 relative text-fg max-h-[80vh] overflow-y-auto">
            <button type="button" onClick={() => setIsTermsModalOpen(false)} className="absolute top-4 right-4 p-1.5 rounded-md hover:bg-surface-hover text-muted hover:text-fg cursor-pointer" aria-label="Close dialog">
              <X className="w-5 h-5" />
            </button>
            <h3 id="terms-dialog-title" className="text-base font-semibold text-fg mb-1">Terms of Institutional Evaluation</h3>
            <p className="text-xs font-mono text-accent-text mb-4">Commercial Evaluation &amp; Research Prototype Notice</p>
            <div className="space-y-3 text-xs text-fg-secondary leading-relaxed">
              <p><strong>1. Scope:</strong> Provided for compliance evaluation and AML/CFT workflow testing under MLPA 2012.</p>
              <p><strong>2. Maker-Checker Governance:</strong> Final regulatory filings require independent verification by an authorized Officer / MLRO.</p>
              <p><strong>3. Full Draft Page:</strong> View the standalone <Link href="/terms" className="text-accent-text underline">Evaluation Terms</Link>.</p>
            </div>
          </div>
        </div>
      )}

      {!isCookieDismissed && (
        <div
          role="region"
          aria-label="Cookie notice"
          className="fixed bottom-4 left-4 right-4 sm:right-auto sm:max-w-sm z-40 rounded-xl border border-line bg-panel p-4 shadow-2xl"
        >
          <p className="text-sm text-fg-secondary">
            We only use strictly necessary cookies to keep your session and workspace settings intact.{' '}
            <button type="button" onClick={() => setIsPrivacyModalOpen(true)} className="text-accent-text underline underline-offset-2 cursor-pointer">
              Details
            </button>
          </p>
          <div className="mt-3 flex justify-end">
            <button
              type="button"
              onClick={handleAcknowledgeCookie}
              className="rounded-lg bg-accent px-3 py-1.5 text-sm font-semibold text-accent-fg hover:bg-accent-hover cursor-pointer"
            >
              Got it
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
