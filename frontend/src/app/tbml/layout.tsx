import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Trade-Based Money Laundering (TBML) Radar',
  description: 'Trade corridor price divergence analytics, dual-use goods detection, and BFIU TBML Guidelines compliance.',
  robots: {
    index: false,
    follow: false,
    noarchive: true,
  },
};

export default function TbmlLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
