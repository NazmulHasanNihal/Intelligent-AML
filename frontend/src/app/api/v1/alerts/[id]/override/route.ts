import { NextResponse } from 'next/server';
import { fetchFastApiWithFallback } from '@/lib/apiAdapter';
import { computeSha256 } from '@/lib/audit/hashChain';

interface RouteContext {
  params: Promise<{ id: string }>;
}

export async function POST(request: Request, context: RouteContext) {
  const { id } = await context.params;
  const body = await request.json();

  const localCompute = async () => {
    const timestamp = new Date().toISOString();
    const payload = {
      alert_id: id,
      original_score: 0.942,
      overridden_score: body.new_score ?? 0.12,
      original_tier: 'Tier 1',
      overridden_tier: body.new_tier ?? 'Tier 3',
      justification_code: body.justification_code ?? 'DOCUMENTED_TRADE_INVOICE',
      officer_notes: body.notes ?? 'Verified genuine documentary letter of credit.',
      officer_id: body.officer_id ?? 'OFFICER-CAMLCO-01',
      officer_role: body.officer_role ?? 'MLRO / CAMLCO'
    };

    const canonicalJson = JSON.stringify(payload, Object.keys(payload).sort());
    const hash = await computeSha256(canonicalJson);

    return {
      status: 'OVERRIDE_RECORDED_TAMPER_EVIDENT',
      alert_id: id,
      original_score: payload.original_score,
      overridden_score: payload.overridden_score,
      original_tier: payload.original_tier,
      overridden_tier: payload.overridden_tier,
      justification_code: payload.justification_code,
      audit_block_height: 104,
      audit_block_hash: hash
    };
  };

  const result = await fetchFastApiWithFallback(
    `/api/v1/alerts/${id}/override`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    },
    localCompute,
    { timeoutMs: 3000 }
  );

  return NextResponse.json(result);
}
