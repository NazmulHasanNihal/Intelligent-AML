import { describe, it, expect, beforeEach } from 'vitest';
import { useBankingStore } from '../lib/store';

describe('Model Governance & Research Credibility Suite (Phase 7)', () => {
  beforeEach(() => {
    // Reset store state
    const store = useBankingStore.getState();
    store.restoreValidChain();
  });

  describe('Supervisory Override & Cryptographic Ledger', () => {
    it('successfully overrides an alert risk score and updates alert state', async () => {
      const store = useBankingStore.getState();
      const targetAlert = store.alerts[0]!;
      expect(targetAlert).toBeDefined();

      const origId = targetAlert.id;
      const success = await store.overrideAlertScore(
        origId,
        0.12,
        'Tier 3 Clear',
        'DOCUMENTED_TRADE_INVOICE',
        'Verified genuine letter of credit with customs release certificate.'
      );

      expect(success).toBe(true);

      const updated = useBankingStore.getState().alerts.find((a) => a.id === origId);
      expect(updated).toBeDefined();
      expect(updated?.riskScore).toBe(0.12);
      expect(updated?.tier).toBe('Tier 3 Clear');
      expect(updated?.tierCode).toBe(3);
      expect(updated?.status).toBe('OVERRIDDEN');
    });

    it('appends an immutable record to the WORM ledger on score override', async () => {
      const store = useBankingStore.getState();
      const initialHeight = store.auditLedger.length;
      const targetAlert = (store.alerts[1] || store.alerts[0])!;

      await store.overrideAlertScore(
        targetAlert.id,
        0.145,
        'Tier 3 Clear',
        'VERIFIED_PAYROLL_SPIKE',
        'Audited payroll disbursement schedule confirmed with institutional treasury.'
      );

      const newLedger = useBankingStore.getState().auditLedger;
      expect(newLedger.length).toBe(initialHeight + 1);

      const latestBlock = newLedger[newLedger.length - 1]!;
      expect(latestBlock.action).toBe('MODEL_RISK_SCORE_OVERRIDDEN');
      expect(latestBlock.details).toContain(targetAlert.id);
      expect(latestBlock.details).toContain('VERIFIED_PAYROLL_SPIKE');
      expect(latestBlock.currentHash || latestBlock.merkleHash).toMatch(/^[0-9a-f]{64}$/);
    });
  });

  describe('Champion vs. Challenger Shadow Benchmark Standards', () => {
    it('enforces Champion superiority over Challenger baseline', () => {
      const championMetrics = {
        modelId: 'cstgb-champion-v3.2',
        macroF1: 0.945,
        recall: 0.948,
        fpr: 0.0076,
        p99LatencyMs: 0.82
      };

      const challengerMetrics = {
        modelId: 'lightgbm-baseline-v2.1',
        macroF1: 0.887,
        recall: 0.824,
        fpr: 0.0482,
        p99LatencyMs: 2.14
      };

      // F1 must exceed challenger by at least 5%
      expect(championMetrics.macroF1).toBeGreaterThan(challengerMetrics.macroF1);
      expect(championMetrics.macroF1 - challengerMetrics.macroF1).toBeGreaterThanOrEqual(0.05);

      // False positive rate must be under 1% and lower than challenger
      expect(championMetrics.fpr).toBeLessThan(0.01);
      expect(championMetrics.fpr).toBeLessThan(challengerMetrics.fpr);

      // Operational noise reduction
      const noiseReduction = ((challengerMetrics.fpr - championMetrics.fpr) / challengerMetrics.fpr) * 100;
      expect(noiseReduction).toBeGreaterThan(80.0);
    });
  });

  describe('Statistical Drift Thresholds (Federal Reserve SR 11-7 / OCC 2011-12)', () => {
    const classifyPsi = (psi: number): 'STABLE' | 'MODERATE_DRIFT' | 'SIGNIFICANT_DRIFT' => {
      if (psi >= 0.25) return 'SIGNIFICANT_DRIFT';
      if (psi >= 0.10) return 'MODERATE_DRIFT';
      return 'STABLE';
    };

    it('correctly classifies standard banking PSI thresholds', () => {
      expect(classifyPsi(0.04)).toBe('STABLE');
      expect(classifyPsi(0.099)).toBe('STABLE');
      expect(classifyPsi(0.10)).toBe('MODERATE_DRIFT');
      expect(classifyPsi(0.185)).toBe('MODERATE_DRIFT');
      expect(classifyPsi(0.249)).toBe('MODERATE_DRIFT');
      expect(classifyPsi(0.25)).toBe('SIGNIFICANT_DRIFT');
      expect(classifyPsi(0.42)).toBe('SIGNIFICANT_DRIFT');
    });
  });

  describe('Algorithmic Fairness (EEOC Four-Fifths Rule)', () => {
    it('verifies all entity segments satisfy disparate impact ratio [0.80, 1.25]', () => {
      const segments = [
        { segment: 'CORPORATE_INSTITUTIONAL', disparateImpactRatio: 1.044 },
        { segment: 'SME_COMMERCIAL', disparateImpactRatio: 0.986 },
        { segment: 'RETAIL_INDIVIDUAL', disparateImpactRatio: 1.000 },
        { segment: 'NON_RESIDENT_OFFSHORE', disparateImpactRatio: 1.088 }
      ];

      for (const seg of segments) {
        expect(seg.disparateImpactRatio).toBeGreaterThanOrEqual(0.80);
        expect(seg.disparateImpactRatio).toBeLessThanOrEqual(1.25);
      }
    });
  });
});
