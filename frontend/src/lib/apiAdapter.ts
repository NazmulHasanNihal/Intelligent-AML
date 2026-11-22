/**
 * apiAdapter.ts — Tier-1 Banking Hybrid BFF (Backend-For-Frontend) Adapter
 * 
 * Routes requests to external FastAPI backend (when configured and healthy)
 * with automatic, zero-downtime fallback to local in-memory TypeScript C-STGB engine
 * during standalone serverless Vercel deployments.
 */

export interface HybridBffOptions {
  timeoutMs?: number;
  tags?: string[];
}

export async function fetchFastApiWithFallback<T>(
  endpoint: string,
  init: RequestInit = {},
  fallbackFn: () => Promise<T> | T,
  options: HybridBffOptions = {}
): Promise<T> {
  const backendBase = process.env.FASTAPI_BACKEND_URL || process.env.BACKEND_API_URL;
  const timeoutMs = options.timeoutMs ?? 2500;

  if (!backendBase) {
    // Zero-config standalone serverless mode (e.g. Vercel deployment preview)
    return await fallbackFn();
  }

  const url = `${backendBase.replace(/\/+$/, '')}/${endpoint.replace(/^\/+/, '')}`;
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, {
      ...init,
      headers: {
        'Content-Type': 'application/json',
        'X-BFF-Proxy': 'Intelligent-AML-Next16-BFF',
        ...(init.headers || {})
      },
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      console.warn(`[Hybrid BFF] Backend returned HTTP ${response.status} for ${endpoint}. Falling back to internal engine.`);
      return await fallbackFn();
    }

    return (await response.json()) as T;
  } catch (err: unknown) {
    clearTimeout(timeoutId);
    const message = err instanceof Error ? err.message : String(err);
    console.info(`[Hybrid BFF] Upstream FastAPI unavailable (${message}). Activating deterministic in-memory C-STGB engine.`);
    return await fallbackFn();
  }
}
