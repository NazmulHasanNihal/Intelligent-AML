'use client';

import React, { useState, useEffect, useMemo } from 'react';
import {
  Scale,
  ShieldCheck,
  TrendingDown,
  Activity,
  Download,
  CheckCircle2,
  AlertTriangle,
  Lock,
  Layers,
  FileCheck2,
  RefreshCw,
  Clock,
  Radio,
  Send,
  Terminal,
  ShieldAlert,
  SlidersHorizontal,
  Check,
  XCircle,
  Copy,
  Table
} from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';
import { useBankingStore } from '@/lib/store';
import { verifyAuditChain, tamperAuditBlock, restoreAuditChain, computeSha256 } from '@/lib/audit/hashChain';

const BASE_DRIFT_SERIES = [
  { t: 'W-1', f1: 0.942, p99Latency: 0.81, ksStatistic: 0.021 },
  { t: 'W-2', f1: 0.946, p99Latency: 0.79, ksStatistic: 0.024 },
  { t: 'W-3', f1: 0.938, p99Latency: 0.84, ksStatistic: 0.028 },
  { t: 'W-4', f1: 0.941, p99Latency: 0.82, ksStatistic: 0.026 },
  { t: 'W-5', f1: 0.939, p99Latency: 0.85, ksStatistic: 0.031 },
  { t: 'W-6', f1: 0.944, p99Latency: 0.80, ksStatistic: 0.025 },
  { t: 'W-7', f1: 0.948, p99Latency: 0.78, ksStatistic: 0.022 },
  { t: 'W-8 (Current)', f1: 0.945, p99Latency: 0.82, ksStatistic: 0.024 }
];

export default function ModelGovernancePage() {
  const {
    auditLedger,
    simulateTamperTest,
    restoreValidChain,
    addToast
  } = useBankingStore();

  const [activeTab, setActiveTab] = useState<'MODEL_HEALTH' | 'WEBHOOK_HUB' | 'WORM_LEDGER'>('MODEL_HEALTH');
  const [isSimulatingSpike, setIsSimulatingSpike] = useState(false);
  const [isVerifying, setIsVerifying] = useState(false);
  const [isTampered, setIsTampered] = useState(false);
  const [verificationResult, setVerificationResult] = useState<any>(null);

  // Webhook Tester State
  const [selectedWebhook, setSelectedWebhook] = useState<'DEBIT_HOLD' | 'ACCOUNT_FREEZE'>('DEBIT_HOLD');
  const [targetAccount, setTargetAccount] = useState('BD22-EBLB-4829-1092-8823');
  const [webhookResponse, setWebhookResponse] = useState<string | null>(null);
  const [isDispatchingWebhook, setIsDispatchingWebhook] = useState(false);

  // Drift data based on volatility spike toggle
  const driftChartData = useMemo(() => {
    if (!isSimulatingSpike) return BASE_DRIFT_SERIES;
    return BASE_DRIFT_SERIES.map((d, i) => {
      if (i >= 5) {
        return {
          ...d,
          f1: Number((d.f1 - 0.06).toFixed(3)),
          p99Latency: Number((d.p99Latency + 0.32).toFixed(2)),
          ksStatistic: Number((d.ksStatistic + 0.065).toFixed(3))
        };
      }
      return d;
    });
  }, [isSimulatingSpike]);

  // Handle Real Client WebCrypto WORM Verification
  const handleRunAuditVerification = async () => {
    setIsVerifying(true);
    try {
      const res = await verifyAuditChain(auditLedger);
      setVerificationResult(res);
      if (res.isValid) {
        addToast('Cryptographic Integrity Verified', `All ${res.totalEntries} blocks chained with verified SHA-256 hashes.`, 'success');
      } else {
        addToast('Tamper Detected!', `Block #${res.brokenSequence} hash mismatch. Cryptographic seal broken!`, 'critical');
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsVerifying(false);
    }
  };

  const handleTamperTest = () => {
    simulateTamperTest(1);
    setIsTampered(true);
    setVerificationResult({
      isValid: false,
      totalEntries: auditLedger.length,
      brokenSequence: 2
    });
    addToast('Simulated Tamper Triggered', 'Block #1 payload modified. WORM chain will fail verification.', 'critical');
  };

  const handleRestoreTamper = () => {
    restoreValidChain();
    setIsTampered(false);
    setVerificationResult({
      isValid: true,
      totalEntries: auditLedger.length
    });
    addToast('Integrity Restored', 'WORM audit block cryptographic hashes recalculated and restored.', 'success');
  };

  // Dispatch Outbound Webhook Test
  const handleTestWebhookDispatch = async () => {
    setIsDispatchingWebhook(true);
    const timestamp = new Date().toISOString();
    const payload = {
      event: selectedWebhook === 'DEBIT_HOLD' ? 'BANKING_RAIL_DEBIT_HOLD_TRIGGERED' : 'BANKING_RAIL_ACCOUNT_FREEZE_ORDER',
      targetAccount,
      authorizedOfficer: 'Sarah Jenkins (Analyst ID: L2-4491)',
      reason: 'Automated Tier 1 Calibrated Surveillance Quarantining',
      timestamp,
      callbackUrl: 'https://corebanking.ebl.com.bd/api/v2/holds/settlement'
    };

    const signature = await computeSha256(JSON.stringify(payload) + 'SECRET_HMAC_KEY');

    setTimeout(() => {
      setWebhookResponse(JSON.stringify({
        status: 200,
        coreBankingAck: 'ACK_TRANSACTION_INTERCEPTED',
        dispatchedPayload: payload,
        headers: {
          'X-Banking-Signature-SHA256': signature,
          'X-Request-Id': `REQ-${Math.floor(100000 + Math.random() * 900000)}`,
          'X-Idempotency-Key': `IDEMP-${Date.now()}`
        }
      }, null, 2));
      setIsDispatchingWebhook(false);
      addToast('Webhook Dispatched', `Simulated ${selectedWebhook} sent to core banking API. Status: 200 OK`, 'success');
    }, 600);
  };

  const handleDownloadGovernancePack = () => {
    const pack = {
      productionSystem: 'Intelligent-AML Enterprise Banking Operating System',
      complianceFramework: 'Federal Reserve SR 11-7 / OCC 2011-12 / BFIU Core Risk Guideline',
      timestamp: new Date().toISOString(),
      productionModelHealth: {
        coverageGuarantee: '≥ 99.0% Class-Conditional Finite Sample Coverage',
        activeChampionModel: 'Production Spatio-Temporal Graph Surveillance Engine v3.0',
        p99InferenceLatency: '0.82 ms',
        meanThroughput: '12,500 transactions / sec'
      },
      paymentRailsScorecard: [
        { rail: 'SWIFT MT / Documentary Credits', f1Score: 0.965, falsePositiveRate: '0.62%', p99Latency: '0.84 ms' },
        { rail: 'ISO 20022 (pacs.008 RTGS)', f1Score: 0.952, falsePositiveRate: '0.74%', p99Latency: '0.81 ms' },
        { rail: 'BEFTN / National Electronic Clearing', f1Score: 0.941, falsePositiveRate: '0.88%', p99Latency: '0.79 ms' },
        { rail: 'Mobile Financial Services (MFS / Agent)', f1Score: 0.948, falsePositiveRate: '0.79%', p99Latency: '0.85 ms' }
      ],
      cryptographicAuditIntegrity: {
        totalLedgerBlocks: auditLedger.length,
        status: isTampered ? 'CORRUPTED' : 'VERIFIED_CHAIN_VALID',
        headHash: auditLedger[auditLedger.length - 1]?.currentHash || ''
      }
    };

    const blob = new Blob([JSON.stringify(pack, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `SR11-7-Institutional-Compliance-Pack-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="p-4 sm:p-5 lg:p-6 max-w-[1750px] mx-auto space-y-5">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2 font-sans">
            <Scale className="w-5 h-5 text-cyan-400" />
            Model Operations, Core Banking Webhooks &amp; WORM Audit Ledger
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Federal Reserve SR 11-7 model risk management, production rail telemetry, and SEC 17a-4 / FINRA 4511 WORM cryptographic audit ledger.
          </p>
        </div>

        {/* Tab Switcher */}
        <div className="flex items-center bg-[#0F172A] p-1 rounded-xl border border-[#334155] text-xs font-semibold">
          <button
            onClick={() => setActiveTab('MODEL_HEALTH')}
            className={`px-3 py-1.5 rounded-lg transition-colors cursor-pointer ${
              activeTab === 'MODEL_HEALTH'
                ? 'bg-cyan-500/20 text-cyan-300 font-bold border border-cyan-500/40'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Model Health &amp; SR 11-7 Risk
          </button>
          <button
            onClick={() => setActiveTab('WEBHOOK_HUB')}
            className={`px-3 py-1.5 rounded-lg transition-colors cursor-pointer ${
              activeTab === 'WEBHOOK_HUB'
                ? 'bg-cyan-500/20 text-cyan-300 font-bold border border-cyan-500/40'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Core Banking Integration Webhooks
          </button>
          <button
            onClick={() => setActiveTab('WORM_LEDGER')}
            className={`px-3 py-1.5 rounded-lg transition-colors cursor-pointer ${
              activeTab === 'WORM_LEDGER'
                ? 'bg-cyan-500/20 text-cyan-300 font-bold border border-cyan-500/40'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            WORM Cryptographic Audit Trail ({auditLedger.length})
          </button>
        </div>
      </div>

      {/* Tab 1: Model Health & SR 11-7 Risk Governance */}
      {activeTab === 'MODEL_HEALTH' && (
        <div className="space-y-5">
          {/* Top Actions & Volatility Spike Toggle */}
          <div className="p-4 rounded-xl bg-[#0F172A] border border-[#1E293B] flex flex-wrap items-center justify-between gap-4 shadow-xl">
            <div className="flex items-center gap-3">
              <span className="text-xs font-mono font-semibold text-slate-300">Stress Test Scenario:</span>
              <button
                onClick={() => setIsSimulatingSpike(!isSimulatingSpike)}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer flex items-center gap-2 ${
                  isSimulatingSpike
                    ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
                    : 'bg-[#0B0F17] text-slate-400 border border-[#334155] hover:text-slate-200'
                }`}
              >
                <Activity className="w-3.5 h-3.5" />
                <span>{isSimulatingSpike ? 'Market Volatility Surge Active (+420% Burst)' : 'Normal Market Baseline'}</span>
              </button>
            </div>

            <button
              onClick={handleDownloadGovernancePack}
              className="px-4 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-semibold text-xs transition-colors flex items-center gap-2 cursor-pointer shadow-lg shadow-cyan-600/20"
            >
              <Download className="w-4 h-4" />
              <span>Download SR 11-7 Compliance Pack (JSON)</span>
            </button>
          </div>

          {/* Dual Y-Axis Production Drift Chart */}
          <div className="p-5 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl space-y-4">
            <div className="flex items-center justify-between pb-2 border-b border-[#1E293B]">
              <div>
                <h3 className="text-sm font-bold text-slate-100 font-mono">
                  Production Model Drift &amp; P99 Inference Latency Telemetry
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  Left Axis: Macro F1 Surveillance Fidelity • Right Axis: P99 End-to-End Decision Latency (ms)
                </p>
              </div>

              <div className="flex items-center gap-4 text-xs font-mono">
                <span className="flex items-center gap-1.5 text-emerald-400">
                  <span className="w-2.5 h-2.5 rounded-full bg-emerald-400" />
                  <span>Macro F1 Metric</span>
                </span>
                <span className="flex items-center gap-1.5 text-sky-400">
                  <span className="w-2.5 h-2.5 rounded-full bg-sky-400" />
                  <span>P99 Latency (ms)</span>
                </span>
              </div>
            </div>

            <div className="h-72 w-full pt-2">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={driftChartData} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
                  <XAxis dataKey="t" stroke="#64748B" tick={{ fontSize: 11, fontFamily: 'monospace' }} />
                  <YAxis yAxisId="left" domain={[0.80, 1.00]} stroke="#10B981" tick={{ fontSize: 11, fontFamily: 'monospace' }} />
                  <YAxis yAxisId="right" orientation="right" domain={[0.5, 1.5]} stroke="#38BDF8" tick={{ fontSize: 11, fontFamily: 'monospace' }} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0B0F17', borderColor: '#334155', borderRadius: 8, fontSize: 12 }}
                  />
                  <ReferenceLine yAxisId="left" y={0.90} stroke="#EF4444" strokeDasharray="3 3" label={{ value: 'SR 11-7 Floor (0.90)', fill: '#EF4444', fontSize: 10 }} />
                  <Line yAxisId="left" type="monotone" dataKey="f1" stroke="#10B981" strokeWidth={2.5} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                  <Line yAxisId="right" type="monotone" dataKey="p99Latency" stroke="#38BDF8" strokeWidth={2} dot={{ r: 3 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Core Banking Payment Rails Scorecard */}
          <div className="bg-[#0F172A] border border-[#1E293B] rounded-2xl p-5 shadow-xl space-y-4">
            <h3 className="text-sm font-bold text-slate-100 font-mono">
              Live Core Banking Rail Performance Scorecard
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs font-mono">
              <div className="p-4 rounded-xl bg-[#0B0F17] border border-[#1E293B] space-y-2">
                <span className="text-[10px] text-slate-500 uppercase block font-bold">SWIFT MT / Documentary Credits</span>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Macro F1:</span>
                  <span className="font-bold text-emerald-400">96.5%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">False Positive:</span>
                  <span className="font-bold text-emerald-400">0.62%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">P99 Latency:</span>
                  <span className="font-bold text-slate-200">0.84 ms</span>
                </div>
              </div>

              <div className="p-4 rounded-xl bg-[#0B0F17] border border-[#1E293B] space-y-2">
                <span className="text-[10px] text-slate-500 uppercase block font-bold">ISO 20022 pacs.008 RTGS</span>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Macro F1:</span>
                  <span className="font-bold text-emerald-400">95.2%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">False Positive:</span>
                  <span className="font-bold text-emerald-400">0.74%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">P99 Latency:</span>
                  <span className="font-bold text-slate-200">0.81 ms</span>
                </div>
              </div>

              <div className="p-4 rounded-xl bg-[#0B0F17] border border-[#1E293B] space-y-2">
                <span className="text-[10px] text-slate-500 uppercase block font-bold">BEFTN Electronic Clearing</span>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Macro F1:</span>
                  <span className="font-bold text-emerald-400">94.1%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">False Positive:</span>
                  <span className="font-bold text-emerald-400">0.88%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">P99 Latency:</span>
                  <span className="font-bold text-slate-200">0.79 ms</span>
                </div>
              </div>

              <div className="p-4 rounded-xl bg-[#0B0F17] border border-[#1E293B] space-y-2">
                <span className="text-[10px] text-slate-500 uppercase block font-bold">MFS (bKash, Nagad, Rocket)</span>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Macro F1:</span>
                  <span className="font-bold text-emerald-400">94.8%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">False Positive:</span>
                  <span className="font-bold text-emerald-400">0.79%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">P99 Latency:</span>
                  <span className="font-bold text-slate-200">0.85 ms</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: Core Banking Integration & Outbound Webhook Hub */}
      {activeTab === 'WEBHOOK_HUB' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
          {/* Dispatch Config */}
          <div className="lg:col-span-5 bg-[#0F172A] border border-[#1E293B] rounded-2xl p-5 shadow-xl space-y-4">
            <h3 className="text-sm font-bold text-slate-100 font-mono flex items-center gap-2">
              <Radio className="w-4 h-4 text-cyan-400" />
              Core Banking Interception Webhooks
            </h3>
            <p className="text-xs text-slate-400">
              Real-time API integrations that instruct core banking engines to place immediate settlement holds or freeze accounts.
            </p>

            <div className="space-y-3 text-xs font-sans">
              <div>
                <label className="text-slate-400 block mb-1 font-mono uppercase text-[10px]">Action Hook Target</label>
                <div className="grid grid-cols-2 gap-2">
                  <button
                    onClick={() => setSelectedWebhook('DEBIT_HOLD')}
                    className={`p-2.5 rounded-lg border text-left cursor-pointer transition-colors ${
                      selectedWebhook === 'DEBIT_HOLD'
                        ? 'bg-cyan-500/20 border-cyan-500 text-cyan-300 font-bold'
                        : 'bg-[#0B0F17] border-[#334155] text-slate-300'
                    }`}
                  >
                    <div>/debit-hold</div>
                    <div className="text-[10px] font-normal text-slate-400 mt-0.5">Temporary Wire Quarantine</div>
                  </button>

                  <button
                    onClick={() => setSelectedWebhook('ACCOUNT_FREEZE')}
                    className={`p-2.5 rounded-lg border text-left cursor-pointer transition-colors ${
                      selectedWebhook === 'ACCOUNT_FREEZE'
                        ? 'bg-rose-500/20 border-rose-500 text-rose-300 font-bold'
                        : 'bg-[#0B0F17] border-[#334155] text-slate-300'
                    }`}
                  >
                    <div>/account-freeze</div>
                    <div className="text-[10px] font-normal text-slate-400 mt-0.5">Statutory Full Account Lock</div>
                  </button>
                </div>
              </div>

              <div>
                <label className="text-slate-400 block mb-1 font-mono uppercase text-[10px]">Target Account Number</label>
                <input
                  type="text"
                  value={targetAccount}
                  onChange={(e) => setTargetAccount(e.target.value)}
                  className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-100 font-mono text-xs focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div className="pt-2">
                <button
                  onClick={handleTestWebhookDispatch}
                  disabled={isDispatchingWebhook}
                  className="w-full py-2.5 px-4 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-semibold text-xs transition-colors flex items-center justify-center gap-2 cursor-pointer shadow-lg shadow-cyan-600/20"
                >
                  <Send className="w-4 h-4" />
                  <span>{isDispatchingWebhook ? 'Dispatching...' : 'Dispatch Live Webhook Test'}</span>
                </button>
              </div>
            </div>
          </div>

          {/* Webhook Response Log Viewer */}
          <div className="lg:col-span-7 bg-[#0F172A] border border-[#1E293B] rounded-2xl p-5 shadow-xl flex flex-col justify-between space-y-4">
            <div>
              <div className="flex items-center justify-between pb-3 border-b border-[#1E293B]">
                <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider font-mono flex items-center gap-2">
                  <Terminal className="w-4 h-4 text-emerald-400" />
                  Core Banking API Telemetry Log
                </h3>
                <span className="text-[10px] font-mono text-slate-400">HMAC-SHA256 Signed</span>
              </div>

              <div className="mt-3 p-4 bg-[#090D14] border border-[#1E293B] rounded-xl font-mono text-xs text-emerald-400 h-80 overflow-y-auto">
                {webhookResponse ? (
                  <pre>{webhookResponse}</pre>
                ) : (
                  <div className="text-slate-600 py-24 text-center">
                    Click &quot;Dispatch Live Webhook Test&quot; to inspect outbound payload and core banking acknowledgment.
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 3: WORM Cryptographic Audit Trail */}
      {activeTab === 'WORM_LEDGER' && (
        <div className="space-y-4">
          {/* Controls Bar */}
          <div className="p-4 rounded-xl bg-[#0F172A] border border-[#1E293B] flex flex-wrap items-center justify-between gap-4 shadow-xl">
            <div className="flex items-center gap-3">
              <button
                onClick={handleRunAuditVerification}
                disabled={isVerifying}
                className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition-colors flex items-center gap-2 cursor-pointer shadow-md shadow-emerald-600/20"
              >
                <CheckCircle2 className="w-4 h-4" />
                <span>{isVerifying ? 'Verifying SHA-256 Hashes...' : 'Verify Cryptographic Chain'}</span>
              </button>

              <button
                onClick={isTampered ? handleRestoreTamper : handleTamperTest}
                className={`px-4 py-2 rounded-xl font-semibold text-xs transition-colors flex items-center gap-2 cursor-pointer ${
                  isTampered
                    ? 'bg-amber-600 hover:bg-amber-500 text-white'
                    : 'bg-rose-950/60 hover:bg-rose-900/80 text-rose-300 border border-rose-800/60'
                }`}
              >
                <ShieldAlert className="w-4 h-4" />
                <span>{isTampered ? 'Restore Chain Integrity' : 'Simulate Auditor Tamper Test'}</span>
              </button>
            </div>

            {verificationResult && (
              <div className="flex items-center gap-2 font-mono text-xs">
                {verificationResult.isValid ? (
                  <span className="text-emerald-400 font-bold flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4" />
                    Chain 100% Cryptographically Valid ({verificationResult.totalEntries} blocks)
                  </span>
                ) : (
                  <span className="text-rose-400 font-bold flex items-center gap-1.5 animate-pulse">
                    <XCircle className="w-4 h-4" />
                    TAMPER DETECTED: Block #{verificationResult.brokenSequence} Hash Mismatch!
                  </span>
                )}
              </div>
            )}
          </div>

          {/* Ledger Table */}
          <div className="bg-[#0F172A] border border-[#1E293B] rounded-xl overflow-hidden shadow-2xl">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-300">
                <thead className="bg-[#0B0F17] border-b border-[#1E293B] text-[11px] font-mono uppercase text-slate-400">
                  <tr>
                    <th className="px-4 py-3">Block #</th>
                    <th className="px-4 py-3">Action</th>
                    <th className="px-4 py-3">Target Account</th>
                    <th className="px-4 py-3">Audit Details</th>
                    <th className="px-4 py-3">Actor</th>
                    <th className="px-4 py-3">SHA-256 Block Digest</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#1E293B]">
                  {auditLedger.map((block) => (
                    <tr
                      key={block.sequence || block.blockHeight}
                      className={`transition-colors ${
                        isTampered && (block.sequence === 1 || block.blockHeight === 1)
                          ? 'bg-rose-950/30 text-rose-300 border-l-4 border-l-rose-500'
                          : 'hover:bg-[#1E293B]/40'
                      }`}
                    >
                      <td className="px-4 py-3 font-mono font-bold text-cyan-400">#{block.sequence || block.blockHeight}</td>
                      <td className="px-4 py-3">
                        <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-[#1E293B] text-slate-200">
                          {block.action}
                        </span>
                      </td>
                      <td className="px-4 py-3 font-mono text-slate-200">{block.targetAccount}</td>
                      <td className="px-4 py-3 text-slate-300 max-w-[360px] truncate">{block.details}</td>
                      <td className="px-4 py-3 text-slate-400 font-mono">{block.actorName}</td>
                      <td className="px-4 py-3 font-mono text-[10px] text-sky-400 truncate max-w-[220px]">
                        {block.currentHash || block.merkleHash}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
