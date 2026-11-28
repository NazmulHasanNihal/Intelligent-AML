'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  ArrowRight,
  CheckCircle2,
  Lock,
  Layers,
  Zap,
  FileCheck2,
  Globe,
  Building2,
  Shield,
  X,
  Menu,
  ExternalLink
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { ConformalLivePreviewWidget } from '@/components/landing/ConformalLivePreviewWidget';
import { ProductVisualPreview } from '@/components/landing/ProductVisualPreview';
import { InstitutionalInquiryModal } from '@/components/landing/InstitutionalInquiryModal';

export default function EnterpriseLandingPage() {
  const { language, toggleLanguage, t } = useBankingStore();

  const [inquiryModalOpen, setInquiryModalOpen] = useState(false);
  const [inquiryType, setInquiryType] = useState<'EVALUATION' | 'BANK_POC' | 'SOVEREIGN'>('BANK_POC');
  const [isPrivacyModalOpen, setIsPrivacyModalOpen] = useState(false);
  const [isTermsModalOpen, setIsTermsModalOpen] = useState(false);
  const [isMobileNavOpen, setIsMobileNavOpen] = useState(false);
  const [isCookieDismissed, setIsCookieDismissed] = useState(true);

  useEffect(() => {
    const consent = localStorage.getItem('aml_cookie_consent');
    if (!consent) {
      setIsCookieDismissed(false);
    }
  }, []);

  const handleAcknowledgeCookie = () => {
    localStorage.setItem('aml_cookie_consent', 'acknowledged');
    document.cookie = 'aml_consent=1; path=/; max-age=31536000; SameSite=Strict; Secure';
    setIsCookieDismissed(true);
  };

  const handleOpenInquiry = (type: 'EVALUATION' | 'BANK_POC' | 'SOVEREIGN') => {
    setInquiryType(type);
    setInquiryModalOpen(true);
    setIsMobileNavOpen(false);
  };

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setIsMobileNavOpen(false);
        setInquiryModalOpen(false);
        setIsPrivacyModalOpen(false);
        setIsTermsModalOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div className="min-h-screen bg-[#080C12] text-slate-100 flex flex-col font-sans selection:bg-emerald-500/25 selection:text-emerald-200">
      {/* 1. Navigation Header */}
      <header className="sticky top-0 z-40 w-full h-14 border-b border-[#1E2734] bg-[#080C12]/95 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 h-full flex items-center justify-between gap-4">
          <Link href="/" className="flex items-center gap-2.5 shrink-0">
            <div className="w-7 h-7 rounded-md bg-[#111926] border border-[#253142] flex items-center justify-center">
              <Shield className="w-3.5 h-3.5 text-emerald-400" />
            </div>
            <div className="flex items-baseline gap-2">
              <span className="font-semibold text-sm tracking-tight text-slate-100">
                Intelligent-AML
              </span>
              <span className="text-[10px] font-mono text-slate-400 hidden sm:inline">
                Platform v3.0
              </span>
            </div>
          </Link>

          <nav className="hidden lg:flex items-center gap-6 text-xs text-slate-400">
            <a href="#problem" className="hover:text-slate-100 transition-colors">
              Problem
            </a>
            <a href="#differentiators" className="hover:text-slate-100 transition-colors">
              Architecture
            </a>
            <a href="#tiering" className="hover:text-slate-100 transition-colors">
              Conformal Calibration
            </a>
            <Link href="/governance" className="text-slate-200 hover:text-emerald-400 font-medium transition-colors">
              Model Card (SR 11-7)
            </Link>
            <a href="#security" className="hover:text-slate-100 transition-colors">
              Security &amp; BFIU
            </a>
            <a href="#pricing" className="hover:text-slate-100 transition-colors">
              Deployment
            </a>
          </nav>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={toggleLanguage}
              className="px-2.5 py-1.5 rounded-md text-xs font-mono text-slate-300 hover:text-slate-100 bg-[#0D121A] hover:bg-[#141C27] border border-[#1E2734] transition-colors cursor-pointer flex items-center gap-1.5"
              title="Toggle English / বাংলা"
            >
              <Globe className="w-3.5 h-3.5 text-slate-400" />
              <span>{language === 'en' ? 'EN' : 'বাং'}</span>
            </button>

            <button
              type="button"
              onClick={() => handleOpenInquiry('EVALUATION')}
              className="hidden sm:inline-flex px-3 py-1.5 rounded-md text-xs font-medium bg-[#0D121A] hover:bg-[#141C27] text-slate-200 border border-[#253142] transition-colors cursor-pointer"
            >
              Request Briefing
            </button>

            <Link
              href="/app"
              className="px-3.5 py-1.5 rounded-md text-xs font-semibold bg-emerald-500 hover:bg-emerald-400 text-slate-950 transition-colors flex items-center gap-1.5"
            >
              <span>{language === 'en' ? 'Open Workspace' : 'ওএস চালু করুন'}</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>

            <button
              type="button"
              onClick={() => setIsMobileNavOpen(!isMobileNavOpen)}
              className="p-1.5 rounded-md bg-[#0D121A] border border-[#1E2734] text-slate-400 hover:text-slate-200 lg:hidden cursor-pointer"
              aria-label="Toggle navigation menu"
              aria-expanded={isMobileNavOpen}
            >
              {isMobileNavOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {isMobileNavOpen && (
          <div className="lg:hidden fixed inset-x-0 top-14 bg-[#0D121A] border-b border-[#1E2734] p-5 shadow-2xl space-y-4 z-50">
            <nav className="flex flex-col space-y-3 text-sm">
              <a href="#problem" onClick={() => setIsMobileNavOpen(false)} className="text-slate-300 hover:text-emerald-400 py-1">
                Legacy AML Problem
              </a>
              <a href="#differentiators" onClick={() => setIsMobileNavOpen(false)} className="text-slate-300 hover:text-emerald-400 py-1">
                Architecture (12 Invariants)
              </a>
              <a href="#tiering" onClick={() => setIsMobileNavOpen(false)} className="text-slate-300 hover:text-emerald-400 py-1">
                Conformal Risk Tiering
              </a>
              <Link href="/governance" onClick={() => setIsMobileNavOpen(false)} className="text-emerald-400 font-medium py-1">
                Model Card (SR 11-7 / BFIU)
              </Link>
              <a href="#security" onClick={() => setIsMobileNavOpen(false)} className="text-slate-300 hover:text-emerald-400 py-1">
                Security &amp; Bangladesh BFIU
              </a>
              <a href="#pricing" onClick={() => setIsMobileNavOpen(false)} className="text-slate-300 hover:text-emerald-400 py-1">
                Deployment Options
              </a>
            </nav>

            <div className="pt-3 border-t border-[#1E2734] flex flex-col gap-2">
              <button
                type="button"
                onClick={() => handleOpenInquiry('BANK_POC')}
                className="w-full py-2.5 rounded-md text-xs font-medium bg-[#141C27] text-slate-200 border border-[#253142] text-center"
              >
                Request Bank PoC Brief
              </button>
              <Link
                href="/app"
                onClick={() => setIsMobileNavOpen(false)}
                className="w-full py-2.5 rounded-md text-xs font-semibold bg-emerald-500 text-slate-950 text-center"
              >
                Open Compliance Workspace (/app)
              </Link>
            </div>
          </div>
        )}
      </header>

      {/* 2. Asymmetric Split Hero with Live Interactive Workspace Preview */}
      <section className="py-12 lg:py-16 border-b border-[#1E2734]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
            {/* Left Copy */}
            <div className="lg:col-span-6 space-y-6">
              <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-md text-[11px] font-mono text-slate-300 bg-[#0D121A] border border-[#1E2734]">
                <span className="text-emerald-400 font-semibold">C-STGB v3.2</span>
                <span className="text-slate-600">·</span>
                <span>BFIU 2026 &amp; SR 11-7 Aligned</span>
              </div>

              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-semibold tracking-tight text-slate-50 leading-[1.12]">
                {t('landing_headline')}
              </h1>

              <p className="text-sm sm:text-base text-slate-400 leading-relaxed max-w-xl">
                {t('landing_subheadline')}
              </p>

              <div className="flex flex-wrap items-center gap-3 pt-1">
                <Link
                  href="/app"
                  className="px-5 py-2.5 rounded-md text-xs font-semibold bg-emerald-500 hover:bg-emerald-400 text-slate-950 transition-colors inline-flex items-center gap-2"
                >
                  <span>Open Banking Workspace</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
                <button
                  type="button"
                  onClick={() => handleOpenInquiry('BANK_POC')}
                  className="px-4 py-2.5 rounded-md text-xs font-medium bg-[#0D121A] hover:bg-[#141C27] text-slate-200 border border-[#253142] transition-colors inline-flex items-center gap-2 cursor-pointer"
                >
                  <span>Request Bank PoC Brief</span>
                  <ExternalLink className="w-3.5 h-3.5 text-slate-400" />
                </button>
              </div>

              {/* Clean Hairline Metrics Bar */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-6 border-t border-[#1E2734]">
                <div>
                  <div className="text-xl font-mono font-semibold text-slate-50 tabular-nums">94.5%</div>
                  <div className="text-[11px] text-slate-400 mt-0.5">Replay Macro F1</div>
                </div>
                <div>
                  <div className="text-xl font-mono font-semibold text-emerald-400 tabular-nums">84.2%</div>
                  <div className="text-[11px] text-slate-400 mt-0.5">Noise Reduction</div>
                </div>
                <div>
                  <div className="text-xl font-mono font-semibold text-slate-50 tabular-nums">&lt; 200 µs</div>
                  <div className="text-[11px] text-slate-400 mt-0.5">FastPath P50</div>
                </div>
                <div>
                  <div className="text-xl font-mono font-semibold text-slate-50 tabular-nums">99.04%</div>
                  <div className="text-[11px] text-slate-400 mt-0.5">Coverage (1 - α)</div>
                </div>
              </div>
            </div>

            {/* Right Interactive Preview */}
            <div className="lg:col-span-6">
              <ProductVisualPreview />
              <div className="mt-3 flex flex-wrap items-center justify-between gap-2 text-[11px] font-mono text-slate-500 px-1">
                <span>
                  Replay: 94.5% F1 (7d BD synthetic) · 14-dataset corpus: 68.05% Macro F1 (91.42% Elliptic-v1), 0.45 ms P50
                </span>
                <Link href="/governance" className="text-emerald-400 hover:text-emerald-300">
                  Full SR 11-7 Model Card &rarr;
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 3. Problem Ledger Grid */}
      <section id="problem" className="py-16 border-b border-[#1E2734]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6">
          <div className="max-w-2xl mb-10">
            <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">
              Compliance Bottlenecks
            </span>
            <h2 className="text-2xl sm:text-3xl font-semibold text-slate-100 tracking-tight">
              Why threshold-only AML systems overwhelm investigators
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 divide-y lg:divide-y-0 lg:divide-x divide-[#1E2734] border border-[#1E2734] rounded-xl bg-[#0D121A]">
            <div className="p-6 space-y-2">
              <span className="text-[11px] font-mono text-rose-400">01 · ALERT FATIGUE</span>
              <h3 className="text-sm font-semibold text-slate-100">95%+ False Alarm Volume</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Static rule limits bury analysts in routine payroll and supplier settlements, masking genuine layering rings.
              </p>
            </div>
            <div className="p-6 space-y-2">
              <span className="text-[11px] font-mono text-amber-400">02 · AUDITABILITY</span>
              <h3 className="text-sm font-semibold text-slate-100">Unexplained ML Scores</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Unattributed black-box models fail Federal Reserve SR 11-7 and Bangladesh Bank model risk inspections.
              </p>
            </div>
            <div className="p-6 space-y-2">
              <span className="text-[11px] font-mono text-slate-300">03 · TRADE FINANCE</span>
              <h3 className="text-sm font-semibold text-slate-100">TBML Over-Invoicing</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                SWIFT MT700 documentary credits move without cross-checking ASYCUDA customs tariff benchmarks.
              </p>
            </div>
            <div className="p-6 space-y-2">
              <span className="text-[11px] font-mono text-emerald-400">04 · REGULATORY FILING</span>
              <h3 className="text-sm font-semibold text-slate-100">goAML Schema Rejections</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Manual STR drafting breaks schema integrity, drops evidence hashes, and risks anti-tipping-off errors.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* 4. Core Technical Architecture */}
      <section id="differentiators" className="py-16 border-b border-[#1E2734] bg-[#0B0F17]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6">
          <div className="max-w-2xl mb-10">
            <span className="text-[11px] font-mono uppercase tracking-wider text-emerald-400 block mb-2">
              Architecture
            </span>
            <h2 className="text-2xl sm:text-3xl font-semibold text-slate-100 tracking-tight">
              Built for sub-millisecond interdiction and regulatory defensibility
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 rounded-xl bg-[#0D121A] border border-[#1E2734] space-y-4">
              <div className="flex items-center gap-2.5 text-slate-100">
                <Layers className="w-4 h-4 text-emerald-400" />
                <h3 className="text-sm font-semibold">12 Spatio-Temporal Invariants</h3>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed">
                Measures physical cash-flow conservation, cycle motifs, fan-in burst intensity, and structuring proximity relative to CTR ceilings.
              </p>
              <ul className="space-y-1.5 text-[11px] font-mono text-slate-300 pt-2 border-t border-[#1E2734]">
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                  <span>Edge-gated against camouflage</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                  <span>12-D Shapley per-alert attribution</span>
                </li>
              </ul>
            </div>

            <div className="p-6 rounded-xl bg-[#0D121A] border border-[#1E2734] space-y-4">
              <div className="flex items-center gap-2.5 text-slate-100">
                <Zap className="w-4 h-4 text-emerald-400" />
                <h3 className="text-sm font-semibold">Inductive Conformal Calibration</h3>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed">
                Partitions alerts into rigorous prediction sets rather than arbitrary thresholds under nominal coverage error α.
              </p>
              <ul className="space-y-1.5 text-[11px] font-mono text-slate-300 pt-2 border-t border-[#1E2734]">
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                  <span>99.04% empirical coverage (1 - α = 0.99)</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                  <span>Missed-illicit risk bounded (FNR ≤ α = 1.00%)</span>
                </li>
              </ul>
            </div>

            <div className="p-6 rounded-xl bg-[#0D121A] border border-[#1E2734] space-y-4">
              <div className="flex items-center gap-2.5 text-slate-100">
                <Lock className="w-4 h-4 text-emerald-400" />
                <h3 className="text-sm font-semibold">Tamper-Evident Audit Chain</h3>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed">
                Every triage override, freeze, and PII unmasking is SHA-256 chained over RFC 8785 JSON and signed via Ed25519 checkpoints.
              </p>
              <ul className="space-y-1.5 text-[11px] font-mono text-slate-300 pt-2 border-t border-[#1E2734]">
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                  <span>Admissibility-ready (Evidence Act §§ 65A–65B &amp; 73A)</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                  <span>S3 Object Lock Compliance Mode</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* 5. Conformal Tiering & Interactive Calibration Widget */}
      <section id="tiering" className="py-16 border-b border-[#1E2734]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 space-y-10">
          <div className="max-w-2xl">
            <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">
              Conformal Triage
            </span>
            <h2 className="text-2xl sm:text-3xl font-semibold text-slate-100 tracking-tight">
              {t('conformal_title')}
            </h2>
            <p className="text-sm text-slate-400 mt-2">
              {t('conformal_desc')}
            </p>
          </div>

          <ConformalLivePreviewWidget />

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 rounded-xl bg-[#0D121A] border border-[#1E2734] space-y-3">
              <div className="flex items-center justify-between">
                <span className="px-2 py-0.5 rounded text-[11px] font-mono font-semibold bg-rose-500/10 text-rose-300 border border-rose-500/30">
                  Tier 1 Hold
                </span>
                <span className="text-[11px] font-mono text-slate-500">&lt; 200 µs</span>
              </div>
              <h3 className="text-sm font-semibold text-slate-100">Automated Settlement Freeze</h3>
              <p className="text-xs text-slate-400 leading-relaxed">{t('tier1_desc')}</p>
              <div className="text-[11px] font-mono text-slate-400 pt-2 border-t border-[#1E2734] space-y-1">
                <div>· Watchlist match &ge; 85% / structuring near ৳1M</div>
                <div>· High-velocity cyclic laundering topology</div>
              </div>
            </div>

            <div className="p-6 rounded-xl bg-[#0D121A] border border-[#1E2734] space-y-3">
              <div className="flex items-center justify-between">
                <span className="px-2 py-0.5 rounded text-[11px] font-mono font-semibold bg-amber-500/10 text-amber-300 border border-amber-500/30">
                  Tier 2 Review
                </span>
                <span className="text-[11px] font-mono text-slate-500">Queue</span>
              </div>
              <h3 className="text-sm font-semibold text-slate-100">Prioritized Analyst Triage</h3>
              <p className="text-xs text-slate-400 leading-relaxed">{t('tier2_desc')}</p>
              <div className="text-[11px] font-mono text-slate-400 pt-2 border-t border-[#1E2734] space-y-1">
                <div>· 12-Invariant SHAP Waterfall breakdown</div>
                <div>· Internal non-customer sensitivity calibration</div>
              </div>
            </div>

            <div className="p-6 rounded-xl bg-[#0D121A] border border-[#1E2734] space-y-3">
              <div className="flex items-center justify-between">
                <span className="px-2 py-0.5 rounded text-[11px] font-mono font-semibold bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">
                  Tier 3 Clear
                </span>
                <span className="text-[11px] font-mono text-slate-500">Zero Delay</span>
              </div>
              <h3 className="text-sm font-semibold text-slate-100">Autonomous Micro-Clearance</h3>
              <p className="text-xs text-slate-400 leading-relaxed">{t('tier3_desc')}</p>
              <div className="text-[11px] font-mono text-slate-400 pt-2 border-t border-[#1E2734] space-y-1">
                <div>· Empirical FNR: 0.76% (within α = 1.00% bound)</div>
                <div>· 84.2% false alarm volume bypassed cleanly</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 6. Security Posture & BFIU Regulatory Mandate Coverage */}
      <section id="security" className="py-16 border-b border-[#1E2734] bg-[#0B0F17]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6">
          <div className="flex flex-wrap items-end justify-between gap-4 mb-10">
            <div className="max-w-3xl">
              <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">
                OWASP ASVS Level 2 Aligned Architecture
              </span>
              <h2 className="text-2xl sm:text-3xl font-semibold text-slate-100 tracking-tight">
                {t('security_title')}
              </h2>
              <p className="text-xs sm:text-sm text-slate-400 mt-2">
                BFIU Master Circular 26 &amp; Circular 24 (TBML), Circular 32 (Sept 2026), Circular Letters 02 &amp; 03 (Feb 2026), Circular Letter 05 (Aug 2026), MLPA 2012 (§§ 6, 25), ATA 2009, and MLPR 2019.
              </p>
            </div>
            <Link href="/governance" className="text-xs font-mono text-emerald-400 hover:text-emerald-300">
              Inspect BFIU Mapping Matrix &rarr;
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="p-6 rounded-xl bg-[#0D121A] border border-[#1E2734] flex items-start gap-4">
              <Lock className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
              <div>
                <h3 className="text-sm font-semibold text-slate-100 mb-1">{t('security_point1')}</h3>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Blocks chain via SHA-256 over RFC 8785 canonical JSON with Ed25519 signatures. Admissibility-ready under Bangladesh Evidence Act, 1872 (Amended 2022) §§ 65A–65B &amp; 73A (Officer Certificate).
                </p>
              </div>
            </div>

            <div className="p-6 rounded-xl bg-[#0D121A] border border-[#1E2734] flex items-start gap-4">
              <Building2 className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
              <div>
                <h3 className="text-sm font-semibold text-slate-100 mb-1">{t('security_point2')}</h3>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Enforced server-side via JWT/OIDC RBAC: Analysts act as Makers; Supervisors and MLROs act as independent Checkers for freezes, whitelists, and SAR release.
                </p>
              </div>
            </div>

            <div className="p-6 rounded-xl bg-[#0D121A] border border-[#1E2734] flex items-start gap-4">
              <Shield className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
              <div>
                <h3 className="text-sm font-semibold text-slate-100 mb-1">{t('security_point3')}</h3>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Account numbers, NIDs, and entity names remain masked server-side until an officer logs a substantiated justification (rate-limited, 60s expiry).
                </p>
              </div>
            </div>

            <div className="p-6 rounded-xl bg-[#0D121A] border border-[#1E2734] flex items-start gap-4">
              <FileCheck2 className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
              <div>
                <h3 className="text-sm font-semibold text-slate-100 mb-1">{t('security_point4')}</h3>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Generates UNODC goAML v4.2 XML with mandatory attachment checksums and active anti-tipping-off phrase blocking under MLPA 2012 § 6.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 7. Institutional Deployment Options */}
      <section id="pricing" className="py-16 border-b border-[#1E2734]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6">
          <div className="max-w-2xl mb-10">
            <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">
              Deployment Topology
            </span>
            <h2 className="text-2xl sm:text-3xl font-semibold text-slate-100 tracking-tight">
              {t('pricing_title')}
            </h2>
            <p className="text-sm text-slate-400 mt-2">
              Run in an isolated evaluation sandbox, private bank VPC, or air-gapped national sovereign cloud.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 rounded-xl bg-[#0D121A] border border-[#1E2734] flex flex-col justify-between space-y-6">
              <div>
                <span className="text-[11px] font-mono text-slate-400 uppercase">Sandbox</span>
                <h3 className="text-lg font-semibold text-slate-100 mt-1 mb-2">{t('plan_starter')}</h3>
                <p className="text-xs text-slate-400 mb-5">
                  For bank model risk validation, algorithmic auditing, and compliance engineering proofs of concept.
                </p>
                <div className="text-2xl font-mono font-semibold text-slate-100 mb-5">
                  $0 <span className="text-xs font-normal text-slate-400">/ Evaluation</span>
                </div>
                <ul className="space-y-2 text-xs text-slate-300 font-mono">
                  <li className="flex items-center gap-2"><CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />Synthetic Bangladesh banking corpus</li>
                  <li className="flex items-center gap-2"><CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />Full 11-module compliance desk</li>
                  <li className="flex items-center gap-2"><CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />Single-command benchmark evals</li>
                </ul>
              </div>
              <Link
                href="/app"
                className="w-full py-2.5 rounded-md text-xs font-medium bg-[#141C27] hover:bg-[#1C2736] text-slate-200 text-center border border-[#253142] transition-colors block"
              >
                Open Sandbox Workspace
              </Link>
            </div>

            <div className="p-6 rounded-xl bg-[#0D121A] border border-emerald-500/40 flex flex-col justify-between space-y-6">
              <div>
                <span className="text-[11px] font-mono text-emerald-400 uppercase">Production Bank</span>
                <h3 className="text-lg font-semibold text-slate-100 mt-1 mb-2">{t('plan_bank')}</h3>
                <p className="text-xs text-slate-400 mb-5">
                  On-premises deployment for scheduled commercial banks, NBFIs, and mobile financial service operators.
                </p>
                <div className="text-2xl font-mono font-semibold text-emerald-400 mb-5">
                  Enterprise <span className="text-xs font-normal text-slate-400">/ Annual SLA</span>
                </div>
                <ul className="space-y-2 text-xs text-slate-300 font-mono">
                  <li className="flex items-center gap-2"><CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />Air-gapped Kubernetes &amp; Helm charts</li>
                  <li className="flex items-center gap-2"><CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />SWIFT MT700, ISO 20022 &amp; RTGS feeds</li>
                  <li className="flex items-center gap-2"><CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />Ed25519 checkpoints &amp; S3 Object Lock</li>
                </ul>
              </div>
              <button
                type="button"
                onClick={() => handleOpenInquiry('BANK_POC')}
                className="w-full py-2.5 rounded-md text-xs font-semibold bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-center transition-colors cursor-pointer"
              >
                Request Bank PoC &amp; Architecture Brief
              </button>
            </div>

            <div className="p-6 rounded-xl bg-[#0D121A] border border-[#1E2734] flex flex-col justify-between space-y-6">
              <div>
                <span className="text-[11px] font-mono text-slate-400 uppercase">Regulator / FIU</span>
                <h3 className="text-lg font-semibold text-slate-100 mt-1 mb-2">{t('plan_fiu')}</h3>
                <p className="text-xs text-slate-400 mb-5">
                  Cross-institution macro-prudential graph intelligence for Central Banks and Financial Intelligence Units.
                </p>
                <div className="text-2xl font-mono font-semibold text-slate-100 mb-5">
                  Sovereign <span className="text-xs font-normal text-slate-400">/ Mandate</span>
                </div>
                <ul className="space-y-2 text-xs text-slate-300 font-mono">
                  <li className="flex items-center gap-2"><CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />Multi-bank federated entity resolution</li>
                  <li className="flex items-center gap-2"><CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />Direct UNODC goAML v4.2 gateway</li>
                  <li className="flex items-center gap-2"><CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />Hardware Security Module (HSM) keys</li>
                </ul>
              </div>
              <button
                type="button"
                onClick={() => handleOpenInquiry('SOVEREIGN')}
                className="w-full py-2.5 rounded-md text-xs font-medium bg-[#141C27] hover:bg-[#1C2736] text-slate-200 text-center border border-[#253142] transition-colors cursor-pointer"
              >
                Schedule Sovereign Briefing
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* 8. Footer */}
      <footer className="py-10 bg-[#080C12] text-xs font-mono text-slate-400">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 space-y-6">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div className="flex items-center gap-2.5">
              <Shield className="w-4 h-4 text-emerald-400" />
              <span className="font-semibold text-slate-200">Intelligent-AML Platform v3.0</span>
              <span className="text-slate-600">|</span>
              <span className="text-slate-500">C-STGB v3.2 Engine</span>
            </div>

            <div className="flex flex-wrap items-center gap-6 text-[11px]">
              <button type="button" onClick={() => setIsPrivacyModalOpen(true)} className="hover:text-slate-200 cursor-pointer">
                Privacy Policy
              </button>
              <button type="button" onClick={() => setIsTermsModalOpen(true)} className="hover:text-slate-200 cursor-pointer">
                Terms of Service
              </button>
              <Link href="/governance" className="hover:text-slate-200">
                Model Card (SR 11-7)
              </Link>
              <Link href="/app" className="text-emerald-400 hover:text-emerald-300 font-semibold">
                Open Workspace &rarr;
              </Link>
            </div>
          </div>

          <div className="pt-5 border-t border-[#1E2734] text-[11px] text-slate-500 leading-relaxed">
            Research prototype. Not legal advice. Not a certified regulated product. Developed for institutional AML/CFT evaluation and academic verification under BFIU Master Circular 26 and Federal Reserve SR 11-7 governance practices.
          </div>
        </div>
      </footer>

      <InstitutionalInquiryModal
        isOpen={inquiryModalOpen}
        onClose={() => setInquiryModalOpen(false)}
        inquiryType={inquiryType}
      />

      {isPrivacyModalOpen && (
        <div role="dialog" aria-modal="true" aria-labelledby="privacy-dialog-title" className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="w-full max-w-2xl bg-[#0D121A] border border-[#253142] rounded-xl shadow-2xl p-6 relative text-slate-100 max-h-[80vh] overflow-y-auto">
            <button type="button" onClick={() => setIsPrivacyModalOpen(false)} className="absolute top-4 right-4 p-1 rounded-md hover:bg-[#192231] text-slate-400 hover:text-slate-200" aria-label="Close dialog">
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
          <div className="w-full max-w-2xl bg-[#0D121A] border border-[#253142] rounded-xl shadow-2xl p-6 relative text-slate-100 max-h-[80vh] overflow-y-auto">
            <button type="button" onClick={() => setIsTermsModalOpen(false)} className="absolute top-4 right-4 p-1 rounded-md hover:bg-[#192231] text-slate-400 hover:text-slate-200" aria-label="Close dialog">
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

      {!isCookieDismissed && (
        <div role="region" aria-label="Cookie consent banner" className="fixed bottom-4 left-4 right-4 sm:left-auto sm:right-6 sm:max-w-md z-40 p-4 rounded-xl bg-[#0D121A] border border-[#253142] shadow-2xl text-slate-200">
          <div className="flex items-start justify-between gap-3 mb-2">
            <span className="text-xs font-mono font-semibold text-slate-100 flex items-center gap-2">
              <Lock className="w-3.5 h-3.5 text-emerald-400" />
              Essential Session Cookies
            </span>
            <button type="button" onClick={handleAcknowledgeCookie} className="text-slate-400 hover:text-slate-200" aria-label="Dismiss cookie notice">
              <X className="w-4 h-4" />
            </button>
          </div>
          <p className="text-[11px] text-slate-400 leading-relaxed mb-3">
            Uses strictly necessary local session storage for role state and verification settings. No third-party tracking.
          </p>
          <div className="flex items-center justify-end gap-2 pt-2 border-t border-[#1E2734]">
            <button type="button" onClick={() => setIsPrivacyModalOpen(true)} className="px-2.5 py-1 rounded text-xs font-mono text-slate-300 hover:text-slate-100 cursor-pointer">
              Privacy Policy
            </button>
            <button type="button" onClick={handleAcknowledgeCookie} className="px-3 py-1 rounded text-xs font-semibold bg-emerald-500 hover:bg-emerald-400 text-slate-950 cursor-pointer">
              Acknowledge
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
