import { describe, it, expect } from 'vitest';
import {
  compute12DInvariants,
  evaluateEdgeTrust,
  scoreTransactionWithCSTGB,
  CONFORMAL_CALIBRATION
} from '../lib/scoringEngine';

describe('C-STGB Mathematical Scoring Engine', () => {
  it('computes 12D invariants correctly for structuring transaction', () => {
    const tx = {
      amount: 9450,
      burst: true,
      crossBorder: true
    };
    const inv = compute12DInvariants(tx);
    expect(inv.isStructuring).toBe(true);
    expect(inv.phiFlow).toBeGreaterThan(0);
    expect(inv.sFwd).toBe(0.842);
    expect(inv.vA).toBeGreaterThan(0);
  });

  it('prunes camouflage chaff edges with low edge trust gate', () => {
    const chaffEdge = {
      amount: 45,
      rail: 'POS Retail',
      isCamouflage: true
    };
    const result = evaluateEdgeTrust(chaffEdge, 0.10);
    expect(result.gHat).toBeLessThan(0.20);
    expect(result.isPruned).toBe(true);
  });

  it('preserves legitimate and high-risk structural flows', () => {
    const structuredEdge = {
      amount: 9600,
      rail: 'SWIFT MT103',
      isLoop: true
    };
    const result = evaluateEdgeTrust(structuredEdge, 0.10);
    expect(result.gHat).toBeGreaterThan(0.80);
    expect(result.isPruned).toBe(false);
  });

  it('routes high-risk transactions into Tier 1 Quarantine', () => {
    const suspiciousTx = {
      amount: 9450,
      burst: true,
      crossBorder: true,
      rail: 'SWIFT MT700 (LC)'
    };
    const scored = scoreTransactionWithCSTGB(suspiciousTx);
    expect(scored.riskScore).toBeGreaterThan(0.70);
    expect(scored.tierCode).toBe(1);
    expect(scored.tierLabel).toContain('Tier 1');
    expect(scored.conformalSet).toEqual(['Illicit']);
  });

  it('clears low-risk domestic transactions straight through into Tier 3', () => {
    const normalTx = {
      amount: 1500,
      burst: false,
      crossBorder: false,
      rail: 'BEFTN'
    };
    const scored = scoreTransactionWithCSTGB(normalTx);
    expect(scored.riskScore).toBeLessThan(0.40);
    expect(scored.tierCode).toBe(3);
    expect(scored.conformalSet).toEqual(['Licit']);
  });
});
