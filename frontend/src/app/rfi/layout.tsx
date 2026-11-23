import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Compliance RFI & Inter-Bank Sharing Hub',
  description: 'Audited requests for information, document collection, and correspondent bank verification.',
  robots: {
    index: false,
    follow: false,
    noarchive: true,
  },
};

export default function RfiLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
