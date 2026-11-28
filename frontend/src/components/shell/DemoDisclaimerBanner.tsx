'use client';

import React from 'react';
import { AlertCircle, ShieldCheck } from 'lucide-react';
import { IS_DEMO_MODE, IS_ONPREM_MODE } from '@/lib/config/env';

export const DemoDisclaimerBanner: React.FC = () => {
  if (IS_ONPREM_MODE) {
    return (
      <aside aria-label="Security Status" className="w-full bg-[#090F16] border-b border-[#1E2734] px-3 sm:px-4 py-1 text-center text-[11px] font-mono text-cyan-300 flex items-center justify-center gap-2 select-none z-50">
        <ShieldCheck className="w-3.5 h-3.5 text-cyan-400 shrink-0" aria-hidden="true" />
        <span>
          On-Premises Node · Local Network Confined
        </span>
      </aside>
    );
  }

  return (
    <aside aria-label="System Notice" className="w-full bg-[#0D1119] border-b border-[#1E2734] px-3 sm:px-4 py-1 text-center text-[11px] font-mono text-slate-400 flex items-center justify-center gap-2 select-none z-50">
      <AlertCircle className="w-3.5 h-3.5 text-amber-400 shrink-0" aria-hidden="true" />
      <span>
        Evaluation Sandbox · Synthetic institutional telemetry (not connected to live bank accounts)
      </span>
    </aside>
  );
};
