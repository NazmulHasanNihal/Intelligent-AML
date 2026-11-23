import { describe, it, expect } from 'vitest';
import { JURISDICTIONS, formatCurrencyByJurisdiction } from '../lib/compliance/jurisdictions';
import { computeSha256, verifyAuditChain, getAuditChain, tamperAuditBlock, restoreAuditChain } from '../lib/audit/hashChain';
import { scanTextForTippingOff } from '../lib/compliance/tippingOff';
import { REGULATORY_CONFIG, BFIU_GUIDANCE_MAPPING } from '../lib/config/regulatory';

describe('Commercial AML Compliance & Statutory Rules Suite', () => {
  it('correctly configures Bangladesh BFIU statutory limits and legal citations', () => {
    const bd = JURISDICTIONS.BD_BFIU;
    expect(bd.currency).toBe('BDT');
    expect(bd.ctrThresholdNative).toBe(1000000); // ৳1,000,000 BDT
    expect(bd.statutoryAct).toContain('Money Laundering Prevention Act');
    expect(bd.strMandate).toContain('Section 25');

    const formatted = formatCurrencyByJurisdiction(1000000, 'BD_BFIU');
    expect(formatted).toContain('৳');
    expect(formatted).toContain('1,000,000');
  });

  it('correctly configures US FinCEN statutory limits and FRE 902(11) evidentiary citations', () => {
    const us = JURISDICTIONS.US_FINCEN;
    expect(us.currency).toBe('USD');
    expect(us.ctrThresholdNative).toBe(10000); // $10,000 USD
    expect(us.evidenceRule).toContain('902(11)');
    expect(us.urgentSlaHours).toBe(24);

    const formatted = formatCurrencyByJurisdiction(10000, 'US_FINCEN');
    expect(formatted).toBe('$10,000.00 USD');
  });

  it('detects criminal anti-tipping-off violations and protects customer notices', () => {
    const unlawfulText = 'Please provide invoices because we filed a SAR with FinCEN regarding smurfing and money laundering.';
    const scan = scanTextForTippingOff(unlawfulText);

    expect(scan.containsTippingOff).toBe(true);
    const phrases = scan.matchedPhrases.map((p) => p.toLowerCase());
    expect(phrases).toContain('sar');
    expect(phrases).toContain('fincen');
    expect(phrases).toContain('money laundering');

    const lawfulText = 'Routine institutional documentation refresh for LC commercial invoice verification.';
    const lawfulScan = scanTextForTippingOff(lawfulText);
    expect(lawfulScan.containsTippingOff).toBe(false);
    expect(lawfulScan.matchedPhrases.length).toBe(0);
  });

  it('computes real WebCrypto SHA-256 hashes and verifies WORM audit chain integrity', async () => {
    const digest1 = await computeSha256('Block Payload 1');
    const digest2 = await computeSha256('Block Payload 1');
    const digest3 = await computeSha256('Block Payload 2');

    expect(digest1).toBe(digest2);
    expect(digest1).not.toBe(digest3);
    expect(digest1.length).toBe(64);

    // Verify initial certified genesis chain
    const chain = getAuditChain();
    const chainResult = await verifyAuditChain(chain);
    if (!chainResult.isValid) {
      console.log('DEBUG chainResult:', chainResult);
    }
    expect(chainResult.isValid).toBe(true);
    expect(chainResult.totalEntries).toBe(chain.length);
  });

  it('detects tampering in WORM audit chain when a historical block is mutated', async () => {
    const originalChain = getAuditChain();
    const tamperedLedger = JSON.parse(JSON.stringify(originalChain));
    tamperedLedger[1].details = 'Tampered unauthorized memo by malicious insider';

    const check = await verifyAuditChain(tamperedLedger);
    expect(check.isValid).toBe(false);
    expect(check.brokenSequence).toBe(2);
  });

  it('enforces centralized versioned BFIU regulatory configuration standards', () => {
    // 1. CTR Policy
    expect(REGULATORY_CONFIG.ctrPolicy.thresholdBdt).toBe(1000000);
    expect(REGULATORY_CONFIG.ctrPolicy.effectiveDate).toBe('2012-02-20');
    expect(REGULATORY_CONFIG.ctrPolicy.sourceLink).toContain('bb.org.bd');
    expect(REGULATORY_CONFIG.ctrPolicy.statutoryBasis).toContain('Money Laundering Prevention Act 2012 § 2(z)');

    // 2. Structuring Band
    expect(REGULATORY_CONFIG.structuringPolicy.lowerBoundBdt).toBe(800000);
    expect(REGULATORY_CONFIG.structuringPolicy.upperBoundBdt).toBe(999999);
    expect(REGULATORY_CONFIG.structuringPolicy.sourceLink).toContain('bb.org.bd');

    // 3. Dated FX Rate
    expect(REGULATORY_CONFIG.fxRatePolicy.usdToBdt).toBe(120.0);
    expect(REGULATORY_CONFIG.fxRatePolicy.dated).toBe('2026-11-20');
    expect(REGULATORY_CONFIG.fxRatePolicy.sourceLink).toContain('bb.org.bd');

    // 4. Primary Statute & Announced 2025 Amendment with TODO(verify)
    expect(REGULATORY_CONFIG.statuteReferences.primaryAmlAct.title).toContain('Money Laundering Prevention Act, 2012');
    expect(REGULATORY_CONFIG.statuteReferences.primaryAmlAct.tippingOffSection).toContain('Section 6');
    expect(REGULATORY_CONFIG.statuteReferences.amendment2025.verificationTag).toContain('TODO(verify');

    // 5. Retention & Data Residency Policies with TODO(verify)
    expect(REGULATORY_CONFIG.retentionPolicy.statutoryYears).toBe(5);
    expect(REGULATORY_CONFIG.retentionPolicy.verificationTag).toContain('TODO(verify');
    expect(REGULATORY_CONFIG.dataResidencyPolicy.verificationTag).toContain('TODO(verify');
    expect(REGULATORY_CONFIG.piiPrivacyPolicy.verificationTag).toContain('TODO(verify');

    // 6. GDPR Research Notes for ETH Zurich prototype
    expect(REGULATORY_CONFIG.piiPrivacyPolicy.gdprResearchNotes.researchExemption).toContain('Article 89');
    expect(REGULATORY_CONFIG.piiPrivacyPolicy.gdprResearchNotes.complianceBasis).toContain('Article 6(1)(c)');

    // 7. BFIU Guidance Mapping includes TBML Guidelines
    const tbmlMapping = BFIU_GUIDANCE_MAPPING.find((m: any) => m.id === 'BFIU-MAP-03');
    expect(tbmlMapping).toBeDefined();
    expect(tbmlMapping?.frameworkName).toContain('BFIU TBML Guidelines');
    expect(tbmlMapping?.appModule).toContain('Trade Finance TBML');
  });
});
