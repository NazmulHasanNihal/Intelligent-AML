import { z } from 'zod';

/**
 * Enterprise Banking Zod Validation Schemas (OWASP ASVS Level 2)
 * Enforces strict input validation on all client-server boundaries, preventing injection,
 * parameter tampering, and illicit state transitions.
 */

export const PiiRevealSchema = z.object({
  target_account: z
    .string()
    .min(5, 'Account identifier must be at least 5 characters')
    .max(64, 'Account identifier exceeds maximum length of 64')
    .regex(/^[A-Za-z0-9\-_\.]+$/, 'Invalid characters in account identifier'),
  reason: z
    .string()
    .min(10, 'Mandatory regulatory/operational justification must be at least 10 characters')
    .max(500, 'Justification exceeds maximum length of 500 characters')
});

export type PiiRevealInput = z.infer<typeof PiiRevealSchema>;

export const CaseSignoffSchema = z.object({
  case_id: z
    .string()
    .min(3, 'Case ID must be at least 3 characters')
    .max(64, 'Case ID exceeds 64 characters'),
  approver: z
    .string()
    .min(3, 'Approver name is required')
    .max(128, 'Approver name exceeds 128 characters'),
  notes: z
    .string()
    .min(10, 'Four-Eyes ratification review notes must be at least 10 characters')
    .max(2000, 'Notes exceed 2000 characters')
});

export type CaseSignoffInput = z.infer<typeof CaseSignoffSchema>;

export const TransactionScoreSchema = z.object({
  tx_id: z.string().optional(),
  src_id: z.string().min(3, 'Source account required'),
  dst_id: z.string().min(3, 'Destination account required'),
  amount: z.number().positive('Transaction amount must be strictly greater than zero'),
  cross_border: z.boolean().default(false),
  burst_velocity_spikes: z.boolean().default(false),
  payment_rail: z.enum(['ISO20022_RTGS', 'SWIFT_MT103', 'BEFTN_CLEARING', 'MFS_BKASH', 'FAST_PATH']).default('ISO20022_RTGS'),
  conformal_alpha: z.number().min(0.001).max(0.10).default(0.01)
});

export type TransactionScoreInput = z.infer<typeof TransactionScoreSchema>;

export const CreateCaseSchema = z.object({
  title: z.string().min(5, 'Case title must be at least 5 characters').max(256),
  target_account: z.string().min(5, 'Target account required').max(64),
  priority: z.enum(['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']),
  exposure_usd: z.number().nonnegative('Exposure cannot be negative'),
  cstgb_risk_score: z.number().min(0.0).max(1.0),
  initiator: z.string().min(3, 'Initiator identifier required'),
  lead_assignee: z.string().optional(),
  regulatory_framework: z.string().default('BFIU Form STR-1 (MLPA 2012 §25)')
});

export type CreateCaseInput = z.infer<typeof CreateCaseSchema>;

export const SessionCookieConfig = {
  name: '__Secure-AML-Session',
  options: {
    httpOnly: true,
    secure: true,
    sameSite: 'strict' as const,
    path: '/',
    maxAge: 15 * 60 // 15-minute inactivity session timeout
  }
};
