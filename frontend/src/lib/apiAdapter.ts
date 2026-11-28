/**
 * apiAdapter.ts — Tier-1 Banking Hybrid BFF (Backend-For-Frontend) Adapter
 * Delegates to backend-bridge.ts with 3s AbortSignal.timeout and deterministic fallback.
 */

import {
  fetchBackendWithMode,
  engineModeHeaders,
  type EngineExecutionMode,
  type BackendBridgeOptions
} from '@/lib/backend-bridge';

export type HybridBffOptions = BackendBridgeOptions;
export { fetchBackendWithMode, engineModeHeaders, type EngineExecutionMode };

export async function fetchFastApiWithFallback<T>(
  endpoint: string,
  init: RequestInit = {},
  fallbackFn: () => Promise<T> | T,
  options: HybridBffOptions = {}
): Promise<T> {
  const { data } = await fetchBackendWithMode(endpoint, init, fallbackFn, options);
  return data;
}
