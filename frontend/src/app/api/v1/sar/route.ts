import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { INITIAL_CASES, INITIAL_CTR_RECORDS } from '@/lib/data/commercialSeed';
import { appendAuditLog } from '@/lib/audit/hashChain';
import { scanTextForTippingOff } from '@/lib/compliance/tippingOff';
import { fetchBackendWithMode, engineModeHeaders } from '@/lib/apiAdapter';

export const dynamic = 'force-dynamic';

const SarFilingSchema = z.object({
  caseId: z.string().min(3).max(64),
  reportType: z.enum(['STR', 'CTR', 'SAR']).default('STR'),
  jurisdiction: z.enum(['BD_BFIU', 'US_FINCEN', 'EU_AMLA']).default('BD_BFIU'),
  makerId: z.string().min(3),
  checkerId: z.string().min(3),
  narrative: z.string().min(20).max(5000),
  customerFacingMemo: z.string().max(1000).optional(),
});

export async function GET() {
  const { data, mode } = await fetchBackendWithMode(
    '/api/v1/sar',
    { method: 'GET' },
    () => ({
      filings: INITIAL_CASES.map((c) => ({
        filingId: `FIL-${c.id.replace('CASE-', '')}`,
        caseId: c.id,
        entityName: c.entityName,
        reportType: 'STR',
        schemaVersion: 'UNODC-goAML-v4.2-XML',
        exposureUsd: c.riskExposureUsd,
        exposureBdt: c.riskExposureBdt,
        status: c.status,
      })),
      ctrBatch: INITIAL_CTR_RECORDS,
      timestamp: new Date().toISOString(),
    })
  );

  return NextResponse.json(data, { headers: engineModeHeaders(mode) });
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const parsed = SarFilingSchema.safeParse(body);
    if (!parsed.success) {
      return NextResponse.json({ error: 'Validation failed', issues: parsed.error.issues }, { status: 400 });
    }

    const input = parsed.data;

    if (input.makerId === input.checkerId) {
      return NextResponse.json(
        { error: 'Maker-Checker violation: Filing officer and checker must be distinct signatories.' },
        { status: 403 }
      );
    }

    if (input.customerFacingMemo) {
      const tipCheck = scanTextForTippingOff(input.customerFacingMemo);
      if (tipCheck.containsTippingOff) {
        return NextResponse.json(
          {
            error: 'Anti-tipping-off violation blocked (MLPA 2012 § 6 / 31 U.S.C. § 5318(g)(2)).',
            violations: tipCheck.matchedPhrases,
          },
          { status: 422 }
        );
      }
    }

    const { data, mode } = await fetchBackendWithMode(
      '/api/v1/sar',
      { method: 'POST', body: JSON.stringify(input) },
      async () => {
        const block = await appendAuditLog({
          action: `${input.reportType}_FILED_4EYES`,
          officerId: input.checkerId,
          officerName: input.checkerId,
          role: 'MLRO_CAMLCO',
          targetId: input.caseId,
          jurisdiction: input.jurisdiction,
          checkerId: input.checkerId,
          details: `${input.reportType} docket certified by maker ${input.makerId} and checker ${input.checkerId} under ${input.jurisdiction}.`,
        });

        return {
          success: true,
          filingId: `FIL-${Date.now().toString().slice(-6)}`,
          caseId: input.caseId,
          reportType: input.reportType,
          jurisdiction: input.jurisdiction,
          auditHash: block.merkleHash,
          filedAt: new Date().toISOString(),
        };
      }
    );

    return NextResponse.json(data, { status: 201, headers: engineModeHeaders(mode) });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'SAR dispatch error';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
