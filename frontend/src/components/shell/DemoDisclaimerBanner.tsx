'use client';

import React from 'react';
import { IS_ONPREM_MODE } from '@/lib/config/env';

/** One quiet line. The full wording lives on the landing page and in the model card. */
export const DemoDisclaimerBanner: React.FC = () => (
  <aside
    aria-label="System notice"
    className="flex h-7 w-full select-none items-center justify-center border-b border-amber-500/20 bg-amber-500/[0.07] px-3 text-center text-xs text-amber-200/90"
  >
    {IS_ONPREM_MODE
      ? 'On-prem deployment · local network only'
      : 'Demonstration environment · synthetic data, not connected to any institution'}
  </aside>
);
