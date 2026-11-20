import type { Metadata } from 'next';
import { Inter, JetBrains_Mono } from 'next/font/google';
import './globals.css';
import { CommandHeader } from '@/components/shell/CommandHeader';
import { NavigationRail } from '@/components/shell/NavigationRail';
import { GlobalCommandPalette } from '@/components/shell/GlobalCommandPalette';
import { FourEyesApprovalModal } from '@/components/auth/FourEyesApprovalModal';
import { RoleSwitchModal } from '@/components/auth/RoleSwitchModal';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-jetbrains-mono',
});

export const metadata: Metadata = {
  title: 'Intelligent-AML | Institutional Compliance Operating System (V3.0)',
  description: 'Tier-1 Air-Gap-Ready Anti-Money Laundering & Conformal Risk Control Operating System for Central Banks & Enterprise Financial Institutions.',
  icons: {
    icon: '/favicon.ico',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`dark ${inter.variable} ${jetbrainsMono.variable} overflow-x-hidden w-full max-w-full`}>
      <body className="min-h-screen bg-[#0B0F17] text-slate-100 font-sans antialiased selection:bg-emerald-500/30 selection:text-emerald-200 overflow-x-hidden w-full max-w-full">
        {/* Top 56px Institutional Command Bar */}
        <CommandHeader />

        <div className="flex pt-14 min-h-[calc(100vh-3.5rem)]">
          {/* Collapsible Left Rail (240px / 64px) */}
          <NavigationRail />

          {/* Main Application Viewport */}
          <main className="flex-1 min-w-0 bg-[#0B0F17] text-slate-200 overflow-y-auto pb-16 md:pb-0">
            {children}
          </main>
        </div>

        {/* Global Institutional Modals & Palettes */}
        <GlobalCommandPalette />
        <FourEyesApprovalModal />
        <RoleSwitchModal />
      </body>
    </html>
  );
}
