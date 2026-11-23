export type BankingRole =
  | 'ANALYST_L1'
  | 'ANALYST_L2'
  | 'SUPERVISOR'
  | 'MLRO_CAMLCO'
  | 'AUDITOR'
  | 'ADMIN'
  | 'INVESTIGATOR_L2'
  | 'CCO_L3'
  | 'MODEL_AUDITOR';

export interface BankerProfile {
  id: string;
  name: string;
  role: BankingRole;
  roleTitle: string;
  department: string;
  institution: string;
  avatar: string;
  permissions: string[];
  mfaVerified: boolean;
  authMethod: string;
  sessionTimeoutMinutes: number;
}

const personaL1: BankerProfile = {
  id: 'BNK-1092',
  name: 'Tanvir Ahmed (Demo Triage Analyst)',
  role: 'ANALYST_L1',
  roleTitle: 'First-Line Triage Analyst (Demo L1 Maker)',
  department: 'Real-Time Clearing Surveillance Desk',
  institution: 'Eastern Bank PLC',
  avatar: 'TA',
  permissions: [
    'TRIAGE_READ',
    'FLAG_ANOMALOUS_EVENT',
    'ESCALATE_TO_SIU'
  ],
  mfaVerified: true,
  authMethod: 'OIDC_SSO_MFA',
  sessionTimeoutMinutes: 15
};

const personaL2: BankerProfile = {
  id: 'BNK-4419',
  name: 'Amina Rahman, CFE (Demo Lead Investigator)',
  role: 'ANALYST_L2',
  roleTitle: 'Senior AML Forensic Investigator (Demo L2 Maker)',
  department: 'Special Investigations & Trade AML Unit',
  institution: 'Eastern Bank PLC',
  avatar: 'AR',
  permissions: [
    'TRIAGE_EVALUATE',
    'PROPOSE_FREEZE',
    'DRAFT_REGULATORY_SAR',
    'DISPATCH_RFI_NOTICE',
    'PIN_CASE_EVIDENCE',
    'GRAPH_FORENSICS_DEEP',
    'PII_REVEAL'
  ],
  mfaVerified: true,
  authMethod: 'OIDC_SSO_MFA',
  sessionTimeoutMinutes: 15
};

const personaSup: BankerProfile = {
  id: 'BNK-8821',
  name: 'Farhana Ahmed, CAMS (Demo Compliance Supervisor)',
  role: 'SUPERVISOR',
  roleTitle: 'AML Operations & Alert Triage Supervisor (Demo Checker)',
  department: 'Financial Crime Compliance Operations',
  institution: 'Eastern Bank PLC',
  avatar: 'FA',
  permissions: [
    'ALL_CASES_READ',
    'FREEZE_FUNDS_DUAL_AUTH',
    'RATIFY_CASE_4EYES',
    'APPROVE_REGULATORY_SAR',
    'PII_REVEAL',
    'ASSIGN_INVESTIGATORS'
  ],
  mfaVerified: true,
  authMethod: 'OIDC_SSO_MFA',
  sessionTimeoutMinutes: 15
};

const personaMLRO: BankerProfile = {
  id: 'BNK-7842',
  name: 'Kazi Rafiqul Islam, CAMS (Demo CAMLCO)',
  role: 'MLRO_CAMLCO',
  roleTitle: 'Chief Anti-Money Laundering Compliance Officer (Demo L3 Checker)',
  department: 'Financial Crime Compliance Directorate',
  institution: 'Eastern Bank PLC',
  avatar: 'KR',
  permissions: [
    'ALL',
    'FREEZE_FUNDS_DUAL_AUTH',
    'RELEASE_FUNDS_DUAL_AUTH',
    'FILE_REGULATORY_SAR_4EYES',
    'DISPATCH_CUSTOMER_NOTICE',
    'AUDIT_INSPECT_WORM',
    'MODEL_GOVERNANCE_OVERRIDE',
    'EMERGENCY_QUARANTINE',
    'PII_REVEAL'
  ],
  mfaVerified: true,
  authMethod: 'OIDC_SSO_MFA',
  sessionTimeoutMinutes: 15
};

const personaAuditor: BankerProfile = {
  id: 'BNK-9901',
  name: 'Dr. S. K. Haque, FRM (Demo Model Validator)',
  role: 'AUDITOR',
  roleTitle: 'Independent Quantitative Risk Validator (Demo Auditor)',
  department: 'Model Risk Management & Algorithmic Audit',
  institution: 'Supervisory Audit Oversight Bureau',
  avatar: 'SH',
  permissions: [
    'SR11_7_READ',
    'CALIBRATION_AUDIT',
    'INSPECT_INVARIANTS',
    'EXPORT_REPRODUCIBILITY_PACK',
    'AUDIT_INSPECT_WORM'
  ],
  mfaVerified: true,
  authMethod: 'OIDC_SSO_MFA',
  sessionTimeoutMinutes: 15
};

const personaAdmin: BankerProfile = {
  id: 'BNK-0001',
  name: 'System Security Administrator',
  role: 'ADMIN',
  roleTitle: 'Platform Security & Infrastructure Admin',
  department: 'Enterprise Security Architecture',
  institution: 'Eastern Bank PLC',
  avatar: 'SA',
  permissions: ['ALL'],
  mfaVerified: true,
  authMethod: 'OIDC_SSO_MFA',
  sessionTimeoutMinutes: 15
};

export const BANKER_PERSONAS: Record<BankingRole, BankerProfile> = {
  ANALYST_L1: personaL1,
  ANALYST_L2: personaL2,
  SUPERVISOR: personaSup,
  MLRO_CAMLCO: personaMLRO,
  AUDITOR: personaAuditor,
  ADMIN: personaAdmin,
  INVESTIGATOR_L2: personaL2,
  CCO_L3: personaMLRO,
  MODEL_AUDITOR: personaAuditor
};

export function canExecuteAction(role: string, action: string): boolean {
  const profile = (BANKER_PERSONAS as Record<string, BankerProfile>)[role];
  if (!profile) return false;
  if (profile.permissions.includes('ALL')) return true;
  return profile.permissions.includes(action);
}

export function canApproveCase(role: string): boolean {
  return role === 'SUPERVISOR' || role === 'MLRO_CAMLCO' || role === 'CCO_L3' || role === 'ADMIN';
}

export function canRevealPii(role: string): boolean {
  return role === 'ANALYST_L2' || role === 'INVESTIGATOR_L2' || role === 'SUPERVISOR' || role === 'MLRO_CAMLCO' || role === 'CCO_L3' || role === 'ADMIN';
}
