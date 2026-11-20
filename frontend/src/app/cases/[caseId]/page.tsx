'use client';

import React from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import {
  FolderGit2,
  CheckCircle2,
  Clock,
  ShieldAlert,
  GitFork,
  FileCheck2,
  Lock,
  ArrowLeft,
  Download,
  Building,
  User,
  AlertTriangle,
  FileText
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { SEEDED_CASES } from '@/lib/seedData';
import { PiiText } from '@/components/ui/PiiText';

export default function CaseDetailPage() {
  const params = useParams();
  const caseId = params?.caseId as string || 'CASE-2026-0881';
  const { setFourEyesModalOpen } = useBankingStore();

  const caseData = SEEDED_CASES.find((c) => c.id === caseId) || SEEDED_CASES[0]!;

  const milestones = [
    { title: '1. Alert Triggered', status: 'COMPLETE', time: '2026-09-02 08:14 UTC', detail: 'C-STGB Tier 1 Quarantined' },
    { title: '2. Analyst Triage', status: 'COMPLETE', time: '2026-09-02 08:35 UTC', detail: 'Sarah Jenkins (Assigned)' },
    { title: '3. RFI Issued', status: 'COMPLETE', time: '2026-09-02 09:00 UTC', detail: 'Commercial Invoice Requested' },
    { title: '4. Evidence Compiled', status: 'COMPLETE', time: '2026-09-02 10:15 UTC', detail: '4 Documents Hashed (SHA-256)' },
    { title: '5. SAR Drafted', status: 'COMPLETE', time: '2026-09-02 11:00 UTC', detail: 'Autonomous GenAI Narrative Ready' },
    { title: '6. 4-Eyes CCO Sign-Off', status: 'PENDING', time: 'Awaiting Sign-off', detail: 'Dual Signatory Gate Required' },
  ];

  const evidenceDossier = [
    {
      name: 'ASYCUDA_Customs_Declaration_CTG_88912.pdf',
      type: 'Customs Bill of Entry',
      sha256: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
      size: '2.4 MB',
      verified: true
    },
    {
      name: 'SWIFT_MT700_Documentary_Credit.xml',
      type: 'Financial Settlement Rail',
      sha256: 'ca978112ca1bbdcafac231b39a23dc4da786081442f05d060a31e8725b7e0ee9',
      size: '48 KB',
      verified: true
    },
    {
      name: 'Commercial_Invoice_Cotton_Overvaluation.pdf',
      type: 'Invoicing Evidence',
      sha256: '4e1243bd22c66e76c2ba9eddc1f91394e57f9f835f8c6e7f225d57b545464a02',
      size: '1.8 MB',
      verified: true
    }
  ];

  return (
    <div className="p-6 max-w-[1600px] mx-auto space-y-6">
      {/* Back button and Dossier Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <Link
            href="/cases"
            className="flex items-center gap-1.5 text-xs text-slate-400 hover:text-slate-200 mb-2 transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Back to All Cases</span>
          </Link>

          <div className="flex items-center gap-3">
            <h1 className="text-xl font-bold font-mono text-slate-100">{caseData.id}</h1>
            <span className="px-2 py-0.5 rounded text-[11px] font-mono font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">
              {caseData.status}
            </span>
            <span className="text-xs text-slate-400">|</span>
            <span className="text-xs font-semibold text-slate-200">{caseData.title}</span>
          </div>
        </div>

        {/* Action Toolbar */}
        <div className="flex items-center gap-2">
          <Link
            href={`/graph?node=BD22-EBLB-4829-1092-8823`}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#0F172A] hover:bg-[#1E293B] border border-[#334155] text-xs font-medium text-slate-200 transition-colors"
          >
            <GitFork className="w-3.5 h-3.5 text-purple-400" />
            <span>Cash Flow Graph</span>
          </Link>

          <Link
            href={`/sar?caseId=${caseData.id}`}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#0F172A] hover:bg-[#1E293B] border border-[#334155] text-xs font-medium text-slate-200 transition-colors"
          >
            <FileText className="w-3.5 h-3.5 text-rose-400" />
            <span>Review SAR Draft</span>
          </Link>

          <button
            onClick={() => {
              setFourEyesModalOpen(true, {
                actionType: 'SAR_FILING',
                actionTitle: `4-Eyes Final Sign-Off: ${caseData.id}`,
                targetId: caseData.id,
                details: `Formal regulatory SAR sign-off and submission to BFIU under MLPA 2012 § 25.`
              });
            }}
            className="flex items-center gap-1.5 px-4 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold text-xs uppercase tracking-wide transition-all shadow-md"
          >
            <Lock className="w-3.5 h-3.5" />
            <span>Execute 4-Eyes CCO Sign-Off</span>
          </button>
        </div>
      </div>

      {/* 6-Stage Milestone Stepper */}
      <div className="p-5 bg-[#0F172A] border border-[#1E293B] rounded-xl">
        <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-4">
          Statutory Investigation Lifecycle (FRE 902(11) Chain of Custody)
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-3">
          {milestones.map((m, idx) => (
            <div
              key={idx}
              className={`p-3 rounded-lg border text-xs flex flex-col justify-between ${
                m.status === 'COMPLETE'
                  ? 'bg-emerald-950/20 border-emerald-900/40 text-emerald-300'
                  : 'bg-amber-950/20 border-amber-900/40 text-amber-300'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <span className="font-semibold text-slate-200">{m.title}</span>
                  {m.status === 'COMPLETE' ? (
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                  ) : (
                    <Clock className="w-3.5 h-3.5 text-amber-400 animate-pulse" />
                  )}
                </div>
                <p className="text-[11px] text-slate-400">{m.detail}</p>
              </div>
              <div className="mt-3 pt-2 border-t border-slate-800 text-[10px] font-mono text-slate-500">
                {m.time}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Two Column Layout: Subject Info & Cryptographic Evidence Dossier */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Subject Profile & Narrative (5 Cols) */}
        <div className="lg:col-span-5 space-y-6">
          <div className="p-5 bg-[#0F172A] border border-[#1E293B] rounded-xl space-y-4">
            <h2 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
              <Building className="w-4 h-4 text-slate-400" />
              Primary Target Entity Profile
            </h2>

            <div className="space-y-2 text-xs">
              <div className="flex items-center justify-between py-1.5 border-b border-[#1E293B]">
                <span className="text-slate-400">Legal Name:</span>
                <strong className="text-slate-200">{caseData.subjectEntity}</strong>
              </div>
              <div className="flex items-center justify-between py-1.5 border-b border-[#1E293B]">
                <span className="text-slate-400">Account Number:</span>
                <PiiText value={caseData.subjectAccount || "BD22-EBLB-4829-1092-8823"} type="account" className="font-mono text-slate-200" />
              </div>
              <div className="flex items-center justify-between py-1.5 border-b border-[#1E293B]">
                <span className="text-slate-400">Financial Exposure:</span>
                <strong className="font-mono text-rose-400 text-sm">
                  ${caseData.totalExposure.toLocaleString(undefined, { minimumFractionDigits: 2 })}
                </strong>
              </div>
              <div className="flex items-center justify-between py-1.5 border-b border-[#1E293B]">
                <span className="text-slate-400">Lead Investigator:</span>
                <span className="text-slate-200">{caseData.assignedTo}</span>
              </div>
            </div>

            <div className="pt-2">
              <span className="text-xs font-medium text-slate-400 block mb-1">
                Investigative Theory & Typology:
              </span>
              <p className="text-xs text-slate-300 leading-relaxed bg-[#0B0F17] p-3 rounded-lg border border-[#1E293B]">
                Suspected Trade-Based Money Laundering (TBML) through inflated documentary credit pricing exceeding ASYCUDA benchmark valuation by +333.7%, accompanied by domestic smurfing through MFS agent accounts.
              </p>
            </div>
          </div>
        </div>

        {/* Right Column: Cryptographic Evidence Dossier (7 Cols) */}
        <div className="lg:col-span-7 space-y-6">
          <div className="p-5 bg-[#0F172A] border border-[#1E293B] rounded-xl space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
                  <FileCheck2 className="w-4 h-4 text-emerald-400" />
                  Preserved Evidence Dossier (FRE 902(11) Compliant)
                </h2>
                <p className="text-[11px] text-slate-400 mt-0.5">
                  All documents hashed upon ingest with immutable SHA-256 digital fingerprint.
                </p>
              </div>

              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                WORM CHAIN VERIFIED
              </span>
            </div>

            <div className="divide-y divide-[#1E293B]">
              {evidenceDossier.map((doc, idx) => (
                <div key={idx} className="py-3 flex items-start justify-between gap-4">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-xs text-slate-200">{doc.name}</span>
                      <span className="text-[10px] text-slate-400 font-mono">({doc.size})</span>
                    </div>
                    <span className="text-[11px] text-slate-400 block mt-0.5">{doc.type}</span>
                    <div className="mt-1.5 flex items-center gap-1.5 text-[10px] font-mono text-emerald-400 bg-[#0B0F17] px-2 py-1 rounded border border-[#1E293B]">
                      <span className="text-slate-500">SHA-256:</span>
                      <span className="break-all">{doc.sha256}</span>
                    </div>
                  </div>

                  <button
                    onClick={() => alert(`Downloading verified copy of ${doc.name}`)}
                    className="p-1.5 rounded bg-[#1E293B] hover:bg-[#334155] text-slate-300 transition-colors shrink-0"
                    title="Download Verified Evidence"
                  >
                    <Download className="w-3.5 h-3.5" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
