import { NextRequest, NextResponse } from 'next/server';
import { screenWatchlistCandidate } from '@/lib/screening/watchlistRegistry';

/**
 * POST /api/v1/screening/search
 * Screens candidate entity across all 5 official watchlists.
 */
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { name, country, dob, nationalId, watchlistFilter, limit = 10, config } = body;

    if (!name || typeof name !== 'string') {
      return NextResponse.json({ error: 'Valid candidate name is required.' }, { status: 400 });
    }

    const hits = screenWatchlistCandidate(name, {
      country,
      dob,
      nationalId,
      watchlistFilter,
      config
    });

    return NextResponse.json({
      query: { name, country, dob, nationalId, watchlistFilter },
      totalHits: hits.length,
      hits: hits.slice(0, limit)
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || 'Search execution error' }, { status: 500 });
  }
}
