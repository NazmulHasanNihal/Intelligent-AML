'use client';

import React from 'react';
import { AlertCircle, ShieldCheck } from 'lucide-react';
import { IS_DEMO_MODE, IS_ONPREM_MODE } from '@/lib/config/env';

export const DemoDisclaimerBanner: React.FC = () => {
  if (IS_ONPREM_MODE) {
    return (
      <aside aria-label="Security Status" className="w-full bg-cyan-950/40 border-b border-cyan-800/40 px-3 sm:px-4 py-1 text-center text-[11px] font-mono text-cyan-300 flex items-center justify-center gap-2 select-none z-50">
        <ShieldCheck className="w-3.5 h-3.5 text-cyan-400 shrink-0" aria-hidden="true" />
        <span>
          <strong>ON-PREM DEPLOYMENT:</strong> Local Network Air-Gap Mode Active • External Egress Restricted
        </span>
      </aside>
    );
  }

  return (
    <aside aria-label="System Notice" className="w-full bg-amber-950/60 border-b border-amber-600/40 px-3 sm:px-4 py-1 text-center text-[11px] font-mono text-amber-200 flex items-center justify-center gap-2 select-none z-50">
      <AlertCircle className="w-3.5 h-3.5 text-amber-400 shrink-0" aria-hidden="true" />
      <span>
        <strong>DEMONSTRATION PROTOTYPE:</strong> Synthetic demo data, not connected to any institution. Simulated compliance workflows for evaluation.
      </span>
    </aside>
  );
};
