import { NextResponse } from 'next/server';
import { OFFICIAL_WATCHLIST_FEEDS } from '@/lib/screening/watchlistRegistry';

/**
 * GET /api/v1/screening/lists
 * Returns all 5 official registered watchlist feeds with published versions,
 * SHA-256 cryptographic hashes, fetch timestamps, and record counts.
 */
export const dynamic = 'force-dynamic';

export async function GET() {
  const feeds = Object.values(OFFICIAL_WATCHLIST_FEEDS);
  return NextResponse.json({
    status: 'HEALTHY',
    timestamp: new Date().toISOString(),
    totalFeeds: feeds.length,
    feeds
  });
}
