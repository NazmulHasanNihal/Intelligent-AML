'use client';

import React, { useState, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import {
  FileCheck2,
  FileText,
  Download,
  AlertTriangle,
  CheckCircle2,
  Lock,
  Layers,
  Globe,
  Code,
  ShieldAlert,
  Sparkles,
  RefreshCw
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { PiiText } from '@/components/ui/PiiText';

const ALGO_LEAKAGE_TERMS = [
  'GCN',
  'GNN',
  'neural network',
  'SHAP',
  'Hawkes intensity',
  'lambda_u',
  'embedding',
  'conformal set',
  'algorithm',
  'C-STGB',
  'machine learning model'
];

function SarWorkbenchContent() {
  const searchParams = useSearchParams();
  const caseId = searchParams?.get('caseId') || 'CASE-2026-0881';
  const { setFourEyesModalOpen } = useBankingStore();

  const [jurisdictionTemplate, setJurisdictionTemplate] = useState<'BFIU' | 'FINCEN' | 'GOAML'>('BFIU');
  
  // Structured Form Fields
  const [subjectEntity, setSubjectEntity] = useState('Meghna Industrial & Agro Processing Ltd');
  const [accountNumber, setAccountNumber] = useState('BD22-EBLB-4829-1092-8823');
  const [transactionAmount, setTransactionAmount] = useState('9,450.00 USD (৳1,134,000 BDT)');
  const [typologyCategory, setTypologyCategory] = useState('TBML Over-Invoicing & Near-CTR Structuring');

  // Narrative State
  const initialNarrative = `CONFIDENTIAL SUSPICIOUS TRANSACTION REPORT (STR)
SUBMITTED PURSUANT TO SECTION 25, MONEY LAUNDERING PREVENTION ACT 2012 (ACT NO. 5 OF 2012)
TO: BANGLADESH FINANCIAL INTELLIGENCE UNIT (BFIU), BANGLADESH BANK

1. REPORTING INSTITUTION & SUBJECT IDENTIFICATION:
Reporting Institution: Eastern Bank PLC (EBL), Motijheel Head Office, Dhaka (BIC: EBLBBDDH).
Subject Account: Meghna Industrial & Agro Processing Ltd (Account No: BD22-EBLB-4829-1092-8823).
Counterparty: Gulf Star Commodities FZE, JAFZA Free Zone, Dubai, UAE (BIC: EBILAEAD).

2. FACTUAL BASIS FOR SUSPICIOUS TRANSACTION DETERMINATION:
Between August 28, 2026 and September 02, 2026, the Subject initiated documentary credit transactions under Letter of Credit (LC) No. LC-2026-CTG-88912. The declared invoice price for raw cotton imports was $42.50/kg. Verification against National Board of Revenue (NBR) ASYCUDA customs valuation databases indicated a prevailing market benchmark of $9.80/kg, representing a gross price divergence of +333.7%.

Furthermore, individual drawdown transfers were structured beneath the mandatory Cash Transaction Reporting (CTR) threshold of ৳1,000,000 BDT ($10,000 USD), specifically executed at $9,450.00 USD. The funds were immediately wired onward from the Dubai counterparty to an offshore jurisdiction in the Cayman Islands with no verifiable economic substance.

3. REMEDIAL ACTION TAKEN:
The Subject account has been placed on Tier 1 institutional hold pending formal regulatory direction under Section 2(v) of the Money Laundering Prevention Act 2012.`;

  const [narrativeText, setNarrativeText] = useState(initialNarrative);

  // Check for ML jargon leakage
  const detectedLeakage = ALGO_LEAKAGE_TERMS.filter((term) =>
    new RegExp(`\\b${term}\\b`, 'i').test(narrativeText)
  );

  return (
    <div className="p-6 max-w-[1700px] mx-auto space-y-5">
      {/* Header and Controls */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <FileCheck2 className="w-5 h-5 text-rose-500" />
            Autonomous SAR Filings Workbench
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Autonomous multi-jurisdiction regulatory narrative drafting with algorithm leakage protection and 4-Eyes cryptographic sign-off.
          </p>
        </div>

        {/* Template Switcher */}
        <div className="flex items-center gap-3">
          <div className="flex items-center bg-[#0F172A] p-1 rounded-lg border border-[#334155]">
            <button
              onClick={() => setJurisdictionTemplate('BFIU')}
              className={`px-3 py-1 rounded text-xs font-semibold transition-all ${
                jurisdictionTemplate === 'BFIU'
                  ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              BFIU STR-1 / STR-2 (BD)
            </button>
            <button
              onClick={() => setJurisdictionTemplate('FINCEN')}
              className={`px-3 py-1 rounded text-xs font-semibold transition-all ${
                jurisdictionTemplate === 'FINCEN'
                  ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              FinCEN Form 111 (US)
            </button>
            <button
              onClick={() => setJurisdictionTemplate('GOAML')}
              className={`px-3 py-1 rounded text-xs font-semibold transition-all ${
                jurisdictionTemplate === 'GOAML'
                  ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              UN goAML XML (Intl)
            </button>
          </div>

          <button
            onClick={() => {
              setFourEyesModalOpen(true, {
                actionType: 'SAR_FILING',
                actionTitle: `Submit SAR to 4-Eyes Sign-Off Gate (${caseId})`,
                targetId: caseId,
                details: `Submit drafted regulatory ${jurisdictionTemplate} filing for Subject: ${subjectEntity}`
              });
            }}
            className="flex items-center gap-1.5 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold text-xs uppercase tracking-wide rounded-lg transition-all shadow-md"
          >
            <Lock className="w-3.5 h-3.5" />
            <span>Submit to 4-Eyes Gate</span>
          </button>
        </div>
      </div>

      {/* Algorithm Leakage Warning Banner */}
      {detectedLeakage.length > 0 && (
        <div className="p-3 bg-rose-950/40 border border-rose-700/60 rounded-xl flex items-center justify-between text-xs text-rose-200">
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-rose-500 shrink-0" />
            <span>
              <strong>Regulatory Notice: Algorithm Leakage Detected!</strong> The narrative references internal ML terms: (
              <span className="font-mono font-bold text-rose-300">{detectedLeakage.join(', ')}</span>). FIU regulators require factual legal reasoning, not proprietary algorithmic jargon.
            </span>
          </div>
          <button
            onClick={() => {
              let sanitized = narrativeText;
              detectedLeakage.forEach((term) => {
                sanitized = sanitized.replace(new RegExp(`\\b${term}\\b`, 'gi'), 'institutional compliance review criteria');
              });
              setNarrativeText(sanitized);
            }}
            className="px-2.5 py-1 bg-rose-900/60 hover:bg-rose-800/80 rounded border border-rose-600 text-rose-100 font-semibold text-[11px] shrink-0"
          >
            Auto-Sanitize Jargon
          </button>
        </div>
      )}

      {/* Split-Screen Workbench */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Structured Statutory Fields (5 Cols) */}
        <div className="lg:col-span-5 bg-[#0F172A] border border-[#1E293B] rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-[#1E293B]">
            <h2 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
              <FileText className="w-4 h-4 text-slate-400" />
              Statutory Reporting Fields
            </h2>
            <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
              {jurisdictionTemplate} PRESET
            </span>
          </div>

          <div className="space-y-3 text-xs">
            <div>
              <label className="block text-slate-400 mb-1 font-medium">Subject Legal Entity</label>
              <input
                type="text"
                value={subjectEntity}
                onChange={(e) => setSubjectEntity(e.target.value)}
                className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-100 focus:outline-none focus:border-rose-500 font-medium"
              />
            </div>

            <div>
              <label className="block text-slate-400 mb-1 font-medium">Account Identifier</label>
              <input
                type="text"
                value={accountNumber}
                onChange={(e) => setAccountNumber(e.target.value)}
                className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-100 focus:outline-none focus:border-rose-500 font-mono text-xs"
              />
            </div>

            <div>
              <label className="block text-slate-400 mb-1 font-medium">Total Suspicious Exposure</label>
              <input
                type="text"
                value={transactionAmount}
                onChange={(e) => setTransactionAmount(e.target.value)}
                className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-100 focus:outline-none focus:border-rose-500 font-mono text-xs"
              />
            </div>

            <div>
              <label className="block text-slate-400 mb-1 font-medium">Typology / Suspicion Category</label>
              <input
                type="text"
                value={typologyCategory}
                onChange={(e) => setTypologyCategory(e.target.value)}
                className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-100 focus:outline-none focus:border-rose-500"
              />
            </div>

            <div className="pt-2">
              <span className="block text-slate-400 mb-1.5 font-medium">Statutory Red Flags Identified:</span>
              <div className="space-y-1.5">
                {[
                  'Documentary credit price divergence > 300% (ASYCUDA benchmark)',
                  'Sub-threshold near-CTR structuring (< $10,000 / ৳1,000,000)',
                  'Immediate pass-through fund transfers to offshore secrecy haven'
                ].map((flag, idx) => (
                  <div key={idx} className="flex items-center gap-2 p-2 bg-[#0B0F17] rounded border border-[#1E293B] text-[11px] text-slate-300">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                    <span>{flag}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Right: Autonomous GenAI Narrative Draft Editor (7 Cols) */}
        <div className="lg:col-span-7 bg-[#0F172A] border border-[#1E293B] rounded-xl flex flex-col overflow-hidden">
          <div className="p-3.5 bg-[#0B0F17] border-b border-[#1E293B] flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-amber-400" />
              <h2 className="text-sm font-semibold text-slate-100">
                Autonomous GenAI Narrative Draft
              </h2>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => setNarrativeText(initialNarrative)}
                className="p-1 rounded bg-[#1E293B] hover:bg-[#334155] text-slate-300 transition-colors"
                title="Regenerate Narrative"
              >
                <RefreshCw className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => alert('Downloading official signed regulatory PDF...')}
                className="flex items-center gap-1 px-2.5 py-1 rounded bg-[#1E293B] hover:bg-[#334155] text-slate-200 text-xs font-medium transition-colors"
              >
                <Download className="w-3 h-3 text-slate-400" />
                <span>Download PDF</span>
              </button>
            </div>
          </div>

          <div className="p-4 flex-1 flex flex-col">
            <textarea
              value={narrativeText}
              onChange={(e) => setNarrativeText(e.target.value)}
              className="w-full flex-1 min-h-[460px] p-4 bg-[#090D14] border border-[#1E293B] rounded-xl font-mono text-xs text-slate-200 leading-relaxed focus:outline-none focus:border-rose-500/60 resize-none selection:bg-rose-500/20"
            />

            <div className="mt-3 flex items-center justify-between text-[11px] text-slate-500">
              <span>Word count: {narrativeText.split(/\s+/).length} words</span>
              <span>Audit Hash: {narrativeText.length} bytes (WORM-tracked)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function SarWorkbenchPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center text-xs font-mono text-slate-400">Loading SAR Workbench...</div>}>
      <SarWorkbenchContent />
    </Suspense>
  );
}
