import React from 'react';

export default function GraphLoading() {
  return (
    <div className="p-4 sm:p-6 space-y-6 animate-pulse" role="status" aria-label="Loading Forensic Cash Flow Graph">
      {/* Top Header Skeleton */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-line pb-4">
        <div>
          <div className="h-6 w-64 bg-surface rounded mb-2" />
          <div className="h-4 w-96 bg-surface/60 rounded" />
        </div>
        <div className="flex items-center gap-2">
          <div className="h-8 w-24 bg-surface rounded-lg" />
          <div className="h-8 w-32 bg-surface rounded-lg" />
        </div>
      </div>

      {/* Main Canvas & Controls Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Graph Canvas Skeleton */}
        <div className="lg:col-span-3 h-[600px] rounded-xl bg-panel border border-line flex flex-col items-center justify-center p-6 relative overflow-hidden">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-emerald-950/10 via-transparent to-transparent" />
          <div className="w-16 h-16 rounded-full border-2 border-emerald-500/30 border-t-emerald-400 animate-spin mb-4" />
          <span className="text-xs font-mono font-bold text-fg-secondary">
            Synthesizing Spatio-Temporal Graph Subgraph...
          </span>
          <span className="text-xs font-mono text-fg0 mt-1">
            Computing 12 topological invariants &amp; WebGL nodes
          </span>
        </div>

        {/* Sidebar Controls Skeleton */}
        <div className="space-y-4">
          <div className="h-44 rounded-xl bg-panel border border-line p-4 space-y-3">
            <div className="h-4 w-28 bg-surface rounded" />
            <div className="h-3 w-full bg-surface/60 rounded" />
            <div className="h-3 w-3/4 bg-surface/60 rounded" />
          </div>
          <div className="h-56 rounded-xl bg-panel border border-line p-4 space-y-3">
            <div className="h-4 w-32 bg-surface rounded" />
            <div className="h-8 w-full bg-surface/80 rounded" />
            <div className="h-8 w-full bg-surface/80 rounded" />
          </div>
        </div>
      </div>
    </div>
  );
}
