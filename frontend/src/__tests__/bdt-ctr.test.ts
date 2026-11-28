import { describe, it, expect } from 'vitest';
import { INITIAL_ALERTS } from '@/lib/data/commercialSeed';
import { REGULATORY_CONFIG } from '@/lib/config/regulatory';

describe('BDT Statutory CTR vs TBML Separation Integrity', () => {
  it('enforces BFIU ৳1,000,000 cash CTR limit', () => {
    expect(REGULATORY_CONFIG.ctrPolicy.thresholdBdt).toBe(1000000);
    expect(REGULATORY_CONFIG.structuringPolicy.upperBoundBdt).toBe(999999);
  });

  it('separates ALT-994821 ($48,500 / ৳5,820,000 TBML) without mislabeling as below CTR threshold', () => {
    const tbmlAlert = INITIAL_ALERTS.find((a) => a.id === 'ALT-994821');
    expect(tbmlAlert).toBeDefined();
    expect(tbmlAlert!.amount).toBe(48500);
    expect(tbmlAlert!.amountBdt).toBe(5820000);
    expect(tbmlAlert!.tbmlData?.priceDeviationPct).toBeCloseTo(333.7, 1);
    expect(tbmlAlert!.whyFlagged.toLowerCase()).not.toContain('below');
    expect(tbmlAlert!.whyFlagged.toLowerCase()).not.toContain('under internal $10,000');
  });

  it('flags ALT-994824 ($7,950 / ৳954,000) cleanly for multi-branch cash structuring below ৳1,000,000 CTR', () => {
    const cashAlert = INITIAL_ALERTS.find((a) => a.id === 'ALT-994824');
    expect(cashAlert).toBeDefined();
    expect(cashAlert!.amount).toBe(7950);
    expect(cashAlert!.amountBdt).toBe(954000);
    expect(cashAlert!.amountBdt).toBeLessThan(REGULATORY_CONFIG.ctrPolicy.thresholdBdt);
    expect(cashAlert!.whyFlagged).toContain('৳1,000,000 BDT');
  });
});
