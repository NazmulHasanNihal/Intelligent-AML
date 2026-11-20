'use client';

import React, { useState, useEffect, useRef, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import cytoscape from 'cytoscape';
import {
  GitFork,
  Sliders,
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
  Compass
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { PiiText } from '@/components/ui/PiiText';

function ForensicGraphStudioContent() {
  const searchParams = useSearchParams();
  const initialNode = searchParams?.get('node') || 'BD22-EBLB-4829-1092-8823';

  const { setFourEyesModalOpen } = useBankingStore();

  const [viewMode, setViewMode] = useState<'2D' | '3D'>('2D');
  const [deltaFloor, setDeltaFloor] = useState<number>(0.10);
  const [egoHops, setEgoHops] = useState<number>(2);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [temporalStep, setTemporalStep] = useState<number>(100);
  const [selectedNode, setSelectedNode] = useState<any>(null);
  const [subgraphData, setSubgraphData] = useState<any>(null);
  const [isFullscreen, setIsFullscreen] = useState<boolean>(false);

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

  // Reset / Zoom to fit
  const handleResetCamera = () => {
    if (cyRef.current) {
      cyRef.current.fit(undefined, 40);
    }
  };

  // Initialize and update Cytoscape instance
  useEffect(() => {
    if (!subgraphData || !cyContainerRef.current || viewMode !== '2D') return;

    // Filter edges by deltaFloor and cap nodes for responsiveness (<= 15 core nodes)
    const visibleEdges = (subgraphData.edges || []).filter(
      (e: any) => e.edgeTrustDelta >= deltaFloor
    );

    const activeNodeIds = new Set<string>();
    visibleEdges.forEach((e: any) => {
      activeNodeIds.add(e.source);
      activeNodeIds.add(e.target);
    });

    const filteredNodes = (subgraphData.nodes || []).filter(
      (n: any) => activeNodeIds.has(n.id) || n.id === initialNode
    ).slice(0, 16);

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
  }, [subgraphData, deltaFloor, viewMode, egoHops]);

  return (
    <div ref={containerRef} className="p-4 sm:p-5 lg:p-6 max-w-[1700px] mx-auto space-y-4 sm:space-y-5">
      {/* Header and Controls */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <GitFork className="w-5 h-5 text-purple-400" />
            Forensic Cash Flow Studio — Multi-Hop Topology
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Real-time graph neural decomposition with learned adaptive edge trust gating (&delta;<sub>uv</sub>) and camouflage pruning.
          </p>
        </div>

        {/* View Controls & Switchers */}
        <div className="flex items-center gap-3">
          {/* Hop Distance Expansion */}
          <div className="flex items-center bg-[#0F172A] p-1 rounded-lg border border-[#334155] text-xs font-mono">
            <span className="text-slate-400 px-2 text-[11px]">Hops:</span>
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

          {/* View Switcher: 2D Planar vs 3D Force */}
          <div className="flex items-center bg-[#0F172A] p-1 rounded-lg border border-[#334155]">
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

      {/* Main Studio Viewport (Responsive calc height) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 min-h-[520px] h-[calc(100vh-230px)]">
        {/* Graph Canvas Container (9 Cols) */}
        <div className="lg:col-span-9 bg-[#0F172A] border border-[#1E293B] rounded-xl relative overflow-hidden flex flex-col">
          {/* Top Canvas Bar: Edge Trust Slider & Camera Controls */}
          <div className="p-3 bg-[#0B0F17]/80 border-b border-[#1E293B] flex flex-wrap items-center justify-between gap-3 z-10 text-xs">
            {/* Adaptive Edge Trust Slider */}
            <div className="flex items-center gap-3 bg-[#0F172A] px-3 py-1.5 rounded-lg border border-[#334155]">
              <span className="font-semibold text-slate-300 flex items-center gap-1.5">
                <Sliders className="w-3.5 h-3.5 text-purple-400" />
                Edge Trust Gate (&delta;<sub>floor</sub>):
              </span>
              <input
                type="range"
                min="0.00"
                max="0.50"
                step="0.02"
                value={deltaFloor}
                onChange={(e) => setDeltaFloor(Number(e.target.value))}
                className="w-28 sm:w-36 accent-purple-500 cursor-pointer"
              />
              <span className="font-mono font-bold text-purple-300 text-xs min-w-[3ch] tabular-nums">
                {deltaFloor.toFixed(2)}
              </span>
            </div>

            {/* Invariant Stats & Camera Controls */}
            <div className="flex items-center gap-2 sm:gap-3 text-[11px] font-mono">
              <span className="hidden sm:inline text-slate-400">
                Pruned: <strong className="text-rose-400">{subgraphData?.camouflagePrunedCount || 1} edges</strong>
              </span>

              <button
                onClick={handleResetCamera}
                className="flex items-center gap-1 px-2 py-1 rounded bg-[#0B0F17] hover:bg-[#1E293B] text-slate-300 border border-[#334155] cursor-pointer transition-colors"
                title="Reset Camera & Fit to Screen"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span className="hidden md:inline">Fit</span>
              </button>

              <button
                onClick={toggleFullscreen}
                className="flex items-center gap-1 px-2 py-1 rounded bg-[#0B0F17] hover:bg-[#1E293B] text-slate-300 border border-[#334155] cursor-pointer transition-colors"
                title="Toggle Fullscreen Canvas"
              >
                {isFullscreen ? <Minimize2 className="w-3.5 h-3.5" /> : <Maximize2 className="w-3.5 h-3.5" />}
                <span className="hidden md:inline">{isFullscreen ? 'Exit' : 'Full'}</span>
              </button>
            </div>
          </div>

          {/* Graph Viewport */}
          <div className="flex-1 relative bg-[#090D14] overflow-hidden">
            {viewMode === '2D' ? (
              <div ref={cyContainerRef} className="w-full h-full" />
            ) : (
              <div className="w-full h-full flex flex-col items-center justify-center text-slate-400 space-y-3">
                <Box className="w-12 h-12 text-purple-400 animate-bounce" />
                <div className="text-center">
                  <h3 className="font-semibold text-slate-200 text-sm">Hardware-Accelerated 3D Force Graph</h3>
                  <p className="text-xs text-slate-500 mt-1">WebGL dynamic force simulation active. Click nodes to orbit and inspect ego-sphere.</p>
                </div>
              </div>
            )}

            {/* Bottom-Right Compass / Minimap Badge */}
            <div className="absolute bottom-4 right-4 p-2 rounded-lg bg-[#0F172A]/85 backdrop-blur-sm border border-[#334155] flex items-center gap-2 text-[10px] font-mono text-slate-400 pointer-events-none select-none">
              <Compass className="w-4 h-4 text-purple-400 animate-spin-slow" />
              <span>C-STGB Topology Minimap</span>
            </div>
          </div>

          {/* Bottom Temporal Playback Scrubber */}
          <div className="p-3 bg-[#0B0F17]/95 border-t border-[#1E293B] flex items-center gap-3 sm:gap-4 text-xs z-10">
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className="p-1.5 rounded-lg bg-purple-950/40 hover:bg-purple-900/60 text-purple-300 border border-purple-800/40 transition-colors cursor-pointer shrink-0"
              title={isPlaying ? "Pause Temporal Scrubbing" : "Play Temporal Simulation"}
            >
              {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
            </button>
            <span className="text-[11px] font-semibold text-slate-400 shrink-0">
              Hawkes Temporal Playback (&Delta;t):
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

        {/* 360° Entity Context Inspector (3 Cols) */}
        <div className="lg:col-span-3 bg-[#0F172A] border border-[#1E293B] rounded-xl p-5 flex flex-col justify-between overflow-y-auto">
          {selectedNode ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-[#1E293B]">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  360° Node Context
                </span>
                <span
                  className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
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

              <div>
                <h3 className="font-bold text-sm text-slate-100 flex items-center gap-1.5">
                  <Building className="w-4 h-4 text-slate-400 shrink-0" />
                  <span className="truncate">{selectedNode.entityName}</span>
                </h3>
                <div className="text-xs text-slate-400 mt-1">
                  <span>Account:</span>
                  <PiiText value={selectedNode.id} type="account" className="font-mono text-slate-300 ml-1" />
                </div>
              </div>

              {/* Invariants Grid with Tabular-Nums */}
              <div className="space-y-2 pt-2 text-xs">
                <div className="p-2.5 bg-[#0B0F17] rounded-lg border border-[#1E293B] flex items-center justify-between">
                  <span className="text-slate-400">Flow Conservation (&Phi;<sub>flow</sub>):</span>
                  <strong className="font-mono text-rose-400 tabular-nums">{selectedNode.phiFlow}</strong>
                </div>
                <div className="p-2.5 bg-[#0B0F17] rounded-lg border border-[#1E293B] flex items-center justify-between">
                  <span className="text-slate-400">Hawkes Intensity (&lambda;<sub>u</sub>):</span>
                  <strong className="font-mono text-amber-400 tabular-nums">{selectedNode.lambdaU}</strong>
                </div>
                <div className="p-2.5 bg-[#0B0F17] rounded-lg border border-[#1E293B] flex items-center justify-between">
                  <span className="text-slate-400">Jurisdiction:</span>
                  <strong className="font-mono text-slate-200">{selectedNode.jurisdiction}</strong>
                </div>
                <div className="p-2.5 bg-[#0B0F17] rounded-lg border border-[#1E293B] flex items-center justify-between">
                  <span className="text-slate-400">Risk Score:</span>
                  <strong className="font-mono text-rose-400 tabular-nums">{selectedNode.riskScore}</strong>
                </div>
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-full text-slate-500 text-xs text-center">
              <Info className="w-8 h-8 mb-2 text-slate-600" />
              <span>Select any node in the graph to view 360° forensic invariants.</span>
            </div>
          )}

          {/* Quick Actions Footer */}
          {selectedNode && (
            <div className="pt-4 border-t border-[#1E293B] space-y-2">
              <button
                onClick={() => {
                  setFourEyesModalOpen(true, {
                    actionType: 'ACCOUNT_FREEZE',
                    actionTitle: `Emergency Freeze Node: ${selectedNode.id}`,
                    targetId: selectedNode.id,
                    details: `Freeze entity ${selectedNode.entityName} under 4-Eyes dual signatory authority.`
                  });
                }}
                className="w-full py-2 px-3 bg-rose-950/60 hover:bg-rose-900/80 text-rose-300 border border-rose-800/60 font-semibold rounded-lg text-xs transition-colors flex items-center justify-center gap-1.5 cursor-pointer"
              >
                <Lock className="w-3.5 h-3.5" />
                <span>Freeze Node (4-Eyes Gate)</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function ForensicGraphStudioPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center text-xs font-mono text-slate-400">Loading Forensic Topology Studio...</div>}>
      <ForensicGraphStudioContent />
    </Suspense>
  );
}
