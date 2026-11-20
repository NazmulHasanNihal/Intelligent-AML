// Deterministic 31 U.S.C. § 5318(g)(2) / MLPA 2012 Anti-Tipping-Off Scanner
// Prevents internal AML suspicion, GNN, or law enforcement language from leaking into customer notices

const FORBIDDEN_AML_TERMS = [
  /\bSAR\b/i,
  /\bSTR\b/i,
  /\bSuspicious Activity\b/i,
  /\bMoney Laundering\b/i,
  /\bSmurfing\b/i,
  /\bStructuring\b/i,
  /\bLaundering\b/i,
  /\bLaw Enforcement\b/i,
  /\bFinCEN\b/i,
  /\bBFIU\b/i,
  /\bgoAML\b/i,
  /\bGNN\b/i,
  /\bNeural\b/i,
  /\bSoftmax\b/i,
  /\bTensor\b/i,
  /\bHawkes\b/i,
  /\bInvariants?\b/i
];

export interface TippingOffCheckResult {
  isClean: boolean;
  violations: string[];
  safeText: string;
}

export function scanForTippingOffViolations(text: string): TippingOffCheckResult {
  const violations: string[] = [];
  
  for (const pattern of FORBIDDEN_AML_TERMS) {
    const match = text.match(pattern);
    if (match) {
      violations.push(match[0]);
    }
  }

  return {
    isClean: violations.length === 0,
    violations: Array.from(new Set(violations)),
    safeText: text
  };
}

export function scanTextForTippingOff(text: string): { containsTippingOff: boolean; matchedPhrases: string[]; sanitizedText: string } {
  const result = scanForTippingOffViolations(text);
  return {
    containsTippingOff: !result.isClean,
    matchedPhrases: result.violations,
    sanitizedText: redactTippingOffTerms(text)
  };
}

export function redactTippingOffTerms(text: string): string {
  let redacted = text;
  for (const pattern of FORBIDDEN_AML_TERMS) {
    redacted = redacted.replace(pattern, '[REDACTED REGULATORY TERM]');
  }
  return redacted;
}
