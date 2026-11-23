import { describe, it, expect } from 'vitest';
import {
  stripDiacritics,
  stripLegalSuffixes,
  standardizeBanglaTransliteration,
  normalizeEntityName,
  getNameOrderPermutations
} from '../lib/screening/normalizer';
import {
  jaroSimilarity,
  jaroWinklerSimilarity,
  tokenSetSimilarity,
  soundex,
  phoneticSimilarity,
  computeScreeningScore
} from '../lib/screening/matcher';
import {
  OFFICIAL_WATCHLIST_FEEDS,
  screenWatchlistCandidate
} from '../lib/screening/watchlistRegistry';

describe('Screening Fidelity & Multi-Algorithm Entity Resolution Suite', () => {
  describe('Normalization Pipeline', () => {
    it('strips unicode diacritics and non-spacing marks correctly', () => {
      expect(stripDiacritics('Müller')).toBe('Muller');
      expect(stripDiacritics('François')).toBe('Francois');
      expect(stripDiacritics('Łódź')).toBe('Lodz');
      expect(stripDiacritics('São Paulo')).toBe('Sao Paulo');
    });

    it('strips corporate legal entity suffixes from various jurisdictions', () => {
      expect(stripLegalSuffixes(['gulf', 'star', 'commodities', 'fze'])).toEqual([
        'gulf',
        'star',
        'commodities'
      ]);
      expect(stripLegalSuffixes(['helvetia', 'metallurgical', 'trading', 'ag'])).toEqual([
        'helvetia',
        'metallurgical'
      ]);
      expect(stripLegalSuffixes(['singapore', 'shipping', 'pte', 'ltd'])).toEqual([
        'singapore'
      ]);
    });

    it('standardizes Bangla-to-Latin transliteration variations', () => {
      expect(standardizeBanglaTransliteration('md. farhan ahmed')).toBe('mohammed farhan ahmed');
      expect(standardizeBanglaTransliteration('seikh rohman')).toBe('sheikh rahman');
      expect(standardizeBanglaTransliteration('choudhury kahn')).toBe('chowdhury khan');
      expect(standardizeBanglaTransliteration('hussain haque')).toBe('hossain haq');
    });

    it('generates name order permutations for reversed patronymics', () => {
      const perms = getNameOrderPermutations('Hasan, Nazmul');
      expect(perms.some((p) => p.includes('nazmul') && p.includes('hassan'))).toBe(true);
    });
  });

  describe('Multi-Algorithm Matching & Corroboration', () => {
    it('computes Jaro-Winkler similarity with prefix scaling', () => {
      expect(jaroWinklerSimilarity('GULF STAR', 'GULF STAR')).toBe(1.0);
      expect(jaroWinklerSimilarity('', 'TEST')).toBe(0.0);
      const sim = jaroWinklerSimilarity('GULF STAR COMMODITIES', 'GULF STAR TRADING');
      expect(sim).toBeGreaterThan(0.7);
      expect(sim).toBeLessThan(0.95);
    });

    it('achieves permutation invariance via token-set similarity', () => {
      const score = tokenSetSimilarity('Farhan Ahmed Kazi', 'Kazi Farhan Ahmed');
      expect(score).toBeGreaterThanOrEqual(0.95);
    });

    it('encodes phonetically equivalent names using Soundex', () => {
      expect(soundex('Sheikh')).toBe(soundex('Seikh'));
      expect(soundex('Khan')).toBe(soundex('Kahn'));
    });

    it('applies corroboration bonuses for matching DOB and country, and penalties for mismatch', () => {
      const base = computeScreeningScore('Mohammed Farooq Sheikh', 'Sheikh Mohammed Faruk');

      const boosted = computeScreeningScore('Mohammed Farooq Sheikh', 'Sheikh Mohammed Faruk', {
        queryDob: '1974-06-15',
        targetDob: '1974-06-15',
        queryCountry: 'Pakistan',
        targetCountry: 'Pakistan'
      });
      expect(boosted.matchScore).toBeGreaterThan(base.matchScore);
      expect(boosted.corroborationDetails.dobStatus).toBe('EXACT_MATCH');
      expect(boosted.corroborationDetails.countryStatus).toBe('MATCH');

      const penalized = computeScreeningScore('Mohammed Farooq Sheikh', 'Sheikh Mohammed Faruk', {
        queryDob: '1995-12-01',
        targetDob: '1974-06-15'
      });
      expect(penalized.matchScore).toBeLessThan(base.matchScore);
      expect(penalized.corroborationDetails.dobStatus).toBe('MISMATCH_PENALTY');
    });
  });

  describe('Official Watchlist Registry & Engine Parity', () => {
    it('contains all 5 official watchlist feeds with valid SHA-256 hashes and versions', () => {
      const feeds = Object.values(OFFICIAL_WATCHLIST_FEEDS);
      const feedIds = feeds.map((f) => f.listId);
      expect(feedIds).toContain('OFAC_SDN');
      expect(feedIds).toContain('UN_CONSOLIDATED');
      expect(feedIds).toContain('EU_CONSOLIDATED');
      expect(feedIds).toContain('UK_HMT');
      expect(feedIds).toContain('BFIU_DOMESTIC');

      for (const feed of feeds) {
        expect(feed.version).toBeTruthy();
        expect(feed.sha256Hash).toHaveLength(64);
        expect(feed.fetchTimestamp).toContain('Z');
        expect(feed.totalRecords).toBeGreaterThan(0);
        expect(feed.status).toBe('SYNCED_VERIFIED');
      }
    });

    it('acceptance: demo candidate screening match score equals what the engine computes', () => {
      // Direct pair scoring parity with Python engine calculation (93.8%)
      const directPair = computeScreeningScore(
        'Gulf Star Commodities FZE',
        'Gulf Star Trading & Logistics LLC',
        {
          queryCountry: 'United Arab Emirates',
          targetCountry: 'United Arab Emirates'
        }
      );
      expect(directPair.matchScore).toBe(93.8);
      expect(directPair.disposition).toBe('CONFIRMED_TRUE_HIT');
      expect(directPair.algorithmBreakdown.tokenSetScore).toBe(100.0);
      expect(directPair.algorithmBreakdown.corroborationAdjustment).toBe(5.0);

      // Full entity resolution scan returns top hit
      const hits = screenWatchlistCandidate('Gulf Star Commodities FZE', {
        country: 'United Arab Emirates'
      });
      expect(hits.length).toBeGreaterThan(0);

      const topHit = hits[0]!;
      expect(topHit.entityId).toBe('OFAC-SDN-19482');
      expect(topHit.matchScore).toBeGreaterThanOrEqual(93.8);
      expect(topHit.disposition).toBe('CONFIRMED_TRUE_HIT');
    });
  });
});
