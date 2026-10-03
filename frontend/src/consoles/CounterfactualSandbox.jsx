import React, { useState } from 'react';
import { 
  Sliders, 
  CheckCircle2, 
  AlertTriangle,
  ArrowRight, 
  ShieldAlert, 
  Sparkles, 
  RefreshCw, 
  Check,
  UserCheck,
  HelpCircle,
  Activity,
  GitPullRequest,
  RotateCcw,
  Mail,
  ShieldCheck,
  FileCheck,
  Clock,
  DollarSign,
  Send,
  Lock,
  Layers,
  BarChart3,
  Users
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const CounterfactualSandbox = ({ onOpenNoticeModal }) => {
  const { currentBanker, logBankerAction } = useAuth();
  const [activeTab, setActiveTab] = useState('ANALYST_PERTURBATION'); // 'ANALYST_PERTURBATION' | 'THRESHOLD_TUNING'
  
  // Tab 1: Feature Perturbation State
  const [transferAmount, setTransferAmount] = useState(48500);
  const [holdingHours, setHoldingHours] = useState(0.4);
  const [fanInDegree, setFanInDegree] = useState(4);
  const [burstRate, setBurstRate] = useState(8.5);
  const [rfiGenerated, setRfiGenerated] = useState(false);

  // Tab 2: Policy Threshold & Capacity Tuning State
  const [alphaThreshold, setAlphaThreshold] = useState(0.01); // 1% error rate
  const [dwellThreshold, setDwellThreshold] = useState(2.0); // hours
  const [structuringFloor, setStructuringFloor] = useState(9000); // USD
  const [policyStaged, setPolicyStaged] = useState(false);

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

  // Corrected Tier Classification Logic
  let simulatedTier = 'Tier 3 Clear (<30%)';
  let tierBadgeClass = 'badge-tier3';
  let tierStatus = 'SAFE TO CLEAR';

  if (dynamicRisk >= 0.85) {
    simulatedTier = 'Tier 1 Hold (Quarantine)';
    tierBadgeClass = 'badge-tier1';
    tierStatus = 'QUARANTINE ENFORCED';
  } else if (dynamicRisk >= 0.30) {
    simulatedTier = 'Tier 2 Analyst Review';
    tierBadgeClass = 'badge-tier2';
    tierStatus = 'MANUAL REVIEW REQUIRED';
  }

  const isRemediated = dynamicRisk < 0.30;

  // Threshold Simulation Calculations (Total 24h tx: 148,312)
  const totalTx24h = 148312;
  // Baseline: at alpha=0.01, quarantine rate is ~0.86% (1,280 alerts)
  const simulatedQuarantineRate = (0.86 * (alphaThreshold / 0.01) * (dwellThreshold / 2.0)).toFixed(2);
  const projectedAlertVolume = Math.round(totalTx24h * (parseFloat(simulatedQuarantineRate) / 100));
  const bankAnalystCapacity = 2100; // 14 analysts * 150 reviews/day
  const capacityUtilization = ((projectedAlertVolume / bankAnalystCapacity) * 100).toFixed(1);
  const projectedRecall = (99.8 - (alphaThreshold * 80)).toFixed(1);
  const projectedPrecision = (91.0 + (alphaThreshold * 200)).toFixed(1);

  const handleGenerateRFIPackage = () => {
    logBankerAction(
      'COMPLIANT_RFI_PACKAGE_GENERATED',
      `Internal analyst compiled Form RFI-1092 with commercial invoice and Bill of Lading requirements. (Confidential under 31 U.S.C. § 5318(g)(2)).`,
      'US-JPMC-4829-1092-8823 (Apex Global)'
    );

    setRfiGenerated(true);
    setTimeout(() => {
      setRfiGenerated(false);
      if (onOpenNoticeModal) {
        onOpenNoticeModal();
      }
    }, 1200);
  };

  const handleStagePolicyUpdate = () => {
    logBankerAction(
      'AML_POLICY_THRESHOLD_CHANGE_STAGED',
      `Staged threshold update: alpha=${alphaThreshold}, dwell=${dwellThreshold}h, structuringFloor=$${structuringFloor}. Pending CCO Four-Eyes dual-approval.`,
      'Global Policy Ruleset v4.2'
    );
    setPolicyStaged(true);
    setTimeout(() => setPolicyStaged(false), 2500);
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
              <span className="font-bold text-[var(--text-primary)] text-xs sm:text-sm block truncate">
                Remediation &amp; Policy Simulation Hub
              </span>
              <span className="text-[9px] sm:text-[10px] font-mono px-2 py-0.5 rounded font-bold bg-amber-500/15 text-amber-700 dark:text-amber-300 border border-amber-500/30">
                Internal Analyst Console
              </span>
            </div>
            <p className="text-[var(--text-secondary)] text-[10px] sm:text-[11px] truncate mt-0.5">
              Simulate feature perturbations, evaluate RFI clearing conditions, and stress-test threshold policies under 31 U.S.C. § 5318(g)(2) confidentiality.
            </p>
          </div>
        </div>

        {/* Tab Switcher */}
        <div className="flex items-center gap-1 p-1 bg-[var(--bg-well)] rounded-lg border border-[var(--border-subtle)] shrink-0 font-mono text-[10px]">
          <button
            onClick={() => setActiveTab('ANALYST_PERTURBATION')}
            className={`px-2.5 py-1 rounded-md transition-all cursor-pointer flex items-center gap-1.5 ${
              activeTab === 'ANALYST_PERTURBATION'
                ? 'bg-gradient-to-b from-[#257843] to-[#144726] text-white font-bold shadow-[var(--skeuo-btn)]'
                : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
            }`}
          >
            <Sliders className="w-3 h-3" />
            <span>Case Perturbation</span>
          </button>
          <button
            onClick={() => setActiveTab('THRESHOLD_TUNING')}
            className={`px-2.5 py-1 rounded-md transition-all cursor-pointer flex items-center gap-1.5 ${
              activeTab === 'THRESHOLD_TUNING'
                ? 'bg-gradient-to-b from-[#257843] to-[#144726] text-white font-bold shadow-[var(--skeuo-btn)]'
                : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
            }`}
          >
            <BarChart3 className="w-3 h-3" />
            <span>Policy &amp; Capacity Tuning</span>
          </button>
        </div>
      </div>

      {/* Strict Anti-Tipping-Off Safeguard Banner */}
      <div className="p-2 sm:p-2.5 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-start gap-2.5 text-xs">
        <Lock className="w-4 h-4 text-rose-500 shrink-0 mt-0.5" />
        <div className="text-[10px] sm:text-[11px] text-rose-800 dark:text-rose-200 leading-tight">
          <strong className="font-mono uppercase font-bold">Confidential Internal Investigation Tool (31 U.S.C. § 5318(g)(2)):</strong>
          <span className="block mt-0.5 text-rose-900/80 dark:text-rose-300/80">
            Perturbation hypotheses and threshold triggers must NEVER be shared with customers or outside parties. Customer contact must solely use verified Request for Information (RFI) document workflows.
          </span>
        </div>
      </div>

      {activeTab === 'ANALYST_PERTURBATION' ? (
        <div className="grid grid-cols-1 xl:grid-cols-12 gap-2.5 sm:gap-3">
          {/* Left Column: Interactive Perturbation Sliders */}
          <div className="xl:col-span-6 skeuo-card p-2.5 sm:p-3 space-y-2.5 font-sans">
            <div className="flex items-center justify-between pb-2 border-b border-[var(--border-subtle)]">
              <div className="flex items-center gap-1.5">
                <Sliders className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                <h2 className="text-[11px] sm:text-xs font-bold text-[var(--text-primary)] font-mono uppercase tracking-wider">Internal Hypothesis Testing</h2>
              </div>
              <span className="badge-tier2 text-[9px] sm:text-[10px] px-2 py-0.5">
                Target: US-JPMC-4829 (Apex Global)
              </span>
            </div>

            <div className="space-y-2 text-xs">
              {/* 1. Transaction Amount Slider */}
              <div className="space-y-1.5 p-2 sm:p-2.5 rounded-xl skeuo-well">
                <div className="flex justify-between items-center text-[11px]">
                  <span className="font-semibold text-[var(--text-primary)]">1. Aggregate Transfer Exposure</span>
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
                <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] block">Amounts between $7,500 and $9,999 trip federal structuring tripwires. Baseline wash: $48,500.</span>
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
                <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] block">Dwell times &lt;2 hours exhibit rapid conduit pass-through behavior (Φ ≈ 1.0).</span>
              </div>

              {/* 3. Transaction Arrival Rate (Hawkes Intensity) */}
              <div className="space-y-1.5 p-2 sm:p-2.5 rounded-xl skeuo-well">
                <div className="flex justify-between items-center text-[11px]">
                  <span className="font-semibold text-[var(--text-primary)]">3. Arrival Burst Velocity (λ)</span>
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
                <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] block">Cluster velocities &gt;3 tx/hr trigger temporal Hawkes anomaly filters.</span>
              </div>

              {/* 4. Fan-In Degree */}
              <div className="space-y-1.5 p-2 sm:p-2.5 rounded-xl skeuo-well">
                <div className="flex justify-between items-center text-[11px]">
                  <span className="font-semibold text-[var(--text-primary)]">4. Inbound Source Fan-In Degree</span>
                  <span className="font-mono text-[var(--accent-primary)] font-bold text-xs sm:text-sm">{fanInDegree} Source Nodes</span>
                </div>
                <input
                  type="range"
                  min="1"
                  max="10"
                  step="1"
                  value={fanInDegree}
                  onChange={(e) => setFanInDegree(Number(e.target.value))}
                  className="w-full accent-[#1B5E34] cursor-pointer h-1.5"
                />
                <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] block">Multiple unlinked remitters routing into a single hub indicate mule gathering.</span>
              </div>
            </div>
          </div>

          {/* Right Column: Recalculated Risk Score & RFI Verification Steps */}
          <div className="xl:col-span-6 skeuo-card p-2.5 sm:p-3 space-y-2.5 flex flex-col justify-between font-sans">
            <div className="space-y-2.5">
              <div className="flex items-center justify-between pb-2 border-b border-[var(--border-subtle)]">
                <span className="text-[11px] sm:text-xs font-bold text-[var(--text-primary)] font-mono uppercase tracking-wider flex items-center gap-1.5">
                  <Activity className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                  <span>Simulated Policy Disposition</span>
                </span>
                <span className={`text-[9px] sm:text-[10px] font-mono px-2 py-0.5 rounded-full font-bold border ${tierBadgeClass}`}>
                  {tierStatus}
                </span>
              </div>

              {/* Corrected Recalculated Risk Comparison Card */}
              <div className="p-2.5 sm:p-3 rounded-xl skeuo-well grid grid-cols-2 gap-2 font-mono text-center">
                <div>
                  <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] block uppercase">ORIGINAL BASE RISK</span>
                  <span className="text-xl sm:text-2xl font-black text-rose-600 dark:text-rose-400">94.0%</span>
                  <span className="text-[9px] sm:text-[10px] text-rose-600/80 dark:text-rose-300 block mt-0.5">Tier 1 Hold</span>
                </div>
                <div className="border-l border-[var(--border-subtle)] pl-2">
                  <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] block uppercase">SIMULATED RISK</span>
                  <span className={`text-xl sm:text-2xl font-black ${
                    dynamicRisk >= 0.85 
                      ? 'text-rose-600 dark:text-rose-400' 
                      : dynamicRisk >= 0.30 
                        ? 'text-amber-600 dark:text-amber-300' 
                        : 'text-[var(--accent-primary)]'
                  }`}>
                    {(dynamicRisk * 100).toFixed(1)}%
                  </span>
                  <span className={`text-[9px] sm:text-[10px] block mt-0.5 font-bold ${
                    dynamicRisk >= 0.85 
                      ? 'text-rose-600 dark:text-rose-400' 
                      : dynamicRisk >= 0.30 
                        ? 'text-amber-600 dark:text-amber-300' 
                        : 'text-[var(--accent-primary)]'
                  }`}>
                    {simulatedTier}
                  </span>
                </div>
              </div>

              {/* Compliant RFI Verification Package Checklist */}
              <div className="space-y-1.5 text-xs">
                <span className="font-bold text-[var(--text-primary)] font-mono text-[11px] block">
                  Mandatory Clearing Evidence Checklist (RFI Form 1092):
                </span>
                <ul className="space-y-1.5 text-[var(--text-secondary)] text-[10px] sm:text-[11px]">
                  <li className="flex items-start gap-1.5">
                    <FileCheck className="w-3.5 h-3.5 text-[var(--accent-primary)] shrink-0 mt-0.5" />
                    <span>Commercial invoice matching $48,500 total exposure with matching buyer Purchase Order.</span>
                  </li>
                  <li className="flex items-start gap-1.5">
                    <FileCheck className="w-3.5 h-3.5 text-[var(--accent-primary)] shrink-0 mt-0.5" />
                    <span>Customs declaration / carrier Bill of Lading confirming physical cargo movement.</span>
                  </li>
                  <li className="flex items-start gap-1.5">
                    <FileCheck className="w-3.5 h-3.5 text-[var(--accent-primary)] shrink-0 mt-0.5" />
                    <span>Ultimate Beneficial Ownership (UBO) declaration for all entities holding &ge; 25% equity.</span>
                  </li>
                  <li className="flex items-start gap-1.5">
                    <FileCheck className="w-3.5 h-3.5 text-[var(--accent-primary)] shrink-0 mt-0.5" />
                    <span>Source of Wealth declaration verifying legitimate commercial operating cash flow.</span>
                  </li>
                </ul>
              </div>
            </div>

            {/* Compliant Action Buttons */}
            <div className="pt-2 border-t border-[var(--border-subtle)] flex items-center justify-between gap-2">
              <span className="text-[10px] sm:text-[11px] font-mono text-[var(--text-muted)] truncate">
                Case Officer: <strong className="text-[var(--text-primary)]">{currentBanker.name}</strong>
              </span>

              <button
                onClick={handleGenerateRFIPackage}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg skeuo-btn skeuo-btn-primary text-[10px] sm:text-[11px] font-bold shrink-0 cursor-pointer"
              >
                {rfiGenerated ? <CheckCircle2 className="w-3.5 h-3.5 text-white" /> : <Mail className="w-3.5 h-3.5" />}
                <span>{rfiGenerated ? 'RFI Dispatched to Case' : 'Generate Compliant RFI Package'}</span>
              </button>
            </div>
          </div>
        </div>
      ) : (
        /* Tab 2: Policy Threshold & Analyst Capacity Tuning (Compliance Manager What-If Simulator) */
        <div className="grid grid-cols-1 xl:grid-cols-12 gap-2.5 sm:gap-3">
          {/* Left Column: Threshold Parameters */}
          <div className="xl:col-span-6 skeuo-card p-2.5 sm:p-3 space-y-2.5 font-sans">
            <div className="flex items-center justify-between pb-2 border-b border-[var(--border-subtle)]">
              <div className="flex items-center gap-1.5">
                <Sliders className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                <h2 className="text-[11px] sm:text-xs font-bold text-[var(--text-primary)] font-mono uppercase tracking-wider">Policy Threshold Simulator</h2>
              </div>
              <span className="badge-tier3 text-[9px] sm:text-[10px] px-2 py-0.5">
                MLRO Management Mode
              </span>
            </div>

            <p className="text-[10px] text-[var(--text-secondary)]">
              Simulate enterprise-wide threshold changes against historical 24h baseline (148,312 transactions) to calibrate alert volume to analyst capacity.
            </p>

            <div className="space-y-2 text-xs">
              {/* Alpha Threshold */}
              <div className="space-y-1.5 p-2 sm:p-2.5 rounded-xl skeuo-well">
                <div className="flex justify-between items-center text-[11px]">
                  <span className="font-semibold text-[var(--text-primary)]">Conformal Significance Level (&alpha;)</span>
                  <span className="font-mono text-[var(--accent-primary)] font-bold text-xs sm:text-sm">&alpha; = {alphaThreshold} ({(alphaThreshold * 100).toFixed(1)}%)</span>
                </div>
                <input
                  type="range"
                  min="0.005"
                  max="0.05"
                  step="0.005"
                  value={alphaThreshold}
                  onChange={(e) => setAlphaThreshold(Number(e.target.value))}
                  className="w-full accent-[#1B5E34] cursor-pointer h-1.5"
                />
                <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] block">Mathematical coverage guarantee: At most {(alphaThreshold * 100).toFixed(1)}% of true positives are missed on average.</span>
              </div>

              {/* Conduit Dwell Time Threshold */}
              <div className="space-y-1.5 p-2 sm:p-2.5 rounded-xl skeuo-well">
                <div className="flex justify-between items-center text-[11px]">
                  <span className="font-semibold text-[var(--text-primary)]">Conduit Dwell Time Floor</span>
                  <span className="font-mono text-amber-700 dark:text-amber-300 font-bold text-xs sm:text-sm">{dwellThreshold} Hours</span>
                </div>
                <input
                  type="range"
                  min="0.5"
                  max="6.0"
                  step="0.5"
                  value={dwellThreshold}
                  onChange={(e) => setDwellThreshold(Number(e.target.value))}
                  className="w-full accent-amber-500 cursor-pointer h-1.5"
                />
                <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] block">Transfers holding funds less than this floor trip rapid pass-through heuristic flags.</span>
              </div>

              {/* Structuring Proximity Threshold */}
              <div className="space-y-1.5 p-2 sm:p-2.5 rounded-xl skeuo-well">
                <div className="flex justify-between items-center text-[11px]">
                  <span className="font-semibold text-[var(--text-primary)]">Structuring Detection Window</span>
                  <span className="font-mono text-rose-600 dark:text-rose-400 font-bold text-xs sm:text-sm">${structuringFloor.toLocaleString()} &ndash; $9,999</span>
                </div>
                <input
                  type="range"
                  min="7000"
                  max="9800"
                  step="200"
                  value={structuringFloor}
                  onChange={(e) => setStructuringFloor(Number(e.target.value))}
                  className="w-full accent-rose-500 cursor-pointer h-1.5"
                />
                <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] block">Sub-$10k transfers in this range are flagged for CTR evasion pattern analysis.</span>
              </div>
            </div>
          </div>

          {/* Right Column: Capacity & Workload Impact */}
          <div className="xl:col-span-6 skeuo-card p-2.5 sm:p-3 space-y-2.5 flex flex-col justify-between font-sans">
            <div className="space-y-2.5">
              <div className="flex items-center justify-between pb-2 border-b border-[var(--border-subtle)]">
                <span className="text-[11px] sm:text-xs font-bold text-[var(--text-primary)] font-mono uppercase tracking-wider flex items-center gap-1.5">
                  <Users className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                  <span>Analyst Capacity &amp; Workload Impact</span>
                </span>
                <span className={`text-[9px] sm:text-[10px] font-mono px-2 py-0.5 rounded-full font-bold border ${
                  parseFloat(capacityUtilization) > 100 ? 'badge-tier1' : 'badge-tier3'
                }`}>
                  {parseFloat(capacityUtilization) > 100 ? 'CAPACITY OVERLOAD' : 'WORKLOAD SUSTAINABLE'}
                </span>
              </div>

              {/* Capacity Metrics Grid */}
              <div className="grid grid-cols-2 gap-2 font-mono text-center">
                <div className="p-2 rounded-xl skeuo-well">
                  <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] block uppercase">SIMULATED QUARANTINE RATE</span>
                  <span className="text-xl sm:text-2xl font-black text-rose-600 dark:text-rose-400">{simulatedQuarantineRate}%</span>
                  <span className="text-[9px] sm:text-[10px] text-[var(--text-secondary)] block mt-0.5">{projectedAlertVolume.toLocaleString()} alerts / 24h</span>
                </div>
                <div className="p-2 rounded-xl skeuo-well">
                  <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] block uppercase">CAPACITY UTILIZATION</span>
                  <span className={`text-xl sm:text-2xl font-black ${parseFloat(capacityUtilization) > 100 ? 'text-rose-600 dark:text-rose-400' : 'text-[var(--accent-primary)]'}`}>
                    {capacityUtilization}%
                  </span>
                  <span className="text-[9px] sm:text-[10px] text-[var(--text-secondary)] block mt-0.5">Cap: {bankAnalystCapacity} reviews/day</span>
                </div>
              </div>

              {/* Statistical Performance Tradeoff */}
              <div className="p-2 rounded-xl skeuo-well space-y-1 text-xs">
                <div className="flex justify-between items-center text-[10px]">
                  <span className="text-[var(--text-secondary)]">Projected True Detection Recall:</span>
                  <span className="font-mono font-bold text-[var(--accent-primary)]">{projectedRecall}%</span>
                </div>
                <div className="flex justify-between items-center text-[10px]">
                  <span className="text-[var(--text-secondary)]">Projected Alert Precision:</span>
                  <span className="font-mono font-bold text-blue-600 dark:text-blue-400">{projectedPrecision}%</span>
                </div>
                <div className="flex justify-between items-center text-[10px]">
                  <span className="text-[var(--text-secondary)]">Straight-Through Processing (STP) Rate:</span>
                  <span className="font-mono font-bold text-[var(--accent-primary)]">{(100 - parseFloat(simulatedQuarantineRate)).toFixed(2)}%</span>
                </div>
              </div>

              <p className="text-[9px] text-[var(--text-muted)] italic">
                * Tuning alpha allows compliance teams to trade marginal false positives against analyst review capacity while preserving strict regulatory coverage under SR 11-7 model risk governance.
              </p>
            </div>

            {/* Stage Policy Button */}
            <div className="pt-2 border-t border-[var(--border-subtle)] flex items-center justify-between gap-2">
              <button
                onClick={() => {
                  setAlphaThreshold(0.01);
                  setDwellThreshold(2.0);
                  setStructuringFloor(9000);
                }}
                className="px-2.5 py-1.5 rounded-lg skeuo-btn skeuo-btn-secondary text-[10px] font-mono flex items-center gap-1 cursor-pointer"
              >
                <RotateCcw className="w-3 h-3" />
                <span>Reset to Baseline</span>
              </button>

              <button
                onClick={handleStagePolicyUpdate}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg skeuo-btn skeuo-btn-primary text-[10px] sm:text-[11px] font-bold shrink-0 cursor-pointer"
              >
                {policyStaged ? <Check className="w-3.5 h-3.5" /> : <ShieldCheck className="w-3.5 h-3.5" />}
                <span>{policyStaged ? 'Policy Staged for Four-Eyes Sign-Off' : 'Stage Policy (Dual-Approval Required)'}</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
