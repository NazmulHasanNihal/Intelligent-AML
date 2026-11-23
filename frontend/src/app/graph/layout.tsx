import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Forensic Cash Flow & Spatio-Temporal Topology',
  description: 'Interactive graph visualization of multi-hop money flow, circular layering loops, and rapid mule dispersion.',
  robots: {
    index: false,
    follow: false,
    noarchive: true,
  },
};

export default function GraphLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
