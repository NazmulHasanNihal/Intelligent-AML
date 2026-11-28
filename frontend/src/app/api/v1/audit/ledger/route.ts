import { NextResponse } from 'next/server';
import { getAuditChain } from '@/lib/audit/hashChain';

export const dynamic = 'force-dynamic';

export async function GET() {
  const chain = getAuditChain();
  return NextResponse.json({
    chain,
    length: chain.length,
    latestHash: chain[chain.length - 1]?.currentHash || '',
    complianceStandard: '31 CFR § 1010.430 & FRE 902(11) Self-Authenticating Hash Chain'
  });
}
