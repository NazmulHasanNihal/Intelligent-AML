'use client';

import React, { useState } from 'react';
import {
  RotateCcw,
  Sliders,
  FileText,
  Send,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  ShieldCheck,
  Building,
  Terminal,
  Clock
} from 'lucide-react';
import { PiiText } from '@/components/ui/PiiText';

export default function CounterfactualRecoursePage() {
  // Recourse Sliders
  const [spreadDays, setSpreadDays] = useState<number>(1);
  const [valuationDiscount, setValuationDiscount] = useState<number>(333);
  const [verifiedDocumentation, setVerifiedDocumentation] = useState<boolean>(false);
  const [showNoticeModal, setShowNoticeModal] = useState<boolean>(false);
  const [webhookLog, setWebhookLog] = useState<string | null>(null);

  // Dynamic counterfactual calculation
  const baseRisk = 0.984;
  let simulatedRisk = baseRisk;
  if (spreadDays > 1) simulatedRisk -= (spreadDays * 0.05);
  if (valuationDiscount < 100) simulatedRisk -= 0.40;
  if (verifiedDocumentation) simulatedRisk -= 0.35;
  simulatedRisk = Math.max(simulatedRisk, 0.008);

  const simulatedHawkes = Math.max(4.82 - (spreadDays * 0.4), 0.15);
  const simulatedTier = simulatedRisk > 0.70 ? 1 : simulatedRisk > 0.20 ? 2 : 3;

  const handleSimulateWebhook = () => {
    const payload = {
      event: 'AML_ADVERSE_ACTION_RECOURSE_CALCULATED',
      timestamp: new Date().toISOString(),
      account: 'BD22-EBLB-4829-1092-8823',
      entity: 'Meghna Industrial & Agro Processing Ltd',
      originalRisk: baseRisk,
      counterfactualRisk: Number(simulatedRisk.toFixed(4)),
      recommendedTier: simulatedTier === 3 ? 'TIER_3_AUTO_CLEARED' : 'TIER_2_OFFICER_REVIEW',
      cfpbComplianceNoticeId: `CFPB-ADV-2026-${Math.floor(1000 + Math.random() * 9000)}`,
      hmacSignature: 'sha256=9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72'
    };

    setWebhookLog(JSON.stringify(payload, null, 2));
  };

  return (
    <div className="p-6 max-w-[1700px] mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2">
          <RotateCcw className="w-5 h-5 text-teal-400" />
          Counterfactual Recourse & Adverse Action Engine
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Causal sensitivity analysis determining actionable customer pathways to licitness under CFPB Circular 2022-03 and FCRA requirements.
        </p>
      </div>

      {/* Main Grid: Causal Sliders & Recourse Visualization */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Causal Sliders (5 Cols) */}
        <div className="lg:col-span-5 bg-[#0F172A] border border-[#1E293B] rounded-xl p-5 space-y-5">
          <h2 className="text-sm font-semibold text-slate-100 flex items-center gap-2 pb-2 border-b border-[#1E293B]">
            <Sliders className="w-4 h-4 text-teal-400" />
            Causal Perturbation Sliders (What-If Analysis)
          </h2>

          <div className="space-y-4 text-xs">
            {/* Slider 1: Transaction Temporal Spread */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-slate-300 font-medium">Drawdown Temporal Dispersion (&Delta;t)</span>
                <span className="font-mono font-bold text-teal-300">{spreadDays} Day(s)</span>
              </div>
              <input
                type="range"
                min="1"
                max="14"
                value={spreadDays}
                onChange={(e) => setSpreadDays(Number(e.target.value))}
                className="w-full accent-teal-500 cursor-pointer"
              />
              <span className="text-[10px] text-slate-500 mt-0.5 block">
                Spreading rapid consecutive withdrawals suppresses Hawkes arrival intensity (&lambda;<sub>u</sub>).
              </span>
            </div>

            {/* Slider 2: Invoice Valuation Divergence */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-slate-300 font-medium">Invoice Price Divergence vs ASYCUDA</span>
                <span className="font-mono font-bold text-teal-300">+{valuationDiscount}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="350"
                value={valuationDiscount}
                onChange={(e) => setValuationDiscount(Number(e.target.value))}
                className="w-full accent-teal-500 cursor-pointer"
              />
              <span className="text-[10px] text-slate-500 mt-0.5 block">
                Harmonizing declared commodity prices within 15% of customs benchmark eliminates TBML penalties.
              </span>
            </div>

            {/* Checkbox: Independent Customs Verification */}
            <div className="pt-2">
              <label className="flex items-center gap-2.5 p-3 bg-[#0B0F17] rounded-lg border border-[#1E293B] cursor-pointer hover:border-[#334155] transition-colors">
                <input
                  type="checkbox"
                  checked={verifiedDocumentation}
                  onChange={(e) => setVerifiedDocumentation(e.target.checked)}
                  className="w-4 h-4 accent-teal-500 rounded"
                />
                <span className="text-xs text-slate-200 font-medium">
                  Provide Certified Third-Party Pre-Shipment Inspection (PSI) Certificate
                </span>
              </label>
            </div>

            <div className="pt-3 border-t border-[#1E293B] flex items-center justify-between gap-3">
              <button
                onClick={() => setShowNoticeModal(true)}
                className="flex-1 py-2 px-3 bg-[#1E293B] hover:bg-[#334155] text-slate-200 rounded-lg text-xs font-semibold transition-colors flex items-center justify-center gap-1.5"
              >
                <FileText className="w-3.5 h-3.5 text-teal-400" />
                <span>Generate CFPB Notice</span>
              </button>

              <button
                onClick={handleSimulateWebhook}
                className="flex-1 py-2 px-3 bg-teal-600 hover:bg-teal-500 text-slate-950 font-bold rounded-lg text-xs uppercase tracking-wide transition-all shadow-md flex items-center justify-center gap-1.5"
              >
                <Send className="w-3.5 h-3.5" />
                <span>Simulate Webhook</span>
              </button>
            </div>
          </div>
        </div>

        {/* Right Column: Recourse Impact & Webhook Terminal (7 Cols) */}
        <div className="lg:col-span-7 space-y-6">
          {/* Simulated Conformal State Ribbon */}
          <div className="p-5 bg-[#0F172A] border border-[#1E293B] rounded-xl space-y-4">
            <h3 className="text-sm font-semibold text-slate-200">
              Counterfactual Transition State
            </h3>

            <div className="grid grid-cols-2 md:grid-cols-3 gap-3 text-xs">
              <div className="p-3 bg-[#0B0F17] rounded-lg border border-[#1E293B]">
                <span className="text-slate-500 block text-[10px] uppercase">Simulated Risk</span>
                <span className="text-lg font-bold font-mono text-teal-300">
                  {simulatedRisk.toFixed(3)}
                </span>
                <span className="text-[10px] text-slate-400 block mt-0.5">
                  Original: <span className="line-through text-rose-400 font-mono">0.984</span>
                </span>
              </div>

              <div className="p-3 bg-[#0B0F17] rounded-lg border border-[#1E293B]">
                <span className="text-slate-500 block text-[10px] uppercase">Hawkes Intensity (&lambda;)</span>
                <span className="text-lg font-bold font-mono text-teal-300">
                  {simulatedHawkes.toFixed(2)}
                </span>
                <span className="text-[10px] text-slate-400 block mt-0.5">
                  Original: <span className="line-through text-amber-400 font-mono">4.82</span>
                </span>
              </div>

              <div className="p-3 bg-[#0B0F17] rounded-lg border border-[#1E293B]">
                <span className="text-slate-500 block text-[10px] uppercase">Predicted Tier</span>
                <span
                  className={`inline-block mt-1 px-2 py-0.5 rounded text-xs font-mono font-bold ${
                    simulatedTier === 1
                      ? 'bg-rose-500/20 text-rose-300'
                      : simulatedTier === 2
                      ? 'bg-amber-500/20 text-amber-300'
                      : 'bg-emerald-500/20 text-emerald-300'
                  }`}
                >
                  Tier {simulatedTier} {simulatedTier === 3 ? '(Auto-Clear)' : simulatedTier === 2 ? '(Review)' : '(Hold)'}
                </span>
              </div>
            </div>

            {simulatedTier === 3 && (
              <div className="p-3 bg-emerald-950/20 border border-emerald-900/40 rounded-lg text-emerald-300 text-xs flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>
                  <strong>Full Recourse Achieved:</strong> The proposed customer operational adjustments successfully clear the finite-sample conformal safety gate (Coverage ≥ 99.0%).
                </span>
              </div>
            )}
          </div>

          {/* Webhook Output Terminal */}
          {webhookLog && (
            <div className="bg-[#0B0F17] border border-[#1E293B] rounded-xl overflow-hidden">
              <div className="p-2.5 bg-[#0F172A] border-b border-[#1E293B] flex items-center justify-between text-xs text-slate-400 font-mono">
                <div className="flex items-center gap-2">
                  <Terminal className="w-3.5 h-3.5 text-teal-400" />
                  <span>Core Banking Outbound Webhook Dispatch (Temenos T24 / Finacle)</span>
                </div>
                <span className="text-emerald-400">HTTP 200 OK</span>
              </div>
              <pre className="p-4 text-[11px] font-mono text-teal-200 overflow-x-auto leading-relaxed">
                {webhookLog}
              </pre>
            </div>
          )}
        </div>
      </div>

      {/* CFPB Adverse Action Notice Modal */}
      {showNoticeModal && (
        <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="w-full max-w-2xl bg-[#0F172A] border border-[#334155] rounded-xl shadow-2xl p-6 space-y-4 text-xs text-slate-200">
            <div className="flex items-center justify-between pb-3 border-b border-[#1E293B]">
              <h3 className="font-bold text-sm text-slate-100 flex items-center gap-2">
                <FileText className="w-4 h-4 text-teal-400" />
                CFPB / FCRA Plain-Language Adverse Action Notice
              </h3>
              <button
                onClick={() => setShowNoticeModal(false)}
                className="text-slate-400 hover:text-slate-200"
              >
                ✕
              </button>
            </div>

            <div className="p-4 bg-[#0B0F17] rounded-lg border border-[#1E293B] space-y-3 font-sans leading-relaxed text-slate-300">
              <p className="font-bold text-slate-100">
                NOTICE OF TRANSACTION HOLD & SPECIFIC REASONS FOR COMPLIANCE ACTION
              </p>
              <p>
                <strong>Date:</strong> September 02, 2026<br />
                <strong>Customer:</strong> Meghna Industrial & Agro Processing Ltd<br />
                <strong>Account:</strong> BD22-EBLB-••••-••••-8823
              </p>
              <p>
                In accordance with regulatory disclosure guidelines (CFPB Circular 2022-03), this notice provides the primary factual reasons why your recent transaction of $9,450.00 USD was held for verification:
              </p>
              <ol className="list-decimal pl-5 space-y-1 text-slate-200">
                <li>
                  <strong>Declared Valuation Discrepancy:</strong> The commodity unit pricing in Letter of Credit LC-2026-CTG-88912 diverged significantly (+333.7%) from standard customs benchmarks.
                </li>
                <li>
                  <strong>Transaction Frequency:</strong> High-velocity transfers occurred within a shortened timeframe without prior trade documentation on file.
                </li>
              </ol>
              <p className="text-[11px] text-slate-400">
                <strong>Action Required to Clear:</strong> To expedite processing, please submit a verified commercial invoice and bill of lading via our secure documentation portal.
              </p>
            </div>

            <div className="flex justify-end gap-2 pt-2">
              <button
                onClick={() => alert('Official CFPB Notice PDF downloaded.')}
                className="px-3 py-1.5 bg-[#1E293B] hover:bg-[#334155] rounded-lg text-slate-200 font-medium"
              >
                Download Official PDF
              </button>
              <button
                onClick={() => setShowNoticeModal(false)}
                className="px-4 py-1.5 bg-teal-600 hover:bg-teal-500 text-slate-950 font-bold rounded-lg"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
