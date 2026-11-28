'use client';

import React, { useEffect, useRef, useState } from 'react';
import ForceGraph3D from '3d-force-graph';

export interface Graph3DNode {
  id: string;
  entityName: string;
  tier: number;
  riskScore?: number;
  [key: string]: unknown;
}

export interface Graph3DEdge {
  id: string;
  source: string;
  target: string;
  rail?: string;
  amount?: number;
  edgeTrustDelta?: number;
}

interface ForceGraph3DCanvasProps {
  nodes: Graph3DNode[];
  edges: Graph3DEdge[];
  onSelectNode: (node: Graph3DNode) => void;
  onFallbackTo2D: () => void;
}

export default function ForceGraph3DCanvas({
  nodes,
  edges,
  onSelectNode,
  onFallbackTo2D
}: ForceGraph3DCanvasProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [webglError, setWebglError] = useState<string | null>(null);
  const onSelectRef = useRef(onSelectNode);
  onSelectRef.current = onSelectNode;

  useEffect(() => {
    const container = containerRef.current;
    if (!container || typeof window === 'undefined') return;

    // Verify WebGL context availability before instantiating Three.js renderer
    try {
      const testCanvas = document.createElement('canvas');
      const gl = testCanvas.getContext('webgl') || testCanvas.getContext('experimental-webgl');
      if (!gl) {
        setWebglError('WebGL hardware acceleration unavailable in this viewport.');
        return;
      }
    } catch {
      setWebglError('WebGL initialization blocked by browser policy.');
      return;
    }

    let graph: any = null;
    let resizeObserver: ResizeObserver | null = null;
    let webglCanvas: HTMLCanvasElement | null = null;

    const handleContextLost = (e: Event) => {
      e.preventDefault();
      setWebglError('WebGL graphics context lost. Falling back to 2D canvas.');
    };

    try {
      const width = container.clientWidth || 720;
      const height = container.clientHeight || 480;

      const graphNodes = nodes.map((n) => ({
        ...n,
        name: n.entityName || n.id,
        color: n.tier === 1 ? '#F43F5E' : n.tier === 2 ? '#F59E0B' : '#10B981',
        val: n.tier === 1 ? 8 : n.tier === 2 ? 5 : 3
      }));

      const nodeIds = new Set(graphNodes.map((n) => n.id));
      const graphLinks = edges
        .filter((e) => nodeIds.has(e.source) && nodeIds.has(e.target))
        .map((e) => ({
          source: e.source,
          target: e.target,
          rail: e.rail || 'WIRE',
          delta: e.edgeTrustDelta ?? 0.5,
          color: (e.edgeTrustDelta ?? 0) > 0.85 ? '#F43F5E' : '#475569'
        }));

      const ForceGraphConstructor = ForceGraph3D as unknown as () => (el: HTMLElement) => any;
      graph = ForceGraphConstructor()(container)
        .width(width)
        .height(height)
        .backgroundColor('#090D14')
        .showNavInfo(false)
        .graphData({ nodes: graphNodes, links: graphLinks })
        .nodeLabel((node: any) => `${node.entityName || node.id} (Tier ${node.tier})`)
        .nodeColor((node: any) => node.color)
        .nodeVal((node: any) => node.val)
        .linkColor((link: any) => link.color)
        .linkWidth((link: any) => (link.delta > 0.85 ? 2.4 : 1.0))
        .linkDirectionalParticles(2)
        .linkDirectionalParticleSpeed(0.004)
        .onNodeClick((node: any) => {
          onSelectRef.current?.(node);
        });

      webglCanvas = container.querySelector('canvas');
      webglCanvas?.addEventListener('webglcontextlost', handleContextLost);

      resizeObserver = new ResizeObserver((entries) => {
        for (const entry of entries) {
          if (entry.contentRect.width > 0 && entry.contentRect.height > 0 && graph) {
            graph.width(entry.contentRect.width);
            graph.height(entry.contentRect.height);
          }
        }
      });
      resizeObserver.observe(container);
    } catch {
      setWebglError('3D WebGL renderer failed to mount cleanly.');
    }

    return () => {
      if (webglCanvas) {
        webglCanvas.removeEventListener('webglcontextlost', handleContextLost);
      }
      if (resizeObserver) {
        resizeObserver.disconnect();
      }
      if (graph) {
        try {
          graph.pauseAnimation?.();
          const renderer = graph.renderer?.();
          renderer?.dispose?.();
          graph._destructor?.();
        } catch {
          // Ignore teardown errors
        }
      }
      if (container) {
        container.innerHTML = '';
      }
    };
  }, [nodes, edges]);

  if (webglError) {
    return (
      <div className="w-full h-full flex flex-col items-center justify-center text-slate-300 space-y-3 p-6 text-center">
        <p className="text-xs font-mono text-amber-300">{webglError}</p>
        <button
          type="button"
          onClick={onFallbackTo2D}
          className="px-3.5 py-2 rounded-lg bg-surface-2 hover:bg-surface-2 border border-line-strong text-xs font-mono text-slate-100 cursor-pointer"
        >
          Switch to 2D Planar Canvas
        </button>
      </div>
    );
  }

  return <div ref={containerRef} className="w-full h-full" />;
}
