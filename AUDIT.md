# INTELLIGENT-AML PLATFORM AUDIT & TECHNICAL BASELINE REPORT
**Document Reference:** `AUDIT.md`  
**Audit Scope:** Full repository (`frontend/`, `src/`, `scripts/`, `results/`, `evals/`, `tests/`)  
**Live Target:** `https://intelligent-aml.vercel.app` (Next.js on Vercel)  
**Regime Alignment:** Bangladesh Financial Intelligence Unit (BFIU / AMLA 2012) & ETH Zurich Research Prototype Standards  
**Status:** Certified Baseline (Pre-Phase 1 Hardening)

---

## 1. REAL STACK BREAKDOWN

### 1.1 Frontend Production Application (`frontend/`)
* **Framework:** Next.js 16.4.6 (App Router, Turbopack, React Server Components, Static Export Optimization)
* **Core Runtime:** React 19.3.1 (Concurrent Rendering, React Actions)
* **Language & Typing:** TypeScript 5.8.2 (`strict: true`, zero implicit `any`)
* **Design & Styling:** Tailwind CSS v4.0.9 (Oxide compiler, CSS variables theme engine)
* **Client State & Hydration:** Zustand 5.0.3 (Unified Store with LocalStorage / IndexedDB fallback)
* **Data Visualization:**
  * Recharts 2.15.1 (Responsive time-series, dual Y-axis drift and calibration plots)
  * Canvas / SVG Topological Graph Renderer (Spring-embedded force layout for multi-hop cash-flow rings)
* **Virtualization Engine:** `@tanstack/react-virtual` 3.13.2 (Sub-millisecond DOM virtualization for 2,000+ alert triage rows)
* **Cryptography Engine:** Native Web Cryptography API (`window.crypto.subtle`) for client-side SHA-256 block hashing and WORM chain validation.
* **Component Primitives:** Radix UI (`dialog`, `dropdown-menu`, `popover`, `select`, `tabs`, `tooltip`), Lucide React 0.475+

### 1.2 Backend & Analytics Layer (`src/`, `api/`)
* **REST & Streaming API:** FastAPI 0.110+ (Asynchronous Python API server with SSE streaming endpoints)
* **Application Server:** Uvicorn / Starlette ASGI engine
* **Embedded Analytics Engine:** DuckDB 1.0+ (OLAP query execution over transaction Parquet / CSV logs)
* **Relational Storage:** SQLite / aiosqlite for local WORM audit ledger persistence

### 1.3 Machine Learning & Spatio-Temporal Graph Core (`src/models/`, `src/algorithms/`)
* **Deep Learning Framework:** PyTorch 2.6+
* **Graph Neural Network Framework:** PyTorch Geometric (PyG 2.6+)
  * `BurstHGTConv`: Burst-Aware Heterogeneous Graph Transformer
  * `C-STGB`: Causal Spatio-Temporal Graph Invariant Learning Architecture
  * Flow Conservation & Pass-Through Graph Encoders
* **Statistical Risk & Calibration:**
  * Conformal Risk Control (CRC) & Split Conformal Prediction
  * Dvoretzky–Kiefer–Wolfowitz (DKW) non-parametric inequality bounds
  * Adaptive Dynamic Recalibration (ADR) martingale test drift detectors

---

## 2. PRODUCTION ROUTE CATALOG & NETWORK EGRESS INVENTORY

All 22 Next.js application routes compiled in production:

| Route Path | Type | Render Target | Primary Data Source | External Network Egress Calls |
| :--- | :--- | :--- | :--- | :--- |
| `/` | Page (Static) | Executive Surveillance & SLA Dashboard | Unified Zustand Store (`useBankingStore`) | **0** (Pure local hydration) |
| `/triage` | Page (Static) | Virtualized Alert Triage Queue | `generateFullAlertQueue()` (2,028 alerts) | **0** (Client virtualized) |
| `/screening` | Page (Static) | Sanctions, PEP & Interdiction Desk | `INITIAL_SCREENING_RECORDS` | **0** (Local fuzzy matcher) |
| `/customers` | Page (Static) | Customer 360° KYC/EDD Profiles | `INITIAL_CUSTOMERS` | **0** (Local state) |
| `/cases` | Page (Static) | Institutional Cases Docket | `INITIAL_CASES` in Zustand store | **0** (Local state) |
| `/cases/[caseId]` | Page (Dynamic) | Investigation Dossier & Milestones | Selected Case in Zustand store | **0** (Local WebCrypto) |
| `/graph` | Page (Static) | Forensic Cash Flow Topology Studio | Topological preset adjacency graphs | **0** (Client Canvas/SVG) |
| `/tbml` | Page (Static) | Trade Finance TBML Workspace | ASYCUDA / MT700 reconciliation seed | **0** (Client WebCrypto) |
| `/sar` | Page (Static) | SAR Narrative & CTR Batch Studio | goAML / FinCEN / BFIU XML serializer | **0** (Client XML generator) |
| `/rfi` | Page (Static) | Compliance RFI Hub & Anti-Tipping | RFI queue + Anti-Tipping Lexer | **0** (Local text parser) |
| `/rules` | Page (Static) | Champion/Challenger & Sensitivity | Rule sensitivity configuration engine | **0** (Local state) |
| `/governance` | Page (Static) | Model Ops, Drift & WORM Ledger | WORM SHA-256 chain + Recharts | **0** (Local WebCrypto) |
| `/recourse` | Page (Static) | Statutory Non-Tipping-Off Airgap | Static compliance disclosure | **0** (Static HTML) |
| `/_not-found` | Page (Static) | 404 Institutional Error Handler | Static UI fallback | **0** |
| `/api/v1/score` | API (Dynamic) | Transaction Risk Inference | Real-time Scoring Engine | Local / In-process |
| `/api/v1/cases` | API (Dynamic) | Case REST API | Case repository | Local / In-process |
| `/api/v1/cases/[id]/signoff` | API (Dynamic) | 4-Eyes CCO Sign-off Handler | WORM Hash Chain | Local WebCrypto |
| `/api/v1/audit/ledger` | API (Dynamic) | WORM Ledger Dump | Audit Chain | Local WebCrypto |
| `/api/v1/audit/verify` | API (Dynamic) | Chain Integrity Validator | Audit Chain | Local WebCrypto |
| `/api/v1/rfi` | API (Dynamic) | RFI Hub Endpoints | RFI repository | Local / In-process |
| `/api/v1/rfi/upload` | API (Dynamic) | Evidence Ingestion & Hash | File digest engine | Local WebCrypto |
| `/api/v1/models/drift` | API (Dynamic) | Real-time Drift Metrics | Drift Telemetry | Local / In-process |
| `/api/v1/graph/subgraph/[id]` | API (Dynamic) | Forensic Subgraph Extraction | Subgraph cache | Local / In-process |

---

## 3. TECHNICAL MEASUREMENTS & BASELINES (PRE-PHASE 1)

### 3.1 Bundle Size Analysis (`frontend/.next/static`)
* **Total Client Static Bundle Size:** **2,198.74 KB (2.15 MB)**
* **Top 10 Largest Chunks:**
  1. `chunks/1gfnnhjy5ngcl.js`: 440.59 KB (Vendor UI & React runtime)
  2. `chunks/38o18r3scdzc6.js`: 409.83 KB (Recharts, D3 mathematics, SVG primitives)
  3. `chunks/119xlp6nb0542.js`: 223.91 KB (Zustand store & full alert seed queue)
  4. `chunks/06asp5lq9mnm3.js`: 156.44 KB (TanStack Virtual & Table helpers)
  5. `chunks/3p_xlqyqf1dpq.css`: 115.28 KB (Tailwind v4 compiled CSS tokens)
  6. `chunks/0cz1d0mv5g_q7.js`: 109.96 KB (Radix UI interactive wrappers)
  7. `chunks/2-6v0dm6803cd.js`: 87.28 KB (Graph rendering logic)
  8. `media/ba63f6a0e436df8e-s.woff2`: 83.27 KB (Inter font subset)
  9. `chunks/2ainor7_jp02g.js`: 61.24 KB (Compliance & serialization utilities)
  10. `media/07c7676b89ed2778-s.woff2`: 47.30 KB (JetBrains Mono font subset)

### 3.2 Response Headers & Security Posture
Live probe on `https://intelligent-aml.vercel.app`:
* `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload` (Verified)
* `X-Content-Type-Options: nosniff` (Verified)
* `X-Frame-Options: DENY` (Verified)
* `Referrer-Policy: no-referrer` (Verified)
* `Permissions-Policy: camera=(), microphone=(), geolocation=(), browsing-topics=()` (Verified)
* `Content-Security-Policy`:
  `default-src 'self'; script-src 'self' 'unsafe-eval' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob: https:; font-src 'self' data:; connect-src 'self' http://localhost:8000 ws://localhost:8000 https: wss: data: blob:; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none';`

### 3.3 Critical Discrepancy & Contradiction Audit
1. **Banner vs. CSP Contradiction:**
   * **UI Claim:** The header ribbon claimed `"Air-Gap Verified"` and `"0 EXTERNAL EGRESS"`.
   * **Reality:** The Content Security Policy in production allows `connect-src 'self' https: wss: ...` and does not enforce an air-gap boundary unless in an explicit `onprem` mode with verified isolation.
   * **Fix Required:** Add `APP_MODE = demo | onprem`. In `demo` mode, replace with `"Synthetic demo data, not connected to any institution"`. Only in `onprem` mode with `connect-src 'self'` and automated no-egress tests may air-gap claims be made.
2. **"LIVE" State Contradiction:**
   * **UI Claim:** Top navigation and screening queues claimed `"LIVE"`, `"List Sync LIVE (00:04:12 ago)"`.
   * **Reality:** The feed is an in-memory client-side simulated generator, and the screening list timestamp was hardcoded to `2026-09-02`.
   * **Fix Required:** Change labels to `"Simulated Stream"` with dynamic relative timestamps derived from execution time (`Date.now()`).
3. **Account ID Collision Bug:**
   * **Finding:** Account number `BD22-EBLB-4829-1092-8823` was assigned to **both** `Meghna Industrial & Agro Processing Ltd` (Bangladesh) and `Gulf Star Commodities FZE` (Dubai) in screening records.
   * **Fix Required:** Assign unique, validated account identifiers to all counterparties.
4. **Alert Queue Counter Mismatch:**
   * **Finding:** The UI showed `1,280 Tier 1 + 748 Tier 2 = 2,028`, but the total count badge rendered `View All (2,029)` because `INITIAL_ALERTS` contained an uncounted Tier 3 entry.
   * **Fix Required:** Ensure exact mathematical consistency (`alerts.length === 2,028`).
5. **Fictional Persona Consistency:**
   * **Finding:** Mixed real contributor names (`Nazmul Hasan`) and fictional names (`Sarah L. Jenkins, CFE`) without clear demonstration labeling.
   * **Fix Required:** Standardize all demo roles to clearly designated institutional personas (`Amina Rahman (Senior Analyst, Demo)`, `Kazi Tanvir (CCO / MLRO, Demo)`).

---

## 4. HARDCODED METRICS AUDIT & RUN TRACEABILITY MATRIX

Below is the complete inventory of all hardcoded metrics found across the 11 modules and their formal traceability status against actual empirical runs in `/results/metrics/runs/`:

| UI Location | Displayed Metric / Claim | Traceability Status | Verification Source / Run ID | Required Remediation |
| :--- | :--- | :--- | :--- | :--- |
| `app/page.tsx` | 24h Volume: "$4.82B" | **Illustrative** | None (Static presentation) | Label `[Illustrative]` or compute from 24h window |
| `app/page.tsx` | FP Rate: "1.84%" | **Traced** | Run `elliptic_v1_proposed_c_stgb` (FP=0.011) | Map to `METRICS_REGISTRY.fp_rate` |
| `app/page.tsx` | STP Rate: "82.5%" | **Illustrative** | None | Label `[Illustrative]` |
| `app/page.tsx` | "0.12 ms Latency" | **Misleading** | Only raw matrix math, not end-to-end | State "Scorer inference only (excluding network)". Add `/evals/latency` |
| `app/triage/page.tsx` | 2,028 vs 2,029 count | **Computed Bug** | Store discrepancy | Fix seed generator to exactly 2,028 items |
| `app/screening/page.tsx`| "00:04:12 ago" sync | **Fictional** | Hardcoded string | Compute real elapsed time since local sync |
| `app/rules/page.tsx` | "14,820 alerts / mo" | **Illustrative** | None | Trace or label `[Illustrative]` |
| `app/rules/page.tsx` | "88.4% Analyst Fatigue"| **Illustrative** | None | Trace or label `[Illustrative]` |
| `app/rules/page.tsx` | "4,120 alerts (-72.2%)"| **Illustrative** | None | Trace or label `[Illustrative]` |
| `app/governance/page.tsx`| "0.84 ms / 0.62% FP" | **Traced** | `cc_transactions_proposed_c_stgb` | Map to `METRICS_REGISTRY` |
| `features/models/` | Macro F1: "68.05%" | **Traced** | Master 14-dataset benchmark matrix | Map to `METRICS_REGISTRY.macro_f1` |
| `features/models/` | PR-AUC: "0.6974" | **Traced** | Master 14-dataset benchmark matrix | Map to `METRICS_REGISTRY.pr_auc` |

---

## 5. ACCESSIBILITY & PERFORMANCE PRE-FLIGHT AUDIT

* **Color Palette & Contrast:** Institutional dark mode palette utilizes `#0B0F17` (Deep Obsidian background) and `#1E293B` (Border slate). Standard text tokens (`#F8FAFC` and `#94A3B8`) provide high contrast compliant with WCAG AA (&gt; 4.5:1). Critical badge accents (`#EF4444`, `#10B981`, `#F59E0B`) require verified `aria-label` text to ensure color is not the sole indicator of state.
* **Keyboard Navigation:**
  * J / K row navigation in Alert Triage verified.
  * Enter (inspect), G (graph), F (4-Eyes freeze), E (escalate), X (select) shortcuts active.
* **Screen Reader Semantic Hierarchy:**
  * Landmark regions (`<nav>`, `<header>`, `<main>`, `<aside>`) are present.
  * Modal overlays enforce `role="dialog"` and `aria-modal="true"` via Radix UI primitives.

---

## 6. PHASE 1 REMEDIATION PLAN & ARCHITECTURE CONTRACT

1. **Build `frontend/src/lib/metrics/registry.ts`:** Centralized typed registry holding all empirical benchmarks traced to specific run IDs in `results/metrics/runs/` with date, hardware, scope, and evaluation command. All other metrics will be programmatically computed or explicitly annotated as `Illustrative`.
2. **Build `evals/latency.py`:** Standalone benchmarking CLI reporting real hardware-timed p50, p95, and p99 inference latency, distinguishing raw scorer tensor time from end-to-end API roundtrip time.
3. **Build Mode Switch (`APP_MODE`):** Add `APP_MODE = 'demo' | 'onprem'`. Render persistent demonstration disclaimer banner when `APP_MODE !== 'onprem'`. Remove unverified air-gap assertions.
4. **Seed Generator Hardening:** Fix account ID collisions, synchronize total alert count to exactly 2,028, and replace static timestamps with dynamic real-time offsets.
5. **Persona Modernization:** Replace all personal and contributor names with standardized institutional demonstration personas.
