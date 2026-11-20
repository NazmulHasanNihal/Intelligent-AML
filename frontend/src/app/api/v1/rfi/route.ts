import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { scanTextForTippingOff } from '@/lib/compliance/tippingOff';
import { SEEDED_RFI_REQUESTS } from '@/lib/seedData';

const CreateRfiSchema = z.object({
  caseId: z.string(),
  targetEntity: z.string(),
  accountNumber: z.string(),
  reason: z.string().min(10),
  deadlineDays: z.number().int().min(1).max(30).default(7),
  requiredDocuments: z.array(z.string()).min(1)
});

export async function GET() {
  return NextResponse.json({
    rfis: SEEDED_RFI_REQUESTS,
    total: SEEDED_RFI_REQUESTS.length,
    timestamp: new Date().toISOString()
  });
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const parsed = CreateRfiSchema.safeParse(body);

    if (!parsed.success) {
      return NextResponse.json({ error: 'Validation failed', issues: parsed.error.issues }, { status: 400 });
    }

    const data = parsed.data;

    // Scan text against 31 U.S.C. § 5318(g)(2) Anti-Tipping-Off rules
    const scan = scanTextForTippingOff(data.reason);
    if (scan.containsTippingOff) {
      return NextResponse.json({
        error: 'CRITICAL_TIPPING_OFF_VIOLATION',
        message: 'The RFI communication contains prohibited statutory terms that reveal an active SAR filing or criminal investigation to the customer or counterparty.',
        matchedPhrases: scan.matchedPhrases,
        legalNotice: 'Under 31 U.S.C. § 5318(g)(2) and MLPA 2012 § 6, disclosing an AML investigation carries strict criminal penalties.'
      }, { status: 422 });
    }

    const newRfi = {
      id: `RFI-2026-${Math.floor(1000 + Math.random() * 9000)}`,
      caseId: data.caseId,
      entityName: data.targetEntity,
      account: data.accountNumber,
      status: 'PENDING_CUSTOMER_RESPONSE',
      requestDate: new Date().toISOString(),
      deadline: new Date(Date.now() + data.deadlineDays * 86400000).toISOString(),
      reason: data.reason,
      requiredDocs: data.requiredDocuments,
      documentsReceived: []
    };

    return NextResponse.json({ success: true, rfi: newRfi }, { status: 201 });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Failed to create RFI';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
