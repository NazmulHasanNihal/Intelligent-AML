/**
 * jurisdictions.ts — Multi-Jurisdiction Statutory Engine
 * Provides dynamic legal citations, CTR thresholds, structuring bands,
 * SLA countdowns, and reporting standards across central bank regimes.
 */

import { REGULATORY_CONFIG } from '@/lib/config/regulatory';

export type JurisdictionCode = 'BD_BFIU' | 'US_FINCEN' | 'EU_AMLA';

export interface JurisdictionProfile {
  id: JurisdictionCode;
  shortCode: string;
  name: string;
  authority: string;
  country: string;
  currency: string;
  currencySymbol: string;
  usdFxRate: number; // 1 unit in USD or USD to local
  ctrThresholdNative: number;
  ctrThresholdUsd: number;
  structuringRangeNative: [number, number];
  statutoryAct: string;
  strMandate: string;
  antiTippingOffStatute: string;
  evidenceRule: string;
  modelGovernanceRule: string;
  urgentSlaHours: number;
  standardSlaHours: number;
  sarTemplateName: string;
  sarSchemaVersion: string;
}

export const JURISDICTIONS: Record<JurisdictionCode, JurisdictionProfile> = {
  BD_BFIU: {
    id: 'BD_BFIU',
    shortCode: 'BFIU',
    name: 'Bangladesh Financial Intelligence Unit',
    authority: 'Bangladesh Bank, Motijheel Head Office, Dhaka',
    country: 'Bangladesh',
    currency: 'BDT',
    currencySymbol: '৳',
    usdFxRate: REGULATORY_CONFIG.fxRatePolicy.usdToBdt, // 1 USD = 120 BDT
    ctrThresholdNative: REGULATORY_CONFIG.ctrPolicy.thresholdBdt, // ৳1,000,000 BDT
    ctrThresholdUsd: REGULATORY_CONFIG.ctrPolicy.thresholdUsd,
    structuringRangeNative: [
      REGULATORY_CONFIG.structuringPolicy.lowerBoundBdt,
      REGULATORY_CONFIG.structuringPolicy.upperBoundBdt
    ], // ৳800,000 - ৳999,999 BDT
    statutoryAct: 'Money Laundering Prevention Act, 2012 (Act V of 2012 §§ 6, 25), ATA 2009 & MLPR 2019',
    strMandate: 'Money Laundering Prevention Act 2012 Section 25 (§ 25) / BFIU Master Circular No. 26 & Circular No. 24 (TBML), Circular 32 (2026), Circular Letters 02/03/05 (2026)',
    antiTippingOffStatute: 'MLPA 2012 § 6 (Prohibition of Disclosure / Anti-Tipping-Off — up to 2 years imprisonment & fine)',
    evidenceRule: 'Admissibility-ready under Bangladesh Evidence Act, 1872 (Amended 2022) §§ 65A–65B & 73A (Officer Certificate)',
    modelGovernanceRule: 'Bangladesh Bank Core Risk Management Guidelines (AML/CFT) & BFIU Circular Letters 02/03 (2026)',
    urgentSlaHours: 72,
    standardSlaHours: 120, // 5 Banking Days
    sarTemplateName: 'BFIU Suspicious Transaction Report (STR/SAR) / UNODC goAML XML',
    sarSchemaVersion: 'UNODC-goAML-v4.2-XML'
  },
  US_FINCEN: {
    id: 'US_FINCEN',
    shortCode: 'FinCEN',
    name: 'Financial Crimes Enforcement Network',
    authority: 'U.S. Department of the Treasury, Vienna, VA',
    country: 'United States',
    currency: 'USD',
    currencySymbol: '$',
    usdFxRate: 1.0,
    ctrThresholdNative: 10000, // $10,000 USD
    ctrThresholdUsd: 10000,
    structuringRangeNative: [8000, 9999], // $8,000 - $9,999 USD
    statutoryAct: 'Bank Secrecy Act (BSA), 31 U.S.C. § 5311 et seq.',
    strMandate: '31 CFR § 1020.320 & FinCEN Form 111 (SAR-DI)',
    antiTippingOffStatute: '31 U.S.C. § 5318(g)(2) (Absolute Prohibition on SAR Disclosure)',
    evidenceRule: 'Federal Rules of Evidence Rule 902(11) Certified Domestic Business Records',
    modelGovernanceRule: 'Federal Reserve SR 11-7 / OCC 2011-12 Model Risk Management Standards',
    urgentSlaHours: 24, // FinCEN 314(a)
    standardSlaHours: 720, // 30 Calendar Days
    sarTemplateName: 'FinCEN Suspicious Activity Report (Form 111 XML)',
    sarSchemaVersion: 'FinCEN-BSA-XML-v2.0'
  },
  EU_AMLA: {
    id: 'EU_AMLA',
    shortCode: 'AMLA',
    name: 'European Anti-Money Laundering Authority',
    authority: 'European Union AML/CFT Oversight Framework, Frankfurt',
    country: 'European Union',
    currency: 'EUR',
    currencySymbol: '€',
    usdFxRate: 1.08, // 1 EUR = 1.08 USD
    ctrThresholdNative: 10000, // €10,000 EUR
    ctrThresholdUsd: 10800,
    structuringRangeNative: [8000, 9999], // €8,000 - €9,999 EUR
    statutoryAct: 'EU Anti-Money Laundering Regulation (AMLR) & Directive (EU) 2018/1673 (6AMLD)',
    strMandate: 'Article 54 AMLR & UN goAML European Union Schema',
    antiTippingOffStatute: 'Directive 2015/849/EU Article 39 (Prohibition on Disclosure of Suspicious Transactions)',
    evidenceRule: 'Regulation (EU) No 910/2014 (eIDAS) & Article 14 EU AI Act (Human Oversight)',
    modelGovernanceRule: 'EBA Guidelines on Internal Governance (EBA/GL/2021/05) & EU AI Act Risk Tiering',
    urgentSlaHours: 48,
    standardSlaHours: 360, // 15 Banking Days
    sarTemplateName: 'UN goAML XML (European FIU Specification)',
    sarSchemaVersion: 'goAML-EU-v5.0-XML'
  }
};

export function formatCurrencyByJurisdiction(amount: number, jurisdictionId: JurisdictionCode): string {
  const jur = JURISDICTIONS[jurisdictionId] || JURISDICTIONS.BD_BFIU;
  if (jur.id === 'BD_BFIU') {
    const bdt = amount * jur.usdFxRate;
    return `${jur.currencySymbol}${bdt.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} BDT ($${amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} USD)`;
  } else if (jur.id === 'EU_AMLA') {
    const eur = amount / jur.usdFxRate;
    return `${jur.currencySymbol}${eur.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} EUR ($${amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} USD)`;
  } else {
    return `$${amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} USD`;
  }
}
