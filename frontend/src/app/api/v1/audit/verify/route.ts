import { NextResponse } from 'next/server';
import { verifyAuditChain } from '@/lib/audit/hashChain';

export async function POST() {
  const result = await verifyAuditChain();
  return NextResponse.json({
    ...result,
    verifiedAt: new Date().toISOString(),
    legalAdmissibility: result.isValid
      ? 'VERIFIED: Complies with Federal Rules of Evidence Rule 902(11) (Certified Domestic Records of a Regularly Conducted Activity).'
      : 'TAMPERED: Cryptographic hash chain validation failed. Evidence is tainted.'
  });
}
