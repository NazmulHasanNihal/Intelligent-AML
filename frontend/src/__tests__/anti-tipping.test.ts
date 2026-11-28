import { describe, it, expect } from 'vitest';
import { NextRequest } from 'next/server';
import { scanTextForTippingOff, redactTippingOffTerms } from '@/lib/compliance/tippingOff';
import { POST as sarPost } from '@/app/api/v1/sar/route';

describe('MLPA 2012 § 6 & 31 U.S.C. § 5318(g)(2) Anti-Tipping-Off Enforcement', () => {
  it('flags forbidden SAR/STR/AML references in customer-facing text', () => {
    const res = scanTextForTippingOff('We filed an STR with BFIU after GNN detected smurfing.');
    expect(res.containsTippingOff).toBe(true);
    expect(res.matchedPhrases.length).toBeGreaterThanOrEqual(4);
    expect(redactTippingOffTerms('Blocked STR for BFIU')).not.toContain('STR');
  });

  it('permits neutral commercial KYC refresh notices', () => {
    const safe = 'Please provide certified commercial invoice and packing list within 5 banking days.';
    const res = scanTextForTippingOff(safe);
    expect(res.containsTippingOff).toBe(false);
    expect(res.matchedPhrases).toHaveLength(0);
  });

  it('blocks POST /api/v1/sar with HTTP 422 when customerFacingMemo leaks AML suspicion', async () => {
    const req = new NextRequest('http://localhost/api/v1/sar', {
      method: 'POST',
      body: JSON.stringify({
        caseId: 'CASE-2026-0881',
        reportType: 'STR',
        jurisdiction: 'BD_BFIU',
        makerId: 'BNK-4419',
        checkerId: 'BNK-7842',
        narrative: 'Detailed investigator internal narrative covering +333.7% ASYCUDA variance.',
        customerFacingMemo: 'Notice: we submitted a Suspicious Activity Report (SAR) to FinCEN.',
      }),
    });

    const res = await sarPost(req);
    expect(res.status).toBe(422);
    const json = await res.json();
    expect(json.violations.length).toBeGreaterThan(0);
  });
});
