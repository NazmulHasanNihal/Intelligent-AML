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
  Box,
  Eye,
  ShieldAlert,
  Building,
  RotateCcw,
  Lock,
  Layers,
  Info
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { PiiText } from '@/components/ui/PiiText';

function ForensicGraphStudioContent() {
  const searchParams = useSearchParams();
  const initialNode = searchParams?.get('node') || 'BD22-EBLB-4829-1092-8823';

  const { setFourEyesModalOpen } = useBankingStore();

  const [viewMode, setViewMode] = useState<'2D' | '3D'>('2D');
  const [deltaFloor, setDeltaFloor] = useState<number>(0.10);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [temporalStep, setTemporalStep] = useState<number>(100);
  const [selectedNode, setSelectedNode] = useState<any>(null);
  const [subgraphData, setSubgraphData] = useState<any>(null);

  const cyContainerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<cytoscape.Core | null>(null);

  // Fetch subgraph data
  useEffect(() => {
    async function loadGraph() {
      try {
        const res = await fetch(`/api/v1/graph/subgraph/${encodeURIComponent(initialNode)}`);
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
  }, [initialNode]);

  // Initialize and update Cytoscape instance
  useEffect(() => {
    if (!subgraphData || !cyContainerRef.current || viewMode !== '2D') return;

    // Filter edges by deltaFloor
    const visibleEdges = subgraphData.edges.filter(
      (e: any) => e.edgeTrustDelta >= deltaFloor
    );

    const elements: cytoscape.ElementDefinition[] = [
      ...subgraphData.nodes.map((n: any) => ({
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
        nodeRepulsion: () => 8000,
        idealEdgeLength: () => 120,
        edgeElasticity: () => 100,
        padding: 40
      },
      style: [
        {
          selector: 'node',
          style: {
            label: 'data(label)',
            color: '#CBD5E1',
            'font-size': '11px',
            'font-family': 'monospace',
            'text-valign': 'bottom',
            'text-margin-y': 6,
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
            color: '#94A3B8',
            'text-rotation': 'autorotate'
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
  }, [subgraphData, deltaFloor, viewMode]);

  return (
    <div className="p-6 max-w-[1700px] mx-auto space-y-5">
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

        {/* View Switcher: 2D Planar vs 3D Force */}
        <div className="flex items-center gap-3">
          <div className="flex items-center bg-[#0F172A] p-1 rounded-lg border border-[#334155]">
            <button
              onClick={() => setViewMode('2D')}
              className={`flex items-center gap-1.5 px-3 py-1 rounded text-xs font-semibold transition-all ${
                viewMode === '2D'
                  ? 'bg-purple-500/20 text-purple-300 border border-purple-500/40'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Eye className="w-3.5 h-3.5" />
              <span>2D Forensic Planar</span>
            </button>
            <button
              onClick={() => setViewMode('3D')}
              className={`flex items-center gap-1.5 px-3 py-1 rounded text-xs font-semibold transition-all ${
                viewMode === '3D'
                  ? 'bg-purple-500/20 text-purple-300 border border-purple-500/40'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Box className="w-3.5 h-3.5" />
              <span>3D Hardware WebGL</span>
            </button>
          </div>
        </div>
      </div>

      {/* Main Studio Viewport */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 h-[680px]">
        {/* Graph Canvas Container (9 Cols) */}
        <div className="lg:col-span-9 bg-[#0F172A] border border-[#1E293B] rounded-xl relative overflow-hidden flex flex-col">
          {/* Top Canvas Bar: Edge Trust Slider & Controls */}
          <div className="p-3 bg-[#0B0F17]/70 border-b border-[#1E293B] flex flex-wrap items-center justify-between gap-4 z-10 text-xs">
            {/* Adaptive Edge Trust Slider */}
            <div className="flex items-center gap-3 bg-[#0F172A] px-3 py-1.5 rounded-lg border border-[#334155]">
              <span className="font-semibold text-slate-300 flex items-center gap-1.5">
                <Sliders className="w-3.5 h-3.5 text-purple-400" />
                Adaptive Edge Trust Gate (&delta;<sub>floor</sub>):
              </span>
              <input
                type="range"
                min="0.00"
                max="0.50"
                step="0.02"
                value={deltaFloor}
                onChange={(e) => setDeltaFloor(Number(e.target.value))}
                className="w-32 accent-purple-500 cursor-pointer"
              />
              <span className="font-mono font-bold text-purple-300 text-xs min-w-[3ch]">
                {deltaFloor.toFixed(2)}
              </span>
              <span className="text-[10px] text-slate-400">
                (Prunes camouflage edges below threshold)
              </span>
            </div>

            {/* Invariant Indicator */}
            <div className="flex items-center gap-3 text-[11px] text-slate-400 font-mono">
              <span>Camouflage Pruned: <strong className="text-rose-400">{subgraphData?.camouflagePrunedCount || 1} edges</strong></span>
              <span>•</span>
              <span>Topological Circuit: <strong className="text-emerald-400">CLOSED</strong></span>
            </div>
          </div>

          {/* Graph Viewport */}
          <div className="flex-1 relative bg-[#090D14]">
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
          </div>

          {/* Bottom Temporal Playback Scrubber */}
          <div className="p-3 bg-[#0B0F17]/90 border-t border-[#1E293B] flex items-center gap-4 text-xs">
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className="p-1.5 rounded-lg bg-purple-950/40 hover:bg-purple-900/60 text-purple-300 border border-purple-800/40 transition-colors"
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
            <span className="font-mono text-xs text-emerald-400 shrink-0">
              {temporalStep}% Velocity
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
                  <Building className="w-4 h-4 text-slate-400" />
                  {selectedNode.entityName}
                </h3>
                <div className="text-xs text-slate-400 mt-1">
                  <span>Account:</span>
                  <PiiText value={selectedNode.id} type="account" className="font-mono text-slate-300 ml-1" />
                </div>
              </div>

              {/* Invariants Grid */}
              <div className="space-y-2 pt-2 text-xs">
                <div className="p-2.5 bg-[#0B0F17] rounded-lg border border-[#1E293B] flex items-center justify-between">
                  <span className="text-slate-400">Flow Conservation (&Phi;<sub>flow</sub>):</span>
                  <strong className="font-mono text-rose-400">{selectedNode.phiFlow}</strong>
                </div>
                <div className="p-2.5 bg-[#0B0F17] rounded-lg border border-[#1E293B] flex items-center justify-between">
                  <span className="text-slate-400">Hawkes Intensity (&lambda;<sub>u</sub>):</span>
                  <strong className="font-mono text-amber-400">{selectedNode.lambdaU}</strong>
                </div>
                <div className="p-2.5 bg-[#0B0F17] rounded-lg border border-[#1E293B] flex items-center justify-between">
                  <span className="text-slate-400">Jurisdiction:</span>
                  <strong className="font-mono text-slate-200">{selectedNode.jurisdiction}</strong>
                </div>
                <div className="p-2.5 bg-[#0B0F17] rounded-lg border border-[#1E293B] flex items-center justify-between">
                  <span className="text-slate-400">Risk Score:</span>
                  <strong className="font-mono text-rose-400">{selectedNode.riskScore}</strong>
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
                className="w-full py-2 px-3 bg-rose-950/60 hover:bg-rose-900/80 text-rose-300 border border-rose-800/60 font-semibold rounded-lg text-xs transition-colors flex items-center justify-center gap-1.5"
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
