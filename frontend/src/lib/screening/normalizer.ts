/**
 * normalizer.ts — Entity Normalization Engine (TypeScript Client/BFF Mirror)
 * Normalizes input entity and person names identically to the Python engine.
 */

export const CORPORATE_LEGAL_SUFFIXES: Set<string> = new Set([
  'llc', 'l.l.c.', 'ltd', 'ltd.', 'limited', 'corp', 'corp.', 'corporation',
  'inc', 'inc.', 'incorporated', 'co', 'co.', 'company', 'plc', 'p.l.c.',
  'holdings', 'holding', 'group', 'enterprises', 'enterprise', 'industries',
  'industry', 'syndicate', 'international', 'intl', 'global', 'trading',
  'logistics', 'shipping', 'services', 'management', 'investments',
  'fze', 'fzc', 'fzco', 'dmcc', 'llc - so', 'pjsc', 'prjs',
  'ag', 'a.g.', 'gmbh', 'g.m.b.h.', 'sa', 's.a.', 'sarl', 'bv', 'b.v.', 'nv', 'n.v.',
  'pte', 'pte.', 'pte ltd', 'sdn bhd', 'bhd', 'pvt', 'pvt.', 'private limited'
]);

export const BANGLA_TRANSLITERATION_MAP: [RegExp, string][] = [
  [/\bmd\.(?=\s|$)/gi, 'mohammed'],
  [/\bmd\b/gi, 'mohammed'],
  [/\bmohammad\b/gi, 'mohammed'],
  [/\bmuhammad\b/gi, 'mohammed'],
  [/\bmohammod\b/gi, 'mohammed'],
  [/\bseikh\b/gi, 'sheikh'],
  [/\bshaikh\b/gi, 'sheikh'],
  [/\bshaykh\b/gi, 'sheikh'],
  [/\bsheykh\b/gi, 'sheikh'],
  [/\brohman\b/gi, 'rahman'],
  [/\brokhman\b/gi, 'rahman'],
  [/\brehman\b/gi, 'rahman'],
  [/\bchoudhury\b/gi, 'chowdhury'],
  [/\bchowdury\b/gi, 'chowdhury'],
  [/\bchaudhury\b/gi, 'chowdhury'],
  [/\bchaudhri\b/gi, 'chowdhury'],
  [/\bchoudhry\b/gi, 'chowdhury'],
  [/\bkahn\b/gi, 'khan'],
  [/\bahmad\b/gi, 'ahmed'],
  [/\behmed\b/gi, 'ahmed'],
  [/\bhussain\b/gi, 'hossain'],
  [/\bhussein\b/gi, 'hossain'],
  [/\bhossein\b/gi, 'hossain'],
  [/\bhasan\b/gi, 'hassan'],
  [/\bhaque\b/gi, 'haq'],
  [/\bhuq\b/gi, 'haq'],
  [/\bislam\b/gi, 'islam'],
  [/\bislem\b/gi, 'islam'],
  [/\bali\b/gi, 'ali'],
  [/\bal-/gi, 'al '],
  [/\bel-/gi, 'al ']
];

export function stripDiacritics(text: string): string {
  if (!text) return '';
  return text
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/ł/g, 'l')
    .replace(/Ł/g, 'L')
    .replace(/ø/g, 'o')
    .replace(/Ø/g, 'O')
    .replace(/æ/g, 'ae')
    .replace(/Æ/g, 'AE')
    .replace(/œ/g, 'oe')
    .replace(/Œ/g, 'OE')
    .replace(/ß/g, 'ss')
    .replace(/đ/g, 'd')
    .replace(/Đ/g, 'D');
}

export function stripLegalSuffixes(tokens: string[]): string[] {
  const cleaned = [...tokens];
  while (cleaned.length > 0) {
    const tail = cleaned[cleaned.length - 1]?.toLowerCase() || '';
    if (CORPORATE_LEGAL_SUFFIXES.has(tail)) {
      cleaned.pop();
      continue;
    }
    if (cleaned.length >= 2) {
      const twoWord = `${cleaned[cleaned.length - 2]?.toLowerCase()} ${tail}`;
      if (CORPORATE_LEGAL_SUFFIXES.has(twoWord)) {
        cleaned.pop();
        cleaned.pop();
        continue;
      }
    }
    break;
  }
  return cleaned;
}

export function standardizeBanglaTransliteration(text: string): string {
  let normalized = text;
  for (const [pattern, replacement] of BANGLA_TRANSLITERATION_MAP) {
    normalized = normalized.replace(pattern, replacement);
  }
  return normalized;
}

export function normalizeEntityName(
  rawName: string,
  stripLegal: boolean = true,
  applyBangla: boolean = true
): string {
  if (!rawName) return '';

  let cleaned = stripDiacritics(rawName).toLowerCase();
  if (applyBangla) {
    cleaned = standardizeBanglaTransliteration(cleaned);
  }
  cleaned = cleaned.replace(/[^\w\s]/g, ' ');
  let tokens = cleaned.split(/\s+/).filter(Boolean);

  if (stripLegal) {
    tokens = stripLegalSuffixes(tokens);
  }

  return tokens.join(' ');
}

export function getTokenBag(name: string): string[] {
  return normalizeEntityName(name, true).split(/\s+/).filter(Boolean);
}

export function getNameOrderPermutations(name: string): string[] {
  const tokens = getTokenBag(name);
  if (tokens.length === 0) return [];

  const original = tokens.join(' ');
  const perms = [original];

  if (tokens.length > 1) {
    const sorted = [...tokens].sort().join(' ');
    if (!perms.includes(sorted)) perms.push(sorted);

    const reversed = [...tokens].reverse().join(' ');
    if (!perms.includes(reversed)) perms.push(reversed);
  }

  return perms;
}
