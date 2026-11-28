import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { scanTextForTippingOff } from '@/lib/compliance/tippingOff';
import { fetchFastApiWithFallback } from '@/lib/apiAdapter';

const CreateRfiSchema = z.object({
  caseId: z.string(),
  targetEntity: z.string(),
  accountNumber: z.string(),
  reason: z.string().min(10),
  deadlineDays: z.number().int().min(1).max(30).default(7),
  requiredDocuments: z.array(z.string()).min(1)
});

const INITIAL_RFIS = [
  {
    id: 'RFI-2026-0042',
    caseId: 'CASE-2026-0881',
    entityName: 'Meghna Industrial & Agro Processing Ltd',
    account: 'BD22-EBLB-4829-1092-8823',
    status: 'ISSUED_PENDING',
    requestDate: '2026-09-02 09:00:00 UTC',
    deadline: '2026-09-09T09:00:00Z',
    reason: 'Routine institutional documentation refresh for LC-2026-CTG-88912 commercial invoice verification.',
    requiredDocs: ['Customs Bill of Entry', 'Supplier Commercial Invoice'],
    documentsReceived: []
  },
  {
    id: 'RFI-2026-0043',
    caseId: 'CASE-2026-0882',
    entityName: 'Tanvir Ahmed Logistics',
    account: 'BD22-SCBL-9912-3341-7719',
    status: 'ISSUED_PENDING',
    requestDate: '2026-09-02 10:15:00 UTC',
    deadline: '2026-09-07T10:15:00Z',
    reason: 'Periodic customer due diligence update and agent aggregation turnover review.',
    requiredDocs: ['Trade License', 'Agent Commission Settlement Statement'],
    documentsReceived: []
  }
];

export const dynamic = 'force-dynamic';

export async function GET() {
  const result = await fetchFastApiWithFallback(
    '/api/v1/rfi',
    { method: 'GET' },
    () => ({
      rfis: INITIAL_RFIS,
      total: INITIAL_RFIS.length,
      timestamp: new Date().toISOString()
    }),
    { timeoutMs: 2500 }
  );

  if (Array.isArray(result)) {
    return NextResponse.json({
      rfis: result,
      total: result.length,
      timestamp: new Date().toISOString()
    });
  }

  return NextResponse.json(result);
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const parsed = CreateRfiSchema.safeParse(body);

    if (!parsed.success) {
      return NextResponse.json({ error: 'Validation failed', issues: parsed.error.issues }, { status: 400 });
    }

    const data = parsed.data;

    // Scan text against 31 U.S.C. § 5318(g)(2) & MLPA 2012 § 6 Anti-Tipping-Off rules
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
      status: 'ISSUED_PENDING',
      requestDate: new Date().toISOString().replace('T', ' ').slice(0, 19) + ' UTC',
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
