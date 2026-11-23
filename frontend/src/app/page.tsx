'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  ShieldAlert,
  ArrowRight,
  CheckCircle2,
  Lock,
  Layers,
  Zap,
  Activity,
  FileCheck2,
  FileSpreadsheet,
  Globe,
  Sliders,
  Scale,
  Building2,
  AlertTriangle,
  ExternalLink,
  ChevronRight,
  Database,
  Users,
  Terminal,
  Shield,
  X,
  Menu,
  Info
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { ConformalLivePreviewWidget } from '@/components/landing/ConformalLivePreviewWidget';
import { ProductVisualPreview } from '@/components/landing/ProductVisualPreview';
import { InstitutionalInquiryModal } from '@/components/landing/InstitutionalInquiryModal';

export default function EnterpriseLandingPage() {
  const { language, toggleLanguage, t } = useBankingStore();
  
  // Institutional Inquiry Modal State
  const [inquiryModalOpen, setInquiryModalOpen] = useState(false);
  const [inquiryType, setInquiryType] = useState<'EVALUATION' | 'BANK_POC' | 'SOVEREIGN'>('BANK_POC');
  
  // Regulatory Modal States
  const [isPrivacyModalOpen, setIsPrivacyModalOpen] = useState(false);
  const [isTermsModalOpen, setIsTermsModalOpen] = useState(false);
  
  // Mobile Nav Drawer
  const [isMobileNavOpen, setIsMobileNavOpen] = useState(false);

  // Cookie Notice State with Zero CLS on hydration
  const [isCookieDismissed, setIsCookieDismissed] = useState(true);

  useEffect(() => {
    // Read consent from localStorage on client mount without layout shift
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

  // Close mobile drawer on Escape key
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
    <div className="min-h-screen bg-[#070B12] text-slate-100 flex flex-col font-sans selection:bg-emerald-500/30 selection:text-emerald-200">
      {/* 1. Top Enterprise Navigation Bar (<= 56px height) */}
      <header className="sticky top-0 z-40 w-full h-14 border-b border-[#1E293B] bg-[#070B12]/95 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 h-full flex items-center justify-between gap-3">
          {/* Brand */}
          <Link href="/" className="flex items-center gap-2.5 group cursor-pointer shrink-0">
            <div className="w-7 h-7 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center">
              <div className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
            </div>
            <div>
              <span className="font-bold text-xs tracking-wider uppercase text-slate-100 flex items-center gap-1.5">
                Intelligent-AML
                <span className="text-[10px] px-1.5 py-0.2 rounded font-mono font-bold bg-[#1E293B] text-emerald-400 border border-emerald-500/30">
                  Platform v3.0
                </span>
              </span>
              <p className="text-[9px] font-mono text-slate-400 hidden sm:block">
                C-STGB v3.2 Engine
              </p>
            </div>
          </Link>

          {/* Desktop Nav Links (Promoted Model Card) */}
          <nav className="hidden lg:flex items-center gap-5 text-xs font-mono text-slate-300">
            <a href="#problem" className="hover:text-emerald-400 transition-colors">
              The Problem
            </a>
            <a href="#differentiators" className="hover:text-emerald-400 transition-colors">
              Differentiators
            </a>
            <a href="#tiering" className="hover:text-emerald-400 transition-colors">
              Conformal Tiering
            </a>
            <Link href="/governance" className="text-cyan-400 hover:text-cyan-300 font-bold transition-colors flex items-center gap-1">
              <span>Model Card</span>
              <span className="text-[9px] px-1 py-0.2 rounded bg-cyan-950/60 border border-cyan-800 text-cyan-300">SR 11-7</span>
            </Link>
            <a href="#security" className="hover:text-emerald-400 transition-colors">
              Security &amp; BFIU
            </a>
            <a href="#pricing" className="hover:text-emerald-400 transition-colors">
              Deployment Tiers
            </a>
          </nav>

          {/* Action CTAs */}
          <div className="flex items-center gap-2">
            {/* Language Switcher */}
            <button
              type="button"
              onClick={toggleLanguage}
              className="px-2 py-1 rounded text-xs font-mono font-bold bg-[#0F172A] hover:bg-[#1E293B] text-slate-200 border border-[#334155] transition-all cursor-pointer flex items-center gap-1"
              title="Toggle English / বাংলা"
            >
              <Globe className="w-3 h-3 text-cyan-400" />
              <span>{language === 'en' ? 'EN' : 'বাং'}</span>
            </button>

            {/* Request Demo Trigger */}
            <button
              type="button"
              onClick={() => handleOpenInquiry('EVALUATION')}
              className="hidden sm:inline-flex px-3 py-1.5 rounded-lg text-xs font-mono font-semibold bg-[#1E293B] hover:bg-[#334155] text-slate-200 border border-[#475569] transition-all cursor-pointer"
            >
              Request Briefing
            </button>

            {/* Launch App Main CTA */}
            <Link
              href="/app"
              className="px-3.5 py-1.5 rounded-lg text-xs font-mono font-bold bg-emerald-500 hover:bg-emerald-400 text-slate-950 transition-all shadow-md shadow-emerald-500/20 flex items-center gap-1.5 cursor-pointer"
            >
              <span>{language === 'en' ? 'Launch Banking OS' : 'ওএস চালু করুন'}</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>

            {/* Mobile Hamburger Toggle */}
            <button
              type="button"
              onClick={() => setIsMobileNavOpen(!isMobileNavOpen)}
              className="p-1.5 rounded-lg bg-[#0F172A] border border-[#334155] text-slate-400 hover:text-slate-200 lg:hidden cursor-pointer"
              aria-label="Toggle navigation menu"
              aria-expanded={isMobileNavOpen}
            >
              {isMobileNavOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation Drawer */}
        {isMobileNavOpen && (
          <div className="lg:hidden fixed inset-x-0 top-14 bg-[#0F172A] border-b border-[#334155] p-5 shadow-2xl space-y-4 animate-in slide-in-from-top-3 z-50">
            <nav className="flex flex-col space-y-3 font-mono text-sm">
              <a
                href="#problem"
                onClick={() => setIsMobileNavOpen(false)}
                className="text-slate-300 hover:text-emerald-400 py-1"
              >
                1. The Problem (False Positives)
              </a>
              <a
                href="#differentiators"
                onClick={() => setIsMobileNavOpen(false)}
                className="text-slate-300 hover:text-emerald-400 py-1"
              >
                2. Differentiators (12 Invariants)
              </a>
              <a
                href="#tiering"
                onClick={() => setIsMobileNavOpen(false)}
                className="text-slate-300 hover:text-emerald-400 py-1"
              >
                3. Conformal Tiering Pipeline
              </a>
              <Link
                href="/governance"
                onClick={() => setIsMobileNavOpen(false)}
                className="text-cyan-400 hover:text-cyan-300 font-bold py-1 flex items-center justify-between"
              >
                <span>4. Model Card (SR 11-7 / BFIU)</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-cyan-950 border border-cyan-800">Verified</span>
              </Link>
              <a
                href="#security"
                onClick={() => setIsMobileNavOpen(false)}
                className="text-slate-300 hover:text-emerald-400 py-1"
              >
                5. Security &amp; Bangladesh BFIU
              </a>
              <a
                href="#pricing"
                onClick={() => setIsMobileNavOpen(false)}
                className="text-slate-300 hover:text-emerald-400 py-1"
              >
                6. Commercial Licensure &amp; PoC
              </a>
            </nav>

            <div className="pt-3 border-t border-[#1E293B] flex flex-col gap-2">
              <button
                type="button"
                onClick={() => handleOpenInquiry('BANK_POC')}
                className="w-full py-2.5 rounded-lg text-xs font-mono font-bold bg-[#1E293B] hover:bg-[#334155] text-slate-200 border border-[#475569] text-center"
              >
                Request Bank PoC &amp; Brief
              </button>
              <Link
                href="/app"
                onClick={() => setIsMobileNavOpen(false)}
                className="w-full py-2.5 rounded-lg text-xs font-mono font-bold bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-center flex items-center justify-center gap-1.5"
              >
                <span>Launch Banking OS (/app)</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>
        )}
      </header>

      {/* 2. Hero Section */}
      <section className="relative pt-16 pb-20 overflow-hidden border-b border-[#1E293B]/60">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-emerald-950/20 via-transparent to-transparent pointer-events-none" />
        <div className="max-w-6xl mx-auto px-4 sm:px-6 relative z-10 text-center">
          {/* Eyebrow Badge */}
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-mono font-semibold bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 mb-6">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span>Platform v3.0 // C-STGB v3.2 Engine // BFIU 2026 Mandate Aligned</span>
          </div>

          {/* Main Headline */}
          <h1 className="text-3xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-slate-100 max-w-4xl mx-auto leading-tight sm:leading-none mb-6">
            {t('landing_headline')}
          </h1>

          {/* Subheadline */}
          <p className="text-base sm:text-lg text-slate-400 max-w-3xl mx-auto font-sans leading-relaxed mb-10">
            {t('landing_subheadline')}
          </p>

          {/* Dual Action CTAs */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-14">
            <Link
              href="/app"
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl text-sm font-mono font-bold bg-emerald-500 hover:bg-emerald-400 text-slate-950 transition-all shadow-lg shadow-emerald-500/25 flex items-center justify-center gap-2 cursor-pointer"
            >
              <span>Launch Banking Platform (/app)</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
            <button
              type="button"
              onClick={() => handleOpenInquiry('BANK_POC')}
              className="w-full sm:w-auto px-6 py-3.5 rounded-xl text-sm font-mono font-semibold bg-[#0F172A] hover:bg-[#1E293B] text-slate-200 border border-[#334155] transition-all flex items-center justify-center gap-2 cursor-pointer"
            >
              <span>Request Bank PoC &amp; Brief</span>
              <ExternalLink className="w-4 h-4 text-slate-400" />
            </button>
          </div>

          {/* 4 Verified Metric Scorecards */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-left mb-6">
            <div className="p-4 rounded-xl bg-[#0F172A]/80 border border-[#1E293B] shadow-xs">
              <span className="text-[11px] font-mono font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                Champion Macro F1
              </span>
              <span className="text-2xl font-bold font-mono text-emerald-400">94.5%</span>
              <p className="text-[10px] text-slate-400 mt-1 font-mono">
                C-STGB v3.2 (p &lt; 10⁻⁶ vs Baselines)
              </p>
            </div>

            <div className="p-4 rounded-xl bg-[#0F172A]/80 border border-[#1E293B] shadow-xs">
              <span className="text-[11px] font-mono font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                Noise Reduction
              </span>
              <span className="text-2xl font-bold font-mono text-emerald-400">84.2%</span>
              <p className="text-[10px] text-slate-400 mt-1 font-mono">
                7-Day Continuous Shadow Replay
              </p>
            </div>

            <div className="p-4 rounded-xl bg-[#0F172A]/80 border border-[#1E293B] shadow-xs">
              <span className="text-[11px] font-mono font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                Autonomous Clearance
              </span>
              <span className="text-2xl font-bold font-mono text-cyan-400">&lt; 200 µs</span>
              <p className="text-[10px] text-slate-400 mt-1 font-mono">
                P50 In-Memory FastPath Scorer
              </p>
            </div>

            <div className="p-4 rounded-xl bg-[#0F172A]/80 border border-[#1E293B] shadow-xs">
              <span className="text-[11px] font-mono font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                Conformal Coverage
              </span>
              <span className="text-2xl font-bold font-mono text-indigo-400">99.04%</span>
              <p className="text-[10px] text-slate-400 mt-1 font-mono">
                Nominal 1 - α = 99.00% Guarantee
              </p>
            </div>
          </div>

          {/* Rigorous Benchmark Footnote & Scope Reconciliation */}
          <div className="p-3.5 rounded-xl bg-[#0B0F17] border border-[#1E293B] text-[11px] font-mono text-slate-400 flex items-start gap-2.5 text-left">
            <Info className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
            <div>
              <strong className="text-slate-300">Empirical Benchmark Scope Reconciliation:</strong>
              <span className="ml-1">
                <strong>(1) 7-Day Bangladesh Synthetic Bank Replay:</strong> 94.5% Macro F1, 84.2% noise reduction, &lt; 200 µs P50 FastPath latency, 99.04% empirical coverage.
                <strong className="ml-2">(2) 14-Dataset Cross-Domain Research Corpus:</strong> 68.05% cross-domain Macro F1 (91.42% Elliptic-v1), 0.45 ms full-pipeline P50 (0.12 ms GNN forward pass), 99.33% offline conformal STP. Verified in{' '}
                <Link href="/governance" className="text-cyan-400 underline hover:text-cyan-300 font-bold">
                  SR 11-7 Model Card (/governance) &rarr;
                </Link>
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* 2.5 Product Visual Preview (New Phase 2 Item) */}
      <section className="py-14 border-b border-[#1E293B]/60 bg-[#070B12]">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="text-center max-w-3xl mx-auto mb-8">
            <span className="text-xs font-mono font-bold uppercase tracking-wider text-emerald-400 block mb-1">
              Production Architecture Showcase
            </span>
            <h2 className="text-2xl font-bold text-slate-100">
              Interactive 11-Module Banking OS Preview
            </h2>
            <p className="text-xs text-slate-400 mt-1 font-sans">
              Inspect the real-time Forensic Graph Studio and Virtualized Alert Triage Queue before entering the live workspace.
            </p>
          </div>
          <ProductVisualPreview />
        </div>
      </section>

      {/* 3. The Problem Section */}
      <section id="problem" className="py-20 border-b border-[#1E293B]/60 bg-[#0B0F17]/40">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="text-center max-w-3xl mx-auto mb-14">
            <h2 className="text-xs font-mono font-bold uppercase tracking-wider text-rose-400 mb-2">
              Legacy AML Infrastructure Failure
            </h2>
            <h3 className="text-2xl sm:text-3xl font-bold text-slate-100">
              Why 95%+ False Positives Cripple Banking Compliance
            </h3>
            <p className="text-sm text-slate-400 mt-3 font-sans">
              Traditional rule engines generate millions of benign alerts, drowning compliance teams while sophisticated smurfing, mule networks, and trade-based laundering go undetected.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="p-5 rounded-xl bg-[#0F172A] border border-rose-500/20">
              <div className="w-8 h-8 rounded-lg bg-rose-500/10 text-rose-400 flex items-center justify-center mb-3">
                <AlertTriangle className="w-4 h-4" />
              </div>
              <h4 className="text-sm font-bold text-slate-100 mb-1.5">
                95%+ False Alarm Deluge
              </h4>
              <p className="text-xs text-slate-400 leading-relaxed font-sans">
                Analysts spend 80% of their day rubber-stamping trivial salary transfers, leading to acute fatigue and missed high-risk typologies.
              </p>
            </div>

            <div className="p-5 rounded-xl bg-[#0F172A] border border-amber-500/20">
              <div className="w-8 h-8 rounded-lg bg-amber-500/10 text-amber-400 flex items-center justify-center mb-3">
                <Scale className="w-4 h-4" />
              </div>
              <h4 className="text-sm font-bold text-slate-100 mb-1.5">
                Opaque Black-Box Risk
              </h4>
              <p className="text-xs text-slate-400 leading-relaxed font-sans">
                Complex neural nets without formal validation fail Federal Reserve SR 11-7 and Bangladesh Bank audits due to lack of explainability.
              </p>
            </div>

            <div className="p-5 rounded-xl bg-[#0F172A] border border-cyan-500/20">
              <div className="w-8 h-8 rounded-lg bg-cyan-500/10 text-cyan-400 flex items-center justify-center mb-3">
                <FileSpreadsheet className="w-4 h-4" />
              </div>
              <h4 className="text-sm font-bold text-slate-100 mb-1.5">
                TBML Invisibility
              </h4>
              <p className="text-xs text-slate-400 leading-relaxed font-sans">
                Over-invoicing, fictitious goods, and LC structuring evade siloed transaction monitoring without trade-corridor price benchmarks.
              </p>
            </div>

            <div className="p-5 rounded-xl bg-[#0F172A] border border-emerald-500/20">
              <div className="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center mb-3">
                <FileCheck2 className="w-4 h-4" />
              </div>
              <h4 className="text-sm font-bold text-slate-100 mb-1.5">
                goAML Schema Rejection
              </h4>
              <p className="text-xs text-slate-400 leading-relaxed font-sans">
                Manual STR/SAR filing leads to validation errors, missing documentary attachments, and regulatory scrutiny from BFIU.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* 4. Differentiators Section */}
      <section id="differentiators" className="py-20 border-b border-[#1E293B]/60">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="text-center max-w-3xl mx-auto mb-14">
            <h2 className="text-xs font-mono font-bold uppercase tracking-wider text-emerald-400 mb-2">
              The Intelligent-AML Difference
            </h2>
            <h3 className="text-2xl sm:text-3xl font-bold text-slate-100">
              Mathematical Soundness Meets Sovereign Banking Control
            </h3>
            <p className="text-sm text-slate-400 mt-3 font-sans">
              Designed from first principles to give financial institutions provable statistical guarantees, sub-millisecond latencies, and air-gapped security.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] relative overflow-hidden">
              <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 flex items-center justify-center mb-4">
                <Layers className="w-5 h-5" />
              </div>
              <h4 className="text-base font-bold text-slate-100 mb-2">
                12 Spatio-Temporal Invariants
              </h4>
              <p className="text-xs text-slate-400 leading-relaxed font-sans mb-4">
                Rather than memorizing ephemeral patterns, C-STGB evaluates physical flow invariants: pass-through ratios, cycle participation, fan-in burst rates, and structuring bands.
              </p>
              <ul className="space-y-1.5 text-[11px] font-mono text-slate-300">
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                  <span>Robust against adversarial camouflage</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                  <span>Shapley feature attribution per alert</span>
                </li>
              </ul>
            </div>

            <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] relative overflow-hidden">
              <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 flex items-center justify-center mb-4">
                <Zap className="w-5 h-5" />
              </div>
              <h4 className="text-base font-bold text-slate-100 mb-2">
                Inductive Conformal Calibration
              </h4>
              <p className="text-xs text-slate-400 leading-relaxed font-sans mb-4">
                Guarantees finite-sample coverage at nominal error rate α. Alerts are classified into rigorous confidence bands, never heuristic probability guesses.
              </p>
              <ul className="space-y-1.5 text-[11px] font-mono text-slate-300">
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
                  <span>99.04% empirical coverage (1 - α = 0.99)</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
                  <span>Statistically bounded missed-illicit risk in Tier 3 clearance (FNR ≤ α = 1.00%)</span>
                </li>
              </ul>
            </div>

            <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] relative overflow-hidden">
              <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 flex items-center justify-center mb-4">
                <Lock className="w-5 h-5" />
              </div>
              <h4 className="text-base font-bold text-slate-100 mb-2">
                Tamper-Evident WORM Ledger
              </h4>
              <p className="text-xs text-slate-400 leading-relaxed font-sans mb-4">
                Every action, triage decision, and PII unmasking is hash-chained with RFC 8785 Canonical JSON and signed with RFC 8032 Ed25519 asymmetric cryptography.
              </p>
              <ul className="space-y-1.5 text-[11px] font-mono text-slate-300">
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
                  <span>Admissibility-ready under Bangladesh Evidence Act, 1872 (Amended 2022) §§ 65A–65B &amp; 73A</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
                  <span>Anchored to AWS S3 / MinIO Object Lock Compliance Mode</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* 5. Conformal Tiering Explainer & Live Preview Widget */}
      <section id="tiering" className="py-20 border-b border-[#1E293B]/60 bg-[#0B0F17]/40">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 space-y-12">
          <div className="text-center max-w-3xl mx-auto">
            <h2 className="text-xs font-mono font-bold uppercase tracking-wider text-cyan-400 mb-2">
              Operational Pipeline
            </h2>
            <h3 className="text-2xl sm:text-3xl font-bold text-slate-100">
              {t('conformal_title')}
            </h3>
            <p className="text-sm text-slate-400 mt-3 font-sans">
              {t('conformal_desc')}
            </p>
          </div>

          {/* Interactive Live Preview Component */}
          <ConformalLivePreviewWidget />

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Tier 1 */}
            <div className="p-6 rounded-2xl bg-[#0F172A] border-2 border-rose-500/40 relative">
              <div className="flex items-center justify-between mb-4">
                <span className="px-2.5 py-1 rounded text-xs font-mono font-bold bg-rose-500/20 text-rose-300 border border-rose-500/40">
                  Tier 1 Hold
                </span>
                <span className="text-[11px] font-mono text-rose-400">Interdict &lt; 200 µs</span>
              </div>
              <h4 className="text-base font-bold text-slate-100 mb-2">
                Automated Settlement Freeze
              </h4>
              <p className="text-xs text-slate-400 leading-relaxed font-sans mb-4">
                {t('tier1_desc')}
              </p>
              <div className="text-[11px] font-mono text-slate-300 p-3 rounded-lg bg-[#0B0F17] border border-[#1E293B]">
                <p className="text-rose-400 font-bold mb-1">Trigger Signals:</p>
                <p>• OFAC / UN Watchlist Hit (Score &ge; 85%)</p>
                <p>• Structuring ৳954,000 near CTR ceiling</p>
                <p>• High-velocity cyclic laundering graph</p>
              </div>
            </div>

            {/* Tier 2 */}
            <div className="p-6 rounded-2xl bg-[#0F172A] border-2 border-amber-500/40 relative">
              <div className="flex items-center justify-between mb-4">
                <span className="px-2.5 py-1 rounded text-xs font-mono font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40">
                  Tier 2 Review
                </span>
                <span className="text-[11px] font-mono text-amber-400">Bounded Risk Queue</span>
              </div>
              <h4 className="text-base font-bold text-slate-100 mb-2">
                Prioritized Analyst Triage
              </h4>
              <p className="text-xs text-slate-400 leading-relaxed font-sans mb-4">
                {t('tier2_desc')}
              </p>
              <div className="text-[11px] font-mono text-slate-300 p-3 rounded-lg bg-[#0B0F17] border border-[#1E293B]">
                <p className="text-amber-400 font-bold mb-1">Investigation Support:</p>
                <p>• 12-Invariant SHAP Waterfall attribution</p>
                <p>• Internal analyst sensitivity &amp; false-positive analysis (strictly non-customer-facing)</p>
                <p>• Maker-Checker sign-off workflow</p>
              </div>
            </div>

            {/* Tier 3 */}
            <div className="p-6 rounded-2xl bg-[#0F172A] border-2 border-emerald-500/40 relative">
              <div className="flex items-center justify-between mb-4">
                <span className="px-2.5 py-1 rounded text-xs font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                  Tier 3 Clear
                </span>
                <span className="text-[11px] font-mono text-emerald-400">Zero-Human Delay</span>
              </div>
              <h4 className="text-base font-bold text-slate-100 mb-2">
                Autonomous Micro-Clearance
              </h4>
              <p className="text-xs text-slate-400 leading-relaxed font-sans mb-4">
                {t('tier3_desc')}
              </p>
              <div className="text-[11px] font-mono text-slate-300 p-3 rounded-lg bg-[#0B0F17] border border-[#1E293B]">
                <p className="text-emerald-400 font-bold mb-1">Statistical Guarantee:</p>
                <p>• Empirical Missed-Illicit Rate (FNR): 0.76% (within α = 1.00% conformal bound)</p>
                <p>• 84.2% noise stripped before analyst queue</p>
                <p>• Decision hash stamped in audit ledger</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 6. Security Posture & BFIU Compliance */}
      <section id="security" className="py-20 border-b border-[#1E293B]/60">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="text-center max-w-3xl mx-auto mb-14">
            <span className="px-3 py-1 rounded-full text-xs font-mono font-bold bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 uppercase tracking-wider mb-3 inline-block">
              OWASP ASVS LEVEL 2 ALIGNED ARCHITECTURE
            </span>
            <h3 className="text-2xl sm:text-3xl font-bold text-slate-100 mt-2">
              {t('security_title')}
            </h3>
            <p className="text-sm text-slate-400 mt-3 font-sans">
              Tailored specifically for the Bangladesh regulatory regime: BFIU Master Circular 26 &amp; Circular 24 (TBML), Circular 32 (Sept 2026), Circular Letters 02 &amp; 03 (Feb 2026), Circular Letter 05 (Aug 2026), MLPA 2012 (§§ 6, 25), ATA 2009, and MLPR 2019.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] flex items-start gap-4">
              <div className="w-10 h-10 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center shrink-0">
                <Lock className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-sm font-bold text-slate-100 mb-1">
                  {t('security_point1')}
                </h4>
                <p className="text-xs text-slate-400 leading-relaxed font-sans">
                  Blocks are chained via SHA-256 over RFC 8785 canonical JSON and signed with Ed25519 private keys. Admissibility-ready under Bangladesh Evidence Act, 1872 (Amended 2022) §§ 65A–65B &amp; 73A with responsible officer certificate.
                </p>
              </div>
            </div>

            <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] flex items-start gap-4">
              <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center shrink-0">
                <Users className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-sm font-bold text-slate-100 mb-1">
                  {t('security_point2')}
                </h4>
                <p className="text-xs text-slate-400 leading-relaxed font-sans">
                  Enforced strictly on the server: Analysts (L1/L2) act as Makers; Supervisors and MLROs act as Checkers. Dual sign-off required for all case dockets.
                </p>
              </div>
            </div>

            <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] flex items-start gap-4">
              <div className="w-10 h-10 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center shrink-0">
                <Shield className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-sm font-bold text-slate-100 mb-1">
                  {t('security_point3')}
                </h4>
                <p className="text-xs text-slate-400 leading-relaxed font-sans">
                  Account numbers, NIDs, and names are masked server-side. Unmasking requires substantiated justification, rate-limited to 5/10min, with 60s expiration.
                </p>
              </div>
            </div>

            <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] flex items-start gap-4">
              <div className="w-10 h-10 rounded-xl bg-cyan-500/10 text-cyan-400 flex items-center justify-center shrink-0">
                <FileCheck2 className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-sm font-bold text-slate-100 mb-1">
                  {t('security_point4')}
                </h4>
                <p className="text-xs text-slate-400 leading-relaxed font-sans">
                  Automated generation of UNODC goAML v4.2 XML with mandatory supporting attachment validation and anti-tipping-off prohibitions under MLPA 2012 § 6.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 7. Pricing & Institutional Deployment Models */}
      <section id="pricing" className="py-20 border-b border-[#1E293B]/60 bg-[#0B0F17]/40">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="text-center max-w-3xl mx-auto mb-14">
            <h2 className="text-xs font-mono font-bold uppercase tracking-wider text-emerald-400 mb-2">
              Commercial Licensure
            </h2>
            <h3 className="text-2xl sm:text-3xl font-bold text-slate-100">
              {t('pricing_title')}
            </h3>
            <p className="text-sm text-slate-400 mt-3 font-sans">
              Deployable across sovereign cloud or completely isolated air-gapped data centers.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Tier A: Evaluation */}
            <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] flex flex-col justify-between">
              <div>
                <span className="text-xs font-mono text-slate-400 uppercase tracking-wider">Evaluation</span>
                <h4 className="text-lg font-bold text-slate-100 mt-1 mb-2">{t('plan_starter')}</h4>
                <p className="text-xs text-slate-400 mb-4 font-sans">
                  For internal model validation, ETH Zurich thesis review, and risk management proofs of concept.
                </p>
                <div className="text-2xl font-bold font-mono text-slate-100 mb-6">$0 <span className="text-xs font-normal text-slate-400">/ 30-Day PoC</span></div>
                <ul className="space-y-2 text-xs text-slate-300 font-mono mb-6">
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    <span>Synthetic Bangladesh banking dataset</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    <span>All 11 Compliance Modules</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    <span>Single-command eval reproduction</span>
                  </li>
                </ul>
              </div>
              <Link
                href="/app"
                className="w-full py-2.5 rounded-lg text-xs font-mono font-bold bg-[#1E293B] hover:bg-[#334155] text-slate-200 text-center border border-[#475569] transition-all cursor-pointer block"
              >
                Access Free Sandbox
              </Link>
            </div>

            {/* Tier B: Bank On-Premises (Most Popular) */}
            <div className="p-6 rounded-2xl bg-[#0F172A] border-2 border-emerald-500/50 flex flex-col justify-between relative shadow-lg shadow-emerald-950/20">
              <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-0.5 rounded-full text-[10px] font-mono font-bold bg-emerald-500 text-slate-950 uppercase tracking-wider">
                Most Popular
              </div>
              <div>
                <span className="text-xs font-mono text-emerald-400 uppercase tracking-wider">Production Bank</span>
                <h4 className="text-lg font-bold text-slate-100 mt-1 mb-2">{t('plan_bank')}</h4>
                <p className="text-xs text-slate-400 mb-4 font-sans">
                  Turnkey on-premises deployment for scheduled commercial banks and digital payment operators.
                </p>
                <div className="text-2xl font-bold font-mono text-emerald-400 mb-6">Custom <span className="text-xs font-normal text-slate-400">/ Annual SLA</span></div>
                <ul className="space-y-2 text-xs text-slate-300 font-mono mb-6">
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    <span>Air-gapped Kubernetes / Helm deployment</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    <span>Core banking &amp; SWIFT MT700 connectors</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    <span>Ed25519 WORM ledger &amp; Object-Lock</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    <span>24/7 Tier-1 Mission-Critical SLA</span>
                  </li>
                </ul>
              </div>
              <button
                type="button"
                onClick={() => handleOpenInquiry('BANK_POC')}
                className="w-full py-2.5 rounded-lg text-xs font-mono font-bold bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-center transition-all cursor-pointer shadow-md shadow-emerald-500/20"
              >
                Request Bank PoC &amp; Architecture Brief
              </button>
            </div>

            {/* Tier C: National FIU / Central Bank */}
            <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] flex flex-col justify-between">
              <div>
                <span className="text-xs font-mono text-slate-400 uppercase tracking-wider">Sovereign Authority</span>
                <h4 className="text-lg font-bold text-slate-100 mt-1 mb-2">{t('plan_fiu')}</h4>
                <p className="text-xs text-slate-400 mb-4 font-sans">
                  Multi-institution macro-prudential surveillance for Central Banks, FIUs, and Law Enforcement.
                </p>
                <div className="text-2xl font-bold font-mono text-slate-100 mb-6">Sovereign <span className="text-xs font-normal text-slate-400">/ Government Mandate</span></div>
                <ul className="space-y-2 text-xs text-slate-300 font-mono mb-6">
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    <span>Multi-tenant inter-bank flow graph</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    <span>UNODC goAML Central Gateway</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    <span>Hardware Security Module (HSM) keys</span>
                  </li>
                </ul>
              </div>
              <button
                type="button"
                onClick={() => handleOpenInquiry('SOVEREIGN')}
                className="w-full py-2.5 rounded-lg text-xs font-mono font-semibold bg-[#1E293B] hover:bg-[#334155] text-slate-200 text-center border border-[#475569] transition-all cursor-pointer"
              >
                Schedule Sovereign Briefing
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* 8. Footer */}
      <footer className="py-12 border-t border-[#1E293B] bg-[#070B12] text-xs font-mono text-slate-400">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6 mb-8">
            <div className="flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-full bg-emerald-400" />
              <span className="font-bold text-slate-200">Intelligent-AML Enterprise Banking Platform</span>
              <span className="text-[10px] text-slate-400">Platform v3.0 | C-STGB v3.2 Engine</span>
            </div>

            <div className="flex flex-wrap items-center gap-6 text-[11px]">
              <button
                type="button"
                onClick={() => setIsPrivacyModalOpen(true)}
                className="hover:text-slate-200 transition-colors cursor-pointer"
              >
                Privacy Policy (GDPR / BCA 1991)
              </button>
              <button
                type="button"
                onClick={() => setIsTermsModalOpen(true)}
                className="hover:text-slate-200 transition-colors cursor-pointer"
              >
                Terms of Service
              </button>
              <Link href="/governance" className="hover:text-slate-200 transition-colors">
                Model Card (SR 11-7)
              </Link>
              <Link href="/app" className="text-emerald-400 hover:text-emerald-300 font-bold transition-colors">
                Open Banking OS &rarr;
              </Link>
            </div>
          </div>

          <div className="pt-6 border-t border-[#1E293B]/60 text-[11px] text-slate-500 leading-relaxed text-center sm:text-left">
            <p className="font-bold text-slate-400 mb-1">
              &copy; 2026 Intelligent-AML Compliance Platform. All rights reserved.
            </p>
            <p>
              Notice: Research prototype. Not legal advice. Not a certified regulated product. C-STGB and Conformal Risk Control are developed for academic and institutional evaluation under BFIU Master Circular 26 and Federal Reserve SR 11-7 standards.
            </p>
          </div>
        </div>
      </footer>

      {/* 9. Institutional Inquiry Modal */}
      <InstitutionalInquiryModal
        isOpen={inquiryModalOpen}
        onClose={() => setInquiryModalOpen(false)}
        inquiryType={inquiryType}
      />

      {/* 10. Privacy Policy Modal */}
      {isPrivacyModalOpen && (
        <div
          role="dialog"
          aria-modal="true"
          aria-labelledby="privacy-dialog-title"
          className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4"
        >
          <div className="w-full max-w-2xl bg-[#0F172A] border border-[#334155] rounded-2xl shadow-2xl p-6 relative text-slate-100 max-h-[80vh] overflow-y-auto">
            <button
              type="button"
              onClick={() => setIsPrivacyModalOpen(false)}
              className="absolute top-4 right-4 p-1 rounded-lg hover:bg-[#1E293B] text-slate-400 hover:text-slate-200"
              aria-label="Close dialog"
            >
              <X className="w-5 h-5" />
            </button>

            <h3 id="privacy-dialog-title" className="text-lg font-bold text-slate-100 mb-2">
              Privacy Policy &amp; Sovereign Data Governance
            </h3>
            <p className="text-xs font-mono text-emerald-400 mb-4">
              Bangladesh Bank ICT Security Guidelines v3.0 &amp; Banking Companies Act 1991 § 46
            </p>

            <div className="space-y-4 text-xs text-slate-300 font-sans leading-relaxed">
              <p>
                <strong>1. Sovereign Data Residency:</strong> In on-premises deployment mode (<code>APP_MODE=onprem</code>), no transaction data, customer identifiers, or graph topology leaves the financial institution&apos;s physical intranet perimeter. All computation is strictly local.
              </p>
              <p>
                <strong>2. Client-Side Masking &amp; Audited PII Unmasking:</strong> Personally Identifiable Information (PII) including National IDs, account numbers, and legal names are masked server-side. Unmasking requires substantiated justification, is limited by sliding-window rate limiting, and permanently creates a cryptographically signed entry in the append-only ledger.
              </p>
              <p>
                <strong>3. EU GDPR Research Evaluation Safeguards:</strong> For academic evaluation (ETH Zurich), all demonstration datasets are synthetic, pseudonymized, and processed under GDPR Articles 6(1)(c), 9(2)(g), 32 (pseudonymization), and 89 (scientific research safeguards).
              </p>
            </div>
          </div>
        </div>
      )}

      {/* 11. Terms of Service Modal */}
      {isTermsModalOpen && (
        <div
          role="dialog"
          aria-modal="true"
          aria-labelledby="terms-dialog-title"
          className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4"
        >
          <div className="w-full max-w-2xl bg-[#0F172A] border border-[#334155] rounded-2xl shadow-2xl p-6 relative text-slate-100 max-h-[80vh] overflow-y-auto">
            <button
              type="button"
              onClick={() => setIsTermsModalOpen(false)}
              className="absolute top-4 right-4 p-1 rounded-lg hover:bg-[#1E293B] text-slate-400 hover:text-slate-200"
              aria-label="Close dialog"
            >
              <X className="w-5 h-5" />
            </button>

            <h3 id="terms-dialog-title" className="text-lg font-bold text-slate-100 mb-2">
              Terms of Institutional Evaluation
            </h3>
            <p className="text-xs font-mono text-emerald-400 mb-4">
              Commercial Evaluation License &amp; Research Prototype Agreement
            </p>

            <div className="space-y-4 text-xs text-slate-300 font-sans leading-relaxed">
              <p>
                <strong>1. Evaluation Scope:</strong> This software is an advanced research and commercial evaluation prototype. It is provided for authorized institutional testing, algorithmic auditing, and regulatory review under the Money Laundering Prevention Act, 2012.
              </p>
              <p>
                <strong>2. Dual Maker-Checker Obligation:</strong> The software enforces algorithmic dual control. No case or regulatory export should be treated as finalized without review by a qualified Chief Compliance Officer (CCO) or authorized CAMLCO.
              </p>
              <p>
                <strong>3. No Legal or Fiduciary Advice:</strong> Use of this software does not constitute formal legal counsel or statutory certification. Compliance officers must independently verify filings against current BFIU circulars and applicable banking law.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* 12. Fixed Cookie Consent Banner with zero CLS */}
      {!isCookieDismissed && (
        <div
          role="region"
          aria-label="Cookie consent banner"
          className="fixed bottom-4 left-4 right-4 sm:left-auto sm:right-6 sm:max-w-md z-40 p-4 rounded-xl bg-[#0F172A] border border-[#334155] shadow-2xl animate-in slide-in-from-bottom-5 text-slate-200"
        >
          <div className="flex items-start justify-between gap-3 mb-2">
            <div className="flex items-center gap-2">
              <Lock className="w-4 h-4 text-emerald-400" />
              <span className="text-xs font-bold font-mono text-slate-100">Essential Banking Cookies</span>
            </div>
            <button
              type="button"
              onClick={handleAcknowledgeCookie}
              className="text-slate-400 hover:text-slate-200"
              aria-label="Dismiss cookie notice"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
          <p className="text-[11px] text-slate-400 font-sans leading-relaxed mb-3">
            We use only strictly necessary local session cookies to maintain your authenticated role and cryptographic WORM verification keys. Zero ad tracking or third-party telemetry.
          </p>
          <div className="flex items-center justify-end gap-2 pt-1 border-t border-[#1E293B]">
            <button
              type="button"
              onClick={() => setIsPrivacyModalOpen(true)}
              className="px-2.5 py-1.5 rounded-lg text-xs font-mono text-slate-300 hover:text-slate-100 hover:bg-[#1E293B] transition-colors cursor-pointer"
            >
              Security &amp; Cookie Policy
            </button>
            <button
              type="button"
              onClick={handleAcknowledgeCookie}
              className="px-3 py-1.5 rounded-lg text-xs font-mono font-bold bg-emerald-500 hover:bg-emerald-400 text-slate-950 transition-all cursor-pointer shadow-sm shadow-emerald-500/20"
            >
              Acknowledge &amp; Continue
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
