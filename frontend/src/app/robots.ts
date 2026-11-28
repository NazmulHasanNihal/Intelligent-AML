import { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  const allowAudit = process.env.ALLOW_PUBLIC_AUDIT !== 'false';

  return {
    rules: [
      {
        userAgent: '*',
        allow: allowAudit ? ['/', '/governance', '/app'] : ['/', '/governance'],
        disallow: allowAudit ? ['/api/', '/styleguide'] : ['/api/', '/styleguide', '/app'],
      },
    ],
    sitemap: 'https://intelligent-aml.vercel.app/sitemap.xml',
  };
}
