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
  Calendar
} from 'lucide-react';
import { scanTextForTippingOff } from '@/lib/compliance/tippingOff';
import { SEEDED_RFI_REQUESTS } from '@/lib/seedData';
import { PiiText } from '@/components/ui/PiiText';

export default function RfiHubPage() {
  const [rfis, setRfis] = useState(SEEDED_RFI_REQUESTS);
  
  // New RFI Form State
  const [targetEntity, setTargetEntity] = useState('Meghna Industrial & Agro Processing Ltd');
  const [targetAccount, setTargetAccount] = useState('BD22-EBLB-4829-1092-8823');
  const [rfiReason, setRfiReason] = useState('Routine institutional documentation refresh for LC-2026-CTG-88912 commercial invoice verification.');
  const [deadlineDays, setDeadlineDays] = useState(7);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);

  // Live anti-tipping-off check
  const tippingOffCheck = scanTextForTippingOff(rfiReason);

  const handleCreateRfi = async () => {
    if (tippingOffCheck.containsTippingOff) {
      alert('CANNOT ISSUE RFI: Statutory Anti-Tipping-Off Violation detected.');
      return;
    }

    setIsSubmitting(true);
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
          requiredDocuments: ['Customs Bill of Entry', 'Supplier Commercial Invoice']
        })
      });
      const data = await res.json();
      if (data.success) {
        setRfis([data.rfi, ...rfis]);
        alert(`RFI ${data.rfi.id} created successfully with 0 tipping-off violations.`);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploadStatus('Computing client SHA-256 hash...');
    const buffer = await file.arrayBuffer();
    const hashBuffer = await crypto.subtle.digest('SHA-256', buffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const clientSha256 = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');

    setUploadStatus(`Uploading & verifying digital signature (${file.name})...`);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('rfiId', 'RFI-2026-0042');
    formData.append('clientSha256', clientSha256);

    try {
      const res = await fetch('/api/v1/rfi/upload', {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      if (data.success) {
        setUploadStatus(`Uploaded & Verified! SHA-256: ${data.sha256.slice(0, 16)}...`);
      }
    } catch (err) {
      setUploadStatus('Upload failed.');
    }
  };

  return (
    <div className="p-6 max-w-[1700px] mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2">
          <MailQuestion className="w-5 h-5 text-indigo-400" />
          Compliance Request for Information (RFI) Hub
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Secure information requests with automated statutory Anti-Tipping-Off filtering under 31 U.S.C. § 5318(g)(2) and MLPA 2012 § 6.
        </p>
      </div>

      {/* Mandatory Statutory Anti-Tipping-Off Warning Banner */}
      <div className="p-4 bg-amber-950/30 border border-amber-800/50 rounded-xl flex items-start gap-3.5 text-xs text-amber-200">
        <ShieldAlert className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
        <div>
          <h3 className="font-bold text-amber-300 uppercase tracking-wide">
            Statutory Anti-Tipping-Off Safeguard (31 U.S.C. § 5318(g)(2) & MLPA 2012 § 6)
          </h3>
          <p className="mt-1 text-slate-300 leading-relaxed">
            Financial institutions, officers, and employees are prohibited by law from disclosing to any person involved in a transaction that the transaction has been reported or that an AML/SAR investigation is underway. All RFI inquiries must strictly use neutral commercial audit language.
          </p>
        </div>
      </div>

      {/* Grid: Create New RFI & Active Requests */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Create RFI (5 Cols) */}
        <div className="lg:col-span-5 bg-[#0F172A] border border-[#1E293B] rounded-xl p-5 space-y-4">
          <h2 className="text-sm font-semibold text-slate-100 flex items-center gap-2 pb-2 border-b border-[#1E293B]">
            <Plus className="w-4 h-4 text-emerald-400" />
            Issue New Information Request
          </h2>

          <div className="space-y-3 text-xs">
            <div>
              <label className="block text-slate-400 mb-1 font-medium">Target Entity</label>
              <input
                type="text"
                value={targetEntity}
                onChange={(e) => setTargetEntity(e.target.value)}
                className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-100 focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div>
              <label className="block text-slate-400 mb-1 font-medium">Account Number</label>
              <input
                type="text"
                value={targetAccount}
                onChange={(e) => setTargetAccount(e.target.value)}
                className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-100 focus:outline-none focus:border-indigo-500 font-mono"
              />
            </div>

            <div>
              <label className="block text-slate-400 mb-1 font-medium">Customer Inquiry Narrative (Scanned in Real Time)</label>
              <textarea
                value={rfiReason}
                onChange={(e) => setRfiReason(e.target.value)}
                rows={4}
                className="w-full p-3 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-200 focus:outline-none focus:border-indigo-500 leading-relaxed text-xs"
              />

              {/* Tipping Off Real-Time Validation Feedback */}
              {tippingOffCheck.containsTippingOff ? (
                <div className="mt-2 p-2.5 bg-rose-950/40 border border-rose-800/60 rounded-lg text-rose-300 text-[11px] flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-rose-500 shrink-0" />
                  <span>
                    <strong>Blocked:</strong> Contains prohibited term &quot;{tippingOffCheck.matchedPhrases.join(', ')}&quot;. Cannot disclose AML/SAR suspicion.
                  </span>
                </div>
              ) : (
                <div className="mt-2 p-2 bg-emerald-950/20 border border-emerald-900/40 rounded-lg text-emerald-300 text-[11px] flex items-center gap-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                  <span>Verified Safe: 0 statutory tipping-off terms detected.</span>
                </div>
              )}
            </div>

            <div>
              <label className="block text-slate-400 mb-1 font-medium">Response Deadline (Days)</label>
              <select
                value={deadlineDays}
                onChange={(e) => setDeadlineDays(Number(e.target.value))}
                className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-200 focus:outline-none focus:border-indigo-500"
              >
                <option value={3}>3 Business Days (Expedited)</option>
                <option value={7}>7 Business Days (Standard)</option>
                <option value={14}>14 Business Days (Complex Trade)</option>
              </select>
            </div>

            <button
              onClick={handleCreateRfi}
              disabled={isSubmitting || tippingOffCheck.containsTippingOff}
              className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-slate-100 font-bold rounded-lg uppercase tracking-wide text-xs transition-all shadow-md flex items-center justify-center gap-2 mt-2"
            >
              <MailQuestion className="w-4 h-4" />
              <span>Dispatch Secure Customer RFI</span>
            </button>
          </div>
        </div>

        {/* Right Column: Active RFI Ledger & Upload Zone (7 Cols) */}
        <div className="lg:col-span-7 space-y-6">
          {/* Client-Side Document Upload Zone */}
          <div className="p-5 bg-[#0F172A] border border-dashed border-[#334155] rounded-xl text-center space-y-3">
            <UploadCloud className="w-8 h-8 text-indigo-400 mx-auto" />
            <div>
              <h3 className="font-semibold text-sm text-slate-200">
                Incoming Customer Document Verification Portal
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Upload customer documentation. WebCrypto calculates client-side SHA-256 for FRE 902(11) evidentiary integrity.
              </p>
            </div>

            <label className="inline-block cursor-pointer px-4 py-2 bg-[#1E293B] hover:bg-[#334155] text-slate-200 rounded-lg text-xs font-semibold transition-colors">
              <span>Select File to Ingest & Verify</span>
              <input type="file" onChange={handleFileUpload} className="hidden" />
            </label>

            {uploadStatus && (
              <div className="text-xs font-mono text-emerald-400 bg-[#0B0F17] p-2 rounded border border-[#1E293B]">
                {uploadStatus}
              </div>
            )}
          </div>

          {/* RFI Requests List */}
          <div className="bg-[#0F172A] border border-[#1E293B] rounded-xl overflow-hidden">
            <div className="p-3.5 bg-[#0B0F17] border-b border-[#1E293B] flex items-center justify-between">
              <h3 className="text-sm font-semibold text-slate-200">
                Active Regulatory RFI Tracking Ledger
              </h3>
              <span className="text-xs text-slate-400 font-mono">{rfis.length} Active Records</span>
            </div>

            <div className="divide-y divide-[#1E293B]">
              {rfis.map((rfi) => (
                <div key={rfi.id} className="p-4 hover:bg-[#1E293B]/40 transition-colors text-xs space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-bold text-slate-200">{rfi.id}</span>
                      <span className="text-[10px] text-slate-500 font-mono">[{rfi.caseId}]</span>
                    </div>
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">
                      {rfi.status}
                    </span>
                  </div>

                  <div className="font-medium text-slate-100 flex items-center gap-1.5">
                    <Building className="w-3.5 h-3.5 text-slate-400" />
                    <span>{rfi.targetEntity}</span>
                  </div>

                  <p className="text-slate-300 bg-[#0B0F17] p-2 rounded border border-[#1E293B]">
                    {rfi.subject}
                  </p>

                  <div className="flex items-center justify-between text-[11px] text-slate-400 pt-1">
                    <span>Deadline: {rfi.dueDate}</span>
                    <span className="text-indigo-400 font-semibold cursor-pointer hover:underline">
                      Required Documents ({rfi.requiredDocs?.length || 0})
                    </span>
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
