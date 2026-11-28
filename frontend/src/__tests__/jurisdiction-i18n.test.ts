import { describe, it, expect } from 'vitest';
import { JURISDICTIONS } from '@/lib/compliance/jurisdictions';
import { TRANSLATIONS } from '@/lib/i18n/translations';
import { formatCurrencyAmount } from '@/lib/i18n/formatters';

describe('Jurisdiction Isolation & Localization Parity', () => {
  it('isolates BD_BFIU statutory profile with zero US FRE/CFPB references', () => {
    const bd = JURISDICTIONS.BD_BFIU;
    const serialized = JSON.stringify(bd);
    expect(bd.evidenceRule).toContain('Bangladesh Evidence Act');
    expect(bd.statutoryAct).toContain('Money Laundering Prevention Act, 2012');
    expect(serialized).not.toContain('FRE 902(11)');
    expect(serialized).not.toContain('CFPB');
    expect(serialized).not.toContain('FinCEN');
  });

  it('maintains distinct US_FINCEN and EU_AMLA statutory profiles', () => {
    expect(JURISDICTIONS.US_FINCEN.evidenceRule).toContain('902(11)');
    expect(JURISDICTIONS.US_FINCEN.ctrThresholdNative).toBe(10000);
    expect(JURISDICTIONS.EU_AMLA.statutoryAct).toContain('6AMLD');
    expect(JURISDICTIONS.EU_AMLA.currency).toBe('EUR');
  });

  it('keeps complete en/bn i18n keys and BDT/USD digit formatting', () => {
    expect(Object.keys(TRANSLATIONS.en).sort()).toEqual(Object.keys(TRANSLATIONS.bn).sort());
    expect(formatCurrencyAmount(5820000, 'BDT', 'en')).toBe('৳58,20,000');
    expect(formatCurrencyAmount(5820000, 'USD', 'en')).toBe('$48,500.00');
    expect(formatCurrencyAmount(5820000, 'BDT', 'bn')).toBe('৳৫৮,২০,০০০');
  });
});
