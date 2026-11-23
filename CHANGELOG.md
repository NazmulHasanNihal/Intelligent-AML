# Changelog — Intelligent-AML Enterprise Compliance Platform

All notable changes to this project are documented in this file, adhering to Ground Rules and Phase-by-Phase milestones.

---

## [Phase 6: Screening Fidelity & Multi-Algorithm Entity Resolution] — 2026-11-23

### Added
- **Official Watchlist Ingestion Feeds (`src/screening/watchlist_registry.py` & `frontend/src/lib/screening/watchlistRegistry.ts`)**:
  - Registered official metadata for 5 key regulatory watchlists:
    - **OFAC SDN** (`2026.11.20-SDN-v48`, US Treasury, 14,820 records)
    - **UN Consolidated Sanctions** (`2026-Q4-UN-REV-119`, UNSC, 1,124 records)
    - **EU Consolidated Sanctions** (`EU-FSF-2026-11-19`, EEAS, 3,410 records)
    - **UK HM Treasury / OFSI** (`OFSI-UK-2026.47`, HM Treasury, 4,289 records)
    - **Bangladesh BFIU Domestic List** (`BFIU-DOM-2026-V3`, BFIU & ATA 2009 Schedules 1 & 2, 48 records)
  - Pinned version tags, SHA-256 cryptographic hashes, fetch timestamps, published source URLs, and `SYNCED_VERIFIED` status displayed in live UI.
- **Enterprise Normalization Pipeline (`src/screening/normalizer.py` & `frontend/src/lib/screening/normalizer.ts`)**:
  - Unicode NFKD decomposition and diacritic stripping (`Müller` -> `Muller`, `François` -> `Francois`, `Łódź` -> `Lodz`).
  - Case folding and punctuation harmonization.
  - Multi-jurisdiction corporate legal suffix stripping (`LLC`, `FZE`, `Ltd`, `Limited`, `AG`, `GmbH`, `Corp`, `Inc`, `PLC`, `Pte Ltd`, `SA`, `BV`, etc.).
  - Name-order permutations (order-invariant token sets, `Last, First` <-> `First Last`).
  - Bangla-to-Latin transliteration canonicalization (`Mohammed` <-> `Md.`, `Sheikh` <-> `Seikh`, `Rahman` <-> `Rohman`, `Chowdhury` <-> `Choudhury`, `Hossain` <-> `Hussain`).
- **Multi-Algorithm Matcher with Corroboration (`src/screening/matcher.py` & `frontend/src/lib/screening/matcher.ts`)**:
  - **Jaro-Winkler Similarity** (character prefix-weighted distance, weight 40%).
  - **Token-Set Ratio** (word-order invariant set intersection/union, weight 40%).
  - **Phonetic Soundex Encoding** (phonetic equivalence, weight 20%).
  - **Attribute Corroboration**:
    - Date of Birth (DOB): Exact match $+10.0\%$, mismatch penalty $-15.0\%$.
    - Jurisdiction / Domicile: Match $+5.0\%$.
    - Official Identifier (Passport, NID, TIN): Match $+25.0\%$.
  - Operational triage disposition:
    - $\ge 85.0\% \rightarrow$ `CONFIRMED_TRUE_HIT`
    - $\ge 65.0\% \rightarrow$ `PENDING_REVIEW` (Interdicted)
    - $< 65.0\% \rightarrow$ `DISMISSED_FALSE_POSITIVE`
- **FastAPI & Next.js Endpoints**:
  - `GET /api/v1/screening/lists`: Returns all 5 official feeds with cryptographic hashes and versions.
  - `POST /api/v1/screening/score`: Multi-algorithm pair score decomposition.
  - `POST /api/v1/screening/search`: Full-text candidate search across all official lists.
- **Enhanced Screening UI (`frontend/src/app/screening/page.tsx`)**:
  - Official Feeds Registry status card with version, SHA-256 hash, and direct source links.
  - Configurable scoring weights and statutory thresholds slider drawer.
  - Ad-hoc screening with optional DOB and Identifier corroboration inputs.
  - Match Forensics Panel with live per-algorithm decomposition (Jaro-Winkler, Token-Set, Phonetic, Corroboration Adjustment) and linguistic token diffs.
- **Labeled Benchmark & Evaluation Suite (`/evals`)**:
  - Curated 34 labeled ground-truth pairs across all 5 lists (`evals/data/screening_labeled_test_set.json`).
  - Evaluation harness `evals/screening_eval.py` computing Precision, Recall, F1-score, and confusion matrices per list.
  - Generated `evals/SCREENING_EVAL_REPORT.md` (90.9% Recall, 81.6% F1, 0.659 ms p50 latency).
- **Automated Verification Suites**:
  - Backend: `tests/test_screening_engine.py` (10 passing tests; 29/29 total backend tests passing).
  - Frontend: `frontend/src/__tests__/screeningFidelity.test.ts` (10 passing tests; 47/47 total frontend tests passing).
  - Build: All 26 Next.js routes compiled with 0 errors.
  - **Acceptance Verified**: Demo candidate match score mathematically equals what the engine computes.

---

## [Phase 5: Tamper-Evident Audit Log & Storage WORM] — 2026-11-23

### Added
- **Tamper-Evident Append-Only Hash Chain**:
  - SHA-256 sequential Merkle hash chaining across all audit events in Python engine (`src/engine/persistence.py`) and Next.js frontend (`frontend/src/lib/audit/hashChain.ts`).
  - RFC 8785 Canonical JSON payload serialization (`json.dumps(..., sort_keys=True, separators=(',', ':'), ensure_ascii=True)`), ensuring cross-platform, deterministic payload recalculation without whitespace jitter.
  - Pointer continuity check: Enforces `block[i].prev_hash == block[i-1].curr_hash`.
  - Content integrity check: Recomputes SHA-256 over canonical payload for all blocks including Genesis block #0.
- **RFC 8032 Ed25519 Asymmetric Periodic Checkpointing (`src/engine/audit_checkpointer.py`)**:
  - Binary Merkle tree root calculation over batch block digests.
  - Ed25519 signing keypair generation and asymmetric signature generation over `(checkpoint_id, start_index, end_index, root_hash, head_hash, merkle_root, timestamp)`.
  - Automatic milestone checkpoint creation every 3 blocks with local vault backup to `results/audit_checkpoints/`.
- **Object-Lock Bucket Anchoring & Storage-Level WORM Documentation**:
  - Created `docs/security/OBJECT_LOCK_STORAGE_WORM.md` establishing the formal distinction between application-level tamper evidence and storage-level WORM.
  - Documented AWS S3 Object Lock configuration in `COMPLIANCE` mode with 5-year immutable retention (`1825d`) per Bangladesh MLPA 2012 § 25 and FRE 902(11) certified electronic records.
  - Documented MinIO Object Lock configuration for air-gapped on-premises banking deployments.
- **Verification Endpoints & Interactive UI**:
  - `GET /api/v1/audit/verify` and `POST /api/v1/audit/verify` returning cryptographic verification receipts with `firstBrokenRow`, `status: "TAMPER_EVIDENT_VERIFIED" | "TAMPER_DETECTED"`, and `anchored_object_lock_uri`.
  - Governance UI (`frontend/src/app/governance/page.tsx`):
    - Relabeled to "Tamper-Evident Audit Ledger (Ed25519 Signed)".
    - "Verify Cryptographic Chain" button verifying SHA-256 and Ed25519 signatures in real time.
    - "Simulate Auditor Tamper Test": Alters block payload in-memory $\rightarrow$ UI immediately detects and displays red alert: `TAMPER DETECTED: Row #0 (Block #1) Hash Mismatch!`.
    - "Restore Chain Integrity": Restores pristine certified genesis chain with green verification confirmation.
- **Automated Verification Test Suites**:
  - Backend: `tests/test_audit_ledger.py` (5 passing tests validating pristine verification, payload tampering detection, pointer tampering detection, genesis tampering detection, and Ed25519 signature rejection on forgery).
  - Frontend: `frontend/src/__tests__/auditLedger.test.ts` (5 passing Vitest tests; 37/37 total frontend tests passing).

---

## [Phase 4: Security, RBAC & Hardening] — 2026-11-23

### Added
- **OIDC SSO with Multi-Factor Authentication (MFA)**:
  - 6 Standard Institutional Roles: `Analyst L1`, `Analyst L2`, `Supervisor`, `MLRO/CAMLCO`, `Auditor` (read-only), and `Admin`.
  - JWT Bearer tokens with signed `mfa_verified: true`, `auth_method: "OIDC_SSO_MFA"`, and strict 15-minute inactivity session timeout (`ACCESS_TOKEN_EXPIRE_MINUTES = 15`).
- **Server-Side RBAC & Maker-Checker Separation (`src/engine/auth.py` & `src/engine/api.py`)**:
  - Enforced `enforce_maker_checker()` on all sign-off endpoints (`/api/v1/cases/{case_id}/sign-off`).
  - Proved server-side that `Analyst L1` and `Analyst L2` cannot sign off on case dockets (HTTP 403 Forbidden).
  - Proved that `Auditor` is mathematically read-only and cannot mutate state or approve cases (HTTP 403 Forbidden).
  - Enforced strict Maker != Checker identity collision check: Case initiator cannot ratify their own case even if they hold Supervisor role.
- **Server-Side PII Masking & Audited Reveal Gate**:
  - Implemented `POST /api/v1/pii/reveal` in FastAPI and Next.js BFF (`frontend/src/app/api/pii/reveal/route.ts`).
  - Enforced role clearance: `Analyst L1` and `Auditor` are forbidden from unmasking customer PII (HTTP 403 Forbidden).
  - Enforced mandatory operational justification ($\ge 10$ characters; rejected with HTTP 422 if insufficient).
  - Enforced sliding-window rate limiting (maximum 5 reveals per 10-minute window per officer; HTTP 429).
  - Every reveal writes an immutable cryptographically sealed audit block to the WORM ledger and returns a 60-second validity receipt.
- **HTTP Security Headers (Target: A on securityheaders.com)**:
  - Hardened `frontend/next.config.ts`:
    - `Content-Security-Policy`: `default-src 'self'`, `frame-ancestors 'none'`, `object-src 'none'`, `base-uri 'self'`, `form-action 'self'`, `upgrade-insecure-requests`.
    - `Strict-Transport-Security`: `max-age=63072000; includeSubDomains; preload` (2 years).
    - `X-Content-Type-Options`: `nosniff`.
    - `X-Frame-Options`: `DENY`.
    - `Referrer-Policy`: `strict-origin-when-cross-origin`.
    - `Permissions-Policy`: `camera=(), microphone=(), geolocation=(), browsing-topics=(), payment=(), usb=(), accelerometer=(), gyroscope=()`.
    - `Cross-Origin-Opener-Policy`: `same-origin`.
    - `Cross-Origin-Resource-Policy`: `same-origin`.
    - `X-DNS-Prefetch-Control`: `off`.
    - `X-Permitted-Cross-Domain-Policies`: `none`.
- **Zod Schema Boundary Validation (`frontend/src/lib/validation/schemas.ts`)**:
  - Schemas for `PiiRevealSchema`, `CaseSignoffSchema`, `TransactionScoreSchema`, `CreateCaseSchema`, and `SessionCookieConfig` (15-min timeout with `HttpOnly`, `Secure`, `SameSite=Strict`).
- **Supply Chain, SBOM, CodeQL & Vulnerability Management**:
  - Created RFC 9116 compliant security disclosure policy in `frontend/public/.well-known/security.txt` and `public/.well-known/security.txt`.
  - Authored comprehensive STRIDE Threat Model targeting OWASP ASVS Level 2 in `docs/security/STRIDE_THREAT_MODEL.md`.
  - Added CI security workflow in `.github/workflows/security.yml` executing CodeQL static analysis, `npm audit`, `pip-audit`, CycloneDX SBOM generation, and TruffleHog secret scanning.
- **Automated Security Verification Test Suites**:
  - `tests/test_rbac_security.py` (8 Python tests passing).
  - `frontend/src/__tests__/roleMatrixSecurity.test.ts` (7 Vitest tests passing, 32 total passing).

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
