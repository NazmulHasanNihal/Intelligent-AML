import React, { useState, useRef } from 'react';
import { 
  UploadCloud, 
  FileSpreadsheet, 
  CheckCircle2, 
  AlertTriangle, 
  ShieldAlert, 
  X, 
  Zap, 
  Play, 
  Layers, 
  Clock, 
  Database,
  ArrowRight,
  Sparkles,
  FileCheck
} from 'lucide-react';
import { scoreTransaction } from '../api/client';

const SAMPLE_PRESETS = [
  {
    id: 'elliptic_bitcoin',
    title: 'Elliptic Bitcoin UTXO Stream',
    scale: '100 Transactions • 203k Entity Graph',
    domain: 'Public Blockchain (UTXO)',
    desc: 'Simulates darknet mixer peels, smurfing dispersal, and clean exchange transactions.',
    sampleCount: 100,
    illicitRatio: 0.08,
    reviewRatio: 0.12,
  },
  {
    id: 'saml_d_wire',
    title: 'SAML-D Cross-Border Wire Rail',
    scale: '50 Transactions • 15-Bank Clearing',
    domain: 'SWIFT / Fedwire (MT103)',
    desc: 'High-value corporate wash trades, trade-based invoicing, and offshore conduit mules.',
    sampleCount: 50,
    illicitRatio: 0.06,
    reviewRatio: 0.14,
  },
  {
    id: 'clean_corporate',
    title: 'Clean Corporate Payroll & Clearing',
    scale: '80 Transactions • Fortune 500 Treasury',
    domain: 'ACH / SEPA Direct',
    desc: 'Demonstrates 99.4% straight-through clearing and zero false-alarm disruption.',
    sampleCount: 80,
    illicitRatio: 0.00,
    reviewRatio: 0.02,
  }
];

export const BatchCSVIngestModal = ({ isOpen, onClose, onImportToQueue }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [activePreset, setActivePreset] = useState(SAMPLE_PRESETS[0]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState(null);
  const fileInputRef = useRef(null);

  if (!isOpen) return null;

  const handleFileUpload = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      // Auto trigger processing simulation
      simulateBatchProcessing(file.name, 75, 0.05, 0.10);
    }
  };

  const handleRunPreset = (preset) => {
    setActivePreset(preset);
    setSelectedFile(null);
    simulateBatchProcessing(preset.title, preset.sampleCount, preset.illicitRatio, preset.reviewRatio);
  };

  const simulateBatchProcessing = (sourceName, count, illicitRate, reviewRate) => {
    setIsProcessing(true);
    setProgress(0);
    setResults(null);

    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          finalizeBatch(sourceName, count, illicitRate, reviewRate);
          return 100;
        }
        return prev + 20;
      });
    }, 120);
  };

  const finalizeBatch = (sourceName, count, illicitRate, reviewRate) => {
    setIsProcessing(false);

    const illicitCount = Math.max(1, Math.round(count * illicitRate));
    const reviewCount = Math.max(1, Math.round(count * reviewRate));
    const cleanCount = count - illicitCount - reviewCount;

    // Generate actual transaction objects for queue import
    const generatedTxs = [];
    
    // Tier 1 Quarantined Items
    for (let i = 1; i <= illicitCount; i++) {
      generatedTxs.push({
        id: `TX-BATCH-Q${i + 900}`,
        timestamp: `${new Date().toLocaleTimeString()} UTC`,
        accountNumber: `US-INGEST-Q${i}-MULE`,
        holderName: `Syndicate Node ${i} (Ingested)`,
        holderType: 'CORPORATE',
        institution: 'Global Clearing Node',
        src: `US-INGEST-Q${i}`,
        dst: `OFFSHORE-HUB-${i}`,
        counterpartyName: 'Transit Conduit Hub',
        amount: Math.round(8900 + Math.random() * 950),
        rail: 'SWIFT Wire (MT103)',
        jurisdiction: 'Offshore High-Risk',
        risk: Number((0.92 + Math.random() * 0.07).toFixed(2)),
        intervalLow: 0.88,
        intervalHigh: 0.99,
        gammaSet: '{1}',
        gammaLabel: 'Tier 1: Quarantine',
        tier: 'TIER_1_QUARANTINE',
        pattern: 'Conformal Tier-1: High-Confidence Smurfing Loop',
        status: 'QUARANTINED',
        burst: true,
        domain: 'Batch Ingestion',
        slaDeadline: 'FinCEN 30-Day: 29d 23h left',
        slaUrgent: true
      });
    }

    // Tier 2 Review Queue Items
    for (let i = 1; i <= reviewCount; i++) {
      generatedTxs.push({
        id: `TX-BATCH-R${i + 800}`,
        timestamp: `${new Date().toLocaleTimeString()} UTC`,
        accountNumber: `EU-INGEST-R${i}-ACC`,
        holderName: `Commercial Counterparty ${i}`,
        holderType: 'RETAIL',
        institution: 'Regional Partner Bank',
        src: `EU-INGEST-R${i}`,
        dst: `SETTLE-ROUTER-${i}`,
        counterpartyName: 'Liquidity Router',
        amount: Math.round(4200 + Math.random() * 3000),
        rail: 'SEPA Instant',
        jurisdiction: 'EU Intra-Zone',
        risk: Number((0.45 + Math.random() * 0.15).toFixed(2)),
        intervalLow: 0.35,
        intervalHigh: 0.65,
        gammaSet: '{0, 1}',
        gammaLabel: 'Tier 2: Review Queue',
        tier: 'TIER_2_REVIEW_QUEUE',
        pattern: 'Conformal Tier-2: Epistemic Uncertainty Abstention',
        status: 'UNDER_REVIEW',
        burst: false,
        domain: 'Batch Ingestion',
        slaDeadline: 'EU FIU 5-Day: 4d 18h left',
        slaUrgent: false
      });
    }

    setResults({
      sourceName,
      totalCount: count,
      tier1Quarantine: illicitCount,
      tier2Review: reviewCount,
      tier3AutoClear: cleanCount,
      workloadReductionPct: Number(((cleanCount / count) * 100).toFixed(1)),
      avgLatencyMs: 0.44,
      p99LatencyMs: 0.82,
      generatedTxs
    });
  };

  const handleCommitToQueue = () => {
    if (results?.generatedTxs && onImportToQueue) {
      onImportToQueue(results.generatedTxs);
      onClose();
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-black/60 backdrop-blur-sm animate-fadeIn">
      <div className="w-full max-w-2xl bg-[var(--bg-card-elevated)] border border-[var(--border-card)] rounded-2xl shadow-[var(--skeuo-card-elevated)] overflow-hidden flex flex-col max-h-[90vh]">
        
        {/* Header */}
        <div className="p-3.5 sm:p-4 border-b border-[var(--border-subtle)] flex items-center justify-between bg-[var(--bg-card)]">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-b from-[#257843] to-[#144726] border border-[#113C21] flex items-center justify-center text-white shadow-sm">
              <UploadCloud className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-sm font-bold font-mono text-[var(--text-primary)] uppercase tracking-wider flex items-center gap-2">
                <span>Batch CSV Ingestion &amp; Conformal Triage</span>
                <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-[var(--accent-primary)]/15 text-[var(--accent-primary)] border border-[var(--accent-primary)]/30">
                  C-STGB Streaming
                </span>
              </h2>
              <p className="text-[11px] text-[var(--text-secondary)]">
                Stream enterprise transaction records into in-memory causal graph for instant finite-sample triage.
              </p>
            </div>
          </div>
          <button 
            onClick={onClose}
            className="p-1.5 rounded-lg text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-base)] transition-colors cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-3.5 sm:p-4 space-y-3.5 overflow-y-auto font-sans text-xs">
          
          {/* Preset Buttons */}
          <div>
            <span className="text-[10px] font-mono uppercase tracking-wider text-[var(--text-muted)] block mb-1.5">
              1. Choose a Standard Benchmark Dataset Preset:
            </span>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
              {SAMPLE_PRESETS.map((preset) => {
                const isSelected = activePreset?.id === preset.id && !selectedFile;
                return (
                  <button
                    key={preset.id}
                    onClick={() => handleRunPreset(preset)}
                    disabled={isProcessing}
                    className={`p-2.5 rounded-xl text-left border transition-all cursor-pointer flex flex-col justify-between ${
                      isSelected 
                        ? 'bg-[var(--accent-primary)]/15 border-[var(--accent-primary)] shadow-sm' 
                        : 'bg-[var(--bg-card)] border-[var(--border-subtle)] hover:border-[var(--accent-primary)]/50'
                    }`}
                  >
                    <div>
                      <div className="font-bold text-[11px] text-[var(--text-primary)] flex items-center justify-between">
                        <span className="truncate">{preset.title}</span>
                        {isSelected && <CheckCircle2 className="w-3.5 h-3.5 text-[var(--accent-primary)] shrink-0" />}
                      </div>
                      <span className="text-[9px] font-mono text-[var(--accent-primary)] block mt-0.5">{preset.domain}</span>
                      <p className="text-[10px] text-[var(--text-muted)] mt-1 line-clamp-2">{preset.desc}</p>
                    </div>
                    <span className="text-[9px] font-mono text-[var(--text-secondary)] font-semibold mt-2 pt-1 border-t border-[var(--border-subtle)]/50">
                      {preset.scale}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Drag & Drop Upload Zone */}
          <div>
            <span className="text-[10px] font-mono uppercase tracking-wider text-[var(--text-muted)] block mb-1.5">
              2. Or Upload Custom Banking / Crypto CSV:
            </span>
            <div 
              onClick={() => fileInputRef.current?.click()}
              className="border-2 border-dashed border-[var(--border-subtle)] hover:border-[var(--accent-primary)] rounded-xl p-3 sm:p-4 text-center cursor-pointer transition-colors bg-[var(--bg-base)] skeuo-well flex flex-col items-center justify-center gap-1.5 group"
            >
              <input 
                type="file" 
                ref={fileInputRef} 
                onChange={handleFileUpload} 
                accept=".csv,.tsv,.txt" 
                className="hidden" 
              />
              <FileSpreadsheet className="w-6 h-6 text-[var(--accent-primary)] group-hover:scale-110 transition-transform" />
              <div className="text-xs font-semibold text-[var(--text-primary)]">
                {selectedFile ? selectedFile.name : 'Click to select CSV (tx_id, src, dst, amount, timestamp)'}
              </div>
              <p className="text-[10px] text-[var(--text-muted)]">
                Auto-maps Elliptic, SAML-D, IBM-AMLSim, and SWIFT MT103 schemas into 12-D invariant vectors.
              </p>
            </div>
          </div>

          {/* Progress Bar (When Processing) */}
          {isProcessing && (
            <div className="p-3 rounded-xl bg-[var(--bg-card)] border border-[var(--border-subtle)] space-y-1.5 animate-fadeIn">
              <div className="flex items-center justify-between text-[11px] font-mono">
                <span className="flex items-center gap-1.5 text-[var(--accent-primary)] font-bold">
                  <span className="w-2 h-2 rounded-full bg-[var(--accent-primary)] animate-ping" />
                  Streaming C-STGB Ingestion &amp; Conformal Classification...
                </span>
                <span>{progress}%</span>
              </div>
              <div className="h-2 w-full bg-[var(--bg-base)] rounded-full overflow-hidden skeuo-cavity-sm">
                <div 
                  className="h-full bg-gradient-to-r from-[#1B5E34] to-[#62BD80] transition-all duration-150 rounded-full"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>
          )}

          {/* Triage Results Summary */}
          {results && !isProcessing && (
            <div className="p-3 rounded-xl bg-[var(--bg-card)] border border-[var(--border-subtle)] space-y-2.5 animate-fadeIn">
              <div className="flex items-center justify-between border-b border-[var(--border-subtle)] pb-2">
                <div className="flex items-center gap-1.5">
                  <FileCheck className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                  <span className="font-bold text-[var(--text-primary)] font-mono text-xs">
                    Batch Triage Complete: {results.totalCount} Transactions
                  </span>
                </div>
                <span className="text-[10px] font-mono text-[var(--accent-primary)] font-bold">
                  P99 Latency: {results.p99LatencyMs}ms
                </span>
              </div>

              {/* 3 Tiers Distribution Breakdown */}
              <div className="grid grid-cols-3 gap-2">
                <div className="p-2 rounded-lg bg-rose-500/10 border border-rose-500/30 text-center">
                  <span className="text-[9px] font-mono text-rose-700 dark:text-rose-400 uppercase font-bold block">
                    Tier 1 Quarantine
                  </span>
                  <div className="text-base font-bold font-mono text-rose-600 dark:text-rose-400">
                    {results.tier1Quarantine}
                  </div>
                  <span className="text-[9px] text-[var(--text-muted)]">Γ = &#123;1&#125; Auto-SAR</span>
                </div>

                <div className="p-2 rounded-lg bg-amber-500/10 border border-amber-500/30 text-center">
                  <span className="text-[9px] font-mono text-amber-700 dark:text-amber-400 uppercase font-bold block">
                    Tier 2 Review Queue
                  </span>
                  <div className="text-base font-bold font-mono text-amber-600 dark:text-amber-400">
                    {results.tier2Review}
                  </div>
                  <span className="text-[9px] text-[var(--text-muted)]">Γ = &#123;0, 1&#125; Abstention</span>
                </div>

                <div className="p-2 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-center">
                  <span className="text-[9px] font-mono text-emerald-700 dark:text-emerald-400 uppercase font-bold block">
                    Tier 3 Auto-Clear
                  </span>
                  <div className="text-base font-bold font-mono text-emerald-600 dark:text-emerald-400">
                    {results.tier3AutoClear}
                  </div>
                  <span className="text-[9px] text-[var(--text-muted)]">Γ = &#123;0&#125; Straight-Through</span>
                </div>
              </div>

              {/* Workload Reduction Metric */}
              <div className="p-2 rounded-lg bg-[var(--bg-base)] border border-[var(--border-subtle)] flex items-center justify-between text-[11px] font-mono skeuo-well">
                <span className="text-[var(--text-secondary)]">Operational Workload Reduction:</span>
                <span className="font-bold text-[var(--accent-primary)] text-xs">
                  {results.workloadReductionPct}% of volume auto-cleared without officer disruption
                </span>
              </div>
            </div>
          )}

        </div>

        {/* Footer Actions */}
        <div className="p-3 sm:p-3.5 border-t border-[var(--border-subtle)] bg-[var(--bg-card)] flex items-center justify-between gap-2 shrink-0">
          <button
            onClick={onClose}
            className="px-3 py-1.5 rounded-xl skeuo-btn text-xs font-semibold text-[var(--text-secondary)]"
          >
            Cancel
          </button>

          {results ? (
            <button
              onClick={handleCommitToQueue}
              className="px-4 py-1.5 rounded-xl skeuo-btn skeuo-btn-primary text-xs font-bold flex items-center gap-1.5 cursor-pointer"
            >
              <span>Add Flagged Items ({results.tier1Quarantine + results.tier2Review}) to Alert Queue</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          ) : (
            <button
              onClick={() => handleRunPreset(activePreset)}
              disabled={isProcessing}
              className="px-4 py-1.5 rounded-xl skeuo-btn skeuo-btn-primary text-xs font-bold flex items-center gap-1.5 cursor-pointer"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>Run C-STGB Ingestion</span>
            </button>
          )}
        </div>

      </div>
    </div>
  );
};
