# EXECUTION_PLAN.md — Intelligent-AML Master Directive

## Phase 1 Findings
- `frontend/src/components/DemoToolsModal.jsx:41` conflates `$9,450` USD (`৳1,134,000` BDT) with being beneath the `৳1,000,000` BDT cash CTR threshold.
- `frontend/next.config.ts` sets `Referrer-Policy: strict-origin-when-cross-origin` instead of `no-referrer`.
- `frontend/package.json` lacks `"engines": { "node": ">=20.9.0" }`.
- `frontend/src/app/api/v1/health/route.ts` is missing (`/api/health` exists without `v1` contract fields `{ status: "ok", mode, nextVersion, timestamp, merkleVerified }`).
- `frontend/src/lib/backend-bridge.ts` does not exist separately (`apiAdapter.ts` handles proxy fallback with 2.5s manual timeout instead of `AbortSignal.timeout(3000)` + `X-AML-Engine-Mode: serverless-demo` response header).
- `frontend/src/app/graph/page.tsx` renders a static placeholder for `3D WebGL` view instead of a client-only dynamically imported `3d-force-graph` component with `webglcontextlost` and `.dispose()` cleanup, and caps the edge-trust gate slider at `0.50` instead of `0.95`.
- Dynamic `/api/v1/*` route handlers should explicitly declare `export const dynamic = "force-dynamic"`.

## Execution Mapping (Parts A–D)

### Part A — Unblock AI Agents & Crawlers (Reversible)
1. `frontend/src/app/robots.ts` & `frontend/src/proxy.ts`: Keep `Allow: /`, `/governance`, `/app`, `Disallow: /api/`, primary `export function proxy` (with Next.js 16 matcher excluding static assets), `ALLOW_PUBLIC_AUDIT !== "false"` toggle, and `Referrer-Policy: no-referrer`.
2. `frontend/next.config.ts`: Align `Referrer-Policy: no-referrer` while preserving `CSP`, `HSTS`, `X-Content-Type-Options`, `X-Frame-Options`, `Permissions-Policy`.

### Part B — Audit, Math, Legal & UX Remediation
1. `frontend/src/components/DemoToolsModal.jsx`: Separate TBML LC splitting (`$9,450 / $9,600 / $9,800` beneath `$10,000` correspondent review + `+333.7%` ASYCUDA over-invoicing) from cash/MFS structuring (`৳954,000` / `$7,950` beneath `৳1,000,000` BFIU cash CTR).
2. `frontend/src/lib/compliance/jurisdictions.ts`: Include `MLPA 2012 §§ 6, 25, 27` and `BFIU Circular 26, 31 & 32` in `BD_BFIU` statutory profile alongside `US_FINCEN` and `EU_AMLA`.

### Part C — Next.js 16 / Vercel / Security Hardening
1. `frontend/package.json`: Add `"engines": { "node": ">=20.9.0" }`.
2. `frontend/src/lib/backend-bridge.ts` & `frontend/src/lib/apiAdapter.ts`: Implement typed `fetchBackendWithFallback` using `AbortSignal.timeout(3000)` and exposing `X-AML-Engine-Mode` (`fastapi-live` | `serverless-demo`).
3. `frontend/src/app/api/v1/health/route.ts`: Add `GET /api/v1/health` (`force-dynamic`) returning `{ status: "ok", mode, nextVersion, timestamp, merkleVerified: true }`.
4. Add `export const dynamic = "force-dynamic"` across `/api/v1/*` handlers.
5. `frontend/src/components/graph/ForceGraph3DCanvas.tsx`: Create client-only `3d-force-graph` component with WebGL detection, `webglcontextlost` recovery to 2D, and WebGL renderer `.dispose()` on unmount; load via `next/dynamic(..., { ssr: false })`.

### Part D — Interactive Control Activation
1. `frontend/src/app/graph/page.tsx`: Connect real `ForceGraph3DCanvas`, extend Edge Trust Gate slider (`0.00 -> 0.95`), and ensure live chronological `Hawkes Temporal Playback (Δt)` edge filtering during playback/scrubbing.
2. `frontend/src/app/sar/page.tsx`: Ensure `"Show Officer Edit Diff"` & multi-jurisdiction XML export remain live and verified.

### Part E — Verification Gates
- `Remove-Item -Recurse -Force frontend/.next`
- `VERCEL=1` runs of `npx tsc --noEmit`, `npm run lint`, `npm test`, `npm run build`
- Zero external CDN scan (`googleapis`, `unpkg`, `jsdelivr`)
- Live HTTP 200 verification on `/`, `/robots.txt`, `/governance`, `/app`, and `/api/v1/health`.
