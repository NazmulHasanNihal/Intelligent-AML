import { NextRequest, NextResponse } from 'next/server';
import { getAuditChain } from '@/lib/audit/hashChain';
import { JURISDICTIONS, JurisdictionCode } from '@/lib/compliance/jurisdictions';

export const dynamic = 'force-dynamic';

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const jurParam = (searchParams.get('jurisdiction') || 'BD_BFIU') as JurisdictionCode;
  const jur = JURISDICTIONS[jurParam] || JURISDICTIONS.BD_BFIU;
  const chain = getAuditChain();

  return NextResponse.json({
    chain,
    length: chain.length,
    latestHash: chain[chain.length - 1]?.currentHash || '',
    jurisdiction: jur.id,
    complianceStandard: jur.evidenceRule,
  });
}
