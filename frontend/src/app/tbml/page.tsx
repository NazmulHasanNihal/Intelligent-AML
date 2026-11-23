'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import {
  Ship,
  FileCheck,
  AlertTriangle,
  UploadCloud,
  CheckCircle2,
  FileText,
  Lock,
  ArrowRight,
  TrendingUp,
  MapPin,
  ExternalLink,
  ShieldAlert,
  Copy,
  Check
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { computeFileSha256 } from '@/lib/audit/hashChain';
import { formatCurrencyByJurisdiction } from '@/lib/compliance/jurisdictions';

export default function TradeFinanceTbmlPage() {
  const { jurisdiction, setFourEyesModalOpen, addAuditEntry } = useBankingStore();

  const [activeTab, setActiveTab] = useState<'PACKET_VIEW' | 'PRICE_BENCHMARK' | 'VESSEL_TRACKING'>('PACKET_VIEW');
  const [uploadedFileHash, setUploadedFileHash] = useState<string | null>(null);
  const [uploadedFileName, setUploadedFileName] = useState<string | null>(null);
  const [isHashing, setIsHashing] = useState(false);
  const [isPinned, setIsPinned] = useState(false);
  const [copiedHash, setCopiedHash] = useState(false);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsHashing(true);
    setUploadedFileName(file.name);
    try {
      const buffer = await file.arrayBuffer();
      const hash = await computeFileSha256(buffer);
      setUploadedFileHash(hash);
      addAuditEntry({
        eventType: 'DOCUMENT_UPLOADED',
        entityId: 'TBML-PKG-2026-0881',
        details: `Uploaded trade document ${file.name} with verified SHA-256 digest: ${hash}`,
        actionBy: 'Amina Rahman, CFE (Lead Investigator)'
      });
    } catch (err) {
      console.error('Failed to hash file:', err);
    } finally {
      setIsHashing(false);
    }
  };

  const handlePinReport = () => {
    setIsPinned(true);
    addAuditEntry({
      eventType: 'CASE_ESCALATED',
      entityId: 'CASE-2026-0881',
      details: 'Trade-Based Money Laundering (TBML) Over-Invoicing Dossier pinned to active institutional case and regulatory SAR draft.',
      actionBy: 'Amina Rahman, CFE (Lead Investigator)'
    });
  };

  return (
    <div className="p-4 sm:p-5 lg:p-6 max-w-[1750px] mx-auto space-y-5">
      {/* Page Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2 font-sans">
            <Ship className="w-5 h-5 text-sky-400" />
            Trade Finance &amp; TBML Document Cross-Check
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Automated multi-document reconciliation: SWIFT MT700 Documentary Credit vs Commercial Invoice vs ASYCUDA World Customs Bill of Entry.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Link
            href="/cases/CASE-2026-0881"
            className="px-3 py-1.5 rounded-lg bg-[#0F172A] hover:bg-[#1E293B] border border-[#334155] text-xs font-semibold text-slate-200 transition-colors flex items-center gap-1.5"
          >
            <span>Linked Case: CASE-2026-0881</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>

      {/* Main Split-Screen Workspace */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Left Column: Trade Packet Navigation & Price Variance */}
        <div className="lg:col-span-8 space-y-4">
          {/* Sub-Tabs */}
          <div className="flex items-center gap-2 pb-2 border-b border-[#1E293B]">
            <button
              onClick={() => setActiveTab('PACKET_VIEW')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer ${
                activeTab === 'PACKET_VIEW'
                  ? 'bg-sky-500/20 text-sky-300 border border-sky-500/40'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Document Packet Decomposition
            </button>
            <button
              onClick={() => setActiveTab('PRICE_BENCHMARK')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer ${
                activeTab === 'PRICE_BENCHMARK'
                  ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              ASYCUDA World Price Benchmark (+333.7%)
            </button>
            <button
              onClick={() => setActiveTab('VESSEL_TRACKING')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer ${
                activeTab === 'VESSEL_TRACKING'
                  ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              AIS Vessel Route Tracking
            </button>
          </div>

          {/* Packet Decomposition View */}
          {activeTab === 'PACKET_VIEW' && (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Document 1: SWIFT MT700 */}
                <div className="p-4 rounded-xl bg-[#0F172A] border border-[#1E293B] space-y-3">
                  <div className="flex items-center justify-between pb-2 border-b border-[#1E293B]">
                    <span className="font-mono text-xs font-bold text-sky-400">1. SWIFT MT700 Documentary Credit</span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300">ISSUED</span>
                  </div>
                  <div className="space-y-1.5 text-xs font-mono text-slate-300">
                    <div>:20: Doc Credit Number: <strong className="text-white">LC-CTG-2026-9921</strong></div>
                    <div>:31D: Date of Expiry: <span className="text-slate-400">2026-10-31</span></div>
                    <div>:32A: Amount: <strong className="text-emerald-400">$945,000.00 USD</strong></div>
                    <div>:50: Applicant: <span className="text-slate-200">Meghna Industrial &amp; Agro Ltd</span></div>
                    <div>:59: Beneficiary: <span className="text-slate-200">Gulf Star Commodities FZE (JAFZA)</span></div>
                    <div>:45A: Goods Description: <span className="text-slate-300">100,000 KG Combed Cotton Yarn 30/1</span></div>
                  </div>
                </div>

                {/* Document 2: Commercial Invoice */}
                <div className="p-4 rounded-xl bg-[#0F172A] border border-[#1E293B] space-y-3">
                  <div className="flex items-center justify-between pb-2 border-b border-[#1E293B]">
                    <span className="font-mono text-xs font-bold text-amber-400">2. Commercial Invoice #INV-8812</span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-500/20 text-amber-300">PRICE DISCREPANCY</span>
                  </div>
                  <div className="space-y-1.5 text-xs font-mono text-slate-300">
                    <div>Invoice Date: <span className="text-slate-400">2026-09-01</span></div>
                    <div>Quantity: <strong className="text-white">100,000 KG</strong></div>
                    <div>Invoiced Unit Price: <strong className="text-rose-400">$9.45 / KG</strong></div>
                    <div>Total Invoiced Value: <strong className="text-rose-400">$945,000.00 USD</strong></div>
                    <div>Terms: <span className="text-slate-300">CIF Chittagong Port</span></div>
                    <div>Country of Origin: <span className="text-slate-300">United Arab Emirates</span></div>
                  </div>
                </div>
              </div>

              {/* Document 3: ASYCUDA World Bill of Entry */}
              <div className="p-4 rounded-xl bg-[#0F172A] border border-[#1E293B] space-y-3">
                <div className="flex items-center justify-between pb-2 border-b border-[#1E293B]">
                  <span className="font-mono text-xs font-bold text-rose-400">
                    3. ASYCUDA World Customs Declaration (Chittagong Custom House)
                  </span>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/40">
                    FLAGGED BY CUSTOMS INTELLIGENCE
                  </span>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs font-mono">
                  <div className="p-2.5 bg-[#0B0F17] rounded-lg">
                    <span className="text-slate-500 text-[10px] block">Bill of Entry No</span>
                    <span className="font-bold text-white">C-1882910</span>
                  </div>
                  <div className="p-2.5 bg-[#0B0F17] rounded-lg">
                    <span className="text-slate-500 text-[10px] block">HS Tariff Code</span>
                    <span className="font-bold text-white">5205.12.00 (Single Cotton Yarn)</span>
                  </div>
                  <div className="p-2.5 bg-[#0B0F17] rounded-lg">
                    <span className="text-slate-500 text-[10px] block">Official Assessment Value</span>
                    <span className="font-bold text-amber-400">$218,000.00 USD</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Price Benchmark Comparison */}
          {activeTab === 'PRICE_BENCHMARK' && (
            <div className="p-5 rounded-2xl bg-[#0F172A] border border-[#1E293B] space-y-4">
              <div>
                <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2 font-mono">
                  <AlertTriangle className="w-4 h-4 text-rose-500" />
                  ASYCUDA World Global Trade Tariff Divergence Analysis
                </h3>
                <p className="text-xs text-slate-400 mt-1">
                  Comparing declared LC unit price against historical 90-day moving average from National Customs Database (ASYCUDA World).
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
                <div className="p-4 rounded-xl bg-[#0B0F17] border border-[#1E293B] text-center">
                  <span className="text-[10px] font-mono uppercase text-slate-500 block">Declared LC Invoice Price</span>
                  <span className="text-2xl font-mono font-bold text-rose-400 mt-1 block">$9.45 / KG</span>
                  <span className="text-xs text-slate-400">Total: $945,000.00 USD</span>
                </div>

                <div className="p-4 rounded-xl bg-[#0B0F17] border border-[#1E293B] text-center">
                  <span className="text-[10px] font-mono uppercase text-slate-500 block">ASYCUDA Market Fair Value</span>
                  <span className="text-2xl font-mono font-bold text-emerald-400 mt-1 block">$2.18 / KG</span>
                  <span className="text-xs text-slate-400">Total: $218,000.00 USD</span>
                </div>

                <div className="p-4 rounded-xl bg-[#0B0F17] border border-rose-500/40 text-center">
                  <span className="text-[10px] font-mono uppercase text-slate-500 block">Capital Outflow Divergence</span>
                  <span className="text-2xl font-mono font-bold text-rose-500 mt-1 block">+333.7%</span>
                  <span className="text-xs text-rose-300 font-semibold font-mono">+$727,000.00 Illicit Flight</span>
                </div>
              </div>

              <div className="p-3 bg-rose-950/20 border border-rose-800/40 rounded-xl text-xs text-rose-300 flex items-start gap-2.5">
                <ShieldAlert className="w-4 h-4 shrink-0 mt-0.5 text-rose-400" />
                <div className="space-y-1">
                  <span>
                    <strong>BFIU TBML Guidelines &amp; MLPA 2012 § 25 Alert:</strong> Over-invoicing exceeds trade surveillance variance ceiling (&gt; 50%). Capital siphoning to JAFZA offshore entity indicated. Automated STR filing to Bangladesh Bank BFIU mandatory within 24 hours.
                  </span>
                  <div className="text-[11px] text-slate-400 flex items-center gap-1.5 pt-0.5">
                    <span>Statutory Reference: BFIU Guidelines for Prevention of Trade Based Money Laundering (2019)</span>
                    <a
                      href="https://www.bb.org.bd/en/index.php/bfiu/publication"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-cyan-400 hover:text-cyan-300 inline-flex items-center gap-0.5"
                    >
                      <span>BFIU Publication</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* AIS Vessel Tracking */}
          {activeTab === 'VESSEL_TRACKING' && (
            <div className="p-5 rounded-2xl bg-[#0F172A] border border-[#1E293B] space-y-4">
              <div>
                <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2 font-mono">
                  <MapPin className="w-4 h-4 text-amber-400" />
                  Automated AIS Vessel Trajectory &amp; Port Divergence Audit
                </h3>
                <p className="text-xs text-slate-400 mt-1">
                  Vessel: <strong className="text-slate-200">MV Arabian Pearl (IMO 9481920)</strong> • Flag: Panama
                </p>
              </div>

              <div className="space-y-3 font-mono text-xs">
                <div className="p-3 bg-[#0B0F17] rounded-xl border border-[#1E293B] flex items-center justify-between">
                  <span className="text-slate-400">Port of Loading (B/L):</span>
                  <strong className="text-slate-100">Chittagong Port (BDCGP) — Departed 2026-08-28</strong>
                </div>
                <div className="p-3 bg-[#0B0F17] rounded-xl border border-[#1E293B] flex items-center justify-between">
                  <span className="text-slate-400">Declared Port of Discharge (B/L):</span>
                  <strong className="text-slate-100">Port Klang, Malaysia (MYPKG)</strong>
                </div>
                <div className="p-3 bg-[#0B0F17] rounded-xl border border-rose-500/40 flex items-center justify-between">
                  <span className="text-rose-400 font-bold">Actual AIS Telemetry Discharge:</span>
                  <strong className="text-rose-400 font-bold">Jebel Ali / Dubai, UAE (AEJEA) — Diverted</strong>
                </div>
              </div>

              <div className="p-3 bg-amber-950/20 border border-amber-800/40 rounded-xl text-xs text-amber-300">
                <strong>Anomalous Transshipment:</strong> AIS satellite transponder tracking confirms the vessel never called at Port Klang. Cargo discharged directly into JAFZA free-trade zone without customs duty or re-export documentation.
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Evidence Drag-and-Drop & WORM Anchor Actions */}
        <div className="lg:col-span-4 bg-[#0F172A] border border-[#1E293B] rounded-2xl p-5 shadow-2xl flex flex-col justify-between space-y-6">
          <div className="space-y-5">
            <div>
              <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2 font-mono">
                <UploadCloud className="w-4 h-4 text-sky-400" />
                Cryptographic Evidence Ingestion
              </h3>
              <p className="text-xs text-slate-400 mt-1">
                Upload supplemental bills of lading, phytosanitary certificates, or port manifests. Instant client-side WebCrypto SHA-256 calculation.
              </p>
            </div>

            {/* Upload Zone */}
            <label className="p-6 border-2 border-dashed border-[#334155] hover:border-sky-500 rounded-xl flex flex-col items-center justify-center gap-2 cursor-pointer transition-colors bg-[#0B0F17]/50">
              <UploadCloud className="w-8 h-8 text-slate-500" />
              <span className="text-xs font-semibold text-slate-300">
                {isHashing ? 'Computing SHA-256 Digest...' : 'Select or Drop Trade Document'}
              </span>
              <span className="text-[10px] text-slate-500">PDF, XML, or TIFF up to 25MB</span>
              <input
                type="file"
                onChange={handleFileUpload}
                disabled={isHashing}
                className="hidden"
                accept=".pdf,.xml,.tiff,.png"
              />
            </label>

            {/* Uploaded File Hash Display */}
            {uploadedFileHash && (
              <div className="p-3 bg-[#0B0F17] border border-emerald-500/40 rounded-xl space-y-1.5 text-xs font-mono">
                <div className="flex items-center justify-between text-emerald-400 font-bold">
                  <span>{uploadedFileName}</span>
                  <CheckCircle2 className="w-4 h-4" />
                </div>
                <div className="text-[10px] text-slate-400 break-all">
                  SHA-256: <span className="text-slate-200">{uploadedFileHash}</span>
                </div>
              </div>
            )}

            {/* Audit Status */}
            <div className="space-y-2 text-xs">
              <div className="p-3 bg-[#0B0F17] rounded-xl border border-[#1E293B] flex items-center justify-between">
                <span className="text-slate-400">Verified Evidence Count:</span>
                <strong className="font-mono text-emerald-400">4 Items Anchored</strong>
              </div>
              <div className="p-3 bg-[#0B0F17] rounded-xl border border-[#1E293B] flex items-center justify-between">
                <span className="text-slate-400">FRE 902(11) Self-Authentication:</span>
                <strong className="font-mono text-emerald-400">COMPLIANT</strong>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="pt-4 border-t border-[#1E293B] space-y-2.5">
            <button
              onClick={handlePinReport}
              disabled={isPinned}
              className={`w-full py-2.5 px-4 rounded-xl font-semibold text-xs transition-colors flex items-center justify-center gap-2 cursor-pointer ${
                isPinned
                  ? 'bg-emerald-950 text-emerald-300 border border-emerald-800'
                  : 'bg-sky-600 hover:bg-sky-500 text-white shadow-lg shadow-sky-600/20'
              }`}
            >
              <FileCheck className="w-4 h-4" />
              <span>{isPinned ? 'TBML Report Pinned to Case & SAR' : 'Pin Verified TBML Report to Case'}</span>
            </button>

            <Link
              href="/sar?caseId=CASE-2026-0881"
              className="w-full py-2.5 px-4 rounded-xl bg-[#1E293B] hover:bg-[#334155] text-slate-200 font-medium text-xs transition-colors flex items-center justify-center gap-2"
            >
              <FileText className="w-4 h-4 text-purple-400" />
              <span>Proceed to Regulatory SAR Filing</span>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
