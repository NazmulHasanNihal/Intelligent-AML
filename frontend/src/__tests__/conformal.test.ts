import { describe, it, expect } from 'vitest';
import { NextRequest } from 'next/server';
import { CONFORMAL_CALIBRATION } from '@/lib/scoringEngine';
import { POST as scorePost } from '@/app/api/v1/score/route';

describe('Conformal Prediction & Coverage Calibration', () => {
  it('enforces valid finite-sample conformal quantiles (q0 < q1, alpha = 0.01)', () => {
    expect(CONFORMAL_CALIBRATION.q0).toBeGreaterThan(0);
    expect(CONFORMAL_CALIBRATION.q1).toBeGreaterThan(CONFORMAL_CALIBRATION.q0);
    expect(CONFORMAL_CALIBRATION.q1).toBeLessThan(1);
  });

  it('classifies extreme TBML divergence into singleton Tier 1 Hold Γ = {1}', async () => {
    const req = new NextRequest('http://localhost/api/v1/score', {
      method: 'POST',
      body: JSON.stringify({
        amount: 48500,
        sourceAccount: 'BD22-EBLB-4829-1092-8823',
        targetAccount: 'AE-EBIL-1109-8421-4402',
        rail: 'SWIFT MT700 (LC)',
        burst: true,
        crossBorder: true,
        tbmlData: {
          declaredUnitValuation: 42.5,
          benchmarkValuation: 9.8,
          hsCode: 'HS 5201.00',
        },
      }),
    });

    const res = await scorePost(req);
    expect(res.status).toBe(200);
    const json = await res.json();
    expect(json.tierCode).toBe(1);
    expect(json.conformalSet).toBe('Γ = {1}');
    expect(json.rawProbability).toBeGreaterThan(0.95);
  });

  it('classifies low-risk domestic settlement within Tier 3 Clear Γ = {0} or bounded review', async () => {
    const req = new NextRequest('http://localhost/api/v1/score', {
      method: 'POST',
      body: JSON.stringify({
        amount: 1200,
        sourceAccount: 'BD22-APEX-PAYROLL-01',
        targetAccount: 'BD22-STAFF-0092',
        rail: 'BEFTN',
        burst: false,
        crossBorder: false,
      }),
    });

    const res = await scorePost(req);
    expect(res.status).toBe(200);
    const json = await res.json();
    expect([2, 3]).toContain(json.tierCode);
    expect(json.rawProbability).toBeLessThan(0.2);
  });
});
