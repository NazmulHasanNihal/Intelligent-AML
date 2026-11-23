import type { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  const baseUrl = 'https://intelligent-aml.vercel.app';
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: [
          '/app',
          '/app/*',
          '/api/*',
          '/triage',
          '/screening',
          '/customers',
          '/cases',
          '/graph',
          '/tbml',
          '/sar',
          '/rfi',
          '/rules',
          '/governance',
        ],
      },
    ],
    sitemap: `${baseUrl}/sitemap.xml`,
  };
}
