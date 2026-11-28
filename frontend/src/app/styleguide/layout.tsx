import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Design System & UI Styleguide',
  description: 'Internal component, token, and contrast verification surface for Night Ledger & Federal Paper palettes.',
  robots: {
    index: false,
    follow: false,
  },
};

export default function StyleguideLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
