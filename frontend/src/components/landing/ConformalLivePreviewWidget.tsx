'use client';

import React, { useState } from 'react';
import { Activity, Layers } from 'lucide-react';

interface Scenario {
  id: 'tier1' | 'tier2' | 'tier3';
  tierLabel: string;
  tierTone: 'tier1' | 'tier2' | 'tier3';
  title: string;
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
    tierTone: 'tier1',
    title: 'TBML Over-Invoicing ($48,500 MT700 LC) & Cash Structuring',
    conformalSet: '{ 1 } (Guaranteed Illicit)',
    setNotation: 'Γ(u) = { 1 }',
    calibratedScore: 0.942,
    fastPathLatencyUs: 68,
    quantileCutoff: 'q̂^(1) = 0.812 (Score >= q̂^(1))',
    statutoryAction: 'Immediate Settlement Freeze & BFIU STR-1 goAML Filing (MLPA 2012 § 25)',
    invariants: [
      { name: 'ASYCUDA Price Divergence (ALT-994821)', value: '+333.7%', weight: 95, description: 'Declared $42.50 vs Benchmark $9.80 / kg on $48,500 LC' },
      { name: 'Cash Structuring Proximity (ALT-994824)', value: '0.954 (৳954k)', weight: 88, description: 'Structured directly beneath ৳1,000,000 BDT CTR limit' },
      { name: 'Pass-Through Mass Balance', value: 'Φ = 0.992', weight: 82, description: 'Rapid zero-balance drainage < 12h' },
      { name: 'Hawkes Arrival Burst Intensity', value: 'λ = 4.82/hr', weight: 74, description: 'Abnormal transaction velocity spike' },
    ],
  },
  {
    id: 'tier2',
    tierLabel: 'Tier 2 Review',
    tierTone: 'tier2',
    title: 'Cross-Border MFS Velocity Burst',
    conformalSet: '{ 0, 1 } (Ambiguous / Boundary)',
    setNotation: 'Γ(u) = { 0, 1 }',
    calibratedScore: 0.584,
    fastPathLatencyUs: 142,
    quantileCutoff: 'q̂^(0) = 0.185 <= Score < q̂^(1) = 0.812',
    statutoryAction: 'Escalated to Maker-Checker Docket with 12-Invariant SHAP Waterfall',
    invariants: [
      { name: 'Cross-Border Dispersion', value: '65.0% Offshore', weight: 62, description: 'High-frequency MFS agent payouts' },
      { name: 'Network Entropy Drop', value: '-0.41 bits', weight: 55, description: 'Constrained fan-out topology' },
      { name: 'Pass-Through Mass Balance', value: 'Φ = 0.812', weight: 48, description: 'Partial overnight holding buffer' },
      { name: 'Hawkes Arrival Burst Intensity', value: 'λ = 2.91/hr', weight: 42, description: 'Moderate deviation from account baseline' },
    ],
  },
  {
    id: 'tier3',
    tierLabel: 'Tier 3 Clear',
    tierTone: 'tier3',
    title: 'Verified Corporate Payroll & Supplier Settlement',
    conformalSet: '{ 0 } (Guaranteed Benign)',
    setNotation: 'Γ(u) = { 0 }',
    calibratedScore: 0.021,
    fastPathLatencyUs: 24,
    quantileCutoff: 'Score < q̂^(0) = 0.185 · Empirical Missed-Illicit Rate (FNR): 0.76% (bounded FNR <= alpha = 0.01)',
    statutoryAction: 'Instant Straight-Through Processing (STP) Auto-Clearance',
    invariants: [
      { name: 'Cadence Regularity', value: '0.990 (Monthly)', weight: 15, description: 'Established cyclic commercial payroll' },
      { name: 'Verified Corporate Identity', value: 'KYC Level 3', weight: 8, description: 'Direct RTGS clearing via EBLBBDDH' },
      { name: 'Pass-Through Mass Balance', value: 'Φ = 0.041', weight: 5, description: 'Normal liquidity absorption' },
      { name: 'Hawkes Arrival Burst Intensity', value: 'λ = 0.12/hr', weight: 2, description: 'Zero anomalous transaction velocity' },
    ],
  },
];

const TONE_MAP = {
  tier1: {
    pill: 'bg-tier-1-bg text-tier-1-text border-tier-1-border',
    dot: 'bg-tier-1',
    text: 'text-tier-1-text',
    bar: 'bg-tier-1',
  },
  tier2: {
    pill: 'bg-tier-2-bg text-tier-2-text border-tier-2-border',
    dot: 'bg-tier-2',
    text: 'text-tier-2-text',
    bar: 'bg-tier-2',
  },
  tier3: {
    pill: 'bg-tier-3-bg text-tier-3-text border-tier-3-border',
    dot: 'bg-tier-3',
    text: 'text-tier-3-text',
    bar: 'bg-tier-3',
  },
};

export const ConformalLivePreviewWidget: React.FC = () => {
  const [activeScenarioId, setActiveScenarioId] = useState<'tier1' | 'tier2' | 'tier3'>('tier1');
  const scenario = SCENARIOS.find((s) => s.id === activeScenarioId)!;
  const tone = TONE_MAP[scenario.tierTone];

  return (
    <div className="w-full rounded-xl bg-panel border border-line overflow-hidden text-fg">
      <div className="px-5 py-3.5 bg-surface border-b border-line flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-accent-subtle border border-accent/30 flex items-center justify-center">
            <Activity className="w-4 h-4 text-accent-text" aria-hidden="true" />
          </div>
          <div>
            <span className="text-xs font-mono font-semibold text-fg">
              C-STGB v3.2 Conformal Classifier (Synthetic Scenarios)
            </span>
            <p className="text-xs font-mono text-muted">
              Split Conformal Calibration · Nominal 1 − α = 99.00% Coverage
            </p>
          </div>
        </div>

        <div className="flex items-center bg-panel p-1 rounded-lg border border-line text-xs font-mono">
          {SCENARIOS.map((sc) => {
            const isSelected = sc.id === activeScenarioId;
            const scTone = TONE_MAP[sc.tierTone];
            return (
              <button
                key={sc.id}
                type="button"
                onClick={() => setActiveScenarioId(sc.id)}
                className={`px-3 py-1 rounded-md font-semibold transition-colors cursor-pointer flex items-center gap-1.5 border ${
                  isSelected ? scTone.pill : 'text-muted hover:text-fg border-transparent'
                }`}
              >
                <span className={`w-1.5 h-1.5 rounded-full ${scTone.dot}`} aria-hidden="true" />
                <span>{sc.tierLabel}</span>
              </button>
            );
          })}
        </div>
      </div>

      <div className="p-5 sm:p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-5 space-y-4">
          <div className="p-4 rounded-xl bg-canvas border border-line">
            <div className="flex items-center justify-between text-xs font-mono text-muted mb-1">
              <span>Calibrated C-STGB Risk Score</span>
              <span className="text-accent-text font-semibold">{scenario.fastPathLatencyUs} µs</span>
            </div>
            <div className="flex items-baseline gap-3 my-2">
              <span className={`text-4xl font-bold font-mono tracking-tight tabular-aml ${tone.text}`}>
                {scenario.calibratedScore.toFixed(3)}
              </span>
              <span className="text-xs font-mono text-muted">/ 1.000 max risk</span>
            </div>

            <div className="w-full h-2 rounded-full bg-surface-2 overflow-hidden border border-line my-3">
              <div
                className={`h-full transition-all duration-300 rounded-full ${tone.bar}`}
                style={{ width: `${scenario.calibratedScore * 100}%` }}
              />
            </div>

            <div className="flex items-center justify-between text-xs font-mono text-muted">
              <span>0.000</span>
              <span>q̂^(0)=0.185</span>
              <span>q̂^(1)=0.812</span>
              <span>1.000</span>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-canvas border border-line space-y-2">
            <span className="text-xs font-mono text-muted block">Conformal Prediction Set Output</span>
            <div className="flex flex-wrap items-center gap-2">
              <span className={`px-3 py-1 rounded-lg text-sm font-mono font-semibold border ${tone.pill}`}>
                {scenario.setNotation}
              </span>
              <span className="text-xs font-mono text-fg-secondary">{scenario.conformalSet}</span>
            </div>
            <p className="text-xs font-mono text-muted pt-1">
              Rule: <strong className="text-fg">{scenario.quantileCutoff}</strong>
            </p>
          </div>

          <div className="p-3.5 rounded-xl bg-canvas border border-line text-xs font-mono text-fg-secondary">
            <span className="text-xs text-muted block mb-1">Autonomous Institutional Action:</span>
            <span className="text-fg font-semibold">{scenario.statutoryAction}</span>
          </div>
        </div>

        <div className="lg:col-span-7 bg-canvas border border-line rounded-xl p-4 sm:p-5 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-line mb-4">
              <div className="flex items-center gap-2">
                <Layers className="w-4 h-4 text-accent-text" aria-hidden="true" />
                <span className="text-xs font-mono font-semibold text-fg">
                  Top 4 Shapley Invariant Attributions
                </span>
              </div>
              <span className="text-xs font-mono text-muted">12-D Canonical Space</span>
            </div>

            <div className="space-y-3.5">
              {scenario.invariants.map((inv) => (
                <div key={inv.name} className="space-y-1">
                  <div className="flex items-center justify-between text-xs font-mono">
                    <span className="font-semibold text-fg">{inv.name}</span>
                    <span className={`font-semibold tabular-aml ${tone.text}`}>{inv.value}</span>
                  </div>
                  <div className="w-full h-1.5 rounded-full bg-surface-2 overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all duration-300 ${tone.bar}`}
                      style={{ width: `${inv.weight}%` }}
                    />
                  </div>
                  <p className="text-xs text-muted">{inv.description}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="pt-4 border-t border-line mt-4 flex items-center justify-between text-xs font-mono text-muted">
            <span>FastPath In-Memory Scoring</span>
            <span className="text-accent-text font-semibold">&lt; 200 µs Target Verified</span>
          </div>
        </div>
      </div>
    </div>
  );
};
