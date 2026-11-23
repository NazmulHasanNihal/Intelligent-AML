import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'BFIU goAML STR/SAR & CTR Workbench',
  description: 'UNODC goAML v4.2 XML filing workbench with mandatory supporting attachments and anti-tipping-off safeguards under MLPA 2012 § 27.',
  robots: {
    index: false,
    follow: false,
    noarchive: true,
  },
};

export default function SarLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
