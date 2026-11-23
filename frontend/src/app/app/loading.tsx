import React from 'react';

export default function AppLoading() {
  return (
    <div className="p-4 sm:p-6 space-y-6 animate-pulse" role="status" aria-label="Loading Surveillance Overview">
      {/* Top Header Skeleton */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#1E293B] pb-4">
        <div>
          <div className="h-6 w-80 bg-[#1E293B] rounded mb-2" />
          <div className="h-4 w-96 bg-[#1E293B]/60 rounded" />
        </div>
        <div className="flex items-center gap-2">
          <div className="h-8 w-28 bg-[#1E293B] rounded-lg" />
          <div className="h-8 w-36 bg-[#1E293B] rounded-lg" />
        </div>
      </div>

      {/* 4 KPI Cards Skeleton */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-28 rounded-xl bg-[#0F172A] border border-[#1E293B] p-4 space-y-3">
            <div className="h-3 w-24 bg-[#1E293B] rounded" />
            <div className="h-7 w-20 bg-[#1E293B] rounded" />
            <div className="h-3 w-32 bg-[#1E293B]/60 rounded" />
          </div>
        ))}
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 h-96 rounded-xl bg-[#0F172A] border border-[#1E293B] p-4 space-y-4">
          <div className="h-4 w-48 bg-[#1E293B] rounded" />
          <div className="space-y-2">
            {[1, 2, 3, 4, 5].map((i) => (
              <div key={i} className="h-12 w-full bg-[#1E293B]/40 rounded-lg" />
            ))}
          </div>
        </div>

        <div className="h-96 rounded-xl bg-[#0F172A] border border-[#1E293B] p-4 space-y-4">
          <div className="h-4 w-36 bg-[#1E293B] rounded" />
          <div className="h-64 w-full bg-[#0B0F17] rounded-lg border border-[#1E293B] flex items-center justify-center">
            <span className="text-xs font-mono text-slate-500">Connecting to Stream...</span>
          </div>
        </div>
      </div>
    </div>
  );
}
