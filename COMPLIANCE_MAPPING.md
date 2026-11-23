# Intelligent-AML: Statutory & Regulatory Compliance Mapping Matrix

**Classification:** Institutional Regulatory Architecture  
**Primary Jurisdiction:** People's Republic of Bangladesh (Bangladesh Financial Intelligence Unit - BFIU / Bangladesh Bank)  
**Secondary Reference:** Financial Action Task Force (FATF Recommendations) & European Union GDPR (for Academic/Research Deployment)  
**Effective Date:** November 2026  

---

### 1. Bangladesh Statutory Compliance Framework

The Intelligent-AML platform is explicitly engineered to fulfill statutory obligations under the **Money Laundering Prevention Act, 2012 (Act No. V of 2012)**, the **Anti-Terrorism Act, 2009 (Act No. XVI of 2009)**, and governing circulars issued by the Bangladesh Financial Intelligence Unit (BFIU):

| Module Name | Statutory / Regulatory Mandate | Specific Legal Citation | Intelligent-AML Technical Implementation |
| :--- | :--- | :--- | :--- |
| **Executive Surveillance (`/app`)** | Institutional AML Governance & Daily Oversight | BFIU Master Circular 26 (Sec 2.1, 2.4) | Aggregates daily transaction velocity, CTR volume, pending STR/SAR dossiers, and high-risk counterparty exposure in real time. |
| **Alert Triage (`/triage`)** | Automated Alert Generation & Structuring Detection | MLPA 2012 Sec 2(v); BFIU MC 26 Sec 7 | Virtualized queue processing 2,028 alerts with deterministic rule tagging, including the **৳800,000–৳999,999 Structuring Band** beneath the ৳1M CTR threshold. |
| **Sanctions & PEP (`/screening`)** | Mandatory Targeted Financial Sanctions (TFS) & UNSCR 1267/1373 Screening | Anti-Terrorism Act 2009 Sec 15, 16; BFIU MC 26 Sec 5.2 | Multi-algorithm fuzzy matching (Jaro-Winkler + Token-Set + Metaphone phonetic + DOB/NID corroboration) against UN Consolidated, OFAC SDN, EU, UK HMT, and Bangladesh Domestic Sanctions lists. |
| **Customer 360° (`/customers`)** | Customer Due Diligence (CDD), Enhanced Due Diligence (EDD) & Beneficial Ownership | MLPA 2012 Sec 25(1)(a); BFIU MC 26 Sec 3 | Complete KYC dossiers, risk tiering (Low/Medium/High/PEP), Ultimate Beneficial Owner (UBO) unwrapping, server-masked PII, and audited reveal tracking. |
| **Case Docket (`/cases`)** | Structured Financial Crime Investigation & Record Keeping | MLPA 2012 Sec 8(1); BFIU MC 26 Sec 8 | Multi-stage investigation workflow with evidence attachment manifests, investigator notes, decision logs, and BFIU-compliant print dossiers (with Section 65B Evidence Act certificates). |
| **Forensic Cash Flow (`/graph`)** | Complex Layering & Multi-Hop Network Detection | MLPA 2012 Sec 2(v)(i); FATF Rec 10 | Interactive topological graph analysis highlighting pass-through entities, circular transaction loops, fan-in/fan-out structuring, and progressive node disclosure. |
| **Trade Finance TBML (`/tbml`)** | Trade-Based Money Laundering Detection & Over/Under Invoicing | BFIU Guidelines for Prevention of TBML (2019, Sec 3-5) | Cross-references commercial invoices, bills of lading, and letters of credit (MT700) against ASYCUDA unit prices and dual-use goods catalogs with &plusmn;20% price divergence alerts. |
| **SAR & CTR Studio (`/sar`)** | Statutory Cash Transaction Reporting (CTR) & Suspicious Transaction Reporting (STR) | MLPA 2012 Sec 25(1)(c); BFIU MC 26 Sec 6.1, 6.2 | Automated CTR batching for all cash transactions &ge; ৳1,000,000. Full BFIU goAML XML schema serializer with 4-eyes / maker-checker sign-off and tipping-off warnings. |
| **Compliance RFI Hub (`/rfi`)** | Anti-Tipping-Off Safeguards & Customer Inquiries | MLPA 2012 Sec 6(1) (Penalty for Tipping-Off) | Strict anti-tipping-off lexer blocking sensitive AML terminology in customer-facing inquiries; client-side SHA-256 evidence attachment digest hashing. |
| **Rule Studio (`/rules`)** | Rule Optimization, Champion/Challenger & Sensitivity | BFIU MC 26 Sec 7.4 (Threshold Tuning) | Transparent rule parameter tuning with live false-positive impact simulation, sensitivity sliders, and historical replay. |
| **Model Ops & WORM (`/governance`)** | Model Governance, Drift Telemetry & Tamper-Evident Record Retention | MLPA 2012 Sec 8(2) (6-Year Retention); BB ICT Guidelines v3.0 | Population Stability Index (PSI) drift monitoring, Conformal Risk Control calibration curves, and append-only cryptographic WORM ledger with Ed25519 checkpoint validation. |

---

### 2. Specific Regulatory Constants & Policies

All regulatory thresholds in Intelligent-AML are parameterized in [frontend/src/lib/compliance/regulatoryConfig.ts](file:///c:/Users/SAAD/Documents/GitHub/Intelligent-AML/frontend/src/lib/compliance/regulatoryConfig.ts) and verified via unit tests:

```typescript
export const REGULATORY_CONFIG = {
  jurisdiction: 'BD',
  regulator: 'BFIU (Bangladesh Financial Intelligence Unit)',
  primaryStatute: 'Money Laundering Prevention Act, 2012 (Act No. V of 2012)',
  amendmentStatus: 'TODO(verify): Monitor published gazette for announced Dec 2025/2026 AMLA amendments',
  
  // Mandatory Cash Transaction Reporting (CTR)
  ctrPolicy: {
    thresholdBdt: 1_000_000, // ৳ 1,000,000 statutory CTR threshold
    structuringLowerBoundBdt: 800_000, // Structuring pattern detection lower bound
    structuringUpperBoundBdt: 999_999,
    source: 'BFIU Master Circular 26 (Section 6.1)',
  },

  // Foreign Exchange Reference Rate
  fxRatePolicy: {
    usdToBdt: 120.00,
    source: 'Bangladesh Bank Reference Rate (dated November 2026)',
    sourceUrl: 'https://www.bb.org.bd',
  },

  // Statutory Data Retention
  retentionPolicy: {
    retentionYears: 6, // 6 Years (2,190 days) statutory minimum
    citation: 'MLPA 2012 Section 8(1) & BFIU Master Circular 26 Section 8.3',
  },

  // Trade-Based Money Laundering (TBML)
  tbmlPolicy: {
    priceVarianceThresholdPct: 20.0, // Alert on > 20% divergence from historical / ASYCUDA benchmark
    source: 'BFIU Guidelines for Prevention of Trade Based Money Laundering (2019)',
  }
};
```

---

### 3. Model Governance & SR 11-7 Alignment

While SR 11-7 is a Federal Reserve Supervisory Guidance standard, Intelligent-AML adheres to its structural tenets as an international best practice for Model Risk Management (MRM):
* **Model Validation Report:** [docs/governance/SR11_7_VALIDATION_REPORT.md](file:///c:/Users/SAAD/Documents/GitHub/Intelligent-AML/docs/governance/SR11_7_VALIDATION_REPORT.md)
* **Model Card:** [docs/governance/MODEL_CARD_CSTGB.md](file:///c:/Users/SAAD/Documents/GitHub/Intelligent-AML/docs/governance/MODEL_CARD_CSTGB.md)
* **Drift Monitoring:** Kolmogorov-Smirnov and Population Stability Index (PSI) with automatic fallback to deterministic rule tiering when PSI > 0.25.

---

### 4. European Union GDPR Alignment (Research Prototype Context)

For demonstration and evaluation in European and Swiss research environments (e.g. ETH Zurich):
* **Article 15 (Right of Access):** Customer 360 provides full KYC profile and transaction graph inspection.
* **Article 22 (Automated Decision-Making & Profiling):** Intelligent-AML **does not execute automated case closures**. Every high-risk alert requires human analyst adjudication with mandatory four-eyes supervisor sign-off.
* **Article 32 (Security of Processing):** AES-256-GCM encryption at rest, TLS 1.3 in transit, server-side PII masking, and role-based access control.
