/**
 * Seeded Demo Data Engine with Strict Mathematical Invariants
 * Every KPI, count, and percentage is derived directly from this single source of truth.
 */

export const RAW_TELEMETRY = {
  totalProcessed24h: 148312,
  tier1Quarantined: 1280,
  tier2ReviewQueue: 748,
  tier3AutoCleared: 146284,
  avgLatencyMs: 0.45,
  p50LatencyMs: 0.38,
  p95LatencyMs: 0.62,
  p99LatencyMs: 0.82,
  peakThroughputTxPerSec: 500,
  avgThroughputTxPerSec: 1.7
};

// Derived Invariants Verification
export const DERIVED_METRICS = {
  get totalAlerts() {
    return RAW_TELEMETRY.tier1Quarantined + RAW_TELEMETRY.tier2ReviewQueue; // 2,028
  },
  get stpRate() {
    return Number(((RAW_TELEMETRY.tier3AutoCleared / RAW_TELEMETRY.totalProcessed24h) * 100).toFixed(1)); // 98.6%
  },
  get quarantineRate() {
    return Number(((RAW_TELEMETRY.tier1Quarantined / RAW_TELEMETRY.totalProcessed24h) * 100).toFixed(2)); // 0.86%
  },
  get reviewRate() {
    return Number(((RAW_TELEMETRY.tier2ReviewQueue / RAW_TELEMETRY.totalProcessed24h) * 100).toFixed(2)); // 0.50%
  }
};

/// Seeded Alerts Queue (Real-World Institutional & Trade-Based AML Profiles)
export const SEEDED_ALERTS = [
  {
    id: 'ALT-994821',
    caseId: 'CASE-2026-0881',
    timestamp: '2026-09-02 08:14:22 UTC',
    account: 'BD22-EBLB-4829-1092-8823',
    entityName: 'Meghna Industrial & Agro Processing Ltd',
    amount: 9450.00,
    amountBdt: 1134000.00,
    caseTotalExposure: 48500.00,
    rail: 'SWIFT MT700 (LC)',
    bic: 'EBLBBDDH',
    counterparty: 'AE-EBIL-1109-8421-4402',
    counterpartyName: 'Gulf Star Commodities FZE (JAFZA Dubai)',
    counterpartyBic: 'EBILAEAD',
    tier: 'Tier 1 Hold',
    tierCode: 1,
    riskScore: 0.984,
    pConformal: 0.0004,
    status: 'UNDER_INVESTIGATION',
    assignee: 'Sarah Jenkins',
    typology: 'TBML Over-Invoicing & Sub-Threshold Structuring',
    typologyBadge: 'TBML Over-Invoice',
    decisionSet: 'Γ = {1}',
    slaMinutesLeft: 38,
    whyFlagged: 'Documentary Credit (LC) unit price for raw cotton exceeds ASYCUDA customs valuation by +333.7%, structured beneath $10k (৳1,000,000 BDT BFIU CTR threshold).',
    tbmlDetails: {
      lcNumber: 'LC-2026-CTG-88912',
      hsCode: 'HS 5201.00 (Raw Cotton / Combed Yarn)',
      declaredPrice: '$42.50 / kg',
      benchmarkPrice: '$9.80 / kg',
      priceDeviation: '+333.7% Over-Invoiced',
      ports: 'Chittagong Port (BDCGP) ➔ Jebel Ali Dubai (AEJEA)',
      vessel: 'MV Banglar Joy (IMO 9832101)',
      originBank: 'Eastern Bank PLC (EBL), Motijheel Head Office',
      bfiuCompliance: 'BFIU Section 2(v) TBML Capital Flight Alert'
    },
    shapDrivers: [
      { name: 'Customs Valuation Divergence (+333%)', weight: 0.42, direction: 'risk' },
      { name: 'CTR Structuring Proximity ($9.4k / ৳1.13M)', weight: 0.35, direction: 'risk' },
      { name: 'JAFZA Free Zone High-Risk Corridor', weight: 0.18, direction: 'risk' },
      { name: 'Verified Authorized Dealer (AD) License', weight: -0.07, direction: 'mitigant' }
    ]
  },
  {
    id: 'ALT-994820',
    caseId: 'CASE-2026-0881',
    timestamp: '2026-09-02 08:22:15 UTC',
    account: 'BD22-EBLB-4829-1092-8823',
    entityName: 'Meghna Industrial & Agro Processing Ltd',
    amount: 9600.00,
    amountBdt: 1152000.00,
    caseTotalExposure: 48500.00,
    rail: 'SWIFT MT700 (LC)',
    bic: 'EBLBBDDH',
    counterparty: 'AE-EBIL-1109-8421-4402',
    counterpartyName: 'Gulf Star Commodities FZE (JAFZA Dubai)',
    counterpartyBic: 'EBILAEAD',
    tier: 'Tier 1 Hold',
    tierCode: 1,
    riskScore: 0.978,
    pConformal: 0.0007,
    status: 'UNDER_INVESTIGATION',
    assignee: 'Sarah Jenkins',
    typology: 'Smurfing & Rapid Re-transmission',
    typologyBadge: 'Structuring (<$10k)',
    decisionSet: 'Γ = {1}',
    slaMinutesLeft: 46,
    whyFlagged: 'Second structured export LC transfer within 8 minutes into the same Dubai intermediary entity without physical Bill of Lading verification.',
    tbmlDetails: {
      lcNumber: 'LC-2026-CTG-88912',
      hsCode: 'HS 5201.00 (Raw Cotton / Combed Yarn)',
      declaredPrice: '$42.50 / kg',
      benchmarkPrice: '$9.80 / kg',
      priceDeviation: '+333.7% Over-Invoiced',
      ports: 'Chittagong Port (BDCGP) ➔ Jebel Ali Dubai (AEJEA)',
      vessel: 'MV Banglar Joy (IMO 9832101)',
      originBank: 'Eastern Bank PLC (EBL), Motijheel Head Office',
      bfiuCompliance: 'BFIU Section 2(v) TBML Capital Flight Alert'
    },
    shapDrivers: [
      { name: 'Rapid Re-transmission Velocity', weight: 0.41, direction: 'risk' },
      { name: 'Round Sub-threshold Allocation', weight: 0.34, direction: 'risk' },
      { name: 'LEI Entity Verification', weight: -0.05, direction: 'mitigant' }
    ]
  },
  {
    id: 'ALT-994819',
    caseId: 'CASE-2026-0882',
    timestamp: '2026-09-02 08:31:04 UTC',
    account: 'BD04-BRAC-1109-8421-4402',
    entityName: 'Tanvir Ahmed Rahman (Trade Conduit)',
    amount: 38400.00,
    amountBdt: 4608000.00,
    caseTotalExposure: 38400.00,
    rail: 'SWIFT MT103',
    bic: 'BRAKBDDH',
    counterparty: 'GB-BARC-1109-8421-4402',
    counterpartyName: 'Anglo-Bengal Logistics Ltd (London E1)',
    counterpartyBic: 'BARCGB22',
    tier: 'Tier 1 Hold',
    tierCode: 1,
    riskScore: 0.992,
    pConformal: 0.0001,
    status: 'ESCALATED_MLRO',
    assignee: 'Nazmul Hasan',
    typology: 'Cross-Border Hundi & MFS Layering',
    typologyBadge: 'Layering Loop',
    decisionSet: 'Γ = {1}',
    slaMinutesLeft: 14,
    whyFlagged: 'High-velocity aggregation of 14 bKash MFS cash-out micro-deposits converted to cross-border wire to London with zero dwell time (Φ_flow ≈ 0.98).',
    shapDrivers: [
      { name: 'MFS Dispersed Inbound Aggregation', weight: 0.48, direction: 'risk' },
      { name: 'Conduit Dwell Time (0.3h < 2h)', weight: 0.35, direction: 'risk' },
      { name: 'Informal Remittance (Hundi) Pattern', weight: 0.19, direction: 'risk' }
    ]
  },
  {
    id: 'ALT-994818',
    caseId: 'CASE-2026-0883',
    timestamp: '2026-09-02 08:37:50 UTC',
    account: 'MFS-BKASH-0171-8840',
    entityName: 'Mohammad Rafiqul Islam (MFS Cash-Out Agent)',
    amount: 4800.00,
    amountBdt: 576000.00,
    caseTotalExposure: 4800.00,
    rail: 'bKash MFS',
    bic: 'BKASHBDD',
    counterparty: 'SG-DBS-8819-3301',
    counterpartyName: 'Pacific Commodities Pte Ltd (Singapore)',
    counterpartyBic: 'DBSSSGSG',
    tier: 'Tier 2 Review',
    tierCode: 2,
    riskScore: 0.642,
    pConformal: 0.0180,
    status: 'NEW_UNASSIGNED',
    assignee: 'Unassigned',
    typology: 'Dormant Agent Sudden Outbound Flare',
    typologyBadge: 'Rapid MFS Velocity',
    decisionSet: 'Γ = {0, 1}',
    slaMinutesLeft: 112,
    whyFlagged: 'MFS agent account dormant for 340 days initiated sudden international trade remittance exceeding historical monthly turnover.',
    shapDrivers: [
      { name: 'Dormancy Spike Ratio (14.2x)', weight: 0.44, direction: 'risk' },
      { name: 'Unusual Cross-Border Corridors', weight: 0.28, direction: 'risk' },
      { name: 'Agent Biometric Re-auth Match', weight: -0.15, direction: 'mitigant' }
    ]
  },
  {
    id: 'ALT-994816',
    caseId: 'CASE-2026-0884',
    timestamp: '2026-09-02 08:42:19 UTC',
    account: 'BD18-CIBL-3312-8804-1290',
    entityName: 'Square Fashion & Apparels Ltd',
    amount: 6200.00,
    amountBdt: 744000.00,
    caseTotalExposure: 6200.00,
    rail: 'RTGS (BD Bank)',
    bic: 'CIBLBDDH',
    counterparty: 'DE-DB-9901-7721-5540',
    counterpartyName: 'EuroTextile Importers GmbH (Hamburg)',
    counterpartyBic: 'DEUTDEFF',
    tier: 'Tier 2 Review',
    tierCode: 2,
    riskScore: 0.580,
    pConformal: 0.0240,
    status: 'UNDER_INVESTIGATION',
    assignee: 'Sarah Jenkins',
    typology: 'RMG Commercial Velocity Anomaly',
    typologyBadge: 'Smurfing Fan-Out',
    decisionSet: 'Γ = {0, 1}',
    slaMinutesLeft: 135,
    whyFlagged: 'Multiple consecutive RTGS settlements exceeding standard commercial export billing intervals.',
    shapDrivers: [
      { name: 'Intraday Frequency Burst', weight: 0.36, direction: 'risk' },
      { name: 'Verified BGMEA Garment Export Registration', weight: -0.22, direction: 'mitigant' }
    ]
  },
  {
    id: 'ALT-994815',
    caseId: null,
    timestamp: '2026-09-02 08:45:00 UTC',
    account: 'BD04-BRAC-0192-8821-4401',
    entityName: 'Beximco Pharmaceuticals Ltd',
    amount: 14250.00,
    amountBdt: 1710000.00,
    caseTotalExposure: 14250.00,
    rail: 'SWIFT MT103',
    bic: 'BRAKBDDH',
    counterparty: 'BD12-HSBC-2201-9940-1120',
    counterpartyName: 'Grameenphone Corporate Treasury',
    counterpartyBic: 'HSBCBDDH',
    tier: 'Tier 3 Clear',
    tierCode: 3,
    riskScore: 0.012,
    pConformal: 0.9880,
    status: 'AUTO_CLEARED',
    assignee: 'Autonomous Filter',
    typology: 'Corporate Interbank Commercial Settlement (Safe)',
    typologyBadge: 'Licit Corporate STP',
    decisionSet: 'Γ = {0}',
    slaMinutesLeft: null,
    whyFlagged: 'Verified recurring corporate dividend settlement and telecommunications infrastructure billing.',
    shapDrivers: [
      { name: 'Recognized Prime Corporate Beneficiary', weight: -0.65, direction: 'mitigant' },
      { name: 'Consistent Historical Recurrence & Tax TIN', weight: -0.32, direction: 'mitigant' }
    ]
  }
];

// Seeded Enterprise Case Workspace (BFIU & Cross-Border Correspondent Compliance)
export const SEEDED_CASES = [
  {
    id: 'CASE-2026-0881',
    title: 'Meghna Industrial & Agro RMG Over-Invoicing & Smurfing Loop',
    subjectEntity: 'Meghna Industrial & Agro Processing Ltd',
    subjectAccount: 'BD22-EBLB-4829-1092-8823',
    subjectBic: 'EBLBBDDH',
    totalExposure: 48500.00,
    totalExposureBdt: 5820000.00,
    riskScore: 0.984,
    tier: 'Tier 1 Hold',
    status: 'SAR_PENDING_APPROVAL',
    assignedTo: 'Sarah Jenkins (Senior Investigator)',
    fourEyesInitiator: 'Sarah Jenkins',
    fourEyesApprover: null,
    fourEyesVerified: false,
    openedAt: '2026-09-02 08:15:00 UTC',
    slaDeadline: '2026-09-05 08:15:00 UTC',
    statutoryJurisdiction: 'BFIU Form STR-1 (MLPA 2012 §25) / FinCEN Form 111',
    statutorySlaHours: 72,
    linkedAlertIds: ['ALT-994821', 'ALT-994820'],
    tbmlDetails: {
      lcNumber: 'LC-2026-CTG-88912',
      hsCode: 'HS 5201.00 (Raw Cotton / Combed Yarn)',
      declaredPrice: '$42.50 / kg',
      benchmarkPrice: '$9.80 / kg',
      priceDeviation: '+333.7% Over-Invoiced',
      ports: 'Chittagong Port (BDCGP) ➔ Jebel Ali Dubai (AEJEA)',
      vessel: 'MV Banglar Joy (IMO 9832101)',
      originBank: 'Eastern Bank PLC (EBL), Motijheel Head Office',
      bfiuCompliance: 'BFIU Section 2(v) TBML Capital Flight'
    },
    timeline: [
      { id: 1, time: '08:14:22 UTC', event: 'Alert ALT-994821 triggered for $9,450 (৳1,134,000) wire under LC-2026-CTG-88912.' },
      { id: 2, time: '08:16:00 UTC', event: 'Administrative hold placed on outbound LC settlement by Senior Investigator Sarah Jenkins.' },
      { id: 3, time: '08:22:15 UTC', event: 'Second structured attempt ALT-994820 ($9,600) blocked and linked to Case-0881.' },
      { id: 4, time: '08:35:00 UTC', event: 'Autonomous BFIU STR-1 / FinCEN narrative generated with deterministic customs citations.' },
      { id: 5, time: '08:40:00 UTC', event: 'Four-Eyes Dual Sign-Off requested from Chief Compliance Officer Nazmul Hasan.' }
    ],
    notes: [
      {
        id: 'note-1',
        author: 'Sarah Jenkins',
        time: '08:28 UTC',
        text: 'Examined 90-day export history. Account conducted domestic textile trading averaging $3,500. The rapid sequence of four transfers just below $10,000 (৳1,000,000 CTR limit) to Dubai intermediary Gulf Star Commodities indicates intentional trade over-invoicing under Section 25 of Money Laundering Prevention Act 2012.'
      },
      {
        id: 'note-2',
        author: 'Sarah Jenkins',
        time: '08:38 UTC',
        text: 'Drafted BFIU STR-1 Form XML. Four-Eyes sign-off submitted to CCO Nazmul Hasan. Do not contact client directly to prevent tipping off under Section 27 of MLPA 2012 / 31 U.S.C. § 5318(g)(2).'
      }
    ],
    milestones: [
      { step: 'TRIGGERED', label: 'Triggered', time: '08:14 UTC', status: 'completed' },
      { step: 'ASSIGNED', label: 'Analyst Assigned', time: '08:16 UTC', status: 'completed' },
      { step: 'RFI_DISPATCHED', label: 'RFI Dispatched', time: '08:25 UTC', status: 'completed' },
      { step: 'SAR_DRAFTED', label: 'SAR Drafted', time: '08:35 UTC', status: 'completed' },
      { step: 'FOUR_EYES', label: '4-Eyes Approved', time: null, status: 'pending' }
    ],
    pinnedEvidence: [
      { id: 'pin-1', type: 'subgraph', title: 'Cycle-3 Dubai Laundering Subgraph (3 Nodes)', timestamp: '08:26 UTC', pinnedBy: 'Sarah Jenkins' },
      { id: 'pin-2', type: 'document', title: 'ASYCUDA World Customs Declaration #CTG-88912', timestamp: '08:30 UTC', pinnedBy: 'Sarah Jenkins' }
    ],
    sourcesUsed: [
      { id: 'SRC-1', claim: 'Four wire transfers totaling $48,500 (৳5,820,000) originated between 08:14 and 08:28 UTC.', ref: 'SWIFT MT700 / MT103 Ref #EBL-8821' },
      { id: 'SRC-2', claim: 'National Board of Revenue (NBR) ASYCUDA customs price database verifies standard cotton yarn median at $9.80/kg.', ref: 'Customs Valuation Database NBR-CTG-2026' },
      { id: 'SRC-3', claim: 'Subject entity beneficial ownership documentation does not disclose cross-border freight subsidiaries in JAFZA.', ref: 'KYC Registry Dossier BD22-EBLB-4829' }
    ],
    attachments: [
      { id: 'att-1', name: 'Letter_of_Credit_LC2026CTG88912_EBL_Bank.pdf', size: '245 KB', type: 'application/pdf', uploadedAt: '08:25 UTC', uploadedBy: 'Sarah Jenkins' },
      { id: 'att-2', name: 'ASYCUDA_World_Customs_Declaration_Chittagong.pdf', size: '1.2 MB', type: 'application/pdf', uploadedAt: '08:30 UTC', uploadedBy: 'Sarah Jenkins' },
      { id: 'att-3', name: 'BFIU_Form_STR1_Draft_Dossier_Confidential.pdf', size: '480 KB', type: 'application/pdf', uploadedAt: '08:34 UTC', uploadedBy: 'Sarah Jenkins' }
    ]
  },
  {
    id: 'CASE-2026-0882',
    title: 'Tanvir Ahmed Rahman Cross-Border Hundi & Layering Conduit',
    subjectEntity: 'Tanvir Ahmed Rahman (Trade Conduit)',
    subjectAccount: 'BD04-BRAC-1109-8421-4402',
    subjectBic: 'BRAKBDDH',
    totalExposure: 38400.00,
    totalExposureBdt: 4608000.00,
    riskScore: 0.972,
    tier: 'Tier 1 Hold',
    status: 'UNDER_INVESTIGATION',
    assignedTo: 'Nazmul Hasan (Chief Compliance Officer)',
    fourEyesInitiator: 'Sarah Jenkins',
    fourEyesApprover: null,
    fourEyesVerified: false,
    openedAt: '2026-09-02 08:20:00 UTC',
    slaDeadline: '2026-09-07 08:20:00 UTC',
    statutoryJurisdiction: 'BFIU Form STR-1 / UNODC goAML v4.0 (UK NCA)',
    statutorySlaHours: 120,
    linkedAlertIds: ['ALT-994819'],
    milestones: [
      { step: 'TRIGGERED', label: 'Triggered', time: '08:20 UTC', status: 'completed' },
      { step: 'ASSIGNED', label: 'Analyst Assigned', time: '08:22 UTC', status: 'completed' },
      { step: 'RFI_DISPATCHED', label: 'RFI Dispatched', time: '08:25 UTC', status: 'completed' },
      { step: 'SAR_DRAFTED', label: 'SAR Drafted', time: null, status: 'in_progress' },
      { step: 'FOUR_EYES', label: '4-Eyes Approved', time: null, status: 'pending' }
    ],
    pinnedEvidence: [
      { id: 'pin-101', type: 'subgraph', title: 'bKash MFS Aggregation Fan-In Subgraph', timestamp: '08:26 UTC', pinnedBy: 'Nazmul Hasan' }
    ],
    timeline: [
      { id: 1, time: '08:20:00 UTC', event: 'Case opened from multi-hop conduit clustering alert across bKash and BRAC Bank.' },
      { id: 2, time: '08:25:00 UTC', event: 'RFI Form CDD-1092 generated requesting verified source of wealth.' }
    ],
    notes: [
      {
        id: 'note-1',
        author: 'Nazmul Hasan',
        time: '08:30 UTC',
        text: 'Conduit account displays classical pass-through characteristics (Φ_flow ≈ 0.98). Funds do not dwell. Initiating bilateral inquiry under Section 314(b) / BFIU cross-border liaison protocols.'
      }
    ],
    sourcesUsed: [
      { id: 'SRC-1', claim: 'Pass-through velocity exceeded 8.5 transactions per hour through bKash cash-out agents.', ref: 'BEFTN / MFS Clearing Stream #1109' }
    ],
    attachments: [
      { id: 'att-101', name: 'BEFTN_Settlement_Audit_Stream_1109.csv', size: '82 KB', type: 'text/csv', uploadedAt: '08:28 UTC', uploadedBy: 'Nazmul Hasan' }
    ]
  }
];

// 360° Comprehensive Entity Profiles for Customer Dossiers & Surveillance
export const SEEDED_ENTITIES_360 = {
  'BD22-EBLB-4829-1092-8823': {
    account: 'BD22-EBLB-4829-1092-8823',
    name: 'Meghna Industrial & Agro Processing Ltd',
    legalType: 'Private Limited Company (Export-Oriented)',
    incorporation: 'RJSC Dhaka Registration #C-94821/2014',
    openDate: '2014-06-18',
    accountAge: '12 Years, 3 Months',
    institution: 'Eastern Bank PLC (Principal Branch)',
    tin: 'TIN-4882-9912-1088',
    jurisdiction: 'Motijheel, Dhaka, Bangladesh',
    address: 'Meghna Tower, Level 9, 44 Dilkusha C/A, Motijheel, Dhaka-1000',
    phone: '+880 2-9568201',
    email: 'treasury@meghna-agro.com.bd',
    balance: '$1,480,250.00 USD (৳177,630,000 BDT)',
    riskScore: 0.982,
    riskRating: 'CRITICAL (Tier 1 Hold)',
    kycStatus: 'ENHANCED_EDD_HOLD',
    kycTier: 'Tier-3 Enhanced Due Diligence (EDD Flagged)',
    ubo: 'Tanvir Ahmed Rahman (64% Equity), Meghna Family Trust (36%)',
    pepSanctions: {
      ofacSdn: 'NEGATIVE (Cleared)',
      unSanctions: 'NEGATIVE (Cleared)',
      bfiuWatchlist: 'ADVERSE FINDING (Administrative Hold §15)',
      pepDirect: 'NOT IDENTIFIED'
    },
    flowConservation: {
      phiFlow: 0.992,
      massBalanceRatio: '0.998 (Pass-Through Ratio 99.8%)',
      inboundTurnover: '$48,500.00 (৳5,820,000)',
      outboundTurnover: '$47,600.00 (৳5,712,000)',
      dwellTimeHours: 0.35,
      classification: 'Pure Passthrough Wash Hub'
    },
    counterfactualRemedy: 'Reduce LC unit price to official customs benchmark ($9.80/kg) and space transactions over >72h to clear automated hold.',
    ledger: [
      { id: 'TX-BFIU-948201', date: '2026-09-02 08:24:10', type: 'OUT', counterparty: 'Gulf Star Commodities FZE', counterpartyAccount: 'AE-EBIL-4412-8819-3301', amount: 9450.00, amountBdt: 1134000.00, rail: 'SWIFT MT700 (LC)', status: 'BLOCKED', memo: 'DOC-CREDIT DRAWDOWN / COMBED COTTON YARN' },
      { id: 'TX-BFIU-948192', date: '2026-09-02 08:16:00', type: 'IN', counterparty: 'Tanvir Ahmed Rahman', counterpartyAccount: 'BD04-BRAC-1109-8421-4402', amount: 47600.00, amountBdt: 5712000.00, rail: 'RTGS (BD Bank)', status: 'FLAGGED', memo: 'INTERBANK CONDUIT SETTLEMENT / BATCH 88' },
      { id: 'TX-BFIU-948170', date: '2026-09-01 14:10:00', type: 'OUT', counterparty: 'Customs House Chattogram', counterpartyAccount: 'BD00-NBR-CUSTOMS-CTG-01', amount: 12400.00, amountBdt: 1488000.00, rail: 'NBR e-Challan', status: 'COMPLETED', memo: 'CUSTOMS IMPORT DUTY ASSESSMENT #1982' },
      { id: 'TX-BFIU-948145', date: '2026-08-28 11:30:00', type: 'IN', counterparty: 'Prime Garments Sourcing Ltd', counterpartyAccount: 'BD12-HSBC-4412-8801', amount: 84000.00, amountBdt: 10080000.00, rail: 'SWIFT MT103', status: 'COMPLETED', memo: 'EXPORT ADVANCE PAYMENT / EXP-2026-99' },
      { id: 'TX-BFIU-948110', date: '2026-08-20 09:15:00', type: 'OUT', counterparty: 'Dhaka Electric Supply Co', counterpartyAccount: 'BD00-DESCO-UTILITY-01', amount: 3200.00, amountBdt: 384000.00, rail: 'BEFTN', status: 'COMPLETED', memo: 'COMMERCIAL INDUSTRIAL TARIFF UTILITY' }
    ],
    activityLogs: [
      { id: 'ACT-901', timestamp: '2026-09-02 08:24:10 UTC', action: 'TRANSACTION_INTERCEPTED', officer: 'Surveillance Engine', details: 'Statutory hold placed on wire TX-BFIU-948201 ($9,450 USD). Price divergence +333.7% triggered.' },
      { id: 'ACT-902', timestamp: '2026-09-02 08:20:00 UTC', action: 'FOUR_EYES_HOLD_RATIFIED', officer: 'Nazmul Hasan (CCO)', details: 'Four-Eyes dual signature ratified administrative freeze under BFIU §15.' },
      { id: 'ACT-903', timestamp: '2026-09-02 08:10:00 UTC', action: 'RFI_DISPATCHED', officer: 'Sarah Jenkins', details: 'Dispatched Form RFI-2026-1092 requesting certified Bill of Lading and ASYCUDA port clearance.' },
      { id: 'ACT-904', timestamp: '2026-08-15 10:00:00 UTC', action: 'PERIODIC_EDD_REVIEW', officer: 'Audit Committee', details: 'Annual Enhanced Due Diligence audit completed. Trade license verified.' },
      { id: 'ACT-905', timestamp: '2014-06-18 09:00:00 UTC', action: 'ACCOUNT_ONBOARDED', officer: 'Principal Branch Desk', details: 'Commercial corporate export current account opened.' }
    ]
  },
  'BD04-BRAC-1109-8421-4402': {
    account: 'BD04-BRAC-1109-8421-4402',
    name: 'Tanvir Ahmed Rahman (Trade Conduit)',
    legalType: 'Individual Commercial Proprietorship',
    incorporation: 'Trade License #DSCC-TL-2022-8841',
    openDate: '2022-03-10',
    accountAge: '4 Years, 6 Months',
    institution: 'BRAC Bank PLC (Gulshan Branch)',
    tin: 'TIN-1192-4412-8801',
    jurisdiction: 'Gulshan-2, Dhaka, Bangladesh',
    address: 'Apartment 4B, Road 71, Gulshan-2, Dhaka-1212',
    phone: '+880 1711-482910',
    email: 't.rahman.trade@gmail.com',
    balance: '$42,800.00 USD (৳5,136,000 BDT)',
    riskScore: 0.941,
    riskRating: 'HIGH RISK (Tier 1 Hold)',
    kycStatus: 'HIGH_RISK_HOLD',
    kycTier: 'Tier-2 Customer Due Diligence (Flagged)',
    ubo: 'Tanvir Ahmed Rahman (100% Sole Proprietor)',
    pepSanctions: {
      ofacSdn: 'NEGATIVE (Cleared)',
      unSanctions: 'NEGATIVE (Cleared)',
      bfiuWatchlist: 'FLAGGED (Informal Remittance Hundi Cluster)',
      pepDirect: 'NOT IDENTIFIED'
    },
    flowConservation: {
      phiFlow: 0.985,
      massBalanceRatio: '0.991 (Zero Retention)',
      inboundTurnover: '$38,400.00 (৳4,608,000)',
      outboundTurnover: '$38,400.00 (৳4,608,000)',
      dwellTimeHours: 0.28,
      classification: 'Rapid MFS-to-SWIFT Layering Conduit'
    },
    counterfactualRemedy: 'Provide formal tax clearance certificate and verified payroll source of funds to release administrative lock.',
    ledger: [
      { id: 'TX-BFIU-948190', date: '2026-09-02 08:22:15', type: 'OUT', counterparty: 'Gulf Star Commodities FZE', counterpartyAccount: 'AE-EBIL-4412-8819-3301', amount: 47600.00, amountBdt: 5712000.00, rail: 'SWIFT MT103', status: 'BLOCKED', memo: 'OFFSHORE TELEGRAPHIC WIRE / JAFZA DUBAI' },
      { id: 'TX-BFIU-948185', date: '2026-09-02 08:14:20', type: 'IN', counterparty: 'Mohammad Rafiqul Islam (MFS)', counterpartyAccount: 'MFS-BKASH-0171-8840', amount: 4800.00, amountBdt: 576000.00, rail: 'bKash MFS', status: 'FLAGGED', memo: 'MFS BATCH DISBURSEMENT SETTLEMENT' },
      { id: 'TX-BFIU-948160', date: '2026-09-01 16:45:00', type: 'IN', counterparty: 'Meghna Industrial & Agro', counterpartyAccount: 'BD22-EBLB-4829-1092-8823', amount: 32000.00, amountBdt: 3840000.00, rail: 'RTGS (BD Bank)', status: 'COMPLETED', memo: 'COMMERCIAL COMMISSION SETTLEMENT' },
      { id: 'TX-BFIU-948130', date: '2026-08-25 12:10:00', type: 'OUT', counterparty: 'ATM Cash Withdrawal', counterpartyAccount: 'BD04-ATM-GULSHAN-01', amount: 1500.00, amountBdt: 180000.00, rail: 'NPSB ATM', status: 'COMPLETED', memo: 'DEBIT CARD CASH WITHDRAWAL' }
    ],
    activityLogs: [
      { id: 'ACT-801', timestamp: '2026-09-02 08:22:15 UTC', action: 'OUTBOUND_WIRE_BLOCKED', officer: 'Sarah Jenkins', details: 'SWIFT MT103 wire of $47,600 USD blocked. Zero account dwell time flagged.' },
      { id: 'ACT-802', timestamp: '2026-09-02 08:15:00 UTC', action: 'VELOCITY_ALERT_TRIGGERED', officer: 'Hawkes Engine', details: 'Transaction velocity flared to 9.1 tx/min. Account flagged for smurfing fan-in.' },
      { id: 'ACT-803', timestamp: '2022-03-10 11:30:00 UTC', action: 'ACCOUNT_ONBOARDED', officer: 'Gulshan Branch Desk', details: 'Proprietorship current account opened under DSCC trade license.' }
    ]
  },
  'AE-EBIL-1109-8421-4402': {
    account: 'AE-EBIL-1109-8421-4402',
    name: 'Gulf Star Commodities FZE',
    legalType: 'Free Zone Offshore Establishment',
    incorporation: 'JAFZA Free Zone Authority #FZE-88219-DXB',
    openDate: '2023-01-15',
    accountAge: '3 Years, 8 Months',
    institution: 'Emirates NBD Bank PJSC (JAFZA Branch)',
    tin: 'TRN-1002-8841-9921',
    jurisdiction: 'Jebel Ali Free Zone, Dubai, UAE',
    address: 'LOB 15, Suite 402, Jebel Ali Free Zone, Dubai, United Arab Emirates',
    phone: '+971 4-8819200',
    email: 'ops@gulfstar-commodities.ae',
    balance: '$3,890,400.00 USD',
    riskScore: 0.965,
    riskRating: 'HIGH RISK (Offshore Secrecy Shell)',
    kycStatus: 'FOREIGN_INTERMEDIARY_REVIEW',
    kycTier: 'Enhanced Correspondent Due Diligence (EDD)',
    ubo: 'Nominee Director Services Ltd (BVI 100%)',
    pepSanctions: {
      ofacSdn: 'NEGATIVE (Cleared)',
      unSanctions: 'NEGATIVE (Cleared)',
      bfiuWatchlist: 'HIGH-RISK OFFSHORE TRADE CORRIDOR',
      pepDirect: 'OPAQUE BENEFICIAL OWNERSHIP'
    },
    flowConservation: {
      phiFlow: 0.998,
      massBalanceRatio: '1.000 (Exact Conservation)',
      inboundTurnover: '$48,500.00',
      outboundTurnover: '$47,600.00',
      dwellTimeHours: 0.15,
      classification: 'Offshore Re-invoicing Shell'
    },
    counterfactualRemedy: 'Submit certified physical bill of entry and verified Dubai warehouse storage receipts.',
    ledger: [
      { id: 'TX-BFIU-948201', date: '2026-09-02 08:24:10', type: 'IN', counterparty: 'Meghna Industrial & Agro', counterpartyAccount: 'BD22-EBLB-4829-1092-8823', amount: 9450.00, amountBdt: 1134000.00, rail: 'SWIFT MT700 (LC)', status: 'BLOCKED', memo: 'DOC-CREDIT DRAWDOWN BENEFICIARY' },
      { id: 'TX-BFIU-948190', date: '2026-09-02 08:22:15', type: 'IN', counterparty: 'Tanvir Ahmed Rahman', counterpartyAccount: 'BD04-BRAC-1109-8421-4402', amount: 47600.00, amountBdt: 5712000.00, rail: 'SWIFT MT103', status: 'BLOCKED', memo: 'INCOMING TELEGRAPHIC WIRE' },
      { id: 'TX-DXB-8812', date: '2026-08-30 14:00:00', type: 'OUT', counterparty: 'Al-Madina Freight Logistics LLC', counterpartyAccount: 'AE-FAB-9912-3341', amount: 18500.00, amountBdt: 2220000.00, rail: 'UAE-FTS Local Wire', status: 'COMPLETED', memo: 'FREIGHT FORWARDING CLEARANCE' }
    ],
    activityLogs: [
      { id: 'ACT-701', timestamp: '2026-09-02 08:24:10 UTC', action: 'CORRESPONDENT_MONITORING_ALERT', officer: 'BFIU Liaison Desk', details: 'Offshore counterparty identified in circular trade loop back to Dhaka origin.' },
      { id: 'ACT-702', timestamp: '2023-01-15 10:00:00 UTC', action: 'CORRESPONDENT_ONBOARDING', officer: 'Emirates NBD', details: 'JAFZA Free Zone trading entity corporate account registered.' }
    ]
  },
  'MFS-BKASH-0171-8840': {
    account: 'MFS-BKASH-0171-8840',
    name: 'Mohammad Rafiqul Islam (MFS Agent)',
    legalType: 'Retail MFS Agent Outlet',
    incorporation: 'Trade License #DNCC-MFS-2021-9941',
    openDate: '2021-08-12',
    accountAge: '5 Years, 1 Month',
    institution: 'bKash Limited (Agent Wallet Desk)',
    tin: 'TIN-8891-2201-9940',
    jurisdiction: 'Mirpur-10, Dhaka, Bangladesh',
    address: 'Shop #14, Muktijoddha Market, Mirpur-10, Dhaka-1216',
    phone: '+880 1718-840912',
    email: 'rafiqul.mfs@gmail.com',
    balance: '$5,820.00 USD (৳698,400 BDT)',
    riskScore: 0.720,
    riskRating: 'MEDIUM-HIGH RISK (Tier 2 Review)',
    kycStatus: 'AGENT_VELOCITY_REVIEW',
    kycTier: 'Tier-1 MFS Biometric Agent KYC',
    ubo: 'Mohammad Rafiqul Islam (Sole Retail Agent)',
    pepSanctions: {
      ofacSdn: 'NEGATIVE (Cleared)',
      unSanctions: 'NEGATIVE (Cleared)',
      bfiuWatchlist: 'UNDER SURVEILLANCE (Dormancy Surge)',
      pepDirect: 'NOT IDENTIFIED'
    },
    flowConservation: {
      phiFlow: 0.880,
      massBalanceRatio: '0.940',
      inboundTurnover: '$4,800.00',
      outboundTurnover: '$4,800.00',
      dwellTimeHours: 0.12,
      classification: 'Retail MFS Smurfing Aggregator'
    },
    counterfactualRemedy: 'Submit bKash retail POS transaction log and distributor cash-in receipts.',
    ledger: [
      { id: 'TX-BFIU-948185', date: '2026-09-02 08:14:20', type: 'OUT', counterparty: 'Tanvir Ahmed Rahman', counterpartyAccount: 'BD04-BRAC-1109-8421-4402', amount: 4800.00, amountBdt: 576000.00, rail: 'bKash MFS', status: 'FLAGGED', memo: 'MFS B2C WALLET TRANSFER' },
      { id: 'TX-MFS-7712', date: '2026-09-02 08:10:00', type: 'IN', counterparty: 'Retail Cash In (Walk-in)', counterpartyAccount: 'CASH-OVER-COUNTER', amount: 4800.00, amountBdt: 576000.00, rail: 'Over Counter Cash', status: 'COMPLETED', memo: 'CASH INGESTION MULTI-SLOT' }
    ],
    activityLogs: [
      { id: 'ACT-601', timestamp: '2026-09-02 08:14:20 UTC', action: 'DORMANCY_SURGE_FLAGGED', officer: 'MFS Surveillance Gateway', details: 'Account dormant for 340 days initiated sudden remittance transfer.' }
    ]
  },
  'BD20-BSRM-7712-4491-0021': {
    account: 'BD20-BSRM-7712-4491-0021',
    name: 'BSRM Steels Limited',
    legalType: 'Public Listed Corporate (DSE/CSE Listed)',
    incorporation: 'RJSC Registration #C-34192/1984',
    openDate: '1984-11-20',
    accountAge: '41 Years, 10 Months',
    institution: 'Eastern Bank PLC (Agrabad Corporate Branch)',
    tin: 'TIN-9012-3341-8890',
    jurisdiction: 'Agrabad C/A, Chattogram, Bangladesh',
    address: 'Ali Mansion, 1207/1099 Sadarghat Road, Chattogram-4000',
    phone: '+880 31-2854901',
    email: 'corporate.treasury@bsrm.com',
    balance: '$14,250,800.00 USD (৳1,710,096,000 BDT)',
    riskScore: 0.008,
    riskRating: 'LOW RISK (Tier 3 Clear - Licit Corporate)',
    kycStatus: 'VERIFIED_PRIME_CORPORATE',
    kycTier: 'Tier-3 Enhanced Due Diligence (Corporate Clean)',
    ubo: 'BSRM Group Family Holding (54%), Institutional & Public Float (46%)',
    pepSanctions: {
      ofacSdn: 'NEGATIVE (Cleared)',
      unSanctions: 'NEGATIVE (Cleared)',
      bfiuWatchlist: 'NEGATIVE (Clean Record)',
      pepDirect: 'NOT IDENTIFIED'
    },
    flowConservation: {
      phiFlow: 0.720,
      massBalanceRatio: '0.640',
      inboundTurnover: '$3,450,000.00',
      outboundTurnover: '$3,120,000.00',
      dwellTimeHours: 72.0,
      classification: 'Legitimate Prime Corporate Treasury'
    },
    counterfactualRemedy: 'Account operates within normal baseline commercial parameters.',
    ledger: [
      { id: 'TX-BFIU-948202', date: '2026-09-02 08:23:55', type: 'OUT', counterparty: 'Chittagong Port Authority', counterpartyAccount: 'BD00-CPA-PORT-AUTH-02', amount: 28750.00, amountBdt: 3450000.00, rail: 'RTGS (BD Bank)', status: 'CLEARED', memo: 'PORT WHARFAGE & BERTHING DUES / BERTH #4' },
      { id: 'TX-BSRM-9910', date: '2026-08-30 11:00:00', type: 'IN', counterparty: 'Square Pharmaceuticals Ltd', counterpartyAccount: 'BD18-CIBL-3312-8804-1290', amount: 142000.00, amountBdt: 17040000.00, rail: 'BEFTN', status: 'COMPLETED', memo: 'STEEL REBAR COMMERCIAL INVOICE #BSRM-441' }
    ],
    activityLogs: [
      { id: 'ACT-501', timestamp: '2026-09-02 08:23:55 UTC', action: 'STRAIGHT_THROUGH_CLEARED', officer: 'Autonomous Filter', details: 'Routine commercial port authority dues cleared via automated straight-through processing.' }
    ]
  }
};

// Seeded Compliance RFI Requests (Strictly Anti-Tipping-Off Compliant)
export const SEEDED_RFI_REQUESTS = [
  {
    id: 'RFI-2026-1092',
    caseId: 'CASE-2026-0881',
    targetAccount: 'BD22-EBLB-4829-1092-8823',
    targetEntity: 'Meghna Industrial & Agro Processing Ltd',
    amount: '$48,500.00 USD (৳5,820,000 BDT)',
    templateType: 'DOCUMENT_REQUEST_RFI',
    subject: '[SUPPORTING DOCUMENTATION] Request for Information (RFI) — Reference #1092-8823 (LC-2026-CTG-88912)',
    status: 'PENDING_CUSTOMER_UPLOAD',
    issuedDate: '2026-09-02',
    dueDate: '2026-09-07',
    complianceOfficer: 'Sarah Jenkins',
    requiredDocs: [
      'Bangladesh Bank Export Form (EXP) and certified Bill of Lading (B/L)',
      'Commercial invoice or sales contract detailing the counterparty relationship',
      'ASYCUDA Customs Assessment Notice and Port Clearance certificate',
      'Corporate board resolution authorizing the trade signatory'
    ]
  },
  {
    id: 'RFI-2026-1093',
    caseId: 'CASE-2026-0883',
    targetAccount: 'MFS-BKASH-0171-8840',
    targetEntity: 'Mohammad Rafiqul Islam (MFS Agent)',
    amount: '$4,800.00 USD (৳576,000 BDT)',
    templateType: 'SOURCE_OF_FUNDS_DECLARATION',
    subject: '[DUE DILIGENCE] Source of Funds & Purpose of Remittance Declaration',
    status: 'UNDER_OFFICER_REVIEW',
    issuedDate: '2026-09-01',
    dueDate: '2026-09-06',
    complianceOfficer: 'Sarah Jenkins',
    requiredDocs: [
      'Source of Wealth / MFS Agent Trade License declaration form',
      'Certified bank statement of originating commercial capital'
    ]
  }
];

// Seeded Cryptographic Audit Ledger (Chained SHA-256 Hashes)
export const SEEDED_AUDIT_LOGS = [
  {
    id: 'LOG-001',
    action: 'CASE_QUARANTINE_HOLD_INITIATED',
    targetAccount: 'BD22-EBLB-4829-1092-8823 (Meghna Industrial)',
    bankerName: 'Sarah Jenkins',
    role: 'Senior Investigator',
    initiator: 'Sarah Jenkins',
    approver: null,
    fourEyesStatus: 'PENDING_SECOND_SIGNATURE',
    timestamp: '2026-09-02 08:16:00 UTC',
    details: 'Administrative trade hold placed following TBML price divergence & structuring trigger. Exposure: $48,500 (৳5,820,000).',
    merkleHash: '9f8e4b7a12c85d6e3f019a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d',
    prevHash: '0000000000000000000000000000000000000000000000000000000000000000'
  },
  {
    id: 'LOG-002',
    action: 'FOUR_EYES_HOLD_RATIFIED',
    targetAccount: 'BD22-EBLB-4829-1092-8823 (Meghna Industrial)',
    bankerName: 'Nazmul Hasan',
    role: 'Chief Compliance Officer',
    initiator: 'Sarah Jenkins',
    approver: 'Nazmul Hasan',
    fourEyesStatus: 'DUAL_CONTROL_VERIFIED',
    timestamp: '2026-09-02 08:24:10 UTC',
    details: 'Four-Eyes dual signature completed. Mandatory hold certified under BFIU MLPA 2012 §15 & SR 11-7.',
    merkleHash: '3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b',
    prevHash: '9f8e4b7a12c85d6e3f019a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d'
  },
  {
    id: 'LOG-003',
    action: 'COMPLIANT_RFI_PACKAGE_DISPATCHED',
    targetAccount: 'BD22-EBLB-4829-1092-8823 (Meghna Industrial)',
    bankerName: 'Sarah Jenkins',
    role: 'Senior Investigator',
    initiator: 'Sarah Jenkins',
    approver: 'Sarah Jenkins',
    fourEyesStatus: 'SINGLE_ACTION_PERMITTED',
    timestamp: '2026-09-02 08:30:00 UTC',
    details: 'Dispatched Form RFI-2026-1092 (Export EXP and Bill of Lading request) via secure banking portal.',
    merkleHash: '7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d',
    prevHash: '3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b'
  }
];

// Helper to mathematically validate invariants
export function validateInvariants() {
  const sumTiers = RAW_TELEMETRY.tier1Quarantined + RAW_TELEMETRY.tier2ReviewQueue + RAW_TELEMETRY.tier3AutoCleared;
  const matchTotal = sumTiers === RAW_TELEMETRY.totalProcessed24h;
  const matchStp = DERIVED_METRICS.stpRate === 98.6;
  return {
    valid: matchTotal && matchStp,
    sumTiers,
    totalExpected: RAW_TELEMETRY.totalProcessed24h,
    stpCalculated: DERIVED_METRICS.stpRate
  };
}
