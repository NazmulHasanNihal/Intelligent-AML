# Changelog — Intelligent-AML Enterprise Compliance Platform

All notable changes to this project are documented in this file, adhering to Ground Rules and Phase-by-Phase milestones.

---

## [Phase 3: Real Backend, Data Persistence & Infrastructure] — 2026-11-23

### Added
- **Single Source of Truth Decision**: Python FastAPI + DuckDB/Polars + PyTorch backend is authoritative system of record; Next.js 16 is the single enterprise web frontend.
- **Typed OpenAPI v3.1 Specification Contract**:
  - Exported complete schema to `api/openapi.json` and mirrored in `frontend/src/lib/api/openapi.json` (121.6 KB, 13 operations).
  - Built strongly typed client `frontend/src/lib/api/backendClient.ts` with error handling (`BackendConnectionError` rejecting silent mock fallbacks in `APP_MODE=onprem`).
- **Tiered Scoring Service (`src/scoring/tiered_scorer.py`)**:
  - **Tier 1 (FastPath)**: Microsecond auto-clear for routine sub-$1,000 domestic transactions (< 200 µs).
  - **Tier 2 (Statutory Rules)**: Sub-millisecond BFIU CTR structuring checks (৳800k-৳1M) and ASYCUDA TBML price divergence.
  - **Tier 3 (Online Lightweight Model)**: Precomputed topological flow invariants ($\phi_{flow}, \lambda_u, d_u$) with logistic inference (< 1-2 ms budget).
  - **Tier 4 (Asynchronous GNN Refresh)**: Background queue for spatio-temporal graph neural network re-indexing.
  - **Artifact Versioning & Hashing**: Champ model `cstgb-champion-v3.2` with cryptographic SHA-256 artifact hash stamped on every scoring decision receipt.
- **Conformal Prediction Calibration Registry & Telemetry**:
  - Calibration state persisted to `results/metrics/conformal_calibration.json` with nominal $\alpha=0.01$, calibration size $n=10,000$, empirical coverage $99.04\%$, and nonconformity quantile $\hat{q}=0.8542$.
  - Integrated dedicated **Conformal Calibration & Exchangeability under Temporal Drift** telemetry card in `frontend/src/app/governance/page.tsx`.
- **Relational OLTP & Analytics Infrastructure**:
  - Initialized relational schemas for PostgreSQL 16 and SQLite (`cases`, `alerts`, `audit_ledger`, `rfi_requests`, `users`, `conformal_calibration_audit`) in `deploy/docker/init-postgres.sql` and `src/engine/persistence.py`.
  - Created root `docker-compose.yml` orchestrating PostgreSQL 16, Redpanda v24 (Kafka streaming), FastAPI backend, and Next.js 16 frontend.
  - Created production Helm chart in `deploy/helm/intelligent-aml/` (`Chart.yaml`, `values.yaml`, `configmap.yaml`, `secret.yaml`, `pvc-analytics.yaml`, `deployment-backend.yaml`, `service-backend.yaml`, `deployment-frontend.yaml`, `service-frontend.yaml`, `ingress.yaml`).
- **Automated API Contract Test Suites**:
  - Python FastAPI contract test in `tests/test_api_contract.py` (6 tests passing).
  - Frontend Vitest contract test in `frontend/src/__tests__/apiContract.test.ts` (4 tests passing, 25 total suite passing).

---

## [Phase 2: Bangladesh Compliance Fit] — 2026-11-23

### Added
- **Centralized Versioned Regulatory Configuration (`frontend/src/lib/config/regulatory.ts`)**:
  - **CTR Threshold Policy**: Mandatory ৳1,000,000 BDT ceiling (effective 2012-02-20, MLPA 2012 § 2(z), BFIU Master Circular No. 26 § 4.2), with official source link to Bangladesh Bank.
  - **Structuring Band**: ৳800,000 to ৳999,999 BDT detection band under BFIU Master Circular No. 26 § 4.3.
  - **Exchange Rate Policy**: 120.00 BDT/USD dated 2026-11-20 (Bangladesh Bank Interbank Weighted Average Reference Rate).
  - **Statute References**: Primary citation of Money Laundering Prevention Act, 2012 (Act No. V of 2012) §§ 2(z), 4, 8, 25, 27 with official Ministry of Law gazette link.
  - **December 2025 Amendment**: Explicitly flagged with `TODO(verify: Money Laundering Prevention (Amendment) Ordinance announced Dec 2025 by Interim Government / BFIU)`.
  - **Configurable Policies**:
    - **Record Retention Policy**: 5 years under MLPA 2012 § 8 with `TODO(verify: 2025 amendment proposed extension)`.
    - **Data Residency Policy**: Sovereign in-country primary storage mandate under Bangladesh Bank Guidelines on ICT Security for Scheduled Banks (v3.0, May 2020) § 6.2 with `TODO(verify: Cloud DR circular)`.
    - **PII & Secrecy Policy**: Banking Companies Act 1991 § 46 with `TODO(verify: Draft Data Protection Act)`.
    - **EU GDPR Research Prototype Notes**: Documented for ETH Zurich evaluation under GDPR Articles 6(1)(c), 9(2)(g), 32 (pseudonymization & WORM SHA-256), and 89 (scientific research safeguards).
  - **BFIU Guidance Mapping Matrix (`BFIU_GUIDANCE_MAPPING`)**: 7-point compliance matrix linking app modules to MLPA 2012, BFIU Master Circular 26, BFIU TBML Guidelines (2019), ATA 2009, BB ICT Security Guidelines v3.0, and Aligned Model Risk Practice.

### Changed
- **BFIU STR/SAR & CTR Workbench (`frontend/src/app/sar/page.tsx`)**:
  - Adopted strict BFIU terminology (`STR/SAR`, `CTR`).
  - Implemented official BFIU UNODC goAML v4.2 XML schema export.
  - Enforced mandatory **Supporting Documentary Attachments Gate** (minimum 1 document with SHA-256 seal required before export/transmission).
  - Enforced **Maker-Checker Workflow** (Maker investigator signs, Checker CCO approves).
  - Pinned non-dismissible **Anti-Tipping-Off Warning Banner** citing MLPA 2012 § 27 with official gazette link.
  - Implemented structured **Decision Log** with typology reason codes and cryptographic seals.
- **Model Governance (`frontend/src/app/governance/page.tsx`)**:
  - Relabeled Federal Reserve SR 11-7 / OCC 2011-12 as *"aligned with model-risk practice"* rather than binding US jurisdiction.
  - Removed all SEC 17a-4 and FINRA 4511 broker-dealer claims; replaced with **Bangladesh Evidence Act (Amended 2022) § 65B** and **Bangladesh Bank ICT Security Guidelines v3.0**.
  - Added interactive **BFIU Guidance Mapping Matrix** tab.
  - Added **Retention, Data Residency & GDPR Policies** tab.
- **Trade Finance TBML (`frontend/src/app/tbml/page.tsx`)**:
  - Linked ASYCUDA World price divergence radar to official **BFIU Guidelines for Prevention of Trade Based Money Laundering (2019)**.

---

## [Phase 1: Honesty and Consistency] — 2026-11-23

### Added
- **Build Mode Architecture (`frontend/src/lib/config/env.ts`)**: `APP_MODE = 'demo' | 'onprem'`.
- **Persistent Disclaimer Banner (`frontend/src/components/shell/DemoDisclaimerBanner.tsx`)**: Prominently displays "DEMONSTRATION PROTOTYPE: Synthetic demo data, not connected to any institution" in demo mode.
- **Institutional Metrics Registry (`frontend/src/lib/metrics/registry.ts`)**: Single source of truth for all quantitative claims (`MACRO_F1`, `PR_AUC`, `CALIBRATED_FP_RATE`, latencies), mapping to empirical run IDs in `/results/metrics/runs/` or labeling as `[Illustrative]`.
- **Standalone Latency Benchmark (`evals/latency.py`)**: Times warm vs cold, p50/p95/p99 across batches, explicitly separating raw tensor scorer math (~0.022 ms) from in-process ingestion (~0.037 ms) and HTTP roundtrips (~14.8 ms).
- **System Pre-Flight Audit (`AUDIT.md`)**: Full inventory of routes, data sources, bundle sizes, and HTTP response security headers.

### Changed
- Replaced unverified "Air-Gap Verified Intranet Node" and "0 EXTERNAL EGRESS" with conditional labels based on `APP_MODE`.
- Replaced static "LIVE" stream labels with dynamic "SIMULATED STREAM".
- Replaced real researcher names and fictional "Sarah L. Jenkins" with consistent fictional banking personas:
  - Lead Investigator (Maker): `Amina Rahman, CFE (Demo Lead Investigator)`
  - Chief Compliance Officer (Checker): `Kazi Rafiqul Islam, CAMS (Demo CCO)`
  - Triage Analyst: `Tanvir Ahmed (Demo Triage Analyst)`
  - Model Validator: `Dr. S. K. Haque, FRM (Demo Model Validator)`
- Fixed account collision: `BD22-EBLB-4829-1092-8823` reserved exclusively for Meghna Industrial.
- Fixed alert queue count: Aligned to exactly 2,028 alerts (1,280 Tier 1 + 748 Tier 2).
