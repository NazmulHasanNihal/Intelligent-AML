/**
 * matcher.ts — Multi-Algorithm Entity Screening & Scoring Engine (TypeScript Client/BFF Mirror)
 * Guarantees that client-side demo and API screening match the Python engine calculations identically.
 */

import { normalizeEntityName, getTokenBag, getNameOrderPermutations } from './normalizer';

export interface ScreeningThresholdConfig {
  autoFreezeThreshold: number; // default: 85.0
  quarantineThreshold: number;  // default: 65.0
  weightJaroWinkler: number;    // default: 0.40
  weightTokenSet: number;       // default: 0.40
  weightPhonetic: number;       // default: 0.20
  dobMatchBonus: number;        // default: +10.0
  dobMismatchPenalty: number;   // default: -15.0
  countryMatchBonus: number;    // default: +5.0
  identifierMatchBonus: number; // default: +25.0
}

export const DEFAULT_THRESHOLDS: ScreeningThresholdConfig = {
  autoFreezeThreshold: 85.0,
  quarantineThreshold: 65.0,
  weightJaroWinkler: 0.40,
  weightTokenSet: 0.40,
  weightPhonetic: 0.20,
  dobMatchBonus: 10.0,
  dobMismatchPenalty: 15.0,
  countryMatchBonus: 5.0,
  identifierMatchBonus: 25.0
};

export interface MatchResult {
  matchScore: number;
  algorithmBreakdown: {
    jaroWinklerScore: number;
    tokenSetScore: number;
    phoneticScore: number;
    corroborationAdjustment: number;
  };
  corroborationDetails: {
    dobStatus: string;
    countryStatus: string;
    idStatus: string;
  };
  matchType: string;
  disposition: 'CONFIRMED_TRUE_HIT' | 'PENDING_REVIEW' | 'DISMISSED_FALSE_POSITIVE';
  tokenDiffs: {
    screenedTokens: string[];
    matchedTokens: string[];
    commonTokens: string[];
  };
  screenedName: string;
  matchedEntity: string;
}

export function jaroSimilarity(s1: string, s2: string): number {
  if (!s1 && !s2) return 1.0;
  if (!s1 || !s2) return 0.0;
  if (s1 === s2) return 1.0;

  const len1 = s1.length;
  const len2 = s2.length;
  const maxDist = Math.max(0, Math.floor(Math.max(len1, len2) / 2) - 1);

  const s1Matches = new Array<boolean>(len1).fill(false);
  const s2Matches = new Array<boolean>(len2).fill(false);

  let matches = 0;
  let transpositions = 0;

  for (let i = 0; i < len1; i++) {
    const start = Math.max(0, i - maxDist);
    const end = Math.min(i + maxDist + 1, len2);
    for (let j = start; j < end; j++) {
      if (s2Matches[j]) continue;
      if (s1[i] !== s2[j]) continue;
      s1Matches[i] = true;
      s2Matches[j] = true;
      matches++;
      break;
    }
  }

  if (matches === 0) return 0.0;

  let k = 0;
  for (let i = 0; i < len1; i++) {
    if (!s1Matches[i]) continue;
    while (!s2Matches[k]) {
      k++;
    }
    if (s1[i] !== s2[k]) {
      transpositions++;
    }
    k++;
  }

  transpositions = Math.floor(transpositions / 2);
  return (matches / len1 + matches / len2 + (matches - transpositions) / matches) / 3.0;
}

export function jaroWinklerSimilarity(
  s1: string,
  s2: string,
  prefixWeight: number = 0.1,
  maxPrefix: number = 4
): number {
  const jSim = jaroSimilarity(s1, s2);
  if (jSim < 0.7) return jSim;

  let prefixLen = 0;
  const limit = Math.min(s1.length, s2.length, maxPrefix);
  for (let i = 0; i < limit; i++) {
    if (s1[i] === s2[i]) {
      prefixLen++;
    } else {
      break;
    }
  }

  return jSim + prefixLen * prefixWeight * (1.0 - jSim);
}

export function tokenSetSimilarity(s1: string, s2: string): number {
  const t1 = new Set(getTokenBag(s1));
  const t2 = new Set(getTokenBag(s2));

  if (t1.size === 0 || t2.size === 0) return 0.0;

  const intersection = new Set([...t1].filter((x) => t2.has(x)));
  const diff1 = new Set([...t1].filter((x) => !t2.has(x)));
  const diff2 = new Set([...t2].filter((x) => !t1.has(x)));

  if (diff1.size === 0 && diff2.size === 0) return 1.0;

  const sortedIntersect = [...intersection].sort().join(' ');
  const sortedDiff1 = [...diff1].sort().join(' ');
  const sortedDiff2 = [...diff2].sort().join(' ');

  const comb1 = (sortedIntersect + ' ' + sortedDiff1).trim();
  const comb2 = (sortedIntersect + ' ' + sortedDiff2).trim();

  const scores = [
    sortedIntersect ? jaroWinklerSimilarity(sortedIntersect, comb1) : 0,
    sortedIntersect ? jaroWinklerSimilarity(sortedIntersect, comb2) : 0,
    jaroWinklerSimilarity(comb1, comb2)
  ];

  return Math.max(...scores);
}

export function soundex(text: string): string {
  if (!text) return 'Z000';
  const cleaned = text.toUpperCase().replace(/[^A-Z]/g, '');
  if (!cleaned) return 'Z000';

  const mapping: Record<string, string> = {
    B: '1', F: '1', P: '1', V: '1',
    C: '2', G: '2', J: '2', K: '2', Q: '2', S: '2', X: '2', Z: '2',
    D: '3', T: '3',
    L: '4',
    M: '5', N: '5',
    R: '6'
  };

  const firstChar = cleaned[0]!;
  const encoded: string[] = [firstChar];
  let prevCode = mapping[firstChar] || '';

  for (let i = 1; i < cleaned.length; i++) {
    const char = cleaned[i]!;
    const code = mapping[char] || '';
    if (code) {
      if (code !== prevCode) {
        encoded.push(code);
      }
      prevCode = code;
    } else {
      prevCode = '';
    }
  }

  const result = encoded.join('').slice(0, 4);
  return result.padEnd(4, '0');
}

export function phoneticSimilarity(s1: string, s2: string): number {
  const t1 = getTokenBag(s1);
  const t2 = getTokenBag(s2);

  if (t1.length === 0 || t2.length === 0) return 0.0;

  const sx1 = t1.map((t) => soundex(t));
  const sx2 = t2.map((t) => soundex(t));

  const matched = sx1.filter((s) => sx2.includes(s)).length;
  const maxTokens = Math.max(sx1.length, sx2.length);

  return maxTokens > 0 ? matched / maxTokens : 0.0;
}

export function computeScreeningScore(
  queryName: string,
  targetName: string,
  options?: {
    queryDob?: string | null;
    targetDob?: string | null;
    queryCountry?: string | null;
    targetCountry?: string | null;
    queryId?: string | null;
    targetId?: string | null;
    config?: Partial<ScreeningThresholdConfig>;
  }
): MatchResult {
  const cfg = { ...DEFAULT_THRESHOLDS, ...(options?.config || {}) };

  const normQuery = normalizeEntityName(queryName);
  const normTarget = normalizeEntityName(targetName);

  let jwScore = 0.0;
  let tokenScore = 0.0;
  let phoneticScore = 0.0;
  let matchType = 'LOW_SIMILARITY';

  if (normQuery === normTarget && normQuery !== '') {
    jwScore = 100.0;
    tokenScore = 100.0;
    phoneticScore = 100.0;
    matchType = 'EXACT_NAME_MATCH';
  } else {
    const queryPerms = getNameOrderPermutations(queryName);
    const targetPerms = getNameOrderPermutations(targetName);

    let isWordReversal = false;
    for (const qp of queryPerms) {
      if (targetPerms.includes(qp) && qp !== '') {
        isWordReversal = true;
        break;
      }
    }

    const jwRaw = jaroWinklerSimilarity(normQuery, normTarget);
    jwScore = jwRaw * 100.0;

    const tokenRaw = tokenSetSimilarity(queryName, targetName);
    tokenScore = tokenRaw * 100.0;

    const phoneticRaw = phoneticSimilarity(queryName, targetName);
    phoneticScore = phoneticRaw * 100.0;

    if (isWordReversal) {
      matchType = 'WORD_REVERSAL_PERMUTATION';
    } else if (jwScore >= 88.0 && tokenScore >= 88.0) {
      matchType = 'FUZZY_JARO_WINKLER';
    } else if (phoneticScore >= 75.0 && jwScore >= 70.0) {
      matchType = 'PHONETIC_SOUNDEX';
    } else if (tokenScore >= 70.0) {
      matchType = 'TOKEN_SET_PARTIAL';
    }
  }

  const baseScore =
    cfg.weightJaroWinkler * jwScore +
    cfg.weightTokenSet * tokenScore +
    cfg.weightPhonetic * phoneticScore;

  let corroborationAdj = 0.0;
  const corroborationDetails = {
    dobStatus: 'NOT_PROVIDED',
    countryStatus: 'NOT_PROVIDED',
    idStatus: 'NOT_PROVIDED'
  };

  // Identifier Corroboration
  if (options?.queryId && options?.targetId) {
    const cleanQid = options.queryId.replace(/[-\s]/g, '').toUpperCase();
    const cleanTid = options.targetId.replace(/[-\s]/g, '').toUpperCase();
    if (cleanQid === cleanTid && cleanQid !== '') {
      corroborationAdj += cfg.identifierMatchBonus;
      corroborationDetails.idStatus = 'EXACT_MATCH';
    } else {
      corroborationDetails.idStatus = 'MISMATCH';
    }
  }

  // DOB Corroboration
  if (options?.queryDob && options?.targetDob) {
    if (options.queryDob === options.targetDob) {
      corroborationAdj += cfg.dobMatchBonus;
      corroborationDetails.dobStatus = 'EXACT_MATCH';
    } else {
      corroborationAdj -= cfg.dobMismatchPenalty;
      corroborationDetails.dobStatus = 'MISMATCH_PENALTY';
    }
  }

  // Country Corroboration
  if (options?.queryCountry && options?.targetCountry) {
    if (options.queryCountry.trim().toLowerCase() === options.targetCountry.trim().toLowerCase()) {
      corroborationAdj += cfg.countryMatchBonus;
      corroborationDetails.countryStatus = 'MATCH';
    } else {
      corroborationDetails.countryStatus = 'DIFFERENT_JURISDICTION';
    }
  }

  const finalScore = Math.max(0.0, Math.min(100.0, baseScore + corroborationAdj));

  const qTokens = getTokenBag(queryName);
  const tTokens = getTokenBag(targetName);
  const commonTokens = qTokens.filter((x) => tTokens.includes(x)).sort();

  let disposition: 'CONFIRMED_TRUE_HIT' | 'PENDING_REVIEW' | 'DISMISSED_FALSE_POSITIVE' = 'DISMISSED_FALSE_POSITIVE';
  if (finalScore >= cfg.autoFreezeThreshold) {
    disposition = 'CONFIRMED_TRUE_HIT';
  } else if (finalScore >= cfg.quarantineThreshold) {
    disposition = 'PENDING_REVIEW';
  }

  return {
    matchScore: Number(finalScore.toFixed(1)),
    algorithmBreakdown: {
      jaroWinklerScore: Number(jwScore.toFixed(1)),
      tokenSetScore: Number(tokenScore.toFixed(1)),
      phoneticScore: Number(phoneticScore.toFixed(1)),
      corroborationAdjustment: Number(corroborationAdj.toFixed(1))
    },
    corroborationDetails,
    matchType,
    disposition,
    tokenDiffs: {
      screenedTokens: qTokens,
      matchedTokens: tTokens,
      commonTokens
    },
    screenedName: queryName,
    matchedEntity: targetName
  };
}
