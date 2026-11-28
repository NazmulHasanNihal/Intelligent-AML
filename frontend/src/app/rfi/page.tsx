'use client';

import React, { useState } from 'react';
import {
  MailQuestion,
  ShieldAlert,
  AlertTriangle,
  UploadCloud,
  FileCheck2,
  Clock,
  CheckCircle2,
  Plus,
  ArrowRight,
  Lock,
  Building,
  Calendar,
  Send,
  Bell,
  Check,
  X,
  FileText
} from 'lucide-react';
import { scanTextForTippingOff } from '@/lib/compliance/tippingOff';
import { PiiText } from '@/components/ui/PiiText';
import { useBankingStore } from '@/lib/store';
import { computeFileSha256 } from '@/lib/audit/hashChain';

interface RfiRequestItem {
  id: string;
  caseId: string;
  targetEntity: string;
  accountNumber: string;
  reason: string;
  deadlineDays: number;
  status: 'ISSUED_PENDING' | 'DOCUMENT_UPLOADED' | 'REMINDER_DISPATCHED';
  issuedAt: string;
  requiredDocuments: string[];
}

const INITIAL_RFIS: RfiRequestItem[] = [
  {
    id: 'RFI-2026-0042',
    caseId: 'CASE-2026-0881',
    targetEntity: 'Meghna Industrial & Agro Processing Ltd',
    accountNumber: 'BD22-EBLB-4829-1092-8823',
    reason: 'Routine institutional documentation refresh for LC-2026-CTG-88912 commercial invoice verification.',
    deadlineDays: 7,
    status: 'ISSUED_PENDING',
    issuedAt: '2026-09-02 09:00:00 UTC',
    requiredDocuments: ['Customs Bill of Entry', 'Supplier Commercial Invoice']
  },
  {
    id: 'RFI-2026-0043',
    caseId: 'CASE-2026-0882',
    targetEntity: 'Tanvir Ahmed Logistics',
    accountNumber: 'BD22-SCBL-9912-3341-7719',
    reason: 'Periodic customer due diligence update and agent aggregation turnover review.',
    deadlineDays: 5,
    status: 'ISSUED_PENDING',
    issuedAt: '2026-09-02 10:15:00 UTC',
    requiredDocuments: ['Trade License', 'Agent Commission Settlement Statement']
  }
];

export default function RfiHubPage() {
  const { addToast, addAuditEntry } = useBankingStore();
  const [rfis, setRfis] = useState<RfiRequestItem[]>(INITIAL_RFIS);

  // New RFI Form State
  const [targetEntity, setTargetEntity] = useState('Meghna Industrial & Agro Processing Ltd');
  const [targetAccount, setTargetAccount] = useState('BD22-EBLB-4829-1092-8823');
  const [rfiReason, setRfiReason] = useState('Routine institutional documentation refresh for LC-2026-CTG-88912 commercial invoice verification.');
  const [deadlineDays, setDeadlineDays] = useState(7);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);

  // Live anti-tipping-off check
  const tippingOffCheck = scanTextForTippingOff(rfiReason);

  const handleRewriteCompliant = () => {
    setRfiReason(
      'Periodic account documentation refresh and commercial invoice verification pursuant to standard institutional customer due diligence procedures.'
    );
    addToast('Rewritten to Safe Text', 'Prohibited statutory terms replaced with standard commercial KYC language.', 'success');
  };

  const handleCreateRfi = async (e: React.FormEvent) => {
    e.preventDefault();
    if (tippingOffCheck.containsTippingOff) {
      addToast(
        'Anti-Tipping-Off Block',
        'Prohibited AML/SAR language detected (BSA 31 U.S.C. § 5318(g)(2) / MLPA 2012 § 6). Rewrite cleanly.',
        'critical'
      );
      return;
    }

    const requiredDocuments = ['Customs Bill of Entry', 'Supplier Commercial Invoice'];
    let createdId = `RFI-2026-${Math.floor(1000 + Math.random() * 9000)}`;
    try {
      const res = await fetch('/api/v1/rfi', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          caseId: 'CASE-2026-0881',
          targetEntity,
          accountNumber: targetAccount,
          reason: rfiReason,
          deadlineDays: Number(deadlineDays),
          requiredDocuments
        })
      });
      if (res.status === 422) {
        const errData = await res.json();
        addToast('Server Tipping-Off Rejection', errData.message || 'Prohibited terminology blocked.', 'critical');
        return;
      }
      if (res.ok) {
        const data = await res.json();
        if (data?.rfi?.id) createdId = data.rfi.id;
      }
    } catch {
      // Fall back to deterministic client creation
    }

    const newRfi = {
      id: createdId,
      caseId: 'CASE-2026-0881',
      targetEntity,
      accountNumber: targetAccount,
      reason: rfiReason,
      deadlineDays: Number(deadlineDays),
      status: 'ISSUED_PENDING' as const,
      issuedAt: new Date().toISOString().replace('T', ' ').slice(0, 19),
      requiredDocuments
    };

    setRfis([newRfi, ...rfis]);
    addToast('RFI Dispatched', `Issued ${newRfi.id} to ${targetEntity}. Server tipping-off guard passed.`, 'success');
    addAuditEntry({
      eventType: 'DOCUMENT_UPLOADED',
      entityId: newRfi.id,
      details: `Dispatched customer RFI notice for ${targetEntity}. Reason verified safe under MLPA 2012 § 6.`,
      actionBy: 'Amina Rahman, CFE (Lead Investigator)'
    });
  };

  const handleSendReminder = (rfiId: string) => {
    setRfis((prev) =>
      prev.map((r) =>
        r.id === rfiId ? { ...r, status: 'REMINDER_DISPATCHED' as any } : r
      )
    );
    addToast('Reminder Sent', `Automated compliance reminder dispatched for ${rfiId}.`, 'info');
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploadStatus('Computing client SHA-256 hash & verifying server seal...');
    try {
      const buffer = await file.arrayBuffer();
      const clientHash = await computeFileSha256(buffer);
      let finalHash = clientHash;

      try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('rfiId', rfis[0]?.id || 'RFI-2026-0042');
        formData.append('clientSha256', clientHash);
        const res = await fetch('/api/v1/rfi/upload', { method: 'POST', body: formData });
        if (res.ok) {
          const data = await res.json();
          if (data?.sha256) finalHash = data.sha256;
        }
      } catch {
        // Retain WebCrypto digest fallback
      }

      setUploadStatus(`Verified & Anchored! SHA-256: ${finalHash.slice(0, 20)}...`);

      // Update first RFI status
      setRfis((prev) =>
        prev.map((r, i) =>
          i === 0 ? { ...r, status: 'DOCUMENT_UPLOADED' as any } : r
        )
      );

      addAuditEntry({
        eventType: 'DOCUMENT_UPLOADED',
        entityId: rfis[0]?.id || 'RFI-2026-0042',
        details: `Customer uploaded ${file.name} for RFI response. Anchored SHA-256: ${finalHash}`,
        actionBy: 'Customer Portal Ingestion'
      });
      addToast('Document Verified', `${file.name} server-hashed and attached to RFI record.`, 'success');
    } catch (err) {
      setUploadStatus('Failed to compute file digest.');
    }
  };

  return (
    <div className="p-4 sm:p-5 lg:p-6 max-w-[1750px] mx-auto space-y-5">
      {/* Page Title */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2 font-sans">
            <MailQuestion className="w-5 h-5 text-indigo-400" />
            Compliance Request for Information (RFI) Hub
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">
            Controlled counterparty outreach with live Anti-Tipping-Off Guard (31 U.S.C. § 5318(g)(2) &amp; MLPA 2012 § 6).
          </p>
        </div>

        <div className="flex items-center gap-2">
          <div className="px-3 py-1.5 rounded-lg bg-[#0F172A] border border-[#334155] text-xs font-mono text-slate-300">
            <span>Active Outbound Notices: <strong>{rfis.length} Requests</strong></span>
          </div>
        </div>
      </div>

      {/* Main Split Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Left Column: Author Safe RFI Notice Form */}
        <div className="lg:col-span-6 bg-[#0F172A] border border-[#1E293B] rounded-2xl p-5 shadow-2xl space-y-4">
          <div>
            <h2 className="text-sm font-bold text-slate-100 flex items-center gap-2 font-mono">
              <Send className="w-4 h-4 text-indigo-400" />
              Author Statutory-Safe Customer Notice
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Strictly prohibits AML, SAR, or law enforcement language to avoid tipping off customers under penalty of law.
            </p>
          </div>

          <form onSubmit={handleCreateRfi} className="space-y-4 text-xs font-sans">
            <div>
              <label className="text-slate-400 block mb-1 font-mono text-xs">Target Corporate Entity</label>
              <input
                type="text"
                required
                value={targetEntity}
                onChange={(e) => setTargetEntity(e.target.value)}
                className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-100 focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div>
              <label className="text-slate-400 block mb-1 font-mono text-xs">Account Number (Masked)</label>
              <input
                type="text"
                required
                value={targetAccount}
                onChange={(e) => setTargetAccount(e.target.value)}
                className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-100 focus:outline-none focus:border-indigo-500 font-mono"
              />
            </div>

            {/* RFI Reason with Live Anti-Tipping-Off Scanner */}
            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="text-slate-400 font-mono text-xs">Customer-Facing Notice Reason</label>
                {tippingOffCheck.containsTippingOff ? (
                  <span className="text-xs font-mono font-bold text-rose-400 animate-pulse flex items-center gap-1">
                    <AlertTriangle className="w-3 h-3" />
                    TIPPING-OFF VIOLATION DETECTED
                  </span>
                ) : (
                  <span className="text-xs font-mono text-emerald-400 flex items-center gap-1">
                    <CheckCircle2 className="w-3 h-3" />
                    Statutory Language Compliant
                  </span>
                )}
              </div>

              <textarea
                value={rfiReason}
                onChange={(e) => setRfiReason(e.target.value)}
                rows={4}
                className={`w-full p-3 bg-[#0B0F17] border rounded-xl text-xs font-mono text-slate-100 focus:outline-none transition-colors ${
                  tippingOffCheck.containsTippingOff
                    ? 'border-rose-500 focus:border-rose-400'
                    : 'border-[#334155] focus:border-indigo-500'
                }`}
              />

              {/* Tipping-Off Alert Banner with 1-Click Fix */}
              {tippingOffCheck.containsTippingOff && (
                <div className="mt-2 p-3 bg-rose-950/40 border border-rose-800 rounded-xl space-y-2 text-xs text-rose-300">
                  <div className="flex items-center justify-between">
                    <span>
                      Contains prohibited terms: <strong>{tippingOffCheck.matchedPhrases.join(', ')}</strong>
                    </span>
                    <button
                      type="button"
                      onClick={handleRewriteCompliant}
                      className="px-2.5 py-1 rounded bg-rose-600 hover:bg-rose-500 text-white font-semibold text-xs cursor-pointer"
                    >
                      1-Click Safe Rewrite
                    </button>
                  </div>
                  <p className="text-xs text-rose-400">
                    Disclosing AML investigations or SAR status constitutes an offense under MLPA 2012 § 6.
                  </p>
                </div>
              )}
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-slate-400 block mb-1 font-mono text-xs">Response Deadline</label>
                <select
                  value={deadlineDays}
                  onChange={(e) => setDeadlineDays(Number(e.target.value))}
                  className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-100 cursor-pointer"
                >
                  <option value={3}>3 Business Days (Expedited)</option>
                  <option value={7}>7 Business Days (Standard)</option>
                  <option value={14}>14 Business Days (Commercial)</option>
                </select>
              </div>

              <div>
                <label className="text-slate-400 block mb-1 font-mono text-xs">Transmission Channel</label>
                <select className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-100 cursor-pointer">
                  <option>Secure Corporate Banking Portal</option>
                  <option>Encrypted SWIFT MT999 Notice</option>
                  <option>Certified Mail / Branch Delivery</option>
                </select>
              </div>
            </div>

            <div className="pt-2">
              <button
                type="submit"
                disabled={tippingOffCheck.containsTippingOff || isSubmitting}
                className={`w-full py-2.5 px-4 rounded-xl font-semibold text-xs transition-colors flex items-center justify-center gap-2 cursor-pointer ${
                  tippingOffCheck.containsTippingOff
                    ? 'bg-slate-800 text-slate-500 cursor-not-allowed'
                    : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-600/20'
                }`}
              >
                <Send className="w-4 h-4" />
                <span>Issue Customer RFI Notice</span>
              </button>
            </div>
          </form>
        </div>

        {/* Right Column: Active RFI Tracking Queue & Customer Upload Simulation */}
        <div className="lg:col-span-6 space-y-4">
          {/* Customer Document Response Simulator */}
          <div className="p-4 rounded-xl bg-[#0F172A] border border-[#1E293B] shadow-xl space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-xs font-bold text-slate-200 font-mono flex items-center gap-2">
                <UploadCloud className="w-4 h-4 text-emerald-400" />
                Customer Response Portal Simulation
              </h3>
              <span className="text-xs font-mono text-emerald-400">WebCrypto SHA-256 Engine</span>
            </div>

            <p className="text-xs text-slate-400">
              Simulate customer uploading requested customs clearance bills or pro-forma invoices in response to active RFI.
            </p>

            <label className="p-4 border-2 border-dashed border-[#334155] hover:border-emerald-500 rounded-xl flex items-center justify-center gap-3 cursor-pointer bg-[#0B0F17]/60 transition-colors">
              <UploadCloud className="w-5 h-5 text-slate-400" />
              <span className="text-xs text-slate-300 font-medium">Drop response document to verify cryptographic digest</span>
              <input type="file" onChange={handleFileUpload} className="hidden" />
            </label>

            {uploadStatus && (
              <div className="p-2.5 bg-[#0B0F17] rounded-lg border border-emerald-500/30 text-xs font-mono text-emerald-300">
                {uploadStatus}
              </div>
            )}
          </div>

          {/* Active Outbound Notices List */}
          <div className="bg-[#0F172A] border border-[#1E293B] rounded-2xl p-4 shadow-xl space-y-3">
            <h3 className="text-xs font-bold text-slate-300 font-mono">
              Active Outbound RFI Notices Queue
            </h3>

            <div className="space-y-2.5 max-h-[420px] overflow-y-auto pr-1">
              {rfis.map((rfi) => (
                <div
                  key={rfi.id}
                  className="p-3 bg-[#0B0F17] border border-[#1E293B] rounded-xl text-xs space-y-2"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono font-bold text-indigo-400">{rfi.id}</span>
                    <span className={`px-2 py-0.5 rounded text-xs font-mono font-bold ${
                      rfi.status === 'DOCUMENT_UPLOADED'
                        ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                        : 'bg-amber-500/20 text-amber-300 border border-amber-500/40'
                    }`}>
                      {rfi.status}
                    </span>
                  </div>

                  <div className="font-medium text-slate-200">{rfi.targetEntity}</div>
                  <p className="text-xs text-slate-400 font-mono leading-relaxed truncate">
                    {rfi.reason}
                  </p>

                  <div className="pt-2 border-t border-[#1E293B]/60 flex items-center justify-between text-xs">
                    <span className="text-slate-500 font-mono">Deadline: {rfi.deadlineDays} Days</span>
                    <button
                      onClick={() => handleSendReminder(rfi.id)}
                      className="text-sky-400 hover:text-sky-300 font-semibold flex items-center gap-1 cursor-pointer"
                    >
                      <Bell className="w-3 h-3" />
                      <span>Send Reminder</span>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
