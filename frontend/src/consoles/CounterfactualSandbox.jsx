import React, { useState } from 'react';
import { 
  Sliders, 
  CheckCircle2, 
  ArrowRight, 
  ShieldAlert, 
  Sparkles, 
  RefreshCw, 
  Check,
  UserCheck,
  HelpCircle,
  PhoneCall,
  Activity,
  GitPullRequest,
  RotateCcw,
  Mail,
  ShieldCheck,
  FileCheck,
  Clock,
  DollarSign,
  Send
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { solveCounterfactual } from '../api/client';

export const CounterfactualSandbox = ({ onOpenNoticeModal }) => {
  const { currentBanker, logBankerAction } = useAuth();
  const [transferAmount, setTransferAmount] = useState(48500);
  const [holdingHours, setHoldingHours] = useState(0.4);
  const [fanInDegree, setFanInDegree] = useState(4);
  const [burstRate, setBurstRate] = useState(8.5);
  const [loading, setLoading] = useState(false);
  const [noticeSent, setNoticeSent] = useState(false);

  // Dynamic Counterfactual Anomaly Recalculation
  const isStructuring = transferAmount >= 7500 && transferAmount <= 9999;
  const isPassThrough = holdingHours < 2.0;
  const isBurst = burstRate > 3.0;
  
  let dynamicRisk = 0.05;
  if (transferAmount > 20000) dynamicRisk += 0.25;
  if (isStructuring) dynamicRisk += 0.35;
  if (isPassThrough) dynamicRisk += 0.35;
  if (isBurst) dynamicRisk += 0.25;
  if (fanInDegree >= 4) dynamicRisk += 0.15;
  dynamicRisk = Math.min(0.99, Math.max(0.01, dynamicRisk));

  const isRemediated = dynamicRisk < 0.30;

  const handleSendRemediationLetter = () => {
    logBankerAction(
      'CUSTOMER_REMEDIATION_LETTER_ISSUED',
      'Automated 4-step safe transaction retry checklist transmitted to customer portal.',
      'US-JPMC-4829-1092-8823 (Apex Global)'
    );

    setNoticeSent(true);
    setTimeout(() => setNoticeSent(false), 2500);
  };

  return (
    <div className="space-y-2.5 font-sans text-[var(--text-primary)] min-w-0">
      {/* Top Banner (Skeuomorphic) */}
      <div className="p-2.5 sm:p-3 rounded-xl skeuo-card flex flex-col md:flex-row items-start md:items-center justify-between gap-2 text-xs">
        <div className="flex items-center gap-2.5 min-w-0">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-b from-[#257843] to-[#144726] border border-[#113C21] flex items-center justify-center text-white shrink-0 shadow-[var(--skeuo-btn)]">
            <UserCheck className="w-4 h-4 text-white" />
          </div>
          <div className="min-w-0">
            <div className="flex items-center gap-1.5 flex-wrap">
              <span className="font-bold text-[var(--text-primary)] text-xs sm:text-sm block truncate">Algorithmic Recourse &amp; Customer Remediation Sandbox</span>
              <span className="text-[9px] sm:text-[10px] font-mono px-2 py-0.5 rounded font-bold bg-[var(--accent-primary)]/15 text-[var(--accent-primary)] border border-[var(--accent-primary)]/30 shadow-inner">
                Recourse Suite
              </span>
            </div>
            <p className="text-[var(--text-secondary)] text-[10px] sm:text-[11px] truncate mt-0.5">
              Simulate feature perturbations and calculate minimal recourse distances for legitimate clients.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-1.5 shrink-0">
          <span className="text-[10px] sm:text-[11px] font-mono text-[var(--accent-primary)] font-semibold bg-[var(--accent-primary)]/10 px-2.5 py-1 rounded-lg border border-[var(--accent-primary)]/20 shadow-inner">
            Pareto Frontier Active
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-12 gap-2.5 sm:gap-3">
        {/* Left Column: Interactive Perturbation Sliders */}
        <div className="xl:col-span-6 skeuo-card p-2.5 sm:p-3 space-y-2.5 font-sans">
          <div className="flex items-center justify-between pb-2 border-b border-[var(--border-subtle)]">
            <div className="flex items-center gap-1.5">
              <Sliders className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
              <h2 className="text-[11px] sm:text-xs font-bold text-[var(--text-primary)] font-mono uppercase tracking-wider">Feature Perturbation</h2>
            </div>
            <span className="badge-tier3 text-[9px] sm:text-[10px] px-2 py-0.5">
              Interactive Sliders
            </span>
          </div>

          <div className="space-y-2 text-xs">
            {/* 1. Transaction Amount Slider */}
            <div className="space-y-1.5 p-2 sm:p-2.5 rounded-xl skeuo-well">
              <div className="flex justify-between items-center text-[11px]">
                <span className="font-semibold text-[var(--text-primary)]">1. Wire Transfer Amount</span>
                <span className="font-mono text-[var(--accent-primary)] font-bold text-xs sm:text-sm">${transferAmount.toLocaleString()}</span>
              </div>
              <input
                type="range"
                min="1000"
                max="100000"
                step="500"
                value={transferAmount}
                onChange={(e) => setTransferAmount(Number(e.target.value))}
                className="w-full accent-[#1B5E34] cursor-pointer h-1.5"
              />
              <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] block">Sub-$10k transfers near $9k-$9.95k trigger structuring flags (31 U.S.C. 5324).</span>
            </div>

            {/* 2. Fund Holding Dwell Duration */}
            <div className="space-y-1.5 p-2 sm:p-2.5 rounded-xl skeuo-well">
              <div className="flex justify-between items-center text-[11px]">
                <span className="font-semibold text-[var(--text-primary)]">2. Fund Holding Dwell Duration</span>
                <span className="font-mono text-amber-700 dark:text-amber-300 font-bold text-xs sm:text-sm">{holdingHours} Hours</span>
              </div>
              <input
                type="range"
                min="0.1"
                max="72.0"
                step="0.5"
                value={holdingHours}
                onChange={(e) => setHoldingHours(Number(e.target.value))}
                className="w-full accent-amber-500 cursor-pointer h-1.5"
              />
              <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] block">Dwell times &lt;2 hours exhibit pass-through conduit behavior (Φ ≈ 1.0).</span>
            </div>

            {/* 3. Transaction Arrival Rate (Hawkes Intensity) */}
            <div className="space-y-1.5 p-2 sm:p-2.5 rounded-xl skeuo-well">
              <div className="flex justify-between items-center text-[11px]">
                <span className="font-semibold text-[var(--text-primary)]">3. Burst Arrival Velocity (λ)</span>
                <span className="font-mono text-rose-600 dark:text-rose-400 font-bold text-xs sm:text-sm">{burstRate} tx/hr</span>
              </div>
              <input
                type="range"
                min="0.5"
                max="20.0"
                step="0.5"
                value={burstRate}
                onChange={(e) => setBurstRate(Number(e.target.value))}
                className="w-full accent-rose-500 cursor-pointer h-1.5"
              />
              <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] block">High Hawkes velocity triggers Band 1 continuous temporal attention decay.</span>
            </div>
          </div>
        </div>

        {/* Right Column: Recalculated Risk Score & Safe Action Recipe */}
        <div className="xl:col-span-6 skeuo-card p-2.5 sm:p-3 space-y-2.5 flex flex-col justify-between font-sans">
          <div className="space-y-2.5">
            <div className="flex items-center justify-between pb-2 border-b border-[var(--border-subtle)]">
              <span className="text-[11px] sm:text-xs font-bold text-[var(--text-primary)] font-mono uppercase tracking-wider flex items-center gap-1.5">
                <Activity className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                <span>Simulated Recourse Result</span>
              </span>
              <span className={`text-[9px] sm:text-[10px] font-mono px-2 py-0.5 rounded-full font-bold border ${
                isRemediated ? 'badge-tier3' : 'badge-tier1'
              }`}>
                {isRemediated ? 'SAFE TO CLEAR' : 'RESTRICTION MAINTAINED'}
              </span>
            </div>

            {/* Recalculated Risk Comparison Card */}
            <div className="p-2.5 sm:p-3 rounded-xl skeuo-well grid grid-cols-2 gap-2 font-mono text-center">
              <div>
                <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] block uppercase">ORIGINAL BASE RISK</span>
                <span className="text-xl sm:text-2xl font-black text-rose-600 dark:text-rose-400">94.0%</span>
                <span className="text-[9px] sm:text-[10px] text-rose-600/80 dark:text-rose-300 block mt-0.5">Tier 1 Hold</span>
              </div>
              <div className="border-l border-[var(--border-subtle)] pl-2">
                <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] block uppercase">SIMULATED RECOURSE</span>
                <span className={`text-xl sm:text-2xl font-black ${isRemediated ? 'text-[var(--accent-primary)]' : 'text-amber-600 dark:text-amber-300'}`}>
                  {(dynamicRisk * 100).toFixed(1)}%
                </span>
                <span className="text-[9px] sm:text-[10px] text-[var(--text-secondary)] block mt-0.5">
                  {isRemediated ? 'Tier 3 Clear (<30%)' : 'Tier 2 Review Queue'}
                </span>
              </div>
            </div>

            {/* Actionable Customer Remediation Steps */}
            <div className="space-y-1.5 text-xs">
              <span className="font-bold text-[var(--text-primary)] font-mono text-[11px] block">Actionable Safe Settlement Checklist:</span>
              <ul className="space-y-1.5 text-[var(--text-secondary)] text-[10px] sm:text-[11px]">
                <li className="flex items-start gap-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5 text-[var(--accent-primary)] shrink-0 mt-0.5" />
                  <span>Consolidate sub-transfers into a single invoice-backed batch settlement.</span>
                </li>
                <li className="flex items-start gap-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5 text-[var(--accent-primary)] shrink-0 mt-0.5" />
                  <span>Maintain funds in clearing balance &ge; 24 hours to break conduit signature.</span>
                </li>
                <li className="flex items-start gap-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5 text-[var(--accent-primary)] shrink-0 mt-0.5" />
                  <span>Upload validated trade Bill of Lading or verified commercial contracts.</span>
                </li>
              </ul>
            </div>
          </div>

          {/* Issue Notice Action Button */}
          <div className="pt-2 border-t border-[var(--border-subtle)] flex items-center justify-between gap-2">
            <span className="text-[10px] sm:text-[11px] font-mono text-[var(--text-muted)] truncate">
              Officer: <strong className="text-[var(--text-primary)]">{currentBanker.name}</strong>
            </span>

            <button
              onClick={handleSendRemediationLetter}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg skeuo-btn skeuo-btn-success text-[10px] sm:text-[11px] font-bold shrink-0"
            >
              {noticeSent ? <CheckCircle2 className="w-3.5 h-3.5" /> : <Mail className="w-3.5 h-3.5" />}
              <span>{noticeSent ? 'Remediation Transmitted!' : 'Send Safe Advice'}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
