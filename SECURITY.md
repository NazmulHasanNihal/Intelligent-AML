# Security Policy: Intelligent-AML

## 1. Security & Vulnerability Disclosure

Intelligent-AML takes software and data security with the utmost rigor expected of Tier-1 banking compliance infrastructure. If you discover a potential security vulnerability within this repository, we appreciate your responsible disclosure.

* **Reporting Email:** `security@intelligent-aml.internal` (PGP key fingerprint: `9B42 81E3 A270 D5F1 C834 7690 EF12 4A39 BD10 9801`)
* **RFC 9116 Metadata:** [frontend/public/.well-known/security.txt](file:///c:/Users/SAAD/Documents/GitHub/Intelligent-AML/frontend/public/.well-known/security.txt)
* **Response SLA:** Acknowledgment within 24 hours; initial severity triage and mitigation roadmap within 72 hours.
* **Responsible Disclosure:** We request that security researchers refrain from public disclosure until a patched release is published.

---

## 2. OWASP ASVS Level 2 Verification Matrix

Intelligent-AML implements technical controls aligned with the **OWASP Application Security Verification Standard (ASVS) v4.0.3 (Level 2: Standard Applications)**:

| ASVS Domain | Control Implementation in Intelligent-AML | Verification Evidence |
| :--- | :--- | :--- |
| **V1: Architecture** | Multi-tier defense-in-depth: Isolated frontend App router (`frontend/`), FastAPI backend (`src/`), synchronous WORM audit ledger, and air-gapped ML scoring pipeline. | `AUDIT.md`, `docker-compose.prod.yml` |
| **V2: Authentication** | OIDC SSO with Multi-Factor Authentication (MFA), RS256 JWT signature verification, cryptographically secure session cookies (`SameSite=Strict`, `Secure`, `HttpOnly`). | `src/engine/rbac.py`, `tests/test_rbac_security.py` |
| **V3: Session Management** | 15-minute inactivity timeouts, automatic session invalidation on logout, token revocation lists, stateful token replay prevention. | `frontend/src/lib/auth/rbac.ts` |
| **V4: Access Control** | **6-Tier Role-Based Access Control (RBAC)** strictly enforced on the **SERVER**, never client-only. Four-eyes / maker-checker enforcement preventing single-analyst SAR submissions. | `src/engine/rbac.py`, `tests/test_rbac_security.py` |
| **V5: Malicious Input** | Strict Zod validation schemas across every Next.js API input; Pydantic v2 schemas across FastAPI; SQL injection immunity via parameterized queries and ORM abstractions. | `frontend/src/lib/compliance/`, `api/v1/cases.py` |
| **V6: Cryptography** | Ed25519 digital signatures for WORM ledger checkpoints; SHA-256 hash chaining; AES-256-GCM envelope encryption for data at rest; TLS 1.3 in transit. | `src/audit/tamper_evident_ledger.py`, `tests/test_audit_ledger.py` |
| **V7: Error Handling & Logging** | Structured JSON logging with `PiiRedactionFilter` regex masking account numbers, NIDs, debit cards, and emails. Zero stack traces or PII leaked to clients. | `src/engine/logging_config.py`, `src/engine/telemetry.py` |
| **V8: Data Protection** | Strict server-side PII masking. "Reveal PII" action requires mandatory justification, enforces rate-limiting (max 5/min), and writes non-repudiable audit events. | `frontend/src/app/customers/page.tsx`, `src/engine/rbac.py` |
| **V14: Configuration** | Hardened HTTP response headers: Strict Content Security Policy (`connect-src 'self'`), HSTS 2-year preload, `X-Content-Type-Options: nosniff`, `frame-ancestors 'none'`. | `frontend/next.config.ts`, `AUDIT.md` |

---

## 3. Role-Based Access Control (RBAC) Server Enforcement

The platform enforces 6 distinct operational roles:

| Role Name | Identifier | Permissions & Capabilities | Server Gate Implementation |
| :--- | :--- | :--- | :--- |
| **Analyst L1** | `ANALYST_L1` | View alerts, review screening hits, prepare initial case drafts, submit RFI requests. *Cannot sign off cases, approve SARs, or reveal PII.* | `src/engine/rbac.py` |
| **Analyst L2** | `ANALYST_L2` | Deep forensic triage, update transaction topology, author SAR narratives, recommend actions. | `src/engine/rbac.py` |
| **Supervisor** | `SUPERVISOR` | Maker-checker review, assign cases, initiate RFI escalations, approve standard escalations. | `src/engine/rbac.py` |
| **MLRO / CAMLCO** | `MLRO_CAMLCO` | Final four-eyes SAR sign-off, direct goAML submission to BFIU, freeze asset orders, manage AML policies. | `src/engine/rbac.py` |
| **Auditor** | `AUDITOR` | Read-only inspection across all modules, export tamper-evident audit logs, execute `verify_chain()`. *Zero mutation access.* | `src/engine/rbac.py` |
| **System Admin** | `ADMIN` | Manage user credentials, configure node environments, inspect telemetry, monitor DR restore drills. | `src/engine/rbac.py` |

---

## 4. Cryptographic Key Management & WORM Integrity

1. **Ed25519 Digital Checkpoint Signatures:**
   - WORM ledger blocks are sealed with Ed25519 cryptographic keypairs.
   - Private keys are injected at runtime via environment variables or Cloud HSM secrets.
   - Public keys are published in `results/audit_checkpoints/` for independent public auditability.
2. **Object Lock Storage Architecture:**
   - Detailed specification: [docs/security/OBJECT_LOCK_STORAGE_WORM.md](file:///c:/Users/SAAD/Documents/GitHub/Intelligent-AML/docs/security/OBJECT_LOCK_STORAGE_WORM.md)
   - S3-compatible compliance mode enforces retention for 6 years in accordance with AMLA 2012 Sec 8.
3. **STRIDE Threat Model:**
   - Full adversarial threat modeling and mitigation catalog: [docs/security/STRIDE_THREAT_MODEL.md](file:///c:/Users/SAAD/Documents/GitHub/Intelligent-AML/docs/security/STRIDE_THREAT_MODEL.md)

---

## 5. Security Scanning in CI/CD

Every pull request and release build runs:
* `pip-audit --desc` (Python dependency vulnerabilities).
* `npm audit --audit-level=high` (Node.js dependency vulnerabilities).
* `ruff check` (Static code security and bug analysis).
* Automated RBAC security matrix test: `tests/test_rbac_security.py`.
