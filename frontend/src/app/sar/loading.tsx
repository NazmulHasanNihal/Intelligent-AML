import React from 'react';

export default function SarLoading() {
  return (
    <div className="p-4 sm:p-6 space-y-6 animate-pulse" role="status" aria-label="Loading BFIU SAR & CTR Workbench">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#1E293B] pb-4">
        <div>
          <div className="h-6 w-72 bg-[#1E293B] rounded mb-2" />
          <div className="h-4 w-96 bg-[#1E293B]/60 rounded" />
        </div>
        <div className="flex items-center gap-2">
          <div className="h-8 w-32 bg-[#1E293B] rounded-lg" />
          <div className="h-8 w-44 bg-[#1E293B] rounded-lg" />
        </div>
      </div>

      {/* Tabs Skeleton */}
      <div className="flex items-center gap-2 border-b border-[#1E293B] pb-2">
        <div className="h-8 w-36 bg-[#1E293B] rounded-lg" />
        <div className="h-8 w-36 bg-[#1E293B]/60 rounded-lg" />
        <div className="h-8 w-36 bg-[#1E293B]/60 rounded-lg" />
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <div className="h-64 rounded-xl bg-[#0F172A] border border-[#1E293B] p-4 space-y-3">
            <div className="h-4 w-40 bg-[#1E293B] rounded" />
            <div className="h-10 w-full bg-[#1E293B]/70 rounded-lg" />
            <div className="h-10 w-full bg-[#1E293B]/70 rounded-lg" />
          </div>
          <div className="h-48 rounded-xl bg-[#0F172A] border border-[#1E293B] p-4 space-y-3">
            <div className="h-4 w-48 bg-[#1E293B] rounded" />
            <div className="h-8 w-full bg-[#1E293B]/50 rounded" />
          </div>
        </div>

        <div className="h-[450px] rounded-xl bg-[#0F172A] border border-[#1E293B] p-4 space-y-3">
          <div className="h-4 w-32 bg-[#1E293B] rounded" />
          <div className="h-full bg-[#0B0F17] rounded-lg border border-[#1E293B] flex items-center justify-center">
            <span className="text-xs font-mono text-slate-500">Compiling UNODC goAML v4.2 Schema...</span>
          </div>
        </div>
      </div>
    </div>
  );
}
