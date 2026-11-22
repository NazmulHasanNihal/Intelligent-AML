import { NextRequest, NextResponse } from 'next/server';
import { SEEDED_CASES } from '@/lib/seedData';
import { fetchFastApiWithFallback } from '@/lib/apiAdapter';

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const statusFilter = searchParams.get('status');

  const localCompute = () => {
    let cases = [...SEEDED_CASES];
    if (statusFilter && statusFilter !== 'ALL') {
      cases = cases.filter(c => c.status === statusFilter);
    }
    return {
      cases,
      total: cases.length,
      timestamp: new Date().toISOString()
    };
  };

  const endpoint = statusFilter ? `/api/v1/cases?status=${encodeURIComponent(statusFilter)}` : '/api/v1/cases';
  const result = await fetchFastApiWithFallback(
    endpoint,
    { method: 'GET' },
    localCompute,
    { timeoutMs: 2500 }
  );

  return NextResponse.json(result);
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();

    const localCompute = () => {
      const newCase = {
        id: `CASE-2026-${Math.floor(1000 + Math.random() * 9000)}`,
        createdAt: new Date().toISOString(),
        status: 'INVESTIGATION_OPEN',
        ...body
      };
      return { success: true, case: newCase };
    };

    const result = await fetchFastApiWithFallback(
      '/api/v1/cases',
      {
        method: 'POST',
        body: JSON.stringify(body)
      },
      localCompute,
      { timeoutMs: 2500 }
    );

    return NextResponse.json(result, { status: 201 });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Error creating case';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
