'use client';

import React from 'react';
import { usePathname } from 'next/navigation';
import { CommandHeader } from '@/components/shell/CommandHeader';
import { DemoDisclaimerBanner } from '@/components/shell/DemoDisclaimerBanner';
import { NavigationRail } from '@/components/shell/NavigationRail';
import { GlobalCommandPalette } from '@/components/shell/GlobalCommandPalette';
import { NotificationDrawer } from '@/components/shell/NotificationDrawer';
import { FourEyesApprovalModal } from '@/components/auth/FourEyesApprovalModal';
import { RoleSwitchModal } from '@/components/auth/RoleSwitchModal';

export function AppShellWrapper({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isMarketing = pathname === '/' || pathname.startsWith('/terms') || pathname.startsWith('/privacy');

  if (isMarketing) {
    return <main className="min-h-screen bg-[#070B12] text-slate-100">{children}</main>;
  }

  return (
    <>
      {/* Fixed Top Container: Disclaimer Banner & Command Header */}
      <div className="fixed top-0 left-0 right-0 z-40 bg-[#0F172A]/95 backdrop-blur-md">
        <DemoDisclaimerBanner />
        <CommandHeader />
      </div>

      <div className="flex pt-[5.25rem] min-h-[calc(100vh-5.25rem)]">
        {/* Collapsible Left Rail */}
        <NavigationRail />

        {/* Main Application Viewport */}
        <main className="flex-1 min-w-0 bg-[#0B0F17] text-slate-200 overflow-y-auto pb-16 md:pb-0">
          {children}
        </main>
      </div>

      {/* Global Institutional Modals, Drawers & Palettes */}
      <GlobalCommandPalette />
      <NotificationDrawer />
      <FourEyesApprovalModal />
      <RoleSwitchModal />
    </>
  );
}
