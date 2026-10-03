/**
 * Intelligent-AML Enterprise TypeScript Definitions
 * Standardized across C-STGB Model, FastAPI v1 REST API, and Vite Frontend
 */

export type DecisionTier = 'Tier 1 Hold' | 'Tier 2 Review' | 'Tier 3 Clear';

export type CaseStatus = 
  | 'OPEN'
  | 'UNDER_INVESTIGATION'
  | 'SAR_PENDING_APPROVAL'
  | 'SAR_APPROVED_FILED'
  | 'CLOSED_FALSE_POSITIVE';

export interface GroundedEvidence {
  id: string;
  claim: string;
  ref: string;
}

export interface CaseAttachment {
  id: string;
  name: string;
  size: string;
  type: string;
  uploadedAt: string;
  uploadedBy: string;
}

export interface CaseNote {
  id: string;
  author: string;
  time: string;
  text: string;
}

export interface CaseTimelineEvent {
  id: number;
  time: string;
  event: string;
}

export interface AMLCase {
  id: string;
  title: string;
  subjectEntity: string;
  subjectAccount: string;
  subjectBic?: string;
  totalExposure: number;
  riskScore: number;
  tier: DecisionTier;
  status: CaseStatus;
  assignedTo: string;
  fourEyesInitiator: string;
  fourEyesApprover: string | null;
  fourEyesVerified: boolean;
  openedAt: string;
  slaDeadline: string;
  statutoryJurisdiction: string;
  statutorySlaHours: number;
  linkedAlertIds: string[];
  timeline: CaseTimelineEvent[];
  notes: CaseNote[];
  sourcesUsed: GroundedEvidence[];
  attachments?: CaseAttachment[];
}

export interface AMLAlert {
  id: string;
  caseId: string;
  timestamp: string;
  account: string;
  entityName: string;
  amount: number;
  caseTotalExposure: number;
  rail: string;
  bic: string;
  counterparty: string;
  counterpartyName: string;
  counterpartyBic: string;
  tier: DecisionTier;
  tierCode: 1 | 2 | 3;
  riskScore: number;
  pConformal: number;
  status: 'ESCALATED_MLRO' | 'NEW_UNASSIGNED' | 'DISMISSED';
  assignee: string;
  typology: string;
  slaMinutesLeft: number;
  whyFlagged: string;
  shapDrivers: Array<{
    name: string;
    weight: number;
    direction: 'risk' | 'mitigant';
  }>;
}

export interface AuditBlock {
  index: number;
  prev_hash: string;
  curr_hash: string;
  timestamp: string;
  event_type: string;
  actor: string;
  payload: Record<string, unknown>;
}

export interface RFIRequest {
  id: string;
  caseId: string;
  targetAccount: string;
  targetEntity: string;
  amount: string;
  templateType: string;
  subject: string;
  status: 'PENDING_CUSTOMER_UPLOAD' | 'IN_REVIEW' | 'FULFILLED' | 'EXPIRED';
  issuedDate: string;
  dueDate: string;
  complianceOfficer: string;
  requiredDocs: string[];
}

export interface InvariantMetrics {
  total24hTransactions: number;
  straightThroughRatePct: number;
  tier1QuarantineCount: number;
  tier1Pct: number;
  tier2ReviewCount: number;
  tier2Pct: number;
  tier3ClearedCount: number;
  tier3Pct: number;
  activeThroughputTps: number;
  peakCapacityTps: number;
}
