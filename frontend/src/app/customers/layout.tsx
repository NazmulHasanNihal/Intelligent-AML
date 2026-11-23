import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Customer 360° KYC & Beneficial Ownership',
  description: 'Entity relationship graph, beneficial ownership trees, risk ratings, and audited PII management.',
  robots: {
    index: false,
    follow: false,
    noarchive: true,
  },
};

export default function CustomersLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
