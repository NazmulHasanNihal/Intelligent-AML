-- ==============================================================================
-- Intelligent-AML Enterprise Banking Operating System
-- PostgreSQL 16 OLTP Production Database Initialization
-- Authoritative System of Record for Cases, Alerts, Users, WORM Audit & Conformal
-- ==============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Cases Table (Four-Eyes Dual Control & Evidence Grounding)
CREATE TABLE IF NOT EXISTS cases (
    id VARCHAR(128) PRIMARY KEY,
    title VARCHAR(256) NOT NULL,
    target_account VARCHAR(128) NOT NULL,
    status VARCHAR(64) NOT NULL DEFAULT 'OPEN',
    priority VARCHAR(32) NOT NULL DEFAULT 'MEDIUM',
    exposure_usd DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    cstgb_risk_score DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    initiator VARCHAR(128) NOT NULL,
    lead_assignee VARCHAR(128) NOT NULL,
    second_approver VARCHAR(128),
    regulatory_framework VARCHAR(128) NOT NULL DEFAULT 'BFIU Form STR-1 (MLPA 2012 §25)',
    data_json TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_cases_status ON cases(status);
CREATE INDEX IF NOT EXISTS idx_cases_target_account ON cases(target_account);
CREATE INDEX IF NOT EXISTS idx_cases_priority ON cases(priority);

-- 2. Alerts Table (Tiered Surveillance Stream)
CREATE TABLE IF NOT EXISTS alerts (
    id VARCHAR(128) PRIMARY KEY,
    target_account VARCHAR(128) NOT NULL,
    counterparty VARCHAR(128) NOT NULL,
    amount_usd DOUBLE PRECISION NOT NULL,
    risk_score DOUBLE PRECISION NOT NULL,
    tier VARCHAR(32) NOT NULL, -- Tier 1, Tier 2, Tier 3
    typology VARCHAR(128) NOT NULL,
    status VARCHAR(64) NOT NULL DEFAULT 'PENDING',
    assignee VARCHAR(128),
    latency_ms DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    timestamp VARCHAR(64) NOT NULL,
    data_json TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_alerts_tier ON alerts(tier);
CREATE INDEX IF NOT EXISTS idx_alerts_status ON alerts(status);
CREATE INDEX IF NOT EXISTS idx_alerts_risk_score ON alerts(risk_score DESC);
CREATE INDEX IF NOT EXISTS idx_alerts_target_account ON alerts(target_account);

-- 3. Cryptographically Chained WORM Audit Ledger
CREATE TABLE IF NOT EXISTS audit_ledger (
    block_index INTEGER PRIMARY KEY,
    prev_hash VARCHAR(128) NOT NULL,
    curr_hash VARCHAR(128) NOT NULL,
    timestamp VARCHAR(64) NOT NULL,
    event_type VARCHAR(64) NOT NULL,
    actor VARCHAR(128) NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_audit_event_type ON audit_ledger(event_type);
CREATE INDEX IF NOT EXISTS idx_audit_actor ON audit_ledger(actor);

-- 4. Regulatory Requests for Information (RFI)
CREATE TABLE IF NOT EXISTS rfi_requests (
    id VARCHAR(128) PRIMARY KEY,
    case_id VARCHAR(128) NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    target_account VARCHAR(128) NOT NULL,
    entity_name VARCHAR(256) NOT NULL,
    status VARCHAR(64) NOT NULL DEFAULT 'ISSUED',
    data_json TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_rfi_case_id ON rfi_requests(case_id);

-- 5. Authorized Compliance Users & Signatories
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(128) PRIMARY KEY,
    username VARCHAR(128) UNIQUE NOT NULL,
    full_name VARCHAR(128) NOT NULL,
    email VARCHAR(128) UNIQUE NOT NULL,
    role VARCHAR(64) NOT NULL,
    institution VARCHAR(128) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. Conformal Calibration Audit Trail
CREATE TABLE IF NOT EXISTS conformal_calibration_audit (
    id VARCHAR(128) PRIMARY KEY,
    alpha DOUBLE PRECISION NOT NULL,
    calibration_size INTEGER NOT NULL,
    empirical_coverage DOUBLE PRECISION NOT NULL,
    quantile DOUBLE PRECISION NOT NULL,
    model_version VARCHAR(64) NOT NULL,
    artifact_hash VARCHAR(64) NOT NULL,
    timestamp VARCHAR(64) NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Seed Canonical Bankers & Signatories
INSERT INTO users (id, username, full_name, email, role, institution, is_active)
VALUES
    ('USR-001', 'investigator_l1', 'Alex Rivera', 'alex.rivera@easternbank.example.com', 'INVESTIGATOR_L1', 'Eastern Bank PLC', TRUE),
    ('USR-002', 'investigator_l2', 'Sarah Jenkins', 'sarah.jenkins@easternbank.example.com', 'INVESTIGATOR_L2', 'Eastern Bank PLC', TRUE),
    ('USR-003', 'mlro', 'Marcus Vance', 'marcus.vance@easternbank.example.com', 'MLRO', 'Eastern Bank PLC', TRUE),
    ('USR-004', 'compliance_admin', 'Elena Rostova', 'elena.rostova@easternbank.example.com', 'COMPLIANCE_ADMIN', 'Eastern Bank PLC', TRUE),
    ('USR-005', 'auditor', 'David Kim', 'david.kim@audit.example.com', 'AUDITOR', 'Independent Audit & Risk Advisory', TRUE)
ON CONFLICT (id) DO NOTHING;
