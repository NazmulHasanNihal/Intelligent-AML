import React, { useState, useMemo, Suspense } from 'react';
import {
  ShieldAlert,
  Box,
  Layers,
  Sliders,
  Search,
  Filter,
  ArrowRight,
  Clock,
  Sparkles,
  Download,
  CheckCircle2,
  AlertTriangle,
  Lock,
  Mail,
  FileText,
  ChevronDown,
  ChevronUp,
  SlidersHorizontal,
  Eye,
  EyeOff,
  ShieldCheck,
  Zap,
  Info,
  Maximize2,
  Minimize2,
  Route,
  Activity,
  Repeat,
  RotateCcw,
  SlidersVertical,
  PanelLeftClose,
  PanelLeftOpen
} from 'lucide-react';
import { useAppStore } from '../../lib/store';
import { useAuth } from '../../context/AuthContext';
import { Cytoscape2DGraph } from './Cytoscape2DGraph';
import { CustomerNoticeModal } from '../../components/CustomerNoticeModal';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';

// Lazy-load WebGL 3D engine to protect initial load performance
const Neo4j3DGraph = React.lazy(() => import('../../components/Neo4j3DGraph'));

export const NetworkView = () => {
  const { currentBanker, logBankerAction } = useAuth();
  const {
    cases,
    selectedCaseId,
    selectCase,
    navigate,
    timelineStep,
    setTimelineStep,
    camouflageDelta,
    setCamouflageDelta,
    camouflageGatingEnabled,
    setCamouflageGatingEnabled,
    selectedGraphNode,
    setSelectedGraphNode,
    entities360,
    logAuditAction,
    addToast
  } = useAppStore();

  // Layout & View Mode States
  const [layoutMode, setLayoutMode] = useState('sugiyama'); // 'sugiyama' | 'orbital' | 'cose' | 'circle'
  const [engineMode, setEngineMode] = useState('2D'); // '2D' | '3D'
  const [tierFilter, setTierFilter] = useState('ALL'); // 'ALL' | 'Tier 1 Hold' | 'Tier 2 Review'
  const [searchQuery, setSearchQuery] = useState('');
  const [isChronicleOpen, setIsChronicleOpen] = useState(false); // Collapsed by default for zero vertical scrolling
  const [isNoticeModalOpen, setIsNoticeModalOpen] = useState(false);
  const [isQueueCollapsed, setIsQueueCollapsed] = useState(false); // Collapsible triage queue for extra wide canvas
  const [focusMode, setFocusMode] = useState(false); // Zen Mode: full-width canvas
  const [inspectorTab, setInspectorTab] = useState('evidence'); // 'evidence' | 'recourse'

  // Counterfactual Recourse Simulation State
  const [simulatedDwellHours, setSimulatedDwellHours] = useState(0.35); // 21 mins
  const [simulatedAmount, setSimulatedAmount] = useState(9450); // near-CTR $9,450

  // Selected Case resolution
  const activeCase = useMemo(() => {
    return cases.find(c => c.id === selectedCaseId) || cases[0];
  }, [cases, selectedCaseId]);

  // Inspected Entity resolution
  const activeEntityAccount = selectedGraphNode?.id || activeCase?.subjectAccount || 'BD22-EBLB-4829-1092-8823';
  const entityDossier = entities360[activeEntityAccount] || entities360['BD22-EBLB-4829-1092-8823'];

  // Filtered Cases for Triage Queue
  const filteredCases = useMemo(() => {
    return (cases || []).filter(c => {
      const matchTier = tierFilter === 'ALL' || c.tier === tierFilter;
      const q = searchQuery.toLowerCase().trim();
      const matchSearch = !q ||
        c.title.toLowerCase().includes(q) ||
        c.id.toLowerCase().includes(q) ||
        c.subjectEntity.toLowerCase().includes(q) ||
        c.subjectAccount.toLowerCase().includes(q);
      return matchTier && matchSearch;
    });
  }, [cases, tierFilter, searchQuery]);

  // Multi-Hop Forensic Chronicle Data
  const CHRONICLE_HOPS = [
    {
      step: 0,
      timestamp: '08:00 UTC',
      phase: 'Quiescent Baseline',
      origin: 'All Corridors',
      beneficiary: 'Clearing Gateway',
      rail: 'RTGS / ACH',
      amount: '$0.00',
      dwell: 'Baseline',
      invariant: 'Quiescent Baseline Verified',
      status: 'CLEARED'
    },
    {
      step: 1,
      timestamp: '08:14 UTC',
      phase: 'MFS Smurfing Fan-In',
      origin: 'Rafiqul Islam (MFS)',
      beneficiary: 'Tanvir Rahman (Conduit)',
      rail: 'bKash MFS',
      amount: '$4,800.00',
      dwell: '42s',
      invariant: 'Sub-CTR Structuring (< ৳1M)',
      status: 'FLAGGED'
    },
    {
      step: 2,
      timestamp: '08:16 UTC',
      phase: 'RTGS Layering Injection',
      origin: 'Meghna Industrial (Hub)',
      beneficiary: 'Tanvir Rahman (Conduit)',
      rail: 'RTGS (BD Bank)',
      amount: '$47,600.00',
      dwell: '120s',
      invariant: 'Velocity Anomaly (9.1 tx/min)',
      status: 'VIOLATION'
    },
    {
      step: 3,
      timestamp: '08:22 UTC',
      phase: 'SWIFT Offshore Wire',
      origin: 'Tanvir Rahman (Conduit)',
      beneficiary: 'Gulf Star (Dubai)',
      rail: 'SWIFT MT103',
      amount: '$47,600.00',
      dwell: '6.2m',
      invariant: 'Offshore Secrecy Shell (JAFZA)',
      status: 'VIOLATION'
    },
    {
      step: 4,
      timestamp: '08:35 UTC',
      phase: 'Cycle-3 Trade Wash Return',
      origin: 'Gulf Star (Dubai)',
      beneficiary: 'Meghna Industrial (Hub)',
      rail: 'SWIFT MT700 (LC)',
      amount: '$47,600.00',
      dwell: '13.0m',
      invariant: '100% Closed Wash Loop',
      status: 'VIOLATION'
    }
  ];

  // Dynamic Counterfactual Evaluation
  const counterfactualOutcome = useMemo(() => {
    if (simulatedDwellHours >= 24 && simulatedAmount <= 5000) {
      return {
        tier: 'Tier 3 Clear',
        conformalSet: 'Γ = {0}',
        badgeVariant: 'cleared',
        statusText: 'Statutory Hold Released',
        explanation: 'Normal commercial billing dwell (>24h) and micro-ticket size eliminate structuring and smurfing invariants.'
      };
    } else if (simulatedDwellHours >= 6 || simulatedAmount <= 10000) {
      return {
        tier: 'Tier 2 Review',
        conformalSet: 'Γ = {0, 1}',
        badgeVariant: 'review',
        statusText: 'Enhanced Due Diligence (EDD) Required',
        explanation: 'Dwell time mitigates automated hold, but cross-border offshore destination requires officer check.'
      };
    } else {
      return {
        tier: 'Tier 1 Hold',
        conformalSet: 'Γ = {1}',
        badgeVariant: 'critical',
        statusText: 'Administrative Hold Enforced',
        explanation: 'Rapid pass-through (<120s) and near-CTR allocation trigger Section 25 of MLPA 2012 / FinCEN invariants.'
      };
    }
  }, [simulatedDwellHours, simulatedAmount]);

  // Handler: Export Forensic Cryptographic Snapshot (FRE 902(11) Proof)
  const handleExportSnapshot = () => {
    const merkleRoot = `MRK-${Date.now().toString(16).toUpperCase()}-FRE902`;
    logAuditAction(
      'FORENSIC_SNAPSHOT_EXPORTED',
      `Exported Rule 902(11) cryptographic forensic proof for Case ${activeCase.id}. Merkle: ${merkleRoot}`,
      activeEntityAccount,
      currentBanker?.name || 'Compliance Officer'
    );
    addToast('Forensic Snapshot Certified', `FRE 902(11) seal ${merkleRoot} generated.`, 'success');
  };

  // Handler: Core Banking Administrative Debit Freeze
  const handleFreezeDebit = () => {
    logBankerAction(
      'ADMINISTRATIVE_HOLD_PLACED',
      `Placed administrative debit freeze on account ${activeEntityAccount} under MLPA 2012 §15.`,
      activeEntityAccount,
      'Severe invariant violation / 100% circular wash loop'
    );
    logAuditAction(
      'CORE_BANKING_DEBIT_FREEZE',
      `Direct core banking administrative hold applied to ${activeEntityAccount}. Dual sign-off required to lift.`,
      activeEntityAccount,
      currentBanker?.name || 'Authorized Officer'
    );
    addToast('Administrative Hold Enforced', `Core banking freeze active on ${activeEntityAccount}.`, 'critical');
  };

  // Handler: Draft Regulatory SAR
  const handleDraftSAR = () => {
    logBankerAction(
      'SAR_DRAFT_INITIATED',
      `Initiated FinCEN Form 111 / BFIU STR-1 filing draft for Case ${activeCase.id}`,
      activeEntityAccount,
      'FATF Typology #4 match'
    );
    navigate('filings', { caseId: activeCase.id });
    addToast('SAR Draft Opened', `Navigating to Filings Vault for ${activeCase.id}.`, 'info');
  };

  // Compute responsive grid layout based on view modes
  const centerColSpan = focusMode
    ? 'lg:col-span-12'
    : isQueueCollapsed
      ? 'lg:col-span-9'
      : 'lg:col-span-6 xl:col-span-7';

  return (
    <div className="space-y-2.5">
      {/* Sleek, Low-Noise Hub Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 p-2.5 px-3.5 rounded-lg bg-surface border border-border shadow-xs">
        <div className="flex items-center gap-2.5">
          <div className="p-1.5 rounded-md bg-accent/10 text-accent">
            <Activity className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-sm font-bold text-text tracking-tight">Forensic Cash Flow Network Studio</h1>
              <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-surfaceRaised text-text-muted border border-border/60">
                Rule 902(11) Certified
              </span>
            </div>
            <p className="text-[11px] text-text-muted">
              Causal flow preservation (Placement ➔ Layering ➔ Integration), noise pruning, and counterfactual recourse.
            </p>
          </div>
        </div>

        {/* Header Right: Focus Mode & Engine Mode */}
        <div className="flex items-center gap-2">
          {/* Zen / Focus Mode Toggle */}
          <button
            onClick={() => setFocusMode(!focusMode)}
            className={`px-2.5 py-1 rounded border text-xs font-mono transition-colors cursor-pointer flex items-center gap-1.5 shadow-xs ${
              focusMode
                ? 'bg-accent text-white border-accent font-semibold'
                : 'bg-surfaceRaised border-border hover:border-accent text-text'
            }`}
            title={focusMode ? 'Exit Focus Mode' : 'Focus Mode (Maximize Canvas Width)'}
          >
            {focusMode ? <Minimize2 className="w-3.5 h-3.5" /> : <Maximize2 className="w-3.5 h-3.5" />}
            <span>{focusMode ? 'Exit Focus' : 'Focus Mode'}</span>
          </button>

          {/* Dual Engine Switcher */}
          <div className="flex items-center p-0.5 bg-bg rounded border border-border font-mono text-[11px]">
            <button
              onClick={() => setEngineMode('2D')}
              className={`px-2.5 py-1 rounded transition-colors cursor-pointer ${
                engineMode === '2D' ? 'bg-surface font-semibold text-text shadow-xs' : 'text-text-muted hover:text-text'
              }`}
            >
              2D Cytoscape
            </button>
            <button
              onClick={() => setEngineMode('3D')}
              className={`px-2 py-1 rounded transition-colors cursor-pointer flex items-center gap-1 ${
                engineMode === '3D' ? 'bg-surface font-semibold text-text shadow-xs' : 'text-text-muted hover:text-text'
              }`}
            >
              <Box className="w-3 h-3" />
              <span>3D WebGL</span>
            </button>
          </div>
        </div>
      </div>

      {/* Main Layout Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-3 items-start">

        {/* ========================================================================= */}
        {/* PANEL 1: TRIAGE QUEUE (Left Column, collapsible for extra wide view)      */}
        {/* ========================================================================= */}
        {!focusMode && !isQueueCollapsed && (
          <div className="lg:col-span-3 xl:col-span-2.5 bg-surface border border-border rounded-lg p-2.5 space-y-2.5 flex flex-col shadow-xs">
            {/* Triage Queue Header */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-1.5">
                <span className="text-xs font-bold uppercase tracking-wider text-text">Triage Cases</span>
                <span className="text-[10px] font-mono text-text-muted bg-bg px-1.5 py-0.2 rounded border border-border">
                  {filteredCases.length}
                </span>
              </div>
              <button
                onClick={() => setIsQueueCollapsed(true)}
                className="p-1 rounded text-text-muted hover:text-text hover:bg-surfaceRaised cursor-pointer transition-colors"
                title="Collapse Queue for Wide Canvas"
              >
                <PanelLeftClose className="w-3.5 h-3.5" />
              </button>
            </div>

            {/* Compact Search & Filter */}
            <div className="space-y-1.5">
              <div className="relative">
                <Search className="w-3 h-3 text-text-muted absolute left-2 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="Filter cases..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-6 pr-2 py-1 rounded bg-bg border border-border text-[11px] text-text placeholder-text-muted focus:outline-hidden focus:border-accent font-mono"
                />
              </div>

              {/* Tier Filter Pills */}
              <div className="flex items-center gap-1 p-0.5 bg-bg rounded border border-border text-[10px] font-mono">
                {['ALL', 'Tier 1 Hold', 'Tier 2 Review'].map((tier) => (
                  <button
                    key={tier}
                    onClick={() => setTierFilter(tier)}
                    className={`flex-1 py-0.5 rounded text-center transition-colors cursor-pointer truncate ${
                      tierFilter === tier
                        ? tier === 'Tier 1 Hold'
                          ? 'bg-critical text-white font-bold'
                          : tier === 'Tier 2 Review'
                            ? 'bg-review text-white font-bold'
                            : 'bg-surface font-bold text-text shadow-xs'
                        : 'text-text-muted hover:text-text'
                    }`}
                  >
                    {tier === 'ALL' ? 'All' : tier === 'Tier 1 Hold' ? 'Hold' : 'Review'}
                  </button>
                ))}
              </div>
            </div>

            {/* Case Cards List (Clean, Compact) */}
            <div className="space-y-1.5 max-h-[460px] overflow-y-auto pr-0.5">
              {filteredCases.length === 0 ? (
                <div className="p-3 text-center text-xs text-text-muted border border-dashed border-border rounded">
                  No cases found.
                </div>
              ) : (
                filteredCases.map((c) => {
                  const isSelected = c.id === activeCase.id;
                  return (
                    <div
                      key={c.id}
                      onClick={() => selectCase(c.id)}
                      className={`p-2 rounded-md border text-xs cursor-pointer transition-all ${
                        isSelected
                          ? 'bg-accent/5 border-accent shadow-xs ring-1 ring-accent/30'
                          : 'bg-bg/50 border-border hover:border-borderHover hover:bg-bg'
                      }`}
                    >
                      <div className="flex items-center justify-between gap-1 mb-0.5">
                        <span className="font-mono font-bold text-text text-[11px] truncate">
                          {c.id}
                        </span>
                        <span className={`px-1.5 py-0.2 rounded text-[9px] font-mono font-semibold ${
                          c.tier === 'Tier 1 Hold' ? 'bg-critical/15 text-critical' : 'bg-review/15 text-review'
                        }`}>
                          {c.tier === 'Tier 1 Hold' ? 'Hold' : 'Review'}
                        </span>
                      </div>

                      <div className="font-medium text-text text-[11px] truncate" title={c.title}>
                        {c.subjectEntity}
                      </div>

                      <div className="flex items-center justify-between text-[10px] font-mono mt-1 pt-1 border-t border-border/40 text-text-muted">
                        <span>${c.totalExposure?.toLocaleString()}</span>
                        <span className="text-amber-500 font-semibold flex items-center gap-1">
                          <Clock className="w-2.5 h-2.5" />
                          <span>38m SLA</span>
                        </span>
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* PANEL 2: EXPANSIVE HERO CANVAS & CHRONICLE (Wide Center Column)           */}
        {/* ========================================================================= */}
        <div className={`${centerColSpan} space-y-2.5 flex flex-col transition-all`}>

          {/* Top Canvas Toolbar */}
          <div className="p-2 rounded-lg bg-surface border border-border shadow-xs flex flex-wrap items-center justify-between gap-2 text-xs font-mono">
            {/* Left: Layout Switcher & Wide Canvas Toggle */}
            <div className="flex items-center gap-1.5 flex-wrap">
              {!focusMode && isQueueCollapsed && (
                <button
                  onClick={() => setIsQueueCollapsed(false)}
                  className="px-2 py-1 rounded bg-bg hover:bg-surfaceRaised border border-border text-[11px] font-mono text-text flex items-center gap-1 cursor-pointer transition-colors"
                  title="Show Triage Queue"
                >
                  <PanelLeftOpen className="w-3.5 h-3.5 text-accent" />
                  <span>Queue</span>
                </button>
              )}

              <span className="text-text-muted text-[11px] font-sans font-medium mr-0.5">Layout:</span>
              <div className="flex items-center p-0.5 bg-bg rounded border border-border text-[11px]">
                {[
                  { id: 'sugiyama', label: 'Sugiyama Flow' },
                  { id: 'orbital', label: 'Orbital Ring' },
                  { id: 'cose', label: 'COSE' },
                  { id: 'circle', label: 'Cycle Ring' }
                ].map(l => (
                  <button
                    key={l.id}
                    onClick={() => setLayoutMode(l.id)}
                    className={`px-2 py-0.5 rounded transition-colors cursor-pointer ${
                      layoutMode === l.id
                        ? 'bg-surface font-bold text-accent shadow-xs'
                        : 'text-text-muted hover:text-text'
                    }`}
                  >
                    {l.label}
                  </button>
                ))}
              </div>

              {!focusMode && (
                <button
                  onClick={() => setIsQueueCollapsed(!isQueueCollapsed)}
                  className="px-2 py-0.5 rounded bg-bg hover:bg-surfaceRaised border border-border text-[10px] font-mono text-text-muted hover:text-text cursor-pointer transition-colors hidden sm:flex items-center gap-1"
                  title={isQueueCollapsed ? "Show Triage Queue" : "Expand canvas horizontally"}
                >
                  <span>{isQueueCollapsed ? "Standard Width" : "Wide Canvas"}</span>
                </button>
              )}
            </div>

            {/* Right: Noise Prune & Snapshot */}
            <div className="flex items-center gap-2">
              <div className="flex items-center gap-1.5 text-[11px] px-2 py-0.5 rounded bg-bg border border-border">
                <span className="text-text-muted">Prune:</span>
                <input
                  type="range"
                  min="0"
                  max="0.4"
                  step="0.05"
                  value={camouflageDelta}
                  onChange={(e) => setCamouflageDelta(parseFloat(e.target.value))}
                  className="w-14 h-1.5 bg-border rounded-lg appearance-none cursor-pointer accent-accent"
                />
                <span className="font-bold text-text w-6 text-right">
                  {Math.round(camouflageDelta * 100)}%
                </span>
              </div>

              <button
                onClick={handleExportSnapshot}
                className="px-2 py-1 rounded bg-surfaceRaised border border-border hover:border-accent text-text text-[11px] font-medium cursor-pointer flex items-center gap-1 transition-colors shadow-xs"
                title="Export Rule 902(11) Cryptographic Snapshot"
              >
                <Download className="w-3 h-3 text-accent" />
                <span>Proof</span>
              </button>
            </div>
          </div>

          {/* Graph Viewport (Optimized Height for Zero-Scroll Viewport) */}
          <div className="w-full">
            {engineMode === '2D' ? (
              <Cytoscape2DGraph
                layoutMode={layoutMode}
                onLayoutChange={setLayoutMode}
                selectedNodeId={selectedGraphNode?.id || activeCase?.subjectAccount}
                onNodeSelect={(node) => setSelectedGraphNode(node)}
                showTopControls={false}
                externalCamouflageDelta={camouflageDelta}
                className="relative w-full h-[430px] sm:h-[450px] lg:h-[470px] bg-surface rounded-lg border border-border overflow-hidden flex flex-col justify-between select-none shadow-xs"
              />
            ) : (
              <div className="w-full h-[430px] sm:h-[450px] lg:h-[470px] rounded-lg border border-border overflow-hidden relative bg-surface">
                <Suspense fallback={
                  <div className="w-full h-full flex flex-col items-center justify-center text-xs font-mono text-text-muted gap-2">
                    <span className="w-3 h-3 rounded-full bg-accent animate-ping" />
                    <span>Initializing WebGL 3D Engine...</span>
                  </div>
                }>
                  <Neo4j3DGraph />
                </Suspense>
              </div>
            )}
          </div>

          {/* Collapsible Multi-Hop Chronicle Shelf */}
          <div className="bg-surface border border-border rounded-lg overflow-hidden shadow-xs">
            <div
              onClick={() => setIsChronicleOpen(!isChronicleOpen)}
              className="p-2 px-3 bg-surfaceRaised flex items-center justify-between cursor-pointer select-none text-xs"
            >
              <div className="flex items-center gap-2">
                <Repeat className="w-3.5 h-3.5 text-accent" />
                <span className="font-bold uppercase tracking-wider text-text text-[11px]">
                  Multi-Hop Chronicle
                </span>
                <span className="px-1.5 py-0.2 rounded text-[10px] font-mono bg-bg text-text-muted border border-border">
                  {CHRONICLE_HOPS.length - 1} Hops
                </span>
              </div>
              <div className="flex items-center gap-1 text-text-muted text-[11px] font-mono">
                <span>{isChronicleOpen ? 'Hide' : 'Expand'}</span>
                {isChronicleOpen ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
              </div>
            </div>

            {isChronicleOpen && (
              <div className="overflow-x-auto max-h-[170px]">
                <table className="w-full text-left text-[11px] font-mono">
                  <thead className="bg-bg text-text-muted border-b border-border sticky top-0 z-10">
                    <tr>
                      <th className="py-1.5 px-3">Hop</th>
                      <th className="py-1.5 px-3">Time</th>
                      <th className="py-1.5 px-3">Path</th>
                      <th className="py-1.5 px-3">Rail</th>
                      <th className="py-1.5 px-3 text-right">Volume</th>
                      <th className="py-1.5 px-3">Dwell</th>
                      <th className="py-1.5 px-3">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-border/50">
                    {CHRONICLE_HOPS.map((hop) => {
                      const isActive = timelineStep === hop.step;
                      return (
                        <tr
                          key={hop.step}
                          onClick={() => setTimelineStep(hop.step)}
                          className={`cursor-pointer transition-colors ${
                            isActive
                              ? 'bg-accent/10 font-bold text-text'
                              : 'hover:bg-bg/80 text-text-2'
                          }`}
                        >
                          <td className="py-1.5 px-3 whitespace-nowrap">
                            <span className={`px-1.5 py-0.2 rounded text-[10px] ${
                              hop.step === 0 ? 'bg-cleared/15 text-cleared' : 'bg-critical/15 text-critical'
                            }`}>
                              {hop.step === 0 ? 't₀' : `t${hop.step}`}
                            </span>
                          </td>
                          <td className="py-1.5 px-3 whitespace-nowrap text-text-muted">{hop.timestamp}</td>
                          <td className="py-1.5 px-3 whitespace-nowrap">
                            <span>{hop.origin}</span>
                            <span className="text-text-muted mx-1">➔</span>
                            <span>{hop.beneficiary}</span>
                          </td>
                          <td className="py-1.5 px-3 whitespace-nowrap">
                            <span className="px-1.5 py-0.2 rounded bg-surfaceRaised text-text-muted text-[10px] border border-border/50">
                              {hop.rail}
                            </span>
                          </td>
                          <td className="py-1.5 px-3 text-right whitespace-nowrap font-semibold text-text">
                            {hop.amount}
                          </td>
                          <td className="py-1.5 px-3 whitespace-nowrap text-text-muted">
                            {hop.dwell}
                          </td>
                          <td className="py-1.5 px-3 whitespace-nowrap">
                            <span className={hop.status === 'VIOLATION' ? 'text-critical font-semibold' : hop.status === 'FLAGGED' ? 'text-amber-500 font-semibold' : 'text-cleared'}>
                              {hop.invariant}
                            </span>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>

        {/* ========================================================================= */}
        {/* PANEL 3: PROGRESSIVE EXPLANATORY INSPECTOR (Right Column)                 */}
        {/* ========================================================================= */}
        {!focusMode && (
          <div className="lg:col-span-3 space-y-2.5 flex flex-col">

            {/* Unified Entity Header & Status */}
            <div className="p-2.5 rounded-lg bg-surface border border-border shadow-xs space-y-2">
              <div className="flex items-start justify-between gap-2">
                <div className="min-w-0">
                  <span className="text-[10px] font-mono text-text-muted uppercase">Inspected Target</span>
                  <h3 className="font-bold text-text text-xs truncate">
                    {entityDossier?.name || 'Meghna Industrial & Agro'}
                  </h3>
                  <span className="font-mono text-[10px] text-text-muted truncate block">
                    {activeEntityAccount}
                  </span>
                </div>
                <Badge
                  variant={entityDossier?.riskScore > 0.8 ? 'critical' : 'review'}
                  size="sm"
                  className="font-mono text-[10px] shrink-0"
                >
                  {entityDossier?.riskRating ? entityDossier.riskRating.split(' ')[0] : 'CRITICAL'}
                </Badge>
              </div>

              {/* Micro Flow Meter */}
              <div className="space-y-1 font-mono text-[11px]">
                <div className="flex justify-between text-[10px]">
                  <span className="text-text-muted">Flow Conservation (Φ):</span>
                  <span className="font-bold text-critical">
                    {entityDossier?.flowConservation?.phiFlow || 0.992} (99.2% Pass-Through)
                  </span>
                </div>
                <div className="w-full bg-border h-1 rounded-full overflow-hidden">
                  <div
                    className="bg-critical h-full rounded-full transition-all duration-500"
                    style={{ width: `${(entityDossier?.flowConservation?.phiFlow || 0.992) * 100}%` }}
                  />
                </div>
              </div>

              {/* Segmented Inspector Tabs (Progressive Disclosure) */}
              <div className="flex items-center p-0.5 bg-bg rounded border border-border font-mono text-[11px] pt-1">
                <button
                  onClick={() => setInspectorTab('evidence')}
                  className={`flex-1 py-1 rounded text-center transition-colors cursor-pointer ${
                    inspectorTab === 'evidence'
                      ? 'bg-surface font-bold text-accent shadow-xs'
                      : 'text-text-muted hover:text-text'
                  }`}
                >
                  Evidence & SHAP
                </button>
                <button
                  onClick={() => setInspectorTab('recourse')}
                  className={`flex-1 py-1 rounded text-center transition-colors cursor-pointer ${
                    inspectorTab === 'recourse'
                      ? 'bg-surface font-bold text-accent shadow-xs'
                      : 'text-text-muted hover:text-text'
                  }`}
                >
                  What-If Recourse
                </button>
              </div>

              {/* TAB CONTENT 1: EVIDENCE & CAUSAL SHAP */}
              {inspectorTab === 'evidence' && (
                <div className="space-y-2 pt-1 text-xs">
                  {/* Typology Match Pill */}
                  <div className="p-2 rounded bg-critical/10 border border-critical/20 space-y-0.5">
                    <div className="flex items-center justify-between text-[11px] font-bold text-critical">
                      <span>FATF Typology #4</span>
                      <span className="text-[10px] font-mono">FinCEN §1020</span>
                    </div>
                    <p className="text-[10px] text-text-2 leading-tight">
                      Rapid pass-through layering to Dubai JAFZA free zone with circular trade wash loop.
                    </p>
                  </div>

                  {/* SHAP Attribution Waterfall */}
                  <div className="space-y-1.5 font-mono text-[11px]">
                    <span className="text-[10px] font-bold text-text-muted uppercase tracking-wider block">
                      Causal Risk Drivers
                    </span>
                    {[
                      { name: 'Dwell Deficit (<120s)', impact: '+38%', width: '38%', isRisk: true },
                      { name: 'Conservation (99.8%)', impact: '+29%', width: '29%', isRisk: true },
                      { name: 'Offshore Conduit', impact: '+19%', width: '19%', isRisk: true },
                      { name: 'Frequency Burst', impact: '+10%', width: '10%', isRisk: true },
                      { name: 'Commercial License', impact: '-6%', width: '12%', isRisk: false }
                    ].map((driver, i) => (
                      <div key={i} className="space-y-0.5">
                        <div className="flex justify-between text-[10px]">
                          <span className="text-text-2 truncate max-w-[170px]">{driver.name}</span>
                          <span className={driver.isRisk ? 'text-critical font-bold' : 'text-cleared font-bold'}>
                            {driver.impact}
                          </span>
                        </div>
                        <div className="w-full bg-border h-1 rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full ${driver.isRisk ? 'bg-critical' : 'bg-cleared'}`}
                            style={{ width: driver.width }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* TAB CONTENT 2: WHAT-IF RECOURSE SIMULATOR */}
              {inspectorTab === 'recourse' && (
                <div className="space-y-2 pt-1 text-xs font-mono">
                  {/* Dwell Slider */}
                  <div className="space-y-1 text-[11px]">
                    <div className="flex justify-between text-text-muted">
                      <span>Dwell Time:</span>
                      <span className="font-bold text-text">
                        {simulatedDwellHours < 1 ? `${Math.round(simulatedDwellHours * 60)}m` : `${simulatedDwellHours}h`}
                      </span>
                    </div>
                    <input
                      type="range"
                      min="0.2"
                      max="48"
                      step="0.5"
                      value={simulatedDwellHours}
                      onChange={(e) => setSimulatedDwellHours(parseFloat(e.target.value))}
                      className="w-full h-1.5 bg-border rounded-lg appearance-none cursor-pointer accent-accent"
                    />
                  </div>

                  {/* Amount Slider */}
                  <div className="space-y-1 text-[11px]">
                    <div className="flex justify-between text-text-muted">
                      <span>Ticket Size:</span>
                      <span className="font-bold text-text">${simulatedAmount.toLocaleString()}</span>
                    </div>
                    <input
                      type="range"
                      min="2000"
                      max="50000"
                      step="1000"
                      value={simulatedAmount}
                      onChange={(e) => setSimulatedAmount(parseInt(e.target.value))}
                      className="w-full h-1.5 bg-border rounded-lg appearance-none cursor-pointer accent-accent"
                    />
                  </div>

                  {/* Recourse Outcome Box */}
                  <div className="p-2 rounded bg-bg border border-border text-[10px] space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="text-text-muted">Prediction:</span>
                      <Badge variant={counterfactualOutcome.badgeVariant} size="sm">
                        {counterfactualOutcome.tier} ({counterfactualOutcome.conformalSet})
                      </Badge>
                    </div>
                    <p className="text-text-2 leading-tight">
                      {counterfactualOutcome.explanation}
                    </p>
                  </div>
                </div>
              )}
            </div>

            {/* Unified Compliance Action Dock */}
            <div className="p-2.5 rounded-lg bg-surface border border-border shadow-xs space-y-2">
              <span className="text-[10px] font-mono text-text-muted uppercase font-bold tracking-wider block">
                1-Click Decision Dock
              </span>

              <div className="grid grid-cols-3 gap-1.5 font-mono text-xs">
                {/* Primary Action: Hold */}
                <button
                  onClick={handleFreezeDebit}
                  className="py-1.5 px-1 rounded bg-critical hover:bg-critical/90 text-white font-semibold flex flex-col items-center justify-center gap-1 cursor-pointer transition-colors shadow-xs"
                  title="Place Core Banking Administrative Hold"
                >
                  <Lock className="w-3.5 h-3.5" />
                  <span className="text-[10px] truncate">Debit Hold</span>
                </button>

                {/* Notice Action */}
                <button
                  onClick={() => setIsNoticeModalOpen(true)}
                  className="py-1.5 px-1 rounded bg-surfaceRaised hover:bg-surface border border-border hover:border-accent text-text font-semibold flex flex-col items-center justify-center gap-1 cursor-pointer transition-colors shadow-xs"
                  title="Issue Non-Tipping Customer RFI Notice"
                >
                  <Mail className="w-3.5 h-3.5 text-accent" />
                  <span className="text-[10px] truncate">Notice RFI</span>
                </button>

                {/* SAR Action */}
                <button
                  onClick={handleDraftSAR}
                  className="py-1.5 px-1 rounded bg-accent hover:bg-accent/90 text-white font-semibold flex flex-col items-center justify-center gap-1 cursor-pointer transition-colors shadow-xs"
                  title="Draft Statutory FinCEN / BFIU SAR"
                >
                  <FileText className="w-3.5 h-3.5" />
                  <span className="text-[10px] truncate">Draft SAR</span>
                </button>
              </div>

              {/* Discreet Safeguard Footnote */}
              <div className="pt-1 flex items-center justify-center gap-1 text-[10px] text-text-muted font-mono border-t border-border/40">
                <ShieldCheck className="w-3 h-3 text-cleared" />
                <span>31 U.S.C. § 5318(g)(2) Non-Tipping Airgap</span>
              </div>
            </div>
          </div>
        )}

      </div>

      {/* Customer Notice Modal (Strict Anti-Tipping-Off Isolation) */}
      <CustomerNoticeModal
        isOpen={isNoticeModalOpen}
        onClose={() => setIsNoticeModalOpen(false)}
        targetAccount={{
          holderName: entityDossier?.name || 'Meghna Industrial & Agro Processing Ltd',
          accountNumber: activeEntityAccount,
          amount: activeCase.totalExposure || 48500,
          rail: 'SWIFT MT700 (LC)'
        }}
        onNoticeDispatched={() => {
          setIsNoticeModalOpen(false);
          addToast('RFI Dispatched', `Neutral verification request transmitted to ${entityDossier?.name}.`, 'success');
        }}
      />
    </div>
  );
};
