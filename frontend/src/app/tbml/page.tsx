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
import { formatCurrencyByJurisdiction, JURISDICTIONS } from '@/lib/compliance/jurisdictions';

const TBML_LC_PRESETS = [
  {
    lcNumber: 'LC-CTG-2026-9921',
    applicant: 'Meghna Industrial & Agro Ltd',
    beneficiary: 'Gulf Star Commodities FZE (JAFZA)',
    goods: 'Combed Cotton Yarn 30/1',
    hsCode: '5205.12.00',
    quantity: 100000,
    unitPrice: 9.45,
    benchmarkPrice: 2.18,
    billOfEntry: 'C-1882910'
  },
  {
    lcNumber: 'LC-DHK-2026-4410',
    applicant: 'Padma Textile Mills PLC',
    beneficiary: 'Sino-Apex Fiber Trading (HK)',
    goods: 'Polyester Filament Yarn DTY',
    hsCode: '5402.33.00',
    quantity: 80000,
    unitPrice: 4.90,
    benchmarkPrice: 1.65,
    billOfEntry: 'C-1904112'
  },
  {
    lcNumber: 'LC-BEN-2026-7102',
    applicant: 'Karnaphuli Heavy Eng. Ltd',
    beneficiary: 'Emirates Alloy Brokers LLC',
    goods: 'Cold-Rolled Steel Coils',
    hsCode: '7209.16.00',
    quantity: 250000,
    unitPrice: 1.85,
    benchmarkPrice: 0.78,
    billOfEntry: 'C-1910544'
  }
];

export default function TradeFinanceTbmlPage() {
  const { jurisdiction, setFourEyesModalOpen, addAuditEntry } = useBankingStore();

  const [activeTab, setActiveTab] = useState<'PACKET_VIEW' | 'PRICE_BENCHMARK' | 'VESSEL_TRACKING'>('PACKET_VIEW');
  const [selectedPresetIdx, setSelectedPresetIdx] = useState(0);
  const preset = TBML_LC_PRESETS[selectedPresetIdx] ?? TBML_LC_PRESETS[0]!;
  const [declaredUnitPrice, setDeclaredUnitPrice] = useState<number>(preset.unitPrice);
  const [asycudaUnitPrice, setAsycudaUnitPrice] = useState<number>(preset.benchmarkPrice);
  const [declaredQuantityKg, setDeclaredQuantityKg] = useState<number>(preset.quantity);
  const [verifiedCount, setVerifiedCount] = useState<number>(4);

  const [uploadedFileHash, setUploadedFileHash] = useState<string | null>(null);
  const [uploadedFileName, setUploadedFileName] = useState<string | null>(null);
  const [isHashing, setIsHashing] = useState(false);
  const [isPinned, setIsPinned] = useState(false);
  const [copiedHash, setCopiedHash] = useState(false);

  const declaredTotal = declaredUnitPrice * declaredQuantityKg;
  const asycudaTotal = asycudaUnitPrice * declaredQuantityKg;
  const illicitCapitalGap = declaredTotal - asycudaTotal;
  const divergencePct = asycudaUnitPrice > 0 ? ((declaredUnitPrice - asycudaUnitPrice) / asycudaUnitPrice) * 100 : 0;

  const handleSelectPreset = (idx: number) => {
    const p = TBML_LC_PRESETS[idx];
    if (!p) return;
    setSelectedPresetIdx(idx);
    setDeclaredUnitPrice(p.unitPrice);
    setAsycudaUnitPrice(p.benchmarkPrice);
    setDeclaredQuantityKg(p.quantity);
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsHashing(true);
    setUploadedFileName(file.name);
    try {
      const buffer = await file.arrayBuffer();
      const clientHash = await computeFileSha256(buffer);
      let verifiedHash = clientHash;

      try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('rfiId', `TBML-${preset.lcNumber}`);
        formData.append('clientSha256', clientHash);
        const res = await fetch('/api/v1/rfi/upload', { method: 'POST', body: formData });
        if (res.ok) {
          const data = await res.json();
          if (data?.sha256) verifiedHash = data.sha256;
        }
      } catch {
        // Retain client WebCrypto digest fallback
      }

      setUploadedFileHash(verifiedHash);
      setVerifiedCount((c) => c + 1);
      addAuditEntry({
        eventType: 'DOCUMENT_UPLOADED',
        entityId: `TBML-${preset.lcNumber}`,
        details: `Uploaded trade document ${file.name} with verified SHA-256 digest: ${verifiedHash}`,
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
      details: `TBML variance dossier (${preset.lcNumber}, +${divergencePct.toFixed(1)}% divergence) pinned to active institutional case.`,
      actionBy: 'Amina Rahman, CFE (Lead Investigator)'
    });
  };

  return (
    <div className="p-4 sm:p-5 lg:p-6 max-w-[1750px] mx-auto space-y-5">
      {/* Page Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-fg flex items-center gap-2 font-sans">
            <Ship className="w-5 h-5 text-accent-2" />
            Trade Finance &amp; TBML Document Cross-Check
          </h1>
          <p className="text-xs text-muted mt-0.5">
            SWIFT MT700 vs Commercial Invoice vs ASYCUDA World Customs Bill of Entry.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <select
            aria-label="Select LC Shipment"
            value={selectedPresetIdx}
            onChange={(e) => handleSelectPreset(Number(e.target.value))}
            className="px-3 py-1.5 rounded-lg bg-panel border border-line-strong text-xs font-mono text-fg-secondary focus:outline-none focus:border-sky-500"
          >
            {TBML_LC_PRESETS.map((p, i) => (
              <option key={p.lcNumber} value={i}>
                {p.lcNumber} — {p.goods}
              </option>
            ))}
          </select>
          <Link
            href="/cases/CASE-2026-0881"
            className="px-3 py-1.5 rounded-lg bg-panel hover:bg-surface border border-line-strong text-xs font-semibold text-fg-secondary transition-colors flex items-center gap-1.5"
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
          <div className="flex items-center gap-2 pb-2 border-b border-line">
            <button
              onClick={() => setActiveTab('PACKET_VIEW')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer ${
                activeTab === 'PACKET_VIEW'
                  ? 'bg-sky-500/20 text-accent-2 border border-sky-500/40'
                  : 'text-muted hover:text-fg-secondary'
              }`}
            >
              Document Packet Decomposition
            </button>
            <button
              onClick={() => setActiveTab('PRICE_BENCHMARK')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer ${
                activeTab === 'PRICE_BENCHMARK'
                  ? 'bg-rose-500/20 text-tier-1-text border border-rose-500/40'
                  : 'text-muted hover:text-fg-secondary'
              }`}
            >
              ASYCUDA World Price Benchmark (+333.7%)
            </button>
            <button
              onClick={() => setActiveTab('VESSEL_TRACKING')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer ${
                activeTab === 'VESSEL_TRACKING'
                  ? 'bg-amber-500/20 text-tier-2-text border border-amber-500/40'
                  : 'text-muted hover:text-fg-secondary'
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
                <div className="p-4 rounded-xl bg-panel border border-line space-y-3">
                  <div className="flex items-center justify-between pb-2 border-b border-line">
                    <span className="font-mono text-xs font-bold text-accent-2">1. SWIFT MT700 Documentary Credit</span>
                    <span className="text-xs font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-tier-3-text">ISSUED</span>
                  </div>
                  <div className="space-y-1.5 text-xs font-mono text-fg-secondary">
                    <div>:20: Doc Credit Number: <strong className="text-white">{preset.lcNumber}</strong></div>
                    <div>:31D: Date of Expiry: <span className="text-muted">2026-10-31</span></div>
                    <div>:32A: Amount: <strong className="text-tier-3-text">${declaredTotal.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} USD</strong></div>
                    <div>:50: Applicant: <span className="text-fg-secondary">{preset.applicant}</span></div>
                    <div>:59: Beneficiary: <span className="text-fg-secondary">{preset.beneficiary}</span></div>
                    <div>:45A: Goods Description: <span className="text-fg-secondary">{declaredQuantityKg.toLocaleString()} KG {preset.goods}</span></div>
                  </div>
                </div>

                {/* Document 2: Commercial Invoice */}
                <div className="p-4 rounded-xl bg-panel border border-line space-y-3">
                  <div className="flex items-center justify-between pb-2 border-b border-line">
                    <span className="font-mono text-xs font-bold text-tier-2-text">2. Commercial Invoice #INV-8812</span>
                    <span className={`text-xs font-mono px-2 py-0.5 rounded ${Math.abs(divergencePct) >= 25 ? 'bg-amber-500/20 text-tier-2-text' : 'bg-emerald-500/20 text-tier-3-text'}`}>
                      {Math.abs(divergencePct) >= 25 ? 'PRICE DISCREPANCY' : 'WITHIN TOLERANCE'}
                    </span>
                  </div>
                  <div className="space-y-1.5 text-xs font-mono text-fg-secondary">
                    <div>Invoice Date: <span className="text-muted">2026-09-01</span></div>
                    <div>Quantity: <strong className="text-white">{declaredQuantityKg.toLocaleString()} KG</strong></div>
                    <div>Invoiced Unit Price: <strong className={divergencePct >= 25 ? 'text-tier-1-text' : 'text-tier-3-text'}>${declaredUnitPrice.toFixed(2)} / KG</strong></div>
                    <div>Total Invoiced Value: <strong className={divergencePct >= 25 ? 'text-tier-1-text' : 'text-tier-3-text'}>${declaredTotal.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} USD</strong></div>
                    <div>Terms: <span className="text-fg-secondary">CIF Chittagong Port</span></div>
                    <div>Country of Origin: <span className="text-fg-secondary">United Arab Emirates</span></div>
                  </div>
                </div>
              </div>

              {/* Document 3: ASYCUDA World Bill of Entry */}
              <div className="p-4 rounded-xl bg-panel border border-line space-y-3">
                <div className="flex items-center justify-between pb-2 border-b border-line">
                  <span className="font-mono text-xs font-bold text-tier-1-text">
                    3. ASYCUDA World Customs Declaration (Chittagong Custom House)
                  </span>
                  <span className="text-xs font-mono px-2 py-0.5 rounded bg-rose-500/20 text-tier-1-text border border-rose-500/40">
                    {Math.abs(divergencePct) >= 25 ? 'FLAGGED BY CUSTOMS INTELLIGENCE' : 'CUSTOMS BASELINE MATCHED'}
                  </span>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs font-mono">
                  <div className="p-2.5 bg-canvas rounded-lg">
                    <span className="text-fg0 text-xs block">Bill of Entry No</span>
                    <span className="font-bold text-white">{preset.billOfEntry}</span>
                  </div>
                  <div className="p-2.5 bg-canvas rounded-lg">
                    <span className="text-fg0 text-xs block">HS Tariff Code</span>
                    <span className="font-bold text-white">{preset.hsCode} ({preset.goods})</span>
                  </div>
                  <div className="p-2.5 bg-canvas rounded-lg">
                    <span className="text-fg0 text-xs block">Official Assessment Value</span>
                    <span className="font-bold text-tier-2-text">${asycudaTotal.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} USD</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Price Benchmark Comparison */}
          {activeTab === 'PRICE_BENCHMARK' && (
            <div className="p-5 rounded-2xl bg-panel border border-line space-y-4">
              <div>
                <h3 className="text-sm font-bold text-fg flex items-center gap-2 font-mono">
                  <AlertTriangle className="w-4 h-4 text-rose-500" />
                  ASYCUDA World Global Trade Tariff Divergence Calculator
                </h3>
                <p className="text-xs text-muted mt-1">
                  Adjust declared invoice unit price, shipment weight, or ASYCUDA reference benchmark to test capital flight divergence in real time.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs font-mono">
                <label className="p-3 rounded-xl bg-canvas border border-line space-y-1 block">
                  <span className="text-[10px] text-muted uppercase block">Declared Unit Price ($/KG)</span>
                  <input
                    type="number"
                    step="0.05"
                    min="0.01"
                    value={declaredUnitPrice}
                    onChange={(e) => setDeclaredUnitPrice(Math.max(0.01, parseFloat(e.target.value) || 0.01))}
                    className="w-full bg-panel border border-line-strong rounded-lg px-2.5 py-1.5 text-tier-1-text font-bold focus:outline-none focus:border-sky-500"
                  />
                </label>
                <label className="p-3 rounded-xl bg-canvas border border-line space-y-1 block">
                  <span className="text-[10px] text-muted uppercase block">ASYCUDA Benchmark ($/KG)</span>
                  <input
                    type="number"
                    step="0.05"
                    min="0.01"
                    value={asycudaUnitPrice}
                    onChange={(e) => setAsycudaUnitPrice(Math.max(0.01, parseFloat(e.target.value) || 0.01))}
                    className="w-full bg-panel border border-line-strong rounded-lg px-2.5 py-1.5 text-tier-3-text font-bold focus:outline-none focus:border-sky-500"
                  />
                </label>
                <label className="p-3 rounded-xl bg-canvas border border-line space-y-1 block">
                  <span className="text-[10px] text-muted uppercase block">Quantity (KG)</span>
                  <input
                    type="number"
                    step="1000"
                    min="100"
                    value={declaredQuantityKg}
                    onChange={(e) => setDeclaredQuantityKg(Math.max(100, parseInt(e.target.value, 10) || 100))}
                    className="w-full bg-panel border border-line-strong rounded-lg px-2.5 py-1.5 text-fg font-bold focus:outline-none focus:border-sky-500"
                  />
                </label>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-1">
                <div className="p-4 rounded-xl bg-canvas border border-line text-center">
                  <span className="text-xs font-mono uppercase text-fg0 block">Declared LC Invoice Price</span>
                  <span className="text-2xl font-mono font-bold text-tier-1-text mt-1 block">${declaredUnitPrice.toFixed(2)} / KG</span>
                  <span className="text-xs text-muted">Total: ${declaredTotal.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} USD</span>
                </div>

                <div className="p-4 rounded-xl bg-canvas border border-line text-center">
                  <span className="text-xs font-mono uppercase text-fg0 block">ASYCUDA Market Fair Value</span>
                  <span className="text-2xl font-mono font-bold text-tier-3-text mt-1 block">${asycudaUnitPrice.toFixed(2)} / KG</span>
                  <span className="text-xs text-muted">Total: ${asycudaTotal.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} USD</span>
                </div>

                <div className={`p-4 rounded-xl bg-canvas border text-center ${Math.abs(divergencePct) >= 25 ? 'border-rose-500/40' : 'border-emerald-500/40'}`}>
                  <span className="text-xs font-mono uppercase text-fg0 block">Capital Outflow Divergence</span>
                  <span className={`text-2xl font-mono font-bold mt-1 block ${Math.abs(divergencePct) >= 25 ? 'text-rose-500' : 'text-tier-3-text'}`}>
                    {divergencePct >= 0 ? '+' : ''}{divergencePct.toFixed(1)}%
                  </span>
                  <span className={`text-xs font-semibold font-mono ${Math.abs(divergencePct) >= 25 ? 'text-tier-1-text' : 'text-tier-3-text'}`}>
                    {illicitCapitalGap >= 0 ? '+' : ''}${illicitCapitalGap.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} Delta
                  </span>
                </div>
              </div>

              <div className="p-3 bg-tier-1-bg border border-rose-800/40 rounded-xl text-xs text-tier-1-text flex items-start gap-2.5">
                <ShieldAlert className="w-4 h-4 shrink-0 mt-0.5 text-tier-1-text" />
                <div className="space-y-1">
                  <span>
                    <strong>BFIU TBML Guidelines &amp; MLPA 2012 § 25 Alert:</strong> Over-invoicing exceeds trade surveillance variance ceiling (&gt; 50%). Capital siphoning to JAFZA offshore entity indicated. Automated STR filing to Bangladesh Bank BFIU mandatory within 24 hours.
                  </span>
                  <div className="text-xs text-muted flex items-center gap-1.5 pt-0.5">
                    <span>Statutory Reference: BFIU Guidelines for Prevention of Trade Based Money Laundering (2019)</span>
                    <a
                      href="https://www.bb.org.bd/en/index.php/bfiu/publication"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-accent-2 hover:text-accent-2 inline-flex items-center gap-0.5"
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
            <div className="p-5 rounded-2xl bg-panel border border-line space-y-4">
              <div>
                <h3 className="text-sm font-bold text-fg flex items-center gap-2 font-mono">
                  <MapPin className="w-4 h-4 text-tier-2-text" />
                  Automated AIS Vessel Trajectory &amp; Port Divergence Audit
                </h3>
                <p className="text-xs text-muted mt-1">
                  Vessel: <strong className="text-fg-secondary">MV Arabian Pearl (IMO 9481920)</strong> • Flag: Panama
                </p>
              </div>

              <div className="space-y-3 font-mono text-xs">
                <div className="p-3 bg-canvas rounded-xl border border-line flex items-center justify-between">
                  <span className="text-muted">Port of Loading (B/L):</span>
                  <strong className="text-fg">Chittagong Port (BDCGP) — Departed 2026-08-28</strong>
                </div>
                <div className="p-3 bg-canvas rounded-xl border border-line flex items-center justify-between">
                  <span className="text-muted">Declared Port of Discharge (B/L):</span>
                  <strong className="text-fg">Port Klang, Malaysia (MYPKG)</strong>
                </div>
                <div className="p-3 bg-canvas rounded-xl border border-rose-500/40 flex items-center justify-between">
                  <span className="text-tier-1-text font-bold">Actual AIS Telemetry Discharge:</span>
                  <strong className="text-tier-1-text font-bold">Jebel Ali / Dubai, UAE (AEJEA) — Diverted</strong>
                </div>
              </div>

              <div className="p-3 bg-tier-2-bg border border-amber-800/40 rounded-xl text-xs text-tier-2-text">
                <strong>Anomalous Transshipment:</strong> AIS satellite transponder tracking confirms the vessel never called at Port Klang. Cargo discharged directly into JAFZA free-trade zone without customs duty or re-export documentation.
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Evidence Drag-and-Drop & WORM Anchor Actions */}
        <div className="lg:col-span-4 bg-panel border border-line rounded-2xl p-5 shadow-2xl flex flex-col justify-between space-y-6">
          <div className="space-y-5">
            <div>
              <h3 className="text-sm font-bold text-fg flex items-center gap-2 font-mono">
                <UploadCloud className="w-4 h-4 text-accent-2" />
                Cryptographic Evidence Ingestion
              </h3>
              <p className="text-xs text-muted mt-1">
                Upload supplemental bills of lading, phytosanitary certificates, or port manifests. Instant client-side WebCrypto SHA-256 calculation.
              </p>
            </div>

            {/* Upload Zone */}
            <label className="p-6 border-2 border-dashed border-line-strong hover:border-sky-500 rounded-xl flex flex-col items-center justify-center gap-2 cursor-pointer transition-colors bg-canvas/50">
              <UploadCloud className="w-8 h-8 text-fg0" />
              <span className="text-xs font-semibold text-fg-secondary">
                {isHashing ? 'Computing SHA-256 Digest...' : 'Select or Drop Trade Document'}
              </span>
              <span className="text-xs text-fg0">PDF, XML, or TIFF up to 25MB</span>
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
              <div className="p-3 bg-canvas border border-emerald-500/40 rounded-xl space-y-1.5 text-xs font-mono">
                <div className="flex items-center justify-between text-tier-3-text font-bold">
                  <span>{uploadedFileName}</span>
                  <CheckCircle2 className="w-4 h-4" />
                </div>
                <div className="text-xs text-muted break-all">
                  SHA-256: <span className="text-fg-secondary">{uploadedFileHash}</span>
                </div>
              </div>
            )}

            {/* Audit Status */}
            <div className="space-y-2 text-xs">
              <div className="p-3 bg-canvas rounded-xl border border-line flex items-center justify-between">
                <span className="text-muted">Verified Evidence Count:</span>
                <strong className="font-mono text-tier-3-text">{verifiedCount} Items Anchored</strong>
              </div>
              <div className="p-3 bg-canvas rounded-xl border border-line flex items-center justify-between gap-2">
                <span className="text-muted">Admissibility Standard:</span>
                <strong className="font-mono text-tier-3-text text-right">
                  {JURISDICTIONS[jurisdiction]?.evidenceRule || JURISDICTIONS.BD_BFIU.evidenceRule}
                </strong>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="pt-4 border-t border-line space-y-2.5">
            <button
              onClick={handlePinReport}
              disabled={isPinned}
              className={`w-full py-2.5 px-4 rounded-xl font-semibold text-xs transition-colors flex items-center justify-center gap-2 cursor-pointer ${
                isPinned
                  ? 'bg-tier-3-bg text-tier-3-text border border-emerald-800'
                  : 'bg-sky-600 hover:bg-sky-500 text-white shadow-lg shadow-sky-600/20'
              }`}
            >
              <FileCheck className="w-4 h-4" />
              <span>{isPinned ? 'TBML Report Pinned to Case & SAR' : 'Pin Verified TBML Report to Case'}</span>
            </button>

            <Link
              href="/sar?caseId=CASE-2026-0881"
              className="w-full py-2.5 px-4 rounded-xl bg-surface hover:bg-surface-hover text-fg-secondary font-medium text-xs transition-colors flex items-center justify-center gap-2"
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
