import { describe, it, expect } from 'vitest';
import { NextRequest } from 'next/server';
import { POST as signoffPost } from '@/app/api/v1/cases/[caseId]/signoff/route';
import { POST as sarPost } from '@/app/api/v1/sar/route';
import { canApproveCase, canRevealPii } from '@/lib/auth/session';

describe('Server-Side RBAC & Four-Eyes Maker-Checker Controls', () => {
  it('enforces separation of duties on POST /api/v1/cases/[caseId]/signoff', async () => {
    const selfReq = new NextRequest('http://localhost/api/v1/cases/CASE-2026-0881/signoff', {
      method: 'POST',
      body: JSON.stringify({
        actionType: 'ACCOUNT_FREEZE',
        makerId: 'BNK-4419',
        makerRole: 'ANALYST_L2',
        checkerId: 'BNK-4419',
        checkerRole: 'MLRO_CAMLCO',
        justificationCode: 'BFIU-SEC-15',
        operationalRationale: 'Dual verification rationale over fifteen chars.',
        evidenceDossierHash: 'a'.repeat(64),
      }),
    });

    const blocked = await signoffPost(selfReq, { params: Promise.resolve({ caseId: 'CASE-2026-0881' }) });
    expect(blocked.status).toBe(403);
  });

  it('enforces separation of duties on POST /api/v1/sar', async () => {
    const selfSar = new NextRequest('http://localhost/api/v1/sar', {
      method: 'POST',
      body: JSON.stringify({
        caseId: 'CASE-2026-0881',
        reportType: 'STR',
        jurisdiction: 'BD_BFIU',
        makerId: 'BNK-7842',
        checkerId: 'BNK-7842',
        narrative: 'Substantive MLPA 2012 § 25 investigator narrative exceeding 20 characters.',
      }),
    });

    const res = await sarPost(selfSar);
    expect(res.status).toBe(403);
  });

  it('prevents ANALYST_L1 and AUDITOR from PII unmasking or case ratification', () => {
    expect(canApproveCase('ANALYST_L1')).toBe(false);
    expect(canRevealPii('ANALYST_L1')).toBe(false);
    expect(canApproveCase('AUDITOR')).toBe(false);
    expect(canRevealPii('AUDITOR')).toBe(false);
    expect(canApproveCase('MLRO_CAMLCO')).toBe(true);
  });
});
