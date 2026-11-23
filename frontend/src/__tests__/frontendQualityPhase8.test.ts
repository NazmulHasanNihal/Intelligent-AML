import { describe, it, expect } from 'vitest';
import { TRANSLATIONS } from '../lib/i18n/translations';
import { toBengaliDigits, formatCurrencyAmount, formatDualCurrency } from '../lib/i18n/formatters';
import robots from '../app/robots';
import sitemap from '../app/sitemap';
import { REGULATORY_CONFIG } from '../lib/config/regulatory';

describe('Phase 8: Frontend Quality, i18n, Currency & Site Structure Suite', () => {
  describe('1. Internationalization (i18n) Dictionary Completeness', () => {
    it('contains identical translation keys across English and Bangla dictionaries', () => {
      const enKeys = Object.keys(TRANSLATIONS.en).sort();
      const bnKeys = Object.keys(TRANSLATIONS.bn).sort();

      expect(enKeys).toEqual(bnKeys);
      expect(enKeys.length).toBeGreaterThan(30);
    });

    it('translates all 11 compliance modules accurately in Bangla', () => {
      expect(TRANSLATIONS.bn.nav_overview).toContain('১. নির্বাহী নজরদারি');
      expect(TRANSLATIONS.bn.nav_triage).toContain('২. সতর্কতা বাছাই');
      expect(TRANSLATIONS.bn.nav_screening).toContain('৩. নিষেধাজ্ঞা ও পিইপি বাছাই');
      expect(TRANSLATIONS.bn.nav_cases).toContain('৫. প্রাতিষ্ঠানিক মামলা');
      expect(TRANSLATIONS.bn.nav_sar).toContain('৮. এসটিআর ও সিটিআর ডকেট');
      expect(TRANSLATIONS.bn.nav_governance).toContain('১১. মডেল গভর্নেন্স ও অডিট লেজার');
    });

    it('translates key regulatory terminology accurately', () => {
      expect(TRANSLATIONS.bn.tier1_hold).toBe('স্তর ১ স্থগিত');
      expect(TRANSLATIONS.bn.tier2_review).toBe('স্তর ২ পর্যালোচনা');
      expect(TRANSLATIONS.bn.tier3_clear).toBe('স্তর ৩ ছাড়');
      expect(TRANSLATIONS.bn.maker_checker).toBe('মেকার-চেকার দ্বৈত নিয়ন্ত্রণ');
    });
  });

  describe('2. Currency Formatting & Conversion Engine', () => {
    it('converts Western numbers to Bengali digits correctly', () => {
      expect(toBengaliDigits('1234567890')).toBe('১২৩৪৫৬৭৮৯০');
      expect(toBengaliDigits('1,000,000')).toBe('১,০০০,০০০');
    });

    it('formats BDT currency in English with Indian/Bangla comma notation and ৳ symbol', () => {
      const formatted = formatCurrencyAmount(1000000, 'BDT', 'en');
      expect(formatted).toBe('৳10,00,000');
    });

    it('formats BDT currency in Bangla using Eastern Bengali numerals', () => {
      const formatted = formatCurrencyAmount(1000000, 'BDT', 'bn');
      expect(formatted).toBe('৳১০,০০,০০০');
    });

    it('converts BDT to USD at the dated official Bangladesh Bank rate (120.00 BDT/USD)', () => {
      // ৳1,200,000 BDT = $10,000.00 USD
      const usdEnglish = formatCurrencyAmount(1200000, 'USD', 'en');
      expect(usdEnglish).toBe('$10,000.00');

      const usdBangla = formatCurrencyAmount(1200000, 'USD', 'bn');
      expect(usdBangla).toBe('$১০,০০০.০০');
    });

    it('generates accurate dual-currency breakdowns', () => {
      const dual = formatDualCurrency(600000, 'en');
      expect(dual.primary).toBe('৳6,00,000');
      expect(dual.secondary).toBe('$5,000.00');
    });
  });

  describe('3. SEO Metadata, Sitemap & Robots.txt Directives', () => {
    it('generates dynamic sitemap.xml with landing page prioritized', () => {
      const map = sitemap();
      expect(map).toHaveLength(1);
      expect(map[0]!.url).toBe('https://intelligent-aml.vercel.app');
      expect(map[0]!.priority).toBe(1.0);
    });

    it('generates dynamic crawler rules respecting reversible audit mode and public governance', () => {
      const bot = robots();
      expect(bot.sitemap).toBe('https://intelligent-aml.vercel.app/sitemap.xml');
      expect(bot.rules).toBeDefined();

      const rule = Array.isArray(bot.rules) ? bot.rules[0] : bot.rules;
      const allows = Array.isArray(rule?.allow) ? rule?.allow : [rule?.allow];
      expect(allows).toContain('/');
      expect(allows).toContain('/governance');

      const disallows = Array.isArray(rule?.disallow) ? rule?.disallow : [rule?.disallow];
      expect(disallows).toContain('/api/');
    });
  });

  describe('4. Regulatory Baseline Consistency', () => {
    it('verifies CTR threshold and exchange rate match official BFIU policies', () => {
      expect(REGULATORY_CONFIG.ctrPolicy.thresholdBdt).toBe(1000000);
      expect(REGULATORY_CONFIG.fxRatePolicy.usdToBdt).toBe(120.00);
      expect(REGULATORY_CONFIG.statuteReferences.primaryAmlAct.title).toContain('Money Laundering Prevention Act, 2012');
    });
  });
});
