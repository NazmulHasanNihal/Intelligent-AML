import { NextRequest, NextResponse } from 'next/server';
import { computeScreeningScore } from '@/lib/screening/matcher';
import { fetchFastApiWithFallback } from '@/lib/apiAdapter';

/**
 * POST /api/v1/screening/score
 * Multi-algorithm score decomposition between query name and target name (FastAPI BFF + TS fallback).
 */
export const dynamic = 'force-dynamic';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const {
      queryName,
      targetName,
      queryDob,
      targetDob,
      queryCountry,
      targetCountry,
      queryId,
      targetId,
      config
    } = body;

    if (!queryName || !targetName) {
      return NextResponse.json(
        { error: 'queryName and targetName are required.' },
        { status: 400 }
      );
    }

    const localScore = () =>
      computeScreeningScore(queryName, targetName, {
        queryDob,
        targetDob,
        queryCountry,
        targetCountry,
        queryId,
        targetId,
        config
      });

    const raw = await fetchFastApiWithFallback<Record<string, any>>(
      '/api/v1/screening/score',
      {
        method: 'POST',
        body: JSON.stringify({
          query_name: queryName,
          target_name: targetName,
          query_dob: queryDob || undefined,
          target_dob: targetDob || undefined,
          query_country: queryCountry || undefined,
          target_country: targetCountry || undefined,
          query_id: queryId || undefined,
          target_id: targetId || undefined,
          auto_freeze_threshold: config?.autoFreezeThreshold ?? 85.0,
          quarantine_threshold: config?.quarantineThreshold ?? 65.0
        })
      },
      localScore,
      { timeoutMs: 2500 }
    );

    if ('matchScore' in raw) {
      return NextResponse.json(raw);
    }

    const bd = raw.algorithm_breakdown || {};
    const corr = raw.corroboration_details || {};
    const td = raw.token_diffs || {};
    return NextResponse.json({
      matchScore: raw.match_score ?? 0,
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
      matchType: raw.match_type ?? 'EXACT',
      disposition: raw.disposition ?? 'PENDING_REVIEW',
      tokenDiffs: {
        screenedTokens: td.screened_tokens ?? [],
        matchedTokens: td.matched_tokens ?? [],
        commonTokens: td.common_tokens ?? []
      },
      screenedName: raw.screened_name ?? queryName,
      matchedEntity: raw.matched_entity ?? targetName
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || 'Scoring error' }, { status: 500 });
  }
}
