import type { Metadata } from 'next';

const allowAudit = process.env.ALLOW_PUBLIC_AUDIT !== 'false';

export const metadata: Metadata = {
  title: 'Executive Surveillance & SLA Dashboard',
  description: 'Real-time transaction surveillance, topological anomaly telemetry, and automated SLA triage.',
  robots: allowAudit
    ? {
        index: true,
        follow: true,
      }
    : {
        index: false,
        follow: false,
        noarchive: true,
      },
};

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
