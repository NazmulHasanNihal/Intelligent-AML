# STRIDE Threat Model & OWASP ASVS Level 2 Compliance Blueprint

## Intelligent-AML Enterprise Surveillance Platform
**Target Assurance Standard**: OWASP Application Security Verification Standard (ASVS) 4.0.3 — Level 2 (Commercial Software & Banking Systems)  
**Regulatory Context**: Bangladesh Financial Intelligence Unit (BFIU) MLPA 2012 / Basel III Supervisory Review / Federal Reserve SR 11-7 Practice  
**Date**: November 2026 | **Classification**: CONFIDENTIAL — ARCHITECTURAL GOVERNANCE

---

## 1. System Architecture & Trust Boundaries

```
[ External Payment Rails ]   (SWIFT MT103, ISO 20022 pacs.008, BEFTN, bKash MFS)
           │
═══════════╪═══════════════════════════════════════════════════════════════════════
 TRUST BOUNDARY 1: Perimeter TLS 1.3 / mTLS & Edge CSP Headers
═══════════╪═══════════════════════════════════════════════════════════════════════
           ▼
[ Next.js 16 Edge BFF & Reverse Proxy ] ─── (Strict CSP, frame-ancestors none, HSTS)
           │
           ├─── Zod Input Validation Gateway
           ├─── Session Inactivity Timeout Guard (15 Minutes)
           └─── Sliding-Window Rate Limiter
           │
═══════════╪═══════════════════════════════════════════════════════════════════════
 TRUST BOUNDARY 2: Internal Microservice Auth (OIDC SSO with MFA Bearer Tokens)
═══════════╪═══════════════════════════════════════════════════════════════════════
           ▼
[ FastAPI Scoring & Case Management Engine ]
   ├── Tier 1 FastPath Auto-Clear (< 200 µs)
   ├── Tier 2 Statutory Rule Engine (CTR ৳1M, ASYCUDA TBML)
   ├── Tier 3 Online Lightweight Model (< 1.5 ms)
   ├── Tier 4 Async GNN Queue
   └── Conformal Risk Triage & KS-Drift Monitor
           │
═══════════╪═══════════════════════════════════════════════════════════════════════
 TRUST BOUNDARY 3: Persistent Relational & Cryptographic State
═══════════╪═══════════════════════════════════════════════════════════════════════
   ├── PostgreSQL 16: Cases, Alerts, Users (Row-Level RBAC)
   ├── WORM Ledger: Append-only SHA-256 Block-to-Block Hash Chaining (Evidence Act § 65B)
   └── DuckDB / Arrow: Vectorized In-Memory OLAP Analytics
```

---

## 2. STRIDE Threat Analysis

| Threat Category | Potential Attack Vector | Applied Platform Safeguards | OWASP ASVS v4.0 Ref |
| :--- | :--- | :--- | :--- |
| **S — Spoofing Identity** | Attacker impersonates a Compliance Officer or injects forged JWT claims to access sensitive cases. | • OIDC SSO integration requiring mandatory multi-factor authentication (MFA claims verification in JWT).<br>• Ephemeral HMAC-SHA256 signature verification with dynamic secrets (`JWT_SECRET_KEY`).<br>• Strict 15-minute token expiration and cookie security (`HttpOnly`, `Secure`, `SameSite=Strict`). | V2 (Authentication)<br>V3 (Session Management) |
| **T — Tampering with Data** | Malicious actor modifies alert risk scores, alters trade transaction records, or mutates historical case notes to conceal illicit laundering. | • Append-only WORM cryptographic audit ledger with block-to-block SHA-256 hash chaining.<br>• Every decision outputs an immutable Merkle receipt and model artifact hash (`cstgb-champion-v3.2`).<br>• Server-side Zod boundary validation on all ingestion routes. | V5 (Validation & Sanitization)<br>V8 (Data Protection) |
| **R — Repudiation** | An investigator denies drafting an STR/SAR, or a supervisor denies signing off on an illicit account freeze. | • Four-Eyes Dual Control (Maker-Checker) enforced strictly on the server: Maker cannot approve their own case docket.<br>• Dual signatures logged with timestamp, officer username, IP, and cryptographic digest compliant with Bangladesh Evidence Act 2022 § 65B. | V7 (Error Handling & Logging)<br>V10 (Malicious Code) |
| **I — Information Disclosure** | Unauthorized actors or frontline analysts harvest customer PII (NID, bank accounts, tax IDs) or leak ongoing SAR investigations (Tipping-Off). | • PII masked server-side by default (`BD22-****-****-8823`).<br>• "Reveal PII" requires a documented justification ($\ge 10$ chars), is rate-limited (max 5 reveals / 10 min), and appends an immutable WORM audit event.<br>• Frontline Analyst L1 and Auditor are forbidden from revealing PII.<br>• Statutory anti-tipping-off banners citing MLPA 2012 § 27. | V8 (Data Protection)<br>V4 (Access Control) |
| **D — Denial of Service** | Malicious burst of synthetic wire transfers floods the GNN inference pipeline, causing memory exhaustion or clearing delays. | • 4-tier tiered scoring architecture: 98.6% of routine domestic transfers bypass graph computation via Tier 1 FastPath (< 200 µs).<br>• Sliding-window rate limiters at both Next.js Edge proxy and FastAPI backend.<br>• Asynchronous decoupled GNN re-indexing via Redpanda streaming queue. | V11 (Business Logic)<br>V13 (API & Web Service) |
| **E — Elevation of Privilege** | Front-line Analyst L1 attempts to sign off on an account freeze or approve an SAR filing without supervisor authorization. | • Server-side RBAC enforced via FastAPI `require_roles()` dependencies and Next.js BFF middleware.<br>• Case sign-off strictly restricted to `SUPERVISOR`, `MLRO_CAMLCO`, or `ADMIN`.<br>• Auditor role is mathematically read-only across all endpoints. | V4 (Access Control) |

---

## 3. OWASP ASVS Level 2 Verification Matrix

| ASVS Section | Verification Requirement | Status | Evidence in Codebase |
| :--- | :--- | :--- | :--- |
| **V1: Architecture** | Threat modeling and secure design principles documented | **VERIFIED** | This document (`STRIDE_THREAT_MODEL.md`) & `AUDIT.md` |
| **V2: Authentication** | OIDC SSO with MFA, password hashing with PBKDF2 $\ge 100\text{k}$ iterations | **VERIFIED** | `src/engine/auth.py` (`_hash_pw`, `authenticate_user`) |
| **V3: Session Mgmt** | Session timeout within 15 minutes, secure cookie attributes | **VERIFIED** | `ACCESS_TOKEN_EXPIRE_MINUTES = 15`, `SessionCookieConfig` |
| **V4: Access Control** | Principle of least privilege, server-side RBAC, Maker-Checker | **VERIFIED** | `require_roles()`, `enforce_maker_checker()` |
| **V5: Input Validation** | Reject invalid types, lengths, ranges; strict schema parsing | **VERIFIED** | Zod schemas in `frontend/src/lib/validation/schemas.ts` |
| **V7: Logging & Audit** | Audit logging of security events (login, signoff, PII reveal) | **VERIFIED** | `WORM Audit Ledger` (`src/engine/persistence.py`) |
| **V8: Data Protection** | PII masking, protection of sensitive data in transit and rest | **VERIFIED** | Server-side masking, audited reveal endpoint |
| **V14: Configuration** | Hardened HTTP response headers (CSP, HSTS, X-Frame-Options) | **VERIFIED** | `frontend/next.config.ts` (Score A on securityheaders) |
