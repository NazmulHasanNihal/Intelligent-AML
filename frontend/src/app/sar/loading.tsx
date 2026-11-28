import React from 'react';

export default function SarLoading() {
  return (
    <div className="p-4 sm:p-6 space-y-6 animate-pulse" role="status" aria-label="Loading BFIU SAR & CTR Workbench">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-line pb-4">
        <div>
          <div className="h-6 w-72 bg-surface rounded mb-2" />
          <div className="h-4 w-96 bg-surface/60 rounded" />
        </div>
        <div className="flex items-center gap-2">
          <div className="h-8 w-32 bg-surface rounded-lg" />
          <div className="h-8 w-44 bg-surface rounded-lg" />
        </div>
      </div>

      {/* Tabs Skeleton */}
      <div className="flex items-center gap-2 border-b border-line pb-2">
        <div className="h-8 w-36 bg-surface rounded-lg" />
        <div className="h-8 w-36 bg-surface/60 rounded-lg" />
        <div className="h-8 w-36 bg-surface/60 rounded-lg" />
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <div className="h-64 rounded-xl bg-panel border border-line p-4 space-y-3">
            <div className="h-4 w-40 bg-surface rounded" />
            <div className="h-10 w-full bg-surface/70 rounded-lg" />
            <div className="h-10 w-full bg-surface/70 rounded-lg" />
          </div>
          <div className="h-48 rounded-xl bg-panel border border-line p-4 space-y-3">
            <div className="h-4 w-48 bg-surface rounded" />
            <div className="h-8 w-full bg-surface/50 rounded" />
          </div>
        </div>

        <div className="h-[450px] rounded-xl bg-panel border border-line p-4 space-y-3">
          <div className="h-4 w-32 bg-surface rounded" />
          <div className="h-full bg-canvas rounded-lg border border-line flex items-center justify-center">
            <span className="text-xs font-mono text-slate-500">Compiling UNODC goAML v4.2 Schema...</span>
          </div>
        </div>
      </div>
    </div>
  );
}
