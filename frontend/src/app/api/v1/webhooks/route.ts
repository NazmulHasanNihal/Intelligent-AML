import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { computeSha256, appendAuditLog } from '@/lib/audit/hashChain';
import {
  INITIAL_CONNECTORS,
  INITIAL_WEBHOOK_DELIVERIES,
  isPermittedWebhookTarget,
} from '@/lib/connectors/registry';
import { fetchBackendWithMode, engineModeHeaders } from '@/lib/apiAdapter';

export const dynamic = 'force-dynamic';

const WebhookDispatchSchema = z.object({
  connectorId: z.string().min(3),
  eventType: z.enum([
    'HOLD_ENFORCED_TIER1',
    'STR_SCHEMA_VALIDATED',
    'SANCTIONS_INTERDICTION',
    'WORM_CHECKPOINT_SYNC',
    'CONNECTOR_HEARTBEAT_TEST',
  ]),
  targetAccount: z.string().min(3).max(64).default('SYSTEM_HEALTHCHECK'),
  endpointOverride: z.string().url().optional(),
  payload: z.record(z.unknown()).optional(),
});

export async function GET() {
  const { data, mode } = await fetchBackendWithMode(
    '/api/v1/webhooks',
    { method: 'GET' },
    () => ({
      connectors: INITIAL_CONNECTORS,
      recentDeliveries: INITIAL_WEBHOOK_DELIVERIES,
      timestamp: new Date().toISOString(),
    })
  );

  return NextResponse.json(data, { headers: engineModeHeaders(mode) });
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const parsed = WebhookDispatchSchema.safeParse(body);
    if (!parsed.success) {
      return NextResponse.json({ error: 'Validation failed', issues: parsed.error.issues }, { status: 400 });
    }

    const input = parsed.data;
    const connector = INITIAL_CONNECTORS.find((c) => c.id === input.connectorId);
    if (!connector) {
      return NextResponse.json({ error: 'Unknown connector identifier' }, { status: 404 });
    }

    const targetUrl = input.endpointOverride || connector.endpoint;
    if (!isPermittedWebhookTarget(targetUrl)) {
      return NextResponse.json(
        { error: 'Webhook egress blocked: only internal/localhost destinations permitted without explicit ALLOW_WEBHOOK_EGRESS.' },
        { status: 403 }
      );
    }

    const { data, mode } = await fetchBackendWithMode(
      '/api/v1/webhooks',
      { method: 'POST', body: JSON.stringify(input) },
      async () => {
        const envelope = JSON.stringify({
          connectorId: input.connectorId,
          eventType: input.eventType,
          targetAccount: input.targetAccount,
          payload: input.payload || {},
          timestamp: new Date().toISOString(),
        });
        const sigDigest = await computeSha256(envelope);
        const block = await appendAuditLog({
          action: `WEBHOOK_${input.eventType}`,
          officerId: 'SYS-CONNECTOR',
          officerName: connector.name,
          role: 'SYSTEM_ENGINE',
          targetId: input.targetAccount,
          details: `Signed webhook dispatched to ${targetUrl} (${sigDigest.slice(0, 16)}).`,
        });

        return {
          success: true,
          delivery: {
            id: `WH-${Date.now().toString().slice(-6)}`,
            connectorId: input.connectorId,
            eventType: input.eventType,
            targetAccount: input.targetAccount,
            statusCode: 202,
            signaturePrefix: `sha256=${sigDigest.slice(0, 12)}`,
            deliveredAt: new Date().toISOString(),
            auditBlockHash: block.merkleHash,
            mode: 'serverless-demo' as const,
          },
        };
      }
    );

    return NextResponse.json(data, { status: 202, headers: engineModeHeaders(mode) });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Webhook dispatch failed';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
