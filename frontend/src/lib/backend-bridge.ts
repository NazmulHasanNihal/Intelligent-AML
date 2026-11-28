/**
 * backend-bridge.ts — Next.js 16 Hybrid BFF Backend Bridge
 *
 * Forwards /api/v1/* requests to configured FASTAPI_BACKEND_URL with a strict
 * 3-second AbortSignal.timeout(3000), seamlessly falling back to the deterministic
 * local TypeScript C-STGB engine when operating in standalone serverless mode.
 */

export type EngineExecutionMode = 'fastapi-live' | 'serverless-demo';

export interface BackendBridgeOptions {
  timeoutMs?: number;
}

export interface BridgeResult<T> {
  data: T;
  mode: EngineExecutionMode;
}

export async function fetchBackendWithMode<T>(
  endpoint: string,
  init: RequestInit = {},
  fallbackFn: () => Promise<T> | T,
  options: BackendBridgeOptions = {}
): Promise<BridgeResult<T>> {
  const backendBase = process.env.FASTAPI_BACKEND_URL || process.env.BACKEND_API_URL;
  const timeoutMs = options.timeoutMs ?? 3000;

  if (!backendBase) {
    return {
      data: await fallbackFn(),
      mode: 'serverless-demo'
    };
  }

  const url = `${backendBase.replace(/\/+$/, '')}/${endpoint.replace(/^\/+/, '')}`;
  const timeoutSignal =
    typeof AbortSignal !== 'undefined' && typeof AbortSignal.timeout === 'function'
      ? AbortSignal.timeout(timeoutMs)
      : undefined;

  try {
    const response = await fetch(url, {
      ...init,
      headers: {
        'Content-Type': 'application/json',
        'X-BFF-Proxy': 'Intelligent-AML-Next16-BFF',
        ...(init.headers || {})
      },
      signal: init.signal ?? timeoutSignal
    });

    if (!response.ok) {
      return {
        data: await fallbackFn(),
        mode: 'serverless-demo'
      };
    }

    return {
      data: (await response.json()) as T,
      mode: 'fastapi-live'
    };
  } catch {
    return {
      data: await fallbackFn(),
      mode: 'serverless-demo'
    };
  }
}

export function engineModeHeaders(mode: EngineExecutionMode = 'serverless-demo'): Record<string, string> {
  return {
    'X-AML-Engine-Mode': mode
  };
}
