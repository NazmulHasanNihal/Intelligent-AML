import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { generateFullAlertQueue } from '@/lib/data/commercialSeed';
import { fetchBackendWithMode, engineModeHeaders } from '@/lib/apiAdapter';

export const dynamic = 'force-dynamic';

const CreateAlertSchema = z.object({
  account: z.string().min(4).max(64),
  entityName: z.string().min(2).max(160),
  amount: z.number().positive(),
  rail: z.string().default('SWIFT MT700 (LC)'),
  tierCode: z.union([z.literal(1), z.literal(2), z.literal(3)]).default(1),
  typology: z.string().min(3).max(160),
  whyFlagged: z.string().min(10).max(500),
});

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const tierParam = searchParams.get('tier');
  const statusParam = searchParams.get('status');
  const limitParam = Math.min(Math.max(Number(searchParams.get('limit') || 50), 1), 500);

  const query = new URLSearchParams();
  if (tierParam) query.set('tier', tierParam);
  if (statusParam) query.set('status', statusParam);
  query.set('limit', String(limitParam));

  const { data, mode } = await fetchBackendWithMode(
    `/api/v1/alerts?${query.toString()}`,
    { method: 'GET' },
    () => {
      let queue = generateFullAlertQueue();
      if (tierParam) {
        const tierNum = Number(tierParam);
        if ([1, 2, 3].includes(tierNum)) {
          queue = queue.filter((a) => a.tierCode === tierNum);
        }
      }
      if (statusParam && statusParam !== 'ALL') {
        queue = queue.filter((a) => a.status === statusParam);
      }
      return {
        alerts: queue.slice(0, limitParam),
        total: queue.length,
        timestamp: new Date().toISOString(),
      };
    }
  );

  return NextResponse.json(data, { headers: engineModeHeaders(mode) });
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const parsed = CreateAlertSchema.safeParse(body);
    if (!parsed.success) {
      return NextResponse.json(
        { error: 'Validation failed', issues: parsed.error.issues },
        { status: 400 }
      );
    }

    const input = parsed.data;
    const { data, mode } = await fetchBackendWithMode(
      '/api/v1/alerts',
      { method: 'POST', body: JSON.stringify(input) },
      () => ({
        success: true,
        alert: {
          id: `ALT-${Date.now().toString().slice(-6)}`,
          timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19) + ' UTC',
          account: input.account,
          entityName: input.entityName,
          amount: input.amount,
          amountBdt: Number((input.amount * 120).toFixed(2)),
          rail: input.rail,
          tierCode: input.tierCode,
          tier: input.tierCode === 1 ? 'Tier 1 Hold' : input.tierCode === 2 ? 'Tier 2 Review' : 'Tier 3 Clear',
          riskScore: input.tierCode === 1 ? 0.96 : input.tierCode === 2 ? 0.62 : 0.08,
          status: 'PENDING_TRIAGE',
          typology: input.typology,
          whyFlagged: input.whyFlagged,
        },
      })
    );

    return NextResponse.json(data, { status: 201, headers: engineModeHeaders(mode) });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Alert ingestion error';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
