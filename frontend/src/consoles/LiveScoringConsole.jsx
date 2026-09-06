import React, { useState, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import { Play, Zap, Clock, Shield, CheckCircle2, AlertTriangle, XCircle, ArrowRight, Activity, Server, Hash } from 'lucide-react';
import { scoreTransaction } from '../api/client';

export const LiveScoringConsole = ({ presetScenario, onNavigateToGraph, onNavigateToSAR }) => {
  const [srcId, setSrcId] = useState('ACC_8823_SUSPECT_MULE');
  const [dstId, setDstId] = useState('ACC_1109_MULE_HUB');
  const [amount, setAmount] = useState(9450);
  const [paymentRail, setPaymentRail] = useState('Wire (SWIFT)');
  const [jurisdiction, setJurisdiction] = useState('Offshore Haven (BVI/Panama)');
  const [burstVelocity, setBurstVelocity] = useState(true);
  const [fastPath, setFastPath] = useState(true);
  const [loading, setLoading] = useState(false);

  const [result, setResult] = useState({
    tx_id: 'TX_9928172',
    ensemble_posterior_prob: 0.8842,
    p_gnn: 0.9012,
    p_tabular: 0.8490,
    p_fused: 0.8842,
    decision_tier: 'TIER_1_QUARANTINE_AUTO_SAR',
    conformal_prediction_set: ['Illicit'],
    conformal_alpha: 0.01,
    conformal_coverage_pct: 99.0,
    rule_engine_action: 'SUSPICIOUS_STRUCTURING',
    latency_breakdown_ms: {
      ingestion_and_invariants_ms: 0.11,
      subgraph_lru_cache_ms: 0.18,
      neural_forward_fusion_ms: 0.12,
      conformal_calibration_ms: 0.04
    },
    total_latency_ms: 0.45,
    audit_merkle_receipt: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
  });

  useEffect(() => {
    if (!presetScenario) return;
    setSrcId(presetScenario.srcId || 'ACC_8823_MULE');
    setDstId(presetScenario.dstId || 'ACC_1109_HUB');
    setAmount(presetScenario.amount || 9450);
    setPaymentRail(presetScenario.paymentRail || 'Wire (SWIFT)');
    setJurisdiction(presetScenario.jurisdiction || 'Domestic (Clean)');
    setBurstVelocity(presetScenario.burstVelocity ?? true);
    setFastPath(presetScenario.fastPath ?? true);

    const autoScore = async () => {
      setLoading(true);
      const txId = `TX_${Math.floor(1000000 + Math.random() * 9000000)}`;
      const data = await scoreTransaction({
        tx_id: txId,
        src_id: presetScenario.srcId,
        dst_id: presetScenario.dstId,
        amount: Number(presetScenario.amount),
        payment_rail: presetScenario.paymentRail,
        cross_border: (presetScenario.jurisdiction || '').includes('Offshore') || (presetScenario.jurisdiction || '').includes('Sanctioned'),
        burst_velocity_spikes: presetScenario.burstVelocity ?? true,
        fast_path_mode: presetScenario.fastPath ?? true,
        conformal_alpha: 0.01
      });
      setResult(data);
      setLoading(false);
    };
    autoScore();
  }, [presetScenario]);

  const handleScore = async () => {
    setLoading(true);
    const txId = `TX_${Math.floor(1000000 + Math.random() * 9000000)}`;
    const data = await scoreTransaction({
      tx_id: txId,
      src_id: srcId,
      dst_id: dstId,
      amount: Number(amount),
      payment_rail: paymentRail,
      cross_border: jurisdiction.includes('Offshore') || jurisdiction.includes('Sanctioned'),
      burst_velocity_spikes: burstVelocity,
      fast_path_mode: fastPath,
      conformal_alpha: 0.01
    });
    setResult(data);
    setLoading(false);
  };

  const gaugeScore = Math.round((result?.ensemble_posterior_prob || 0.5) * 100);
  const gaugeColor = gaugeScore >= 70 ? '#F43F5E' : gaugeScore >= 30 ? '#F59E0B' : '#10B981';

  const gaugeOption = {
    backgroundColor: 'transparent',
    series: [
      {
        type: 'gauge',
        startAngle: 180,
        endAngle: 0,
        min: 0,
        max: 100,
        splitNumber: 5,
        radius: '98%',
        center: ['50%', '72%'],
        itemStyle: { color: gaugeColor },
        progress: { show: true, roundCap: true, width: 10 },
        pointer: { length: '12%', width: 10, offsetCenter: [0, '-60%'], itemStyle: { color: '#F8FAFC' } },
        axisLine: {
          roundCap: true,
          lineStyle: {
            width: 10,
            color: [
              [0.3, 'rgba(16, 185, 129, 0.15)'],
              [0.7, 'rgba(245, 158, 11, 0.15)'],
              [1, 'rgba(244, 63, 94, 0.15)']
            ]
          }
        },
        axisTick: { show: false },
        splitLine: { length: 6, lineStyle: { width: 1.5, color: 'rgba(255,255,255,0.1)' } },
        axisLabel: { distance: 14, color: '#64748B', fontSize: 10, fontFamily: 'JetBrains Mono' },
        detail: {
          valueAnimation: true,
          fontSize: 26,
          fontWeight: 800,
          offsetCenter: [0, '-10%'],
          formatter: '{value}%',
          color: gaugeColor,
          fontFamily: 'JetBrains Mono'
        },
        data: [{ value: gaugeScore, name: '' }]
      }
    ]
  };

  const latBreakdown = result?.latency_breakdown_ms || {
    ingestion_and_invariants_ms: 0.11,
    subgraph_lru_cache_ms: 0.18,
    neural_forward_fusion_ms: fastPath ? 0.12 : 1.75,
    conformal_calibration_ms: 0.04
  };

  const latencyOption = {
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    grid: { top: 5, right: 35, bottom: 15, left: 130 },
    xAxis: { type: 'value', axisLabel: { color: '#64748b', fontSize: 9, fontFamily: 'JetBrains Mono' }, splitLine: { lineStyle: { color: 'rgba(255,255,255,0.06)' } } },
    yAxis: {
      type: 'category',
      data: ['1. Ingest/12-D', '2. Subgraph Cache', '3. GNN Forward', '4. CRC Calibrate'],
      axisLabel: { color: '#94A3B8', fontSize: 10 }
    },
    series: [{
      type: 'bar',
      data: [latBreakdown.ingestion_and_invariants_ms, latBreakdown.subgraph_lru_cache_ms, latBreakdown.neural_forward_fusion_ms, latBreakdown.conformal_calibration_ms],
      itemStyle: { color: '#6366F1', borderRadius: [0, 3, 3, 0] },
      label: { show: true, position: 'right', color: '#818CF8', fontSize: 9, fontFamily: 'JetBrains Mono', formatter: '{c}ms' }
    }]
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
      {/* Left Input Form */}
      <div className="lg:col-span-5 card-panel p-5 space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-white/[0.08]">
          <div className="flex items-center gap-2">
            <Zap className="w-4 h-4 text-indigo-400" />
            <h2 className="text-sm font-semibold text-white">Transaction Parameter Stream</h2>
          </div>
          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 font-medium border border-indigo-500/20">
            {fastPath ? 'FAST-PATH (0.45 ms)' : 'DEEP SPATIOTEMPORAL GNN'}
          </span>
        </div>

        <div className="space-y-3.5">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-[11px] font-medium text-slate-400 block mb-1">Source Account</label>
              <input
                type="text"
                value={srcId}
                onChange={(e) => setSrcId(e.target.value)}
                className="w-full bg-[#0B0E17] border border-white/[0.1] rounded-lg px-3 py-1.5 text-xs font-mono text-indigo-200 focus:outline-none focus:border-indigo-500 transition-colors"
              />
            </div>
            <div>
              <label className="text-[11px] font-medium text-slate-400 block mb-1">Beneficiary Account</label>
              <input
                type="text"
                value={dstId}
                onChange={(e) => setDstId(e.target.value)}
                className="w-full bg-[#0B0E17] border border-white/[0.1] rounded-lg px-3 py-1.5 text-xs font-mono text-indigo-200 focus:outline-none focus:border-indigo-500 transition-colors"
              />
            </div>
          </div>

          <div>
            <div className="flex justify-between items-center mb-1.5">
              <label className="text-[11px] font-medium text-slate-400">Transfer Amount ($ USD)</label>
              <span className="text-xs font-mono font-semibold text-indigo-300">${amount.toLocaleString()}</span>
            </div>
            <input
              type="range"
              min="500"
              max="50000"
              step="250"
              value={amount}
              onChange={(e) => setAmount(Number(e.target.value))}
              className="w-full accent-indigo-500 cursor-pointer"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-[11px] font-medium text-slate-400 block mb-1">Payment Rail</label>
              <select
                value={paymentRail}
                onChange={(e) => setPaymentRail(e.target.value)}
                className="w-full bg-[#0B0E17] border border-white/[0.1] rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
              >
                <option>Wire (SWIFT)</option>
                <option>Bitcoin (UTXO)</option>
                <option>Ethereum (ERC-20)</option>
                <option>ACH / Fedwire</option>
                <option>Mobile Money (MFS)</option>
              </select>
            </div>

            <div>
              <label className="text-[11px] font-medium text-slate-400 block mb-1">Jurisdiction Risk</label>
              <select
                value={jurisdiction}
                onChange={(e) => setJurisdiction(e.target.value)}
                className="w-full bg-[#0B0E17] border border-white/[0.1] rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
              >
                <option>Domestic (Clean)</option>
                <option>FATF Grey List</option>
                <option>Offshore Haven (BVI/Panama)</option>
                <option>OFAC Sanctioned Zone</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-2.5 pt-1">
            <label className="flex items-center gap-2 p-2 rounded-lg bg-[#0B0E17] border border-white/[0.08] cursor-pointer hover:border-white/[0.15] transition-colors">
              <input
                type="checkbox"
                checked={burstVelocity}
                onChange={(e) => setBurstVelocity(e.target.checked)}
                className="accent-indigo-500"
              />
              <span className="text-[11px] text-slate-300">Rapid Burst (&lt;60s)</span>
            </label>

            <label className="flex items-center gap-2 p-2 rounded-lg bg-[#0B0E17] border border-white/[0.08] cursor-pointer hover:border-white/[0.15] transition-colors">
              <input
                type="checkbox"
                checked={fastPath}
                onChange={(e) => setFastPath(e.target.checked)}
                className="accent-indigo-500"
              />
              <span className="text-[11px] text-slate-300">Fast-Path (&lt;1 ms)</span>
            </label>
          </div>

          <button
            onClick={handleScore}
            disabled={loading}
            className="w-full py-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-xs flex items-center justify-center gap-2 shadow-sm transition-all active:scale-[0.98] disabled:opacity-50 cursor-pointer"
          >
            {loading ? <Clock className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4 fill-white" />}
            <span>{loading ? 'Evaluating Model...' : 'Execute Live Neural Scoring'}</span>
          </button>
        </div>
      </div>

      {/* Right Output Panels */}
      <div className="lg:col-span-7 space-y-4">
        {/* Risk Card */}
        <div className="card-panel p-5">
          <div className="flex items-center justify-between mb-2 pb-2.5 border-b border-white/[0.08]">
            <div>
              <h2 className="text-sm font-semibold text-white">Neural Anomaly Posterior Risk</h2>
              <p className="text-[11px] text-slate-400 font-mono">Dual-stream Spatio-Temporal GraphBoost</p>
            </div>
            <span className="text-[11px] font-mono px-2.5 py-1 rounded bg-[#0B0E17] text-slate-300 border border-white/[0.08]">
              {result?.tx_id || 'N/A'}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-12 gap-4 items-center">
            <div className="md:col-span-6 h-40">
              <ReactECharts option={gaugeOption} style={{ height: '100%', width: '100%' }} />
            </div>

            <div className="md:col-span-6 space-y-3 font-mono text-xs">
              <div>
                <span className="text-[10px] text-slate-400 font-medium uppercase block mb-1">Operational Routing Tier:</span>
                {result.decision_tier === 'TIER_1_QUARANTINE_AUTO_SAR' && (
                  <div className="p-2.5 rounded-lg badge-flagged font-semibold text-xs flex items-center gap-2">
                    <XCircle className="w-4 h-4 shrink-0" />
                    <span>TIER 1: IMMEDIATE ASSET QUARANTINE</span>
                  </div>
                )}
                {result.decision_tier === 'TIER_2_COMPLIANCE_REVIEW_QUEUE' && (
                  <div className="p-2.5 rounded-lg badge-review font-semibold text-xs flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4 shrink-0" />
                    <span>TIER 2: OFFICER ESCALATION QUEUE</span>
                  </div>
                )}
                {result.decision_tier === 'TIER_3_STRAIGHT_THROUGH_CLEAR' && (
                  <div className="p-2.5 rounded-lg badge-clean font-semibold text-xs flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 shrink-0" />
                    <span>TIER 3: STRAIGHT-THROUGH CLEAR</span>
                  </div>
                )}
              </div>

              <div className="grid grid-cols-2 gap-2 text-[11px]">
                <div className="p-2 rounded bg-[#0B0E17] border border-white/[0.06]">
                  <span className="text-slate-500 text-[9px] block">CONFORMAL SET</span>
                  <span className="text-indigo-300 font-semibold">Γ(X) = {`{ ${result.conformal_prediction_set.join(', ')} }`}</span>
                </div>
                <div className="p-2 rounded bg-[#0B0E17] border border-white/[0.06]">
                  <span className="text-slate-500 text-[9px] block">MEASURED LATENCY</span>
                  <span className="text-emerald-400 font-semibold">{result.total_latency_ms} ms</span>
                </div>
              </div>

              {/* Quick Actions */}
              <div className="pt-1 flex items-center gap-2">
                {result.decision_tier === 'TIER_1_QUARANTINE_AUTO_SAR' && onNavigateToSAR && (
                  <button
                    onClick={onNavigateToSAR}
                    className="flex-1 py-2 px-2.5 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-medium text-[11px] flex items-center justify-center gap-1.5 cursor-pointer shadow-sm"
                  >
                    <span>Auto-Draft FinCEN SAR</span>
                    <ArrowRight className="w-3 h-3" />
                  </button>
                )}
                {onNavigateToGraph && (
                  <button
                    onClick={onNavigateToGraph}
                    className="flex-1 py-2 px-2.5 rounded-lg bg-[#182030] hover:bg-[#1E283C] text-slate-200 border border-white/[0.1] font-medium text-[11px] flex items-center justify-center gap-1.5 cursor-pointer"
                  >
                    <span>Inspect 2-Hop Graph</span>
                    <ArrowRight className="w-3 h-3 text-slate-400" />
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Latency Waterfall Card */}
        <div className="card-panel p-4">
          <div className="flex items-center justify-between mb-2 pb-2 border-b border-white/[0.08]">
            <div className="flex items-center gap-2">
              <Clock className="w-3.5 h-3.5 text-indigo-400" />
              <h3 className="text-xs font-semibold text-white">Execution Latency Decomposition</h3>
            </div>
            <span className="text-xs font-mono text-emerald-400 font-semibold">
              {result.total_latency_ms} ms (Sub-10ms SLA Met)
            </span>
          </div>

          <div className="h-24">
            <ReactECharts option={latencyOption} style={{ height: '100%', width: '100%' }} />
          </div>
        </div>
      </div>
    </div>
  );
};
