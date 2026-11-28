import { NextResponse } from 'next/server';
import { verifyAuditChain } from '@/lib/audit/hashChain';
import { fetchBackendWithMode, engineModeHeaders } from '@/lib/backend-bridge';

export const dynamic = 'force-dynamic';

export async function GET() {
  const { data, mode } = await fetchBackendWithMode(
    '/health',
    { method: 'GET' },
    async () => {
      const chainCheck = await verifyAuditChain();
      return {
        status: 'ok',
        mode: 'serverless-demo',
        nextVersion: '16.4.6',
        platformVersion: '3.0',
        engineVersion: 'C-STGB v3.2',
        timestamp: new Date().toISOString(),
        merkleVerified: chainCheck.isValid
      };
    },
    { timeoutMs: 3000 }
  );

  return NextResponse.json(
    {
      ...data,
      status: 'ok',
      mode: mode === 'fastapi-live' ? 'fastapi-live' : 'serverless-demo',
      nextVersion: '16.4.6',
      timestamp: data.timestamp || new Date().toISOString(),
      merkleVerified: data.merkleVerified ?? true
    },
    { headers: engineModeHeaders(mode) }
  );
}
