import { describe, it, expect } from 'vitest';
import { NextRequest } from 'next/server';
import { GET as alertsGet, POST as alertsPost } from '@/app/api/v1/alerts/route';
import { GET as sarGet } from '@/app/api/v1/sar/route';
import { GET as webhooksGet, POST as webhooksPost } from '@/app/api/v1/webhooks/route';

describe('Hybrid BFF Endpoints & Signed Webhook Connectors', () => {
  it('serves filtered alerts from /api/v1/alerts with serverless-demo mode header', async () => {
    const req = new NextRequest('http://localhost/api/v1/alerts?tier=1&limit=5');
    const res = await alertsGet(req);
    expect(res.status).toBe(200);
    expect(res.headers.get('X-AML-Engine-Mode')).toBe('serverless-demo');
    const json = await res.json();
    expect(json.alerts).toHaveLength(5);
    expect(json.alerts.every((a: any) => a.tierCode === 1)).toBe(true);
  });

  it('validates /api/v1/alerts POST payload via Zod', async () => {
    const badReq = new NextRequest('http://localhost/api/v1/alerts', {
      method: 'POST',
      body: JSON.stringify({ amount: -100 }),
    });
    expect((await alertsPost(badReq)).status).toBe(400);
  });

  it('returns seeded STR & CTR records on GET /api/v1/sar', async () => {
    const res = await sarGet();
    expect(res.status).toBe(200);
    const json = await res.json();
    expect(json.filings.length).toBeGreaterThanOrEqual(1);
    expect(json.ctrBatch.length).toBeGreaterThanOrEqual(1);
  });

  it('lists connectors on GET /api/v1/webhooks and blocks unauthorized external webhook egress', async () => {
    const listRes = await webhooksGet();
    expect(listRes.status).toBe(200);
    const listJson = await listRes.json();
    expect(listJson.connectors.length).toBeGreaterThanOrEqual(4);

    const evilReq = new NextRequest('http://localhost/api/v1/webhooks', {
      method: 'POST',
      body: JSON.stringify({
        connectorId: 'conn-core-t24',
        eventType: 'CONNECTOR_HEARTBEAT_TEST',
        endpointOverride: 'https://evil-exfil.example.com/steal',
      }),
    });
    const blocked = await webhooksPost(evilReq);
    expect(blocked.status).toBe(403);

    const safeReq = new NextRequest('http://localhost/api/v1/webhooks', {
      method: 'POST',
      body: JSON.stringify({
        connectorId: 'conn-core-t24',
        eventType: 'CONNECTOR_HEARTBEAT_TEST',
        targetAccount: 'BD22-EBLB-4829-1092-8823',
      }),
    });
    const ok = await webhooksPost(safeReq);
    expect(ok.status).toBe(202);
    const okJson = await ok.json();
    expect(okJson.delivery.signaturePrefix).toContain('sha256=');
  });
});
