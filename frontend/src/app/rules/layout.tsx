import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Rule Studio & Counterfactual Recourse',
  description: 'Dynamic invariant threshold authoring, sandbox simulation, and actionable customer recourse paths.',
  robots: {
    index: false,
    follow: false,
    noarchive: true,
  },
};

export default function RulesLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
