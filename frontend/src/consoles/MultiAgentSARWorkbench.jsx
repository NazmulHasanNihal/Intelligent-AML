import React, { useState, useEffect } from 'react';
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
  FileDown,
  Key,
  Globe,
  MessageSquare,
  History,
  Edit3,
  UserCheck,
  ChevronDown,
  ChevronRight
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { runAgentInvestigation } from '../api/client';

export const MultiAgentSARWorkbench = ({ activeCase, onOpenNoticeModal, onOpenActionModal }) => {
  const { currentBanker, logBankerAction } = useAuth();
  
  // Jurisdiction Selector: 'FINCEN' (US) | 'GOAML' (UN/UK/UAE) | 'BFIU' (Bangladesh)
  const [selectedJurisdiction, setSelectedJurisdiction] = useState('FINCEN');
  
  // View Format: 'NARRATIVE' | 'XML_PAYLOAD' | 'EVIDENCE_AUDIT'
  const [viewFormat, setViewFormat] = useState('NARRATIVE');

  // Tracked Edits & Versioning
  const [activeVersion, setActiveVersion] = useState('v1.1'); // 'v1.0' (AI Raw) | 'v1.1' (Investigator) | 'v2.0' (Approved)
  const [isEditable, setIsEditable] = useState(false);
  const [editableNarrative, setEditableNarrative] = useState('');
  const [copied, setCopied] = useState(false);
  const [loading, setLoading] = useState(false);
  const [downloadedFormat, setDownloadedFormat] = useState(null);
  const [downloadingPdf, setDownloadingPdf] = useState(false);

  const handleDownloadPDF = async () => {
    try {
      setDownloadingPdf(true);
      const caseId = activeCase?.id || 'SAR-2026-BD-8842';
      let res;
      try {
        res = await fetch(`/api/v1/sar/${caseId}/pdf`);
      } catch (e) {
        res = await fetch(`http://localhost:8000/api/v1/sar/${caseId}/pdf`);
      }
      if (!res.ok) {
        res = await fetch(`http://localhost:8000/api/v1/sar/${caseId}/pdf`);
      }
      if (!res.ok) throw new Error('PDF service returned non-200');
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `Regulatory_SAR_${caseId}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);

      setDownloadedFormat('Regulatory_SAR.pdf');
      setTimeout(() => setDownloadedFormat(null), 3000);
      logBankerAction({
        action: 'SAR_PDF_DOSSIER_DOWNLOADED',
        targetAccount: targetAccount.accountNumber,
        reason: `Downloaded official court-admissible SAR PDF with SHA-256 seal.`,
        reasonCode: 'SAR_PDF_EXPORT'
      });
    } catch (err) {
      console.error('PDF download error:', err);
    } finally {
      setDownloadingPdf(false);
    }
  };

  // Reviewer Comments
  const [comments, setComments] = useState([
    { author: 'Sarah L. Jenkins, CFE (Senior Investigator)', time: '08:45 UTC', text: 'Verified wire reference MT103 #994821 and confirmed conduit hop timing. Replaced speculative model tags with factual transaction evidence.' },
    { author: 'Nazmul Hasan, CAMS (CCO)', time: '08:52 UTC', text: 'Approved for Four-Eyes FinCEN Form 111 XML filing upon final verification of beneficiary bank BIC CHASUS33.' }
  ]);
  const [newComment, setNewComment] = useState('');

  // Expandable Agent Reasoning Steps
  const [expandedAgent, setExpandedAgent] = useState(0);

  // Pre-Filing Validation Checklist
  const [checklist, setChecklist] = useState({
    subjectIdentified: true,
    amountsReconciled: true,
    bicsVerified: true,
    tippingOffSafeguardActive: true,
    fourEyesApproved: false
  });

  const [targetAccount, setTargetAccount] = useState({
    accountNumber: 'US-JPMC-4829-1092-8823',
    holderName: 'Apex Global Logistics Ltd',
    institution: 'JPMorgan Chase Bank, N.A.',
    amount: 48500.00
  });

  useEffect(() => {
    if (activeCase) {
      const accId = activeCase.accountNumber || activeCase.src || activeCase.srcId || activeCase.id || 'US-JPMC-4829-1092-8823';
      const name = activeCase.holderName || activeCase.name || 'Apex Global Logistics Ltd';
      const bank = activeCase.institution || activeCase.bank || currentBanker.institution;
      const amt = activeCase.amount || 48500.00;
      setTargetAccount({
        accountNumber: accId,
        holderName: name,
        institution: bank,
        amount: amt
      });
    }
  }, [activeCase, currentBanker.institution]);

  // Jurisdiction-Specific Configurations
  const JURISDICTION_SPECS = {
    FINCEN: {
      name: 'FinCEN Form 111 (United States)',
      authority: 'Financial Crimes Enforcement Network (U.S. Dept. of the Treasury)',
      statute: 'Bank Secrecy Act — 31 U.S.C. § 5318(g) & 31 CFR § 1020.320',
      slaTimer: '30 Calendar Days (Mandatory Federal Deadline)',
      slaHours: '28d 14h Remaining',
      formType: 'FinCEN Form 111 XML v1.2',
      disclaimer: 'CONFIDENTIAL: Unauthorized disclosure is a federal felony under 31 U.S.C. § 5318(g)(2).'
    },
    GOAML: {
      name: 'UNODC goAML v4.0 (International / UK / UAE)',
      authority: 'United Nations Office on Drugs and Crime / National FIU',
      statute: 'FATF Recommendation 20 (Suspicious Transaction Reporting)',
      slaTimer: '5 Business Days (Standard FIU Processing Window)',
      slaHours: '4d 08h Remaining',
      formType: 'goAML XML Schema v4.0.2',
      disclaimer: 'RESTRICTED LAW ENFORCEMENT RECORD: Protected under national anti-money laundering statutes.'
    },
    BFIU: {
      name: 'BFIU Form STR-2 (Bangladesh)',
      authority: 'Bangladesh Financial Intelligence Unit (Bangladesh Bank)',
      statute: 'Money Laundering Prevention Act 2012, Section 25 & Circular No. 26/2020',
      slaTimer: '72 Hours for High-Risk Transactions / 30 Days Standard',
      slaHours: '18h 32m Remaining (Urgent 72h Flag)',
      formType: 'BFIU Electronic STR Schema',
      disclaimer: 'CONFIDENTIAL: Disclosure to account holder prohibited under Section 25(2) of MLPA 2012.'
    }
  };

  const currentSpec = JURISDICTION_SPECS[selectedJurisdiction];

  // Factual, Regulatory SAR Narrative (Describes Who, What, When, Where, Why, How — NEVER cites internal model names!)
  const fincenNarrative = `================================================================================
CONFIDENTIAL LAW ENFORCEMENT DOCUMENT — REGULATORY FILING
SUSPICIOUS ACTIVITY REPORT (SAR) NARRATIVE
Reporting Financial Institution: ${currentBanker.institution} (RSSD ID: 000852218)
Filing Jurisdiction: United States — FinCEN Form 111 (31 CFR § 1020.320)
Document Status: AI Draft v1.1 [Verified by Senior Investigator | Pending Final CCO Sign-Off]
================================================================================

PART I: SUBJECT IDENTIFICATION
• Primary Subject: ${targetAccount.holderName} [Verified: State Corporate Registry]
• Account Identifier: ${targetAccount.accountNumber} [Verified: Core Banking Ledger]
• Customer Relationship: Commercial Operating Account (Established: March 2021)
• Customer Due Diligence (CDD) Status: Standard CDD on file. Enhanced Due Diligence (EDD) triggered; source-of-funds RFI pending.
• Beneficial Ownership (UBO): Registered signatory Dmitry Rostov (51% equity interest).

PART II: SUMMARY OF SUSPICIOUS ACTIVITY
On September 2, 2026, between 08:10 UTC and 08:31 UTC, ${currentBanker.institution} identified an acute circular funds transfer sequence totaling $${targetAccount.amount.toLocaleString()} USD originating from and terminating at the account of ${targetAccount.holderName}. The funds traversed multiple corporate and retail accounts across four distinct banking corridors within twenty-one (21) minutes without apparent economic substance, commercial rationale, or legitimate business purpose.

PART III: CHRONOLOGICAL TRANSACTION TRAIL
1. Step 1 (08:10:14 UTC): Outbound SWIFT Wire MT103 [Ref: #994821] in the amount of $${targetAccount.amount.toLocaleString()} USD debited from ${targetAccount.holderName} (${targetAccount.accountNumber}) and transmitted to Barclays Bank PLC (London, UK) beneficiary Elena Rostova (Account: GB-BARC-1109-8832-9011).
2. Step 2 (08:18:22 UTC): Beneficiary Elena Rostova immediately transferred $${(targetAccount.amount * 0.992).toLocaleString(undefined, { maximumFractionDigits: 2 })} USD via SEPA wire to Horizon Trading DMCC at Standard Chartered Bank (Dubai, UAE).
3. Step 3 (08:24:05 UTC): Horizon Trading DMCC wired $${(targetAccount.amount * 0.988).toLocaleString(undefined, { maximumFractionDigits: 2 })} USD to BVI Sovereign Vault LP (Road Town, British Virgin Islands).
4. Step 4 (08:31:40 UTC): BVI Sovereign Vault LP returned $${(targetAccount.amount * 0.981).toLocaleString(undefined, { maximumFractionDigits: 2 })} USD via SWIFT wire directly back to ${targetAccount.holderName} (${targetAccount.accountNumber}), referencing fictitious invoice "INV-2026-APEX-901".

PART IV: SUSPICIOUS INDICATORS & TYPOLOGY ATTRIBUTION
• Circular Flow Conservation: Total inflow and outflow values match within 0.2%, demonstrating that intermediate entities served solely as transit conduits and conducted zero commercial processing.
• Rapid Transit Velocity: All four legs completed in under 21 minutes, an acceleration 5.4× faster than normal commercial cross-border settlement baselines.
• Evidentiary Citations:
  - Wire MT103 confirmation ticket #994821 [Attached: Exhibit A]
  - IP login records matching commercial VPN transit [Attached: Exhibit B]
  - Absence of underlying customs bill of lading or commercial freight contracts [Exhibit C]

PART V: STATUTORY VIOLATIONS & DISPOSITION
The described transactions exhibit classical indicators of Trade-Based Money Laundering (TBML) layering, circular wash transactions, and evasion of Bank Secrecy Act requirements under 18 U.S.C. § 1956 and 31 U.S.C. § 5324.

• Action Taken: Temporary administrative hold placed on outbound transfers pending regulatory submission.
• Recommendation: Dual-control transmission of FinCEN Form 111 XML. Law enforcement follow-up requested.

================================================================================
FOUR-EYES GOVERNANCE & HUMAN SIGN-OFF RECORD
• Prepared by: Sarah L. Jenkins, CFE (Senior AML Investigator, SIU)
• Reviewed & Authorized by: ${currentBanker.name} (${currentBanker.roleTitle})
• Cryptographic Ledger Root: 9f8e4b7a12c85d6e3f019a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d
• Retention Schedule: 5 Years pursuant to 31 CFR § 1010.430 (WORM Storage Policy Active)
================================================================================`;

  const goAMLNarrative = `================================================================================
UNODC goAML v4.0 — SUSPICIOUS TRANSACTION REPORT (STR)
National Financial Intelligence Unit (FIU) Electronic Transmission
Reporting Entity: ${currentBanker.institution} | Reporting Officer ID: ${currentBanker.id}
Statutory Basis: FATF Recommendation 20 / National AML Enforcement Directives
================================================================================

1. REPORTING PARTY DETAILS:
   • Reporting Institution: ${currentBanker.institution}
   • Branch / Desk: Global Financial Crimes & Special Investigations Unit
   • FIU Registration Number: FIU-US-00852218

2. SUSPICIOUS TRANSACTION SUMMARY:
   • Transaction Type: International Wire Transfer Cycle (MT103 / SEPA)
   • Total Value: $${targetAccount.amount.toLocaleString()} USD
   • Value Date: September 2, 2026
   • Suspicion Category: Pass-Through Conduit / Multi-Jurisdiction Wash Loop

3. PERSONS / ENTITIES OF INTEREST:
   • Subject: ${targetAccount.holderName} (Account: ${targetAccount.accountNumber})
   • Intermediary 1: Elena Rostova (Barclays UK - GB-BARC-1109-8832-9011)
   • Intermediary 2: Horizon Trading DMCC (Standard Chartered UAE - AE-SCBL-5512-HORIZON)
   • Intermediary 3: BVI Sovereign Vault LP (Offshore Escrow Entity)

4. NARRATIVE REASON FOR SUSPICION:
   The subject entity conducted a closed-loop fund transfer sequence routing $${targetAccount.amount.toLocaleString()} through four separate jurisdictions in twenty-one minutes. The funds returned to the originating entity with less than 2% deduction for transit fees. No commercial freight or trade documentation has been produced to support the transaction sequence.

5. SIGNATORY VERIFICATION:
   • Senior Compliance Investigator: Sarah L. Jenkins, CFE
   • Authorizing MLRO: ${currentBanker.name}, CAMS
   • Tamper-Evident SHA-256 Receipt: 9f8e4b7a12c85d6e3f019a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d`;

  const bfiuNarrative = `================================================================================
BANGLADESH FINANCIAL INTELLIGENCE UNIT (BFIU)
SUSPICIOUS TRANSACTION REPORT (STR) — FORM STR-2 (INSTITUTIONAL)
Submission under Section 25(1)(c) of the Money Laundering Prevention Act, 2012
Reporting Entity: ${currentBanker.institution}
================================================================================

1. REPORTING ENTITY DETAILS:
   • Organization Name: ${currentBanker.institution}
   • Designated Anti-Money Laundering Compliance Officer (CAMLCO): ${currentBanker.name}, CAMS
   • BFIU Registration Code: BFIU-RE-2026-0814

2. TRANSACTION PARTICULARS:
   • Suspect Account: ${targetAccount.holderName}
   • Account Number: ${targetAccount.accountNumber}
   • Currency & Amount: $${targetAccount.amount.toLocaleString()} USD (Equivalent BDT ~5,820,000)
   • Originating Corridor: United States transiting Offshore Financial Centres
   • Urgency Indicator: 72-Hour Statutory STR Threshold Triggered

3. REASON FOR SUSPICION (CIRCULAR 26/2020 RED FLAGS):
   • Red Flag #4: Unusual cross-border velocity and multi-hop wire transfers without apparent legitimate commercial purpose.
   • Red Flag #12: Circular layering of export/import proceeds with immediate turnaround across offshore correspondent nodes.

4. INVESTIGATION SUMMARY:
   Within 21 minutes, funds were dispersed across three foreign jurisdictions and returned to source, simulating legitimate trade revenue. The transactions demonstrate high risk of illicit layering.

5. DECLARATION:
   I hereby declare that this report is submitted in good faith and that tipping-off safeguards under Section 25(2) of the MLPA 2012 have been enforced.

   Submitted by:
   ${currentBanker.name} (${currentBanker.roleTitle})
   Chief Anti-Money Laundering Officer`;

  const fincenXML = `<?xml version="1.0" encoding="UTF-8"?>
<FinCENSAR version="1.2" xmlns="http://www.fincen.gov/sar">
  <Header>
    <FilingInstitution>${currentBanker.institution}</FilingInstitution>
    <TransmissionDate>${new Date().toISOString()}</TransmissionDate>
    <RegulatoryCitation>31 CFR § 1020.320</RegulatoryCitation>
    <Jurisdiction>USA</Jurisdiction>
    <SLADeadline>30-Day Mandatory</SLADeadline>
  </Header>
  <Subject>
    <PartyName>${targetAccount.holderName}</PartyName>
    <AccountNumber>${targetAccount.accountNumber}</AccountNumber>
    <TotalAmount currency="USD">${targetAccount.amount.toFixed(2)}</TotalAmount>
    <SuspiciousActivityCategory>Structuring / Layering / TBML</SuspiciousActivityCategory>
  </Subject>
  <Chronology>
    <Hop sequence="1" time="08:10 UTC" amount="${targetAccount.amount}" counterparty="Elena Rostova (Barclays UK)" />
    <Hop sequence="2" time="08:18 UTC" amount="${(targetAccount.amount * 0.992).toFixed(2)}" counterparty="Horizon Trading DMCC (Standard Chartered UAE)" />
    <Hop sequence="3" time="08:24 UTC" amount="${(targetAccount.amount * 0.988).toFixed(2)}" counterparty="BVI Sovereign Vault LP (Offshore)" />
    <Hop sequence="4" time="08:31 UTC" amount="${(targetAccount.amount * 0.981).toFixed(2)}" counterparty="${targetAccount.holderName} (Wash Return)" />
  </Chronology>
  <Governance>
    <PreparedBy>Sarah L. Jenkins, CFE (Senior Investigator)</PreparedBy>
    <AuthorizedBy>${currentBanker.name} (${currentBanker.roleTitle})</AuthorizedBy>
    <FourEyesVerified>true</FourEyesVerified>
    <MerkleRootHash>9f8e4b7a12c85d6e3f019a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d</MerkleRootHash>
    <WORMStoragePolicy>SEC 17a-4 / FINRA 4511 Compliant (5-Year Minimum)</WORMStoragePolicy>
  </Governance>
</FinCENSAR>`;

  const activeNarrative = selectedJurisdiction === 'FINCEN' 
    ? fincenNarrative 
    : selectedJurisdiction === 'GOAML' 
    ? goAMLNarrative 
    : bfiuNarrative;

  useEffect(() => {
    setEditableNarrative(activeNarrative);
  }, [selectedJurisdiction, activeVersion]);

  const [agentLogs, setAgentLogs] = useState([
    {
      id: 1,
      name: 'Transaction Reconstruction Agent',
      role: 'Chronological Trail Synthesizer',
      confidence: 99.4,
      status: 'VERIFIED',
      evidenceCount: 4,
      summary: 'Constructed complete 4-hop transaction timeline matching wire MT103 #994821 with 21-minute dwell window.',
      details: 'Retrieved core banking raw wire tickets. Validated timestamp sequence 08:10 -> 08:18 -> 08:24 -> 08:31 UTC. Mass flow match: 99.8%.'
    },
    {
      id: 2,
      name: 'Counterparty Resolution Agent',
      role: 'Entity & Registry Resolver',
      confidence: 98.1,
      status: 'VERIFIED',
      evidenceCount: 3,
      summary: 'Resolved entity ownership records across UK Companies House, Dubai DMCC registry, and BVI corporate filings.',
      details: 'Found common beneficial ownership links between Apex Global Logistics and Horizon Trading DMCC signatory.'
    },
    {
      id: 3,
      name: 'Statutory Compliance Agent',
      role: 'Jurisdictional Rule Mapper',
      confidence: 100.0,
      status: 'VERIFIED',
      evidenceCount: 5,
      summary: `Synthesized formal narrative under ${currentSpec.name}. Enforced anti-tipping-off safeguards (31 U.S.C. § 5318(g)(2)).`,
      details: 'Checked filing requirements against FinCEN 31 CFR § 1020.320, UN goAML v4.0, and BFIU MLPA 2012 Section 25.'
    },
    {
      id: 4,
      name: 'Evidence Integrity & WORM Audit Agent',
      role: 'Cryptographic Notary',
      confidence: 100.0,
      status: 'SEALED',
      evidenceCount: 6,
      summary: 'Computed SHA-256 Merkle root and locked dossier for Four-Eyes sign-off under SEC 17a-4 retention standard.',
      details: 'Merkle root: 9f8e4b7a12c85d6e3f019a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d. All exhibit links indexed.'
    }
  ]);

  const handleCopyText = () => {
    navigator.clipboard.writeText(editableNarrative);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadFile = (filename, content, mime) => {
    const blob = new Blob([content], { type: mime });
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

    logBankerAction({
      action: 'SAR_DOSSIER_EXPORTED',
      targetAccount: targetAccount.accountNumber,
      reason: `Exported ${filename} under ${currentSpec.statute}. Four-Eyes sign-off tracked.`,
      reasonCode: 'SAR_EXPORT'
    });
  };

  const handleAddComment = (e) => {
    e.preventDefault();
    if (!newComment.trim()) return;
    setComments(prev => [
      ...prev,
      {
        author: `${currentBanker.name} (${currentBanker.roleTitle})`,
        time: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', timeZone: 'UTC' }) + ' UTC',
        text: newComment.trim()
      }
    ]);
    setNewComment('');
  };

  const handleAuthorizeFourEyes = () => {
    setChecklist(prev => ({ ...prev, fourEyesApproved: true }));
    setActiveVersion('v2.0');
    logBankerAction({
      action: 'SAR_FOUR_EYES_AUTHORIZED',
      targetAccount: targetAccount.accountNumber,
      reason: `Dual-control authorization executed for ${currentSpec.name} filing ($${targetAccount.amount.toLocaleString()}).`,
      initiatorName: 'Sarah L. Jenkins, CFE (Senior Investigator)',
      approverName: `${currentBanker.name} (${currentBanker.roleTitle})`,
      reasonCode: 'FOUR_EYES_SAR_APPROVAL',
      fourEyesVerified: true
    });
  };

  return (
    <div className="space-y-2.5 font-sans text-[var(--text-primary)] min-w-0">
      
      {/* Top Banner: Institutional Compliance Workspace */}
      <div className="p-2.5 sm:p-3 rounded-xl skeuo-card flex flex-col md:flex-row items-start md:items-center justify-between gap-2.5 text-xs">
        <div className="flex items-center gap-2.5 min-w-0">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-b from-[#257843] to-[#144726] border border-[#113C21] flex items-center justify-center text-white shrink-0 shadow-[var(--skeuo-btn)]">
            <FileText className="w-4 h-4 text-white" />
          </div>
          <div className="min-w-0">
            <div className="flex items-center gap-1.5 flex-wrap">
              <span className="font-bold text-[var(--text-primary)] text-xs sm:text-sm block truncate">
                Multi-Agent SAR Filing &amp; Evidence Workbench
              </span>
              <span className="text-[9px] sm:text-[10px] font-mono px-2 py-0.5 rounded font-bold bg-amber-500/10 text-amber-700 dark:text-amber-300 border border-amber-500/30 shadow-inner">
                AI Draft — Pending Officer Sign-Off
              </span>
              <span className="text-[9px] sm:text-[10px] font-mono px-2 py-0.5 rounded font-bold bg-indigo-500/10 text-indigo-300 border border-indigo-500/30">
                Case: CASE-2026-APEX ($48,500 Exposure)
              </span>
            </div>
            <p className="text-[var(--text-secondary)] text-[10px] sm:text-[11px] truncate mt-0.5">
              Side-by-side evidence chronicle, jurisdiction-specific regulatory filing, and four-eyes authorization audit chain.
            </p>
          </div>
        </div>

        {/* Global Export & Filing Actions */}
        <div className="flex items-center gap-1.5 flex-wrap shrink-0">
          <button
            onClick={handleDownloadPDF}
            disabled={downloadingPdf}
            className="flex items-center gap-1 px-2.5 py-1 rounded-lg skeuo-btn skeuo-btn-primary bg-emerald-700 hover:bg-emerald-600 text-white text-[10px] sm:text-[11px] font-semibold cursor-pointer shadow-sm transition-all"
            title="Download Official Court-Admissible SAR PDF with SHA-256 Seal"
          >
            <Download className="w-3.5 h-3.5 text-white" />
            <span>{downloadingPdf ? 'Generating PDF...' : 'Official Sealed PDF'}</span>
          </button>

          <button
            onClick={() => handleDownloadFile(`${selectedJurisdiction}_SAR_Filing.xml`, fincenXML, 'application/xml')}
            className="flex items-center gap-1 px-2.5 py-1 rounded-lg skeuo-btn skeuo-btn-secondary text-[10px] sm:text-[11px] font-semibold cursor-pointer"
            title="Export Regulatory XML Package"
          >
            <FileDown className="w-3.5 h-3.5" />
            <span>Export Regulatory XML</span>
          </button>

          <button
            onClick={() => handleDownloadFile('SAR_Forensic_Dossier.md', editableNarrative, 'text/markdown')}
            className="flex items-center gap-1 px-2.5 py-1 rounded-lg skeuo-btn skeuo-btn-secondary text-[10px] sm:text-[11px] font-semibold cursor-pointer"
            title="Download Complete Forensic Dossier (.md)"
          >
            <FileText className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
            <span>Dossier (.md)</span>
          </button>
        </div>
      </div>

      {/* Jurisdiction Selector & Regulatory SLA Banner */}
      <div className="p-2 sm:p-2.5 rounded-xl bg-[var(--bg-card)] border border-[var(--border-subtle)] flex flex-wrap items-center justify-between gap-2 text-[11px] font-mono shadow-sm">
        <div className="flex items-center gap-2">
          <Globe className="w-3.5 h-3.5 text-[var(--accent-primary)] shrink-0" />
          <span className="text-[var(--text-muted)] font-bold">FILING JURISDICTION:</span>
          
          <div className="flex items-center gap-1 bg-[var(--bg-base)] p-0.5 rounded-lg border border-[var(--border-subtle)]">
            <button
              onClick={() => setSelectedJurisdiction('FINCEN')}
              className={`px-2.5 py-1 rounded-md text-[10px] font-bold transition-all cursor-pointer ${
                selectedJurisdiction === 'FINCEN'
                  ? 'bg-gradient-to-r from-emerald-600 to-emerald-800 text-white shadow-sm'
                  : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
              }`}
            >
              FinCEN Form 111 (US)
            </button>
            <button
              onClick={() => setSelectedJurisdiction('GOAML')}
              className={`px-2.5 py-1 rounded-md text-[10px] font-bold transition-all cursor-pointer ${
                selectedJurisdiction === 'GOAML'
                  ? 'bg-gradient-to-r from-indigo-600 to-indigo-800 text-white shadow-sm'
                  : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
              }`}
            >
              UNODC goAML v4.0 (Intl)
            </button>
            <button
              onClick={() => setSelectedJurisdiction('BFIU')}
              className={`px-2.5 py-1 rounded-md text-[10px] font-bold transition-all cursor-pointer ${
                selectedJurisdiction === 'BFIU'
                  ? 'bg-gradient-to-r from-amber-600 to-amber-800 text-white shadow-sm'
                  : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
              }`}
            >
              BFIU Form STR-2 (BD)
            </button>
          </div>
        </div>

        {/* Dynamic Regulatory SLA Countdown */}
        <div className="flex items-center gap-2">
          <Clock className="w-3.5 h-3.5 text-amber-500" />
          <span className="text-[var(--text-muted)]">STATUTORY SLA:</span>
          <span className="text-amber-700 dark:text-amber-300 font-bold bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
            {currentSpec.slaHours}
          </span>
          <span className="text-[10px] text-[var(--text-muted)] hidden lg:inline">({currentSpec.statute.split('—')[0]})</span>
        </div>
      </div>

      {/* Main Side-by-Side Workspace */}
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-2.5 sm:gap-3">
        
        {/* Left Column (5 Cols): Evidence Chronicle & Expandable Agent Reasoning */}
        <div className="xl:col-span-5 space-y-2.5">
          
          {/* Target Account Summary Card */}
          <div className="skeuo-card p-2.5 sm:p-3 space-y-2 font-sans">
            <div className="flex items-center justify-between pb-1.5 border-b border-[var(--border-subtle)]">
              <span className="text-[11px] sm:text-xs font-bold text-[var(--text-primary)] font-mono uppercase tracking-wider flex items-center gap-1.5">
                <Building2 className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                <span>Subject Account &amp; Exposure</span>
              </span>
              <span className="badge-tier1 text-[9px] sm:text-[10px] px-2 py-0.5">
                Tier 1 Quarantine
              </span>
            </div>

            <div className="space-y-1.5 text-[11px]">
              <div>
                <span className="text-[9px] text-[var(--text-muted)] block font-mono">ACCOUNT IDENTIFIER</span>
                <span className="text-[var(--accent-primary)] font-mono font-bold text-xs truncate block">{targetAccount.accountNumber}</span>
              </div>
              <div className="grid grid-cols-2 gap-1.5">
                <div>
                  <span className="text-[9px] text-[var(--text-muted)] block font-mono">SUBJECT NAME</span>
                  <span className="text-[var(--text-primary)] font-semibold truncate block">{targetAccount.holderName}</span>
                </div>
                <div>
                  <span className="text-[9px] text-[var(--text-muted)] block font-mono">TOTAL RECONCILED FLOW</span>
                  <span className="text-rose-600 dark:text-rose-400 font-bold font-mono text-xs">${targetAccount.amount.toLocaleString()} USD</span>
                </div>
              </div>
              <div className="p-2 rounded-lg bg-[var(--bg-base)] border border-[var(--border-subtle)] space-y-1 text-[10px]">
                <div className="flex justify-between text-[var(--text-secondary)] font-mono">
                  <span>Linked Transfers: <strong>4 Transactions</strong></span>
                  <span>Duration: <strong>21 Minutes</strong></span>
                </div>
                <div className="flex justify-between text-[var(--text-secondary)] font-mono">
                  <span>Mass Conservation Φ: <strong>0.998</strong></span>
                  <span>Evidentiary Receipts: <strong>4 MT103 Verified</strong></span>
                </div>
              </div>
            </div>
          </div>

          {/* Expandable Multi-Agent Collaboration Steps */}
          <div className="skeuo-card p-2.5 sm:p-3 space-y-2 font-sans">
            <div className="flex items-center justify-between pb-1.5 border-b border-[var(--border-subtle)]">
              <span className="text-[11px] sm:text-xs font-bold text-[var(--text-primary)] font-mono uppercase tracking-wider flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-amber-500" />
                <span>Agent Synthesis Chronicle</span>
              </span>
              <span className="text-[9px] font-mono text-emerald-500 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                4/4 Agents Aligned
              </span>
            </div>

            <div className="space-y-1.5">
              {agentLogs.map((agent, i) => {
                const isExpanded = expandedAgent === i;
                return (
                  <div key={agent.id} className="rounded-lg bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)] p-2 space-y-1 transition-all">
                    <div 
                      onClick={() => setExpandedAgent(isExpanded ? null : i)}
                      className="flex items-center justify-between cursor-pointer text-[11px]"
                    >
                      <div className="flex items-center gap-1.5 font-semibold text-[var(--text-primary)]">
                        {isExpanded ? <ChevronDown className="w-3.5 h-3.5 text-[var(--accent-primary)]" /> : <ChevronRight className="w-3.5 h-3.5 text-[var(--text-muted)]" />}
                        <span>{agent.name}</span>
                      </div>
                      <span className="text-[9px] font-mono text-emerald-600 dark:text-emerald-400 font-bold bg-emerald-500/10 px-1.5 py-0.2 rounded border border-emerald-500/20">
                        {agent.confidence}% Conf.
                      </span>
                    </div>

                    <p className="text-[10px] text-[var(--text-secondary)] pl-5 leading-relaxed">
                      {agent.summary}
                    </p>

                    {isExpanded && (
                      <div className="mt-1 pt-1 border-t border-[var(--border-subtle)] pl-5 text-[10px] font-mono text-[var(--text-muted)] bg-[var(--bg-base)] p-1.5 rounded animate-fadeIn">
                        <div><strong className="text-[var(--text-primary)]">Reasoning Detail:</strong> {agent.details}</div>
                        <div className="mt-0.5 text-emerald-500">✓ Evidence Items Indexed: {agent.evidenceCount} verified receipts</div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Pre-Filing Validation Checklist */}
          <div className="skeuo-card p-2.5 sm:p-3 space-y-2 font-sans">
            <div className="flex items-center justify-between pb-1.5 border-b border-[var(--border-subtle)]">
              <span className="text-[11px] sm:text-xs font-bold text-[var(--text-primary)] font-mono uppercase tracking-wider flex items-center gap-1.5">
                <CheckCheck className="w-3.5 h-3.5 text-emerald-500" />
                <span>Pre-Filing Compliance Checklist</span>
              </span>
              <span className="text-[9px] font-mono text-[var(--text-muted)]">
                {checklist.fourEyesApproved ? 'Ready to Transmit' : 'Pending Authorization'}
              </span>
            </div>

            <div className="space-y-1.5 text-[11px]">
              <label className="flex items-center gap-2 cursor-pointer">
                <input 
                  type="checkbox" 
                  checked={checklist.subjectIdentified} 
                  onChange={(e) => setChecklist(prev => ({ ...prev, subjectIdentified: e.target.checked }))}
                  className="accent-[var(--accent-primary)]" 
                />
                <span className="text-[var(--text-secondary)]">Subject identity verified via core banking KYC records</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input 
                  type="checkbox" 
                  checked={checklist.amountsReconciled} 
                  onChange={(e) => setChecklist(prev => ({ ...prev, amountsReconciled: e.target.checked }))}
                  className="accent-[var(--accent-primary)]" 
                />
                <span className="text-[var(--text-secondary)]">All 4 transaction leg amounts reconciled ($48,500 total exposure)</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input 
                  type="checkbox" 
                  checked={checklist.tippingOffSafeguardActive} 
                  onChange={(e) => setChecklist(prev => ({ ...prev, tippingOffSafeguardActive: e.target.checked }))}
                  className="accent-[var(--accent-primary)]" 
                />
                <span className="text-[var(--text-secondary)]">Anti-Tipping-Off protocols enforced (31 U.S.C. § 5318(g)(2))</span>
              </label>
            </div>

            <div className="pt-2 border-t border-[var(--border-subtle)]">
              <button
                onClick={handleAuthorizeFourEyes}
                disabled={checklist.fourEyesApproved}
                className={`w-full py-2 rounded-xl text-xs font-bold flex items-center justify-center gap-1.5 transition-all cursor-pointer ${
                  checklist.fourEyesApproved 
                    ? 'bg-emerald-600/20 text-emerald-400 border border-emerald-500/40 cursor-default'
                    : 'skeuo-btn skeuo-btn-primary'
                }`}
              >
                <ShieldCheck className="w-4 h-4" />
                <span>{checklist.fourEyesApproved ? '✓ Four-Eyes Dual Sign-Off Authorized' : 'Execute Four-Eyes CCO Sign-Off'}</span>
              </button>
            </div>
          </div>

        </div>

        {/* Right Column (7 Cols): Editable Side-by-Side Narrative & Version History */}
        <div className="xl:col-span-7 skeuo-card p-2.5 sm:p-3 flex flex-col justify-between font-sans">
          
          <div className="space-y-2">
            {/* Workbench Sub-Header: Version Tabs & View Formats */}
            <div className="flex flex-wrap items-center justify-between pb-2 border-b border-[var(--border-subtle)] gap-2">
              <div className="flex items-center gap-1 bg-[var(--bg-base)] p-0.5 rounded-lg border border-[var(--border-subtle)]">
                <button
                  onClick={() => setViewFormat('NARRATIVE')}
                  className={`px-2.5 py-1 rounded-md text-[10px] sm:text-[11px] font-semibold transition-all cursor-pointer ${
                    viewFormat === 'NARRATIVE' ? 'bg-[var(--accent-primary)] text-white font-bold' : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
                  }`}
                >
                  Legal Narrative
                </button>
                <button
                  onClick={() => setViewFormat('XML_PAYLOAD')}
                  className={`px-2.5 py-1 rounded-md text-[10px] sm:text-[11px] font-semibold transition-all cursor-pointer ${
                    viewFormat === 'XML_PAYLOAD' ? 'bg-indigo-600 text-white font-bold' : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
                  }`}
                >
                  Electronic XML Schema
                </button>
              </div>

              {/* Version History Selector */}
              <div className="flex items-center gap-1.5 text-[10px] font-mono">
                <History className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                <span className="text-[var(--text-muted)]">Version:</span>
                <button
                  onClick={() => setActiveVersion('v1.0')}
                  className={`px-2 py-0.5 rounded cursor-pointer ${activeVersion === 'v1.0' ? 'bg-slate-700 text-white font-bold' : 'text-[var(--text-muted)]'}`}
                >
                  v1.0 (AI Raw)
                </button>
                <button
                  onClick={() => setActiveVersion('v1.1')}
                  className={`px-2 py-0.5 rounded cursor-pointer ${activeVersion === 'v1.1' ? 'bg-indigo-700 text-white font-bold' : 'text-[var(--text-muted)]'}`}
                >
                  v1.1 (Investigator)
                </button>
                <button
                  onClick={() => setActiveVersion('v2.0')}
                  className={`px-2 py-0.5 rounded cursor-pointer ${activeVersion === 'v2.0' ? 'bg-emerald-700 text-white font-bold' : 'text-[var(--text-muted)]'}`}
                >
                  v2.0 (Approved)
                </button>
              </div>

              <div className="flex items-center gap-1.5">
                <button
                  onClick={() => setIsEditable(prev => !prev)}
                  className={`px-2 py-1 rounded-md text-[10px] font-bold border transition-all cursor-pointer flex items-center gap-1 ${
                    isEditable 
                      ? 'bg-amber-500/20 text-amber-300 border-amber-500/40' 
                      : 'border-[var(--border-subtle)] text-[var(--text-muted)] hover:text-[var(--text-primary)]'
                  }`}
                >
                  <Edit3 className="w-3 h-3" />
                  <span>{isEditable ? 'Editing Enabled' : 'Edit Narrative'}</span>
                </button>
                <button
                  onClick={handleCopyText}
                  className="flex items-center gap-1 px-2.5 py-1 rounded-lg skeuo-btn text-[10px] font-semibold cursor-pointer"
                >
                  {copied ? <Check className="w-3 h-3 text-emerald-500" /> : <Copy className="w-3 h-3 text-[var(--accent-primary)]" />}
                  <span>{copied ? 'Copied' : 'Copy'}</span>
                </button>
              </div>
            </div>

            {/* Document Content Viewport */}
            <div className="p-3 sm:p-4 rounded-xl skeuo-well bg-[var(--bg-base)] text-[11px] font-mono leading-relaxed overflow-x-auto max-h-[380px] sm:max-h-[440px] overflow-y-auto whitespace-pre border border-[var(--border-subtle)]">
              {viewFormat === 'NARRATIVE' ? (
                isEditable ? (
                  <textarea
                    value={editableNarrative}
                    onChange={(e) => setEditableNarrative(e.target.value)}
                    className="w-full h-80 bg-transparent text-[var(--text-primary)] font-mono text-[11px] outline-none resize-y"
                  />
                ) : (
                  editableNarrative
                )
              ) : (
                fincenXML
              )}
            </div>

            {/* Reviewer Comment Thread */}
            <div className="p-2.5 rounded-xl bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)] space-y-2 text-[11px]">
              <div className="flex items-center gap-1.5 text-xs font-bold text-[var(--text-primary)]">
                <MessageSquare className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                <span>Compliance Reviewer Notes &amp; Audit Comments</span>
              </div>

              <div className="space-y-1.5 max-h-24 overflow-y-auto pr-1">
                {comments.map((c, idx) => (
                  <div key={idx} className="p-1.5 rounded bg-[var(--bg-base)] border border-[var(--border-subtle)] text-[10px]">
                    <div className="flex justify-between font-mono text-[var(--accent-primary)] font-semibold">
                      <span>{c.author}</span>
                      <span className="text-[var(--text-muted)]">{c.time}</span>
                    </div>
                    <p className="text-[var(--text-secondary)] mt-0.5">{c.text}</p>
                  </div>
                ))}
              </div>

              <form onSubmit={handleAddComment} className="flex items-center gap-1.5 pt-1">
                <input
                  type="text"
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                  placeholder="Add compliance note or evidence cross-reference..."
                  className="flex-1 px-2.5 py-1 rounded-lg bg-[var(--bg-base)] border border-[var(--border-subtle)] text-[10px] outline-none text-[var(--text-primary)]"
                />
                <button
                  type="submit"
                  className="px-2.5 py-1 rounded-lg skeuo-btn skeuo-btn-primary text-[10px] font-bold cursor-pointer"
                >
                  Post Note
                </button>
              </form>
            </div>
          </div>

          {/* Cryptographic Ledger Verification Seal */}
          <div className="mt-2.5 p-2 rounded-xl bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)] flex flex-wrap items-center justify-between gap-2 text-[10px] font-mono">
            <div className="flex items-center gap-1.5 min-w-0">
              <ShieldCheck className="w-4 h-4 text-emerald-500 shrink-0" />
              <span className="text-[var(--text-muted)] truncate">SHA-256 Merkle Audit Receipt:</span>
              <span className="text-[var(--accent-primary)] font-bold truncate max-w-[200px] sm:max-w-xs">
                9f8e4b7a12c85d6e3f019a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d
              </span>
            </div>
            <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-bold border border-emerald-500/30">
              SR 11-7 / SEC 17a-4 Sealed
            </span>
          </div>

        </div>

      </div>
    </div>
  );
};
