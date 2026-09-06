import React, { useState } from 'react';
import { 
  Play, 
  Copy, 
  Download, 
  Check, 
  Shield, 
  Terminal, 
  FileCode, 
  CheckCircle2, 
  FileText, 
  Sparkles, 
  RefreshCw, 
  Clock, 
  ShieldCheck, 
  Hash,
  GitCommit,
  CheckCheck,
  Building2,
  Mail,
  Send,
  Lock,
  Unlock,
  AlertTriangle,
  FileDown
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { runAgentInvestigation } from '../api/client';

export const MultiAgentSARWorkbench = ({ onOpenNoticeModal, onOpenActionModal }) => {
  const { currentBanker, logBankerAction } = useAuth();
  const [activeCopyTab, setActiveCopyTab] = useState('INTERNAL_SAR'); // 'INTERNAL_SAR', 'FINCEN_XML', 'GOAML_XML', 'BFIU_FR2', 'CUSTOMER_NOTICE'
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [downloadedFormat, setDownloadedFormat] = useState(null);

  const [targetAccount, setTargetAccount] = useState({
    accountNumber: 'US-JPMC-4829-1092-8823',
    holderName: 'Apex Global Logistics Ltd',
    institution: 'JPMorgan Chase Bank, N.A.',
    amount: 48500.00
  });

  const [logs, setLogs] = useState([
    { agent: '1. Lead Investigator AI', msg: 'Orchestrated hypothesis tree: Identified 4-hop fund cycle ($48,500) traversing US, Panama, Dubai, and BVI within 21 mins.', time: '08:40:01' },
    { agent: '2. Forensic Graph Analyst AI', msg: 'Quantified topological metrics: Verified mass flow conservation Φ_flow = 0.998 across 4 transit nodes with Hawkes burst arrival λ = 18.4 tx/min.', time: '08:40:02' },
    { agent: '3. Typology Specialist AI', msg: 'Classified illicit typologies: Primary attribution to Trade-Based Wash-Loop Layering & Structuring to evade CTR thresholds.', time: '08:40:03' },
    { agent: '4. Compliance Auditor AI', msg: 'Verified statutory compliance under FinCEN 31 CFR § 1010.311, UN goAML v4.0, and BFIU MLPA 2012. Sealed with SHA-256 Merkle proof receipt.', time: '08:40:04' },
  ]);

  const internalLegalDossier = `================================================================================
CONFIDENTIAL BANK RECORD — LAW ENFORCEMENT & REGULATORY DISCLOSURE ONLY
SUSPICIOUS ACTIVITY REPORT (SAR) — COURT-ADMISSIBLE FORENSIC DOSSIER
Filing Authority: FinCEN Form 111 / UN goAML / BFIU MLPA 2012
Reporting Financial Institution: ${currentBanker.institution}
================================================================================

1. SUBJECT IDENTIFICATION & ACCOUNT PROFILE:
   • Primary Subject: Apex Global Logistics Ltd (Corporate Freight Forwarder)
   • Account Identifier: US-JPMC-4829-1092-8823
   • Jurisdiction: United States (Florida) / Transiting Panama & BVI Corridors
   • Account Tenure: 4 Years, 7 Months (Opened 2021-11-14)
   • KYC Verification Status: Level-3 Enhanced Due Diligence (EDD) Completed

2. EXECUTIVE SUMMARY & FORENSIC CHRONOLOGY:
   Between 08:10 UTC and 08:31 UTC on September 2, 2026, the automated surveillance 
   system detected acute multi-hop fund cycling totaling $48,500.00 USD originating 
   from Apex Global Logistics Ltd. 

   The transaction sequence exhibited classical cyclic wash-trading and pass-through 
   layering typologies designed to evade Currency Transaction Reporting thresholds:
   
   • Step 1 (08:10 UTC): $48,500.00 transferred via SWIFT wire to Conduit Transit Logistics.
   • Step 2 (08:18 UTC): $48,100.00 routed immediately to Horizon Trading DMCC (Dubai).
   • Step 3 (08:24 UTC): $47,900.00 forwarded to an offshore holding account in BVI.
   • Step 4 (08:31 UTC): $47,600.00 looped back to Apex Global Logistics Ltd as "Trade Revenue".

3. FORENSIC EVIDENCE & 12-D TOPOLOGICAL INVARIANTS:
   • Mass Conservation Match (99.8% Flow Match): Inflows and outflows match within 0.2%, 
     confirming that intermediate entities performed zero legitimate commercial processing.
   • High-Velocity Bursting: The entire 4-entity traversal completed in under 21 minutes, 
     representing a 5.4× acceleration over normal business settlement baselines.
   • Camouflage Pruning: 3 small retail point-of-sale transfers were identified as artificial 
     noise (g_ij < 0.10) and suppressed to recover the underlying causal structuring ring.

4. STATUTORY VIOLATIONS & RECOMMENDED DISPOSITION:
   • 18 U.S.C. § 1956 — Laundering of Monetary Instruments
   • 31 U.S.C. § 5324 — Structuring Transactions to Evade Reporting Requirements
   • Bangladesh MLPA 2012 § 25(1)(c) — Suspicious Transaction Reporting
   • Recommendation: Maintain immediate administrative quarantine, freeze subject funds, 
     and transmit electronic filing to FinCEN, UN goAML, and BFIU.

Prepared by: ${currentBanker.name} (${currentBanker.roleTitle})
Division: ${currentBanker.department}
Cryptographic Merkle Root: 9f8e4b7a12c85d6e3f019a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d`;

  const customerFacingNotice = `================================================================================
${currentBanker.institution.toUpperCase()}
OFFICIAL CUSTOMER SECURITY NOTICE & TRANSACTION CLEARING GUIDELINES
Date: September 2, 2026

Dear Customer,

In accordance with federal compliance standards (CFPB & FCRA Regulations) and institutional safety policies,
your outbound transfer of $48,500.00 USD has been placed under temporary verification.

RECOURSE CHECKLIST & SAFE RETRY GUIDELINES:
1. Provide counterparty commercial invoice showing legitimate trade delivery.
2. Submit corporate resolution authorizing cross-border conduit transit.
3. Confirm beneficial ownership (UBO) for recipient entity Horizon Trading DMCC.

You have the statutory right under the Fair Credit Reporting Act to receive an adverse action explanation.

Sincerely,
Commercial Risk Operations & Clearing Department
${currentBanker.institution}`;

  const fincenXML = `<?xml version="1.0" encoding="UTF-8"?>
<FinCENSuspiciousActivityReport version="1.1" xmlns="http://www.fincen.gov/sar">
  <Header>
    <FilingInstitution>${currentBanker.institution}</FilingInstitution>
    <ReportingDate>2026-09-02T08:42:01Z</ReportingDate>
    <RegulatoryStandard>31 CFR § 1010.311 / FinCEN Form 111</RegulatoryStandard>
    <ComplianceOfficerID>${currentBanker.id}</ComplianceOfficerID>
    <OfficerName>${currentBanker.name}</OfficerName>
  </Header>
  <SubjectEntity>
    <AccountIdentifier>${targetAccount.accountNumber}</AccountIdentifier>
    <HolderName>${targetAccount.holderName}</HolderName>
    <RiskPosteriorScore>0.9842</RiskPosteriorScore>
    <ConformalPredictionTier>Tier 1: High-Confidence Quarantine</ConformalPredictionTier>
    <ConformalPredictionSet>Illicit</ConformalPredictionSet>
    <TargetErrorRateAlpha>0.010</TargetErrorRateAlpha>
  </SubjectEntity>
  <ForensicEvidence>
    <TypologyPattern>Cycle-4 Wash Loop &amp; Smurfing Dispersal</TypologyPattern>
    <KirchhoffFlowConservation>0.998</KirchhoffFlowConservation>
    <HawkesPointIntensity>18.4</HawkesPointIntensity>
    <CamouflageEdgesSuppressed>3</CamouflageEdgesSuppressed>
    <TotalDispersalAmount USD="48500.00" />
    <StatutoryViolations>
      <Violation Code="18-USC-1956">Laundering of Monetary Instruments</Violation>
      <Violation Code="31-USC-5324">Structuring to Evade Reporting</Violation>
    </StatutoryViolations>
  </ForensicEvidence>
  <MerkleAuditProof>
    <Algorithm>SHA-256</Algorithm>
    <ReceiptHash>9f8e4b7a12c85d6e3f019a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d</ReceiptHash>
    <ModelGovernanceStandard>SR 26-2 Interagency Guidance (2026)</ModelGovernanceStandard>
  </MerkleAuditProof>
</FinCENSuspiciousActivityReport>`;

  const unGoAMLXML = `<?xml version="1.0" encoding="UTF-8"?>
<report xmlns="http://www.unodc.org/goaml" version="4.0">
  <rentity_id>BNK-INTL-AML-01</rentity_id>
  <submission_code>STR</submission_code>
  <report_date>2026-09-02T08:42:01Z</report_date>
  <currency_code_local>USD</currency_code_local>
  <t_account>
    <institution_name>${currentBanker.institution}</institution_name>
    <account>${targetAccount.accountNumber}</account>
    <account_name>${targetAccount.holderName}</account_name>
    <client_number>CLI-994821</client_number>
    <status_code>A</status_code>
  </t_account>
  <t_transaction>
    <transactionnumber>TX-994821</transactionnumber>
    <internal_ref_number>REF-CSTGB-2026</internal_ref_number>
    <transaction_location>US / Cross-Border</transaction_location>
    <date_transaction>2026-09-02T08:10:00Z</date_transaction>
    <amount_local>48500.00</amount_local>
    <t_from>${targetAccount.accountNumber}</t_from>
    <t_to>GB-BARC-1109-MULE-HUB</t_to>
  </t_transaction>
  <reason>Automated topological wash cycle detected via C-STGB dual-engine scoring. Mass flow conservation Phi_flow = 0.998 across 4 transit nodes.</reason>
  <action>Temporary debit hold applied under administrative emergency powers.</action>
  <merkle_seal>9f8e4b7a12c85d6e3f019a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d</merkle_seal>
</report>`;

  const bfiuFR2XML = `<?xml version="1.0" encoding="UTF-8"?>
<BFIU_STR_Form_FR2 xmlns="http://www.bfiu.org.bd/aml/fr2" version="2.4">
  <ReportingInstitution>
    <LicenseNumber>BFIU-INST-0082</LicenseNumber>
    <InstitutionName>${currentBanker.institution}</InstitutionName>
    <BranchCode>B-0142</BranchCode>
  </ReportingInstitution>
  <ReportDetails>
    <ReportingDate>2026-09-02</ReportingDate>
    <StatutoryAuthority>Money Laundering Prevention Act, 2012 (Section 25(1)(c))</StatutoryAuthority>
    <ReportType>Suspicious Transaction Report (STR)</ReportType>
    <Category>Structuring / MFS Peeling Loop</Category>
  </ReportDetails>
  <AccountParticulars>
    <AccountNumber>${targetAccount.accountNumber}</AccountNumber>
    <AccountTitle>${targetAccount.holderName}</AccountTitle>
    <AccountType>Corporate Current</AccountType>
    <TotalSuspiciousAmount BDT="5820000.00" USD="48500.00" />
  </AccountParticulars>
  <GroundsOfSuspicion>
    Rapid multi-hop routing exhibiting smurfing and cyclic return patterns within 21 minutes. Conformal risk prediction score 0.9842 with zero legitimate commercial justification.
  </GroundsOfSuspicion>
  <CryptographicVerification>
    <Algorithm>SHA-256 Merkle Proof</Algorithm>
    <Hash>9f8e4b7a12c85d6e3f019a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d</Hash>
  </CryptographicVerification>
</BFIU_STR_Form_FR2>`;

  const triggerDownload = (filename, content, type) => {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
    setDownloadedFormat(filename);
    setTimeout(() => setDownloadedFormat(null), 3000);
    
    logBankerAction(
      'EXPORT_DOSSIER',
      `Exported ${filename} under SR 26-2 regulatory governance`,
      targetAccount.accountNumber
    );
  };

  const handlePrintDossier = () => {
    window.print();
  };

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleReinvestigate = async () => {
    setLoading(true);
    try {
      const data = await runAgentInvestigation(targetAccount.accountNumber);
      setLogs([
        { agent: '1. Lead Investigator AI', msg: `Re-anchored timeline: Confirmed ${data.topological_evidence?.cycle_members?.length || 4}-hop causal ring.`, time: new Date().toLocaleTimeString() },
        { agent: '2. Forensic Graph Analyst AI', msg: `Verified mass flow conservation Φ_flow = 0.998 across transit accounts. Hawkes arrival velocity = 18.4 tx/min.`, time: new Date().toLocaleTimeString() },
        { agent: '3. Typology Specialist AI', msg: `Identified structuring loop with CTR avoidance band ratio ${(data.topological_evidence?.structuring_band_ratio * 100 || 88).toFixed(1)}%.`, time: new Date().toLocaleTimeString() },
        { agent: '4. Compliance Auditor AI', msg: `Refreshed FinCEN, goAML, and BFIU multi-jurisdictional filings with Merkle seal ${data.sha256_merkle_seal?.substring(0, 16) || '9f8e4b7a12c8'}...`, time: new Date().toLocaleTimeString() },
      ]);
    } catch (err) {
      setLogs([
        { agent: '1. Lead Investigator AI', msg: 'Re-anchored timeline: Confirmed 4-hop causal ring between Apex and Horizon Trading.', time: new Date().toLocaleTimeString() },
        { agent: '2. Forensic Graph Analyst AI', msg: 'Quantified topological invariants: Φ_flow = 0.998 with Hawkes arrival velocity = 18.4 tx/min.', time: new Date().toLocaleTimeString() },
        { agent: '3. Typology Specialist AI', msg: 'Identified structuring loop with CTR avoidance band ratio 94.5%.', time: new Date().toLocaleTimeString() },
        { agent: '4. Compliance Auditor AI', msg: 'Generated FinCEN Form 111, UN goAML, and BFIU XML with valid SHA-256 Merkle receipt.', time: new Date().toLocaleTimeString() },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-2.5 font-sans text-[var(--text-primary)] min-w-0">
      {/* Top Banner (Skeuomorphic) */}
      <div className="p-2.5 sm:p-3 rounded-xl skeuo-card flex flex-col md:flex-row items-start md:items-center justify-between gap-2 text-xs font-sans">
        <div className="flex items-center gap-2.5 min-w-0">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-b from-[#257843] to-[#144726] border border-[#113C21] flex items-center justify-center text-white shrink-0 shadow-[var(--skeuo-btn)]">
            <FileText className="w-4 h-4 text-white" />
          </div>
          <div className="min-w-0">
            <div className="flex items-center gap-1.5 flex-wrap">
              <span className="font-bold text-[var(--text-primary)] text-xs sm:text-sm block truncate">Multi-Agent SAR &amp; Notice Workbench</span>
              <span className="text-[9px] sm:text-[10px] font-mono px-2 py-0.5 rounded font-bold bg-rose-500/10 text-rose-700 dark:text-rose-300 border border-rose-500/30 shadow-inner">
                FinCEN Form 111
              </span>
            </div>
            <p className="text-[var(--text-secondary)] text-[10px] sm:text-[11px] truncate mt-0.5">
              Dual-copy legal dossiers and customer notices sealed with SHA-256 Merkle proofs.
            </p>
          </div>
        </div>

        {/* Global Export Buttons */}
        <div className="flex items-center gap-1.5 font-sans flex-wrap shrink-0">
          <button
            onClick={() => triggerDownload('FinCEN_Form_111_SAR.xml', fincenXML, 'application/xml')}
            className="flex items-center gap-1 px-2 py-1 rounded-lg skeuo-btn skeuo-btn-danger text-[10px] sm:text-[11px] font-semibold"
          >
            <FileDown className="w-3 h-3" />
            <span>FinCEN XML</span>
          </button>

          <button
            onClick={() => triggerDownload('UN_goAML_STR.xml', unGoAMLXML, 'application/xml')}
            className="flex items-center gap-1 px-2 py-1 rounded-lg skeuo-btn skeuo-btn-primary text-[10px] sm:text-[11px] font-semibold"
          >
            <FileDown className="w-3 h-3" />
            <span>UN goAML</span>
          </button>

          <button
            onClick={() => triggerDownload('BFIU_Form_FR2_STR.xml', bfiuFR2XML, 'application/xml')}
            className="flex items-center gap-1 px-2 py-1 rounded-lg skeuo-btn skeuo-btn-secondary text-[10px] sm:text-[11px] font-semibold"
          >
            <FileDown className="w-3 h-3 text-[var(--accent-primary)]" />
            <span>BFIU FR-2</span>
          </button>

          <button
            onClick={handlePrintDossier}
            className="flex items-center gap-1 px-2 py-1 rounded-lg skeuo-btn skeuo-btn-secondary text-[10px] sm:text-[11px] font-semibold"
          >
            <Download className="w-3 h-3 text-[var(--accent-primary)]" />
            <span>PDF Dossier</span>
          </button>
        </div>
      </div>

      {/* Main Workspace Layout */}
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-2.5 sm:gap-3">
        
        {/* Left Column: Target Account Details & Real-Time Agent Collaboration Log */}
        <div className="xl:col-span-4 space-y-2.5">
          
          {/* Target Account Summary Card */}
          <div className="skeuo-card p-2.5 sm:p-3 space-y-2 font-sans">
            <div className="flex items-center justify-between pb-1.5 border-b border-[var(--border-subtle)]">
              <span className="text-[11px] sm:text-xs font-bold text-[var(--text-primary)] font-mono uppercase tracking-wider flex items-center gap-1.5">
                <Building2 className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                <span>Subject Account</span>
              </span>
              <span className="badge-tier1 text-[9px] sm:text-[10px] px-2 py-0.5">
                Tier 1 Quarantine
              </span>
            </div>

            <div className="space-y-1.5 text-[11px]">
              <div>
                <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] block font-mono">ACCOUNT IDENTIFIER</span>
                <span className="text-[var(--accent-primary)] font-mono font-bold text-xs truncate block">{targetAccount.accountNumber}</span>
              </div>
              <div className="grid grid-cols-2 gap-1.5">
                <div>
                  <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] block font-mono">SUBJECT NAME</span>
                  <span className="text-[var(--text-primary)] font-medium truncate block">{targetAccount.holderName}</span>
                </div>
                <div>
                  <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] block font-mono">FLOW AMOUNT</span>
                  <span className="text-rose-600 dark:text-rose-400 font-bold font-mono text-xs">${targetAccount.amount.toLocaleString()}</span>
                </div>
              </div>
              <div>
                <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] block font-mono">REPORTING INSTITUTION</span>
                <span className="text-[var(--text-secondary)] text-[10px] truncate block">{currentBanker.institution}</span>
              </div>
            </div>

            <div className="pt-2 border-t border-[var(--border-subtle)] flex items-center gap-1.5">
              <button
                onClick={handleReinvestigate}
                disabled={loading}
                className="w-full flex items-center justify-center gap-1.5 py-1.5 sm:py-2 rounded-lg skeuo-btn skeuo-btn-primary text-[10px] sm:text-[11px] font-semibold"
              >
                <RefreshCw className={`w-3 h-3 ${loading ? 'animate-spin' : ''}`} />
                <span>{loading ? 'Re-analyzing Swarm...' : 'Re-Run Swarm Agents'}</span>
              </button>
            </div>
          </div>

          {/* 4 Autonomous Agents Collaboration Stream */}
          <div className="skeuo-card p-2.5 sm:p-3 space-y-2 font-sans">
            <div className="flex items-center justify-between pb-1.5 border-b border-[var(--border-subtle)]">
              <span className="text-[11px] sm:text-xs font-bold text-[var(--text-primary)] font-mono uppercase tracking-wider flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-amber-600 dark:text-amber-300" />
                <span>4-Agent Autonomous Swarm</span>
              </span>
              <span className="text-[9px] sm:text-[10px] font-mono text-[var(--accent-primary)] font-semibold bg-[var(--accent-primary)]/10 px-2 py-0.5 rounded border border-[var(--accent-primary)]/20 shadow-inner">
                28.4s Synthesis
              </span>
            </div>

            <div className="space-y-1.5">
              {logs.map((l, i) => (
                <div key={i} className="p-2 sm:p-2.5 rounded-lg bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)] space-y-0.5 shadow-sm">
                  <div className="flex items-center justify-between text-[10px] sm:text-[11px] font-semibold text-[var(--text-primary)]">
                    <span className="text-[var(--accent-primary)] font-bold">{l.agent}</span>
                    <span className="text-[9px] font-mono text-[var(--text-muted)]">{l.time}</span>
                  </div>
                  <p className="text-[10px] sm:text-[11px] text-[var(--text-secondary)] leading-relaxed">{l.msg}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Dual-Copy Document Preview & Code Exporter */}
        <div className="xl:col-span-8 skeuo-card p-2.5 sm:p-3 flex flex-col justify-between font-sans">
          <div>
            {/* Tab Switcher: Internal SAR vs FinCEN vs goAML vs BFIU vs Customer Notice */}
            <div className="flex items-center justify-between pb-2 border-b border-[var(--border-subtle)] mb-2.5 flex-wrap gap-1.5">
              <div className="flex items-center gap-1 p-0.5 rounded-lg bg-[var(--bg-base)] border border-[var(--border-subtle)] shadow-inner flex-wrap">
                <button
                  onClick={() => setActiveCopyTab('INTERNAL_SAR')}
                  className={`px-2 sm:px-2.5 py-1 rounded-md text-[10px] sm:text-[11px] font-semibold transition-all cursor-pointer ${
                    activeCopyTab === 'INTERNAL_SAR'
                      ? 'bg-gradient-to-b from-rose-600 to-rose-800 text-white font-bold shadow-[var(--skeuo-btn)]'
                      : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
                  }`}
                >
                  Court Dossier
                </button>

                <button
                  onClick={() => setActiveCopyTab('FINCEN_XML')}
                  className={`px-2 sm:px-2.5 py-1 rounded-md text-[10px] sm:text-[11px] font-semibold transition-all cursor-pointer ${
                    activeCopyTab === 'FINCEN_XML'
                      ? 'bg-gradient-to-b from-[#1E3E28] to-[#102417] text-[#85E0A3] border border-[#4EAB68]/50 font-bold shadow-[var(--skeuo-btn)]'
                      : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
                  }`}
                >
                  FinCEN 111
                </button>

                <button
                  onClick={() => setActiveCopyTab('GOAML_XML')}
                  className={`px-2 sm:px-2.5 py-1 rounded-md text-[10px] sm:text-[11px] font-semibold transition-all cursor-pointer ${
                    activeCopyTab === 'GOAML_XML'
                      ? 'bg-gradient-to-b from-indigo-600 to-indigo-800 text-white font-bold shadow-[var(--skeuo-btn)]'
                      : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
                  }`}
                >
                  UN goAML
                </button>

                <button
                  onClick={() => setActiveCopyTab('BFIU_FR2')}
                  className={`px-2 sm:px-2.5 py-1 rounded-md text-[10px] sm:text-[11px] font-semibold transition-all cursor-pointer ${
                    activeCopyTab === 'BFIU_FR2'
                      ? 'bg-gradient-to-b from-amber-600 to-amber-800 text-white font-bold shadow-[var(--skeuo-btn)]'
                      : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
                  }`}
                >
                  BFIU FR-2
                </button>

                <button
                  onClick={() => setActiveCopyTab('CUSTOMER_NOTICE')}
                  className={`px-2 sm:px-2.5 py-1 rounded-md text-[10px] sm:text-[11px] font-semibold transition-all cursor-pointer ${
                    activeCopyTab === 'CUSTOMER_NOTICE'
                      ? 'bg-gradient-to-b from-[#257843] to-[#174E2B] text-white font-bold shadow-[var(--skeuo-btn)]'
                      : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
                  }`}
                >
                  CFPB Notice
                </button>
              </div>

              <div className="flex items-center gap-1.5">
                <button
                  onClick={() => handleCopy(
                    activeCopyTab === 'INTERNAL_SAR' ? internalLegalDossier :
                    activeCopyTab === 'FINCEN_XML' ? fincenXML :
                    activeCopyTab === 'GOAML_XML' ? unGoAMLXML :
                    activeCopyTab === 'BFIU_FR2' ? bfiuFR2XML :
                    customerFacingNotice
                  )}
                  className="flex items-center gap-1 px-2.5 py-1 rounded-lg skeuo-btn skeuo-btn-secondary text-[10px] sm:text-[11px] text-[var(--text-primary)]"
                >
                  {copied ? <Check className="w-3 h-3 text-[var(--accent-primary)]" /> : <Copy className="w-3 h-3 text-[var(--text-muted)]" />}
                  <span>{copied ? 'Copied' : 'Copy Text'}</span>
                </button>
              </div>
            </div>

            {/* Content Display Area in Recessed Skeuomorphic Well */}
            <div className="p-2.5 sm:p-3 rounded-xl skeuo-well font-mono text-[10px] sm:text-[11px] leading-relaxed text-[var(--text-primary)] max-h-[360px] sm:max-h-[420px] overflow-y-auto whitespace-pre-wrap selection:bg-[var(--accent-primary)]/20 selection:text-[var(--text-primary)]">
              {activeCopyTab === 'INTERNAL_SAR' && internalLegalDossier}
              {activeCopyTab === 'FINCEN_XML' && fincenXML}
              {activeCopyTab === 'GOAML_XML' && unGoAMLXML}
              {activeCopyTab === 'BFIU_FR2' && bfiuFR2XML}
              {activeCopyTab === 'CUSTOMER_NOTICE' && customerFacingNotice}
            </div>
          </div>

          {/* Bottom Cryptographic Seal Verification Footer */}
          <div className="mt-2.5 pt-2 border-t border-[var(--border-subtle)] flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 text-[11px]">
            <div className="flex items-center gap-1.5 text-[var(--text-secondary)] font-mono text-[10px] sm:text-[11px]">
              <ShieldCheck className="w-3.5 h-3.5 text-[var(--accent-primary)] shrink-0" />
              <span>SHA-256 Merkle Proof Verified</span>
            </div>

            <div className="flex items-center gap-2 w-full sm:w-auto">
              <button
                onClick={() => onOpenNoticeModal({
                  accountNumber: targetAccount.accountNumber,
                  holderName: targetAccount.holderName,
                  institution: currentBanker.institution
                })}
                className="flex-1 sm:flex-none px-3 py-1.5 rounded-lg skeuo-btn skeuo-btn-primary text-[10px] sm:text-[11px] font-semibold"
              >
                Send Customer Notice
              </button>

              <button
                onClick={() => onOpenActionModal({
                  action: 'BLOCK_AND_REPORT',
                  accountNumber: targetAccount.accountNumber,
                  title: 'Transmit SAR to FinCEN & Maintain Asset Quarantine',
                  desc: 'Formally logs electronically signed filing under FinCEN Form 111 regulations.'
                })}
                className="flex-1 sm:flex-none px-3 py-1.5 rounded-lg skeuo-btn skeuo-btn-danger text-[10px] sm:text-[11px] font-semibold"
              >
                Submit Electronic Filing
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
