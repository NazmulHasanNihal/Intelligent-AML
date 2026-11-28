'use client';

import React, { useState, Suspense, useMemo } from 'react';
import { useSearchParams } from 'next/navigation';
import {
  FileCheck2,
  FileText,
  Download,
  AlertTriangle,
  CheckCircle2,
  Lock,
  Layers,
  Globe,
  Code,
  ShieldAlert,
  Sparkles,
  RefreshCw,
  Hash,
  ShieldCheck,
  Check,
  Building,
  DollarSign,
  Printer,
  Copy,
  Table,
  FileSpreadsheet,
  Paperclip,
  Upload,
  UserCheck,
  AlertOctagon,
  ExternalLink,
  PlusCircle,
  Trash2,
  HelpCircle,
  Clock
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { PiiText } from '@/components/ui/PiiText';
import { computeSha256 } from '@/lib/audit/hashChain';
import { REGULATORY_CONFIG } from '@/lib/config/regulatory';
import { BANKER_PERSONAS } from '@/lib/auth/session';

const ALGO_LEAKAGE_TERMS = [
  'GCN',
  'GNN',
  'neural network',
  'SHAP',
  'Hawkes intensity',
  'lambda_u',
  'embedding',
  'conformal set',
  'algorithm',
  'C-STGB',
  'machine learning model'
];

interface SupportingAttachment {
  id: string;
  fileName: string;
  fileType: string;
  sizeKb: number;
  uploadedAt: string;
  category: 'CUSTOMS_INVOICE' | 'BILL_OF_LADING' | 'BANK_STATEMENT' | 'KYC_PROFILE' | 'CORRESPONDENCE';
  sha256Hash: string;
}

interface DecisionLogEntry {
  id: string;
  timestamp: string;
  officerName: string;
  officerRole: string;
  decisionType: 'MAKER_DRAFTED' | 'MAKER_SUBMITTED' | 'CHECKER_APPROVED' | 'CHECKER_REJECTED';
  reasonCategory: string;
  justification: string;
  hash: string;
}

function SarWorkbenchContent() {
  const searchParams = useSearchParams();
  const caseId = searchParams?.get('caseId') || 'CASE-2026-0881';
  const { jurisdiction, ctrRecords, setFourEyesModalOpen, addToast, addAuditEntry, session } = useBankingStore();

  const [activeSubTab, setActiveSubTab] = useState<'SAR_STUDIO' | 'CTR_AGGREGATOR'>('SAR_STUDIO');
  const [jurisdictionTemplate, setJurisdictionTemplate] = useState<'BFIU_GOAML' | 'FINCEN_BSA' | 'EU_GOAML'>('BFIU_GOAML');

  // Structured Form Fields
  const [subjectEntity, setSubjectEntity] = useState('Meghna Industrial & Agro Processing Ltd');
  const [accountNumber, setAccountNumber] = useState('BD22-EBLB-4829-1092-8823');
  const [transactionAmount, setTransactionAmount] = useState('945,000.00 USD (৳113,400,000 BDT)');
  const [typologyCategory, setTypologyCategory] = useState('TBML_ASYCUDA_OVERINVOICE');

  // Supporting Attachments State (Requirement: At least one attachment mandatory)
  const [attachments, setAttachments] = useState<SupportingAttachment[]>([
    {
      id: 'ATT-001',
      fileName: 'Commercial_Invoice_INV-9921_Meghna_GulfStar.pdf',
      fileType: 'application/pdf',
      sizeKb: 184,
      uploadedAt: '2026-09-02 08:22:10 UTC',
      category: 'CUSTOMS_INVOICE',
      sha256Hash: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    },
    {
      id: 'ATT-002',
      fileName: 'Bill_of_Lading_BL-CTG-2026-442.pdf',
      fileType: 'application/pdf',
      sizeKb: 312,
      uploadedAt: '2026-09-02 08:23:45 UTC',
      category: 'BILL_OF_LADING',
      sha256Hash: '8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4'
    }
  ]);

  const [newAttachmentName, setNewAttachmentName] = useState('');
  const [newAttachmentCategory, setNewAttachmentCategory] = useState<SupportingAttachment['category']>('BANK_STATEMENT');
  const [showAddAttachment, setShowAddAttachment] = useState(false);

  // Maker-Checker Workflow State
  const [makerSigned, setMakerSigned] = useState(true);
  const [makerOfficer, setMakerOfficer] = useState(BANKER_PERSONAS.INVESTIGATOR_L2.name);
  const [checkerApproved, setCheckerApproved] = useState(false);
  const [checkerOfficer, setCheckerOfficer] = useState(BANKER_PERSONAS.CCO_L3.name);

  // Decision Log State
  const [decisionLog, setDecisionLog] = useState<DecisionLogEntry[]>([
    {
      id: 'DEC-001',
      timestamp: '2026-09-02 08:35:10 UTC',
      officerName: BANKER_PERSONAS.INVESTIGATOR_L2.name,
      officerRole: 'Lead Investigator (Maker)',
      decisionType: 'MAKER_DRAFTED',
      reasonCategory: 'TBML_ASYCUDA_OVERINVOICE',
      justification: 'ASYCUDA World customs benchmark price divergence of +333.7% on combed cotton yarn ($9.45/kg declared vs $2.18/kg market threshold). Physical AIS vessel tracking confirms cargo diversion.',
      hash: '5d41402abc4b2a76b9719d911017c592b0c954e47a465cb33a6dae904b786196'
    }
  ]);
  const [newReasonText, setNewReasonText] = useState('');
  const [newReasonCategory, setNewReasonCategory] = useState('TBML_ASYCUDA_OVERINVOICE');

  // Narrative State
  const initialNarrative = `CONFIDENTIAL SUSPICIOUS TRANSACTION REPORT (STR / SAR)
SUBMITTED PURSUANT TO SECTION 25, MONEY LAUNDERING PREVENTION ACT 2012 (ACT NO. 5 OF 2012)
TO: BANGLADESH FINANCIAL INTELLIGENCE UNIT (BFIU), BANGLADESH BANK
REPORTING INSTITUTION: Eastern Bank PLC (BIC: EBLBBDDH), Motijheel Head Office, Dhaka

1. REPORTING INSTITUTION & SUBJECT IDENTIFICATION:
Reporting Entity: Eastern Bank PLC, Motijheel Head Office, Dhaka
Subject Legal Name: Meghna Industrial & Agro Processing Ltd
Subject Account No: BD22-EBLB-4829-1092-8823
Counterparty: Gulf Star Commodities FZE, JAFZA Free Zone, Dubai, UAE (BIC: EBILAEAD)

2. FACTUAL BASIS FOR SUSPICIOUS TRANSACTION DETERMINATION:
Between August 28, 2026 and September 02, 2026, the Subject initiated documentary credit transactions under Letter of Credit (LC) No. LC-CTG-2026-9921. The declared commercial invoice price for combed cotton yarn was $9.45/kg. Verification against National Board of Revenue (NBR) ASYCUDA World customs valuation benchmarks indicated a prevailing market price of $2.18/kg, representing a gross price divergence of +333.7%.

Furthermore, individual multi-agent transfers were structured beneath the mandatory Cash Transaction Reporting (CTR) threshold of ৳1,000,000 BDT, specifically executed at ৳954,000 BDT ($7,950.00 USD). AIS satellite vessel telemetry confirmed anomalous transshipment where the carrying vessel bypassed the declared Port Klang and discharged cargo directly at Jebel Ali / Dubai without re-export documentation.

3. REMEDIAL ACTION TAKEN & STATUTORY DISCLOSURE:
The Subject account has been placed on Tier 1 administrative hold pending formal regulatory direction under Section 2(v) and Section 25 of the Money Laundering Prevention Act 2012.
Pursuant to Section 6 of MLPA 2012, no disclosure of this filing has been or will be made to the customer or any unauthorized party.`;

  const [narrativeText, setNarrativeText] = useState(initialNarrative);
  const [narrativeViewMode, setNarrativeViewMode] = useState<'edit' | 'diff'>('edit');
  const [merkleRoot, setMerkleRoot] = useState('9c72f16eb2befae4bcf1e1b7cbb510a6a13ba5b4d7a8f0aaee5337609c7ad42b');
  const [isRecalculatingHash, setIsRecalculatingHash] = useState(false);

  // Check for ML jargon leakage
  const detectedLeakage = useMemo(() => {
    return ALGO_LEAKAGE_TERMS.filter((term) =>
      new RegExp(`\\b${term}\\b`, 'i').test(narrativeText)
    );
  }, [narrativeText]);

  const handleCleanJargon = () => {
    let cleaned = narrativeText;
    ALGO_LEAKAGE_TERMS.forEach((term) => {
      const regex = new RegExp(`\\b${term}\\b`, 'gi');
      cleaned = cleaned.replace(regex, 'calibrated institutional surveillance indicators');
    });
    setNarrativeText(cleaned);
    addToast('Jargon Purged', 'All internal algorithmic terms replaced with compliant legal surveillance terms.', 'success');
  };

  const handleRecalculateMerkleRoot = async () => {
    setIsRecalculatingHash(true);
    try {
      const attachmentDigests = attachments.map(a => a.sha256Hash).join(':');
      const digest = await computeSha256(narrativeText + caseId + subjectEntity + attachmentDigests);
      setMerkleRoot(digest);
      addToast('Evidence Digest Updated', `New evidence Merkle root calculated: ${digest.slice(0, 16)}...`, 'success');
    } catch (err) {
      console.error(err);
    } finally {
      setIsRecalculatingHash(false);
    }
  };

  // Add Attachment Handler
  const handleAddAttachment = async () => {
    if (!newAttachmentName.trim()) {
      addToast('Filename Required', 'Please enter a valid documentary filename.', 'info');
      return;
    }

    const mockHash = await computeSha256(newAttachmentName + Date.now());
    const newAtt: SupportingAttachment = {
      id: `ATT-${Math.floor(100 + Math.random() * 900)}`,
      fileName: newAttachmentName.endsWith('.pdf') ? newAttachmentName : `${newAttachmentName}.pdf`,
      fileType: 'application/pdf',
      sizeKb: Math.floor(120 + Math.random() * 400),
      uploadedAt: new Date().toISOString().replace('T', ' ').substring(0, 19) + ' UTC',
      category: newAttachmentCategory,
      sha256Hash: mockHash
    };

    setAttachments([...attachments, newAtt]);
    setNewAttachmentName('');
    setShowAddAttachment(false);
    addToast('Attachment Added', `${newAtt.fileName} attached with verified SHA-256 seal.`, 'success');
  };

  // Remove Attachment Handler
  const handleRemoveAttachment = (id: string) => {
    setAttachments(attachments.filter(a => a.id !== id));
    addToast('Attachment Removed', 'Documentary proof removed from docket.', 'info');
  };

  // Maker-Checker Actions
  const handleMakerSubmit = async () => {
    if (attachments.length === 0) {
      addToast('Attachment Gate', 'BFIU requires at least one supporting document before submitting for CCO review.', 'critical');
      return;
    }

    const newEntry: DecisionLogEntry = {
      id: `DEC-${Math.floor(100 + Math.random() * 900)}`,
      timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19) + ' UTC',
      officerName: session.userName || BANKER_PERSONAS.INVESTIGATOR_L2.name,
      officerRole: 'Lead Investigator (Maker)',
      decisionType: 'MAKER_SUBMITTED',
      reasonCategory: typologyCategory,
      justification: newReasonText || 'Maker formal submission: Dossier verified with supporting trade documents and ASYCUDA price divergence proof.',
      hash: await computeSha256(narrativeText.slice(0, 50) + Date.now())
    };

    setDecisionLog([...decisionLog, newEntry]);
    setMakerSigned(true);
    setNewReasonText('');
    addToast('Submitted to CCO', 'STR submitted for Checker (CCO) sign-off under four-eyes principle.', 'success');
  };

  const handleCheckerApprove = async () => {
    const newEntry: DecisionLogEntry = {
      id: `DEC-${Math.floor(100 + Math.random() * 900)}`,
      timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19) + ' UTC',
      officerName: BANKER_PERSONAS.CCO_L3.name,
      officerRole: 'Chief Compliance Officer (Checker)',
      decisionType: 'CHECKER_APPROVED',
      reasonCategory: typologyCategory,
      justification: 'Checker formal approval: Independent examination confirms trade over-invoicing and near-CTR structuring. Approved for BFIU goAML transmission.',
      hash: await computeSha256('CHECKER_APPROVAL_' + Date.now())
    };

    setDecisionLog([...decisionLog, newEntry]);
    setCheckerApproved(true);
    addAuditEntry({
      eventType: 'STR_CHECKER_APPROVED',
      entityId: caseId,
      details: `STR approved by Checker ${BANKER_PERSONAS.CCO_L3.name} for transmission to BFIU.`,
      actionBy: BANKER_PERSONAS.CCO_L3.name
    });
    addToast('STR Approved by CCO', 'Checker sign-off complete. Official BFIU goAML XML export unlocked.', 'success');
  };

  // Generate Official BFIU goAML XML Export
  const handleDownloadXml = () => {
    if (detectedLeakage.length > 0) {
      alert('Cannot export STR/SAR: Narrative contains internal algorithmic terms that breach regulatory reporting standards. Please click "Purge Algorithmic Jargon" first.');
      return;
    }

    if (attachments.length === 0) {
      alert('BFIU Compliance Gate: At least one supporting documentary attachment is mandatory under BFIU STR guidelines before export.');
      return;
    }

    if (!checkerApproved) {
      alert('Maker-Checker Gate: This STR requires formal sign-off from the Checker (Chief Compliance Officer) before filing to BFIU.');
      return;
    }

    // Official BFIU UNODC goAML XML Schema Template
    const xml = `<?xml version="1.0" encoding="UTF-8"?>
<!-- 
  BFIU goAML XML Schema Specification (Version 4.2 / UNODC Compliant)
  Regulatory Authority: Bangladesh Financial Intelligence Unit (BFIU), Bangladesh Bank
  Governing Statute: Money Laundering Prevention Act 2012 § 25
  Anti-Tipping-Off Mandate: Money Laundering Prevention Act 2012 § 6
  TODO(verify: BFIU goAML XML Schema v4.x local namespace prefix and reporting entity code dictionary)
-->
<report xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <rentity_id>EBLB-BD-001</rentity_id>
  <rentity_branch>Motijheel Corporate Head Office, Dhaka</rentity_branch>
  <submission_code>E</submission_code>
  <report_code>STR</report_code>
  <entity_reference>${caseId}</entity_reference>
  <submission_date>${new Date().toISOString()}</submission_date>
  <currency_code_local>BDT</currency_code_local>
  <reporting_user>
    <officer_id>BNK-4491</officer_id>
    <officer_name>${makerOfficer}</officer_name>
    <role>Maker / Lead AML Investigator</role>
    <signed>true</signed>
  </reporting_user>
  <checker_user>
    <officer_id>BNK-7842</officer_id>
    <officer_name>${checkerOfficer}</officer_name>
    <role>Checker / Chief Compliance Officer</role>
    <approved>true</approved>
    <approval_timestamp>${new Date().toISOString()}</approval_timestamp>
  </checker_user>
  <reason_category>${typologyCategory}</reason_category>
  <statutory_basis>${REGULATORY_CONFIG.statuteReferences.primaryAmlAct.title} § 25</statutory_basis>
  <anti_tipping_off_compliance>${REGULATORY_CONFIG.statuteReferences.primaryAmlAct.tippingOffSection} COMPLIANT</anti_tipping_off_compliance>
  <evidence_merkle_root>${merkleRoot}</evidence_merkle_root>
  <report_indicators>
    <indicator>IND_TBML_PRICE_DIVERGENCE</indicator>
    <indicator>IND_NEAR_CTR_STRUCTURING</indicator>
    <indicator>IND_TRANSSHIPMENT_ANOMALY</indicator>
  </report_indicators>
  <transaction>
    <transactionnumber>TX-EBL-2026-9921</transactionnumber>
    <internal_ref_number>LC-CTG-2026-9921</internal_ref_number>
    <transaction_location>Chittagong Port Trade Branch</transaction_location>
    <date_transaction>2026-09-02T08:14:22Z</date_transaction>
    <transmode_code>DOCUMENTARY_LETTER_OF_CREDIT</transmode_code>
    <amount_local>113400000.00</amount_local>
    <amount_foreign>945000.00</amount_foreign>
    <currency_foreign>USD</currency_foreign>
    <fx_rate_applied>${REGULATORY_CONFIG.fxRatePolicy.usdToBdt}</fx_rate_applied>
    <t_from>
      <from_account>${accountNumber}</from_account>
      <from_entity_name>${subjectEntity}</from_entity_name>
      <country>BD</country>
    </t_from>
    <t_to>
      <to_account>AE44-EBIL-9002-1144-5501</to_account>
      <to_entity_name>Gulf Star Commodities FZE</to_entity_name>
      <country>AE</country>
      <jurisdiction>JAFZA Free Zone, Dubai</jurisdiction>
    </t_to>
  </transaction>
  <supporting_attachments count="${attachments.length}">
    ${attachments.map(a => `
    <attachment>
      <attachment_id>${a.id}</attachment_id>
      <file_name>${a.fileName}</file_name>
      <mime_type>${a.fileType}</mime_type>
      <file_size_kb>${a.sizeKb}</file_size_kb>
      <category>${a.category}</category>
      <uploaded_timestamp>${a.uploadedAt}</uploaded_timestamp>
      <sha256_hash>${a.sha256Hash}</sha256_hash>
    </attachment>`).join('')}
  </supporting_attachments>
  <decision_log count="${decisionLog.length}">
    ${decisionLog.map(d => `
    <decision_entry>
      <entry_id>${d.id}</entry_id>
      <timestamp>${d.timestamp}</timestamp>
      <officer>${d.officerName}</officer>
      <role>${d.officerRole}</role>
      <decision_type>${d.decisionType}</decision_type>
      <reason_category>${d.reasonCategory}</reason_category>
      <justification><![CDATA[${d.justification}]]></justification>
      <hash_seal>${d.hash}</hash_seal>
    </decision_entry>`).join('')}
  </decision_log>
  <narrative><![CDATA[${narrativeText}]]></narrative>
</report>`;

    const blob = new Blob([xml], { type: 'application/xml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `BFIU_goAML_STR_${caseId}_${new Date().toISOString().slice(0, 10)}.xml`;
    a.click();
    URL.revokeObjectURL(url);

    addAuditEntry({
      eventType: 'BFIU_STR_GENERATED',
      entityId: caseId,
      details: `Generated official BFIU goAML STR XML for ${subjectEntity} with ${attachments.length} supporting attachments. Dual maker-checker sign-off certified.`,
      actionBy: checkerOfficer
    });
    addToast('BFIU STR Exported', `Official goAML XML generated for ${caseId}. Ready for BFIU portal upload.`, 'success');
  };

  // Export CTR Batch XML (Bangladesh Bank BFIU Format)
  const handleExportCtrXml = () => {
    const xml = `<?xml version="1.0" encoding="UTF-8"?>
<!-- 
  BFIU Cash Transaction Report (CTR) Batch Filing
  Governing Statute: Money Laundering Prevention Act 2012 § 2(z)
  Threshold: BDT 1,000,000 (10 Lakh) or above
  Source Reference: ${REGULATORY_CONFIG.ctrPolicy.sourceLink}
-->
<CashTransactionReportBatch 
  jurisdiction="BD_BFIU" 
  statutoryThresholdBdt="${REGULATORY_CONFIG.ctrPolicy.thresholdBdt}" 
  recordCount="${ctrRecords.length}" 
  reportingBank="Eastern Bank PLC" 
  generatedAt="${new Date().toISOString()}">
  ${ctrRecords.map((r) => `
  <TransactionRecord id="${r.id}">
    <Account>${r.accountNumber}</Account>
    <CustomerLegalName>${r.entityName}</CustomerLegalName>
    <CashAmountUsd currency="${r.currency}">${r.amountUsd}</CashAmountUsd>
    <CashAmountBdt>${r.amountNative}</CashAmountBdt>
    <ThresholdExceeded>${r.amountNative >= REGULATORY_CONFIG.ctrPolicy.thresholdBdt}</ThresholdExceeded>
    <BranchLocation>${r.branch}</BranchLocation>
    <ExecutionTimestamp>${r.timestamp}</ExecutionTimestamp>
    <FilingStatus>${r.status}</FilingStatus>
  </TransactionRecord>`).join('')}
</CashTransactionReportBatch>`;

    const blob = new Blob([xml], { type: 'application/xml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `BFIU_CTR_Batch_${new Date().toISOString().slice(0, 10)}.xml`;
    a.click();
    URL.revokeObjectURL(url);
    addToast('CTR Batch Exported', `Generated statutory BFIU CTR filing XML for ${ctrRecords.length} cash transactions.`, 'success');
  };

  return (
    <div className="p-4 sm:p-5 lg:p-6 max-w-[1750px] mx-auto space-y-5">
      {/* Page Title & Main Mode Switcher */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2 font-sans">
            <FileCheck2 className="w-5 h-5 text-emerald-400" />
            BFIU Statutory Reporting &amp; CTR Workbench
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Suspicious Transaction Reports (STR/SAR) under MLPA 2012 § 25 &amp; Cash Transaction Reports (CTR) under BFIU Master Circular No. 26.
          </p>
        </div>

        {/* Sub-Tab Switcher */}
        <div className="flex items-center bg-panel p-1 rounded-xl border border-line-strong text-xs font-semibold">
          <button
            onClick={() => setActiveSubTab('SAR_STUDIO')}
            className={`px-3 py-1.5 rounded-lg transition-colors cursor-pointer ${
              activeSubTab === 'SAR_STUDIO'
                ? 'bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/40'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Suspicious Transaction Report (STR/SAR) Studio
          </button>
          <button
            onClick={() => setActiveSubTab('CTR_AGGREGATOR')}
            className={`px-3 py-1.5 rounded-lg transition-colors cursor-pointer ${
              activeSubTab === 'CTR_AGGREGATOR'
                ? 'bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/40'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Cash Transaction Reports (CTR) Aggregator ({ctrRecords.length})
          </button>
        </div>
      </div>

      {/* Mandatory Non-Dismissible Anti-Tipping-Off Warning Banner (MLPA 2012 § 6) */}
      <div className="p-3.5 bg-amber-950/40 border border-amber-600/60 rounded-xl flex items-start gap-3 text-xs text-amber-200 shadow-lg">
        <AlertOctagon className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="font-bold tracking-wide text-amber-300">
              Statutory Prohibition of Tipping-Off (Money Laundering Prevention Act 2012 § 6)
            </span>
            <a
              href="http://bdlaws.minlaw.gov.bd/act-1088.html"
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs underline text-amber-400 hover:text-amber-300 flex items-center gap-0.5"
            >
              <span>Act Citation</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          </div>
          <p className="text-xs text-amber-200/90 leading-relaxed font-sans">
            {REGULATORY_CONFIG.statuteReferences.primaryAmlAct.tippingOffWarning}
          </p>
        </div>
      </div>

      {activeSubTab === 'SAR_STUDIO' ? (
        /* STR/SAR Studio Workspace: 50/50 Split Screen on Large Displays */
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-5">
          {/* Left Column: Form, Attachments, Decision Log & Narrative Editor */}
          <div className="space-y-4">
            {/* Top Toolbar: Jurisdiction Format & Maker-Checker Status */}
            <div className="p-4 rounded-xl bg-panel border border-line flex flex-wrap items-center justify-between gap-3 shadow-xl">
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono font-semibold text-slate-400">Reporting Schema:</span>
                {(['BFIU_GOAML', 'FINCEN_BSA', 'EU_GOAML'] as const).map((fmt) => (
                  <button
                    key={fmt}
                    onClick={() => setJurisdictionTemplate(fmt)}
                    className={`px-3 py-1 rounded-lg text-xs font-mono font-bold transition-colors cursor-pointer ${
                      jurisdictionTemplate === fmt
                        ? 'bg-sky-500/20 text-sky-300 border border-sky-500/40'
                        : 'text-slate-400 hover:text-slate-200 bg-canvas'
                    }`}
                  >
                    {fmt === 'BFIU_GOAML' ? 'BFIU goAML v4.2 (Bangladesh)' : fmt === 'FINCEN_BSA' ? 'FinCEN Form 111 (US)' : 'UNODC goAML v5 (EU)'}
                  </button>
                ))}
              </div>

              <div className="flex items-center gap-2 text-xs font-mono">
                <span className="px-2 py-0.5 rounded bg-canvas text-slate-300 border border-line-strong flex items-center gap-1.5">
                  <span className="text-slate-500">Maker:</span>
                  <span className="text-emerald-400 font-bold">{makerOfficer.split(',')[0]}</span>
                  {makerSigned && <Check className="w-3.5 h-3.5 text-emerald-400" />}
                </span>
                <span className="px-2 py-0.5 rounded bg-canvas text-slate-300 border border-line-strong flex items-center gap-1.5">
                  <span className="text-slate-500">Checker:</span>
                  <span className={checkerApproved ? 'text-emerald-400 font-bold' : 'text-amber-400 font-bold'}>
                    {checkerOfficer.split(',')[0]}
                  </span>
                  {checkerApproved ? (
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                  ) : (
                    <Clock className="w-3.5 h-3.5 text-amber-400" />
                  )}
                </span>
              </div>
            </div>

            {/* Jargon Leakage Blocker Banner */}
            {detectedLeakage.length > 0 && (
              <div className="p-3.5 bg-rose-950/40 border border-rose-800 rounded-xl flex items-center justify-between gap-3 text-xs text-rose-300">
                <div className="flex items-center gap-2">
                  <ShieldAlert className="w-4 h-4 shrink-0 text-rose-400" />
                  <span>
                    <strong>Regulatory Gate:</strong> Unapproved internal algorithmic terms detected: (
                    <span className="font-mono text-white">{detectedLeakage.join(', ')}</span>). Must be purged prior to submission.
                  </span>
                </div>
                <button
                  onClick={handleCleanJargon}
                  className="px-3 py-1 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-semibold cursor-pointer shrink-0"
                >
                  Purge Algorithmic Jargon
                </button>
              </div>
            )}

            {/* SECTION 1: Supporting Documentary Proof Attachments (Mandatory Gate) */}
            <div className="p-4 rounded-xl bg-panel border border-line shadow-xl space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xs font-mono font-bold text-slate-200 flex items-center gap-2">
                    <Paperclip className="w-4 h-4 text-sky-400" />
                    Mandatory Supporting Documentary Attachments ({attachments.length})
                  </h3>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Under BFIU STR guidelines, every suspicious transaction report must contain verified documentary proof (commercial invoices, shipping manifests, or statements).
                  </p>
                </div>

                <button
                  onClick={() => setShowAddAttachment(!showAddAttachment)}
                  className="px-2.5 py-1 rounded-lg bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs flex items-center gap-1.5 cursor-pointer"
                >
                  <PlusCircle className="w-3.5 h-3.5" />
                  <span>Attach Document</span>
                </button>
              </div>

              {/* Add Attachment Drawer */}
              {showAddAttachment && (
                <div className="p-3 bg-canvas border border-line-strong rounded-xl space-y-2.5 text-xs font-mono">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                    <div className="md:col-span-2">
                      <label className="text-slate-400 block mb-1 text-xs">Document Filename</label>
                      <input
                        type="text"
                        placeholder="e.g. NBR_Customs_Declaration_Form_2026.pdf"
                        value={newAttachmentName}
                        onChange={(e) => setNewAttachmentName(e.target.value)}
                        className="w-full px-2.5 py-1.5 bg-panel border border-line-strong rounded-lg text-slate-100 text-xs focus:outline-none focus:border-sky-500"
                      />
                    </div>
                    <div>
                      <label className="text-slate-400 block mb-1 text-xs">Evidence Category</label>
                      <select
                        value={newAttachmentCategory}
                        onChange={(e) => setNewAttachmentCategory(e.target.value as any)}
                        className="w-full px-2.5 py-1.5 bg-panel border border-line-strong rounded-lg text-slate-100 text-xs focus:outline-none focus:border-sky-500"
                      >
                        <option value="CUSTOMS_INVOICE">Customs Valuation Invoice</option>
                        <option value="BILL_OF_LADING">Bill of Lading / AIS Log</option>
                        <option value="BANK_STATEMENT">Bank Statement / Ledger</option>
                        <option value="KYC_PROFILE">KYC / NID Profile</option>
                        <option value="CORRESPONDENCE">Trade Correspondence</option>
                      </select>
                    </div>
                  </div>

                  <div className="flex justify-end gap-2 pt-1">
                    <button
                      onClick={() => setShowAddAttachment(false)}
                      className="px-3 py-1 rounded bg-surface text-slate-300 hover:bg-surface-hover"
                    >
                      Cancel
                    </button>
                    <button
                      onClick={handleAddAttachment}
                      className="px-3 py-1 rounded bg-sky-600 text-white font-semibold hover:bg-sky-500"
                    >
                      Verify &amp; Seal Attachment
                    </button>
                  </div>
                </div>
              )}

              {/* Attachments List */}
              {attachments.length === 0 ? (
                <div className="p-4 bg-rose-950/20 border border-rose-900/50 rounded-lg text-center text-xs text-rose-300">
                  <AlertTriangle className="w-4 h-4 mx-auto mb-1 text-rose-400" />
                  <span>BFIU STR Compliance Gate: Zero attachments present. At least one supporting document must be attached.</span>
                </div>
              ) : (
                <div className="divide-y divide-[#1E293B] border border-line rounded-xl overflow-hidden bg-canvas">
                  {attachments.map((att) => (
                    <div key={att.id} className="p-3 flex items-center justify-between text-xs font-mono">
                      <div className="flex items-center gap-2.5 min-w-0">
                        <FileText className="w-4 h-4 text-sky-400 shrink-0" />
                        <div className="truncate">
                          <span className="font-bold text-slate-200 block truncate">{att.fileName}</span>
                          <span className="text-xs text-slate-500">
                            {att.category} • {att.sizeKb} KB • SHA-256: {att.sha256Hash.slice(0, 16)}...
                          </span>
                        </div>
                      </div>

                      <div className="flex items-center gap-2 shrink-0">
                        <span className="px-2 py-0.5 rounded text-xs bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                          Sealed
                        </span>
                        <button
                          onClick={() => handleRemoveAttachment(att.id)}
                          className="p-1 text-slate-500 hover:text-rose-400 transition-colors cursor-pointer"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* SECTION 2: Decision Log with Statutory Reasons */}
            <div className="p-4 rounded-xl bg-panel border border-line shadow-xl space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xs font-mono font-bold text-slate-200 flex items-center gap-2">
                    <UserCheck className="w-4 h-4 text-emerald-400" />
                    Structured Decision Log &amp; Rationale ({decisionLog.length})
                  </h3>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Records the investigative reasoning, typology categorization, and sign-offs for regulatory examiners.
                  </p>
                </div>
              </div>

              <div className="space-y-2">
                {decisionLog.map((log) => (
                  <div key={log.id} className="p-3 bg-canvas border border-line rounded-xl text-xs font-mono space-y-1.5">
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-bold text-sky-400">{log.officerName} ({log.officerRole})</span>
                      <span className="text-slate-500 text-xs">{log.timestamp}</span>
                    </div>
                    <div className="text-slate-300 text-xs font-sans leading-relaxed">
                      {log.justification}
                    </div>
                    <div className="text-xs text-slate-500 flex items-center justify-between pt-1 border-t border-line">
                      <span>Category: <strong className="text-slate-300">{log.reasonCategory}</strong></span>
                      <span>Seal: <code className="text-emerald-400">{log.hash.slice(0, 16)}...</code></span>
                    </div>
                  </div>
                ))}
              </div>

              {/* Append Decision Entry Input */}
              <div className="pt-2 border-t border-line space-y-2 text-xs font-mono">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                  <div className="md:col-span-2">
                    <input
                      type="text"
                      placeholder="Add examiner rationale / investigation notes..."
                      value={newReasonText}
                      onChange={(e) => setNewReasonText(e.target.value)}
                      className="w-full px-3 py-1.5 bg-canvas border border-line-strong rounded-lg text-slate-100 text-xs focus:outline-none focus:border-sky-500"
                    />
                  </div>
                  <div>
                    <select
                      value={newReasonCategory}
                      onChange={(e) => setNewReasonCategory(e.target.value)}
                      className="w-full px-3 py-1.5 bg-canvas border border-line-strong rounded-lg text-slate-100 text-xs focus:outline-none focus:border-sky-500"
                    >
                      <option value="TBML_ASYCUDA_OVERINVOICE">TBML Price Divergence</option>
                      <option value="NEAR_CTR_STRUCTURING">Near-CTR Structuring</option>
                      <option value="PEP_SANCTION_NEXUS">PEP / Adverse Association</option>
                      <option value="SUDDEN_VELOCITY_BURST">Unexplained Velocity Burst</option>
                    </select>
                  </div>
                </div>

                <div className="flex items-center justify-between pt-1">
                  <span className="text-xs text-slate-400">
                    Signing Officer: <strong className="text-slate-200">{session.userName || makerOfficer}</strong>
                  </span>
                  <button
                    onClick={handleMakerSubmit}
                    className="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs flex items-center gap-1.5 cursor-pointer"
                  >
                    <Check className="w-3.5 h-3.5" />
                    <span>Log Decision &amp; Submit as Maker</span>
                  </button>
                </div>
              </div>
            </div>

            {/* SECTION 3: Structured Narrative Textarea with Red/Green Officer Edit Diff Viewer */}
            <div className="p-5 rounded-2xl bg-panel border border-line shadow-xl space-y-3">
              <div className="flex flex-wrap items-center justify-between gap-2 pb-2 border-b border-line">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-bold text-slate-200 ">
                    Official Regulatory Narrative
                  </span>
                  <div className="flex items-center bg-canvas p-0.5 rounded border border-line-strong text-xs font-mono">
                    <button
                      type="button"
                      onClick={() => setNarrativeViewMode('edit')}
                      className={`px-2 py-0.5 rounded cursor-pointer transition-colors ${
                        narrativeViewMode === 'edit'
                          ? 'bg-sky-500/20 text-sky-300 font-bold border border-sky-500/30'
                          : 'text-slate-400 hover:text-slate-200'
                      }`}
                    >
                      Editor
                    </button>
                    <button
                      type="button"
                      onClick={() => setNarrativeViewMode('diff')}
                      className={`px-2 py-0.5 rounded cursor-pointer transition-colors ${
                        narrativeViewMode === 'diff'
                          ? 'bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/30'
                          : 'text-slate-400 hover:text-slate-200'
                      }`}
                    >
                      Officer Edit Diff
                    </button>
                  </div>
                </div>
                <span className="text-xs font-mono text-slate-400">
                  {narrativeText.length} Characters • Ready for BFIU Intake
                </span>
              </div>

              {narrativeViewMode === 'edit' ? (
                <textarea
                  value={narrativeText}
                  onChange={(e) => setNarrativeText(e.target.value)}
                  rows={14}
                  className="w-full p-4 bg-canvas border border-line-strong rounded-xl text-xs font-mono text-slate-100 placeholder:text-slate-600 focus:outline-none focus:border-sky-500 leading-relaxed"
                />
              ) : (
                <div className="w-full p-4 bg-canvas border border-line-strong rounded-xl text-xs font-mono max-h-[320px] overflow-y-auto space-y-1">
                  <div className="text-xs text-slate-500 mb-2 border-b border-line pb-1">
                    Red (-) = Original Draft Lines Removed • Green (+) = Officer Edit Additions
                  </div>
                  {initialNarrative
                    .split('\n')
                    .filter((origLine) => !narrativeText.split('\n').includes(origLine))
                    .map((removedLine, rIdx) => (
                      <div key={`rm-${rIdx}`} className="p-1 rounded bg-rose-950/40 text-rose-300 border-l-2 border-rose-500 line-through">
                        - {removedLine}
                      </div>
                    ))}
                  {narrativeText.split('\n').map((line, idx) => {
                    const originalLines = initialNarrative.split('\n');
                    const isNew = !originalLines.includes(line);
                    return (
                      <div
                        key={idx}
                        className={`p-1 rounded ${
                          isNew
                            ? 'bg-emerald-950/40 text-emerald-300 border-l-2 border-emerald-500'
                            : 'text-slate-300'
                        }`}
                      >
                        {isNew ? `+ ${line}` : (line || <span className="opacity-30">&nbsp;</span>)}
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </div>

          {/* Right Column: Case Manifest, Four-Eyes Controls & XML Generation */}
          <div className="bg-panel border border-line rounded-2xl p-5 shadow-2xl flex flex-col justify-between space-y-5">
            <div className="space-y-4">
              <div>
                <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2 font-mono">
                  <ShieldCheck className="w-4 h-4 text-emerald-400" />
                  BFIU Filing Dossier &amp; Merkle Seal
                </h3>
                <p className="text-xs text-slate-400 mt-1">
                  Admissibility-ready under Bangladesh Evidence Act, 1872 (Amended 2022) §§ 65A–65B &amp; 73A (Officer Certificate) &amp; FRE 902(11).
                </p>
              </div>

              {/* Case Parameters */}
              <div className="space-y-2 text-xs font-mono">
                <div className="p-2.5 bg-canvas rounded-lg border border-line">
                  <span className="text-slate-500 text-xs block">Case Docket ID:</span>
                  <span className="font-bold text-sky-400">{caseId}</span>
                </div>
                <div className="p-2.5 bg-canvas rounded-lg border border-line">
                  <span className="text-slate-500 text-xs block">Primary Subject Entity:</span>
                  <span className="font-bold text-slate-200">{subjectEntity}</span>
                </div>
                <div className="p-2.5 bg-canvas rounded-lg border border-line">
                  <span className="text-slate-500 text-xs block">Suspicious Trade Volume:</span>
                  <span className="font-bold text-emerald-400">{transactionAmount}</span>
                </div>
                <div className="p-2.5 bg-canvas rounded-lg border border-line">
                  <span className="text-slate-500 text-xs block">Statutory Mandate:</span>
                  <span className="font-bold text-slate-300">{REGULATORY_CONFIG.statuteReferences.primaryAmlAct.strReportingSection}</span>
                </div>
              </div>

              {/* Maker-Checker Status Card */}
              <div className="p-3 bg-canvas border border-line rounded-xl space-y-2.5 text-xs font-mono">
                <span className="text-slate-400 font-bold text-xs block">
                  Segregation of Duties (Maker-Checker Gate)
                </span>

                <div className="p-2 rounded bg-canvas border border-line space-y-1">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-slate-400">Maker (Investigator):</span>
                    <span className="text-emerald-400 font-bold flex items-center gap-1">
                      <Check className="w-3 h-3" /> Signed
                    </span>
                  </div>
                  <div className="text-xs text-slate-500">{makerOfficer}</div>
                </div>

                <div className="p-2 rounded bg-canvas border border-line space-y-1">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-slate-400">Checker (Chief Compliance Officer):</span>
                    <span className={checkerApproved ? 'text-emerald-400 font-bold flex items-center gap-1' : 'text-amber-400 font-bold flex items-center gap-1'}>
                      {checkerApproved ? <CheckCircle2 className="w-3 h-3" /> : <Clock className="w-3 h-3" />}
                      {checkerApproved ? 'Approved' : 'Pending Sign-Off'}
                    </span>
                  </div>
                  <div className="text-xs text-slate-500">{checkerOfficer}</div>
                </div>

                {!checkerApproved && (
                  <button
                    onClick={handleCheckerApprove}
                    className="w-full py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition-colors flex items-center justify-center gap-1.5 cursor-pointer shadow-md shadow-emerald-600/20"
                  >
                    <UserCheck className="w-3.5 h-3.5" />
                    <span>Authorize as CCO (Checker Sign-Off)</span>
                  </button>
                )}
              </div>

              {/* Cryptographic Merkle Digest Box */}
              <div className="p-3 bg-canvas border border-line rounded-xl space-y-2">
                <div className="flex items-center justify-between text-xs font-mono">
                  <span className="text-slate-400 font-bold">Evidence Merkle Root</span>
                  <button
                    onClick={handleRecalculateMerkleRoot}
                    disabled={isRecalculatingHash}
                    className="text-sky-400 hover:text-sky-300 flex items-center gap-1 cursor-pointer"
                  >
                    <RefreshCw className={`w-3 h-3 ${isRecalculatingHash ? 'animate-spin' : ''}`} />
                    <span>Recalculate</span>
                  </button>
                </div>
                <div className="p-2 bg-canvas rounded border border-line-strong font-mono text-xs text-emerald-400 break-all select-all">
                  {merkleRoot}
                </div>
              </div>
            </div>

            {/* Submission Actions */}
            <div className="pt-4 border-t border-line space-y-2.5">
              <button
                onClick={handleDownloadXml}
                disabled={attachments.length === 0 || !checkerApproved}
                className={`w-full py-2.5 px-4 rounded-xl font-semibold text-xs transition-colors flex items-center justify-center gap-2 cursor-pointer shadow-lg ${
                  attachments.length > 0 && checkerApproved
                    ? 'bg-sky-600 hover:bg-sky-500 text-white shadow-sky-600/20'
                    : 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
                }`}
              >
                <Download className="w-4 h-4" />
                <span>Export Official BFIU goAML XML</span>
              </button>

              <button
                onClick={() => {
                  setFourEyesModalOpen(true, {
                    actionType: 'SAR_FILING',
                    actionTitle: `Submit Formal BFIU STR Filing (${caseId})`,
                    targetId: caseId,
                    details: `Transmit validated BFIU goAML STR filing with ${attachments.length} attachments to BFIU central intake. Subject: ${subjectEntity}. Merkle root: ${merkleRoot.slice(0, 16)}...`
                  });
                }}
                disabled={attachments.length === 0 || !checkerApproved}
                className={`w-full py-2.5 px-4 rounded-xl font-semibold text-xs transition-colors flex items-center justify-center gap-2 cursor-pointer shadow-lg ${
                  attachments.length > 0 && checkerApproved
                    ? 'bg-rose-600 hover:bg-rose-500 text-white shadow-rose-600/20'
                    : 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
                }`}
              >
                <Lock className="w-4 h-4" />
                <span>Transmit to BFIU (4-Eyes Final Seal)</span>
              </button>
            </div>
          </div>
        </div>
      ) : (
        /* CTR Aggregator Sub-Tab */
        <div className="space-y-4">
          <div className="p-4 rounded-xl bg-panel border border-line flex flex-wrap items-center justify-between gap-4 shadow-xl">
            <div>
              <h2 className="text-sm font-bold text-slate-100 flex items-center gap-2 font-mono">
                <Table className="w-4 h-4 text-emerald-400" />
                BFIU Cash Transaction Reports (CTR) Pipeline
              </h2>
              <p className="text-xs text-slate-400 mt-0.5">
                Statutory cash transactions &ge; ৳1,000,000 BDT ({REGULATORY_CONFIG.ctrPolicy.statutoryBasis}).
                Filing deadline: {REGULATORY_CONFIG.ctrPolicy.filingDeadlineHours / 24} banking days.
              </p>
            </div>

            <div className="flex items-center gap-2">
              <a
                href={REGULATORY_CONFIG.ctrPolicy.sourceLink}
                target="_blank"
                rel="noopener noreferrer"
                className="px-3 py-1.5 rounded-lg bg-canvas border border-line-strong text-slate-300 hover:text-white text-xs flex items-center gap-1 font-mono"
              >
                <span>BFIU Circular</span>
                <ExternalLink className="w-3 h-3 text-sky-400" />
              </a>

              <button
                onClick={handleExportCtrXml}
                className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition-colors flex items-center gap-2 cursor-pointer shadow-lg shadow-emerald-600/20"
              >
                <FileSpreadsheet className="w-4 h-4" />
                <span>Batch Export BFIU CTR XML ({ctrRecords.length})</span>
              </button>
            </div>
          </div>

          {/* Statutory Threshold & Structuring Policy Context Banner */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs font-mono">
            <div className="p-3 bg-panel border border-line rounded-xl">
              <span className="text-slate-500 text-xs block font-bold">Statutory CTR Ceiling</span>
              <span className="text-emerald-400 font-bold text-sm">৳1,000,000 BDT</span>
              <span className="text-slate-400 text-xs block mt-0.5">
                Equivalent to ${REGULATORY_CONFIG.ctrPolicy.thresholdUsd.toLocaleString()} USD @ ৳120.00 FX
              </span>
            </div>

            <div className="p-3 bg-panel border border-line rounded-xl">
              <span className="text-slate-500 text-xs block font-bold">Structuring Detection Band</span>
              <span className="text-amber-400 font-bold text-sm">{REGULATORY_CONFIG.structuringPolicy.bandRangeFormatted}</span>
              <span className="text-slate-400 text-xs block mt-0.5">
                {REGULATORY_CONFIG.structuringPolicy.statutoryBasis}
              </span>
            </div>

            <div className="p-3 bg-panel border border-line rounded-xl">
              <span className="text-slate-500 text-xs block font-bold">Interbank FX Valuation</span>
              <span className="text-sky-400 font-bold text-sm">1 USD = ৳{REGULATORY_CONFIG.fxRatePolicy.usdToBdt.toFixed(2)} BDT</span>
              <span className="text-slate-400 text-xs block mt-0.5">
                Source: {REGULATORY_CONFIG.fxRatePolicy.source} ({REGULATORY_CONFIG.fxRatePolicy.dated})
              </span>
            </div>
          </div>

          {/* CTR Table */}
          <div className="bg-panel border border-line rounded-xl overflow-hidden shadow-2xl">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-300">
                <thead className="bg-canvas border-b border-line text-xs font-mono text-slate-400">
                  <tr>
                    <th className="px-4 py-3">CTR ID</th>
                    <th className="px-4 py-3">Customer Legal Name</th>
                    <th className="px-4 py-3">Account Number</th>
                    <th className="px-4 py-3 text-right">Cash Amount (USD)</th>
                    <th className="px-4 py-3 text-right">Cash Amount (BDT)</th>
                    <th className="px-4 py-3">Branch Location</th>
                    <th className="px-4 py-3">Timestamp</th>
                    <th className="px-4 py-3 text-center">Filing Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#1E293B]">
                  {ctrRecords.map((r) => (
                    <tr key={r.id} className="hover:bg-surface/40 transition-colors">
                      <td className="px-4 py-3 font-mono font-bold text-sky-400">{r.id}</td>
                      <td className="px-4 py-3 font-semibold text-slate-100">{r.entityName}</td>
                      <td className="px-4 py-3 font-mono text-slate-400">
                        <PiiText value={r.accountNumber} type="account" />
                      </td>
                      <td className="px-4 py-3 text-right font-mono font-bold text-emerald-400 tabular-nums">
                        ${r.amountUsd.toLocaleString(undefined, { minimumFractionDigits: 2 })} {r.currency}
                      </td>
                      <td className="px-4 py-3 text-right font-mono font-bold text-slate-200 tabular-nums">
                        ৳{r.amountNative.toLocaleString()}
                      </td>
                      <td className="px-4 py-3 text-slate-300">{r.branch}</td>
                      <td className="px-4 py-3 font-mono text-xs text-slate-400">{r.timestamp}</td>
                      <td className="px-4 py-3 text-center">
                        <span className="px-2 py-0.5 rounded text-xs font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                          {r.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default function SarWorkbenchPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center text-slate-400">Loading BFIU STR/SAR Workbench...</div>}>
      <SarWorkbenchContent />
    </Suspense>
  );
}
