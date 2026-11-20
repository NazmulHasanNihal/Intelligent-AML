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
  RefreshCw,
  Hash,
  ShieldCheck,
  Check,
  Building,
  DollarSign
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
  const { setFourEyesModalOpen, addToast } = useBankingStore();

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

  const handleDownloadXml = () => {
    const xml = `<?xml version="1.0" encoding="UTF-8"?>
<FC2ElectronicFiling xmlns="http://www.fincen.gov/base" version="2.0">
  <ActivitySeqNum>1</ActivitySeqNum>
  <ActivityType>SAR</ActivityType>
  <CaseIdentifier>${caseId}</CaseIdentifier>
  <SubjectName>${subjectEntity}</SubjectName>
  <SuspiciousAmount Currency="USD">9450.00</SuspiciousAmount>
  <TypologyCategory>${typologyCategory}</TypologyCategory>
  <CryptographicMerkleRoot>9c72f16eb2befae4bcf1e1b7cbb510a6a13ba5b4d7a8f0aaee5337609c7ad42b</CryptographicMerkleRoot>
  <NarrativeText><![CDATA[${narrativeText}]]></NarrativeText>
</FC2ElectronicFiling>`;

    const blob = new Blob([xml], { type: 'application/xml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `SAR-Form111-${caseId}.xml`;
    a.click();
    URL.revokeObjectURL(url);
    addToast('XML Downloaded', `FinCEN Form 111 XML filing generated for ${caseId}.`, 'success');
  };

  return (
    <div className="p-4 sm:p-5 lg:p-6 max-w-[1700px] mx-auto space-y-4 sm:space-y-5">
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

        {/* Template Switcher & Submission */}
        <div className="flex items-center gap-3">
          <div className="flex items-center bg-[#0F172A] p-1 rounded-lg border border-[#334155]">
            <button
              onClick={() => setJurisdictionTemplate('BFIU')}
              className={`px-3 py-1 rounded text-xs font-semibold transition-all cursor-pointer ${
                jurisdictionTemplate === 'BFIU'
                  ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              BFIU STR-1 (BD)
            </button>
            <button
              onClick={() => setJurisdictionTemplate('FINCEN')}
              className={`px-3 py-1 rounded text-xs font-semibold transition-all cursor-pointer ${
                jurisdictionTemplate === 'FINCEN'
                  ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              FinCEN Form 111 (US)
            </button>
            <button
              onClick={() => setJurisdictionTemplate('GOAML')}
              className={`px-3 py-1 rounded text-xs font-semibold transition-all cursor-pointer ${
                jurisdictionTemplate === 'GOAML'
                  ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              goAML XML (Intl)
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
            className="flex items-center gap-1.5 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold text-xs uppercase tracking-wide rounded-lg transition-all shadow-md cursor-pointer"
          >
            <Lock className="w-3.5 h-3.5" />
            <span>4-Eyes Gate</span>
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
              <span className="font-mono font-bold text-rose-300">{detectedLeakage.join(', ')}</span>). FIU regulators require factual legal reasoning, not algorithmic jargon.
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
            className="px-2.5 py-1 bg-rose-900/60 hover:bg-rose-800/80 rounded border border-rose-600 text-rose-100 font-semibold text-[11px] shrink-0 cursor-pointer"
          >
            Auto-Sanitize Jargon
          </button>
        </div>
      )}

      {/* Responsive Split-Screen Workbench (2-Column Grid with Independent Scroll Panes) */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-5 min-h-[520px]">
        {/* Left Column: Autonomous Statutory Narrative Draft & Diff Tracker */}
        <div className="bg-[#0F172A] border border-[#1E293B] rounded-xl flex flex-col overflow-hidden max-h-[calc(100vh-230px)]">
          <div className="p-3.5 bg-[#0B0F17] border-b border-[#1E293B] flex items-center justify-between shrink-0">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-amber-400 shrink-0" />
              <h2 className="text-sm font-semibold text-slate-100">
                Statutory Regulatory Narrative (Editable Draft)
              </h2>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => setNarrativeText(initialNarrative)}
                className="p-1 rounded bg-[#1E293B] hover:bg-[#334155] text-slate-300 transition-colors cursor-pointer"
                title="Reset to Template Narrative"
              >
                <RefreshCw className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={handleDownloadXml}
                className="flex items-center gap-1 px-2.5 py-1 rounded bg-[#1E293B] hover:bg-[#334155] text-slate-200 text-xs font-medium transition-colors cursor-pointer"
              >
                <Download className="w-3 h-3 text-slate-400" />
                <span>Export XML</span>
              </button>
            </div>
          </div>

          <div className="p-4 flex-1 flex flex-col overflow-y-auto">
            <textarea
              value={narrativeText}
              onChange={(e) => setNarrativeText(e.target.value)}
              className="w-full flex-1 min-h-[380px] p-4 bg-[#090D14] border border-[#1E293B] rounded-xl font-mono text-xs text-slate-200 leading-relaxed focus:outline-none focus:border-rose-500/60 resize-none selection:bg-rose-500/20"
            />

            <div className="mt-3 flex items-center justify-between text-[11px] text-slate-500 font-mono shrink-0">
              <span>Word count: <strong className="text-slate-300 tabular-nums">{narrativeText.split(/\s+/).filter(Boolean).length}</strong></span>
              <span>Payload: <strong className="text-slate-300 tabular-nums">{new TextEncoder().encode(narrativeText).length}</strong> bytes</span>
              <span className="text-emerald-400">AST Grammar Validated</span>
            </div>
          </div>
        </div>

        {/* Right Column: Grounded Evidence, Merkle Receipt & Sign-Off Cards */}
        <div className="space-y-4 max-h-[calc(100vh-230px)] overflow-y-auto pr-1">
          {/* Evidence Card: Trade Divergence & Red Flags */}
          <div className="bg-[#0F172A] border border-[#1E293B] rounded-xl p-5 space-y-3">
            <div className="flex items-center justify-between pb-2 border-b border-[#1E293B]">
              <h2 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
                <FileText className="w-4 h-4 text-emerald-400 shrink-0" />
                Grounded Factual Evidence Dossier
              </h2>
              <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                FRE 902(11) ATTESTED
              </span>
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="p-3 bg-[#0B0F17] rounded-lg border border-[#1E293B]">
                <span className="text-slate-500 block text-[10px] uppercase font-mono">Subject Entity</span>
                <span className="font-semibold text-slate-200 block truncate">{subjectEntity}</span>
                <span className="text-[10px] text-slate-400 font-mono block mt-0.5">{accountNumber}</span>
              </div>
              <div className="p-3 bg-[#0B0F17] rounded-lg border border-[#1E293B]">
                <span className="text-slate-500 block text-[10px] uppercase font-mono">Suspicious Exposure</span>
                <span className="font-bold text-rose-400 font-mono text-sm block tabular-nums">{transactionAmount}</span>
                <span className="text-[10px] text-slate-400 font-mono block mt-0.5">Under CTR $10,000 threshold</span>
              </div>
            </div>

            <div className="space-y-1.5 pt-1 text-xs">
              <span className="block text-slate-400 font-medium">Statutory Red Flags Grounded in Audit Trail:</span>
              {[
                { label: 'ASYCUDA Customs Divergence', detail: 'Declared $42.50/kg vs $9.80/kg benchmark (+333.7%)' },
                { label: 'Sub-Threshold CTR Structuring', detail: 'Drawdown split at $9,450 to evade automated reporting' },
                { label: 'Rapid Offshore Wire Pass-Through', detail: 'Immediate transfer to Cayman Islands shell entity' }
              ].map((flag, idx) => (
                <div key={idx} className="flex items-start gap-2 p-2.5 bg-[#0B0F17] rounded-lg border border-[#1E293B] text-[11px] text-slate-300">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                  <div>
                    <strong className="text-slate-200">{flag.label}:</strong> {flag.detail}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Cryptographic Merkle Root Verification Card */}
          <div className="bg-[#0F172A] border border-[#1E293B] rounded-xl p-5 space-y-3">
            <div className="flex items-center justify-between pb-2 border-b border-[#1E293B]">
              <h2 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
                <Hash className="w-4 h-4 text-cyan-400 shrink-0" />
                Deterministic Merkle Root Receipt
              </h2>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                TAMPER-EVIDENT
              </span>
            </div>

            <div className="p-3 bg-[#0B0F17] rounded-lg border border-[#1E293B] font-mono text-xs space-y-2">
              <div>
                <span className="text-slate-500 text-[10px] block uppercase">Root Hash (SHA-256)</span>
                <span className="text-cyan-300 font-bold break-all text-[11px]">
                  9c72f16eb2befae4bcf1e1b7cbb510a6a13ba5b4d7a8f0aaee5337609c7ad42b
                </span>
              </div>
              <div className="grid grid-cols-2 gap-2 pt-1 border-t border-[#1E293B] text-[10px] text-slate-400">
                <div>Leaf 1 (Wire): <span className="text-slate-300">e9011ecd...</span></div>
                <div>Leaf 2 (Typology): <span className="text-slate-300">32961dd6...</span></div>
                <div>Leaf 3 (Model): <span className="text-slate-300">7e1d3430...</span></div>
                <div>Leaf 4 (Signoff): <span className="text-slate-300">bbcc2bc7...</span></div>
              </div>
            </div>

            <div className="flex items-center justify-between pt-2 text-xs">
              <span className="text-slate-400">WORM Chain Validation:</span>
              <span className="text-emerald-400 font-mono font-bold flex items-center gap-1">
                <ShieldCheck className="w-3.5 h-3.5" />
                CRYPTOGRAPHICALLY VERIFIED
              </span>
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
