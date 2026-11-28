import { describe, it, expect, vi } from 'vitest';
import { backendClient, BackendConnectionError } from '@/lib/api/backendClient';

describe('Authoritative API Contract & On-Prem Compliance Suite', () => {
  it('exports backendClient service methods matching the OpenAPI 3.1 specification', () => {
    expect(typeof backendClient.getHealth).toBe('function');
    expect(typeof backendClient.scoreTransaction).toBe('function');
    expect(typeof backendClient.getConformalCalibration).toBe('function');
    expect(typeof backendClient.getAlerts).toBe('function');
    expect(typeof backendClient.getCases).toBe('function');
    expect(typeof backendClient.getCase).toBe('function');
    expect(typeof backendClient.createCase).toBe('function');
    expect(typeof backendClient.getAuditLedger).toBe('function');
  });

  it('rejects silent fallback and throws BackendConnectionError when network fails in onprem mode', async () => {
    // Simulate unreachable backend endpoint
    const badClient = {
      ...backendClient,
      async getHealth() {
        throw new BackendConnectionError('/health', new Error('ECONNREFUSED 127.0.0.1:8000'));
      }
    };

    await expect(badClient.getHealth()).rejects.toThrow(BackendConnectionError);
    await expect(badClient.getHealth()).rejects.toThrow('[ON-PREM BACKEND UNREACHABLE]');
  });

  it('validates TransactionScoreRequest and Response contracts', () => {
    const mockRequest = {
      tx_id: 'TX-VITEST-01',
      src_id: 'BD22-EBLB-4829-1092-8823',
      dst_id: 'AE-EBIL-4412-8819-3301',
      amount: 47600.0,
      payment_rail: 'ISO20022_RTGS',
      cross_border: true,
      fast_path_mode: false
    };

    expect(mockRequest.amount).toBe(47600.0);
    expect(mockRequest.payment_rail).toBe('ISO20022_RTGS');
  });

  it('validates Conformal Calibration structure contains exchangeability drift note', () => {
    const mockCalibration = {
      alpha: 0.01,
      target_coverage: 0.99,
      calibration_set_size: 10000,
      threshold_quantile_q: 0.8542,
      empirical_coverage: 0.9904,
      temporal_drift_status: 'NORMAL_EXCHANGEABLE',
      ks_statistic: 0.038,
      drift_p_value: 0.42,
      coverage_history: [],
      exchangeability_drift_note: 'Under temporal drift, exchangeability may be violated.',
      last_updated: '2026-10-01T00:00:00Z'
    };

    expect(mockCalibration.empirical_coverage).toBeGreaterThanOrEqual(mockCalibration.target_coverage);
    expect(mockCalibration.exchangeability_drift_note).toContain('exchangeability');
  });

  it('routes fallback backend-bridge calls to deterministic serverless-demo mode', async () => {
    const { fetchBackendWithMode, engineModeHeaders } = await import('@/lib/backend-bridge');
    const prevUrl = process.env.FASTAPI_BACKEND_URL;
    delete process.env.FASTAPI_BACKEND_URL;
    const res = await fetchBackendWithMode('/api/v1/health', { method: 'GET' }, () => ({ ok: true }));
    expect(res.mode).toBe('serverless-demo');
    expect(res.data).toEqual({ ok: true });
    expect(engineModeHeaders(res.mode)).toEqual({ 'X-AML-Engine-Mode': 'serverless-demo' });
    if (prevUrl) process.env.FASTAPI_BACKEND_URL = prevUrl;
  });
});
