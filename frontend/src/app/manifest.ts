import type { MetadataRoute } from 'next';

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'Intelligent-AML | Conformal Risk & AML Compliance OS',
    short_name: 'Intelligent-AML',
    description: 'Platform v3.0 — Spatio-temporal AML surveillance, conformal risk tiering, goAML STR reporting & WORM audit vault.',
    start_url: '/app',
    display: 'standalone',
    background_color: '#070A12',
    theme_color: '#10B981',
    icons: [
      {
        src: '/icon-192.png',
        sizes: '192x192',
        type: 'image/png',
      },
      {
        src: '/icon-512.png',
        sizes: '512x512',
        type: 'image/png',
      },
      {
        src: '/icon.svg',
        sizes: 'any',
        type: 'image/svg+xml',
      },
    ],
  };
}
