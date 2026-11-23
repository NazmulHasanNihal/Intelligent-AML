import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Sanctions, PEP & Entity Resolution',
  description: 'Multi-algorithm entity screening across OFAC SDN, UN Consolidated, EU, UK, and Bangladesh domestic watchlists.',
  robots: {
    index: false,
    follow: false,
    noarchive: true,
  },
};

export default function ScreeningLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
