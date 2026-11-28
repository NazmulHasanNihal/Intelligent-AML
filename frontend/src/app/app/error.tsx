'use client';

import React, { useEffect } from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

export default function AppError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error('Surveillance Dashboard Exception:', error);
  }, [error]);

  return (
    <div className="p-6 sm:p-12 max-w-3xl mx-auto my-8">
      <div className="p-8 rounded-2xl bg-[#0F172A] border border-rose-500/40 shadow-2xl text-slate-100 text-center">
        <div className="w-14 h-14 rounded-2xl bg-rose-500/10 text-rose-400 flex items-center justify-center mx-auto mb-4 border border-rose-500/30">
          <AlertTriangle className="w-7 h-7" />
        </div>
        <h2 className="text-lg font-bold text-slate-100 mb-1">
          Surveillance Operating System Exception
        </h2>
        <p className="text-xs text-slate-400 font-sans max-w-md mx-auto mb-4">
          An unhandled error occurred while rendering the executive surveillance dashboard.
        </p>

        <div className="p-3 rounded-lg bg-[#070B12] border border-[#1E293B] font-mono text-left text-xs text-rose-300 mb-6 max-h-36 overflow-y-auto break-all">
          <p className="font-bold text-slate-400 mb-1">Stack Trace Receipt:</p>
          <p>{error.message || 'Fatal Dashboard Rendering Exception'}</p>
          {error.digest && <p className="text-xs text-slate-500 mt-1">Digest: {error.digest}</p>}
        </div>

        <button
          type="button"
          onClick={() => reset()}
          className="px-5 py-2.5 rounded-lg text-xs font-mono font-bold bg-emerald-500 hover:bg-emerald-400 text-slate-950 transition-all flex items-center justify-center gap-2 cursor-pointer shadow-md shadow-emerald-500/20 mx-auto"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Reload Dashboard</span>
        </button>
      </div>
    </div>
  );
}
