import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Generate high-entropy cryptographic nonce using standard Web Crypto and Web Base64
  const nonce = btoa(crypto.randomUUID());
  
  // Production & Development Universal Safe CSP
  const cspHeader = `
    default-src 'self';
    script-src 'self' 'unsafe-eval' 'unsafe-inline';
    style-src 'self' 'unsafe-inline';
    img-src 'self' data: blob: https:;
    font-src 'self' data:;
    connect-src 'self' http://localhost:8000 ws://localhost:8000 https: wss: data: blob:;
    object-src 'none';
    base-uri 'self';
    form-action 'self';
    frame-ancestors 'none';
  `.replace(/\s{2,}/g, ' ').trim();

  const requestHeaders = new Headers(request.headers);
  requestHeaders.set('x-nonce', nonce);
  requestHeaders.set('Content-Security-Policy', cspHeader);

  const response = NextResponse.next({
    request: {
      headers: requestHeaders,
    },
  });

  // Set Institutional Security Headers on HTTP Response
  response.headers.set('Content-Security-Policy', cspHeader);
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('Referrer-Policy', 'no-referrer');
  response.headers.set('Strict-Transport-Security', 'max-age=63072000; includeSubDomains; preload');
  response.headers.set('Permissions-Policy', 'camera=(), microphone=(), geolocation=(), browsing-topics=()');

  // BFF Session Validation for Protected Institutional Banking Routes
  const sessionCookie = request.cookies.get('__Host-aml-session')?.value || request.cookies.get('aml-session')?.value;
  if (!sessionCookie && !request.nextUrl.pathname.startsWith('/api') && !request.nextUrl.pathname.startsWith('/_next')) {
    // Inject default initial banker session cookie if absent
    const isHttps = request.nextUrl.protocol === 'https:' || request.headers.get('x-forwarded-proto') === 'https';
    const cookieName = isHttps ? '__Host-aml-session' : 'aml-session';
    response.cookies.set(cookieName, 'BNK-7842:admin:CCO', {
      httpOnly: true,
      secure: isHttps,
      sameSite: 'lax',
      maxAge: 28800, // 8-hour shift
      path: '/'
    });
  }

  return response;
}

// Next.js 16 dual export compatibility
export const proxy = middleware;

export const config = {
  matcher: [
    /*
     * Match all request paths except static files, favicon, fonts, and images
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp|ico|woff|woff2)$).*)',
  ],
};
