'use client';

import React, { useEffect, useState } from 'react';
import { IS_ONPREM_MODE } from '@/lib/config/env';

function isPrivateHost(host: string): boolean {
  if (!host) return false;
  if (host === 'localhost' || host === '127.0.0.1' || host === '::1') return true;
  if (host.startsWith('10.') || host.startsWith('192.168.') || host.endsWith('.local') || host.endsWith('.internal')) {
    return true;
  }
  return /^172\.(1[6-9]|2\d|3[01])\./.test(host);
}

export function getDeploymentBadgeText(hostname?: string): string {
  if (IS_ONPREM_MODE || (hostname && isPrivateHost(hostname))) {
    return 'DEPLOYMENT: AIR-GAP INTRANET NODE';
  }
  return 'DEPLOYMENT: CLOUD SANDBOX (AIR-GAP READY)';
}

/** Concise institutional environment banner matching active host posture. */
export const DemoDisclaimerBanner: React.FC = () => {
  const [hostname, setHostname] = useState<string>('');

  useEffect(() => {
    setHostname(window.location.hostname);
  }, []);

  const isLocalOrOnPrem = IS_ONPREM_MODE || isPrivateHost(hostname);
  const label = getDeploymentBadgeText(hostname);

  return (
    <aside
      aria-label="System notice"
      className="flex min-h-7 w-full select-none items-center justify-center border-b border-tier-2-border bg-tier-2-bg px-3 py-0.5 text-center text-xs font-medium text-tier-2-text"
    >
      <span>
        {label}
        {!isLocalOrOnPrem && ' · Synthetic data, not connected to any institution'}
      </span>
    </aside>
  );
};
