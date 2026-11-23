import type { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  const baseUrl = 'https://intelligent-aml.vercel.app';
  const allowAudit = process.env.ALLOW_PUBLIC_AUDIT !== 'false';

  return {
    rules: [
      {
        userAgent: '*',
        allow: allowAudit ? ['/', '/governance', '/app'] : ['/', '/governance'],
        disallow: allowAudit ? ['/api/'] : ['/api/', '/app'],
      },
    ],
    sitemap: `${baseUrl}/sitemap.xml`,
  };
}
