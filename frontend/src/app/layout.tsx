import type { Metadata } from 'next';
import { Inter, JetBrains_Mono } from 'next/font/google';
import './globals.css';
import { AppShellWrapper } from '@/components/shell/AppShellWrapper';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-jetbrains-mono',
});

export const metadata: Metadata = {
  metadataBase: new URL('https://intelligent-aml.vercel.app'),
  title: {
    default: 'Intelligent-AML | Enterprise AML Compliance & Conformal Risk OS',
    template: '%s | Intelligent-AML'
  },
  description: 'Tier-1 Air-Gap-Ready Anti-Money Laundering & Conformal Risk Control Operating System for Central Banks & Enterprise Financial Institutions. 84% noise reduction with provable coverage guarantees.',
  keywords: ['AML', 'Anti-Money Laundering', 'BFIU', 'goAML', 'Conformal Prediction', 'Graph Neural Networks', 'Financial Crime', 'KYC', 'Sanctions Screening'],
  authors: [{ name: 'Intelligent-AML Engineering & Research' }],
  creator: 'Intelligent-AML Platform',
  icons: {
    icon: '/favicon.ico',
  },
  openGraph: {
    title: 'Intelligent-AML | Enterprise AML Compliance & Conformal Risk OS',
    description: 'Tier-1 Air-Gap-Ready Anti-Money Laundering & Conformal Risk Control Operating System. 84% noise reduction with finite-sample statistical guarantees.',
    url: 'https://intelligent-aml.vercel.app',
    siteName: 'Intelligent-AML Platform',
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Intelligent-AML | Enterprise AML Compliance & Conformal Risk OS',
    description: 'Tier-1 Air-Gap-Ready Anti-Money Laundering & Conformal Risk Control Operating System.',
  },
  robots: {
    index: true,
    follow: true,
  }
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name: 'Intelligent-AML',
    applicationCategory: 'BusinessApplication',
    operatingSystem: 'Web, Linux (Air-Gapped Kubernetes)',
    description: 'Tier-1 Anti-Money Laundering & Conformal Risk Control Operating System for Central Banks & Enterprise Financial Institutions. 84% noise reduction with provable coverage guarantees.',
    softwareVersion: 'Platform v3.0 | C-STGB v3.2 Engine',
    offers: {
      '@type': 'Offer',
      price: '0',
      priceCurrency: 'USD',
    },
    publisher: {
      '@type': 'Organization',
      name: 'Intelligent-AML Platform',
      url: 'https://intelligent-aml.vercel.app',
    },
  };

  return (
    <html lang="en" data-theme="dark" className={`dark ${inter.variable} ${jetbrainsMono.variable} overflow-x-hidden w-full max-w-full`}>
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </head>
      <body className="min-h-screen bg-[#070B12] text-slate-100 font-sans antialiased selection:bg-emerald-500/30 selection:text-emerald-200 overflow-x-hidden w-full max-w-full">
        <AppShellWrapper>
          {children}
        </AppShellWrapper>
      </body>
    </html>
  );
}
