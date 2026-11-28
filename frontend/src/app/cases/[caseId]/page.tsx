'use client';

import React, { useState } from 'react';
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
  FileText,
  Copy,
  Check,
  Send,
  ExternalLink,
  MessageSquare
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { PiiText } from '@/components/ui/PiiText';
import { formatCurrencyByJurisdiction } from '@/lib/compliance/jurisdictions';

export default function CaseDetailPage() {
  const params = useParams();
  const caseId = (params?.caseId as string) || 'CASE-2026-0881';
  const { cases, jurisdiction, updateCaseMilestone, addCaseNote, setFourEyesModalOpen } = useBankingStore();

  const caseData = cases.find((c) => c.id === caseId) || cases[0];
  const [newNote, setNewNote] = useState('');
  const [copiedHash, setCopiedHash] = useState<string | null>(null);

  if (!caseData) {
    return (
      <div className="p-8 text-center text-slate-400">
        <p>Case dossier not found.</p>
        <Link href="/cases" className="text-sky-400 hover:underline mt-2 inline-block">
          Return to Case Docket
        </Link>
      </div>
    );
  }

  const handlePostNote = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newNote.trim()) return;
    addCaseNote(caseData.id, newNote.trim());
    setNewNote('');
  };

  const handleCopyHash = (hash: string) => {
    navigator.clipboard.writeText(hash);
    setCopiedHash(hash);
    setTimeout(() => setCopiedHash(null), 2500);
  };

  const handleToggleMilestone = (index: number) => {
    const current = caseData.milestones[index];
    if (!current) return;
    const nextStatus =
      current.status === 'COMPLETE'
        ? 'IN_PROGRESS'
        : current.status === 'IN_PROGRESS'
        ? 'PENDING'
        : 'COMPLETE';

    updateCaseMilestone(caseData.id, index, nextStatus);
  };

  return (
    <div className="p-4 sm:p-5 lg:p-6 max-w-[1650px] mx-auto space-y-6">
      {/* Back button and Dossier Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <Link
            href="/cases"
            className="flex items-center gap-1.5 text-xs text-slate-400 hover:text-slate-200 mb-2 transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Back to Case Docket</span>
          </Link>

          <div className="flex flex-wrap items-center gap-3">
            <h1 className="text-xl font-bold font-mono text-slate-100">{caseData.id}</h1>
            <span className="px-2 py-0.5 rounded text-xs font-mono font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">
              {caseData.status.replace(/_/g, ' ')}
            </span>
            <span className="text-xs text-slate-500">|</span>
            <span className="text-sm font-semibold text-slate-200">{caseData.title}</span>
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
            <FileText className="w-3.5 h-3.5 text-sky-400" />
            <span>Draft Regulatory SAR</span>
          </Link>

          <button
            onClick={() => {
              setFourEyesModalOpen(true, {
                actionType: 'SAR_FILING',
                actionTitle: `Senior 4-Eyes CCO Sign-Off (${caseData.id})`,
                targetId: caseData.id,
                details: `Formal supervisory sign-off and regulatory transmission authorization for ${caseData.entityName}. Total exposure: $${caseData.riskExposureUsd.toLocaleString()}`
              });
            }}
            className="flex items-center gap-1.5 px-4 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs tracking-wide transition-all shadow-md cursor-pointer"
          >
            <Lock className="w-3.5 h-3.5" />
            <span>4-Eyes CCO Sign-Off</span>
          </button>
        </div>
      </div>

      {/* Case Overview Metrics Strip */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-[#0F172A] border border-[#1E293B]">
          <span className="text-xs font-mono text-slate-500 block">Primary Target</span>
          <span className="text-sm font-bold text-slate-100 block mt-1">{caseData.entityName}</span>
          <span className="text-xs text-slate-400">Designated High-Risk Subject</span>
        </div>

        <div className="p-4 rounded-xl bg-[#0F172A] border border-[#1E293B]">
          <span className="text-xs font-mono text-slate-500 block">Total Case Exposure</span>
          <span className="text-base font-bold font-mono text-emerald-400 block mt-1">
            {formatCurrencyByJurisdiction(caseData.riskExposureUsd, jurisdiction)}
          </span>
          <span className="text-xs text-slate-400">Summed across all flagged accounts</span>
        </div>

        <div className="p-4 rounded-xl bg-[#0F172A] border border-[#1E293B]">
          <span className="text-xs font-mono text-slate-500 block">SLA Window</span>
          <span className="text-sm font-bold text-rose-400 block mt-1">{caseData.slaHours}H STATUTORY SLA</span>
          <span className="text-xs text-slate-400">Mandatory filing countdown</span>
        </div>

        <div className="p-4 rounded-xl bg-[#0F172A] border border-[#1E293B]">
          <span className="text-xs font-mono text-slate-500 block">Assigned Lead</span>
          <span className="text-sm font-bold text-slate-100 block mt-1">{caseData.leadInvestigator}</span>
          <span className="text-xs text-slate-400 font-mono">Dossier Locked to Lead</span>
        </div>
      </div>

      {/* Investigation Progress Milestones Bar */}
      <div className="p-5 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl space-y-4">
        <div className="flex items-center justify-between pb-2 border-b border-[#1E293B]">
          <div>
            <h2 className="text-sm font-bold text-slate-100 font-mono">
              6-Stage Investigation Progression Pipeline
            </h2>
            <p className="text-xs text-slate-400">
              Click any stage milestone to advance its status. All milestone state transitions are hashed to the WORM audit trail.
            </p>
          </div>
          <span className="text-xs font-mono text-emerald-400 font-bold">
            {caseData.milestones.filter((m) => m.status === 'COMPLETE').length} of {caseData.milestones.length} Stages Completed
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-3">
          {caseData.milestones.map((m, idx) => (
            <div
              key={idx}
              onClick={() => handleToggleMilestone(idx)}
              className={`p-3 rounded-xl border transition-all cursor-pointer select-none ${
                m.status === 'COMPLETE'
                  ? 'bg-emerald-950/20 border-emerald-500/40 hover:border-emerald-500'
                  : m.status === 'IN_PROGRESS'
                  ? 'bg-amber-950/20 border-amber-500/40 hover:border-amber-500'
                  : 'bg-[#0B0F17] border-[#1E293B] hover:border-[#334155]'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-bold text-slate-500">STAGE {idx + 1}</span>
                <span
                  className={`w-2 h-2 rounded-full ${
                    m.status === 'COMPLETE'
                      ? 'bg-emerald-400'
                      : m.status === 'IN_PROGRESS'
                      ? 'bg-amber-400 animate-pulse'
                      : 'bg-slate-600'
                  }`}
                />
              </div>

              <div className="font-semibold text-xs text-slate-200 mt-2 truncate">{m.title}</div>
              <div className="text-xs text-slate-400 mt-1 truncate">{m.detail}</div>

              <div className="mt-3 pt-2 border-t border-[#1E293B]/60 flex items-center justify-between text-xs font-mono">
                <span className={m.status === 'COMPLETE' ? 'text-emerald-400' : 'text-slate-500'}>
                  {m.status}
                </span>
                <span className="text-slate-500">{m.time ? m.time.split(' ')[0] : '—'}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Split Section: Pinned Evidence Vault (Left) & Case Notes / Audit Trail (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Evidence Vault */}
        <div className="lg:col-span-7 bg-[#0F172A] border border-[#1E293B] rounded-2xl p-5 shadow-xl space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-[#1E293B]">
            <div>
              <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2 font-mono">
                <FileCheck2 className="w-4 h-4 text-emerald-400" />
                Pinned Evidence Vault (FRE 902(11) Cryptographic Integrity)
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Every attached trade document, bill of entry, and interbank telegraphic transfer is cryptographically anchored.
              </p>
            </div>
          </div>

          <div className="space-y-3">
            {caseData.evidenceItems.map((ev, i) => (
              <div
                key={i}
                className="p-3.5 rounded-xl bg-[#0B0F17] border border-[#1E293B] flex flex-wrap items-center justify-between gap-3 text-xs"
              >
                <div className="space-y-1 max-w-[420px]">
                  <div className="font-semibold text-slate-100 truncate">{ev.name}</div>
                  <div className="text-xs text-slate-400">
                    Category: <strong className="text-slate-300">{ev.type}</strong> • Size: {ev.size}
                  </div>
                  <div className="flex items-center gap-1.5 font-mono text-xs text-slate-500">
                    <span>SHA-256:</span>
                    <span className="text-sky-400 truncate">{ev.sha256}</span>
                    <button
                      onClick={() => handleCopyHash(ev.sha256)}
                      title="Copy SHA-256 Digest"
                      className="p-1 hover:text-white cursor-pointer"
                    >
                      {copiedHash === ev.sha256 ? (
                        <Check className="w-3 h-3 text-emerald-400" />
                      ) : (
                        <Copy className="w-3 h-3" />
                      )}
                    </button>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded text-xs font-mono bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                    VERIFIED ANCHOR
                  </span>
                  <button
                    onClick={() => {
                      const blob = new Blob([`Intelligent-AML Verified Evidence: ${ev.name}\nSHA-256: ${ev.sha256}\nCase: ${caseData.id}`], { type: 'text/plain' });
                      const url = URL.createObjectURL(blob);
                      const a = document.createElement('a');
                      a.href = url;
                      a.download = `${ev.name}.txt`;
                      a.click();
                    }}
                    className="p-2 rounded-lg bg-[#1E293B] hover:bg-[#334155] text-slate-300 hover:text-white transition-colors cursor-pointer"
                    title="Download Evidence Manifest"
                  >
                    <Download className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Case Notes & Analyst Log */}
        <div className="lg:col-span-5 bg-[#0F172A] border border-[#1E293B] rounded-2xl p-5 shadow-xl flex flex-col justify-between space-y-4">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-[#1E293B]">
              <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2 font-mono">
                <MessageSquare className="w-4 h-4 text-sky-400" />
                Analyst Working Notes &amp; Audit Entries
              </h3>
            </div>

            <div className="mt-3 space-y-3 max-h-[360px] overflow-y-auto pr-1">
              {caseData.notes.map((note, idx) => (
                <div key={idx} className="p-3 bg-[#0B0F17] border border-[#1E293B] rounded-xl text-xs space-y-1">
                  <div className="flex items-center justify-between text-xs font-mono text-slate-500">
                    <span className="text-sky-400 font-semibold">{note.author}</span>
                    <span>{note.timestamp}</span>
                  </div>
                  <p className="text-slate-300 leading-relaxed">{note.content}</p>
                </div>
              ))}
            </div>
          </div>

          {/* New Note Form */}
          <form onSubmit={handlePostNote} className="pt-3 border-t border-[#1E293B] flex items-center gap-2">
            <input
              type="text"
              placeholder="Append timestamped analyst note to case dossier..."
              value={newNote}
              onChange={(e) => setNewNote(e.target.value)}
              className="flex-1 px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-xl text-xs text-slate-100 placeholder:text-slate-500 focus:outline-none focus:border-sky-500"
            />
            <button
              type="submit"
              className="px-4 py-2 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs flex items-center gap-1.5 cursor-pointer shadow-md shadow-sky-600/20"
            >
              <Send className="w-3.5 h-3.5" />
              <span>Post</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
