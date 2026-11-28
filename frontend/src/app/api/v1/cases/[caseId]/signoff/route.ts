import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { appendAuditLog } from '@/lib/audit/hashChain';

const SignOffSchema = z.object({
  actionType: z.enum(['SAR_FILING', 'ACCOUNT_FREEZE', 'CASE_DISMISSAL', 'EMERGENCY_QUARANTINE']),
  makerId: z.string(),
  makerRole: z.string(),
  checkerId: z.string(),
  checkerRole: z.string(),
  justificationCode: z.string(),
  operationalRationale: z.string().min(15),
  evidenceDossierHash: z.string()
});

export const dynamic = 'force-dynamic';

export async function POST(
  req: NextRequest,
  { params }: { params: Promise<{ caseId: string }> }
) {
  try {
    const resolvedParams = await params;
    const caseId = resolvedParams.caseId;
    const body = await req.json();
    const parsed = SignOffSchema.safeParse(body);

    if (!parsed.success) {
      return NextResponse.json({ error: 'Validation failed', issues: parsed.error.issues }, { status: 400 });
    }

    const data = parsed.data;

    // Strict 4-Eyes rule: Maker and Checker cannot be identical
    if (data.makerId === data.checkerId) {
      return NextResponse.json({
        error: '4-Eyes Violation: Maker and Checker must be distinct authorized officers.'
      }, { status: 403 });
    }

    // Append cryptographic entry to WORM hash chain
    const logEntry = await appendAuditLog({
      action: `FOUR_EYES_APPROVAL_${data.actionType}`,
      officerId: data.checkerId,
      officerName: `${data.checkerRole} Officer`,
      role: data.checkerRole as any,
      targetId: caseId,
      details: `Dual signatory approval executed. Maker: ${data.makerId} (${data.makerRole}), Checker: ${data.checkerId} (${data.checkerRole}). Justification: ${data.justificationCode} - ${data.operationalRationale}. Evidence SHA-256: ${data.evidenceDossierHash.slice(0, 16)}...`,
      jurisdiction: 'BGD'
    });

    return NextResponse.json({
      success: true,
      caseId,
      status: data.actionType === 'SAR_FILING' ? 'SAR_FILED' : data.actionType === 'ACCOUNT_FREEZE' ? 'ACCOUNT_FROZEN' : 'RESOLVED',
      auditProof: {
        sequence: logEntry.sequence,
        currentHash: logEntry.currentHash,
        previousHash: logEntry.previousHash,
        timestamp: logEntry.timestamp
      }
    });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Sign-off failed';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
