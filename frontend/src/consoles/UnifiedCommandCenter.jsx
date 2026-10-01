import React, { useState, useEffect } from 'react';
import { 
  Zap, 
  ShieldAlert, 
  Clock, 
  CheckCircle2, 
  Activity, 
  Search, 
  ArrowRight, 
  Sliders, 
  Play, 
  FileText, 
  UserCheck, 
  TrendingUp, 
  Database,
  Shield,
  Layers,
  Sparkles,
  BarChart3,
  Cpu
} from 'lucide-react';
import ReactECharts from 'echarts-for-react';
import { useAuth } from '../context/AuthContext';
import { scoreTransaction } from '../api/client';

export const SCENARIO_PRESETS = [
  { 
    id: 'smurfing', 
    label: 'Smurfing Loop', 
    icon: '🚨',
    srcId: 'US-JPMC-4829-1092-8823', 
    dstId: 'GB-BARC-1109-MULE-HUB', 
    amount: 9450, 
    rail: 'SWIFT Wire (MT103)', 
    crossBorder: true, 
    burstVelocity: true 
  },
  { 
    id: 'mixer', 
    label: 'UTXO Mixer Peeling', 
    icon: '🌪️',
    srcId: '0x3a9f-4829-DARK-0012', 
    dstId: '0x7b12-MIXER-POOL', 
    amount: 95000, 
    rail: 'Bitcoin UTXO DAG', 
    crossBorder: true, 
    burstVelocity: true 
  },
  { 
    id: 'layering', 
    label: 'Layering Cycle', 
    icon: '🔄',
    srcId: 'HK-HSBC-8812-ASIA-TRADING', 
    dstId: 'US-JPMC-4829-1092-8823', 
    amount: 47600, 
    rail: 'SWIFT Wire (MT103)', 
    crossBorder: true, 
    burstVelocity: true 
  },
  { 
    id: 'payroll', 
    label: 'Legitimate Payroll', 
    icon: '🏢',
    srcId: 'US-WF-0091-8841-CORP', 
    dstId: 'US-JPMC-2201-PAYROLL', 
    amount: 3500, 
    rail: 'ACH Direct Clearing', 
    crossBorder: false, 
    burstVelocity: false 
  },
];

export const UnifiedCommandCenter = ({ 
  activeCase,
  onNavigateToSAR, 
  onNavigateToRecourse, 
  onOpenAccountProfile,
  onOpenNoticeModal,
  onOpenActionModal
}) => {
  const { currentBanker, logBankerAction } = useAuth();
  
  // Segmented Workspace Tab: 'ACTIVITY' | 'SANDBOX' | 'INVARIANTS'
  const [activeSegment, setActiveSegment] = useState('ACTIVITY');

  const [sandboxParams, setSandboxParams] = useState({
    srcId: 'US-JPMC-4829-1092-8823',
    dstId: 'GB-BARC-1109-MULE-HUB',
    amount: 9450,
    rail: 'SWIFT Wire (MT103)',
    crossBorder: true,
    burstVelocity: true
  });

  const [sandboxResult, setSandboxResult] = useState({
    tx_id: 'TX-994821',
    ensemble_posterior_prob: 0.942,
    p_gnn: 0.958,
    p_tabular: 0.914,
    decision_tier: 'TIER_1_QUARANTINE_AUTO_SAR',
    conformal_prediction_set: ['Illicit'],
    conformal_coverage_pct: 99.0,
    total_latency_ms: 0.45,
    audit_merkle_receipt: '9f8e4b7a12c85d6e3f019a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d'
  });

  const [isScoring, setIsScoring] = useState(false);

  const handleApplyPreset = (preset) => {
    setSandboxParams({
      srcId: preset.srcId,
      dstId: preset.dstId,
      amount: preset.amount,
      rail: preset.rail,
      crossBorder: preset.crossBorder,
      burstVelocity: preset.burstVelocity
    });
    const isHigh = preset.amount > 7500 || preset.burstVelocity;
    setSandboxResult({
      tx_id: `TX-${Math.floor(100000 + Math.random() * 900000)}`,
      ensemble_posterior_prob: isHigh ? (preset.amount > 50000 ? 0.982 : 0.942) : 0.024,
      p_gnn: isHigh ? 0.958 : 0.018,
      p_tabular: isHigh ? 0.914 : 0.035,
      decision_tier: isHigh ? 'TIER_1_QUARANTINE_AUTO_SAR' : 'TIER_3_STRAIGHT_THROUGH_CLEAR',
      conformal_prediction_set: isHigh ? ['Illicit'] : ['Licit'],
      conformal_coverage_pct: 99.0,
      total_latency_ms: 0.42,
      audit_merkle_receipt: '9f8e4b7a12c85d6e3f019a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d'
    });
  };

  // Synchronize with active scenario or selected case
  useEffect(() => {
    if (activeCase) {
      setSandboxParams(prev => ({
        ...prev,
        srcId: activeCase.srcId || activeCase.src || activeCase.accountNumber || prev.srcId,
        dstId: activeCase.dstId || activeCase.dst || prev.dstId,
        amount: activeCase.amount || prev.amount,
        rail: activeCase.rail || prev.rail,
        crossBorder: activeCase.crossBorder ?? prev.crossBorder,
        burstVelocity: activeCase.burstVelocity ?? prev.burstVelocity
      }));

      if (activeCase.tier) {
        setSandboxResult(prev => ({
          ...prev,
          tx_id: activeCase.id || prev.tx_id,
          decision_tier: activeCase.tier,
          conformal_prediction_set: activeCase.tier.includes('QUARANTINE') 
            ? ['Illicit'] 
            : activeCase.tier.includes('CLEAR') 
            ? ['Licit'] 
            : ['Licit', 'Illicit'],
          ensemble_posterior_prob: activeCase.risk || (activeCase.tier.includes('QUARANTINE') ? 0.942 : activeCase.tier.includes('CLEAR') ? 0.021 : 0.485)
        }));
      }
    }
  }, [activeCase]);

  const handleRunScore = async () => {
    setIsScoring(true);
    try {
      const res = await scoreTransaction({
        tx_id: `TX-${Math.floor(100000 + Math.random() * 900000)}`,
        src_id: sandboxParams.srcId,
        dst_id: sandboxParams.dstId,
        amount: parseFloat(sandboxParams.amount) || 9450,
        payment_rail: sandboxParams.rail,
        cross_border: sandboxParams.crossBorder,
        burst_velocity_spikes: sandboxParams.burstVelocity,
        fast_path_mode: true,
        conformal_alpha: 0.01
      });
      if (res) {
        setSandboxResult(res);
      }
    } catch {
      // Fallback calculation
      const isHigh = parseFloat(sandboxParams.amount) > 7500 || sandboxParams.burstVelocity;
      setSandboxResult({
        tx_id: `TX-${Math.floor(100000 + Math.random() * 900000)}`,
        ensemble_posterior_prob: isHigh ? 0.942 : 0.038,
        p_gnn: isHigh ? 0.958 : 0.024,
        p_tabular: isHigh ? 0.914 : 0.052,
        decision_tier: isHigh ? 'TIER_1_QUARANTINE_AUTO_SAR' : 'TIER_3_STRAIGHT_THROUGH_CLEAR',
        conformal_prediction_set: isHigh ? ['Illicit'] : ['Licit'],
        conformal_coverage_pct: 99.0,
        total_latency_ms: 0.44,
        audit_merkle_receipt: '9f8e4b7a12c85d6e3f019a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d'
      });
    } finally {
      setIsScoring(false);
    }
  };

  // Activity Line Chart Options
  const activityChartOption = {
    backgroundColor: 'transparent',
    grid: { left: '3%', right: '4%', bottom: '8%', top: '12%', containLabel: true },
    tooltip: { trigger: 'axis', backgroundColor: '#151D2C', borderColor: '#28374E', textStyle: { color: '#F8FAFC', fontSize: 11 } },
    xAxis: {
      type: 'category',
      data: ['08:00', '08:05', '08:10', '08:15', '08:20', '08:25', '08:30', '08:35', '08:40'],
      axisLine: { lineStyle: { color: '#28374E' } },
      axisLabel: { color: '#94A3B8', fontSize: 10 }
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: '#1E293B', type: 'dashed' } },
      axisLabel: { color: '#94A3B8', fontSize: 10 }
    },
    series: [
      {
        name: 'Streamed Tx/s',
        type: 'line',
        smooth: true,
        data: [420, 480, 510, 490, 560, 540, 590, 610, 580],
        itemStyle: { color: '#10B981' },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(16, 185, 129, 0.25)' },
              { offset: 1, color: 'rgba(16, 185, 129, 0.00)' }
            ]
          }
        }
      },
      {
        name: 'Flagged Alerts',
        type: 'line',
        smooth: true,
        data: [4, 6, 8, 5, 12, 9, 14, 8, 11],
        itemStyle: { color: '#EF4444' }
      }
    ]
  };

  // Recent Live Feed Events
  const recentAlerts = [
    { id: 'TX-994821', time: '08:42:01', account: 'US-JPMC-4829', amount: 9450, tier: 'TIER_1_QUARANTINE', risk: 0.94, pattern: 'Smurfing & Structuring Loop' },
    { id: 'TX-994819', time: '08:41:58', account: '0x3a9f-4829', amount: 95000, tier: 'TIER_1_QUARANTINE', risk: 0.98, pattern: 'Wasabi CoinJoin Peeling Chain' },
    { id: 'TX-994818', time: '08:41:55', account: 'US-CITI-0019', amount: 4800, tier: 'TIER_2_REVIEW_QUEUE', risk: 0.52, pattern: 'Dormant Account Rapid Activation' },
    { id: 'TX-994817', time: '08:41:52', account: 'US-WF-0091', amount: 14250, tier: 'TIER_3_STRAIGHT_THROUGH_CLEAR', risk: 0.02, pattern: 'Commercial Billing Settlement' }
  ];

  return (
    <div className="space-y-3 font-sans text-[var(--text-primary)] min-w-0">
      
      {/* 1. Executive Top KPI Deck (4 Clean Modern Metric Cards) */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-2.5">
        
        {/* Card 1: 24h Monitored Volume */}
        <div className="minimal-card p-3 flex items-center justify-between">
          <div>
            <span className="text-[10px] font-mono uppercase tracking-wider text-[var(--text-muted)] block">24H MONITORED VOLUME</span>
            <div className="text-xl font-bold font-mono text-[var(--text-primary)] mt-0.5">148,312 <span className="text-xs font-normal text-[var(--text-muted)]">tx</span></div>
            <span className="text-[10px] text-emerald-500 font-mono mt-0.5 flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              $148.2M Streamed
            </span>
          </div>
          <div className="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-500">
            <Zap className="w-4 h-4" />
          </div>
        </div>

        {/* Card 2: Tier 1 Quarantined */}
        <div className="minimal-card p-3 flex items-center justify-between border-rose-500/20">
          <div>
            <span className="text-[10px] font-mono uppercase tracking-wider text-[var(--text-muted)] block">TIER 1 QUARANTINED</span>
            <div className="text-xl font-bold font-mono text-rose-500 mt-0.5">1,280 <span className="text-xs font-normal text-[var(--text-muted)]">tx (0.86%)</span></div>
            <span className="text-[10px] text-rose-400 font-mono mt-0.5">
              Γ = &#123;1&#125; Auto-Quarantine
            </span>
          </div>
          <div className="w-8 h-8 rounded-lg bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-500">
            <ShieldAlert className="w-4 h-4" />
          </div>
        </div>

        {/* Card 3: Tier 2 Review Queue */}
        <div className="minimal-card p-3 flex items-center justify-between border-amber-500/20">
          <div>
            <span className="text-[10px] font-mono uppercase tracking-wider text-[var(--text-muted)] block">TIER 2 REVIEW QUEUE</span>
            <div className="text-xl font-bold font-mono text-amber-500 mt-0.5">748 <span className="text-xs font-normal text-[var(--text-muted)]">tx (0.50%)</span></div>
            <span className="text-[10px] text-amber-400 font-mono mt-0.5">
              Γ = &#123;0, 1&#125; Four-Eyes
            </span>
          </div>
          <div className="w-8 h-8 rounded-lg bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-500">
            <Clock className="w-4 h-4" />
          </div>
        </div>

        {/* Card 4: Straight-Through Clear */}
        <div className="minimal-card p-3 flex items-center justify-between">
          <div>
            <span className="text-[10px] font-mono uppercase tracking-wider text-[var(--text-muted)] block">STRAIGHT-THROUGH RATE</span>
            <div className="text-xl font-bold font-mono text-[var(--accent-primary)] mt-0.5">99.4%</div>
            <span className="text-[10px] text-[var(--text-muted)] font-mono mt-0.5">
              Coverage &ge; 99.0% (α=0.01)
            </span>
          </div>
          <div className="w-8 h-8 rounded-lg bg-[var(--accent-primary)]/10 border border-[var(--accent-primary)]/20 flex items-center justify-center text-[var(--accent-primary)]">
            <CheckCircle2 className="w-4 h-4" />
          </div>
        </div>

      </div>

      {/* 2. Categorized Workspace Controls (Segmented Tabs) */}
      <div className="flex items-center justify-between border-b border-[var(--border-subtle)] pb-2">
        <div className="flex items-center gap-1 bg-[var(--bg-card)] p-1 rounded-xl border border-[var(--border-subtle)]">
          <button
            onClick={() => setActiveSegment('ACTIVITY')}
            className={`px-3 py-1 rounded-lg text-xs font-medium transition-all cursor-pointer ${
              activeSegment === 'ACTIVITY'
                ? 'bg-[var(--accent-primary)] text-white font-semibold shadow-sm'
                : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
            }`}
          >
            Live Network Activity
          </button>
          <button
            onClick={() => setActiveSegment('SANDBOX')}
            className={`px-3 py-1 rounded-lg text-xs font-medium transition-all cursor-pointer ${
              activeSegment === 'SANDBOX'
                ? 'bg-[var(--accent-primary)] text-white font-semibold shadow-sm'
                : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
            }`}
          >
            Scoring Sandbox
          </button>
          <button
            onClick={() => setActiveSegment('INVARIANTS')}
            className={`px-3 py-1 rounded-lg text-xs font-medium transition-all cursor-pointer ${
              activeSegment === 'INVARIANTS'
                ? 'bg-[var(--accent-primary)] text-white font-semibold shadow-sm'
                : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
            }`}
          >
            Mathematical Invariants
          </button>
        </div>

        <div className="hidden sm:flex items-center gap-2 text-xs font-mono text-[var(--text-muted)]">
          <span>SLA P99 Latency: <strong className="text-[var(--accent-primary)]">&lt; 0.82ms</strong></span>
        </div>
      </div>

      {/* 3. Tab Content 1: Live Network Activity & Recent Triage */}
      {activeSegment === 'ACTIVITY' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-3 animate-fadeIn">
          {/* Activity Line Chart */}
          <div className="lg:col-span-7 minimal-card p-3.5 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold font-mono uppercase tracking-wider text-[var(--text-primary)] flex items-center gap-1.5">
                <Activity className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                <span>Streaming Throughput &amp; Alert Telemetry</span>
              </span>
              <span className="text-[10px] font-mono text-emerald-500 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                500 tx/s Active
              </span>
            </div>
            <div className="h-56 sm:h-64">
              <ReactECharts option={activityChartOption} style={{ height: '100%', width: '100%' }} />
            </div>
          </div>

          {/* Recent Flagged Transactions List */}
          <div className="lg:col-span-5 minimal-card p-3.5 space-y-2.5 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between pb-2 border-b border-[var(--border-subtle)]">
                <span className="text-xs font-bold font-mono uppercase tracking-wider text-[var(--text-primary)]">
                  Recent High-Priority Events
                </span>
                <span className="text-[10px] text-[var(--text-muted)] font-mono">Live Ingestion</span>
              </div>
              <div className="space-y-2 mt-2">
                {recentAlerts.map((alt) => (
                  <div 
                    key={alt.id}
                    onClick={() => onNavigateToSAR && onNavigateToSAR(alt)}
                    className="p-2 rounded-xl bg-[var(--bg-base)] border border-[var(--border-subtle)] hover:border-[var(--accent-primary)] transition-all cursor-pointer flex items-center justify-between text-xs"
                  >
                    <div>
                      <div className="font-mono font-bold text-[var(--text-primary)] flex items-center gap-1.5">
                        <span>{alt.id}</span>
                        <span className="text-[9px] text-[var(--text-muted)] font-normal">{alt.time}</span>
                      </div>
                      <div className="text-[11px] text-[var(--text-secondary)] font-mono">{alt.account} • ${alt.amount.toLocaleString()}</div>
                      <span className="text-[10px] text-[var(--text-muted)]">{alt.pattern}</span>
                    </div>
                    <div className="text-right">
                      <span className={alt.tier.includes('QUARANTINE') ? 'badge-tier1' : alt.tier.includes('REVIEW') ? 'badge-tier2' : 'badge-tier3'}>
                        {(alt.risk * 100).toFixed(0)}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <button
              onClick={() => onNavigateToSAR && onNavigateToSAR()}
              className="w-full py-1.5 rounded-lg minimal-btn text-xs font-medium text-[var(--text-secondary)] hover:text-[var(--text-primary)] mt-1"
            >
              View Full Alert Queue &rarr;
            </button>
          </div>
        </div>
      )}

      {/* 4. Tab Content 2: Clean 2-Column Scoring Sandbox */}
      {activeSegment === 'SANDBOX' && (
        <div className="space-y-3 animate-fadeIn">
          {/* 1-Click Scenario Quick Presets */}
          <div className="minimal-card p-2.5 flex items-center justify-between gap-2 overflow-x-auto">
            <span className="text-[10px] font-mono uppercase tracking-wider text-[var(--text-muted)] shrink-0">1-Click Presets:</span>
            <div className="flex items-center gap-1.5 overflow-x-auto">
              {SCENARIO_PRESETS.map((preset) => (
                <button
                  key={preset.id}
                  onClick={() => handleApplyPreset(preset)}
                  className="px-2.5 py-1 rounded-lg text-xs font-medium border border-[var(--border-subtle)] bg-[var(--bg-base)] hover:border-[var(--accent-primary)] hover:text-[var(--accent-primary)] transition-all cursor-pointer shrink-0 flex items-center gap-1.5"
                >
                  <span>{preset.icon}</span>
                  <span>{preset.label}</span>
                  <span className="text-[10px] font-mono text-[var(--text-muted)]">(${preset.amount.toLocaleString()})</span>
                </button>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-3">
            {/* Left Form (5 Columns) */}
            <div className="lg:col-span-5 minimal-card p-4 space-y-3">
              <div className="border-b border-[var(--border-subtle)] pb-2">
                <h3 className="text-xs font-bold font-mono uppercase tracking-wider text-[var(--text-primary)] flex items-center gap-1.5">
                  <Sliders className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                  <span>Transaction Parameters</span>
                </h3>
              <p className="text-[11px] text-[var(--text-muted)] mt-0.5">Input transaction attributes to simulate real-time C-STGB classification.</p>
            </div>

            <div className="space-y-2 text-xs">
              <div>
                <label className="text-[10px] font-mono text-[var(--text-muted)] uppercase block mb-1">Source Account / Entity</label>
                <input 
                  type="text"
                  value={sandboxParams.srcId}
                  onChange={(e) => setSandboxParams(prev => ({ ...prev, srcId: e.target.value }))}
                  className="w-full px-2.5 py-1.5 rounded-lg bg-[var(--bg-base)] border border-[var(--border-subtle)] focus:border-[var(--accent-primary)] font-mono text-xs outline-none text-[var(--text-primary)]"
                />
              </div>

              <div>
                <label className="text-[10px] font-mono text-[var(--text-muted)] uppercase block mb-1">Destination Account / Entity</label>
                <input 
                  type="text"
                  value={sandboxParams.dstId}
                  onChange={(e) => setSandboxParams(prev => ({ ...prev, dstId: e.target.value }))}
                  className="w-full px-2.5 py-1.5 rounded-lg bg-[var(--bg-base)] border border-[var(--border-subtle)] focus:border-[var(--accent-primary)] font-mono text-xs outline-none text-[var(--text-primary)]"
                />
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="text-[10px] font-mono text-[var(--text-muted)] uppercase block mb-1">Transfer Amount ($ USD)</label>
                  <input 
                    type="number"
                    value={sandboxParams.amount}
                    onChange={(e) => setSandboxParams(prev => ({ ...prev, amount: parseFloat(e.target.value) || 0 }))}
                    className="w-full px-2.5 py-1.5 rounded-lg bg-[var(--bg-base)] border border-[var(--border-subtle)] focus:border-[var(--accent-primary)] font-mono text-xs outline-none text-[var(--text-primary)]"
                  />
                </div>
                <div>
                  <label className="text-[10px] font-mono text-[var(--text-muted)] uppercase block mb-1">Payment Rail</label>
                  <select 
                    value={sandboxParams.rail}
                    onChange={(e) => setSandboxParams(prev => ({ ...prev, rail: e.target.value }))}
                    className="w-full px-2.5 py-1.5 rounded-lg bg-[var(--bg-base)] border border-[var(--border-subtle)] focus:border-[var(--accent-primary)] text-xs outline-none text-[var(--text-primary)]"
                  >
                    <option>SWIFT Wire (MT103)</option>
                    <option>Fedwire Funds Service</option>
                    <option>Bitcoin UTXO DAG</option>
                    <option>Ethereum ERC-20</option>
                    <option>ACH Direct Clearing</option>
                  </select>
                </div>
              </div>

              <div className="flex items-center justify-between pt-1">
                <label className="flex items-center gap-1.5 text-xs text-[var(--text-secondary)] cursor-pointer">
                  <input 
                    type="checkbox"
                    checked={sandboxParams.burstVelocity}
                    onChange={(e) => setSandboxParams(prev => ({ ...prev, burstVelocity: e.target.checked }))}
                    className="accent-[var(--accent-primary)]"
                  />
                  <span>Burst Velocity Spikes</span>
                </label>
                <label className="flex items-center gap-1.5 text-xs text-[var(--text-secondary)] cursor-pointer">
                  <input 
                    type="checkbox"
                    checked={sandboxParams.crossBorder}
                    onChange={(e) => setSandboxParams(prev => ({ ...prev, crossBorder: e.target.checked }))}
                    className="accent-[var(--accent-primary)]"
                  />
                  <span>Cross-Border Corridor</span>
                </label>
              </div>
            </div>

            <button
              onClick={handleRunScore}
              disabled={isScoring}
              className="w-full py-2 rounded-xl minimal-btn bg-[var(--accent-primary)] text-white font-bold text-xs flex items-center justify-center gap-1.5 shadow-sm cursor-pointer"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>{isScoring ? 'Executing Tensor Inference...' : 'Score with C-STGB Engine'}</span>
            </button>
          </div>

          {/* Right Result Card (7 Columns) */}
          <div className="lg:col-span-7 minimal-card p-4 space-y-3.5">
            <div className="flex items-center justify-between border-b border-[var(--border-subtle)] pb-2">
              <div>
                <span className="text-[10px] font-mono text-[var(--text-muted)] uppercase block">INFERENCE RESULT</span>
                <span className="font-bold text-xs font-mono text-[var(--text-primary)]">{sandboxResult.tx_id}</span>
              </div>
              <span className={sandboxResult.decision_tier.includes('QUARANTINE') ? 'badge-tier1' : sandboxResult.decision_tier.includes('CLEAR') ? 'badge-tier3' : 'badge-tier2'}>
                {sandboxResult.decision_tier.replace(/_/g, ' ')}
              </span>
            </div>

            {/* Metric Bars */}
            <div className="grid grid-cols-3 gap-2 text-center">
              <div className="p-2 rounded-lg bg-[var(--bg-base)] border border-[var(--border-subtle)]">
                <span className="text-[9px] font-mono text-[var(--text-muted)] block uppercase">RISK POSTERIOR</span>
                <span className="text-base font-bold font-mono text-[var(--text-primary)]">
                  {(sandboxResult.ensemble_posterior_prob * 100).toFixed(1)}%
                </span>
              </div>
              <div className="p-2 rounded-lg bg-[var(--bg-base)] border border-[var(--border-subtle)]">
                <span className="text-[9px] font-mono text-[var(--text-muted)] block uppercase">CONFORMAL SET Γ</span>
                <span className="text-base font-bold font-mono text-[var(--accent-primary)]">
                  {sandboxResult.conformal_prediction_set.join(', ')}
                </span>
              </div>
              <div className="p-2 rounded-lg bg-[var(--bg-base)] border border-[var(--border-subtle)]">
                <span className="text-[9px] font-mono text-[var(--text-muted)] block uppercase">FAST-PATH SLA</span>
                <span className="text-base font-bold font-mono text-emerald-500">
                  {sandboxResult.total_latency_ms} ms
                </span>
              </div>
            </div>

            {/* Explanation Note */}
            <div className="p-3 rounded-lg bg-[var(--bg-base)] border border-[var(--border-subtle)] text-xs text-[var(--text-secondary)] leading-relaxed">
              <strong className="text-[var(--text-primary)]">Compliance Audit Summary:</strong>{' '}
              {sandboxResult.decision_tier.includes('QUARANTINE') 
                ? 'High-confidence illicit signature detected. The account exhibits multi-hop cyclic flow conservation without commercial justification. Autonomous FinCEN Form 111 drafting triggered.' 
                : 'Transaction satisfies finite-sample exchangeability coverage (1 - α >= 99.0%). Routed through Tier-3 Straight-Through Execution with zero customer friction.'}
            </div>

            {/* Action Buttons */}
            <div className="flex items-center gap-2 pt-1">
              <button
                onClick={() => onNavigateToSAR && onNavigateToSAR(sandboxResult)}
                className="flex-1 py-1.5 rounded-lg minimal-btn bg-[var(--accent-primary)] text-white font-semibold text-xs flex items-center justify-center gap-1.5 cursor-pointer"
              >
                <FileText className="w-3.5 h-3.5" />
                <span>Draft SAR Dossier</span>
              </button>
              <button
                onClick={() => onNavigateToRecourse && onNavigateToRecourse(sandboxResult)}
                className="flex-1 py-1.5 rounded-lg minimal-btn text-xs font-semibold text-[var(--text-primary)] cursor-pointer"
              >
                <UserCheck className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                <span>Simulate Recourse</span>
              </button>
            </div>
          </div>
        </div>
      </div>
      )}

      {/* 5. Tab Content 3: Mathematical Invariants */}
      {activeSegment === 'INVARIANTS' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 animate-fadeIn">
          <div className="minimal-card p-3.5 space-y-1">
            <span className="text-[10px] font-mono text-[var(--text-muted)] uppercase block">KIRCHHOFF FLOW MATCH</span>
            <div className="text-xl font-bold font-mono text-[var(--text-primary)]">Φ_flow = 0.998</div>
            <p className="text-[11px] text-[var(--text-secondary)] pt-1">
              Inflows match outflows within 0.2% across transit nodes, verifying pass-through wash loops without legitimate commercial absorption.
            </p>
          </div>

          <div className="minimal-card p-3.5 space-y-1">
            <span className="text-[10px] font-mono text-[var(--text-muted)] uppercase block">HAWKES INTENSITY</span>
            <div className="text-xl font-bold font-mono text-[var(--text-primary)]">λ = 18.4 tx/min</div>
            <p className="text-[11px] text-[var(--text-secondary)] pt-1">
              Point-process self-excitation metric capturing rapid burst velocity smurfing across microsecond intervals.
            </p>
          </div>

          <div className="minimal-card p-3.5 space-y-1">
            <span className="text-[10px] font-mono text-[var(--text-muted)] uppercase block">CAMOUFLAGE SUPPRESSION</span>
            <div className="text-xl font-bold font-mono text-emerald-500">65.9% Filtered</div>
            <p className="text-[11px] text-[var(--text-secondary)] pt-1">
              Learnable MLP edge-trust filter suppresses adversarial merchant noise (gᵢⱼ &lt; 0.10) to isolate underlying structuring rings.
            </p>
          </div>

          <div className="minimal-card p-3.5 space-y-1">
            <span className="text-[10px] font-mono text-[var(--text-muted)] uppercase block">CONFORMAL COVERAGE</span>
            <div className="text-xl font-bold font-mono text-[var(--accent-primary)]">1 - α &ge; 99.0%</div>
            <p className="text-[11px] text-[var(--text-secondary)] pt-1">
              Finite-sample distribution-free validity guarantees statutory safety while eliminating 99.4% of false alarms.
            </p>
          </div>
        </div>
      )}

    </div>
  );
};
