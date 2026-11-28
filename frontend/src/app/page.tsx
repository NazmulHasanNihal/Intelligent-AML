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
  Scale,
  Shield,
  Users,
  X,
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';
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
  { label: 'Macro F1', value: '94.5%', note: 'vs. baselines' },
  { label: 'Noise reduction', value: '84.2%', note: '7-day replay' },
  { label: 'Scoring latency', value: '< 200 µs', note: 'scorer only, p50' },
  { label: 'Conformal coverage', value: '99.04%', note: 'target 99.00%' },
];

const STEPS = [
  { icon: Layers, title: 'Score every wire', body: 'A spatio-temporal graph model reads each transaction in the context of the accounts around it.' },
  { icon: Scale, title: 'Bound the risk', body: 'Conformal prediction gives each alert a calibrated set, so uncertainty is explicit instead of hidden.' },
  { icon: Users, title: 'Route by certainty', body: 'Sure hits are held, ambiguous ones go to an officer, confident clears flow through.' },
];

const SECURITY = [
  { icon: Lock, tone: 'indigo', tKey: 'security_point1', body: 'SHA-256 chain over RFC 8785 JSON with Ed25519 checkpoints; admissibility-ready under Bangladesh Evidence Act §§ 65A–65B & 73A.' },
  { icon: Users, tone: 'emerald', tKey: 'security_point2', body: 'Maker and checker roles enforced on the server, not just in the UI.' },
  { icon: Shield, tone: 'amber', tKey: 'security_point3', body: 'Personal data is masked by default. Reveal needs a reason, expires in 60 seconds and is logged.' },
  { icon: FileCheck2, tone: 'cyan', tKey: 'security_point4', body: 'UNODC goAML v4.2 STR/SAR export with mandatory attachments and MLPA 2012 § 6 anti-tipping-off checks.' },
] as const;

const TONES: Record<string, string> = {
  indigo: 'bg-indigo-500/10 text-indigo-300',
  emerald: 'bg-emerald-500/10 text-emerald-300',
  amber: 'bg-amber-500/10 text-amber-300',
  cyan: 'bg-cyan-500/10 text-cyan-300',
};

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
    unit: '30-day evaluation',
    features: ['Synthetic Bangladesh dataset', 'All 11 modules', 'One-command reproduction'],
    cta: 'Open the sandbox',
    href: '/app',
  },
  {
    key: 'bank',
    tKey: 'plan_bank',
    price: 'Custom',
    unit: 'annual SLA',
    features: ['On-prem Kubernetes / Helm', 'Core banking and SWIFT connectors', 'Tamper-evident audit ledger', '24/7 support'],
    cta: 'Request a bank PoC',
    featured: true,
    inquiry: 'BANK_POC',
  },
  {
    key: 'fiu',
    tKey: 'plan_fiu',
    price: 'Sovereign',
    unit: 'government mandate',
    features: ['Multi-institution flow graph', 'goAML central gateway', 'HSM-backed keys'],
    cta: 'Schedule a briefing',
    inquiry: 'SOVEREIGN',
  },
];

export default function EnterpriseLandingPage() {
  const { language, toggleLanguage, t } = useBankingStore();

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
      /* storage unavailable: leave the notice hidden */
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
    'inline-flex items-center justify-center gap-2 rounded-lg bg-emerald-500 px-5 py-2.5 text-sm font-semibold text-slate-950 transition-colors hover:bg-emerald-400';
  const btnGhost =
    'inline-flex items-center justify-center gap-2 rounded-lg border border-slate-700 px-5 py-2.5 text-sm font-semibold text-slate-100 transition-colors hover:bg-slate-800';

  return (
    <div className="flex min-h-screen flex-col bg-canvas font-sans text-slate-100 selection:bg-emerald-500/30">
      {/* Header */}
      <header className="sticky top-0 z-40 h-16 w-full border-b border-slate-800 bg-canvas/90 backdrop-blur-md">
        <div className="mx-auto flex h-full max-w-6xl items-center justify-between gap-4 px-4 sm:px-6">
          <Link href="/" className="flex shrink-0 items-center gap-2.5" aria-label="Intelligent-AML home">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg border border-emerald-500/30 bg-emerald-500/10">
              <span className="h-2.5 w-2.5 rounded-full bg-emerald-400" />
            </span>
            <span className="text-base font-semibold">Intelligent-AML</span>
            <span className="hidden rounded border border-slate-800 px-1.5 py-0.5 text-xs font-mono text-slate-400 sm:inline">
              Platform v3.0
            </span>
          </Link>

          <nav className="hidden items-center gap-7 text-sm text-slate-300 md:flex" aria-label="Primary">
            {NAV.map((n) => (
              <a key={n.href} href={n.href} className="whitespace-nowrap transition-colors hover:text-white">
                {n.label}
              </a>
            ))}
            <Link href="/governance" className="whitespace-nowrap transition-colors hover:text-white">
              Model card
            </Link>
          </nav>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={toggleLanguage}
              className="rounded-md px-2.5 py-1.5 text-sm text-slate-300 transition-colors hover:bg-slate-800 hover:text-white"
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
              className="rounded-md p-2 text-slate-300 hover:bg-slate-800 md:hidden"
              aria-label={isMobileNavOpen ? 'Close menu' : 'Open menu'}
              aria-expanded={isMobileNavOpen}
            >
              {isMobileNavOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </button>
          </div>
        </div>

        {isMobileNavOpen && (
          <div className="absolute inset-x-0 top-16 border-b border-slate-800 bg-canvas p-4 md:hidden">
            <nav className="flex flex-col gap-1 text-base" aria-label="Mobile">
              {[...NAV, { href: '/governance', label: 'Model card' }].map((n) => (
                <a
                  key={n.href}
                  href={n.href}
                  onClick={() => setIsMobileNavOpen(false)}
                  className="rounded-md px-3 py-2.5 text-slate-200 hover:bg-slate-800"
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
      <section className="relative overflow-hidden border-b border-slate-800/60 px-4 pb-16 pt-20 sm:px-6 sm:pt-24">
        <div className="pointer-events-none absolute inset-x-0 top-0 h-[28rem] bg-[radial-gradient(60%_60%_at_50%_0%,rgba(16,185,129,0.14),transparent)]" />
        <div className="relative mx-auto max-w-4xl text-center">
          <p className="mb-5 inline-flex items-center gap-2 rounded-full border border-emerald-500/25 bg-emerald-500/10 px-3 py-1 text-sm text-emerald-300">
            C-STGB v3.2 · BFIU 2026 &amp; SR 11-7 aligned
          </p>
          <h1 className="text-4xl font-bold leading-[1.1] tracking-tight text-white sm:text-5xl lg:text-6xl">
            Eliminate 84% of False Positives with Provable Conformal Risk Guarantees.
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg leading-relaxed text-slate-300">
            {t('landing_subheadline')}
          </p>
          <div className="mt-9 flex flex-col items-center justify-center gap-3 sm:flex-row">
            <Link href="/app" className={`${btnPrimary} w-full sm:w-auto`}>
              Open the live demo
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </Link>
            <button type="button" onClick={() => handleOpenInquiry('BANK_POC')} className={`${btnGhost} w-full sm:w-auto`}>
              Request a bank PoC
            </button>
          </div>
        </div>

        <div className="relative mx-auto mt-14 max-w-5xl">
          <dl className="grid grid-cols-2 gap-px overflow-hidden rounded-2xl border border-slate-800 bg-slate-800 lg:grid-cols-4">
            {METRICS.map((m) => (
              <div key={m.label} className="bg-canvas p-5">
                <dt className="text-sm text-slate-400">{m.label}</dt>
                <dd className="mt-1 text-3xl font-semibold tabular-nums text-white">{m.value}</dd>
                <p className="mt-1 text-xs text-slate-500">{m.note}</p>
              </div>
            ))}
          </dl>
          <p className="mt-3 text-center text-xs text-slate-500">
            Measured on synthetic Bangladesh banking data (7-day replay; 14-dataset corpus: 68.05% Macro F1, 91.42% Elliptic-v1, 0.45 ms P50), not live customer traffic.{' '}
            <Link href="/governance" className="text-slate-300 underline underline-offset-2 hover:text-white">
              See the model card
            </Link>
          </p>
        </div>
      </section>

      {/* Product preview */}
      <section className="border-b border-slate-800/60 px-4 py-16 sm:px-6">
        <div className="mx-auto max-w-6xl">
          <div className="mx-auto mb-10 max-w-2xl text-center">
            <h2 className="text-2xl font-semibold text-white sm:text-3xl">Eleven modules, one workflow</h2>
            <p className="mt-3 text-slate-400">From alert triage to the filed report, in a single workspace.</p>
          </div>
          <ProductVisualPreview />
        </div>
      </section>

      {/* How it works */}
      <section id="how" className="scroll-mt-20 border-b border-slate-800/60 px-4 py-16 sm:px-6">
        <div className="mx-auto max-w-6xl">
          <h2 className="mx-auto mb-10 max-w-2xl text-center text-2xl font-semibold text-white sm:text-3xl">How it works</h2>
          <div className="grid gap-5 md:grid-cols-3">
            {STEPS.map((s, i) => (
              <div key={s.title} className="rounded-2xl border border-slate-800 bg-canvas p-6">
                <div className="mb-4 flex items-center gap-3">
                  <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/10 text-emerald-300">
                    <s.icon className="h-5 w-5" aria-hidden="true" />
                  </span>
                  <span className="text-sm text-slate-500">Step {i + 1}</span>
                </div>
                <h3 className="text-lg font-semibold text-white">{s.title}</h3>
                <p className="mt-2 leading-relaxed text-slate-400">{s.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Conformal tiering */}
      <section id="tiering" className="scroll-mt-20 border-b border-slate-800/60 px-4 py-16 sm:px-6">
        <div className="mx-auto max-w-6xl">
          <div className="mx-auto mb-10 max-w-2xl text-center">
            <h2 className="text-2xl font-semibold text-white sm:text-3xl">{t('conformal_title')}</h2>
            <p className="mt-3 text-slate-400">
              {t('conformal_desc')} Empirical missed-illicit rate (FNR): 0.76% (within α = 1.00% conformal bound).
            </p>
          </div>
          <ConformalLivePreviewWidget />
        </div>
      </section>

      {/* Security */}
      <section id="security" className="scroll-mt-20 border-b border-slate-800/60 px-4 py-16 sm:px-6">
        <div className="mx-auto max-w-6xl">
          <div className="mx-auto mb-10 max-w-2xl text-center">
            <p className="mb-3 inline-block rounded-full border border-indigo-500/30 bg-indigo-500/10 px-3 py-1 text-sm text-indigo-300">
              OWASP ASVS Level 2 aligned architecture
            </p>
            <h2 className="text-2xl font-semibold text-white sm:text-3xl">{t('security_title')}</h2>
            <p className="mt-3 text-sm text-slate-400">
              BFIU Master Circular 26 &amp; Circular 24 (TBML), Circular 32 (Sept 2026), Circular Letters 02 &amp; 03 (Feb 2026), Circular Letter 05 (Aug 2026), MLPA 2012 (§§ 6, 25), ATA 2009, and MLPR 2019.
            </p>
          </div>
          <div className="grid gap-5 md:grid-cols-2">
            {SECURITY.map((s) => (
              <div key={s.tKey} className="flex items-start gap-4 rounded-2xl border border-slate-800 bg-canvas p-6">
                <span className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl ${TONES[s.tone]}`}>
                  <s.icon className="h-5 w-5" aria-hidden="true" />
                </span>
                <div>
                  <h3 className="font-semibold text-white">{t(s.tKey)}</h3>
                  <p className="mt-1 leading-relaxed text-slate-400">{s.body}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="scroll-mt-20 border-b border-slate-800/60 px-4 py-16 sm:px-6">
        <div className="mx-auto max-w-6xl">
          <div className="mx-auto mb-10 max-w-2xl text-center">
            <h2 className="text-2xl font-semibold text-white sm:text-3xl">{t('pricing_title')}</h2>
            <p className="mt-3 text-slate-400">Run it in a sovereign cloud or fully inside your own data center.</p>
          </div>
          <div className="grid gap-6 md:grid-cols-3">
            {PLANS.map((p) => (
              <div
                key={p.key}
                className={`relative flex flex-col rounded-2xl bg-canvas p-6 ${
                  p.featured ? 'border-2 border-emerald-500/50' : 'border border-slate-800'
                }`}
              >
                {p.featured && (
                  <span className="absolute -top-3 left-6 rounded-full bg-emerald-500 px-3 py-0.5 text-xs font-semibold text-slate-950">
                    Most popular
                  </span>
                )}
                <h3 className="text-lg font-semibold text-white">{t(p.tKey)}</h3>
                <p className="mt-4 text-3xl font-semibold text-white">
                  {p.price} <span className="text-sm font-normal text-slate-400">/ {p.unit}</span>
                </p>
                <ul className="mt-6 flex-1 space-y-3 text-slate-300">
                  {p.features.map((f) => (
                    <li key={f} className="flex items-start gap-2.5">
                      <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-emerald-400" aria-hidden="true" />
                      <span>{f}</span>
                    </li>
                  ))}
                </ul>
                {p.href ? (
                  <Link href={p.href} className={`${btnGhost} mt-8`}>
                    {p.cta}
                  </Link>
                ) : (
                  <button
                    type="button"
                    onClick={() => handleOpenInquiry(p.inquiry as InquiryType)}
                    className={`${p.featured ? btnPrimary : btnGhost} mt-8`}
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
      <footer className="bg-canvas px-4 py-10 text-sm text-slate-400 sm:px-6">
        <div className="mx-auto max-w-6xl">
          <div className="flex flex-col items-center justify-between gap-5 md:flex-row">
            <div className="flex items-center gap-2">
              <span className="h-2.5 w-2.5 rounded-full bg-emerald-400" />
              <span className="font-semibold text-slate-200">Intelligent-AML Platform v3.0 · C-STGB v3.2 Engine</span>
            </div>
            <nav className="flex flex-wrap items-center justify-center gap-x-6 gap-y-2" aria-label="Footer">
              <button type="button" onClick={() => setIsPrivacyModalOpen(true)} className="hover:text-white">
                Privacy
              </button>
              <button type="button" onClick={() => setIsTermsModalOpen(true)} className="hover:text-white">
                Terms
              </button>
              <Link href="/governance" className="hover:text-white">
                Model card
              </Link>
              <Link href="/app" className="font-medium text-emerald-400 hover:text-emerald-300">
                Open the app &rarr;
              </Link>
            </nav>
          </div>
          <p className="mt-8 border-t border-slate-800 pt-6 text-center text-xs text-slate-500 md:text-left">
            &copy; 2026 Intelligent-AML. Research prototype. Not legal advice. Not a certified regulated product.
          </p>
        </div>
      </footer>

      <InstitutionalInquiryModal
        isOpen={inquiryModalOpen}
        onClose={() => setInquiryModalOpen(false)}
        inquiryType={inquiryType}
      />

      {isPrivacyModalOpen && (
        <div role="dialog" aria-modal="true" aria-labelledby="privacy-dialog-title" className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="w-full max-w-2xl bg-panel border border-line rounded-xl shadow-2xl p-6 relative text-slate-100 max-h-[80vh] overflow-y-auto">
            <button type="button" onClick={() => setIsPrivacyModalOpen(false)} className="absolute top-4 right-4 p-1 rounded-md hover:bg-surface-2 text-slate-400 hover:text-slate-200" aria-label="Close dialog">
              <X className="w-5 h-5" />
            </button>
            <h3 id="privacy-dialog-title" className="text-base font-semibold text-slate-100 mb-1">Privacy Policy &amp; Sovereign Data Governance</h3>
            <p className="text-xs font-mono text-emerald-400 mb-4">Bangladesh Bank ICT Security Guidelines v3.0 &amp; Banking Companies Act 1991 § 46</p>
            <div className="space-y-3 text-xs text-slate-300 leading-relaxed">
              <p><strong>1. Sovereign Residency:</strong> In on-premises deployment mode (<code>APP_MODE=onprem</code>), transaction payloads and customer records stay strictly within the bank&apos;s private network perimeter.</p>
              <p><strong>2. Server-Side PII Masking:</strong> NIDs, account numbers, and entity names remain masked by default. Audited unmasking requires a written justification and auto-expires in 60 seconds.</p>
              <p><strong>3. Synthetic Evaluation Data:</strong> Public sandbox sessions contain strictly synthetic transaction data with zero real customer PII.</p>
            </div>
          </div>
        </div>
      )}

      {isTermsModalOpen && (
        <div role="dialog" aria-modal="true" aria-labelledby="terms-dialog-title" className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="w-full max-w-2xl bg-panel border border-line rounded-xl shadow-2xl p-6 relative text-slate-100 max-h-[80vh] overflow-y-auto">
            <button type="button" onClick={() => setIsTermsModalOpen(false)} className="absolute top-4 right-4 p-1 rounded-md hover:bg-surface-2 text-slate-400 hover:text-slate-200" aria-label="Close dialog">
              <X className="w-5 h-5" />
            </button>
            <h3 id="terms-dialog-title" className="text-base font-semibold text-slate-100 mb-1">Terms of Institutional Evaluation</h3>
            <p className="text-xs font-mono text-emerald-400 mb-4">Commercial Evaluation &amp; Research Prototype Notice</p>
            <div className="space-y-3 text-xs text-slate-300 leading-relaxed">
              <p><strong>1. Scope:</strong> Provided for institutional compliance testing, model validation, and AML/CFT workflow evaluation under MLPA 2012.</p>
              <p><strong>2. Maker-Checker Governance:</strong> Final regulatory filings (STR/CTR) require independent verification and sign-off by an authorized Compliance Officer / MLRO.</p>
              <p><strong>3. Statutory Disclaimer:</strong> Software outputs do not constitute legal advice or official regulatory certification.</p>
            </div>
          </div>
        </div>
      )}

      {/* 12. Cookie notice (strictly necessary cookies only) */}
      {!isCookieDismissed && (
        <div
          role="region"
          aria-label="Cookie notice"
          className="fixed bottom-4 left-4 right-4 sm:right-auto sm:max-w-sm z-40 rounded-xl border border-slate-700 bg-slate-900 p-4 shadow-2xl"
        >
          <p className="text-sm text-slate-300">
            We only use cookies needed to keep you signed in. No ads, no tracking.{' '}
            <button type="button" onClick={() => setIsPrivacyModalOpen(true)} className="text-emerald-400 underline underline-offset-2 hover:text-emerald-300">
              Details
            </button>
          </p>
          <div className="mt-3 flex justify-end">
            <button
              type="button"
              onClick={handleAcknowledgeCookie}
              className="rounded-md bg-emerald-500 px-3 py-1.5 text-sm font-semibold text-slate-950 hover:bg-emerald-400"
            >
              Got it
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
