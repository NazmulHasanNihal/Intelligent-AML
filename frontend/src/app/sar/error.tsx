'use client';

import React, { useEffect } from 'react';
import { AlertTriangle, RefreshCw, FileText } from 'lucide-react';

export default function SarError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error('BFIU goAML STR/CTR Workbench Error:', error);
  }, [error]);

  return (
    <div className="p-6 sm:p-12 max-w-3xl mx-auto my-8">
      <div className="p-8 rounded-2xl bg-panel border border-rose-500/40 shadow-2xl text-fg text-center">
        <div className="w-14 h-14 rounded-2xl bg-rose-500/10 text-tier-1-text flex items-center justify-center mx-auto mb-4 border border-rose-500/30">
          <FileText className="w-7 h-7" />
        </div>
        <h2 className="text-lg font-bold text-fg mb-1">
          BFIU goAML XML Workbench Error
        </h2>
        <p className="text-xs text-muted font-sans max-w-md mx-auto mb-4">
          An error occurred while compiling XML nodes, verifying supporting attachments, or calculating SHA-256 seals.
        </p>

        <div className="p-3 rounded-lg bg-canvas border border-line font-mono text-left text-xs text-tier-1-text mb-6 max-h-36 overflow-y-auto break-all">
          <p className="font-bold text-muted mb-1">Error Diagnostic:</p>
          <p>{error.message || 'UNODC Schema Serialization Exception'}</p>
          {error.digest && <p className="text-xs text-fg0 mt-1">Digest: {error.digest}</p>}
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
          <button
            type="button"
            onClick={() => reset()}
            className="w-full sm:w-auto px-5 py-2.5 rounded-lg text-xs font-mono font-bold bg-emerald-500 hover:bg-emerald-400 text-slate-950 transition-all flex items-center justify-center gap-2 cursor-pointer shadow-md shadow-emerald-500/20"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Rebuild Docket State</span>
          </button>
        </div>
      </div>
    </div>
  );
}
