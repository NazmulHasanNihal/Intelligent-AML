import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Model Ops, SR 11-7 & Tamper-Evident Ledger',
  description: 'Federal Reserve SR 11-7 model risk governance, PSI/KS drift monitoring, 7-day shadow replay, and Ed25519-signed WORM audit chain.',
  robots: {
    index: false,
    follow: false,
    noarchive: true,
  },
};

export default function GovernanceLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
