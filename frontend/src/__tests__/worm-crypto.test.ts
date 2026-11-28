import { describe, it, expect, beforeEach } from 'vitest';
import { NextRequest } from 'next/server';
import {
  appendAuditLog,
  getAuditChain,
  restoreAuditChain,
  tamperAuditBlock,
  verifyAuditChain,
} from '@/lib/audit/hashChain';
import { GET as verifyGet } from '@/app/api/v1/audit/verify/route';

describe('WebCrypto SHA-256 WORM Hash Chain Integrity', () => {
  beforeEach(() => {
    restoreAuditChain();
  });

  it('verifies genesis chain and newly appended chained blocks', async () => {
    expect((await verifyAuditChain()).isValid).toBe(true);

    await appendAuditLog({
      action: 'STR_DISPATCHED_4EYES',
      officerId: 'BNK-7842',
      officerName: 'Kazi Rafiqul Islam, CAMS',
      role: 'MLRO_CAMLCO',
      targetId: 'CASE-2026-0881',
      jurisdiction: 'BD_BFIU',
      details: 'Certified STR packet queued to BFIU goAML v4.2.',
    });

    const chain = getAuditChain();
    expect(chain.length).toBeGreaterThanOrEqual(4);
    expect((await verifyAuditChain(chain)).isValid).toBe(true);
  });

  it('detects historical mutation via tamperAuditBlock and restores cleanly', async () => {
    tamperAuditBlock(2, 'MUTATED_UNAUTHORIZED_AMOUNT');
    const broken = await verifyAuditChain();
    expect(broken.isValid).toBe(false);
    expect(broken.brokenSequence).toBe(2);

    restoreAuditChain();
    const restored = await verifyAuditChain();
    expect(restored.isValid).toBe(true);
  });

  it('exposes BD_BFIU admissibility statement on /api/v1/audit/verify without US leaks', async () => {
    const req = new NextRequest('http://localhost/api/v1/audit/verify?jurisdiction=BD_BFIU');
    const res = await verifyGet(req);
    expect(res.status).toBe(200);
    const json = await res.json();
    expect(json.isValid).toBe(true);
    expect(json.legalAdmissibility).toContain('Bangladesh Evidence Act');
    expect(json.legalAdmissibility).not.toContain('FRE 902(11)');
  });
});
