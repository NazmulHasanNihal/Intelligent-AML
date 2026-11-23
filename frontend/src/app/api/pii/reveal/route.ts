import { NextRequest, NextResponse } from 'next/server';
import { PiiRevealSchema } from '@/lib/validation/schemas';
import { canRevealPii } from '@/lib/auth/session';
import { createChainedAuditEntry, getAuditChain } from '@/lib/audit/hashChain';

// Sliding-window rate limit store (in-memory per instance)
const revealRateLimits: Record<string, number[]> = {};
const MAX_REVEALS = 5;
const WINDOW_MS = 10 * 60 * 1000; // 10 minutes

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();

    // 1. Zod Input Schema Validation
    const parseResult = PiiRevealSchema.safeParse(body);
    if (!parseResult.success) {
      return NextResponse.json(
        {
          error: 'VALIDATION_ERROR',
          message: 'Invalid request payload',
          details: parseResult.error.flatten()
        },
        { status: 422 }
      );
    }

    const { target_account, reason } = parseResult.data;

    // 2. Server-side Role Check from Session Header / Cookie
    const authRole = req.headers.get('x-officer-role') || 'ANALYST_L1';
    const officerName = req.headers.get('x-officer-name') || 'Anonymous Officer';

    if (!canRevealPii(authRole)) {
      return NextResponse.json(
        {
          error: 'FORBIDDEN',
          message: `Access Denied: Role '${authRole}' is not authorized to unmask PII. Only L2 Investigators, Supervisors, and MLROs hold unmasking clearance.`
        },
        { status: 403 }
      );
    }

    // 3. Rate Limiting Check
    const now = Date.now();
    const timestamps = (revealRateLimits[officerName] || []).filter(t => now - t < WINDOW_MS);
    if (timestamps.length >= MAX_REVEALS) {
      return NextResponse.json(
        {
          error: 'RATE_LIMIT_EXCEEDED',
          message: `Rate limit exceeded: Maximum ${MAX_REVEALS} PII reveals per 10 minutes reached.`
        },
        { status: 429 }
      );
    }
    timestamps.push(now);
    revealRateLimits[officerName] = timestamps;

    // 4. Immutable Audit Ledger Entry
    const chain = getAuditChain();
    const prevBlock = chain[chain.length - 1];
    const prevHash = prevBlock ? (prevBlock.currentHash || prevBlock.merkleHash) : '0'.repeat(64);
    const blockHeight = chain.length + 1;

    const auditEntry = await createChainedAuditEntry(
      prevHash,
      blockHeight,
      'SERVER_PII_REVEAL_GRANTED',
      officerName,
      `USR-${officerName.toLowerCase().replace(/\s+/g, '_')}`,
      target_account,
      'BFIU_MLPA_2012_S25',
      `Unmasked PII accessed for 60s. Regulatory Reason: ${reason}`
    );

    return NextResponse.json({
      target_account,
      unmasked: true,
      expires_in_seconds: 60,
      actor: officerName,
      actor_role: authRole,
      reason,
      audit_receipt: auditEntry.currentHash || auditEntry.merkleHash,
      timestamp: auditEntry.timestamp
    });
  } catch (err: any) {
    return NextResponse.json(
      { error: 'INTERNAL_ERROR', message: err?.message || 'Server error' },
      { status: 500 }
    );
  }
}
