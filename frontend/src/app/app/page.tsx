'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
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
  DollarSign,
  UserCheck,
  GitBranch,
  Lock,
  PlusCircle,
  Send,
  Eye,
  SlidersHorizontal
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { JURISDICTIONS, formatCurrencyByJurisdiction } from '@/lib/compliance/jurisdictions';
import { PiiText } from '@/components/ui/PiiText';
import { CommercialAlert } from '@/lib/data/commercialSeed';
import { IS_ONPREM_MODE } from '@/lib/config/env';

export default function SurveillanceOverviewPage() {
  const router = useRouter();
  const {
    isLiveStreamActive,
    toggleLiveStream,
    streamSpeed,
    setStreamSpeed,
    activeJurisdiction,
    setFourEyesModalOpen,
    alerts,
    cases,
    injectAlert,
    freezeAccount,
    addToast
  } = useBankingStore();

  const jur = JURISDICTIONS[activeJurisdiction];

  // Active Sandbox State
  const [testAmount, setTestAmount] = useState<number>(9450);
  const [testRail, setTestRail] = useState<string>('SWIFT MT700 (LC)');
  const [testPriceDev, setTestPriceDev] = useState<number>(333.7);
  const [testBurst, setTestBurst] = useState<boolean>(true);
  const [testCountry, setTestCountry] = useState<string>('United Arab Emirates (JAFZA)');
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
          burst: testBurst,
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

  const handleInjectSandboxAlert = () => {
    if (!scoringResult) {
      addToast('Score Transaction First', 'Run risk scoring before injecting into live queue.', 'accent');
      return;
    }

    const newId = `ALT-99${Math.floor(6000 + Math.random() * 3000)}`;
    const newAlert: CommercialAlert = {
      id: newId,
      timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19) + ' UTC',
      account: 'BD22-EBLB-4829-1092-8823',
      entityName: 'Meghna Industrial & Agro Processing Ltd',
      amount: Number(testAmount),
      amountBdt: Number(testAmount) * jur.usdFxRate,
      rail: testRail,
      bic: 'EBLBBDDH',
      counterparty: 'AE-EBIL-4412-8819-3301',
      counterpartyName: 'Gulf Star Commodities FZE',
      counterpartyBic: 'EBILAEAD',
      counterpartyCountry: testCountry,
      tier: scoringResult.tierCode === 1 ? 'Tier 1 Hold' : scoringResult.tierCode === 2 ? 'Tier 2 Review' : 'Tier 3 Clear',
      tierCode: scoringResult.tierCode,
      riskScore: scoringResult.rawProbability,
      status: 'PENDING_TRIAGE',
      assignee: 'Amina Rahman, CFE',
      typology: testPriceDev > 100 ? 'TBML Over-Invoicing' : 'High-Velocity Structuring Burst',
      typologyBadge: testPriceDev > 100 ? 'TBML' : 'Structuring',
      decisionSet: scoringResult.conformalSet,
      slaMinutesLeft: scoringResult.tierCode === 1 ? 55 : 180,
      flowConservationRatio: scoringResult.invariants.phiFlow,
      velocityBurstScore: scoringResult.invariants.lambdaU,
      whyFlagged: `Real-time risk score (${scoringResult.rawProbability}) placed in ${scoringResult.conformalSet} with ${testPriceDev}% price divergence.`
    };

    injectAlert(newAlert);
  };

  // Tactical Counts
  const total24h = 148312;
  const tier1Count = alerts.filter(a => a.tierCode === 1 && a.status !== 'FALSE_POSITIVE_DISMISSED').length;
  const tier2Count = alerts.filter(a => a.tierCode === 2 && a.status !== 'FALSE_POSITIVE_DISMISSED').length;
  const tier3Count = total24h - tier1Count - tier2Count;
  const stpRate = Number(((tier3Count / total24h) * 100).toFixed(1));

  // Urgent High-Risk Breaches
  const urgentBreaches = alerts.filter(a => a.tierCode === 1).slice(0, 3);

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
              <span className="font-semibold text-slate-100 uppercase tracking-wide truncate text-xs font-sans">
                {IS_ONPREM_MODE ? 'On-Prem Secure Node' : 'Cloud Evaluation Sandbox (Air-Gap Ready)'}
              </span>
              <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 shrink-0">
                {IS_ONPREM_MODE ? 'EGRESS CONFINED' : 'SYNTHETIC WORKLOAD DATA'}
              </span>
              <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-sky-500/20 text-sky-300 border border-sky-500/30 shrink-0">
                BFF: {IS_ONPREM_MODE ? 'LIVE FASTAPI BACKEND' : 'DETERMINISTIC DEMO ENGINE'}
              </span>
            </div>
            <p className="text-[11px] text-slate-400 mt-0.5 break-words font-mono">
              Statutory Regime: <strong className="text-slate-200">{jur.name}</strong> ({jur.statutoryAct}) | Cash CTR: <strong className="text-emerald-400">{jur.currencySymbol}{jur.ctrThresholdNative.toLocaleString()} {jur.currency}</strong>
            </p>
          </div>
        </div>

        {/* Live Ingestion Stream Controls */}
        <div className="flex items-center gap-2 sm:gap-3 bg-[#0B0F17] px-3 py-1.5 rounded-lg border border-[#334155] shrink-0 self-start sm:self-auto font-mono">
          <span className="text-[11px] font-medium text-slate-400">Feed:</span>
          <button
            onClick={toggleLiveStream}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded text-xs font-semibold transition-all cursor-pointer ${isLiveStreamActive
              ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 hover:bg-emerald-500/30'
              : 'bg-amber-500/20 text-amber-300 border border-amber-500/30 hover:bg-amber-500/30'
              }`}
          >
            {isLiveStreamActive ? (
              <>
                <Pause className="w-3.5 h-3.5" />
                <span>SIMULATED STREAM</span>
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5" />
                <span>PAUSED</span>
              </>
            )}
          </button>

          <div className="flex items-center border-l border-[#334155] pl-2 gap-1 text-[11px]">
            {([1, 2, 5] as const).map((spd) => (
              <button
                key={spd}
                onClick={() => setStreamSpeed(spd)}
                className={`px-1.5 py-0.5 rounded cursor-pointer ${streamSpeed === spd
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

      {/* 4-Card Tactical KPI Ribbon — All Cards Clickable to Filtered Triage */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: 24h Monitored Volume */}
        <Link
          href="/triage?tier=all"
          className="p-5 bg-[#0F172A] border border-[#1E293B] hover:border-emerald-500/40 rounded-xl transition-all h-full flex flex-col justify-between group cursor-pointer block"
        >
          <div>
            <div className="flex items-center justify-between text-slate-400 mb-2">
              <span className="text-xs font-semibold tracking-wide uppercase font-sans">24h Monitored Volume</span>
              <TrendingUp className="w-4 h-4 text-emerald-400 group-hover:translate-x-0.5 transition-transform" />
            </div>
            <div className="text-2xl font-bold font-mono text-slate-100 tabular-nums">
              {total24h.toLocaleString()}
            </div>
            <div className="text-xs text-slate-400 mt-1 flex items-center gap-1.5">
              <span className="text-emerald-400 font-mono font-bold">STP Rate: {stpRate}%</span>
              <span>straight-through clear</span>
            </div>
          </div>
          <div className="pt-3 border-t border-[#1E293B] mt-4 flex items-center justify-between text-[11px] text-slate-400">
            <span>Filter All Transactions</span>
            <ArrowUpRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-emerald-400 transition-colors" />
          </div>
        </Link>

        {/* Card 2: Tier 1 Quarantined Holds */}
        <Link
          href="/triage?tier=tier1"
          className="p-5 bg-[#0F172A] border border-[#1E293B] hover:border-rose-500/40 rounded-xl transition-all h-full flex flex-col justify-between group cursor-pointer block"
        >
          <div>
            <div className="flex items-center justify-between text-slate-400 mb-2">
              <span className="text-xs font-semibold tracking-wide uppercase font-sans">Tier 1 Administrative Hold</span>
              <ShieldAlert className="w-4 h-4 text-rose-500 group-hover:scale-110 transition-transform" />
            </div>
            <div className="text-2xl font-bold font-mono text-rose-400 tabular-nums">
              {tier1Count.toLocaleString()}
            </div>
            <div className="text-xs text-slate-400 mt-1 flex items-center gap-1.5">
              <span className="text-rose-400 font-mono font-bold">Risk Set: Γ = &#123;1&#125;</span>
              <span>Auto-Quarantined</span>
            </div>
          </div>
          <div className="pt-3 border-t border-[#1E293B] mt-4 flex items-center justify-between text-[11px] text-slate-400">
            <span className="text-rose-300">View Tier 1 Queue</span>
            <ArrowUpRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-rose-400 transition-colors" />
          </div>
        </Link>

        {/* Card 3: Tier 2 Officer Review */}
        <Link
          href="/triage?tier=tier2"
          className="p-5 bg-[#0F172A] border border-[#1E293B] hover:border-amber-500/40 rounded-xl transition-all h-full flex flex-col justify-between group cursor-pointer block"
        >
          <div>
            <div className="flex items-center justify-between text-slate-400 mb-2">
              <span className="text-xs font-semibold tracking-wide uppercase font-sans">Tier 2 Officer Review</span>
              <AlertTriangle className="w-4 h-4 text-amber-500 group-hover:scale-110 transition-transform" />
            </div>
            <div className="text-2xl font-bold font-mono text-amber-400 tabular-nums">
              {tier2Count.toLocaleString()}
            </div>
            <div className="text-xs text-slate-400 mt-1 flex items-center gap-1.5">
              <span className="text-amber-400 font-mono font-bold">Ambiguous: Γ = &#123;0, 1&#125;</span>
              <span>Manual triage</span>
            </div>
          </div>
          <div className="pt-3 border-t border-[#1E293B] mt-4 flex items-center justify-between text-[11px] text-slate-400">
            <span className="text-amber-300">View Tier 2 Queue</span>
            <ArrowUpRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-amber-400 transition-colors" />
          </div>
        </Link>

        {/* Card 4: Clearing Latency SLA */}
        <div className="p-5 bg-[#0F172A] border border-[#1E293B] rounded-xl h-full flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-slate-400 mb-2">
              <span className="text-xs font-semibold tracking-wide uppercase font-sans">Clearing Decision SLA</span>
              <Clock className="w-4 h-4 text-emerald-400" />
            </div>
            <div className="text-2xl font-bold font-mono text-slate-100 tabular-nums">
              0.45 ms
            </div>
            <div className="text-xs text-slate-400 mt-1 flex items-center gap-1.5">
              <span className="text-emerald-400 font-mono font-bold">P99: 0.82 ms</span>
              <span>Ultra-low sub-millisecond</span>
            </div>
          </div>
          <div className="pt-3 border-t border-[#1E293B] mt-4 flex items-center justify-between text-[11px] text-slate-400 font-mono">
            <span>Peak: 500 tx/sec</span>
            <span className="text-emerald-400 font-bold">100% IN BOUNDS</span>
          </div>
        </div>
      </div>

      {/* Main Grid: Urgent Action Queue & Team SLA Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Urgent Action Queue (7 Cols) */}
        <div className="lg:col-span-7 bg-[#0F172A] border border-[#1E293B] rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-[#1E293B]">
            <div>
              <h2 className="text-sm font-semibold text-slate-100 flex items-center gap-2 font-sans">
                <ShieldAlert className="w-4 h-4 text-rose-500" />
                Urgent High-Risk Interdiction Queue
              </h2>
              <p className="text-xs text-slate-400 mt-0.5">
                Priority Tier 1 breaches requiring statutory hold enforcement, case escalation, or SAR filing.
              </p>
            </div>
            <Link
              href="/triage"
              className="text-xs font-mono text-emerald-400 hover:text-emerald-300 flex items-center gap-1"
            >
              <span>View All ({alerts.length.toLocaleString()})</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="space-y-3">
            {urgentBreaches.map((alert) => (
              <div
                key={alert.id}
                className="p-3.5 bg-[#0B0F17] rounded-xl border border-[#1E293B] hover:border-[#334155] transition-all space-y-2.5"
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">
                      {alert.tier}
                    </span>
                    <span className="font-mono text-xs font-bold text-slate-200">{alert.id}</span>
                    <span className="text-slate-400 text-xs truncate max-w-[200px] sm:max-w-[280px]">
                      {alert.entityName}
                    </span>
                  </div>

                  <div className="text-right">
                    <span className="font-mono text-xs font-bold text-rose-400 block tabular-nums">
                      ${alert.amount.toLocaleString('en-US', { minimumFractionDigits: 2 })} USD
                    </span>
                    <span className="text-[10px] font-mono text-slate-500 block">
                      ৳{alert.amountBdt.toLocaleString()} BDT
                    </span>
                  </div>
                </div>

                <p className="text-xs text-slate-400 leading-relaxed font-sans">
                  {alert.whyFlagged}
                </p>

                {/* Inline Action Bar */}
                <div className="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-[#1E293B] text-xs font-mono">
                  <div className="flex items-center gap-2">
                    <span className="text-slate-400">Account:</span>
                    <PiiText value={alert.account} type="account" className="text-slate-300 font-bold" />
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={() => router.push(`/triage?alertId=${alert.id}&inspect=true`)}
                      className="px-2.5 py-1 rounded bg-[#1E293B] hover:bg-[#334155] text-slate-200 transition-colors cursor-pointer text-[11px]"
                    >
                      Inspect Wire
                    </button>
                    <button
                      type="button"
                      onClick={() => router.push(`/graph?node=${encodeURIComponent(alert.account)}`)}
                      className="px-2.5 py-1 rounded bg-purple-950/40 hover:bg-purple-900/60 text-purple-300 border border-purple-800/40 transition-colors cursor-pointer text-[11px] flex items-center gap-1"
                    >
                      <GitBranch className="w-3 h-3" />
                      <span>Graph</span>
                    </button>
                    <button
                      type="button"
                      onClick={() => router.push(`/sar?caseId=${alert.caseId || 'CASE-2026-0881'}`)}
                      className="px-2.5 py-1 rounded bg-emerald-950/40 hover:bg-emerald-900/60 text-emerald-300 border border-emerald-800/40 transition-colors cursor-pointer text-[11px] flex items-center gap-1"
                    >
                      <FileText className="w-3 h-3" />
                      <span>Draft SAR</span>
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        setFourEyesModalOpen(true, {
                          actionType: 'ACCOUNT_FREEZE',
                          actionTitle: `Emergency Administrative Freeze: ${alert.account}`,
                          targetId: alert.account,
                          details: `Statutory hold requested under ${jur.statutoryAct}. Entity: ${alert.entityName}. Amount: $${alert.amount.toLocaleString()}.`
                        });
                      }}
                      className="px-2.5 py-1 rounded bg-rose-950/50 hover:bg-rose-900/70 text-rose-300 border border-rose-800/50 transition-colors cursor-pointer text-[11px] flex items-center gap-1"
                    >
                      <Lock className="w-3 h-3" />
                      <span>Freeze (4-Eyes)</span>
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right: Team Workload & SLA Operations Panel (5 Cols) */}
        <div className="lg:col-span-5 bg-[#0F172A] border border-[#1E293B] rounded-xl p-5 space-y-4 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-[#1E293B]">
              <h2 className="text-sm font-semibold text-slate-100 flex items-center gap-2 font-sans">
                <UserCheck className="w-4 h-4 text-emerald-400" />
                SIU Team Workload & Operational SLA
              </h2>
              <span className="text-[10px] font-mono font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                ACTIVE SHIFT
              </span>
            </div>

            <div className="space-y-3 pt-3">
              {[
                { name: 'Amina Rahman, CFE (Demo Lead)', role: 'Lead Investigator', activeCases: 4, openAlerts: 18, ahtMin: 14.2, status: 'NORMAL' },
                { name: 'Tanvir Ahmed (Demo Analyst)', role: 'Senior Triage Analyst', activeCases: 3, openAlerts: 24, ahtMin: 18.5, status: 'ELEVATED' },
                { name: 'Nadia Hossain (Demo Specialist)', role: 'Trade Compliance Specialist', activeCases: 1, openAlerts: 42, ahtMin: 9.4, status: 'NORMAL' },
                { name: 'Unassigned Escalation Pool', role: 'System Queue', activeCases: 2, openAlerts: 112, ahtMin: 0, status: 'PENDING_DISPATCH' }
              ].map((member, idx) => (
                <div key={idx} className="p-3 bg-[#0B0F17] rounded-lg border border-[#1E293B] text-xs">
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="font-semibold text-slate-200">{member.name}</span>
                    <span className="text-[10px] font-mono text-slate-400">{member.role}</span>
                  </div>
                  <div className="grid grid-cols-3 gap-2 text-[11px] font-mono pt-1 text-slate-400">
                    <div>Alerts: <strong className="text-slate-200 tabular-nums">{member.openAlerts}</strong></div>
                    <div>Cases: <strong className="text-amber-400 tabular-nums">{member.activeCases}</strong></div>
                    <div>AHT: <strong className="text-emerald-400 tabular-nums">{member.ahtMin ? `${member.ahtMin}m` : 'Queue'}</strong></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="pt-3 border-t border-[#1E293B] text-xs text-slate-400 space-y-1 font-mono">
            <div className="flex justify-between">
              <span>Alert-to-Case Conversion Rate:</span>
              <strong className="text-slate-200">1.84%</strong>
            </div>
            <div className="flex justify-between">
              <span>Case-to-SAR Filing Ratio:</span>
              <strong className="text-emerald-400">82.5%</strong>
            </div>
          </div>
        </div>
      </div>

      {/* Real-Time Risk Scoring Sandbox (Active Production Simulator) */}
      <div className="p-5 bg-[#0F172A] border border-[#1E293B] rounded-xl space-y-5">
        <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-[#1E293B]">
          <div>
            <h2 className="text-sm font-semibold text-slate-100 flex items-center gap-2 font-sans">
              <SlidersHorizontal className="w-4 h-4 text-emerald-400" />
              Real-Time Risk Scoring Sandbox
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Simulate transaction parameter variations to test real-time calibrated risk sets, velocity spikes, and inject alerts into live queue.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleRunSandboxScore}
              disabled={isScoring}
              className="px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-slate-950 font-bold text-xs uppercase tracking-wide rounded-lg transition-all cursor-pointer font-mono"
            >
              {isScoring ? 'Computing Risk...' : 'Run Scoring Engine'}
            </button>
            <button
              type="button"
              onClick={handleInjectSandboxAlert}
              disabled={!scoringResult}
              className="px-3.5 py-1.5 bg-purple-900/60 hover:bg-purple-800 disabled:opacity-40 text-purple-200 font-bold text-xs uppercase tracking-wide rounded-lg border border-purple-700/50 transition-all cursor-pointer font-mono flex items-center gap-1.5"
            >
              <PlusCircle className="w-3.5 h-3.5" />
              <span>+ Inject Alert Into Live Queue</span>
            </button>
          </div>
        </div>

        {/* Input Parameters Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 text-xs font-mono">
          <div>
            <label className="text-slate-400 block mb-1">TRANSACTION AMOUNT (USD)</label>
            <input
              type="number"
              value={testAmount}
              onChange={(e) => setTestAmount(Number(e.target.value))}
              className="w-full px-3 py-1.5 rounded bg-[#0B0F17] border border-[#334155] text-slate-100 font-bold"
            />
            <span className="text-[10px] text-slate-500 mt-1 block">
              ≈ ৳{(testAmount * jur.usdFxRate).toLocaleString()} BDT
            </span>
          </div>

          <div>
            <label className="text-slate-400 block mb-1">PAYMENT RAIL / PROTOCOL</label>
            <select
              value={testRail}
              onChange={(e) => setTestRail(e.target.value)}
              className="w-full px-3 py-1.5 rounded bg-[#0B0F17] border border-[#334155] text-slate-100 cursor-pointer"
            >
              <option value="SWIFT MT700 (LC)">SWIFT MT700 (Trade LC)</option>
              <option value="SWIFT MT103">SWIFT MT103 (Cross-Border Wire)</option>
              <option value="ISO 20022 pacs.008">ISO 20022 pacs.008</option>
              <option value="RTGS / BEFTN">Domestic RTGS / BEFTN</option>
              <option value="bKash/Nagad MFS">MFS Agent Clearing Hub</option>
            </select>
          </div>

          <div>
            <label className="text-slate-400 block mb-1">CUSTOMS PRICE DIVERGENCE</label>
            <input
              type="number"
              value={testPriceDev}
              onChange={(e) => setTestPriceDev(Number(e.target.value))}
              className="w-full px-3 py-1.5 rounded bg-[#0B0F17] border border-[#334155] text-slate-100 font-bold"
            />
            <span className="text-[10px] text-slate-500 mt-1 block">
              Benchmark vs Declared Unit Price
            </span>
          </div>

          <div>
            <label className="text-slate-400 block mb-1">HIGH-VELOCITY BURST</label>
            <select
              value={testBurst ? 'true' : 'false'}
              onChange={(e) => setTestBurst(e.target.value === 'true')}
              className="w-full px-3 py-1.5 rounded bg-[#0B0F17] border border-[#334155] text-slate-100 cursor-pointer"
            >
              <option value="true">Active (&gt;5 events / 10m)</option>
              <option value="false">Normal (&le; 1 event / hr)</option>
            </select>
          </div>

          <div>
            <label className="text-slate-400 block mb-1">COUNTERPARTY COUNTRY</label>
            <select
              value={testCountry}
              onChange={(e) => setTestCountry(e.target.value)}
              className="w-full px-3 py-1.5 rounded bg-[#0B0F17] border border-[#334155] text-slate-100 cursor-pointer"
            >
              <option value="United Arab Emirates (JAFZA)">UAE (JAFZA Free Zone)</option>
              <option value="Singapore">Singapore (Port Transit)</option>
              <option value="Switzerland">Switzerland (Industrial)</option>
              <option value="United States">United States (Domestic)</option>
            </select>
          </div>
        </div>

        {/* Live Scoring Result Banner */}
        {scoringResult && (
          <div className="p-4 rounded-xl bg-[#0B0F17] border border-[#1E293B] grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs font-mono">
            <div>
              <span className="text-slate-400 block mb-1">CALIBRATED DECISION TIER</span>
              <span className={`text-sm font-bold block ${scoringResult.tierCode === 1 ? 'text-rose-400' : scoringResult.tierCode === 2 ? 'text-amber-400' : 'text-emerald-400'}`}>
                {scoringResult.tierLabel} ({scoringResult.conformalSet})
              </span>
            </div>

            <div>
              <span className="text-slate-400 block mb-1">RAW MODEL PROBABILITY</span>
              <span className="text-sm font-bold text-slate-100 block tabular-nums">
                p&#770; = {scoringResult.rawProbability}
              </span>
            </div>

            <div>
              <span className="text-slate-400 block mb-1">VELOCITY BURST SCORE</span>
              <span className="text-sm font-bold text-amber-400 block tabular-nums">
                &lambda;<sub>u</sub> = {scoringResult.invariants.lambdaU}
              </span>
            </div>

            <div>
              <span className="text-slate-400 block mb-1">FLOW CONSERVATION RATIO</span>
              <span className="text-sm font-bold text-emerald-400 block tabular-nums">
                &Phi;<sub>flow</sub> = {scoringResult.invariants.phiFlow}
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
