'use client';

import React, { useEffect } from 'react';
import { AlertTriangle, RefreshCw, Layers } from 'lucide-react';

export default function GraphError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error('Forensic Cash Flow WebGL/Cytoscape Error:', error);
  }, [error]);

  return (
    <div className="p-6 sm:p-12 max-w-3xl mx-auto my-8">
      <div className="p-8 rounded-2xl bg-panel border border-rose-500/40 shadow-2xl text-slate-100 text-center">
        <div className="w-14 h-14 rounded-2xl bg-rose-500/10 text-rose-400 flex items-center justify-center mx-auto mb-4 border border-rose-500/30">
          <AlertTriangle className="w-7 h-7" />
        </div>
        <h2 className="text-lg font-bold text-slate-100 mb-1">
          Forensic Graph Visualization Error
        </h2>
        <p className="text-xs text-slate-400 font-sans max-w-md mx-auto mb-4">
          The 3D WebGL / Cytoscape topology engine encountered a rendering or context-loss exception.
        </p>

        <div className="p-3 rounded-lg bg-canvas border border-line font-mono text-left text-xs text-rose-300 mb-6 max-h-36 overflow-y-auto break-all">
          <p className="font-bold text-slate-400 mb-1">Exception Receipt:</p>
          <p>{error.message || 'WebGL Context Lost or Shading Pipeline Interrupted'}</p>
          {error.digest && <p className="text-xs text-slate-500 mt-1">Digest: {error.digest}</p>}
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
          <button
            type="button"
            onClick={() => reset()}
            className="w-full sm:w-auto px-5 py-2.5 rounded-lg text-xs font-mono font-bold bg-emerald-500 hover:bg-emerald-400 text-slate-950 transition-all flex items-center justify-center gap-2 cursor-pointer shadow-md shadow-emerald-500/20"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Re-initialize Graph Canvas</span>
          </button>
          <button
            type="button"
            onClick={() => window.location.reload()}
            className="w-full sm:w-auto px-4 py-2.5 rounded-lg text-xs font-mono font-semibold bg-surface hover:bg-surface-hover text-slate-300 border border-line-strong transition-all cursor-pointer"
          >
            Hard Reload Module
          </button>
        </div>
      </div>
    </div>
  );
}
