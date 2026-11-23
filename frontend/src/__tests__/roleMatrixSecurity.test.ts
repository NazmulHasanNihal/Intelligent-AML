import { describe, it, expect } from 'vitest';
import { canApproveCase, canRevealPii, canExecuteAction } from '@/lib/auth/session';
import { PiiRevealSchema, CaseSignoffSchema } from '@/lib/validation/schemas';
import nextConfig from '../../next.config';

describe('Role-Matrix Security & OWASP ASVS Level 2 Verification', () => {
  it('enforces that Analyst L1 CANNOT approve cases or reveal customer PII', () => {
    expect(canApproveCase('ANALYST_L1')).toBe(false);
    expect(canRevealPii('ANALYST_L1')).toBe(false);
    expect(canExecuteAction('ANALYST_L1', 'RATIFY_CASE_4EYES')).toBe(false);
    expect(canExecuteAction('ANALYST_L1', 'PII_REVEAL')).toBe(false);
  });

  it('enforces that Auditor is strictly read-only and CANNOT approve cases or reveal PII', () => {
    expect(canApproveCase('AUDITOR')).toBe(false);
    expect(canRevealPii('AUDITOR')).toBe(false);
    expect(canExecuteAction('AUDITOR', 'RATIFY_CASE_4EYES')).toBe(false);
    expect(canExecuteAction('AUDITOR', 'PII_REVEAL')).toBe(false);
    expect(canExecuteAction('AUDITOR', 'SR11_7_READ')).toBe(true);
  });

  it('permits Analyst L2 (Maker) to investigate and reveal PII but NOT approve cases without supervisor', () => {
    expect(canApproveCase('ANALYST_L2')).toBe(false);
    expect(canRevealPii('ANALYST_L2')).toBe(true);
    expect(canExecuteAction('ANALYST_L2', 'DRAFT_REGULATORY_SAR')).toBe(true);
  });

  it('permits Supervisor and MLRO/CAMLCO (Checkers) to ratify cases and reveal PII', () => {
    expect(canApproveCase('SUPERVISOR')).toBe(true);
    expect(canRevealPii('SUPERVISOR')).toBe(true);
    expect(canApproveCase('MLRO_CAMLCO')).toBe(true);
    expect(canRevealPii('MLRO_CAMLCO')).toBe(true);
  });

  it('validates Zod PiiRevealSchema enforces minimum 10-character reason gate', () => {
    const valid = PiiRevealSchema.safeParse({
      target_account: 'BD22-EBLB-4829-1092-8823',
      reason: 'Subpoena Grand Jury response MLPA 2012 §25'
    });
    expect(valid.success).toBe(true);

    const invalidReason = PiiRevealSchema.safeParse({
      target_account: 'BD22-EBLB-4829-1092-8823',
      reason: 'check'
    });
    expect(invalidReason.success).toBe(false);
  });

  it('validates Zod CaseSignoffSchema enforces substantive ratification notes', () => {
    const valid = CaseSignoffSchema.safeParse({
      case_id: 'CASE-2026-0881',
      approver: 'Farhana Ahmed, CAMS',
      notes: 'Independent second-signer review of ASYCUDA benchmark confirmed.'
    });
    expect(valid.success).toBe(true);

    const invalid = CaseSignoffSchema.safeParse({
      case_id: 'CASE-2026-0881',
      approver: 'Farhana Ahmed',
      notes: 'ok'
    });
    expect(invalid.success).toBe(false);
  });

  it('verifies Next.js HTTP security headers meet securityheaders.com A-grade criteria', async () => {
    const headersFn = nextConfig.headers;
    expect(typeof headersFn).toBe('function');
    if (!headersFn) return;

    const headersList = await headersFn();
    const globalRule = headersList.find((h: any) => h.source === '/:path*');
    expect(globalRule).toBeDefined();
    if (!globalRule) return;

    const headersMap = new Map(globalRule.headers.map((h: any) => [h.key, h.value]));

    // 1. Content-Security-Policy with frame-ancestors 'none'
    expect(headersMap.has('Content-Security-Policy')).toBe(true);
    const csp = headersMap.get('Content-Security-Policy');
    expect(csp).toContain("frame-ancestors 'none'");
    expect(csp).toContain("default-src 'self'");

    // 2. Strict-Transport-Security (HSTS) with max-age >= 1 year + subdomains + preload
    expect(headersMap.has('Strict-Transport-Security')).toBe(true);
    expect(headersMap.get('Strict-Transport-Security')).toContain('max-age=63072000');
    expect(headersMap.get('Strict-Transport-Security')).toContain('includeSubDomains');
    expect(headersMap.get('Strict-Transport-Security')).toContain('preload');

    // 3. X-Content-Type-Options: nosniff
    expect(headersMap.get('X-Content-Type-Options')).toBe('nosniff');

    // 4. X-Frame-Options: DENY
    expect(headersMap.get('X-Frame-Options')).toBe('DENY');

    // 5. Referrer-Policy
    expect(headersMap.get('Referrer-Policy')).toBe('strict-origin-when-cross-origin');

    // 6. Permissions-Policy
    expect(headersMap.has('Permissions-Policy')).toBe(true);
  });
});
