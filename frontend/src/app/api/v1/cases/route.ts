import { NextRequest, NextResponse } from 'next/server';
import { SEEDED_CASES } from '@/lib/seedData';

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const statusFilter = searchParams.get('status');

  let cases = [...SEEDED_CASES];
  if (statusFilter && statusFilter !== 'ALL') {
    cases = cases.filter(c => c.status === statusFilter);
  }

  return NextResponse.json({
    cases,
    total: cases.length,
    timestamp: new Date().toISOString()
  });
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const newCase = {
      id: `CASE-2026-${Math.floor(1000 + Math.random() * 9000)}`,
      createdAt: new Date().toISOString(),
      status: 'INVESTIGATION_OPEN',
      ...body
    };

    return NextResponse.json({ success: true, case: newCase }, { status: 201 });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Error creating case';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
