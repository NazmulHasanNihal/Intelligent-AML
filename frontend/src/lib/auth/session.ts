export type BankingRole = 'ANALYST_L1' | 'INVESTIGATOR_L2' | 'CCO_L3' | 'MODEL_AUDITOR';

export interface BankerProfile {
  id: string;
  name: string;
  role: BankingRole;
  roleTitle: string;
  department: string;
  institution: string;
  avatar: string;
  permissions: string[];
}

export const BANKER_PERSONAS: Record<BankingRole, BankerProfile> = {
  CCO_L3: {
    id: 'BNK-7842',
    name: 'Nazmul Hasan, CAMS',
    role: 'CCO_L3',
    roleTitle: 'Chief Compliance Officer (CCO / L3 Checker)',
    department: 'Global Financial Crimes Division',
    institution: 'JPMorgan Chase & Co. — Global FIU Operations',
    avatar: 'NH',
    permissions: [
      'ALL',
      'FREEZE_FUNDS_DUAL_AUTH',
      'RELEASE_FUNDS_DUAL_AUTH',
      'FILE_REGULATORY_SAR_4EYES',
      'DISPATCH_CUSTOMER_NOTICE',
      'AUDIT_INSPECT_WORM',
      'MODEL_GOVERNANCE_OVERRIDE',
      'EMERGENCY_QUARANTINE'
    ]
  },
  INVESTIGATOR_L2: {
    id: 'BNK-4419',
    name: 'Sarah L. Jenkins, CFE',
    role: 'INVESTIGATOR_L2',
    roleTitle: 'Senior AML Compliance Investigator (L2 Maker)',
    department: 'Special Investigations Unit (SIU)',
    institution: 'Citibank N.A. — High-Risk Surveillance Hub',
    avatar: 'SJ',
    permissions: [
      'TRIAGE_EVALUATE',
      'PROPOSE_FREEZE',
      'DRAFT_REGULATORY_SAR',
      'DISPATCH_RFI_NOTICE',
      'PIN_CASE_EVIDENCE',
      'GRAPH_FORENSICS_DEEP'
    ]
  },
  ANALYST_L1: {
    id: 'BNK-1092',
    name: 'Musrat Jahan Gungun',
    role: 'ANALYST_L1',
    roleTitle: 'First-Line Triage Analyst (L1 Maker)',
    department: 'Real-Time Clearing Surveillance Desk',
    institution: 'Standard Chartered Bank — Transaction Gateway',
    avatar: 'MJ',
    permissions: [
      'TRIAGE_READ',
      'FLAG_ANOMALOUS_EVENT',
      'ESCALATE_TO_SIU'
    ]
  },
  MODEL_AUDITOR: {
    id: 'BNK-9901',
    name: 'Dr. Tariq Rahman, FRM',
    role: 'MODEL_AUDITOR',
    roleTitle: 'Independent Model Risk Auditor (MRM Lead)',
    department: 'Quantitative Validation Group (SR 11-7)',
    institution: 'Bank for International Settlements (BIS)',
    avatar: 'TR',
    permissions: [
      'SR11_7_READ',
      'CALIBRATION_AUDIT',
      'INSPECT_INVARIANTS',
      'EXPORT_REPRODUCIBILITY_PACK'
    ]
  }
};

export function canExecuteAction(role: BankingRole, action: string): boolean {
  const profile = BANKER_PERSONAS[role];
  if (!profile) return false;
  if (profile.permissions.includes('ALL')) return true;
  return profile.permissions.includes(action);
}
