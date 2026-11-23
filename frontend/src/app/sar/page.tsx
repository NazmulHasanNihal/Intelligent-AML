'use client';

import React, { useState, Suspense, useMemo } from 'react';
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
  DollarSign,
  Printer,
  Copy,
  Table,
  FileSpreadsheet
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { PiiText } from '@/components/ui/PiiText';
import { computeSha256 } from '@/lib/audit/hashChain';
import { formatCurrencyByJurisdiction } from '@/lib/compliance/jurisdictions';

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
  const { jurisdiction, ctrRecords, setFourEyesModalOpen, addToast, addAuditEntry } = useBankingStore();

  const [activeSubTab, setActiveSubTab] = useState<'SAR_STUDIO' | 'CTR_AGGREGATOR'>('SAR_STUDIO');
  const [jurisdictionTemplate, setJurisdictionTemplate] = useState<'BFIU' | 'FINCEN' | 'GOAML'>(
    jurisdiction === 'BD_BFIU' ? 'BFIU' : jurisdiction === 'US_FINCEN' ? 'FINCEN' : 'GOAML'
  );

  // Structured Form Fields
  const [subjectEntity, setSubjectEntity] = useState('Meghna Industrial & Agro Processing Ltd');
  const [accountNumber, setAccountNumber] = useState('BD22-EBLB-4829-1092-8823');
  const [transactionAmount, setTransactionAmount] = useState('945,000.00 USD (৳113,400,000 BDT)');
  const [typologyCategory, setTypologyCategory] = useState('Trade-Based Money Laundering (TBML) Over-Invoicing & Near-CTR Structuring');

  // Narrative State
  const initialNarrative = `CONFIDENTIAL SUSPICIOUS TRANSACTION REPORT (STR / SAR)
SUBMITTED PURSUANT TO SECTION 25, MONEY LAUNDERING PREVENTION ACT 2012 (ACT NO. 5 OF 2012)
TO: BANGLADESH FINANCIAL INTELLIGENCE UNIT (BFIU), BANGLADESH BANK

1. REPORTING INSTITUTION & SUBJECT IDENTIFICATION:
Reporting Institution: Eastern Bank PLC (EBL), Motijheel Head Office, Dhaka (BIC: EBLBBDDH).
Subject Account: Meghna Industrial & Agro Processing Ltd (Account No: BD22-EBLB-4829-1092-8823).
Counterparty: Gulf Star Commodities FZE, JAFZA Free Zone, Dubai, UAE (BIC: EBILAEAD).

2. FACTUAL BASIS FOR SUSPICIOUS TRANSACTION DETERMINATION:
Between August 28, 2026 and September 02, 2026, the Subject initiated documentary credit transactions under Letter of Credit (LC) No. LC-CTG-2026-9921. The declared commercial invoice price for combed cotton yarn was $9.45/kg. Verification against National Board of Revenue (NBR) ASYCUDA World customs valuation databases indicated a prevailing market benchmark of $2.18/kg, representing a gross price divergence of +333.7%.

Furthermore, individual multi-agent transfers were structured beneath the mandatory Cash Transaction Reporting (CTR) threshold of ৳1,000,000 BDT, specifically executed at ৳954,000 BDT ($7,950.00 USD). AIS satellite vessel telemetry confirmed anomalous transshipment where the carrying vessel bypassed the declared Port Klang and discharged cargo directly at Jebel Ali / Dubai without re-export documentation.

3. REMEDIAL ACTION TAKEN:
The Subject account has been placed on Tier 1 administrative hold pending formal regulatory direction under Section 2(v) and Section 25 of the Money Laundering Prevention Act 2012.`;

  const [narrativeText, setNarrativeText] = useState(initialNarrative);
  const [merkleRoot, setMerkleRoot] = useState('9c72f16eb2befae4bcf1e1b7cbb510a6a13ba5b4d7a8f0aaee5337609c7ad42b');
  const [isRecalculatingHash, setIsRecalculatingHash] = useState(false);

  // Check for ML jargon leakage
  const detectedLeakage = useMemo(() => {
    return ALGO_LEAKAGE_TERMS.filter((term) =>
      new RegExp(`\\b${term}\\b`, 'i').test(narrativeText)
    );
  }, [narrativeText]);

  const handleCleanJargon = () => {
    let cleaned = narrativeText;
    ALGO_LEAKAGE_TERMS.forEach((term) => {
      const regex = new RegExp(`\\b${term}\\b`, 'gi');
      cleaned = cleaned.replace(regex, 'calibrated automated surveillance indicators');
    });
    setNarrativeText(cleaned);
    addToast('Jargon Purged', 'All algorithmic terminology replaced with compliant legal surveillance terms.', 'success');
  };

  const handleRecalculateMerkleRoot = async () => {
    setIsRecalculatingHash(true);
    try {
      const digest = await computeSha256(narrativeText + caseId + subjectEntity);
      setMerkleRoot(digest);
      addToast('Merkle Digest Updated', `New evidence root computed: ${digest.slice(0, 16)}...`, 'success');
    } catch (err) {
      console.error(err);
    } finally {
      setIsRecalculatingHash(false);
    }
  };

  const handleDownloadXml = () => {
    if (detectedLeakage.length > 0) {
      alert('Cannot export SAR: Narrative contains unapproved algorithmic terms that breach regulatory reporting standards. Please click "Purge Algorithmic Jargon" first.');
      return;
    }

    const xml = `<?xml version="1.0" encoding="UTF-8"?>
<RegulatoryFiling jurisdiction="${jurisdictionTemplate}" version="2.0">
  <CaseIdentifier>${caseId}</CaseIdentifier>
  <SubjectName>${subjectEntity}</SubjectName>
  <AccountNumber>${accountNumber}</AccountNumber>
  <TotalSuspiciousAmount>${transactionAmount}</TotalSuspiciousAmount>
  <TypologyCategory>${typologyCategory}</TypologyCategory>
  <CryptographicMerkleRoot>${merkleRoot}</CryptographicMerkleRoot>
  <NarrativeText><![CDATA[${narrativeText}]]></NarrativeText>
</RegulatoryFiling>`;

    const blob = new Blob([xml], { type: 'application/xml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `SAR_${jurisdictionTemplate}_${caseId}.xml`;
    a.click();
    URL.revokeObjectURL(url);

    addAuditEntry({
      eventType: 'SAR_GENERATED',
      entityId: caseId,
      details: `Generated and downloaded regulatory SAR XML for ${subjectEntity} (Template: ${jurisdictionTemplate}).`,
      actionBy: 'Sarah Jenkins (Analyst)'
    });
  };

  const handleExportCtrXml = () => {
    const xml = `<?xml version="1.0" encoding="UTF-8"?>
<CashTransactionReportBatch jurisdiction="${jurisdiction}" count="${ctrRecords.length}" generatedAt="${new Date().toISOString()}">
  ${ctrRecords.map((r) => `
  <TransactionRecord id="${r.id}">
    <Account>${r.accountNumber}</Account>
    <CustomerName>${r.entityName}</CustomerName>
    <Amount currency="${r.currency}">${r.amountUsd}</Amount>
    <AmountBdt>${r.amountNative}</AmountBdt>
    <Branch>${r.branch}</Branch>
    <Timestamp>${r.timestamp}</Timestamp>
    <Status>${r.status}</Status>
  </TransactionRecord>`).join('')}
</CashTransactionReportBatch>`;

    const blob = new Blob([xml], { type: 'application/xml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `CTR_Batch_Report_${new Date().toISOString().slice(0, 10)}.xml`;
    a.click();
    URL.revokeObjectURL(url);
    addToast('CTR Batch Exported', `Generated statutory CTR filing XML for ${ctrRecords.length} transactions.`, 'success');
  };

  return (
    <div className="p-4 sm:p-5 lg:p-6 max-w-[1750px] mx-auto space-y-5">
      {/* Page Title & Main Mode Switcher */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2 font-sans">
            <FileCheck2 className="w-5 h-5 text-emerald-400" />
            Automated SAR Filings &amp; CTR Aggregator Workbench
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Statutory filings engine for BFIU STR (MLPA 2012 § 25), FinCEN Form 111, UNODC goAML 2.0, and Cash Threshold Reports (CTR).
          </p>
        </div>

        {/* Sub-Tab Switcher */}
        <div className="flex items-center bg-[#0F172A] p-1 rounded-xl border border-[#334155] text-xs font-semibold">
          <button
            onClick={() => setActiveSubTab('SAR_STUDIO')}
            className={`px-3 py-1.5 rounded-lg transition-colors cursor-pointer ${
              activeSubTab === 'SAR_STUDIO'
                ? 'bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/40'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Suspicious Activity Report (SAR / STR) Studio
          </button>
          <button
            onClick={() => setActiveSubTab('CTR_AGGREGATOR')}
            className={`px-3 py-1.5 rounded-lg transition-colors cursor-pointer ${
              activeSubTab === 'CTR_AGGREGATOR'
                ? 'bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/40'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Cash Threshold Reports (CTR) Aggregator ({ctrRecords.length})
          </button>
        </div>
      </div>

      {activeSubTab === 'SAR_STUDIO' ? (
        /* SAR Studio Workspace */
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
          {/* Left Column: Form & Narrative Editor */}
          <div className="lg:col-span-8 space-y-4">
            {/* Top Toolbar: Jurisdiction Template Selection */}
            <div className="p-4 rounded-xl bg-[#0F172A] border border-[#1E293B] flex flex-wrap items-center justify-between gap-3 shadow-xl">
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono font-semibold text-slate-400">Jurisdiction Format:</span>
                {(['BFIU', 'FINCEN', 'GOAML'] as const).map((fmt) => (
                  <button
                    key={fmt}
                    onClick={() => setJurisdictionTemplate(fmt)}
                    className={`px-3 py-1 rounded-lg text-xs font-mono font-bold transition-colors cursor-pointer ${
                      jurisdictionTemplate === fmt
                        ? 'bg-sky-500/20 text-sky-300 border border-sky-500/40'
                        : 'text-slate-400 hover:text-slate-200 bg-[#0B0F17]'
                    }`}
                  >
                    {fmt === 'BFIU' ? 'BFIU STR (Bangladesh)' : fmt === 'FINCEN' ? 'FinCEN Form 111 (US)' : 'goAML XML 2.0 (EU)'}
                  </button>
                ))}
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => window.print()}
                  className="px-2.5 py-1 rounded-lg bg-[#0B0F17] hover:bg-[#1E293B] text-slate-300 border border-[#334155] text-xs flex items-center gap-1.5 cursor-pointer"
                >
                  <Printer className="w-3.5 h-3.5" />
                  <span>Print View</span>
                </button>
              </div>
            </div>

            {/* Jargon Leakage Blocker Banner */}
            {detectedLeakage.length > 0 && (
              <div className="p-3.5 bg-rose-950/40 border border-rose-800 rounded-xl flex items-center justify-between gap-3 text-xs text-rose-300">
                <div className="flex items-center gap-2">
                  <ShieldAlert className="w-4 h-4 shrink-0 text-rose-400" />
                  <span>
                    <strong>Regulatory Gate:</strong> Unapproved internal algorithmic terms detected: (
                    <span className="font-mono text-white">{detectedLeakage.join(', ')}</span>). Must be purged prior to submission.
                  </span>
                </div>
                <button
                  onClick={handleCleanJargon}
                  className="px-3 py-1 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-semibold cursor-pointer shrink-0"
                >
                  Purge Algorithmic Jargon
                </button>
              </div>
            )}

            {/* Structured Narrative Textarea */}
            <div className="p-5 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-[#1E293B]">
                <span className="text-xs font-mono font-bold text-slate-200 uppercase tracking-wider">
                  Official Regulatory Narrative (Factual Chronology)
                </span>
                <span className="text-[11px] font-mono text-slate-400">
                  {narrativeText.length} Characters • Ready for Regulatory Intake
                </span>
              </div>

              <textarea
                value={narrativeText}
                onChange={(e) => setNarrativeText(e.target.value)}
                rows={16}
                className="w-full p-4 bg-[#0B0F17] border border-[#334155] rounded-xl text-xs font-mono text-slate-100 placeholder:text-slate-600 focus:outline-none focus:border-sky-500 leading-relaxed"
              />
            </div>
          </div>

          {/* Right Column: Case Manifest & Cryptographic Merkle Root */}
          <div className="lg:col-span-4 bg-[#0F172A] border border-[#1E293B] rounded-2xl p-5 shadow-2xl flex flex-col justify-between space-y-5">
            <div className="space-y-4">
              <div>
                <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2 font-mono">
                  <ShieldCheck className="w-4 h-4 text-emerald-400" />
                  Filing Dossier &amp; Merkle Root
                </h3>
                <p className="text-xs text-slate-400 mt-1">
                  Cryptographically binds all evidence files to prevent evidentiary challenge under FRE 902(11).
                </p>
              </div>

              {/* Case Parameters */}
              <div className="space-y-2 text-xs font-mono">
                <div className="p-2.5 bg-[#0B0F17] rounded-lg border border-[#1E293B]">
                  <span className="text-slate-500 text-[10px] block">Case Docket ID:</span>
                  <span className="font-bold text-sky-400">{caseId}</span>
                </div>
                <div className="p-2.5 bg-[#0B0F17] rounded-lg border border-[#1E293B]">
                  <span className="text-slate-500 text-[10px] block">Primary Subject Entity:</span>
                  <span className="font-bold text-slate-200">{subjectEntity}</span>
                </div>
                <div className="p-2.5 bg-[#0B0F17] rounded-lg border border-[#1E293B]">
                  <span className="text-slate-500 text-[10px] block">Total Suspicious Volume:</span>
                  <span className="font-bold text-emerald-400">{transactionAmount}</span>
                </div>
              </div>

              {/* Cryptographic Merkle Digest Box */}
              <div className="p-3 bg-[#0B0F17] border border-[#1E293B] rounded-xl space-y-2">
                <div className="flex items-center justify-between text-[10px] font-mono">
                  <span className="text-slate-400 uppercase font-bold">Evidence Merkle Root</span>
                  <button
                    onClick={handleRecalculateMerkleRoot}
                    disabled={isRecalculatingHash}
                    className="text-sky-400 hover:text-sky-300 flex items-center gap-1 cursor-pointer"
                  >
                    <RefreshCw className={`w-3 h-3 ${isRecalculatingHash ? 'animate-spin' : ''}`} />
                    <span>Recalculate</span>
                  </button>
                </div>
                <div className="p-2 bg-[#090D14] rounded border border-[#334155] font-mono text-[10px] text-emerald-400 break-all select-all">
                  {merkleRoot}
                </div>
              </div>
            </div>

            {/* Submission Actions */}
            <div className="pt-4 border-t border-[#1E293B] space-y-2.5">
              <button
                onClick={handleDownloadXml}
                className="w-full py-2.5 px-4 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs transition-colors flex items-center justify-center gap-2 cursor-pointer shadow-lg shadow-sky-600/20"
              >
                <Download className="w-4 h-4" />
                <span>Export Official {jurisdictionTemplate} XML</span>
              </button>

              <button
                onClick={() => {
                  setFourEyesModalOpen(true, {
                    actionType: 'SAR_FILING',
                    actionTitle: `Submit Formal Regulatory SAR (${caseId})`,
                    targetId: caseId,
                    details: `Transmit validated ${jurisdictionTemplate} SAR filing to regulatory authorities. Subject: ${subjectEntity}. Merkle root: ${merkleRoot.slice(0, 16)}...`
                  });
                }}
                className="w-full py-2.5 px-4 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-semibold text-xs transition-colors flex items-center justify-center gap-2 cursor-pointer shadow-lg shadow-rose-600/20"
              >
                <Lock className="w-4 h-4" />
                <span>Authorize &amp; Transmit (4-Eyes)</span>
              </button>
            </div>
          </div>
        </div>
      ) : (
        /* CTR Aggregator Sub-Tab */
        <div className="space-y-4">
          <div className="p-4 rounded-xl bg-[#0F172A] border border-[#1E293B] flex flex-wrap items-center justify-between gap-4 shadow-xl">
            <div>
              <h2 className="text-sm font-bold text-slate-100 flex items-center gap-2 font-mono">
                <Table className="w-4 h-4 text-emerald-400" />
                Automated Cash Threshold Reports (CTR) Pipeline
              </h2>
              <p className="text-xs text-slate-400 mt-0.5">
                Statutory cash transactions &ge; ৳1,000,000 BDT (Bangladesh) or &ge; $10,000 USD (FinCEN). Automatically compiled from teller systems.
              </p>
            </div>

            <button
              onClick={handleExportCtrXml}
              className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition-colors flex items-center gap-2 cursor-pointer shadow-lg shadow-emerald-600/20"
            >
              <FileSpreadsheet className="w-4 h-4" />
              <span>Batch Export CTR XML</span>
            </button>
          </div>

          {/* CTR Table */}
          <div className="bg-[#0F172A] border border-[#1E293B] rounded-xl overflow-hidden shadow-2xl">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-300">
                <thead className="bg-[#0B0F17] border-b border-[#1E293B] text-[11px] font-mono uppercase text-slate-400">
                  <tr>
                    <th className="px-4 py-3">CTR ID</th>
                    <th className="px-4 py-3">Customer Legal Name</th>
                    <th className="px-4 py-3">Account Number</th>
                    <th className="px-4 py-3 text-right">Cash Amount</th>
                    <th className="px-4 py-3 text-right">Amount (BDT)</th>
                    <th className="px-4 py-3">Branch Location</th>
                    <th className="px-4 py-3">Timestamp</th>
                    <th className="px-4 py-3 text-center">Filing Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#1E293B]">
                  {ctrRecords.map((r) => (
                    <tr key={r.id} className="hover:bg-[#1E293B]/40 transition-colors">
                      <td className="px-4 py-3 font-mono font-bold text-sky-400">{r.id}</td>
                      <td className="px-4 py-3 font-semibold text-slate-100">{r.entityName}</td>
                      <td className="px-4 py-3 font-mono text-slate-400">
                        <PiiText value={r.accountNumber} type="account" />
                      </td>
                      <td className="px-4 py-3 text-right font-mono font-bold text-emerald-400 tabular-nums">
                        ${r.amountUsd.toLocaleString(undefined, { minimumFractionDigits: 2 })} {r.currency}
                      </td>
                      <td className="px-4 py-3 text-right font-mono text-slate-400 tabular-nums">
                        ৳{r.amountNative.toLocaleString()}
                      </td>
                      <td className="px-4 py-3 text-slate-300">{r.branch}</td>
                      <td className="px-4 py-3 font-mono text-[11px] text-slate-400">{r.timestamp}</td>
                      <td className="px-4 py-3 text-center">
                        <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                          {r.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default function SarWorkbenchPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center text-slate-400">Loading SAR Workbench...</div>}>
      <SarWorkbenchContent />
    </Suspense>
  );
}
