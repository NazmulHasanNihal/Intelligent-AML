import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Executive Surveillance & SLA Dashboard',
  description: 'Real-time transaction surveillance, topological anomaly telemetry, and automated SLA triage.',
  robots: {
    index: false,
    follow: false,
    noarchive: true,
  },
};

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
