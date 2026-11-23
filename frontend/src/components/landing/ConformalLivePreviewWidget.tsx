'use client';

import React, { useState } from 'react';
import { ShieldAlert, AlertTriangle, CheckCircle2, Zap, ArrowRight, Activity, Layers, Scale } from 'lucide-react';

interface Scenario {
  id: 'tier1' | 'tier2' | 'tier3';
  tierLabel: string;
  tierColor: 'rose' | 'amber' | 'emerald';
  title: string;
  subtitle: string;
  conformalSet: string;
  setNotation: string;
  calibratedScore: number;
  fastPathLatencyUs: number;
  quantileCutoff: string;
  statutoryAction: string;
  invariants: {
    name: string;
    value: string;
    weight: number;
    description: string;
  }[];
}

const SCENARIOS: Scenario[] = [
  {
    id: 'tier1',
    tierLabel: 'Tier 1 Hold',
    tierColor: 'rose',
    title: 'TBML Over-Invoicing & Near-CTR Structuring',
    subtitle: 'SWIFT MT700 Documentary Credit + ৳954,000 Cash Deposit Layering',
    conformalSet: '{ 1 } (Guaranteed Illicit)',
    setNotation: 'Γ(u) = { 1 }',
    calibratedScore: 0.942,
    fastPathLatencyUs: 68,
    quantileCutoff: 'q̂^(1) = 0.812 (Score ≥ q̂^(1))',
    statutoryAction: 'Immediate Settlement Freeze & BFIU STR-1 goAML Filing (MLPA 2012 § 25)',
    invariants: [
      { name: 'ASYCUDA Price Divergence', value: '+333.7%', weight: 95, description: 'Declared $42.50 vs Benchmark $9.80 / kg' },
      { name: 'CTR Structuring Proximity', value: '0.954 (৳954k)', weight: 88, description: 'Beneath statutory ৳1,000,000 threshold' },
      { name: 'Pass-Through Mass Balance', value: 'Φ = 0.992', weight: 82, description: 'Rapid zero-balance drainage < 12h' },
      { name: 'Hawkes Arrival Burst Intensity', value: 'λ = 4.82/hr', weight: 74, description: 'Abnormal transaction velocity spike' }
    ]
  },
  {
    id: 'tier2',
    tierLabel: 'Tier 2 Review',
    tierColor: 'amber',
    title: 'Cross-Border MFS Velocity Burst',
    subtitle: 'Ambiguous Conformal Set — Prioritized Human Compliance Triage',
    conformalSet: '{ 0, 1 } (Ambiguous / Boundary)',
    setNotation: 'Γ(u) = { 0, 1 }',
    calibratedScore: 0.584,
    fastPathLatencyUs: 142,
    quantileCutoff: 'q̂^(0) = 0.185 ≤ Score < q̂^(1) = 0.812',
    statutoryAction: 'Escalated to Maker-Checker Docket with 12-Invariant SHAP Waterfall',
    invariants: [
      { name: 'Cross-Border Dispersion', value: '65.0% Offshore', weight: 62, description: 'High-frequency MFS agent payouts' },
      { name: 'Network Entropy Drop', value: '-0.41 bits', weight: 55, description: 'Constrained fan-out topology' },
      { name: 'Pass-Through Mass Balance', value: 'Φ = 0.812', weight: 48, description: 'Partial overnight holding buffer' },
      { name: 'Hawkes Arrival Burst Intensity', value: 'λ = 2.91/hr', weight: 42, description: 'Moderate deviation from account baseline' }
    ]
  },
  {
    id: 'tier3',
    tierLabel: 'Tier 3 Clear',
    tierColor: 'emerald',
    title: 'Verified Corporate Payroll & Supplier Settlement',
    subtitle: 'Autonomous Micro-Clearance — Zero Human Latency',
    conformalSet: '{ 0 } (Guaranteed Benign)',
    setNotation: 'Γ(u) = { 0 }',
    calibratedScore: 0.021,
    fastPathLatencyUs: 24,
    quantileCutoff: 'Score < q̂^(0) = 0.185 (FNR ≤ α = 1.00%)',
    statutoryAction: 'Instant Straight-Through Processing (STP) Auto-Clearance',
    invariants: [
      { name: 'Cadence Regularity', value: '0.990 (Monthly)', weight: 15, description: 'Established cyclic commercial payroll' },
      { name: 'Verified Corporate Identity', value: 'KYC Level 3', weight: 8, description: 'Direct RTGS clearing via EBLBBDDH' },
      { name: 'Pass-Through Mass Balance', value: 'Φ = 0.041', weight: 5, description: 'Normal liquidity absorption' },
      { name: 'Hawkes Arrival Burst Intensity', value: 'λ = 0.12/hr', weight: 2, description: 'Zero anomalous transaction velocity' }
    ]
  }
];

export const ConformalLivePreviewWidget: React.FC = () => {
  const [activeScenarioId, setActiveScenarioId] = useState<'tier1' | 'tier2' | 'tier3'>('tier1');
  const scenario = SCENARIOS.find((s) => s.id === activeScenarioId)!;

  return (
    <div className="w-full max-w-5xl mx-auto rounded-2xl bg-[#0B0F17] border border-[#1E293B] shadow-2xl overflow-hidden text-slate-100">
      {/* Widget Header */}
      <div className="px-5 py-3.5 bg-[#0F172A] border-b border-[#1E293B] flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-lg bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center">
            <Activity className="w-3.5 h-3.5 text-cyan-400" />
          </div>
          <div>
            <span className="text-xs font-mono font-bold uppercase tracking-wider text-slate-200">
              Live C-STGB v3.2 Conformal Inference Engine
            </span>
            <p className="text-[10px] font-mono text-slate-400">
              Split Conformal Calibration under Nominal 1 - α = 99.00% Coverage Guarantee
            </p>
          </div>
        </div>

        {/* 3 Scenario Switcher Tabs */}
        <div className="flex items-center bg-[#070B12] p-1 rounded-xl border border-[#334155] text-xs font-mono">
          {SCENARIOS.map((sc) => {
            const isSelected = sc.id === activeScenarioId;
            return (
              <button
                key={sc.id}
                type="button"
                onClick={() => setActiveScenarioId(sc.id)}
                className={`px-3 py-1.5 rounded-lg font-bold transition-all cursor-pointer flex items-center gap-1.5 ${
                  isSelected
                    ? sc.tierColor === 'rose'
                      ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
                      : sc.tierColor === 'amber'
                      ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40'
                      : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                <span
                  className={`w-2 h-2 rounded-full ${
                    sc.tierColor === 'rose'
                      ? 'bg-rose-500'
                      : sc.tierColor === 'amber'
                      ? 'bg-amber-500'
                      : 'bg-emerald-500'
                  }`}
                />
                <span>{sc.tierLabel}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Main Inspection Grid */}
      <div className="p-5 sm:p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Calibrated Score & Conformal Set (5 Cols) */}
        <div className="lg:col-span-5 space-y-4">
          <div className="p-4 rounded-xl bg-[#0F172A] border border-[#1E293B]">
            <div className="flex items-center justify-between text-xs font-mono text-slate-400 mb-1">
              <span>Calibrated C-STGB Risk Score</span>
              <span className="text-cyan-400 font-bold">{scenario.fastPathLatencyUs} µs Latency</span>
            </div>
            <div className="flex items-baseline gap-3 my-2">
              <span
                className={`text-4xl font-extrabold font-mono tracking-tight ${
                  scenario.tierColor === 'rose'
                    ? 'text-rose-400'
                    : scenario.tierColor === 'amber'
                    ? 'text-amber-400'
                    : 'text-emerald-400'
                }`}
              >
                {scenario.calibratedScore.toFixed(3)}
              </span>
              <span className="text-xs font-mono text-slate-400">/ 1.000 max risk</span>
            </div>

            {/* Score Bar */}
            <div className="w-full h-2.5 rounded-full bg-[#0B0F17] overflow-hidden border border-[#1E293B] relative my-3">
              <div
                className={`h-full transition-all duration-500 rounded-full ${
                  scenario.tierColor === 'rose'
                    ? 'bg-gradient-to-r from-amber-500 to-rose-500'
                    : scenario.tierColor === 'amber'
                    ? 'bg-amber-500'
                    : 'bg-emerald-500'
                }`}
                style={{ width: `${scenario.calibratedScore * 100}%` }}
              />
            </div>

            <div className="flex items-center justify-between text-[10px] font-mono text-slate-500">
              <span>0.000 (Safe)</span>
              <span>q̂^(0)=0.185</span>
              <span>q̂^(1)=0.812</span>
              <span>1.000 (Illicit)</span>
            </div>
          </div>

          {/* Conformal Prediction Set Badge */}
          <div className="p-4 rounded-xl bg-[#0F172A] border border-[#1E293B] space-y-2">
            <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider block">
              Conformal Prediction Set Output
            </span>
            <div className="flex items-center gap-2">
              <span
                className={`px-3 py-1 rounded-lg text-sm font-mono font-bold border ${
                  scenario.tierColor === 'rose'
                    ? 'bg-rose-500/20 text-rose-300 border-rose-500/40'
                    : scenario.tierColor === 'amber'
                    ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                    : 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
                }`}
              >
                {scenario.setNotation}
              </span>
              <span className="text-xs font-mono text-slate-300">{scenario.conformalSet}</span>
            </div>
            <p className="text-[11px] font-mono text-slate-400 pt-1">
              Cutoff Rule: <strong className="text-slate-200">{scenario.quantileCutoff}</strong>
            </p>
          </div>

          {/* Statutory Action */}
          <div className="p-3.5 rounded-xl bg-[#0B0F17] border border-[#1E293B] text-xs font-mono text-slate-300">
            <span className="text-[10px] text-slate-400 block mb-1 uppercase tracking-wider">
              Autonomous Institutional Action:
            </span>
            <span className="text-slate-100 font-semibold">{scenario.statutoryAction}</span>
          </div>
        </div>

        {/* Right Column: Top 4 Invariant Feature Attributions (7 Cols) */}
        <div className="lg:col-span-7 bg-[#0F172A] border border-[#1E293B] rounded-xl p-4 sm:p-5 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-[#1E293B] mb-4">
              <div className="flex items-center gap-2">
                <Layers className="w-4 h-4 text-emerald-400" />
                <span className="text-xs font-mono font-bold uppercase tracking-wider text-slate-200">
                  Top 4 Shapley Invariant Attributions
                </span>
              </div>
              <span className="text-[10px] font-mono text-slate-400">12-D Canonical Space</span>
            </div>

            <div className="space-y-3.5">
              {scenario.invariants.map((inv) => (
                <div key={inv.name} className="space-y-1">
                  <div className="flex items-center justify-between text-xs font-mono">
                    <span className="font-semibold text-slate-200">{inv.name}</span>
                    <span
                      className={`font-bold ${
                        scenario.tierColor === 'rose'
                          ? 'text-rose-400'
                          : scenario.tierColor === 'amber'
                          ? 'text-amber-400'
                          : 'text-emerald-400'
                      }`}
                    >
                      {inv.value}
                    </span>
                  </div>
                  <div className="w-full h-1.5 rounded-full bg-[#0B0F17] overflow-hidden border border-[#1E293B]">
                    <div
                      className={`h-full rounded-full transition-all duration-500 ${
                        scenario.tierColor === 'rose'
                          ? 'bg-rose-500'
                          : scenario.tierColor === 'amber'
                          ? 'bg-amber-500'
                          : 'bg-emerald-500'
                      }`}
                      style={{ width: `${inv.weight}%` }}
                    />
                  </div>
                  <p className="text-[10px] font-sans text-slate-400">{inv.description}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="pt-4 border-t border-[#1E293B] mt-4 flex items-center justify-between text-[11px] font-mono text-slate-400">
            <span>FastPath In-Memory Scoring</span>
            <span className="text-emerald-400 font-bold">&lt; 200 µs Target Verified</span>
          </div>
        </div>
      </div>
    </div>
  );
};
