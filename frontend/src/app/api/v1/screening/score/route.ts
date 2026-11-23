import { NextRequest, NextResponse } from 'next/server';
import { computeScreeningScore } from '@/lib/screening/matcher';

/**
 * POST /api/v1/screening/score
 * Multi-algorithm score decomposition between query name and target name.
 */
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

    const result = computeScreeningScore(queryName, targetName, {
      queryDob,
      targetDob,
      queryCountry,
      targetCountry,
      queryId,
      targetId,
      config
    });

    return NextResponse.json(result);
  } catch (err: any) {
    return NextResponse.json({ error: err.message || 'Scoring error' }, { status: 500 });
  }
}
