import React, { useState, useEffect, useRef } from 'react';
import { 
  Inbox,
  ShieldAlert, 
  CheckCircle2, 
  Clock, 
  Play, 
  Pause, 
  Zap, 
  Search, 
  Maximize2, 
  Minimize2, 
  RotateCcw, 
  ZoomIn, 
  ZoomOut, 
  FileText, 
  AlertOctagon, 
  Sparkles, 
  Layers, 
  ArrowRight, 
  Shield, 
  Lock, 
  Unlock, 
  Check, 
  Share2, 
  Eye, 
  Cpu, 
  Activity, 
  Sliders, 
  ExternalLink, 
  DollarSign, 
  UserCheck, 
  Mail, 
  Building2, 
  User, 
  Radio, 
  HelpCircle, 
  TrendingUp, 
  AlertTriangle, 
  Box, 
  RefreshCw, 
  Compass,
  FileDown,
  CheckCheck,
  ChevronDown
} from 'lucide-react';
import { Neo4j3DGraph } from '../components/Neo4j3DGraph';
import { useAuth } from '../context/AuthContext';
import { runAgentInvestigation, scoreTransaction } from '../api/client';

export const UnifiedCommandCenter = ({ 
  onNavigateToSAR, 
  onNavigateToRecourse, 
  onOpenAccountProfile,
  onOpenNoticeModal,
  onOpenActionModal
}) => {
  const { currentBanker, logBankerAction } = useAuth();
  const [selectedDataset, setSelectedDataset] = useState('Elliptic Bitcoin (DAG)');
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
    p_fused: 0.942,
    decision_tier: 'TIER_1_QUARANTINE_AUTO_SAR',
    conformal_prediction_set: ['Illicit'],
    conformal_alpha: 0.01,
    conformal_coverage_pct: 99.0,
    rule_engine_action: 'SUSPICIOUS_STRUCTURING_LOOP',
    latency_breakdown_ms: {
      ingestion_and_invariants_ms: 0.11,
      subgraph_lru_cache_ms: 0.18,
      neural_forward_fusion_ms: 0.12,
      conformal_calibration_ms: 0.04
    },
    total_latency_ms: 0.45,
    audit_merkle_receipt: '9f8e4b7a12c85d6e3f019a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d'
  });
  const [isSandboxScoring, setIsSandboxScoring] = useState(false);
  const [selectedNode, setSelectedNode] = useState({
    id: '0x8f9c-4829-MULE-b4a1',
    role: 'Layering Mule Hub',
    code: 'M_1',
    risk: 0.942,
    intervalLow: 0.914,
    intervalHigh: 0.978,
    tier: 'TIER_2_REVIEW_QUEUE',
    gammaSet: '{0, 1}',
    gammaLabel: 'Tier 2: Officer Review Queue',
    kirchhoff: 0.998,
    hawkesIntensity: 18.4,
    camouflagePruned: '65.9%',
    fusionAlpha: 0.88,
    fusionLabel: 'Topology-Dominated GNN',
    counterparties: 6
  });

  const [lowerTab, setLowerTab] = useState('ACTIVE_QUEUE'); // 'ACTIVE_QUEUE', 'AGENT_STREAM', 'SAR_PREVIEW'
  const [freezeSuccess, setFreezeSuccess] = useState(false);
  const [dismissSuccess, setDismissSuccess] = useState(false);
  const [physicsLocked, setPhysicsLocked] = useState(false);
  const [camouflageActive, setCamouflageActive] = useState(true);
  const [resetTick, setResetTick] = useState(0);

  // Active Real-Time Alerts Queue Data
  const queueAlerts = [
    { id: '#ALT-9042', timestamp: '20:24:11 UTC', src: '0x3a9f...11', dst: '0x9f12...4a', volume: '4.82 BTC (~$284k)', decision: 'Tier 2 {0, 1}', decisionClass: 'badge-tier2', status: 'ACTION_REQ', risk: 0.942 },
    { id: '#ALT-9041', timestamp: '20:23:58 UTC', src: '0x88c4...c4', dst: '0x1209...09', volume: '48,200 USD', decision: 'Tier 1 {1}', decisionClass: 'badge-tier1', status: 'AUTO_QUARANTINED', risk: 0.985 },
    { id: '#ALT-9040', timestamp: '20:23:42 UTC', src: 'US-CITI-4412', dst: 'GB-BARC-1109', volume: '9,450 USD', decision: 'Tier 1 {1}', decisionClass: 'badge-tier1', status: 'AUTO_QUARANTINED', risk: 0.962 },
    { id: '#ALT-9039', timestamp: '20:23:25 UTC', src: 'SG-DBS-8819', dst: 'US-WF-0091', volume: '14,250 USD', decision: 'Tier 3 {0}', decisionClass: 'badge-tier3', status: 'CLEARED', risk: 0.015 },
    { id: '#ALT-9038', timestamp: '20:23:10 UTC', src: 'DE-DB-9901', dst: 'FR-BNP-3312', volume: '6,200 EUR', decision: 'Tier 2 {0, 1}', decisionClass: 'badge-tier2', status: 'ACTION_REQ', risk: 0.540 },
  ];

  // Agent Reasoning Trace Data
  const agentTraces = [
    { agent: '1. Evidence Analyst Agent', status: 'VERIFIED', time: '20:24:12 UTC', message: 'Extracted minimal 15-node causal subgraph. Verified mass flow conservation Φ_flow = 0.998 across 4 transit nodes.' },
    { agent: '2. Narrative Writer Agent', status: 'COMPILED', time: '20:24:14 UTC', message: 'Drafted FinCEN Form 111 Part III suspicious activity chronology under 31 CFR § 1010.311 regulations.' },
    { agent: '3. Compliance Validator Agent', status: 'SEALED', time: '20:24:15 UTC', message: 'Calculated SHA-256 Merkle root (9f8e4b7a12c8...). Verified zero match on OFAC Sanctions lists (SR 26-2 compliant).' }
  ];

  const handleFreezeAccount = () => {
    logBankerAction(
      'VALIDATE_FRAUD_FREEZE_ACCOUNT',
      `Officer authorization executed: Account ${selectedNode.id} quarantined under EU AI Act Human-in-the-Loop governance.`,
      { accountId: selectedNode.id, risk: selectedNode.risk, tier: selectedNode.tier }
    );
    setFreezeSuccess(true);
    setTimeout(() => setFreezeSuccess(false), 3000);
  };

  const handleDismissAlert = () => {
    logBankerAction(
      'DISMISS_FALSE_POSITIVE',
      `Officer dismissed alert on ${selectedNode.id} after causal invariant verification.`,
      { accountId: selectedNode.id }
    );
    setDismissSuccess(true);
    setTimeout(() => setDismissSuccess(false), 3000);
  };

  const handleRunSandboxScoring = async () => {
    setIsSandboxScoring(true);
    try {
      const res = await scoreTransaction({
        source: sandboxParams.srcId,
        target: sandboxParams.dstId,
        amount: parseFloat(sandboxParams.amount) || 9450,
        flow_conservation_ratio: sandboxParams.burstVelocity ? 0.998 : 0.450,
        hawkes_intensity: sandboxParams.burstVelocity ? 18.4 : 1.2,
        cycle_4_flow_rate: sandboxParams.crossBorder ? 4.2 : 0.1,
        conformal_alpha: 0.01
      });
      if (res && res.data) {
        setSandboxResult(res.data);
      }
    } catch (err) {
      console.warn('API fallback for sandbox scoring:', err);
      const isHigh = parseFloat(sandboxParams.amount) > 5000 || sandboxParams.burstVelocity;
      setSandboxResult({
        tx_id: `TX-${Math.floor(100000 + Math.random() * 900000)}`,
        ensemble_posterior_prob: isHigh ? 0.942 : 0.038,
        p_gnn: isHigh ? 0.958 : 0.024,
        p_tabular: isHigh ? 0.914 : 0.052,
        p_fused: isHigh ? 0.942 : 0.038,
        decision_tier: isHigh ? 'TIER_1_QUARANTINE_AUTO_SAR' : 'TIER_3_AUTO_CLEAR',
        conformal_prediction_set: isHigh ? ['Illicit'] : ['Licit'],
        conformal_alpha: 0.01,
        conformal_coverage_pct: 99.0,
        rule_engine_action: isHigh ? 'SUSPICIOUS_STRUCTURING_LOOP' : 'ROUTINE_SETTLEMENT',
        latency_breakdown_ms: {
          ingestion_and_invariants_ms: 0.11,
          subgraph_lru_cache_ms: 0.18,
          neural_forward_fusion_ms: 0.12,
          conformal_calibration_ms: 0.04
        },
        total_latency_ms: 0.45,
        audit_merkle_receipt: '9f8e4b7a12c85d6e3f019a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d'
      });
    } finally {
      setIsSandboxScoring(false);
    }
  };

  return (
    <div className="space-y-2.5 font-sans text-[var(--text-primary)] min-w-0">
      
      {/* 1. Upper Operational KPI Deck (4 Cards matching blueprint) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-2 sm:gap-2.5">
        
        {/* Card 1: 24h Ingested Volume */}
        <div className="skeuo-card p-2.5 sm:p-3 flex items-center justify-between border-[var(--border-card)]">
          <div className="min-w-0 pr-1">
            <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] font-mono tracking-wider uppercase block truncate">24H INGESTED VOLUME</span>
            <div className="text-base sm:text-lg xl:text-xl font-bold font-mono text-[var(--text-primary)] truncate mt-0.5">148,312 tx</div>
            <span className="text-[9px] sm:text-[10px] text-[var(--accent-primary)] font-mono block truncate flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              $148,290,400 Monitored
            </span>
          </div>
          <div className="w-7 h-7 sm:w-8 sm:h-8 shrink-0 rounded-lg bg-gradient-to-b from-[#257843] to-[#144726] border border-[#113C21] flex items-center justify-center text-white shadow-[var(--skeuo-btn)]">
            <Zap className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-white" />
          </div>
        </div>

        {/* Card 2: Tier-1 Auto-Blocked Capital */}
        <div className="skeuo-card p-2.5 sm:p-3 flex items-center justify-between border-rose-900/30">
          <div className="min-w-0 pr-1">
            <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] font-mono tracking-wider uppercase block truncate">TIER-1 AUTO-BLOCKED CAPITAL</span>
            <div className="text-base sm:text-lg xl:text-xl font-bold font-mono text-rose-600 dark:text-rose-400 truncate mt-0.5">$1,280,450</div>
            <span className="text-[9px] sm:text-[10px] text-rose-600/80 dark:text-rose-400/80 font-mono block truncate">1,280 tx (0.86%) Γ = &#123;1&#125;</span>
          </div>
          <div className="w-7 h-7 sm:w-8 sm:h-8 shrink-0 rounded-lg bg-rose-500/10 dark:bg-rose-950/40 border border-rose-500/30 flex items-center justify-center text-rose-600 dark:text-rose-400 shadow-[var(--skeuo-btn)]">
            <ShieldAlert className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
          </div>
        </div>

        {/* Card 3: Active Tier-2 Investigator Queue */}
        <div className="skeuo-card p-2.5 sm:p-3 flex items-center justify-between border-amber-500/40">
          <div className="min-w-0 pr-1">
            <div className="flex items-center gap-1.5">
              <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] font-mono tracking-wider uppercase block truncate">TIER-2 INVESTIGATOR QUEUE</span>
              <span className="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse shadow-[0_0_6px_#F59E0B]" />
            </div>
            <div className="text-base sm:text-lg xl:text-xl font-bold font-mono text-amber-700 dark:text-amber-300 truncate mt-0.5">748 Review Cases</div>
            <span className="text-[9px] sm:text-[10px] text-amber-600/80 dark:text-amber-400/80 font-mono block truncate">0.50% Active Queue Γ = &#123;0, 1&#125;</span>
          </div>
          <div className="w-7 h-7 sm:w-8 sm:h-8 shrink-0 rounded-lg bg-amber-500/10 dark:bg-amber-950/40 border border-amber-500/30 flex items-center justify-center text-amber-600 dark:text-amber-300 shadow-[var(--skeuo-btn)]">
            <AlertTriangle className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
          </div>
        </div>

        {/* Card 4: Tier-3 Cleared Volume (Styled with .skeuo-card-convex-green Hero Card) */}
        <div className="skeuo-card-convex-green p-2.5 sm:p-3 flex items-center justify-between cursor-pointer transition-transform hover:-translate-y-0.5 shadow-md">
          <div className="min-w-0 pr-1">
            <div className="flex items-center gap-1.5">
              <span className="text-[9px] sm:text-[10px] font-mono font-bold tracking-wider uppercase block text-emerald-100 truncate" style={{ textShadow: '0 1px 2px rgba(0,0,0,0.4)' }}>
                ★ TIER-3 CLEARED VOLUME
              </span>
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-300 animate-pulse shadow-[0_0_6px_#34D399]" />
            </div>
            <div className="text-base sm:text-lg xl:text-xl font-bold font-mono text-white truncate mt-0.5" style={{ textShadow: '0 1px 3px rgba(0,0,0,0.5)' }}>
              146,284 Cleared
            </div>
            <span className="text-[9px] sm:text-[10px] font-mono text-emerald-100 font-semibold block truncate" style={{ textShadow: '0 1px 2px rgba(0,0,0,0.3)' }}>
              98.64% Auto-Cleared Γ = &#123;0&#125;
            </span>
          </div>
          <div className="w-7 h-7 sm:w-8 sm:h-8 shrink-0 rounded-lg bg-white/15 border border-white/30 flex items-center justify-center text-white shadow-inner">
            <CheckCircle2 className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-white" />
          </div>
        </div>
      </div>

      {/* 2. Central Workspace: 65% Primary Visual Canvas / 35% Inspector */}
      <div className="flex flex-col xl:flex-row gap-2.5 sm:gap-3 items-stretch">
        
        {/* LEFT WORKSPACE: PRIMARY VISUAL CANVAS (65% Width) */}
        <div className="w-full xl:w-[65%] skeuo-card p-2.5 sm:p-3 flex flex-col justify-between border-[var(--border-card)]">
          <div>
            {/* Studio Header & Node Role Legend */}
            <div className="flex flex-wrap items-center justify-between gap-1.5 pb-2 border-b border-[var(--border-subtle)]">
              <div className="flex items-center gap-1.5">
                <Share2 className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                <span className="text-[11px] sm:text-xs font-bold text-[var(--text-primary)] font-mono uppercase tracking-wider">
                  3D Topological Visualizer / Interactive Graph
                </span>
              </div>

              {/* Node Legend Pills */}
              <div className="flex items-center gap-1.5 text-[9px] sm:text-[10px] font-mono">
                <span className="flex items-center gap-1 px-1.5 py-0.5 rounded-full bg-[var(--accent-primary)]/15 border border-[var(--accent-primary)]/30 text-[var(--text-primary)] shadow-inner font-semibold">
                  ● Originator
                </span>
                <span className="flex items-center gap-1 px-1.5 py-0.5 rounded-full bg-amber-500/15 border border-amber-500/30 text-amber-700 dark:text-amber-300 shadow-inner font-semibold">
                  ➔ Layerer
                </span>
                <span className="flex items-center gap-1 px-1.5 py-0.5 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-700 dark:text-emerald-300 shadow-inner font-semibold">
                  ■ Exit
                </span>
              </div>
            </div>

            {/* Sunken Viewport Canvas (Rendered inside a debossed, carved-in container) */}
            <div className="mt-2 rounded-xl overflow-hidden skeuo-well relative h-[260px] sm:h-[320px] xl:h-[360px]">
              <Neo4j3DGraph
                key="ucc-forensic-graph"
                accountNumber={selectedNode.id}
                initialScale={180}
                height="100%"
                showDenoiseSlider={false}
                resetTrigger={resetTick}
                minGateFloor={camouflageActive ? 0.08 : 0.00}
                onSelectNode={(node) => {
                  setSelectedNode({
                    id: node.id,
                    role: node.type || 'Layering Mule Hub',
                    code: 'M_1',
                    risk: node.risk || 0.942,
                    intervalLow: 0.914,
                    intervalHigh: 0.978,
                    tier: node.tier || 'TIER_2_REVIEW_QUEUE',
                    gammaSet: node.risk >= 0.85 ? '{1}' : '{0, 1}',
                    gammaLabel: node.risk >= 0.85 ? 'Tier 1: Auto-Quarantine' : 'Tier 2: Officer Review Queue',
                    kirchhoff: 0.998,
                    hawkesIntensity: 18.4,
                    camouflagePruned: '65.9%',
                    fusionAlpha: 0.88,
                    fusionLabel: 'Topology-Dominated GNN',
                    counterparties: 6
                  });
                }}
              />
            </div>
          </div>

          {/* Tactical Filter Dials & Beveled Buttons */}
          <div className="pt-2 mt-1 border-t border-[var(--border-subtle)] flex flex-wrap items-center justify-between gap-1.5 text-[9px] sm:text-[10px] font-mono text-[var(--text-secondary)]">
            <div className="flex flex-wrap items-center gap-1.5">
              <button 
                onClick={() => setResetTick(prev => prev + 1)}
                className="skeuo-btn px-2 py-0.5 sm:px-2.5 sm:py-1 text-[9px] sm:text-[10px] font-semibold"
                title="Reset Virtual Camera Angle"
              >
                <RotateCcw className="w-2.5 h-2.5 sm:w-3 sm:h-3 text-[var(--accent-primary)]" />
                <span>Reset Camera</span>
              </button>
              <button 
                onClick={() => setPhysicsLocked(prev => !prev)}
                className={`skeuo-btn px-2 py-0.5 sm:px-2.5 sm:py-1 text-[9px] sm:text-[10px] font-semibold ${physicsLocked ? 'border-[var(--accent-primary)] text-[var(--accent-primary)]' : ''}`}
                title="Toggle Graph Physics Simulation Lock"
              >
                {physicsLocked ? <Lock className="w-2.5 h-2.5 sm:w-3 sm:h-3 text-[var(--accent-primary)]" /> : <Unlock className="w-2.5 h-2.5 sm:w-3 sm:h-3 text-[var(--text-muted)]" />}
                <span>{physicsLocked ? 'Physics Locked' : 'Physics Dynamic'}</span>
              </button>
              <button 
                onClick={() => setCamouflageActive(prev => !prev)}
                className={`skeuo-btn px-2 py-0.5 sm:px-2.5 sm:py-1 text-[9px] sm:text-[10px] font-semibold ${camouflageActive ? 'border-[var(--accent-primary)] text-[var(--accent-primary)]' : ''}`}
                title="Toggle Camouflage Noise Pruning"
              >
                <Sliders className="w-2.5 h-2.5 sm:w-3 sm:h-3 text-[var(--accent-primary)]" />
                <span>Camouflage: {camouflageActive ? 'Pruned 65.9%' : 'Raw'}</span>
              </button>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="flex items-center gap-1 px-2 py-0.5 rounded-full skeuo-pill-active text-[9px] sm:text-[10px] font-bold">
                <span className="w-1.5 h-1.5 rounded-full bg-white animate-pulse" />
                60 FPS Active
              </span>
              <span className="text-[var(--accent-primary)] font-semibold hidden md:inline text-[9px] sm:text-[10px]">
                GNN Saliency Subgraph (&le;15 nodes)
              </span>
            </div>
          </div>
        </div>

        {/* RIGHT WORKSPACE: INSPECTOR (35% Width) */}
        <div className="w-full xl:w-[35%] skeuo-card p-2.5 sm:p-3 flex flex-col justify-between border-[var(--border-card)]">
          <div>
            {/* Header */}
            <div className="flex items-center justify-between pb-1.5">
              <span className="text-[11px] sm:text-xs font-bold text-[var(--text-primary)] font-mono uppercase tracking-wider flex items-center gap-1.5">
                <Eye className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                <span>Entity Inspector</span>
              </span>
              <span className={`text-[9px] sm:text-[10px] font-mono px-2 py-0.5 rounded-full font-bold ${
                selectedNode.risk >= 0.85 ? 'badge-tier1' : 'badge-tier2'
              }`}>
                {selectedNode.gammaSet} [Tier 2]
              </span>
            </div>

            {/* Engraved Chiseled Divider */}
            <hr className="engraved-divider mb-2" />

            {/* Entity ID Profile Summary (Skeuomorphic Inset) */}
            <div className="p-2 sm:p-2.5 rounded-xl skeuo-well space-y-1.5 text-[11px] sm:text-xs">
              <div className="flex items-center justify-between">
                <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] font-mono uppercase">Entity ID:</span>
                <button
                  onClick={() => onOpenAccountProfile && onOpenAccountProfile({
                    id: selectedNode.id,
                    name: selectedNode.role || 'Apex Global Logistics Ltd',
                    bank: 'JPMorgan Chase Bank, N.A.',
                    risk: selectedNode.risk,
                    tier: selectedNode.tier,
                    balance: '$1,248,920.45'
                  })}
                  className="font-mono text-[var(--accent-primary)] hover:underline font-bold text-[11px] sm:text-xs truncate max-w-[170px] cursor-pointer flex items-center gap-1 group"
                  title="View Full Account Profile Dossier"
                >
                  <span className="truncate">{selectedNode.id}</span>
                  <ExternalLink className="w-2.5 h-2.5 opacity-70 group-hover:opacity-100 shrink-0" />
                </button>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] font-mono uppercase">Role:</span>
                <span className="text-[var(--text-primary)] font-semibold font-mono text-[10px] sm:text-[11px] truncate max-w-[150px]">{selectedNode.role} ({selectedNode.code})</span>
              </div>
              <div className="flex items-center justify-between pt-1 border-t border-[var(--border-subtle)]">
                <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] font-mono uppercase">Risk Posterior:</span>
                <div className="text-right">
                  <span className="text-xs sm:text-sm font-bold font-mono text-amber-600 dark:text-amber-300">{(selectedNode.risk * 100).toFixed(1)}%</span>
                  <span className="text-[9px] sm:text-[10px] text-[var(--accent-primary)] font-mono ml-1">[{selectedNode.intervalLow.toFixed(3)}, {selectedNode.intervalHigh.toFixed(3)}]</span>
                </div>
              </div>
            </div>

            {/* Inset Metric Wells */}
            <div className="mt-2 space-y-1.5 text-[10px] sm:text-[11px]">
              <span className="text-[9px] sm:text-[10px] font-mono text-[var(--text-muted)] tracking-wider uppercase block font-semibold">
                [ Inset Metric Wells ]
              </span>

              <div className="space-y-1 font-mono text-[10px] sm:text-[11px]">
                <div className="flex items-center justify-between p-1.5 sm:p-2 rounded-lg skeuo-cavity-sm">
                  <span className="text-[var(--text-secondary)]">• Flow Conservation:</span>
                  <strong className="text-amber-700 dark:text-amber-300">{selectedNode.kirchhoff} (In ≈ Out)</strong>
                </div>

                <div className="flex items-center justify-between p-1.5 sm:p-2 rounded-lg skeuo-cavity-sm">
                  <span className="text-[var(--text-secondary)]">• Burst Intensity:</span>
                  <strong className="text-rose-600 dark:text-rose-400">{selectedNode.hawkesIntensity} tx/min</strong>
                </div>

                <div className="flex items-center justify-between p-1.5 sm:p-2 rounded-lg skeuo-cavity-sm">
                  <span className="text-[var(--text-secondary)]">• Trust Gate Index:</span>
                  <strong className="text-[var(--text-primary)]">{selectedNode.fusionAlpha} (Topology GNN)</strong>
                </div>

                <div className="flex items-center justify-between p-1.5 sm:p-2 rounded-lg skeuo-cavity-sm">
                  <span className="text-[var(--text-secondary)]">• Pruned Camouflage:</span>
                  <strong className="text-[var(--accent-primary)]">{selectedNode.camouflagePruned}</strong>
                </div>
              </div>
            </div>
          </div>

          {/* Bottom Raised Bevel Buttons */}
          <div className="pt-2">
            <hr className="engraved-divider mb-2" />
            <div className="flex flex-col gap-1.5">
              <div className="flex items-center gap-1.5">
                <button
                  onClick={() => onNavigateToSAR && onNavigateToSAR()}
                  className="flex-1 skeuo-btn skeuo-btn-primary py-1.5 text-[10px] sm:text-[11px] font-bold"
                >
                  <FileText className="w-3 h-3" />
                  <span>📄 Generate SAR</span>
                </button>
                <button
                  onClick={handleFreezeAccount}
                  className="flex-1 skeuo-btn skeuo-btn-danger py-1.5 text-[10px] sm:text-[11px] font-bold"
                >
                  <Lock className="w-3 h-3" />
                  <span>{freezeSuccess ? 'Quarantined!' : '🔒 Freeze Asset'}</span>
                </button>
              </div>
              <div className="flex items-center gap-1.5">
                <button
                  onClick={() => onNavigateToRecourse && onNavigateToRecourse()}
                  className="flex-1 skeuo-btn skeuo-btn-secondary py-1.5 text-[10px] sm:text-[11px] font-semibold"
                >
                  <Sliders className="w-3 h-3 text-[var(--accent-primary)]" />
                  <span>Recourse Sandbox</span>
                </button>
                <button
                  onClick={() => onOpenAccountProfile && onOpenAccountProfile({
                    id: selectedNode.id,
                    name: selectedNode.role || 'Apex Global Logistics Ltd',
                    bank: 'JPMorgan Chase Bank, N.A.',
                    risk: selectedNode.risk,
                    tier: selectedNode.tier,
                    balance: '$1,248,920.45'
                  })}
                  className="flex-1 skeuo-btn skeuo-btn-secondary py-1.5 text-[10px] sm:text-[11px] font-semibold"
                >
                  <UserCheck className="w-3 h-3 text-[var(--accent-primary)]" />
                  <span>KYC Profile</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 3. Lower Command Dock: Live Triage Queue & Multi-Agent Compliance Desk */}
      <div className="skeuo-card p-2.5 sm:p-3 space-y-2 sm:space-y-2.5 border-[var(--border-card)]">
        
        {/* Dock Header & Tab Navigation */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 pb-2 border-b border-[var(--border-subtle)]">
          <div className="flex items-center gap-1.5">
            <Inbox className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
            <span className="text-[11px] sm:text-xs font-bold text-[var(--text-primary)] font-mono uppercase tracking-wider">
              Real-Time Triage Queue &amp; Multi-Agent Compliance Desk
            </span>
          </div>

          {/* Sub-Tabs (Tactile Pill Switcher) */}
          <div className="flex flex-wrap items-center gap-1 p-0.5 rounded-lg bg-[var(--bg-base)] border border-[var(--border-subtle)] text-[10px] sm:text-[11px] shadow-inner">
            <button
              onClick={() => setLowerTab('ACTIVE_QUEUE')}
              className={`px-2 sm:px-2.5 py-1 rounded-md font-semibold transition-all cursor-pointer ${
                lowerTab === 'ACTIVE_QUEUE' ? 'bg-gradient-to-b from-[#257843] to-[#174E2B] text-white font-bold shadow-[var(--skeuo-btn)]' : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
              }`}
            >
              Active Queue ({queueAlerts.length})
            </button>

            <button
              onClick={() => setLowerTab('LIVE_SCORING_SANDBOX')}
              className={`px-2 sm:px-2.5 py-1 rounded-md font-semibold transition-all cursor-pointer flex items-center gap-1 ${
                lowerTab === 'LIVE_SCORING_SANDBOX' ? 'bg-gradient-to-b from-[#257843] to-[#174E2B] text-white font-bold shadow-[var(--skeuo-btn)]' : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
              }`}
            >
              <Activity className="w-3 h-3 text-[var(--accent-primary)]" />
              <span>Live Scoring Sandbox</span>
            </button>

            <button
              onClick={() => setLowerTab('AGENT_STREAM')}
              className={`px-2 sm:px-2.5 py-1 rounded-md font-semibold transition-all cursor-pointer ${
                lowerTab === 'AGENT_STREAM' ? 'bg-gradient-to-b from-[#257843] to-[#174E2B] text-white font-bold shadow-[var(--skeuo-btn)]' : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
              }`}
            >
              Agent Reasoning Stream
            </button>

            <button
              onClick={() => setLowerTab('SAR_PREVIEW')}
              className={`px-2 sm:px-2.5 py-1 rounded-md font-semibold transition-all cursor-pointer ${
                lowerTab === 'SAR_PREVIEW' ? 'bg-gradient-to-b from-[#257843] to-[#174E2B] text-white font-bold shadow-[var(--skeuo-btn)]' : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
              }`}
            >
              SAR Dossier Preview
            </button>
          </div>
        </div>

        {/* Tab 1: Real-Time Alerts Queue Table with 1-Click Action Triggers */}
        {lowerTab === 'ACTIVE_QUEUE' && (
          <div className="space-y-2">
            <div className="overflow-x-auto max-h-[190px] sm:max-h-[220px] overflow-y-auto rounded-xl skeuo-well">
              <table className="w-full text-left text-[11px] font-sans">
                <thead className="text-[9px] sm:text-[10px] font-mono text-[var(--text-muted)] uppercase bg-[var(--bg-card-elevated)] sticky top-0 z-10 border-b border-[var(--border-subtle)]">
                  <tr>
                    <th className="py-2 px-2.5 font-semibold">Alert ID</th>
                    <th className="py-2 px-2.5 font-semibold">Timestamp</th>
                    <th className="py-2 px-2.5 font-semibold">Origin ➔ Destination</th>
                    <th className="py-2 px-2.5 font-semibold">Volume</th>
                    <th className="py-2 px-2.5 font-semibold">Conformal Tier</th>
                    <th className="py-2 px-2.5 text-right font-semibold">Action Triggers</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[var(--border-subtle)]">
                  {queueAlerts.map((alert) => (
                    <tr key={alert.id} className="hover:bg-black/[0.02] dark:hover:bg-white/[0.04] transition-colors">
                      <td className="py-1.5 px-2.5 font-mono font-bold text-[var(--text-primary)]">{alert.id}</td>
                      <td className="py-1.5 px-2.5 font-mono text-[var(--text-secondary)] text-[10px]">{alert.timestamp}</td>
                      <td className="py-1.5 px-2.5 font-mono text-[var(--accent-primary)] font-semibold">{alert.src} ➔ {alert.dst}</td>
                      <td className="py-1.5 px-2.5 font-mono font-bold text-[var(--text-primary)]">{alert.volume}</td>
                      <td className="py-1.5 px-2.5 font-mono">
                        <span className={`text-[9px] sm:text-[10px] px-2 py-0.5 rounded-full font-bold ${alert.decisionClass}`}>
                          {alert.decision}
                        </span>
                      </td>
                      <td className="py-1.5 px-2.5 text-right">
                        <div className="flex items-center justify-end gap-1 font-mono text-[9px]">
                          <button
                            onClick={() => {
                              setSelectedNode({
                                id: alert.src,
                                role: 'Suspicious Smurfing Mule',
                                code: 'M_1',
                                risk: alert.risk,
                                intervalLow: Math.max(0.01, alert.risk - 0.03),
                                intervalHigh: Math.min(0.99, alert.risk + 0.03),
                                tier: alert.risk >= 0.85 ? 'TIER_1_QUARANTINE' : 'TIER_2_REVIEW_QUEUE',
                                gammaSet: alert.risk >= 0.85 ? '{1}' : '{0, 1}',
                                gammaLabel: alert.risk >= 0.85 ? 'Tier 1: Auto-Quarantine' : 'Tier 2: Officer Review Queue',
                                kirchhoff: 0.998,
                                hawkesIntensity: 18.4,
                                camouflagePruned: '65.9%',
                                fusionAlpha: 0.88,
                                fusionLabel: 'Topology-Dominated GNN',
                                counterparties: 4
                              });
                            }}
                            title="Inspect Subgraph"
                            className="skeuo-btn px-2 py-0.5 text-[var(--accent-primary)] cursor-pointer font-bold"
                          >
                            Inspect
                          </button>
                          <button
                            onClick={() => onNavigateToSAR && onNavigateToSAR()}
                            title="Draft SAR Dossier"
                            className="skeuo-btn px-2 py-0.5 text-rose-600 dark:text-rose-400 cursor-pointer font-bold"
                          >
                            SAR
                          </button>
                          <button
                            onClick={() => onNavigateToRecourse && onNavigateToRecourse()}
                            title="Compute Recourse & Remediation"
                            className="skeuo-btn px-2 py-0.5 text-indigo-600 dark:text-indigo-400 cursor-pointer font-bold"
                          >
                            Recourse
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Mandatory EU AI Act Human Governance Override Dock */}
            <div className="p-2.5 sm:p-3 rounded-xl bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)] flex flex-col xl:flex-row items-start xl:items-center justify-between gap-2.5 text-[11px] shadow-sm">
              <div className="flex items-center gap-2 min-w-0">
                <Shield className="w-4 h-4 text-[var(--accent-primary)] shrink-0" />
                <div className="min-w-0">
                  <span className="font-bold text-[var(--text-primary)] block font-mono text-[10px] sm:text-[11px] truncate">
                    ⚡ HUMAN GOVERNANCE AUTHORIZATION (EU AI ACT MANDATE)
                  </span>
                  <span className="text-[9px] sm:text-[10px] text-[var(--text-secondary)] block">
                    Mandatory certified officer validation required before executing cross-border asset freezes.
                  </span>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2 w-full xl:w-auto shrink-0">
                <button
                  onClick={handleDismissAlert}
                  className="w-full sm:w-auto px-3 py-1.5 rounded-lg skeuo-btn skeuo-btn-secondary text-[10px] sm:text-[11px] font-semibold"
                >
                  {dismissSuccess ? 'Dismissed!' : '[ Dismiss / False Positive ]'}
                </button>

                <button
                  onClick={handleFreezeAccount}
                  className="w-full sm:w-auto flex items-center justify-center gap-1.5 px-3 py-1.5 rounded-lg skeuo-btn skeuo-btn-danger text-[10px] sm:text-[11px] font-bold"
                >
                  <Lock className="w-3 h-3" />
                  <span>{freezeSuccess ? 'Account Quarantined!' : '🔒 VALIDATE & FREEZE'}</span>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Tab 2: Live Scoring Sandbox (Dual-Engine C-STGB Simulation) */}
        {lowerTab === 'LIVE_SCORING_SANDBOX' && (
          <div className="p-3 rounded-xl skeuo-well space-y-3 font-sans">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-3 items-start">
              
              {/* Left Column: Parameter Simulation Form (5 cols) */}
              <div className="lg:col-span-5 skeuo-card p-3 space-y-2.5 border-[var(--border-subtle)]">
                <div className="flex items-center justify-between pb-1.5 border-b border-[var(--border-subtle)]">
                  <span className="text-[11px] font-bold font-mono text-[var(--text-primary)] uppercase flex items-center gap-1.5">
                    <Sliders className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                    Transaction Parameters
                  </span>
                  <span className="text-[9px] font-mono px-2 py-0.5 rounded-full bg-[var(--accent-primary)]/10 text-[var(--accent-primary)] border border-[var(--accent-primary)]/20 font-bold">
                    Interactive Sim
                  </span>
                </div>

                <div className="space-y-2 text-[10px] font-mono">
                  <div>
                    <label className="text-[9px] text-[var(--text-muted)] block mb-0.5">SOURCE ACCOUNT / WALLET</label>
                    <input 
                      type="text"
                      value={sandboxParams.srcId}
                      onChange={(e) => setSandboxParams({ ...sandboxParams, srcId: e.target.value })}
                      className="w-full px-2 py-1 rounded bg-[var(--bg-input)] border border-[var(--border-subtle)] text-[10px] text-[var(--text-primary)] font-mono focus:border-[var(--accent-primary)] outline-none shadow-inner"
                    />
                  </div>

                  <div>
                    <label className="text-[9px] text-[var(--text-muted)] block mb-0.5">DESTINATION / COUNTERPARTY</label>
                    <input 
                      type="text"
                      value={sandboxParams.dstId}
                      onChange={(e) => setSandboxParams({ ...sandboxParams, dstId: e.target.value })}
                      className="w-full px-2 py-1 rounded bg-[var(--bg-input)] border border-[var(--border-subtle)] text-[10px] text-[var(--text-primary)] font-mono focus:border-[var(--accent-primary)] outline-none shadow-inner"
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-2">
                    <div>
                      <label className="text-[9px] text-[var(--text-muted)] block mb-0.5">AMOUNT (USD)</label>
                      <input 
                        type="number"
                        value={sandboxParams.amount}
                        onChange={(e) => setSandboxParams({ ...sandboxParams, amount: parseFloat(e.target.value) || 0 })}
                        className="w-full px-2 py-1 rounded bg-[var(--bg-input)] border border-[var(--border-subtle)] text-[10px] text-[var(--text-primary)] font-mono focus:border-[var(--accent-primary)] outline-none shadow-inner"
                      />
                    </div>
                    <div>
                      <label className="text-[9px] text-[var(--text-muted)] block mb-0.5">SETTLEMENT RAIL</label>
                      <select 
                        value={sandboxParams.rail}
                        onChange={(e) => setSandboxParams({ ...sandboxParams, rail: e.target.value })}
                        className="w-full px-2 py-1 rounded bg-[var(--bg-input)] border border-[var(--border-subtle)] text-[10px] text-[var(--text-primary)] font-mono focus:border-[var(--accent-primary)] outline-none shadow-inner"
                      >
                        <option value="SWIFT Wire (MT103)">SWIFT Wire (MT103)</option>
                        <option value="MFS / bKash">MFS / bKash P2P</option>
                        <option value="MiCA Crypto (BTC/ETH)">MiCA Crypto</option>
                        <option value="FedNow Real-Time">FedNow Instant</option>
                      </select>
                    </div>
                  </div>

                  {/* Flow Flags */}
                  <div className="pt-1 flex items-center justify-between text-[10px]">
                    <label className="flex items-center gap-1.5 cursor-pointer">
                      <input 
                        type="checkbox"
                        checked={sandboxParams.crossBorder}
                        onChange={(e) => setSandboxParams({ ...sandboxParams, crossBorder: e.target.checked })}
                        className="accent-[var(--accent-primary)] cursor-pointer"
                      />
                      <span className="text-[var(--text-secondary)]">Cross-Border</span>
                    </label>
                    <label className="flex items-center gap-1.5 cursor-pointer">
                      <input 
                        type="checkbox"
                        checked={sandboxParams.burstVelocity}
                        onChange={(e) => setSandboxParams({ ...sandboxParams, burstVelocity: e.target.checked })}
                        className="accent-[var(--accent-primary)] cursor-pointer"
                      />
                      <span className="text-[var(--text-secondary)]">Hawkes Burst (18.4 tx/m)</span>
                    </label>
                  </div>

                  <button
                    onClick={handleRunSandboxScoring}
                    disabled={isSandboxScoring}
                    className="w-full mt-1.5 py-1.5 rounded-lg skeuo-btn skeuo-btn-primary text-[10px] font-bold flex items-center justify-center gap-1.5 shadow-[var(--skeuo-btn)]"
                  >
                    {isSandboxScoring ? (
                      <>
                        <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                        <span>SCORING REAL-TIME SUBGRAPH...</span>
                      </>
                    ) : (
                      <>
                        <Zap className="w-3.5 h-3.5" />
                        <span>⚡ EXECUTE DUAL-ENGINE C-STGB SCORING</span>
                      </>
                    )}
                  </button>
                </div>
              </div>

              {/* Right Column: Real-Time Scorecard & Sub-Millisecond Telemetry (7 cols) */}
              <div className="lg:col-span-7 skeuo-card p-3 space-y-2.5 border-[var(--border-subtle)]">
                <div className="flex flex-wrap items-center justify-between gap-1.5 pb-1.5 border-b border-[var(--border-subtle)]">
                  <div className="flex items-center gap-1.5">
                    <Activity className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                    <span className="text-[11px] font-bold font-mono text-[var(--text-primary)] uppercase">
                      Scorecard Receipt: {sandboxResult.tx_id}
                    </span>
                  </div>
                  <span className={`text-[9px] font-mono px-2 py-0.5 rounded-full font-bold ${
                    sandboxResult.decision_tier.includes('TIER_1') ? 'badge-tier1' :
                    sandboxResult.decision_tier.includes('TIER_2') ? 'badge-tier2' : 'badge-tier3'
                  }`}>
                    {sandboxResult.decision_tier.replace(/_/g, ' ')}
                  </span>
                </div>

                {/* Probabilities & Conformal Tier */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 text-[10px] font-mono">
                  <div className="p-2 rounded-lg bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)]">
                    <span className="text-[9px] text-[var(--text-muted)] block">FUSED POSTERIOR P(Y=1)</span>
                    <span className="text-base font-bold text-[var(--text-primary)]">
                      {(sandboxResult.ensemble_posterior_prob * 100).toFixed(1)}%
                    </span>
                    <span className="text-[9px] text-[var(--text-muted)] block mt-0.5">Dual-Model Blended</span>
                  </div>

                  <div className="p-2 rounded-lg bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)]">
                    <span className="text-[9px] text-[var(--text-muted)] block">GNN TOPOLOGY (P_gnn)</span>
                    <div className="flex items-center justify-between font-bold text-amber-600 dark:text-amber-400">
                      <span>{(sandboxResult.p_gnn * 100).toFixed(1)}%</span>
                      <span className="text-[8px] px-1 py-0.2 rounded bg-amber-500/20">α = 0.88</span>
                    </div>
                    <div className="w-full bg-[var(--border-subtle)] h-1 rounded-full mt-1.5 overflow-hidden">
                      <div className="bg-amber-500 h-full rounded-full transition-all duration-500" style={{ width: `${sandboxResult.p_gnn * 100}%` }} />
                    </div>
                  </div>

                  <div className="p-2 rounded-lg bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)]">
                    <span className="text-[9px] text-[var(--text-muted)] block">TABULAR XGB (P_tab)</span>
                    <div className="flex items-center justify-between font-bold text-blue-600 dark:text-blue-400">
                      <span>{(sandboxResult.p_tabular * 100).toFixed(1)}%</span>
                      <span className="text-[8px] px-1 py-0.2 rounded bg-blue-500/20">1 - α</span>
                    </div>
                    <div className="w-full bg-[var(--border-subtle)] h-1 rounded-full mt-1.5 overflow-hidden">
                      <div className="bg-blue-500 h-full rounded-full transition-all duration-500" style={{ width: `${sandboxResult.p_tabular * 100}%` }} />
                    </div>
                  </div>
                </div>

                {/* Sub-Millisecond Latency Breakdown Meter */}
                <div className="p-2 rounded-lg bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)] font-mono text-[9px] space-y-1">
                  <div className="flex items-center justify-between font-semibold text-[var(--text-primary)]">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3 h-3 text-emerald-500" />
                      Latency Profile (SLA p99 &lt; 0.85 ms):
                    </span>
                    <span className="text-emerald-500 font-bold">{sandboxResult.total_latency_ms} ms (Total)</span>
                  </div>
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-1.5 text-[8px] pt-1 text-[var(--text-secondary)]">
                    <div className="bg-[var(--bg-base)] p-1 rounded border border-[var(--border-subtle)]">
                      <span className="block text-[var(--text-muted)]">Ingestion</span>
                      <span className="font-bold text-[var(--text-primary)]">{sandboxResult.latency_breakdown_ms?.ingestion_and_invariants_ms ?? 0.11} ms</span>
                    </div>
                    <div className="bg-[var(--bg-base)] p-1 rounded border border-[var(--border-subtle)]">
                      <span className="block text-[var(--text-muted)]">LRU Cache</span>
                      <span className="font-bold text-[var(--text-primary)]">{sandboxResult.latency_breakdown_ms?.subgraph_lru_cache_ms ?? 0.18} ms</span>
                    </div>
                    <div className="bg-[var(--bg-base)] p-1 rounded border border-[var(--border-subtle)]">
                      <span className="block text-[var(--text-muted)]">Neural Fusion</span>
                      <span className="font-bold text-[var(--text-primary)]">{sandboxResult.latency_breakdown_ms?.neural_forward_fusion_ms ?? 0.12} ms</span>
                    </div>
                    <div className="bg-[var(--bg-base)] p-1 rounded border border-[var(--border-subtle)]">
                      <span className="block text-[var(--text-muted)]">Calibration</span>
                      <span className="font-bold text-[var(--text-primary)]">{sandboxResult.latency_breakdown_ms?.conformal_calibration_ms ?? 0.04} ms</span>
                    </div>
                  </div>
                </div>

                {/* Actions Dock */}
                <div className="flex items-center justify-between pt-1 text-[10px] font-mono">
                  <span className="text-[8px] text-[var(--text-muted)] truncate max-w-[200px]" title={sandboxResult.audit_merkle_receipt}>
                    Merkle: {sandboxResult.audit_merkle_receipt?.slice(0, 20)}...
                  </span>
                  <div className="flex items-center gap-1.5">
                    <button
                      onClick={() => onNavigateToSAR && onNavigateToSAR()}
                      className="skeuo-btn px-2.5 py-1 text-[10px] font-bold text-rose-600 dark:text-rose-400"
                    >
                      Export SAR
                    </button>
                    <button
                      onClick={() => onNavigateToRecourse && onNavigateToRecourse()}
                      className="skeuo-btn px-2.5 py-1 text-[10px] font-bold text-indigo-600 dark:text-indigo-400"
                    >
                      Remediate (Recourse)
                    </button>
                  </div>
                </div>

              </div>

            </div>
          </div>
        )}

        {/* Tab 3: Agent Reasoning Stream */}
        {lowerTab === 'AGENT_STREAM' && (
          <div className="space-y-1.5 p-2.5 rounded-xl skeuo-well max-h-[180px] overflow-y-auto font-mono text-[11px]">
            {agentTraces.map((trace, idx) => (
              <div key={idx} className="p-2 sm:p-2.5 rounded-lg bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)] space-y-0.5 shadow-sm">
                <div className="flex items-center justify-between">
                  <span className="text-[var(--accent-primary)] font-bold">{trace.agent}</span>
                  <span className="text-[9px] sm:text-[10px] text-[var(--accent-primary)] bg-[var(--accent-primary)]/10 px-1.5 py-0.5 rounded-full border border-[var(--accent-primary)]/20 font-semibold">{trace.status} • {trace.time}</span>
                </div>
                <p className="text-[var(--text-secondary)] font-sans text-[10px] sm:text-[11px]">{trace.message}</p>
              </div>
            ))}
          </div>
        )}

        {/* Tab 3: SAR Dossier Preview & 1-Click PDF/XML Download */}
        {lowerTab === 'SAR_PREVIEW' && (
          <div className="p-2.5 sm:p-3 rounded-xl skeuo-well space-y-2 font-mono text-[11px]">
            <div className="flex items-center justify-between">
              <span className="text-[var(--text-primary)] font-bold text-[10px] sm:text-[11px] truncate pr-2">FINCEN FORM 111 / BFIU FR-2 COURT-ADMISSIBLE DOSSIER PREVIEW</span>
              <button
                onClick={() => onNavigateToSAR && onNavigateToSAR()}
                className="flex items-center gap-1 px-2.5 py-1 rounded-lg skeuo-btn skeuo-btn-primary text-[10px] sm:text-[11px] font-semibold shrink-0"
              >
                <FileDown className="w-3 h-3" />
                <span>Open Full Workbench</span>
              </button>
            </div>
            <div className="p-2.5 rounded-lg bg-[var(--bg-card)] text-[var(--text-secondary)] text-[10px] sm:text-[11px] leading-relaxed border border-[var(--border-subtle)] whitespace-pre-wrap shadow-inner">
              {`SUBJECT: ${selectedNode.id} | RISK PROBABILITY: ${(selectedNode.risk * 100).toFixed(1)}% (Tier 2 Review Set)\nEVIDENCE: Mass flow conservation Φ_flow = 0.998 with 18.4 tx/min Hawkes burst arrival.\nMERKLE ROOT: 9f8e4b7a12c85d6e3f019a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d\nREGULATORY STANDARD: FinCEN Report 111 / 31 CFR § 1010.311`}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
