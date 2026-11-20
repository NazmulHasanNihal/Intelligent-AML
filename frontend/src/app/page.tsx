'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import {
  ShieldAlert,
  Clock,
  CheckCircle2,
  AlertTriangle,
  ArrowUpRight,
  TrendingUp,
  Zap,
  Play,
  Pause,
  Layers,
  Search,
  Activity,
  FileText,
  ExternalLink,
  ChevronRight,
  HelpCircle,
  Building,
  DollarSign
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { RAW_TELEMETRY, DERIVED_METRICS, SEEDED_ALERTS } from '@/lib/seedData';
import { PiiText } from '@/components/ui/PiiText';

export default function SurveillanceOverviewPage() {
  const {
    isLiveStreamActive,
    toggleLiveStream,
    streamSpeed,
    setStreamSpeed,
    jurisdiction,
    setFourEyesModalOpen,
    liveTransactions,
    session
  } = useBankingStore();

  // C-STGB Sandbox State
  const [testAmount, setTestAmount] = useState<number>(9450);
  const [testRail, setTestRail] = useState<string>('SWIFT MT700 (LC)');
  const [testPriceDev, setTestPriceDev] = useState<number>(333.7);
  const [isScoring, setIsScoring] = useState<boolean>(false);
  const [scoringResult, setScoringResult] = useState<any>(null);

  const handleRunSandboxScore = async () => {
    setIsScoring(true);
    try {
      const res = await fetch('/api/v1/score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          amount: Number(testAmount),
          sourceAccount: 'BD22-EBLB-4829-1092-8823',
          targetAccount: 'AE-EBIL-4412-8819-3301',
          rail: testRail,
          tbmlData: {
            declaredUnitValuation: 42.50,
            benchmarkValuation: 9.80,
            hsCode: 'HS 5201.00'
          }
        })
      });
      const data = await res.json();
      setScoringResult(data);
    } catch (err) {
      console.error('Scoring error:', err);
    } finally {
      setIsScoring(false);
    }
  };

  const urgentAlerts = SEEDED_ALERTS.filter(a => a.tierCode === 1).slice(0, 3);

  return (
    <div className="p-4 sm:p-5 lg:p-6 max-w-[1700px] mx-auto space-y-5 sm:space-y-6">
      {/* Air-Gap Intranet Telemetry Watermark & Live Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 sm:gap-4 p-3.5 sm:p-4 bg-[#0F172A] border border-[#1E293B] rounded-xl text-xs text-slate-300">
        <div className="flex items-start sm:items-center gap-2.5 sm:gap-3 min-w-0">
          <div className="relative flex items-center justify-center w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 shrink-0">
            <Activity className="w-4 h-4 animate-pulse" />
          </div>
          <div className="min-w-0">
            <div className="flex flex-wrap items-center gap-1.5 sm:gap-2">
              <span className="font-semibold text-slate-100 uppercase tracking-wide truncate text-xs">
                Air-Gap Verified Intranet Node
              </span>
              <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 shrink-0">
                0 EXTERNAL EGRESS
              </span>
            </div>
            <p className="text-[11px] text-slate-400 mt-0.5 break-words">
              Active Regulatory Profile: <strong className="text-slate-200">{jurisdiction}</strong> | CRC &alpha;=0.01 (&ge; 99.0%)
            </p>
          </div>
        </div>

        {/* Live Ingestion Stream Controls */}
        <div className="flex items-center gap-2 sm:gap-3 bg-[#0B0F17] px-3 py-1.5 rounded-lg border border-[#334155] shrink-0 self-start sm:self-auto">
          <span className="text-[11px] font-medium text-slate-400">Stream:</span>
          <button
            onClick={toggleLiveStream}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded text-xs font-semibold transition-all cursor-pointer ${
              isLiveStreamActive
                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 hover:bg-emerald-500/30'
                : 'bg-amber-500/20 text-amber-300 border border-amber-500/30 hover:bg-amber-500/30'
            }`}
          >
            {isLiveStreamActive ? (
              <>
                <Pause className="w-3.5 h-3.5" />
                <span>Running</span>
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5" />
                <span>Paused</span>
              </>
            )}
          </button>

          <div className="flex items-center border-l border-[#334155] pl-2 gap-1 font-mono text-[11px]">
            {([1, 2, 5] as const).map((spd) => (
              <button
                key={spd}
                onClick={() => setStreamSpeed(spd)}
                className={`px-1.5 py-0.5 rounded cursor-pointer ${
                  streamSpeed === spd
                    ? 'bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/40'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {spd}x
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* 4-Card Tactical KPI Ribbon */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: 24h Monitored Volume */}
        <div className="p-5 bg-[#0F172A] border border-[#1E293B] rounded-xl hover:border-[#334155] transition-all h-full flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-slate-400 mb-2">
              <span className="text-xs font-semibold tracking-wide uppercase">24h Monitored Volume</span>
              <TrendingUp className="w-4 h-4 text-emerald-400" />
            </div>
            <div className="text-2xl font-bold font-mono text-slate-100 tabular-nums">
              $1.42B
            </div>
          </div>
          <div>
            <div className="flex items-center justify-between mt-3 pt-2.5 border-t border-[#1E293B] text-[11px] text-slate-400">
              <span>Total Transactions:</span>
              <span className="font-mono text-slate-200 tabular-nums">{RAW_TELEMETRY.totalProcessed24h.toLocaleString()}</span>
            </div>
            <div className="flex items-center justify-between text-[11px] text-slate-400 mt-1">
              <span>Peak Velocity:</span>
              <span className="font-mono text-emerald-400 tabular-nums">{RAW_TELEMETRY.peakThroughputTxPerSec} tx/sec</span>
            </div>
          </div>
        </div>

        {/* Card 2: Tier 1 Quarantined (Hold) */}
        <div className="p-5 bg-[#0F172A] border border-rose-900/40 rounded-xl hover:border-rose-700/60 transition-all bg-gradient-to-b from-rose-950/20 to-transparent h-full flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-rose-400 mb-2">
              <span className="text-xs font-semibold tracking-wide uppercase flex items-center gap-1.5">
                <ShieldAlert className="w-4 h-4 text-rose-500" />
                Tier 1 Quarantined
              </span>
              <span className="px-1.5 py-0.5 rounded text-[10px] font-mono font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">
                SLA 60m
              </span>
            </div>
            <div className="text-2xl font-bold font-mono text-rose-300 tabular-nums">
              {RAW_TELEMETRY.tier1Quarantined.toLocaleString()}
            </div>
          </div>
          <div>
            <div className="flex items-center justify-between mt-3 pt-2.5 border-t border-rose-900/30 text-[11px] text-slate-400">
              <span>Quarantine Rate:</span>
              <span className="font-mono text-rose-400 font-semibold tabular-nums">{DERIVED_METRICS.quarantineRate}%</span>
            </div>
            <div className="flex items-center justify-between text-[11px] text-slate-400 mt-1">
              <span>Guaranteed Gate:</span>
              <span className="font-mono text-slate-200">Γ = &#123;1&#125; (100% Hold)</span>
            </div>
          </div>
        </div>

        {/* Card 3: Tier 2 Officer Review (Ambiguity - Human Workload Highlighted) */}
        <div className="p-5 bg-[#0F172A] border border-amber-500/50 border-l-4 border-l-amber-500 rounded-xl hover:border-amber-400 transition-all bg-gradient-to-b from-amber-950/30 to-transparent shadow-lg shadow-amber-950/20 h-full flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-amber-300 mb-2">
              <span className="text-xs font-bold tracking-wide uppercase flex items-center gap-1.5">
                <Clock className="w-4 h-4 text-amber-400" />
                Tier 2 Officer Review
              </span>
              <span className="px-1.5 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-500/25 text-amber-200 border border-amber-500/40">
                SLA 4h • Action Req
              </span>
            </div>
            <div className="text-2xl font-bold font-mono text-amber-300 tabular-nums">
              {RAW_TELEMETRY.tier2ReviewQueue.toLocaleString()}
            </div>
          </div>
          <div>
            <div className="flex items-center justify-between mt-3 pt-2.5 border-t border-amber-900/40 text-[11px] text-slate-400">
              <span>Review Escalation Rate:</span>
              <span className="font-mono text-amber-400 font-semibold tabular-nums">{DERIVED_METRICS.reviewRate}%</span>
            </div>
            <div className="flex items-center justify-between text-[11px] text-slate-400 mt-1">
              <span>Conformal Ambiguity:</span>
              <span className="font-mono text-amber-200 font-bold">Γ = &#123;0, 1&#125; (Human Triage)</span>
            </div>
          </div>
        </div>

        {/* Card 4: Tier 3 Auto-Cleared (STP) */}
        <div className="p-5 bg-[#0F172A] border border-emerald-900/40 rounded-xl hover:border-emerald-700/60 transition-all bg-gradient-to-b from-emerald-950/20 to-transparent h-full flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-emerald-400 mb-2">
              <span className="text-xs font-semibold tracking-wide uppercase flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                Tier 3 Auto-Cleared
              </span>
              <span className="px-1.5 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                98.6% STP
              </span>
            </div>
            <div className="text-2xl font-bold font-mono text-emerald-300 tabular-nums">
              {RAW_TELEMETRY.tier3AutoCleared.toLocaleString()}
            </div>
          </div>
          <div>
            <div className="flex items-center justify-between mt-3 pt-2.5 border-t border-emerald-900/30 text-[11px] text-slate-400">
              <span>Straight-Through Processing:</span>
              <span className="font-mono text-emerald-400 font-semibold tabular-nums">{DERIVED_METRICS.stpRate}%</span>
            </div>
            <div className="flex items-center justify-between text-[11px] text-slate-400 mt-1">
              <span>Statistical Guarantee:</span>
              <span className="font-mono text-slate-200">Coverage ≥ 99.0%</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Grid: Urgent Attention Queue & C-STGB Scoring Sandbox */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Urgent Action Queue (7 Cols) */}
        <div className="lg:col-span-7 bg-[#0F172A] border border-[#1E293B] rounded-xl overflow-hidden">
          <div className="flex items-center justify-between px-5 py-3.5 border-b border-[#1E293B] bg-[#0B0F17]/50">
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-rose-500" />
              <h2 className="text-sm font-semibold text-slate-100">
                Urgent Action Queue — High-Risk Breaches
              </h2>
            </div>
            <Link
              href="/triage"
              className="flex items-center gap-1 text-xs text-emerald-400 hover:text-emerald-300 font-medium"
            >
              <span>View All Alerts ({RAW_TELEMETRY.tier1Quarantined + RAW_TELEMETRY.tier2ReviewQueue})</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="divide-y divide-[#1E293B]">
            {urgentAlerts.map((alert) => (
              <div key={alert.id} className="p-4 hover:bg-[#1E293B]/40 transition-colors">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="px-2 py-0.5 rounded text-[11px] font-mono font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">
                        {alert.tier}
                      </span>
                      <span className="font-mono text-xs font-bold text-slate-200">{alert.id}</span>
                      <span className="text-[11px] text-slate-400 font-mono">[{alert.rail}]</span>
                    </div>

                    <h3 className="text-sm font-semibold text-slate-100 mt-1 flex items-center gap-2">
                      <Building className="w-3.5 h-3.5 text-slate-400" />
                      {alert.entityName}
                    </h3>

                    <div className="text-xs text-slate-400 mt-0.5 flex items-center gap-2">
                      <span>Account:</span>
                      <PiiText value={alert.account} type="account" className="text-slate-300 font-mono text-[11px]" />
                    </div>

                    <p className="text-xs text-slate-300 mt-2 line-clamp-2 bg-[#0B0F17] p-2 rounded border border-[#1E293B]">
                      {alert.whyFlagged}
                    </p>
                  </div>

                  <div className="text-right shrink-0">
                    <div className="text-base font-bold font-mono text-rose-400">
                      ${alert.amount.toLocaleString(undefined, { minimumFractionDigits: 2 })}
                    </div>
                    <div className="text-[11px] font-mono text-slate-400 mt-0.5">
                      ৳{alert.amountBdt.toLocaleString()} BDT
                    </div>
                    <div className="mt-2 inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono bg-amber-500/10 text-amber-300 border border-amber-500/20">
                      <Clock className="w-3 h-3" />
                      <span>SLA: {alert.slaMinutesLeft}m left</span>
                    </div>
                  </div>
                </div>

                {/* Quick Action Footer */}
                <div className="flex flex-wrap items-center justify-between gap-2 mt-3 pt-3 border-t border-[#1E293B]/60 text-xs">
                  <div className="flex items-center gap-2 text-slate-400 text-[11px]">
                    <span className="font-mono text-slate-300">{alert.decisionSet}</span>
                    <span>•</span>
                    <span>Risk: <strong className="font-mono text-rose-400 tabular-nums">{alert.riskScore}</strong></span>
                  </div>

                  <div className="flex items-center gap-1.5 sm:gap-2">
                    <Link
                      href={`/graph?node=${encodeURIComponent(alert.account)}`}
                      className="px-2 sm:px-2.5 py-1 rounded bg-[#1E293B] hover:bg-[#334155] text-slate-200 text-xs font-medium transition-colors"
                    >
                      Graph
                    </Link>
                    <Link
                      href={`/sar?caseId=${alert.caseId}`}
                      className="px-2 sm:px-2.5 py-1 rounded bg-rose-950/40 hover:bg-rose-900/60 text-rose-300 border border-rose-800/40 text-xs font-semibold transition-colors"
                    >
                      Draft SAR
                    </Link>
                    <button
                      onClick={() => {
                        setFourEyesModalOpen(true, {
                          actionType: 'ACCOUNT_FREEZE',
                          actionTitle: `Emergency Account Freeze: ${alert.account}`,
                          targetId: alert.account,
                          details: `Immediate institutional freeze for TBML & CTR breach under Section 2(v) MLPA 2012. Amount: $${alert.amount.toLocaleString()}`
                        });
                      }}
                      className="px-2 sm:px-2.5 py-1 rounded bg-emerald-950/40 hover:bg-emerald-900/60 text-emerald-300 border border-emerald-800/40 text-xs font-semibold transition-colors cursor-pointer"
                    >
                      Freeze
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right Column: C-STGB Live Mathematical Scoring Sandbox (5 Cols) */}
        <div className="lg:col-span-5 bg-[#0F172A] border border-[#1E293B] rounded-xl flex flex-col">
          <div className="flex items-center justify-between px-5 py-3.5 border-b border-[#1E293B] bg-[#0B0F17]/50">
            <div className="flex items-center gap-2">
              <Zap className="w-4 h-4 text-emerald-400" />
              <h2 className="text-sm font-semibold text-slate-100">
                C-STGB Mathematical Scoring Sandbox
              </h2>
            </div>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
              FAST-PATH API
            </span>
          </div>

          <div className="p-5 space-y-4 flex-1">
            <p className="text-xs text-slate-400 leading-relaxed">
              Test dynamic Hawkes arrival intensity, 12-dimensional canonical mass-flow invariants, and finite-sample Conformal Risk Control (CRC, α=0.01) in real time.
            </p>

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">
                  Transaction Amount (USD)
                </label>
                <div className="relative">
                  <DollarSign className="w-4 h-4 absolute left-3 top-2.5 text-slate-500" />
                  <input
                    type="number"
                    value={testAmount}
                    onChange={(e) => setTestAmount(Number(e.target.value))}
                    className="w-full pl-9 pr-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-sm font-mono text-slate-100 focus:outline-none focus:border-emerald-500"
                  />
                </div>
                <span className="text-[10px] text-slate-500 mt-0.5 block">
                  Tip: Values between $9,000–$9,950 trigger CTR structuring alerts.
                </span>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">
                    Settlement Rail
                  </label>
                  <select
                    value={testRail}
                    onChange={(e) => setTestRail(e.target.value)}
                    className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-xs font-mono text-slate-200 focus:outline-none focus:border-emerald-500"
                  >
                    <option value="SWIFT MT700 (LC)">SWIFT MT700 (LC)</option>
                    <option value="SWIFT MT103">SWIFT MT103</option>
                    <option value="RTGS">RTGS (Interbank)</option>
                    <option value="BEFTN">BEFTN (ACH)</option>
                    <option value="NPSB">NPSB / MFS</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">
                    Customs Price Divergence
                  </label>
                  <input
                    type="number"
                    value={testPriceDev}
                    onChange={(e) => setTestPriceDev(Number(e.target.value))}
                    className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-xs font-mono text-slate-100 focus:outline-none focus:border-emerald-500"
                  />
                </div>
              </div>

              <button
                onClick={handleRunSandboxScore}
                disabled={isScoring}
                className="w-full py-2.5 px-4 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-slate-900 font-bold rounded-lg text-xs tracking-wide uppercase transition-all shadow-lg flex items-center justify-center gap-2"
              >
                {isScoring ? (
                  <>
                    <Activity className="w-4 h-4 animate-spin text-slate-950" />
                    <span>Evaluating C-STGB Invariants...</span>
                  </>
                ) : (
                  <>
                    <Zap className="w-4 h-4" />
                    <span>Compute 12D Invariants & Conformal Set</span>
                  </>
                )}
              </button>
            </div>

            {/* Live Scoring Output Display */}
            {scoringResult && (
              <div className="p-4 bg-[#0B0F17] border border-emerald-900/50 rounded-xl space-y-3 mt-4 animate-in fade-in">
                <div className="flex items-center justify-between pb-2 border-b border-[#1E293B]">
                  <span className="text-xs font-semibold text-slate-300">Conformal Triage Output:</span>
                  <span
                    className={`px-2 py-0.5 rounded text-xs font-mono font-bold ${
                      scoringResult.tierCode === 1
                        ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                        : scoringResult.tierCode === 2
                        ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                        : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                    }`}
                  >
                    {scoringResult.tierLabel} ({scoringResult.conformalSet})
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-2 text-[11px] font-mono">
                  <div className="p-2 bg-[#0F172A] rounded border border-[#1E293B]">
                    <span className="text-slate-500 block text-[10px]">Model Probability</span>
                    <strong className="text-slate-200 text-sm">{scoringResult.rawProbability}</strong>
                  </div>
                  <div className="p-2 bg-[#0F172A] rounded border border-[#1E293B]">
                    <span className="text-slate-500 block text-[10px]">Hawkes λ_u</span>
                    <strong className="text-slate-200 text-sm">{scoringResult.invariants.lambdaU}</strong>
                  </div>
                  <div className="p-2 bg-[#0F172A] rounded border border-[#1E293B]">
                    <span className="text-slate-500 block text-[10px]">Flow Ratio Φ_flow</span>
                    <strong className="text-slate-200 text-sm">{scoringResult.invariants.phiFlow}</strong>
                  </div>
                  <div className="p-2 bg-[#0F172A] rounded border border-[#1E293B]">
                    <span className="text-slate-500 block text-[10px]">Action Recommendation</span>
                    <strong className="text-emerald-400 text-[10px] break-all">{scoringResult.actionRecommendation}</strong>
                  </div>
                </div>

                <div className="text-[10px] text-slate-500 flex items-center justify-between pt-1">
                  <span>Guaranteed Risk Bound: {scoringResult.calibration.guaranteedCoverage}</span>
                  <span>q1 threshold: {scoringResult.calibration.q1Threshold}</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
