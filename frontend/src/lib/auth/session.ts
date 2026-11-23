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

/**
 * Standardized Institutional Demonstration Personas (Ground Rule 1 & Phase 1 Compliance)
 * Clearly designated fictional institutional operators for research evaluation and BFIU workflow demonstration.
 */
export const BANKER_PERSONAS: Record<BankingRole, BankerProfile> = {
  CCO_L3: {
    id: 'BNK-7842',
    name: 'Kazi Rafiqul Islam, CAMS (Demo CCO)',
    role: 'CCO_L3',
    roleTitle: 'Chief Compliance Officer & MLRO (Demo L3 Checker)',
    department: 'Financial Crime Compliance Directorate (Demo)',
    institution: 'Eastern Commercial Bank PLC — BFIU Compliance Desk',
    avatar: 'KR',
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
    name: 'Amina Rahman, CFE (Demo Lead Investigator)',
    role: 'INVESTIGATOR_L2',
    roleTitle: 'Senior AML Forensic Investigator (Demo L2 Maker)',
    department: 'Special Investigations & Trade AML Unit (Demo)',
    institution: 'Eastern Commercial Bank PLC — High-Risk Surveillance Hub',
    avatar: 'AR',
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
    name: 'Tanvir Ahmed (Demo Triage Analyst)',
    role: 'ANALYST_L1',
    roleTitle: 'First-Line Triage Analyst (Demo L1 Maker)',
    department: 'Real-Time Clearing Surveillance Desk (Demo)',
    institution: 'Eastern Commercial Bank PLC — Ingestion Gateway',
    avatar: 'TA',
    permissions: [
      'TRIAGE_READ',
      'FLAG_ANOMALOUS_EVENT',
      'ESCALATE_TO_SIU'
    ]
  },
  MODEL_AUDITOR: {
    id: 'BNK-9901',
    name: 'Dr. S. K. Haque, FRM (Demo Model Validator)',
    role: 'MODEL_AUDITOR',
    roleTitle: 'Independent Quantitative Risk Validator (Demo SR 11-7 Lead)',
    department: 'Model Risk Management & Algorithmic Audit (Demo)',
    institution: 'Supervisory Audit Group — Research Prototype Evaluation',
    avatar: 'SH',
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
