import { NextRequest, NextResponse } from 'next/server';
import { screenWatchlistCandidate } from '@/lib/screening/watchlistRegistry';
import { fetchFastApiWithFallback } from '@/lib/apiAdapter';

function normalizeScreeningHit(h: Record<string, any>) {
  if ('matchScore' in h) return h;
  const bd = h.algorithm_breakdown || {};
  const corr = h.corroboration_details || {};
  const td = h.token_diffs || {};
  return {
    matchScore: h.match_score ?? 0,
    algorithmBreakdown: {
      jaroWinklerScore: bd.jaro_winkler_score ?? 0,
      tokenSetScore: bd.token_set_score ?? 0,
      phoneticScore: bd.phonetic_score ?? 0,
      corroborationAdjustment: bd.corroboration_adjustment ?? 0
    },
    corroborationDetails: {
      dobStatus: corr.dob_status ?? corr.dobStatus ?? 'UNAVAILABLE',
      countryStatus: corr.country_status ?? corr.countryStatus ?? 'UNAVAILABLE',
      idStatus: corr.id_status ?? corr.idStatus ?? 'UNAVAILABLE'
    },
    matchType: h.match_type ?? 'EXACT',
    disposition: h.disposition ?? 'PENDING_REVIEW',
    tokenDiffs: {
      screenedTokens: td.screened_tokens ?? [],
      matchedTokens: td.matched_tokens ?? [],
      commonTokens: td.common_tokens ?? []
    },
    screenedName: h.screened_name ?? '',
    matchedEntity: h.matched_entity ?? '',
    entityId: h.entity_id ?? '',
    officialPrimaryName: h.official_primary_name ?? '',
    matchedVariant: h.matched_variant ?? '',
    entityType: h.entity_type ?? 'ENTITY',
    watchlistId: h.watchlist_id ?? '',
    watchlistName: h.watchlist_name ?? '',
    program: h.program ?? '',
    remarks: h.remarks ?? ''
  };
}

/**
 * POST /api/v1/screening/search
 * Screens candidate entity across all 5 official watchlists (FastAPI BFF + deterministic TS fallback).
 */
export const dynamic = 'force-dynamic';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { name, country, dob, nationalId, watchlistFilter, limit = 10, config } = body;

    if (!name || typeof name !== 'string') {
      return NextResponse.json({ error: 'Valid candidate name is required.' }, { status: 400 });
    }

    const localSearch = () => {
      const hits = screenWatchlistCandidate(name, {
        country,
        dob,
        nationalId,
        watchlistFilter,
        config
      });
      return {
        query: { name, country, dob, nationalId, watchlistFilter },
        totalHits: hits.length,
        hits: hits.slice(0, limit)
      };
    };

    const raw = await fetchFastApiWithFallback<Record<string, any>>(
      '/api/v1/screening/search',
      {
        method: 'POST',
        body: JSON.stringify({
          name,
          country: country || undefined,
          dob: dob || undefined,
          national_id: nationalId || undefined,
          watchlist_filter: watchlistFilter || undefined,
          limit
        })
      },
      localSearch,
      { timeoutMs: 2500 }
    );

    const hits = Array.isArray(raw.hits) ? raw.hits.map(normalizeScreeningHit) : [];
    return NextResponse.json({
      query: raw.query ?? { name, country, dob, nationalId, watchlistFilter },
      totalHits: raw.totalHits ?? raw.total_hits ?? hits.length,
      hits: hits.slice(0, limit)
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || 'Search execution error' }, { status: 500 });
  }
}
