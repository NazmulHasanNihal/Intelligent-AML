import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Institutional Case Management Docket',
  description: 'WORM-audited multi-stage investigation dossiers with cryptographic evidence preservation complying with FRE 902(11) & BFIU reporting guidelines.',
  robots: {
    index: false,
    follow: false,
    noarchive: true,
  },
};

export default function CasesLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
