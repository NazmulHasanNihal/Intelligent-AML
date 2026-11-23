/**
 * backendClient.ts — Strongly-Typed Client for FastAPI / DuckDB / PyTorch Backend
 *
 * Generated from OpenAPI contract (api/openapi.json).
 * Single Source of Truth: In APP_MODE=onprem, delegates all queries to FastAPI backend.
 * Zero hardcoded mock arrays are returned when running in onprem mode.
 */

import { IS_ONPREM_MODE } from '@/lib/config/env';

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export class BackendConnectionError extends Error {
  constructor(endpoint: string, originalError: any) {
    super(`[ON-PREM BACKEND UNREACHABLE] Failed to connect to FastAPI at ${endpoint}. Details: ${originalError?.message || originalError}`);
    this.name = 'BackendConnectionError';
  }
}

// -----------------------------------------------------------------------------
// Typed Contract Interfaces (Matching openapi.json)
// -----------------------------------------------------------------------------

export interface TransactionScoreRequest {
  tx_id?: string;
  src_id: string;
  dst_id: string;
  amount: number;
  timestamp?: number;
  cross_border?: boolean;
  burst_velocity_spikes?: boolean;
  payment_rail?: string;
  conformal_alpha?: number;
  fast_path_mode?: boolean;
}

export interface TransactionScoreResponse {
  tx_id: string;
  src_id: string;
  dst_id: string;
  amount: number;
  ensemble_posterior_prob: number;
  p_gnn: number;
  p_tabular: number;
  p_fused: number;
  decision_tier: string;
  conformal_prediction_set: string[];
  conformal_alpha: number;
  conformal_coverage_pct: number;
  rule_engine_action: string;
  latency_breakdown_ms: Record<string, number>;
  total_latency_ms: number;
  audit_merkle_receipt: string;
  model_version?: string;
  model_artifact_hash?: string;
}

export interface ConformalCalibrationResponse {
  alpha: number;
  target_coverage: number;
  calibration_set_size: number;
  threshold_quantile_q: number;
  empirical_coverage: number;
  temporal_drift_status: string;
  ks_statistic: number;
  drift_p_value: number;
  coverage_history: Array<{
    week: string;
    coverage: number;
    sample_count: number;
    ks_stat: number;
  }>;
  exchangeability_drift_note: string;
  last_updated: string;
}

export interface BackendAlert {
  id: string;
  target_account: string;
  counterparty: string;
  amount_usd: number;
  risk_score: number;
  tier: string;
  typology: string;
  conformal_set: string[];
  status: string;
  assignee?: string;
  latency_ms: number;
  timestamp: string;
}

export interface AlertListResponse {
  total: number;
  page: number;
  limit: number;
  alerts: BackendAlert[];
}

export interface BackendCase {
  id: string;
  title: string;
  target_account: string;
  status: string;
  priority: string;
  exposure_usd: number;
  cstgb_risk_score: number;
  initiator: string;
  lead_assignee: string;
  second_approver?: string | null;
  regulatory_framework: string;
  linked_alert_ids: string[];
  grounded_evidence: any[];
  timeline: any[];
  notes: any[];
  attachments: any[];
  created_at: string;
}

export interface AuditLedgerResponse {
  total_blocks: number;
  chain_valid: boolean;
  blocks: Array<{
    index: number;
    prev_hash: string;
    curr_hash: string;
    timestamp: string;
    event_type: string;
    actor: string;
    payload: Record<string, any>;
  }>;
}

// -----------------------------------------------------------------------------
// Core HTTP Requester
// -----------------------------------------------------------------------------

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${BASE_URL}${endpoint}`;
  try {
    const res = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
        ...(options.headers || {})
      }
    });

    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`HTTP ${res.status}: ${errorText}`);
    }

    return await res.json() as T;
  } catch (err: any) {
    if (IS_ONPREM_MODE) {
      // In onprem mode, failure to connect to FastAPI is a hard failure (no silent mocks)
      throw new BackendConnectionError(endpoint, err);
    }
    // Re-throw for caller to handle in demo mode
    throw err;
  }
}

// -----------------------------------------------------------------------------
// API Client Service Methods
// -----------------------------------------------------------------------------

export const backendClient = {
  /**
   * Health and readiness checks
   */
  async getHealth(): Promise<{ status: string; engine: string; version: string }> {
    return request('/health');
  },

  /**
   * Real-time tiered scoring (FastPath -> Rules -> Lightweight Model -> Conformal Set)
   */
  async scoreTransaction(payload: TransactionScoreRequest): Promise<TransactionScoreResponse> {
    return request<TransactionScoreResponse>('/api/v1/score', {
      method: 'POST',
      body: JSON.stringify(payload)
    });
  },

  /**
   * Conformal prediction calibration parameters & temporal drift status
   */
  async getConformalCalibration(): Promise<ConformalCalibrationResponse> {
    return request<ConformalCalibrationResponse>('/api/v1/conformal/calibration');
  },

  /**
   * Paginated and filtered alert queue from persistent storage
   */
  async getAlerts(params: {
    tier?: string;
    status?: string;
    page?: number;
    limit?: number;
  } = {}): Promise<AlertListResponse> {
    const query = new URLSearchParams();
    if (params.tier) query.set('tier', params.tier);
    if (params.status) query.set('status', params.status);
    if (params.page) query.set('page', params.page.toString());
    if (params.limit) query.set('limit', params.limit.toString());
    const qs = query.toString() ? `?${query.toString()}` : '';
    return request<AlertListResponse>(`/api/v1/alerts${qs}`);
  },

  /**
   * Case management endpoints
   */
  async getCases(status?: string): Promise<BackendCase[]> {
    const qs = status ? `?status=${encodeURIComponent(status)}` : '';
    return request<BackendCase[]>(`/api/v1/cases${qs}`);
  },

  async getCase(caseId: string): Promise<BackendCase> {
    return request<BackendCase>(`/api/v1/cases/${encodeURIComponent(caseId)}`);
  },

  async createCase(caseData: {
    title: string;
    target_account: string;
    priority: string;
    exposure_usd: number;
    cstgb_risk_score: number;
    initiator: string;
    lead_assignee?: string;
    regulatory_framework?: string;
  }): Promise<BackendCase> {
    return request<BackendCase>('/api/v1/cases', {
      method: 'POST',
      body: JSON.stringify(caseData)
    });
  },

  /**
   * WORM Cryptographic audit ledger
   */
  async getAuditLedger(): Promise<AuditLedgerResponse> {
    return request<AuditLedgerResponse>('/api/v1/audit/ledger');
  },

  /**
   * Model distribution drift status
   */
  async getDriftStatus(): Promise<any> {
    return request('/api/v1/models/drift-status');
  }
};
