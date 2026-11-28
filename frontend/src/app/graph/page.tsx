'use client';

import React, { useState, useEffect, useRef, Suspense, useMemo } from 'react';
import dynamic from 'next/dynamic';
import { useSearchParams, useRouter } from 'next/navigation';
import cytoscape from 'cytoscape';
import { ErrorBoundary } from '@/components/common/ErrorBoundary';

const ForceGraph3DCanvas = dynamic(() => import('@/components/graph/ForceGraph3DCanvas'), {
  ssr: false,
  loading: () => (
    <div className="w-full h-full flex items-center justify-center text-xs font-mono text-slate-400">
      Initializing WebGL 3D Engine...
    </div>
  )
});
import {
  GitFork,
  SlidersHorizontal,
  Play,
  Pause,
  Maximize2,
  Minimize2,
  Box,
  Eye,
  ShieldAlert,
  Building,
  RotateCcw,
  Lock,
  Layers,
  Info,
  ZoomIn,
  Compass,
  CheckCircle2,
  UserCheck,
  AlertTriangle,
  FileText,
  Users,
  Shield,
  ExternalLink
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { PiiText } from '@/components/ui/PiiText';

const SCENARIOS = [
  {
    id: 'meghna_tbml',
    name: '1. Meghna TBML Over-Invoicing Ring',
    rootNode: 'BD22-EBLB-4829-1092-8823',
    description: 'Chittagong port documentary trade LC over-invoiced by +333.7% routed to JAFZA Dubai free zone.'
  },
  {
    id: 'tanvir_mfs',
    name: '2. Tanvir Multi-Agent MFS Cash Structuring',
    rootNode: 'MFS-BKASH-0171-8840',
    description: 'Rapid velocity burst structuring across 14 mobile financial service agents below statutory limits.'
  },
  {
    id: 'cross_border',
    name: '3. Cross-Border Shell Corporation Loop',
    rootNode: 'KY-CIMA-7719-4402-1102',
    description: 'Layered corporate pass-through loop between London, Zurich, Singapore, and Cayman Islands.'
  }
];

function ForensicGraphStudioContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const initialNode = searchParams?.get('node') || 'BD22-EBLB-4829-1092-8823';

  const { setFourEyesModalOpen } = useBankingStore();

  const [activeScenario, setActiveScenario] = useState<string>(
    initialNode === 'MFS-BKASH-0171-8840' ? 'tanvir_mfs' : initialNode === 'KY-CIMA-7719-4402-1102' ? 'cross_border' : 'meghna_tbml'
  );
  const [viewMode, setViewMode] = useState<'2D' | '3D'>('2D');
  const [deltaFloor, setDeltaFloor] = useState<number>(0.10);
  const [egoHops, setEgoHops] = useState<number>(2);
  const [maxNodes, setMaxNodes] = useState<number>(100);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [temporalStep, setTemporalStep] = useState<number>(100);
  const [selectedNode, setSelectedNode] = useState<any>(null);
  const [subgraphData, setSubgraphData] = useState<any>(null);
  const [isFullscreen, setIsFullscreen] = useState<boolean>(false);
  const [drawerTab, setDrawerTab] = useState<'TELEMETRY' | 'ENTITY_RES' | 'SANCTIONS' | 'UBO'>('TELEMETRY');

  const containerRef = useRef<HTMLDivElement>(null);
  const cyContainerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<cytoscape.Core | null>(null);

  // Fetch subgraph data
  useEffect(() => {
    async function loadGraph() {
      try {
        const res = await fetch(`/api/v1/graph/subgraph/${encodeURIComponent(initialNode)}?hops=${egoHops}`);
        const data = await res.json();
        setSubgraphData(data);
        if (data.nodes && data.nodes.length > 0) {
          setSelectedNode(data.nodes[0]);
        }
      } catch (err) {
        console.error('Failed to load subgraph:', err);
      }
    }
    loadGraph();
  }, [initialNode, egoHops]);

  // Toggle fullscreen
  const toggleFullscreen = () => {
    if (!containerRef.current) return;
    if (!document.fullscreenElement) {
      containerRef.current.requestFullscreen?.().then(() => setIsFullscreen(true)).catch(() => {});
    } else {
      document.exitFullscreen?.().then(() => setIsFullscreen(false)).catch(() => {});
    }
  };

  const handleResetCamera = () => {
    if (cyRef.current) {
      cyRef.current.fit(undefined, 40);
    }
  };

  const handleSelectScenario = (scId: string) => {
    setActiveScenario(scId);
    const target = SCENARIOS.find((s) => s.id === scId);
    if (target) {
      router.push(`/graph?node=${encodeURIComponent(target.rootNode)}`);
    }
  };

  // Chronological Temporal Playback Timer (Hawkes Δt)
  useEffect(() => {
    if (!isPlaying) return;
    const timer = setInterval(() => {
      setTemporalStep((prev) => (prev >= 100 ? 10 : Math.min(100, prev + 10)));
    }, 350);
    return () => clearInterval(timer);
  }, [isPlaying]);

  const { filteredNodes, visibleEdges, prunedCount } = useMemo(() => {
    const allEdges = subgraphData?.edges || [];
    const trustFiltered = allEdges.filter((e: any) => e.edgeTrustDelta >= deltaFloor);
    const stepLimit = Math.max(1, Math.ceil((trustFiltered.length * temporalStep) / 100));
    const stepEdges = temporalStep >= 100 ? trustFiltered : trustFiltered.slice(0, stepLimit);

    const activeIds = new Set<string>();
    stepEdges.forEach((e: any) => {
      activeIds.add(e.source);
      activeIds.add(e.target);
    });

    const nodes = (subgraphData?.nodes || [])
      .filter((n: any) => activeIds.has(n.id) || n.id === initialNode)
      .slice(0, maxNodes);

    return {
      filteredNodes: nodes,
      visibleEdges: stepEdges,
      prunedCount: Math.max(0, allEdges.length - trustFiltered.length)
    };
  }, [subgraphData, deltaFloor, temporalStep, maxNodes, initialNode]);

  // Initialize and update Cytoscape instance
  useEffect(() => {
    if (!subgraphData || !cyContainerRef.current || viewMode !== '2D') return;

    const elements: cytoscape.ElementDefinition[] = [
      ...filteredNodes.map((n: any) => ({
        data: {
          id: n.id,
          label: n.entityName.split(' ')[0] || n.label,
          fullData: n,
          tier: n.tier,
          type: n.type
        }
      })),
      ...visibleEdges.map((e: any) => ({
        data: {
          id: e.id,
          source: e.source,
          target: e.target,
          amount: e.amount,
          rail: e.rail,
          delta: e.edgeTrustDelta,
          fullData: e
        }
      }))
    ];

    if (cyRef.current) {
      cyRef.current.destroy();
    }

    const cy = cytoscape({
      container: cyContainerRef.current,
      elements,
      layout: {
        name: 'cose',
        animate: false,
        nodeRepulsion: () => 16000,
        idealEdgeLength: () => 140,
        edgeElasticity: () => 100,
        padding: 50
      },
      style: [
        {
          selector: 'node',
          style: {
            label: 'data(label)',
            color: '#E2E8F0',
            'font-size': '11px',
            'font-family': 'monospace',
            'font-weight': 'bold',
            'text-valign': 'bottom',
            'text-margin-y': 6,
            'text-background-color': '#0F172A',
            'text-background-opacity': 0.85,
            'text-background-padding': '2px',
            'text-background-shape': 'roundrectangle',
            'background-color': '#334155',
            width: 36,
            height: 36,
            'border-width': 2,
            'border-color': '#64748B'
          }
        },
        {
          selector: 'node[tier = 1]',
          style: {
            'background-color': '#881337',
            'border-color': '#F43F5E',
            width: 44,
            height: 44
          }
        },
        {
          selector: 'node[tier = 2]',
          style: {
            'background-color': '#78350F',
            'border-color': '#F59E0B',
            width: 38,
            height: 38
          }
        },
        {
          selector: 'node[tier = 3]',
          style: {
            'background-color': '#064E3B',
            'border-color': '#10B981',
            width: 32,
            height: 32
          }
        },
        {
          selector: 'edge',
          style: {
            width: 2,
            'line-color': '#475569',
            'target-arrow-color': '#64748B',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            label: 'data(rail)',
            'font-size': '9px',
            'font-family': 'monospace',
            color: '#94A3B8',
            'text-rotation': 'autorotate',
            'text-background-color': '#0B0F17',
            'text-background-opacity': 0.90,
            'text-background-padding': '3px',
            'text-background-shape': 'roundrectangle',
            'text-border-color': '#334155',
            'text-border-width': 1,
            'text-border-opacity': 0.8
          }
        },
        {
          selector: 'edge[delta > 0.85]',
          style: {
            'line-color': '#F43F5E',
            'target-arrow-color': '#F43F5E',
            width: 3
          }
        },
        {
          selector: ':selected',
          style: {
            'border-color': '#38BDF8',
            'border-width': 4
          }
        }
      ]
    });

    cy.on('tap', 'node', (evt) => {
      const node = evt.target;
      setSelectedNode(node.data('fullData'));
    });

    cyRef.current = cy;

    return () => {
      cy.destroy();
    };
  }, [subgraphData, filteredNodes, visibleEdges, viewMode]);

  return (
    <div ref={containerRef} className="p-4 sm:p-5 lg:p-6 max-w-[1750px] mx-auto space-y-4">
      {/* Header and Scenario Selector */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2 font-sans">
            <GitFork className="w-5 h-5 text-purple-400" />
            Forensic Cash Flow Studio — Multi-Hop Topology
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Real-time interbank flow topology with Pass-Through Flow Ratios, adaptive edge noise gating, and camouflage cycle pruning.
          </p>
        </div>

        {/* View Controls */}
        <div className="flex items-center gap-3">
          {/* Preset Scenario Selector */}
          <select
            value={activeScenario}
            onChange={(e) => handleSelectScenario(e.target.value)}
            className="px-3 py-1.5 rounded-lg bg-panel border border-line-strong text-xs text-purple-300 font-semibold cursor-pointer"
          >
            {SCENARIOS.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>

          {/* Hop Distance Expansion */}
          <div className="flex items-center bg-panel p-1 rounded-lg border border-line-strong text-xs font-mono">
            <span className="text-slate-400 px-2 text-xs">Hops:</span>
            {([1, 2, 3] as const).map((h) => (
              <button
                key={h}
                onClick={() => setEgoHops(h)}
                className={`px-2 py-0.5 rounded transition-all cursor-pointer ${
                  egoHops === h
                    ? 'bg-purple-500/20 text-purple-300 font-bold border border-purple-500/40'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {h}-Hop
              </button>
            ))}
          </div>

          {/* Progressive Disclosure Node Capping */}
          <div className="flex items-center bg-panel p-1 rounded-lg border border-line-strong text-xs font-mono">
            <span className="text-slate-400 px-2 text-xs">Node Cap:</span>
            {([25, 50, 100, 250] as const).map((cap) => (
              <button
                key={cap}
                onClick={() => setMaxNodes(cap)}
                className={`px-2 py-0.5 rounded transition-all cursor-pointer ${
                  maxNodes === cap
                    ? 'bg-purple-500/20 text-purple-300 font-bold border border-purple-500/40'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {cap}
              </button>
            ))}
          </div>

          {/* View Switcher: 2D Planar vs 3D Force */}
          <div className="flex items-center bg-panel p-1 rounded-lg border border-line-strong">
            <button
              onClick={() => setViewMode('2D')}
              className={`flex items-center gap-1.5 px-3 py-1 rounded text-xs font-semibold transition-all cursor-pointer ${
                viewMode === '2D'
                  ? 'bg-purple-500/20 text-purple-300 border border-purple-500/40'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Eye className="w-3.5 h-3.5" />
              <span>2D Planar</span>
            </button>
            <button
              onClick={() => setViewMode('3D')}
              className={`flex items-center gap-1.5 px-3 py-1 rounded text-xs font-semibold transition-all cursor-pointer ${
                viewMode === '3D'
                  ? 'bg-purple-500/20 text-purple-300 border border-purple-500/40'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Box className="w-3.5 h-3.5" />
              <span>3D WebGL</span>
            </button>
          </div>
        </div>
      </div>

      {/* Main Studio Viewport */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 min-h-[540px] h-[calc(100vh-230px)]">
        {/* Graph Canvas Container (8 Cols) */}
        <div className="lg:col-span-8 bg-panel border border-line rounded-xl relative overflow-hidden flex flex-col shadow-2xl">
          {/* Top Canvas Bar: Noise Filter & Camera Controls */}
          <div className="p-3 bg-canvas/80 border-b border-line flex flex-wrap items-center justify-between gap-3 z-10 text-xs">
            {/* Adaptive Edge Noise Filter Slider */}
            <div className="flex items-center gap-3 bg-panel px-3 py-1.5 rounded-lg border border-line-strong">
              <span className="font-semibold text-slate-300 flex items-center gap-1.5">
                <SlidersHorizontal className="w-3.5 h-3.5 text-purple-400" />
                Adaptive Edge-Trust Gate (ĝ_ij ≥ δ_floor):
              </span>
              <input
                type="range"
                min="0.00"
                max="0.95"
                step="0.02"
                value={deltaFloor}
                onChange={(e) => setDeltaFloor(Number(e.target.value))}
                className="w-28 sm:w-36 accent-purple-500 cursor-pointer"
              />
              <span className="font-mono font-bold text-purple-300 text-xs min-w-[3ch] tabular-nums">
                {deltaFloor.toFixed(2)}
              </span>
            </div>

            {/* Fusion Weight Pill */}
            <div className="hidden 2xl:flex items-center gap-1.5 px-2.5 py-1 rounded bg-panel border border-line-strong text-xs font-mono text-slate-300">
              <span className="text-purple-400 font-bold">α_u = 0.65</span>
              <span className="text-slate-500">GNN/Tabular Fusion</span>
            </div>

            {/* Invariant Stats & Camera Controls */}
            <div className="flex items-center gap-2 sm:gap-3 text-xs font-mono">
              <span className="hidden sm:inline text-slate-400">
                Pruned: <strong className="text-rose-400">{prunedCount} camouflage edges</strong>
              </span>

              <button
                onClick={handleResetCamera}
                className="flex items-center gap-1 px-2.5 py-1 rounded bg-canvas hover:bg-surface text-slate-300 border border-line-strong cursor-pointer transition-colors"
                title="Reset Camera & Fit to Screen"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span className="hidden md:inline">Fit</span>
              </button>

              <button
                onClick={toggleFullscreen}
                className="flex items-center gap-1 px-2.5 py-1 rounded bg-canvas hover:bg-surface text-slate-300 border border-line-strong cursor-pointer transition-colors"
                title="Toggle Fullscreen Canvas"
              >
                {isFullscreen ? <Minimize2 className="w-3.5 h-3.5" /> : <Maximize2 className="w-3.5 h-3.5" />}
                <span className="hidden md:inline">{isFullscreen ? 'Exit' : 'Full'}</span>
              </button>
            </div>
          </div>

          {/* Graph Viewport */}
          <div className="flex-1 relative bg-canvas overflow-hidden">
            <ErrorBoundary viewName="Forensic Graph Studio Viewport">
              {viewMode === '2D' ? (
                <div ref={cyContainerRef} className="w-full h-full" />
              ) : (
                <ForceGraph3DCanvas
                  nodes={filteredNodes}
                  edges={visibleEdges}
                  onSelectNode={(node) => setSelectedNode(node)}
                  onFallbackTo2D={() => setViewMode('2D')}
                />
              )}
            </ErrorBoundary>

            {/* Bottom-Right Minimap Badge */}
            <div className="absolute bottom-4 right-4 p-2 rounded-lg bg-panel/85 backdrop-blur-sm border border-line-strong flex items-center gap-2 text-xs font-mono text-slate-400 pointer-events-none select-none">
              <Compass className="w-4 h-4 text-purple-400 animate-spin-slow" />
              <span>Network Topology Radar</span>
            </div>
          </div>

          {/* Bottom Temporal Playback Scrubber */}
          <div className="p-3 bg-canvas/95 border-t border-line flex items-center gap-3 sm:gap-4 text-xs z-10">
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className="p-1.5 rounded-lg bg-purple-950/40 hover:bg-purple-900/60 text-purple-300 border border-purple-800/40 transition-colors cursor-pointer shrink-0"
            >
              {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
            </button>
            <span className="text-xs font-semibold text-slate-400 shrink-0 font-mono">
              Temporal Step (Sequence Scrubbing):
            </span>
            <input
              type="range"
              min="0"
              max="100"
              value={temporalStep}
              onChange={(e) => setTemporalStep(Number(e.target.value))}
              className="w-full accent-emerald-500 cursor-pointer"
            />
            <span className="font-mono text-xs text-emerald-400 shrink-0 tabular-nums min-w-[5ch] text-right">
              {temporalStep}%
            </span>
          </div>
        </div>

        {/* 4-Tab 360° Entity Context Drawer (4 Cols) */}
        <div className="lg:col-span-4 bg-panel border border-line rounded-xl p-5 flex flex-col justify-between overflow-y-auto shadow-2xl">
          {selectedNode ? (
            <div className="space-y-4">
              {/* Header */}
              <div className="flex items-center justify-between pb-3 border-b border-line">
                <div>
                  <span className="text-xs font-mono font-semibold text-slate-400 block">
                    360° Node Context
                  </span>
                  <h3 className="font-bold text-sm text-slate-100 flex items-center gap-1.5 mt-0.5">
                    <Building className="w-4 h-4 text-slate-400 shrink-0" />
                    <span className="truncate">{selectedNode.entityName}</span>
                  </h3>
                </div>

                <span
                  className={`px-2 py-0.5 rounded text-xs font-mono font-bold ${
                    selectedNode.tier === 1
                      ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                      : selectedNode.tier === 2
                      ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                      : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                  }`}
                >
                  Tier {selectedNode.tier}
                </span>
              </div>

              {/* 4 Tabs */}
              <div className="grid grid-cols-4 gap-1 p-1 bg-canvas rounded-lg border border-line text-xs font-mono">
                {(['TELEMETRY', 'ENTITY_RES', 'SANCTIONS', 'UBO'] as const).map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setDrawerTab(tab)}
                    className={`py-1 rounded text-center transition-colors cursor-pointer ${
                      drawerTab === tab
                        ? 'bg-surface text-sky-300 font-bold'
                        : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    {tab === 'TELEMETRY' ? 'Metrics' : tab === 'ENTITY_RES' ? 'Entity' : tab === 'SANCTIONS' ? 'Watchlist' : 'UBO'}
                  </button>
                ))}
              </div>

              {/* Tab Contents */}
              {drawerTab === 'TELEMETRY' && (
                <div className="space-y-2 text-xs font-sans">
                  <div className="p-2.5 bg-canvas rounded-lg border border-line flex items-center justify-between">
                    <span className="text-slate-400">Account / IBAN:</span>
                    <PiiText value={selectedNode.id} type="account" className="font-mono text-slate-200" />
                  </div>
                  <div className="p-2.5 bg-canvas rounded-lg border border-line flex items-center justify-between">
                    <span className="text-slate-400">Pass-Through Flow Ratio:</span>
                    <strong className="font-mono text-rose-400 tabular-nums">
                      {selectedNode.phiFlow || '0.994'} (Near 1.0 Pass-Through)
                    </strong>
                  </div>
                  <div className="p-2.5 bg-canvas rounded-lg border border-line flex items-center justify-between">
                    <span className="text-slate-400">Velocity Burst Score:</span>
                    <strong className="font-mono text-amber-400 tabular-nums">
                      {selectedNode.lambdaU || '4.82'} events / hr
                    </strong>
                  </div>
                  <div className="p-2.5 bg-canvas rounded-lg border border-line flex items-center justify-between">
                    <span className="text-slate-400">Jurisdiction:</span>
                    <strong className="font-mono text-slate-200">{selectedNode.jurisdiction}</strong>
                  </div>
                  <div className="p-2.5 bg-canvas rounded-lg border border-line flex items-center justify-between">
                    <span className="text-slate-400">Calibrated Risk Score:</span>
                    <strong className="font-mono text-rose-400 tabular-nums">{selectedNode.riskScore}</strong>
                  </div>
                </div>
              )}

              {drawerTab === 'ENTITY_RES' && (
                <div className="space-y-3 text-xs">
                  <div className="p-3 bg-canvas rounded-xl border border-line space-y-1">
                    <span className="text-slate-500 text-xs font-mono block">Resolved Corporate Entity</span>
                    <span className="font-bold text-slate-100">{selectedNode.entityName}</span>
                    <span className="text-xs text-slate-400 block">Registration: CTG-EXP-2018-99120</span>
                  </div>

                  <div className="p-3 bg-canvas rounded-xl border border-line space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-slate-400 text-xs">Entity Resolution Match</span>
                      <span className="font-mono text-emerald-400 font-bold">96.8% Confidence</span>
                    </div>
                    <p className="text-xs text-slate-400">
                      Merged 3 accounts across City Bank, EBL, and bKash corporate wallet into single synthetic node.
                    </p>
                  </div>
                </div>
              )}

              {drawerTab === 'SANCTIONS' && (
                <div className="space-y-2 text-xs">
                  <div className="p-3 bg-canvas rounded-xl border border-line space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-slate-400">OFAC SDN Watchlist:</span>
                      <span className="font-mono text-emerald-400 font-bold">NO DIRECT HIT</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-slate-400">UN Consolidated:</span>
                      <span className="font-mono text-emerald-400 font-bold">CLEAR</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-slate-400">BFIU Schedule 1:</span>
                      <span className="font-mono text-amber-400 font-bold">MONITORED ENTITY</span>
                    </div>
                  </div>
                </div>
              )}

              {drawerTab === 'UBO' && (
                <div className="space-y-2 text-xs">
                  <div className="p-3 bg-canvas rounded-xl border border-line space-y-1.5 font-mono">
                    <div className="flex items-center justify-between text-slate-300">
                      <span>Tanvir Ahmed (Managing Director)</span>
                      <span className="text-emerald-400 font-bold">60%</span>
                    </div>
                    <div className="flex items-center justify-between text-slate-300">
                      <span>Gulf Star Holdings FZE (Offshore)</span>
                      <span className="text-amber-400 font-bold">35%</span>
                    </div>
                    <div className="flex items-center justify-between text-slate-300">
                      <span>Nominee Shareholder</span>
                      <span className="text-slate-400 font-bold">5%</span>
                    </div>
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              <div className="pt-3 border-t border-line space-y-2">
                <button
                  onClick={() => {
                    setFourEyesModalOpen(true, {
                      actionType: 'ACCOUNT_FREEZE',
                      actionTitle: `Emergency Administrative Account Freeze (${selectedNode.entityName})`,
                      targetId: selectedNode.id,
                      details: `Freeze account ${selectedNode.id} across RTGS/SWIFT rails pursuant to money laundering prevention powers.`
                    });
                  }}
                  className="w-full py-2 px-3 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-semibold text-xs flex items-center justify-center gap-1.5 cursor-pointer shadow-lg shadow-rose-600/20"
                >
                  <Lock className="w-3.5 h-3.5" />
                  <span>Freeze Account (4-Eyes)</span>
                </button>

                <button
                  onClick={() => router.push(`/cases/CASE-2026-0881`)}
                  className="w-full py-2 px-3 rounded-lg bg-surface hover:bg-surface-hover text-slate-200 font-medium text-xs flex items-center justify-center gap-1.5 cursor-pointer"
                >
                  <FileText className="w-3.5 h-3.5 text-sky-400" />
                  <span>Open Related Case Dossier</span>
                </button>
              </div>
            </div>
          ) : (
            <div className="py-20 text-center text-slate-500 text-xs">
              Select a node in the graph to inspect 360° compliance telemetry.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function ForensicGraphStudioPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center text-slate-400">Loading Forensic Cash Flow Studio...</div>}>
      <ForensicGraphStudioContent />
    </Suspense>
  );
}
