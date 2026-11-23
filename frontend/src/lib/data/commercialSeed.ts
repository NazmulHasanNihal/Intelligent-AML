/**
 * commercialSeed.ts — Institutional Banking Single Source of Truth
 * Contains deterministic commercial financial crime data for all 11 modules.
 * Strictly 0 academic/research dataset references.
 */

export interface CommercialAlert {
  id: string;
  caseId?: string;
  timestamp: string;
  account: string;
  entityName: string;
  amount: number;
  amountBdt: number;
  rail: string;
  bic: string;
  counterparty: string;
  counterpartyName: string;
  counterpartyBic: string;
  counterpartyCountry: string;
  tier: 'Tier 1 Hold' | 'Tier 2 Review' | 'Tier 3 Clear';
  tierCode: 1 | 2 | 3;
  riskScore: number;
  status: 'PENDING_TRIAGE' | 'UNDER_INVESTIGATION' | 'SAR_DRAFTED' | 'QUARANTINED' | 'FALSE_POSITIVE_DISMISSED';
  assignee: string;
  typology: string;
  typologyBadge: string;
  decisionSet: string;
  slaMinutesLeft: number;
  whyFlagged: string;
  flowConservationRatio: number; // e.g. 0.998
  velocityBurstScore: number; // e.g. 4.82
  tbmlData?: {
    lcNumber: string;
    hsCode: string;
    declaredPrice: string;
    benchmarkPrice: string;
    priceDeviationPct: number;
    ports: string;
    vessel: string;
  };
  wirePayload?: {
    messageType: 'MT103' | 'MT700' | 'pacs.008' | 'RTGS_BGD';
    orderingCustomer: string;
    orderingInstitution: string;
    beneficiaryCustomer: string;
    beneficiaryInstitution: string;
    remittanceInfo: string;
    regulatoryFlags: string[];
  };
}

export interface CommercialCase {
  id: string;
  title: string;
  leadInvestigator: string;
  createdAt: string;
  status: 'INVESTIGATION_OPEN' | 'SAR_DRAFTED' | 'PENDING_FOUR_EYES' | 'CLOSED';
  slaHours: number;
  slaDeadline: string;
  riskExposureUsd: number;
  riskExposureBdt: number;
  targetAccount: string;
  entityName: string;
  primaryTypology: string;
  milestonesCompleted: number;
  milestonesTotal: number;
  milestones: Array<{
    title: string;
    status: 'COMPLETE' | 'IN_PROGRESS' | 'PENDING';
    time?: string;
    detail: string;
  }>;
  evidenceItems: Array<{
    name: string;
    type: string;
    sha256: string;
    size: string;
    verified: boolean;
  }>;
  notes: Array<{
    id: string;
    author: string;
    role: string;
    timestamp: string;
    content: string;
  }>;
}

export interface CommercialCustomer {
  id: string;
  accountNumber: string;
  name: string;
  type: 'CORPORATE' | 'RETAIL' | 'MFS_AGENT';
  registrationNo: string;
  maskedNidTin: string;
  actualNidTin: string;
  riskRating: 'PROHIBITED' | 'HIGH_EDD' | 'MEDIUM' | 'LOW';
  kycStatus: 'VERIFIED' | 'EXPIRING_SOON' | 'OVERDUE';
  accountStatus: 'ACTIVE' | 'DEBIT_HOLD' | 'FROZEN' | 'WHITELISTED';
  onboardedDate: string;
  nextReviewDate: string;
  declaredMonthlyTurnoverUsd: number;
  actualMonthlyTurnoverUsd: number;
  turnoverVarianceMultiplier: number;
  linkedAlertCount: number;
  linkedCaseCount: number;
  linkedRfiCount: number;
  uboHierarchy: Array<{
    name: string;
    shareholdingPct: number;
    pepStatus: boolean;
    jurisdiction: string;
  }>;
}

export interface WatchlistScreeningRecord {
  id: string;
  screenedName: string;
  screenedAccount: string;
  screenedAt: string;
  matchedEntity: string;
  watchlistSource: 'OFAC SDN' | 'UN Security Council' | 'EU Consolidated' | 'UK HMT' | 'Domestic Watchlist' | 'PEP Tier 1' | 'Adverse Media';
  matchScore: number; // e.g. 94.6
  matchAlgorithm: string;
  matchType: 'EXACT' | 'FUZZY_JARO_WINKLER' | 'PHONETIC_SOUNDEX' | 'ALIAS_HIT';
  disposition: 'PENDING_REVIEW' | 'DISMISSED_FALSE_POSITIVE' | 'ESCALATED_RFI' | 'CONFIRMED_TRUE_HIT';
  reviewedBy?: string;
  tokenDiffs: {
    screenedTokens: string[];
    matchedTokens: string[];
    commonTokens: string[];
  };
}

export interface CashThresholdReport {
  id: string;
  timestamp: string;
  accountNumber: string;
  entityName: string;
  branch: string;
  amountNative: number;
  amountUsd: number;
  currency: string;
  rail: 'CASH_OVER_THE_COUNTER' | 'MFS_AGENT_AGGREGATE' | 'RTGS_CASH_SETTLEMENT';
  isStructuringSuspect: boolean;
  thresholdPercentage: number;
  status: 'PENDING_SUBMISSION' | 'BATCHED_FOR_XML' | 'SUBMITTED_TO_FIU';
}

// ─────────────────────────────────────────────────────────────────
// Certified Deterministic Data Sets
// ─────────────────────────────────────────────────────────────────

export const INITIAL_ALERTS: CommercialAlert[] = [
  {
    id: 'ALT-994821',
    caseId: 'CASE-2026-0881',
    timestamp: '2026-09-02 08:14:22 UTC',
    account: 'BD22-EBLB-4829-1092-8823',
    entityName: 'Meghna Industrial & Agro Processing Ltd',
    amount: 9450.00,
    amountBdt: 1134000.00,
    rail: 'SWIFT MT700 (LC)',
    bic: 'EBLBBDDH',
    counterparty: 'AE-EBIL-1109-8421-4402',
    counterpartyName: 'Gulf Star Commodities FZE (JAFZA Dubai)',
    counterpartyBic: 'EBILAEAD',
    counterpartyCountry: 'United Arab Emirates',
    tier: 'Tier 1 Hold',
    tierCode: 1,
    riskScore: 0.984,
    status: 'UNDER_INVESTIGATION',
    assignee: 'Sarah L. Jenkins',
    typology: 'TBML Over-Invoicing & Sub-Threshold Structuring',
    typologyBadge: 'TBML Over-Invoice',
    decisionSet: 'Γ = {1}',
    slaMinutesLeft: 38,
    flowConservationRatio: 0.998,
    velocityBurstScore: 4.82,
    whyFlagged: 'Documentary Credit (LC) unit price for raw cotton exceeds ASYCUDA customs valuation by +333.7%, split into duplicate LCs under internal $10,000 correspondent threshold.',
    tbmlData: {
      lcNumber: 'LC-2026-CTG-88912',
      hsCode: 'HS 5201.00 (Raw Cotton / Combed Yarn)',
      declaredPrice: '$42.50 / kg',
      benchmarkPrice: '$9.80 / kg',
      priceDeviationPct: 333.7,
      ports: 'Chittagong Port (BDCGP) ➔ Jebel Ali Dubai (AEJEA)',
      vessel: 'MV Banglar Joy (IMO 9832101)'
    },
    wirePayload: {
      messageType: 'MT700',
      orderingCustomer: 'Meghna Industrial & Agro Processing Ltd (BD22-EBLB-4829-1092-8823)',
      orderingInstitution: 'Eastern Bank PLC (BIC: EBLBBDDH)',
      beneficiaryCustomer: 'Gulf Star Commodities FZE (AE-EBIL-1109-8421-4402)',
      beneficiaryInstitution: 'Emirates NBD Bank (BIC: EBILAEAD)',
      remittanceInfo: 'COMMERCIAL INVOICE #CTG-2026-44102 FOR RAW COMBED COTTON GRADE-A 220 METRIC TONS',
      regulatoryFlags: ['ASYCUDA_UNIT_PRICE_DIVERGENCE', 'JAFZA_FREE_ZONE_COUNTERPARTY', 'RAPID_LC_DUPLICATION']
    }
  },
  {
    id: 'ALT-994824',
    caseId: 'CASE-2026-0894',
    timestamp: '2026-09-02 08:29:45 UTC',
    account: 'BD22-SCBL-9912-3341-7719',
    entityName: 'Delta River Logistics & Freight Agency',
    amount: 7950.00,
    amountBdt: 954000.00,
    rail: 'BEFTN / Cash Counter',
    bic: 'SCBLBDDX',
    counterparty: 'BD22-IBBL-4412-9901-2211',
    counterpartyName: 'Al-Madina Trading Syndicate (MFS Cash Hub)',
    counterpartyBic: 'IBBLBDDH',
    counterpartyCountry: 'Bangladesh',
    tier: 'Tier 1 Hold',
    tierCode: 1,
    riskScore: 0.946,
    status: 'UNDER_INVESTIGATION',
    assignee: 'Tanvir Mahmud',
    typology: 'Smurfing & Multi-Agent Cash Structuring',
    typologyBadge: 'Cash Structuring',
    decisionSet: 'Γ = {1}',
    slaMinutesLeft: 74,
    flowConservationRatio: 0.985,
    velocityBurstScore: 5.12,
    whyFlagged: 'Consecutive cash deposits of ৳954,000 BDT ($7,950 USD) placed at 3 different branches within 45 minutes, structured directly beneath the ৳1,000,000 BDT BFIU statutory CTR limit.',
    wirePayload: {
      messageType: 'RTGS_BGD',
      orderingCustomer: 'Delta River Logistics & Freight Agency',
      orderingInstitution: 'Standard Chartered Bank Bangladesh',
      beneficiaryCustomer: 'Al-Madina Trading Syndicate',
      beneficiaryInstitution: 'Islami Bank Bangladesh PLC',
      remittanceInfo: 'MFS SUB-AGENT CASH REPLENISHMENT BATCH #8812',
      regulatoryFlags: ['SUB_CTR_STRUCTURING_95pct', 'MULTI_BRANCH_DEPOSIT_BURST', 'AGENT_FAN_OUT']
    }
  },
  {
    id: 'ALT-994828',
    timestamp: '2026-09-02 08:44:11 UTC',
    account: 'BD22-CITY-5512-8819-0021',
    entityName: 'Apex Apex Meridian Apparel Exporters',
    amount: 148500.00,
    amountBdt: 17820000.00,
    rail: 'ISO 20022 pacs.008',
    bic: 'CIBLBDDH',
    counterparty: 'SG-DBSX-9941-8812-4411',
    counterpartyName: 'Pacific Rim Textile Logistics Pte Ltd',
    counterpartyBic: 'DBSSSGSG',
    counterpartyCountry: 'Singapore',
    tier: 'Tier 2 Review',
    tierCode: 2,
    riskScore: 0.642,
    status: 'PENDING_TRIAGE',
    assignee: 'Musrat Jahan Gungun',
    typology: 'Rapid Pass-Through Cross-Border Settlement',
    typologyBadge: 'Pass-Through',
    decisionSet: 'Γ = {0, 1}',
    slaMinutesLeft: 195,
    flowConservationRatio: 0.994,
    velocityBurstScore: 2.18,
    whyFlagged: 'Inflow of $148,500 transferred to Singapore entity within 12 minutes of arrival with zero overnight balance retention.',
    wirePayload: {
      messageType: 'pacs.008',
      orderingCustomer: 'Apex Meridian Apparel Exporters',
      orderingInstitution: 'City Bank PLC',
      beneficiaryCustomer: 'Pacific Rim Textile Logistics Pte Ltd',
      beneficiaryInstitution: 'DBS Bank Singapore',
      remittanceInfo: 'SETTLEMENT INVOICE #PRT-2026-99120',
      regulatoryFlags: ['ZERO_BALANCE_PASSTHROUGH', 'RAPID_CROSSBORDER_OUTFLOW']
    }
  },
  {
    id: 'ALT-994832',
    timestamp: '2026-09-02 08:52:00 UTC',
    account: 'BD22-BRAC-7712-4410-9901',
    entityName: 'Karnaphuli Steel & Re-Rolling Mills Ltd',
    amount: 320000.00,
    amountBdt: 38400000.00,
    rail: 'SWIFT MT103',
    bic: 'BRAEBDDH',
    counterparty: 'CH-UBSW-4412-0091-8822',
    counterpartyName: 'Helvetia Metallurgical Trading AG',
    counterpartyBic: 'UBSWCHZH',
    counterpartyCountry: 'Switzerland',
    tier: 'Tier 3 Clear',
    tierCode: 3,
    riskScore: 0.048,
    status: 'FALSE_POSITIVE_DISMISSED',
    assignee: 'Auto-Cleared STP',
    typology: 'Verified Heavy Machinery Capital Import',
    typologyBadge: 'Capital Import',
    decisionSet: 'Γ = {0}',
    slaMinutesLeft: 999,
    flowConservationRatio: 0.120,
    velocityBurstScore: 0.05,
    whyFlagged: 'Standard industrial equipment payment matching registered Bangladesh Bank Import Form IMP and verified customs bill.',
    wirePayload: {
      messageType: 'MT103',
      orderingCustomer: 'Karnaphuli Steel & Re-Rolling Mills Ltd',
      orderingInstitution: 'BRAC Bank PLC',
      beneficiaryCustomer: 'Helvetia Metallurgical Trading AG',
      beneficiaryInstitution: 'UBS Switzerland AG',
      remittanceInfo: 'SETTLEMENT FOR INDUCTION FURNACE LINE 4',
      regulatoryFlags: ['REGISTERED_BB_IMP_MATCH']
    }
  }
];

// Helper to expand initial alerts into 2,028 deterministic records matching exact KPI invariants
export function generateFullAlertQueue(): CommercialAlert[] {
  const alerts: CommercialAlert[] = [...INITIAL_ALERTS];
  const rails = ['SWIFT MT103', 'SWIFT MT700 (LC)', 'ISO 20022 pacs.008', 'RTGS / MFS', 'BEFTN Wire'];
  const entities = [
    'Padma River Agro Exporters Ltd',
    'Chittagong Global Maritime Logistics',
    'Sonali Yarn & Spinning Mills Ltd',
    'Bexim Synthetic Fibers Ltd',
    'Habib & Brothers Currency Exchange',
    'Sylhet Overseas Remittance Center',
    'Dhaka Digital Commerce MFS Hub',
    'Crown Cement Shipping Agency'
  ];
  const typologies = [
    'TBML Over-Invoicing',
    'MFS Cash Smurfing',
    'Pass-Through Layering',
    'High-Velocity Fan-Out',
    'Circular UBO Loop'
  ];

  // Seed up to 2,028: 1,280 Tier 1 Hold and 748 Tier 2 Review
  const neededTier1 = 1280 - alerts.filter(a => a.tierCode === 1).length;
  const neededTier2 = 748 - alerts.filter(a => a.tierCode === 2).length;

  for (let i = 0; i < neededTier1; i++) {
    const seq = 1000 + i;
    alerts.push({
      id: `ALT-99${seq}`,
      caseId: i % 4 === 0 ? `CASE-2026-${Math.floor(1000 + (i % 30))}` : undefined,
      timestamp: `2026-09-02 ${String(8 + Math.floor(i / 120)).padStart(2, '0')}:${String((i * 7) % 60).padStart(2, '0')}:12 UTC`,
      account: `BD22-BANK-${String(1000 + (i % 9000))}-8823`,
      entityName: entities[i % entities.length]!,
      amount: 4500 + ((i * 137) % 8500),
      amountBdt: (4500 + ((i * 137) % 8500)) * 120,
      rail: rails[i % rails.length]!,
      bic: 'EBLBBDDH',
      counterparty: `EXT-${String(2000 + i)}-TRADE`,
      counterpartyName: 'Offshore Trading Intermediary FZE',
      counterpartyBic: 'EBILAEAD',
      counterpartyCountry: i % 2 === 0 ? 'United Arab Emirates' : 'Singapore',
      tier: 'Tier 1 Hold',
      tierCode: 1,
      riskScore: Number((0.85 + ((i % 15) * 0.01)).toFixed(3)),
      status: i % 3 === 0 ? 'UNDER_INVESTIGATION' : 'PENDING_TRIAGE',
      assignee: i % 2 === 0 ? 'Sarah L. Jenkins' : 'Tanvir Mahmud',
      typology: typologies[i % typologies.length]!,
      typologyBadge: typologies[i % typologies.length]!.split(' ')[0]!,
      decisionSet: 'Γ = {1}',
      slaMinutesLeft: 20 + ((i * 13) % 180),
      flowConservationRatio: Number((0.98 + ((i % 20) * 0.001)).toFixed(3)),
      velocityBurstScore: Number((3.5 + ((i % 25) * 0.1)).toFixed(2)),
      whyFlagged: 'High-velocity transaction burst exceeding internal correspondent threshold with elevated counterparty free-zone risk.'
    });
  }

  for (let i = 0; i < neededTier2; i++) {
    const seq = 5000 + i;
    alerts.push({
      id: `ALT-99${seq}`,
      timestamp: `2026-09-02 ${String(9 + Math.floor(i / 120)).padStart(2, '0')}:${String((i * 11) % 60).padStart(2, '0')}:44 UTC`,
      account: `BD22-BANK-${String(3000 + (i % 7000))}-4412`,
      entityName: entities[(i + 3) % entities.length]!,
      amount: 15000 + ((i * 241) % 55000),
      amountBdt: (15000 + ((i * 241) % 55000)) * 120,
      rail: rails[(i + 1) % rails.length]!,
      bic: 'SCBLBDDX',
      counterparty: `EXT-${String(6000 + i)}-CORP`,
      counterpartyName: 'Regional Industrial Supplier Pte',
      counterpartyBic: 'DBSSSGSG',
      counterpartyCountry: 'Singapore',
      tier: 'Tier 2 Review',
      tierCode: 2,
      riskScore: Number((0.45 + ((i % 25) * 0.01)).toFixed(3)),
      status: 'PENDING_TRIAGE',
      assignee: 'Musrat Jahan Gungun',
      typology: typologies[(i + 2) % typologies.length]!,
      typologyBadge: typologies[(i + 2) % typologies.length]!.split(' ')[0]!,
      decisionSet: 'Γ = {0, 1}',
      slaMinutesLeft: 120 + ((i * 17) % 240),
      flowConservationRatio: Number((0.92 + ((i % 30) * 0.002)).toFixed(3)),
      velocityBurstScore: Number((1.8 + ((i % 20) * 0.08)).toFixed(2)),
      whyFlagged: 'Cross-border wire volume variance requiring secondary KYC validation against declared business turnover.'
    });
  }

  return alerts;
}

export const INITIAL_CASES: CommercialCase[] = [
  {
    id: 'CASE-2026-0881',
    title: 'Meghna Agro & Industrial — TBML Over-Invoicing Syndicate',
    leadInvestigator: 'Sarah L. Jenkins, CFE',
    createdAt: '2026-09-02 08:35:10 UTC',
    status: 'INVESTIGATION_OPEN',
    slaHours: 72,
    slaDeadline: '2026-09-05 08:35:10 UTC',
    riskExposureUsd: 148500.00,
    riskExposureBdt: 17820000.00,
    targetAccount: 'BD22-EBLB-4829-1092-8823',
    entityName: 'Meghna Industrial & Agro Processing Ltd',
    primaryTypology: 'Trade-Based Money Laundering (TBML Over-Invoicing)',
    milestonesCompleted: 4,
    milestonesTotal: 6,
    milestones: [
      { title: '1. Alert Quarantined', status: 'COMPLETE', time: '2026-09-02 08:14 UTC', detail: 'Automated Tier 1 hold executed' },
      { title: '2. Triage & Intake', status: 'COMPLETE', time: '2026-09-02 08:35 UTC', detail: 'Sarah Jenkins assigned as Lead' },
      { title: '3. Compliance RFI Issued', status: 'COMPLETE', time: '2026-09-02 09:00 UTC', detail: 'Commercial invoice requested' },
      { title: '4. Evidence Hash Chain Sealed', status: 'COMPLETE', time: '2026-09-02 10:15 UTC', detail: '3 documents sealed with SHA-256' },
      { title: '5. Regulatory SAR Drafted', status: 'IN_PROGRESS', detail: 'Automated statutory assembly ready' },
      { title: '6. 4-Eyes CCO Sign-Off', status: 'PENDING', detail: 'Awaiting dual signatory ratification' }
    ],
    evidenceItems: [
      {
        name: 'ASYCUDA_Customs_Bill_CTG_88912.pdf',
        type: 'Customs Declaration',
        sha256: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
        size: '2.4 MB',
        verified: true
      },
      {
        name: 'SWIFT_MT700_Documentary_Credit.xml',
        type: 'Settlement Rail',
        sha256: 'ca978112ca1bbdcafac231b39a23dc4da786081442f05d060a31e8725b7e0ee9',
        size: '48 KB',
        verified: true
      },
      {
        name: 'Commercial_Invoice_Cotton_Overvaluation.pdf',
        type: 'Trade Invoice',
        sha256: '4e1243bd22c66e76c2ba9eddc1f91394e57f9f835f8c6e7f225d57b545464a02',
        size: '1.8 MB',
        verified: true
      }
    ],
    notes: [
      {
        id: 'NOTE-1',
        author: 'Sarah L. Jenkins',
        role: 'INVESTIGATOR_L2',
        timestamp: '2026-09-02 09:12 UTC',
        content: 'Cross-checked declared unit price $42.50/kg against Chittagong customs historical tariff benchmark ($9.80/kg). Discrepancy represents 333.7% capital flight premium.'
      },
      {
        id: 'NOTE-2',
        author: 'Nazmul Hasan',
        role: 'CCO_L3',
        timestamp: '2026-09-02 10:30 UTC',
        content: 'Reviewed beneficiary Gulf Star Commodities in JAFZA. No operating warehouse found at declared address. Recommending emergency quarantine and SAR drafting.'
      }
    ]
  },
  {
    id: 'CASE-2026-0894',
    title: 'Delta River Logistics — Multi-Branch Cash Smurfing Ring',
    leadInvestigator: 'Tanvir Mahmud',
    createdAt: '2026-09-02 09:05:00 UTC',
    status: 'INVESTIGATION_OPEN',
    slaHours: 72,
    slaDeadline: '2026-09-05 09:05:00 UTC',
    riskExposureUsd: 87500.00,
    riskExposureBdt: 10500000.00,
    targetAccount: 'BD22-SCBL-9912-3341-7719',
    entityName: 'Delta River Logistics & Freight Agency',
    primaryTypology: 'Cash Smurfing & CTR Evasion',
    milestonesCompleted: 3,
    milestonesTotal: 6,
    milestones: [
      { title: '1. Alert Quarantined', status: 'COMPLETE', time: '2026-09-02 08:30 UTC', detail: 'Rapid burst cash deposits intercepted' },
      { title: '2. Triage & Intake', status: 'COMPLETE', time: '2026-09-02 09:05 UTC', detail: 'Tanvir Mahmud assigned' },
      { title: '3. Compliance RFI Issued', status: 'COMPLETE', time: '2026-09-02 09:30 UTC', detail: 'Proof of commercial cash origin requested' },
      { title: '4. Evidence Hash Chain Sealed', status: 'IN_PROGRESS', detail: 'Gathering branch CCTV & deposit slips' },
      { title: '5. Regulatory SAR Drafted', status: 'PENDING', detail: 'Awaiting deposit slip confirmation' },
      { title: '6. 4-Eyes CCO Sign-Off', status: 'PENDING', detail: 'Awaiting dual signatory ratification' }
    ],
    evidenceItems: [
      {
        name: 'Branch_Deposit_Slips_Batch_88.pdf',
        type: 'Cash Deposit Slips',
        sha256: '8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4',
        size: '3.1 MB',
        verified: true
      }
    ],
    notes: [
      {
        id: 'NOTE-1',
        author: 'Tanvir Mahmud',
        role: 'INVESTIGATOR_L2',
        timestamp: '2026-09-02 09:45 UTC',
        content: 'Pattern demonstrates deliberate structuring at ৳954,000 BDT to evade mandatory ৳1,000,000 CTR filing under MLPA 2012 § 25.'
      }
    ]
  }
];

export const INITIAL_CUSTOMERS: CommercialCustomer[] = [
  {
    id: 'CUST-0081',
    accountNumber: 'BD22-EBLB-4829-1092-8823',
    name: 'Meghna Industrial & Agro Processing Ltd',
    type: 'CORPORATE',
    registrationNo: 'C-78491/2014 (RJSC Dhaka)',
    maskedNidTin: '8022-****-****-8823 / TIN 481-***-991',
    actualNidTin: '8022-1984-7712-8823 / TIN 481-992-991',
    riskRating: 'HIGH_EDD',
    kycStatus: 'EXPIRING_SOON',
    accountStatus: 'DEBIT_HOLD',
    onboardedDate: '2019-04-12',
    nextReviewDate: '2026-09-30',
    declaredMonthlyTurnoverUsd: 25000,
    actualMonthlyTurnoverUsd: 412000,
    turnoverVarianceMultiplier: 16.48, // 16.5x anomaly
    linkedAlertCount: 6,
    linkedCaseCount: 1,
    linkedRfiCount: 2,
    uboHierarchy: [
      { name: 'Kazi Farhan Ahmed', shareholdingPct: 65.0, pepStatus: false, jurisdiction: 'Bangladesh' },
      { name: 'Gulf Star Holdings LLC (Offshore)', shareholdingPct: 35.0, pepStatus: true, jurisdiction: 'UAE' }
    ]
  },
  {
    id: 'CUST-0094',
    accountNumber: 'BD22-SCBL-9912-3341-7719',
    name: 'Delta River Logistics & Freight Agency',
    type: 'CORPORATE',
    registrationNo: 'P-11928/2018 (Chittagong)',
    maskedNidTin: '7712-****-****-3341 / TIN 331-***-882',
    actualNidTin: '7712-9901-4412-3341 / TIN 331-884-882',
    riskRating: 'HIGH_EDD',
    kycStatus: 'VERIFIED',
    accountStatus: 'ACTIVE',
    onboardedDate: '2021-08-19',
    nextReviewDate: '2027-08-19',
    declaredMonthlyTurnoverUsd: 15000,
    actualMonthlyTurnoverUsd: 185000,
    turnoverVarianceMultiplier: 12.33,
    linkedAlertCount: 4,
    linkedCaseCount: 1,
    linkedRfiCount: 1,
    uboHierarchy: [
      { name: 'Sultan Mahmud Hossain', shareholdingPct: 100.0, pepStatus: false, jurisdiction: 'Bangladesh' }
    ]
  },
  {
    id: 'CUST-0105',
    accountNumber: 'BD22-BRAC-7712-4410-9901',
    name: 'Karnaphuli Steel & Re-Rolling Mills Ltd',
    type: 'CORPORATE',
    registrationNo: 'C-22910/2005 (Chittagong)',
    maskedNidTin: '5510-****-****-9901 / TIN 110-***-441',
    actualNidTin: '5510-8812-3310-9901 / TIN 110-221-441',
    riskRating: 'LOW',
    kycStatus: 'VERIFIED',
    accountStatus: 'WHITELISTED',
    onboardedDate: '2010-02-14',
    nextReviewDate: '2028-02-14',
    declaredMonthlyTurnoverUsd: 5000000,
    actualMonthlyTurnoverUsd: 4850000,
    turnoverVarianceMultiplier: 0.97,
    linkedAlertCount: 1,
    linkedCaseCount: 0,
    linkedRfiCount: 0,
    uboHierarchy: [
      { name: 'Engr. M. A. Rashid', shareholdingPct: 70.0, pepStatus: false, jurisdiction: 'Bangladesh' },
      { name: 'Karnaphuli Industrial Trust', shareholdingPct: 30.0, pepStatus: false, jurisdiction: 'Bangladesh' }
    ]
  }
];

export const INITIAL_SCREENING_RECORDS: WatchlistScreeningRecord[] = [
  {
    id: 'SCR-2026-001',
    screenedName: 'Gulf Star Commodities FZE',
    screenedAccount: 'AE-EBIL-1109-8421-4402',
    screenedAt: '2026-09-02 08:14:25 UTC',
    matchedEntity: 'Gulf Star Trading & Logistics LLC (SDN-19482)',
    watchlistSource: 'OFAC SDN',
    matchScore: 94.6,
    matchAlgorithm: 'Jaro-Winkler + Semantic Token Match',
    matchType: 'FUZZY_JARO_WINKLER',
    disposition: 'PENDING_REVIEW',
    tokenDiffs: {
      screenedTokens: ['gulf', 'star', 'commodities', 'fze'],
      matchedTokens: ['gulf', 'star', 'trading', 'logistics', 'llc'],
      commonTokens: ['gulf', 'star']
    }
  },
  {
    id: 'SCR-2026-002',
    screenedName: 'Kazi Farhan Ahmed',
    screenedAccount: 'BD22-EBLB-4829-1092-8823',
    screenedAt: '2026-09-02 08:35:12 UTC',
    matchedEntity: 'Farhan Ahmed Kazi (PEP-BD-0441)',
    watchlistSource: 'PEP Tier 1',
    matchScore: 91.2,
    matchAlgorithm: 'Phonetic Soundex + Word Reversal',
    matchType: 'PHONETIC_SOUNDEX',
    disposition: 'ESCALATED_RFI',
    tokenDiffs: {
      screenedTokens: ['kazi', 'farhan', 'ahmed'],
      matchedTokens: ['farhan', 'ahmed', 'kazi'],
      commonTokens: ['kazi', 'farhan', 'ahmed']
    }
  },
  {
    id: 'SCR-2026-003',
    screenedName: 'Helvetia Metallurgical Trading AG',
    screenedAccount: 'CH-UBSW-4412-0091-8822',
    screenedAt: '2026-09-02 08:52:01 UTC',
    matchedEntity: 'Helvetia Metals Corp (Dismissed)',
    watchlistSource: 'EU Consolidated',
    matchScore: 68.4,
    matchAlgorithm: 'Token Jaccard Similarity',
    matchType: 'FUZZY_JARO_WINKLER',
    disposition: 'DISMISSED_FALSE_POSITIVE',
    reviewedBy: 'Sarah L. Jenkins',
    tokenDiffs: {
      screenedTokens: ['helvetia', 'metallurgical', 'trading', 'ag'],
      matchedTokens: ['helvetia', 'metals', 'corp'],
      commonTokens: ['helvetia']
    }
  }
];

export const INITIAL_CTR_RECORDS: CashThresholdReport[] = [
  {
    id: 'CTR-2026-9901',
    timestamp: '2026-09-02 10:14:00 UTC',
    accountNumber: 'BD22-IBBL-4412-9901-2211',
    entityName: 'Al-Madina Trading Syndicate',
    branch: 'Chawkbazar Commercial Branch, Dhaka',
    amountNative: 1450000.00,
    amountUsd: 12083.33,
    currency: 'BDT',
    rail: 'CASH_OVER_THE_COUNTER',
    isStructuringSuspect: false,
    thresholdPercentage: 145.0, // Crosses ৳1,000,000 threshold
    status: 'BATCHED_FOR_XML'
  },
  {
    id: 'CTR-2026-9902',
    timestamp: '2026-09-02 10:45:22 UTC',
    accountNumber: 'BD22-SCBL-9912-3341-7719',
    entityName: 'Delta River Logistics & Freight Agency',
    branch: 'Agrabad Corporate Branch, Chittagong',
    amountNative: 954000.00,
    amountUsd: 7950.00,
    currency: 'BDT',
    rail: 'MFS_AGENT_AGGREGATE',
    isStructuringSuspect: true,
    thresholdPercentage: 95.4, // Near-CTR Structuring Flag
    status: 'PENDING_SUBMISSION'
  },
  {
    id: 'CTR-2026-9903',
    timestamp: '2026-09-02 11:20:15 UTC',
    accountNumber: 'BD22-EBLB-1192-8812-4412',
    entityName: 'Chittagong Maritime Supply Agency',
    branch: 'Khatunganj Commodity Branch',
    amountNative: 2800000.00,
    amountUsd: 23333.33,
    currency: 'BDT',
    rail: 'CASH_OVER_THE_COUNTER',
    isStructuringSuspect: false,
    thresholdPercentage: 280.0,
    status: 'BATCHED_FOR_XML'
  }
];
