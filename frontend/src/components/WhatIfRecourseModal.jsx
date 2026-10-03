import React, { useState } from 'react';
import { 
  Sliders, 
  X, 
  Sparkles, 
  ShieldCheck, 
  AlertTriangle, 
  ArrowRight, 
  Activity, 
  RefreshCw,
  CheckCircle2,
  TrendingDown
} from 'lucide-react';
import { useAppStore } from '../lib/store';
import { Button } from './ui/Button';
import { Badge } from './ui/Badge';

export const WhatIfRecourseModal = () => {
  const { 
    isRecourseModalOpen, 
    setRecourseModalOpen, 
    recourseSubject, 
    addToast,
    logAuditAction
  } = useAppStore();

  // Sensitivity Sliders State
  const [txAmount, setTxAmount] = useState(48500);
  const [txFrequencyPerHour, setTxFrequencyPerHour] = useState(4);
  const [dwellTimeHours, setDwellTimeHours] = useState(0.35);
  const [documentCompleteness, setDocumentCompleteness] = useState(65);

  if (!isRecourseModalOpen) return null;

  const subject = recourseSubject ? {
    account: recourseSubject.account || recourseSubject.id || 'BD22-EBLB-4829-1092-8823',
    entityName: recourseSubject.entityName || recourseSubject.name || recourseSubject.label || 'Commercial Accountholder',
    initialRisk: recourseSubject.initialRisk || recourseSubject.riskScore || 0.984,
    initialTier: recourseSubject.initialTier || recourseSubject.tier || 'Tier 1 Hold'
  } : {
    account: 'BD22-EBLB-4829-1092-8823',
    entityName: 'Meghna Industrial & Agro Processing Ltd',
    initialRisk: 0.984,
    initialTier: 'Tier 1 Hold'
  };

  // Mathematical Recourse Simulation:
  // Base risk is driven by Hawkes burst intensity: lambda = freq / (dwellTime + 0.1)
  // Higher amount above $10k adds penalty. Higher docs reduce penalty.
  const burstIntensity = (txFrequencyPerHour / (dwellTimeHours + 0.2)).toFixed(1);
  const sizeRatio = Math.max(0, (txAmount - 9500) / 40000);
  const docBonus = documentCompleteness / 100 * 0.45;
  
  const simulatedRisk = Math.max(0.015, Math.min(0.99, 
    0.35 + (burstIntensity * 0.08) + (sizeRatio * 0.40) - docBonus
  ));

  const simulatedTier = simulatedRisk >= 0.85 ? 'Tier 1 Hold' :
                        simulatedRisk >= 0.30 ? 'Tier 2 Review Queue' :
                        'Tier 3 Straight-Through (Cleared)';

  const handleApplyRecoursePlan = () => {
    logAuditAction(
      'COUNTERFACTUAL_RECOURSE_RECOMMENDATION_ISSUED',
      `Issued behavioral recourse parameters for ${subject.account}: Cap amount to $${txAmount.toLocaleString()}, min dwell time ${dwellTimeHours}h, target risk ${ (simulatedRisk * 100).toFixed(1) }%`,
      subject.account,
      'Compliance Officer'
    );
    addToast('Recourse Recommendation Stored', `Prescriptive remedy generated for ${subject.entityName}.`, 'success');
    setRecourseModalOpen(false);
  };

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-black/60 backdrop-blur-xs flex items-center justify-center p-4 animate-fadeIn">
      <div 
        className="w-full max-w-2xl bg-surface border border-border rounded-xl shadow-2xl overflow-hidden flex flex-col text-xs"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-4 bg-surfaceRaised border-b border-border flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-accent/15 border border-accent/30 text-accent flex items-center justify-center font-bold">
              <Sliders className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-semibold text-text text-sm">Counterfactual Behavioral Recourse</h3>
                <Badge variant="accent" size="sm">What-If Sensitivity Engine</Badge>
              </div>
              <p className="text-[11px] text-text-muted mt-0.5">
                Model-driven prescriptive path to resolve Hawkes burst alerts and de-escalate false positives.
              </p>
            </div>
          </div>
          <button 
            onClick={() => setRecourseModalOpen(false)}
            className="p-1 rounded text-text-muted hover:text-text hover:bg-surface transition-colors cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Target Entity Banner */}
        <div className="px-5 py-2.5 bg-bg border-b border-borderSubtle flex items-center justify-between font-mono text-[11px]">
          <div className="truncate">
            <span className="text-text-muted">Subject: </span>
            <span className="text-text font-semibold">{subject.entityName}</span>
            <span className="text-text-muted ml-2">({subject.account})</span>
          </div>
          <div className="flex items-center gap-2 shrink-0">
            <span className="text-text-muted">Current Risk:</span>
            <span className="font-bold text-critical">{(subject.initialRisk ? subject.initialRisk * 100 : 98.4).toFixed(1)}%</span>
          </div>
        </div>

        {/* Content Body */}
        <div className="p-5 space-y-5 overflow-y-auto max-h-[70vh]">
          {/* Real-time Recourse Outcome Cards */}
          <div className="grid grid-cols-3 gap-3">
            <div className="p-3 rounded-lg bg-surfaceRaised border border-border">
              <span className="text-[10px] uppercase font-mono text-text-muted block">Simulated Risk</span>
              <span className={`text-xl font-bold font-mono mt-0.5 block ${
                simulatedRisk >= 0.85 ? 'text-critical' : simulatedRisk >= 0.30 ? 'text-review' : 'text-cleared'
              }`}>
                {(simulatedRisk * 100).toFixed(1)}%
              </span>
              <span className="text-[10px] text-text-muted mt-0.5 block">
                {simulatedRisk < 0.30 ? '✓ Clears Model Hold' : 'Needs further easing'}
              </span>
            </div>

            <div className="p-3 rounded-lg bg-surfaceRaised border border-border">
              <span className="text-[10px] uppercase font-mono text-text-muted block">Decision Tier</span>
              <span className="text-xs font-bold font-mono mt-1 block text-text">
                {simulatedTier}
              </span>
              <span className="text-[10px] text-text-muted mt-0.5 block">
                Conformal Set Γ
              </span>
            </div>

            <div className="p-3 rounded-lg bg-surfaceRaised border border-border">
              <span className="text-[10px] uppercase font-mono text-text-muted block">Hawkes Burst Index</span>
              <span className="text-xl font-bold font-mono mt-0.5 block text-accent">
                {burstIntensity}
              </span>
              <span className="text-[10px] text-text-muted mt-0.5 block">
                Self-excitation decay
              </span>
            </div>
          </div>

          {/* Interactive Sensitivity Sliders */}
          <div className="space-y-4 bg-bg p-4 rounded-lg border border-border">
            <h4 className="font-semibold text-text text-xs uppercase font-mono tracking-wider">
              Recourse Adjustment Knobs
            </h4>

            {/* Slider 1: Transaction Amount */}
            <div className="space-y-1.5">
              <div className="flex justify-between items-center text-xs">
                <label htmlFor="recourse-tx-amount" className="text-text font-medium cursor-pointer">Single Transaction Size (USD):</label>
                <span className="font-mono font-bold text-accent">
                  ${txAmount.toLocaleString()} USD
                </span>
              </div>
              <input
                id="recourse-tx-amount"
                name="recourse-tx-amount"
                aria-label="Single Transaction Size in USD"
                type="range"
                min="2000"
                max="60000"
                step="1000"
                value={txAmount}
                onChange={(e) => setTxAmount(Number(e.target.value))}
                className="w-full h-1.5 bg-border rounded-lg appearance-none cursor-pointer accent-accent"
              />
              <div className="flex justify-between text-[10px] text-text-muted font-mono">
                <span>$2,000 (Low Velocity)</span>
                <span>$10,000 (CTR Boundary)</span>
                <span>$60,000 (High Exposure)</span>
              </div>
            </div>

            {/* Slider 2: Transfer Frequency */}
            <div className="space-y-1.5">
              <div className="flex justify-between items-center text-xs">
                <label htmlFor="recourse-tx-freq" className="text-text font-medium cursor-pointer">Hourly Transfer Frequency:</label>
                <span className="font-mono font-bold text-accent">
                  {txFrequencyPerHour} txs / hour
                </span>
              </div>
              <input
                id="recourse-tx-freq"
                name="recourse-tx-freq"
                aria-label="Hourly Transfer Frequency"
                type="range"
                min="1"
                max="12"
                step="1"
                value={txFrequencyPerHour}
                onChange={(e) => setTxFrequencyPerHour(Number(e.target.value))}
                className="w-full h-1.5 bg-border rounded-lg appearance-none cursor-pointer accent-accent"
              />
              <div className="flex justify-between text-[10px] text-text-muted font-mono">
                <span>1 tx/hr (Routine)</span>
                <span>4 tx/hr (Burst)</span>
                <span>12 tx/hr (Smurfing Fan-out)</span>
              </div>
            </div>

            {/* Slider 3: Inter-Arrival Dwell Time */}
            <div className="space-y-1.5">
              <div className="flex justify-between items-center text-xs">
                <label htmlFor="recourse-dwell-time" className="text-text font-medium cursor-pointer">Account Dwell Time (Hours held before re-transfer):</label>
                <span className="font-mono font-bold text-accent">
                  {dwellTimeHours} hours ({Math.round(dwellTimeHours * 60)} mins)
                </span>
              </div>
              <input
                id="recourse-dwell-time"
                name="recourse-dwell-time"
                aria-label="Account Dwell Time in hours"
                type="range"
                min="0.1"
                max="48.0"
                step="0.5"
                value={dwellTimeHours}
                onChange={(e) => setDwellTimeHours(Number(e.target.value))}
                className="w-full h-1.5 bg-border rounded-lg appearance-none cursor-pointer accent-accent"
              />
              <div className="flex justify-between text-[10px] text-text-muted font-mono">
                <span>0.1h (Passthrough Layering)</span>
                <span>12h (Commercial)</span>
                <span>48h (Capital Retention)</span>
              </div>
            </div>

            {/* Slider 4: Verified Trade Invoicing & Documentation Completeness */}
            <div className="space-y-1.5">
              <div className="flex justify-between items-center text-xs">
                <label htmlFor="recourse-doc-completeness" className="text-text font-medium cursor-pointer">ASYCUDA Customs Documentation Verification:</label>
                <span className="font-mono font-bold text-accent">
                  {documentCompleteness}% Complete
                </span>
              </div>
              <input
                id="recourse-doc-completeness"
                name="recourse-doc-completeness"
                aria-label="ASYCUDA Customs Documentation Verification percentage"
                type="range"
                min="10"
                max="100"
                step="5"
                value={documentCompleteness}
                onChange={(e) => setDocumentCompleteness(Number(e.target.value))}
                className="w-full h-1.5 bg-border rounded-lg appearance-none cursor-pointer accent-accent"
              />
              <div className="flex justify-between text-[10px] text-text-muted font-mono">
                <span>10% (Unverified Wire)</span>
                <span>50% (Standard Invoice)</span>
                <span>100% (ASYCUDA Customs Sealed)</span>
              </div>
            </div>
          </div>

          {/* Prescriptive Guidance Recommendation */}
          <div className="p-3 rounded-lg bg-surfaceRaised border border-border flex items-start gap-2.5">
            <CheckCircle2 className="w-4 h-4 text-cleared shrink-0 mt-0.5" />
            <div className="space-y-1">
              <span className="font-semibold text-text text-xs">Prescriptive Remediation Action:</span>
              <p className="text-[11px] text-text-2 leading-relaxed">
                To eliminate automated Tier-1 holds under Section 15 of MLPA 2012, customer must submit authenticated ASYCUDA customs declarations and maintain account dwell times of &gt;24 hours between interbank wire settlements.
              </p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 bg-surfaceRaised border-t border-border flex items-center justify-between">
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              setTxAmount(8500);
              setTxFrequencyPerHour(1);
              setDwellTimeHours(24.0);
              setDocumentCompleteness(100);
            }}
          >
            Apply Ideal Benign Preset
          </Button>

          <div className="flex items-center gap-2">
            <Button
              variant="secondary"
              size="sm"
              onClick={() => setRecourseModalOpen(false)}
            >
              Cancel
            </Button>
            <Button
              variant="primary"
              size="sm"
              onClick={handleApplyRecoursePlan}
            >
              Save Recourse Guidance
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};
