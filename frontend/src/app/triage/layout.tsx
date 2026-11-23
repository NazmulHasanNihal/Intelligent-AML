import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Alert Triage & 12-Invariant Attribution',
  description: 'Automated 3-tier triage queue with local Shapley invariant waterfall explanations and supervisory override dual controls.',
  robots: {
    index: false,
    follow: false,
    noarchive: true,
  },
};

export default function TriageLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
