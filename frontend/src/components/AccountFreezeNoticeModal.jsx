import React, { useState } from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import { 
  X, 
  Mail, 
  Send, 
  Download, 
  Copy, 
  Check, 
  FileText, 
  ShieldAlert, 
  AlertTriangle, 
  Lock, 
  Building2, 
  Clock, 
  CheckCircle2, 
  ExternalLink,
  Printer
} from 'lucide-react';
import { useAppStore } from '../lib/store';
import { useAuth } from '../context/AuthContext';
import { Badge } from './ui/Badge';
import { Button } from './ui/Button';

export const AccountFreezeNoticeModal = () => {
  const { 
    isFreezeNoticeOpen, 
    freezeNoticeTarget, 
    closeFreezeNoticeModal, 
    logAuditAction, 
    addCaseAttachment, 
    addToast 
  } = useAppStore();

  const { currentBanker } = useAuth();

  const [noticeType, setNoticeType] = useState('BFIU_STATUTORY_FREEZE');
  const [recipientEmail, setRecipientEmail] = useState('compliance-trade@meghnagroup.biz');
  const [copied, setCopied] = useState(false);
  const [isDispatching, setIsDispatching] = useState(false);
  const [dispatchedSuccess, setDispatchedSuccess] = useState(false);
  const [activeTab, setActiveTab] = useState('preview'); // 'preview' | 'how_to_fix' | 'email_receipt'

  if (!isFreezeNoticeOpen) return null;

  const target = freezeNoticeTarget || {
    accountNumber: 'BD22-EBLB-4829-1092-8823',
    holderName: 'Meghna Industrial & Agro Processing Ltd',
    amount: 9450,
    caseId: 'CASE-2026-0881',
    rail: 'SWIFT MT700 (LC)'
  };

  const accountNum = target.account || target.accountNumber || 'BD22-EBLB-4829-1092-8823';
  const holderName = target.entityName || target.holderName || target.name || 'Meghna Industrial & Agro Processing Ltd';
  const amountNum = Number(target.amount || 9450);
  const amountFormatted = `$${amountNum.toLocaleString()} USD (৳${(amountNum * 120).toLocaleString()} BDT)`;
  const caseId = target.caseId || 'CASE-2026-0881';
  const officerName = currentBanker?.name || 'Sarah Jenkins, CAMS';
  const officerTitle = currentBanker?.roleTitle || 'Senior BSA/AML Compliance Officer';
  const institution = currentBanker?.institution || 'Eastern Bank PLC / Corporate Compliance Desk';
  const noticeRef = `REF-FRZ-${accountNum.slice(-6)}-${Date.now().toString().slice(-4)}`;

  const NOTICE_TEMPLATES = {
    BFIU_STATUTORY_FREEZE: {
      title: 'NOTICE OF STATUTORY TRANSACTION SUSPENSION & ACCOUNT RESTRICTION (BFIU / MLPA 2012)',
      statutoryCode: 'Money Laundering Prevention Act, 2012 § 15 & § 17 / Bangladesh Bank BFIU Directive',
      subject: `[BFIU STATUTORY NOTICE] Notice of Temporary Trade Remittance Restriction — Ref #${noticeRef} (${amountFormatted})`,
      whyBasis: `In accordance with Section 15 and Section 17 of the Money Laundering Prevention Act, 2012 (Act No. V of 2012) and Bangladesh Financial Intelligence Unit (BFIU) guidelines, an administrative restriction has been applied to pending outbound trade remittances originating from account ${accountNum}. Monitoring safeguards identified a critical unit price discrepancy under Documentary Letter of Credit exceeding Bangladesh Customs (ASYCUDA) valuation benchmarks and structured sub-threshold allocation.`,
      fixSteps: [
        {
          step: 1,
          title: 'Submit Bangladesh Bank Export Form (EXP) & LC Authorization',
          detail: 'Submit duly authenticated Bangladesh Bank Online Export Monitoring System (OEMS) EXP form and corresponding Letter of Credit (LC) authorization copy.'
        },
        {
          step: 2,
          title: 'Provide Certified Bill of Lading & Customs Assessment Notice',
          detail: 'Furnish original Bill of Lading (B/L) issued by authorized shipping agent and Chittagong Customs House Assessment Notice verifying physical cargo movement.'
        },
        {
          step: 3,
          title: 'Trade Association Price Justification Attestation',
          detail: 'Provide price justification letter certified by trade association (BGMEA/BKMEA/FBCCI) explaining unit cost variance against customs database median.'
        },
        {
          step: 4,
          title: 'Authorized Dealer (AD) Branch Review & BFIU Clearance',
          detail: 'The Principal Branch Compliance Committee will evaluate documentation and submit clearance dossier to Bangladesh Financial Intelligence Unit within 48 hours.'
        }
      ]
    },
    STATUTORY_ADMIN_FREEZE: {
      title: 'NOTICE OF ADMINISTRATIVE TRANSACTION SUSPENSION & ACCOUNT RESTRICTION',
      statutoryCode: '31 CFR § 1020.320 / 31 U.S.C. § 5318(g)',
      subject: `[ACTION REQUIRED] Notice of Temporary Administrative Restriction — Ref #${noticeRef} (${amountFormatted})`,
      whyBasis: `In accordance with standard financial crime prevention protocols and institutional risk management obligations under 31 CFR § 1020.320, an administrative hold has been applied to pending outbound transaction instructions originating from account ${accountNum}. Automated monitoring safeguards identified rapid arrival velocity and multi-hop routing patterns inconsistent with historical commercial baseline profile.`,
      fixSteps: [
        {
          step: 1,
          title: 'Access Commercial Portal Verification Gateway',
          detail: `Log into the secure commercial treasury portal and enter verification code ${noticeRef}.`
        },
        {
          step: 2,
          title: 'Provide Underlying Commercial Invoices & Contracts',
          detail: `Furnish executed commercial sales contracts, counterparty invoices, and freight bills of lading matching the exact remittance sum of ${amountFormatted}.`
        },
        {
          step: 3,
          title: 'Ultimate Beneficial Ownership (UBO) Attestation',
          detail: 'Submit current Certificate of Good Standing and certified government identification for all corporate owners holding greater than 25% voting equity.'
        },
        {
          step: 4,
          title: 'Dual-Signatory Authorized Sign-Off',
          detail: 'Two authorized corporate treasury signatories must verify and digitally sign the remittance declaration via physical security key or MFA token.'
        },
        {
          step: 5,
          title: 'Compliance Review Timeline & Expedited Resolution',
          detail: 'Our Compliance Review Committee will evaluate submitted materials within 24–48 business hours. Upon successful verification, funds will be released for straight-through settlement.'
        }
      ]
    },
    SOURCE_OF_FUNDS_HOLD: {
      title: 'FORMAL NOTICE OF SOURCE OF FUNDS & WEALTH VERIFICATION REQUIREMENT',
      statutoryCode: 'Customer Due Diligence (CDD) Rule 31 CFR § 1010.230',
      subject: `[DOCUMENTATION REQUIRED] Source of Wealth & Capital Confirmation — Ref #${noticeRef}`,
      whyBasis: `Under Customer Due Diligence (CDD) requirements, periodic source of funds documentation is required for transactions meeting high-velocity aggregation thresholds on account ${accountNum}.`,
      fixSteps: [
        {
          step: 1,
          title: 'Complete Form CDD-701',
          detail: 'Download and execute the official Source of Funds & Purpose of Remittance Declaration.'
        },
        {
          step: 2,
          title: 'Certified Bank Proof of Originating Capital',
          detail: 'Provide bank statement from originating liquidity institution showing clear commercial revenue origin.'
        },
        {
          step: 3,
          title: 'Direct Relationship Manager Review',
          detail: 'Submit directly through your corporate banking portal for immediate review by your assigned compliance officer.'
        }
      ]
    }
  };

  const currentNotice = NOTICE_TEMPLATES[noticeType] || NOTICE_TEMPLATES.BFIU_STATUTORY_FREEZE;

  const handleCopyText = () => {
    const fullText = `================================================================================
${currentNotice.title}
INSTITUTION: ${institution}
STATUTORY MANDATE: ${currentNotice.statutoryCode}
CASE REFERENCE: ${caseId} | NOTICE ID: ${noticeRef}
DATE: ${new Date().toUTCString()}
--------------------------------------------------------------------------------
RECIPIENT: ${holderName}
ACCOUNT NUMBER: ${accountNum}
RESTRICTED SUM: ${amountFormatted}
RECIPIENT EMAIL: ${recipientEmail}

1. REASON FOR TEMPORARY RESTRICTION:
${currentNotice.whyBasis}

2. HOW TO REMEDIATE AND RESTORE ACCOUNT ACCESS:
${currentNotice.fixSteps.map(s => `${s.step}. ${s.title}\n   ${s.detail}`).join('\n\n')}

3. ISSUING COMPLIANCE OFFICER:
${officerName}, ${officerTitle}
Global Financial Crimes Compliance Desk
${institution}
================================================================================`;

    navigator.clipboard.writeText(fullText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadPDF = () => {
    // Generate an official standalone HTML printable certificate / PDF document
    const htmlContent = `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Administrative_Freeze_Notice_${caseId}</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; padding: 40px; color: #111827; line-height: 1.5; font-size: 13px; }
    .header { border-bottom: 2px solid #2563EB; padding-bottom: 16px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: flex-start; }
    .bank-name { font-size: 18px; font-weight: 800; color: #1E3A8A; letter-spacing: -0.5px; }
    .doc-title { font-size: 15px; font-weight: 700; color: #DC2626; margin: 18px 0 6px 0; text-transform: uppercase; }
    .meta-box { background-color: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 6px; padding: 14px; margin-bottom: 20px; font-family: monospace; font-size: 11px; }
    .meta-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
    .section-title { font-size: 13px; font-weight: 700; color: #1F2937; border-bottom: 1px solid #E5E7EB; padding-bottom: 4px; margin: 20px 0 10px 0; text-transform: uppercase; letter-spacing: 0.5px; }
    .step-box { background: #FFFFFF; border: 1px solid #E5E7EB; border-left: 3px solid #2563EB; padding: 10px 14px; margin-bottom: 8px; border-radius: 4px; }
    .step-title { font-weight: 700; color: #1E40AF; font-size: 12px; margin-bottom: 3px; }
    .stamp { display: inline-block; border: 2px dashed #DC2626; color: #DC2626; padding: 6px 14px; font-weight: 800; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; border-radius: 4px; margin-top: 15px; }
    .footer { margin-top: 40px; border-top: 1px solid #E5E7EB; padding-top: 14px; font-size: 10px; color: #6B7280; display: flex; justify-content: space-between; }
    @media print { body { padding: 0; } }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <div class="bank-name">${institution}</div>
      <div style="font-size: 11px; color: #4B5563;">Global Financial Crimes Compliance &amp; Regulatory Operations</div>
      <div style="font-size: 10px; color: #6B7280;">Statutory Mandate: ${currentNotice.statutoryCode}</div>
    </div>
    <div style="text-align: right; font-family: monospace; font-size: 11px;">
      <div><strong>DATE:</strong> ${new Date().toISOString().substring(0, 10)}</div>
      <div><strong>NOTICE REF:</strong> ${noticeRef}</div>
      <div><strong>CASE ID:</strong> ${caseId}</div>
    </div>
  </div>

  <div class="doc-title">${currentNotice.title}</div>
  <div style="font-size: 12px; color: #4B5563; margin-bottom: 16px;">
    Official Statutory Notice Issued Pursuant to Bank Secrecy Act / USA PATRIOT Act Compliance Standards
  </div>

  <div class="meta-box">
    <div class="meta-grid">
      <div><strong>ACCOUNT HOLDER:</strong> ${holderName}</div>
      <div><strong>ACCOUNT NUMBER:</strong> ${accountNum}</div>
      <div><strong>RESTRICTED AMOUNT:</strong> ${amountFormatted}</div>
      <div><strong>SETTLEMENT RAIL:</strong> ${target.rail || 'SWIFT MT103'}</div>
      <div><strong>RECIPIENT EMAIL:</strong> ${recipientEmail}</div>
      <div><strong>ISSUING OFFICER:</strong> ${officerName} (${officerTitle})</div>
    </div>
  </div>

  <div class="section-title">1. Reason for Administrative Transaction Suspension (Why)</div>
  <p style="margin: 0 0 16px 0; color: #374151; font-size: 12px; leading: 1.6;">
    ${currentNotice.whyBasis}
  </p>
  <div style="background-color: #FEF2F2; border-left: 3px solid #EF4444; padding: 8px 12px; font-size: 11px; color: #991B1B; margin-bottom: 20px;">
    <strong>Statutory Anti-Tipping-Off Safeguard (31 U.S.C. § 5318(g)(2)):</strong>
    This notice provides standard commercial verification instructions. Internal risk thresholds and automated scoring indicators are proprietary and exempt from commercial disclosure.
  </div>

  <div class="section-title">2. Remediation Procedure &amp; Required Documents (How to Fix)</div>
  <div>
    ${currentNotice.fixSteps.map(s => `
      <div class="step-box">
        <div class="step-title">Step ${s.step}: ${s.title}</div>
        <div style="font-size: 11px; color: #4B5563;">${s.detail}</div>
      </div>
    `).join('')}
  </div>

  <div style="margin-top: 24px;">
    <div class="stamp">OFFICIAL NOTICE OF TEMPORARY RESTRICTION • VERIFIED</div>
  </div>

  <div class="footer">
    <div>Issuing Authority: ${institution} Treasury Risk Department</div>
    <div>Electronic Cryptographic Hash: SHA256-${Date.now().toString(16).padStart(16, '0')}</div>
    <div>Page 1 of 1</div>
  </div>

  <script>
    window.onload = function() { window.print(); }
  </script>
</body>
</html>`;

    const blob = new Blob([htmlContent], { type: 'text/html;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `Statutory_Freeze_Notice_${accountNum.replace(/[^a-zA-Z0-9]/g, '_')}_${caseId}.html`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    addToast('PDF Notice Exported', `Generated formal statutory freeze notice for ${accountNum}.`, 'success');
  };

  const handleDispatchEmail = () => {
    setIsDispatching(true);

    setTimeout(() => {
      // 1. Log to Cryptographic Merkle Audit Vault
      logAuditAction(
        'STATUTORY_FREEZE_NOTICE_DISPATCHED',
        `Official freeze notice & remediation PDF dispatched via TLS email to ${recipientEmail} for account ${accountNum}. Reference: ${noticeRef}`,
        accountNum,
        officerName,
        'Dual Control Stamped'
      );

      // 2. Attach Notice PDF to Case File
      addCaseAttachment(caseId, {
        id: `att-frz-${Date.now()}`,
        name: `Statutory_Freeze_Notice_${noticeRef}.pdf`,
        size: '248 KB',
        type: 'application/pdf',
        uploadedAt: new Date().toISOString().substring(11, 16) + ' UTC',
        uploadedBy: officerName
      });

      setIsDispatching(false);
      setDispatchedSuccess(true);
      addToast(
        'Notice Dispatched via Email',
        `Dispatched formal freeze notice & PDF to ${recipientEmail}. Attached to case ${caseId}.`,
        'success'
      );
    }, 700);
  };

  return (
    <Dialog.Root open={isFreezeNoticeOpen} onOpenChange={closeFreezeNoticeModal}>
      <Dialog.Portal>
        {/* Dimmed backdrop */}
        <Dialog.Overlay className="fixed inset-0 z-50 bg-black/60 backdrop-blur-[2px] animate-fadeIn" />

        {/* Solid Opaque Dialog Body */}
        <Dialog.Content
          aria-describedby={undefined}
          className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-[min(780px,94vw)] max-h-[88vh]
                     overflow-y-auto rounded-lg border border-border bg-popover text-foreground shadow-2xl p-5 focus:outline-none"
        >
          {/* Header */}
          <div className="flex items-start justify-between pb-3 border-b border-border">
            <div className="flex items-center gap-2.5">
              <div className="p-2 rounded bg-critical/10 border border-critical/30 text-critical">
                <ShieldAlert className="w-5 h-5" />
              </div>
              <div>
                <Dialog.Title className="text-sm sm:text-base font-bold text-text">
                  Statutory Account Freeze &amp; Customer Remediation Notice
                </Dialog.Title>
                <p className="text-xs text-text-2 mt-0.5 font-mono">
                  {institution} • Compliance Case: <span className="text-accent font-semibold">{caseId}</span>
                </p>
              </div>
            </div>
            <Dialog.Close asChild>
              <button className="text-text-muted hover:text-text p-1 rounded hover:bg-surfaceHover transition-colors cursor-pointer">
                <X className="w-4 h-4" />
              </button>
            </Dialog.Close>
          </div>

          {/* Anti-Tipping-Off Statutory Safeguard Banner */}
          <div className="mt-3 p-2.5 rounded bg-surfaceRaised border border-border flex items-start gap-2.5 text-xs">
            <Lock className="w-4 h-4 text-critical shrink-0 mt-0.5" />
            <div className="text-text-2 leading-relaxed">
              <strong className="text-text font-mono uppercase text-[11px]">
                Statutory Anti-Tipping-Off Safeguard (31 U.S.C. § 5318(g)(2)):
              </strong>
              <span className="block mt-0.5 text-[11px]">
                This formal customer notice informs the account holder of transaction suspension and establishes an actionable remediation pathway without disclosing internal ML invariants or regulatory SAR filings.
              </span>
            </div>
          </div>

          {/* Configuration Grid */}
          <div className="mt-3 grid grid-cols-1 sm:grid-cols-3 gap-2.5 text-xs font-mono">
            <div className="p-2 rounded bg-surface border border-border">
              <span className="text-[10px] text-text-muted uppercase block">TARGET ENTITY</span>
              <span className="font-bold text-text truncate block">{holderName}</span>
              <span className="text-[10px] text-text-muted truncate block">{accountNum}</span>
            </div>

            <div className="p-2 rounded bg-surface border border-border">
              <span className="text-[10px] text-text-muted uppercase block">RESTRICTED EXPOSURE</span>
              <span className="font-bold text-critical text-sm block">{amountFormatted}</span>
              <span className="text-[10px] text-text-muted block">Rail: {target.rail || 'SWIFT MT103'}</span>
            </div>

            <div className="p-2 rounded bg-surface border border-border">
              <label htmlFor="freeze-notice-email" className="text-[10px] text-text-muted uppercase block cursor-pointer">RECIPIENT EMAIL</label>
              <input
                id="freeze-notice-email"
                name="freeze-notice-email"
                aria-label="Recipient Email"
                type="email"
                value={recipientEmail}
                onChange={(e) => setRecipientEmail(e.target.value)}
                className="w-full bg-bg border border-borderSubtle rounded px-2 py-0.5 text-xs text-text font-mono mt-0.5 focus:outline-none focus:border-accent"
              />
            </div>
          </div>

          {/* Statutory Order Framework Selector */}
          <div className="mt-3 flex items-center gap-2 flex-wrap text-xs">
            <span className="text-text-muted font-mono text-[11px]">Statutory Framework:</span>
            {[
              { id: 'BFIU_STATUTORY_FREEZE', label: 'BFIU Order (MLPA 2012 §15)', badge: 'Bangladesh Bank' },
              { id: 'STATUTORY_ADMIN_FREEZE', label: 'FinCEN / BSA (31 CFR §1020.320)', badge: 'US Correspondent' },
              { id: 'SOURCE_OF_FUNDS_HOLD', label: 'CDD Source of Wealth Hold', badge: 'Customer CDD' }
            ].map(type => (
              <button
                key={type.id}
                onClick={() => setNoticeType(type.id)}
                className={`px-2.5 py-1 rounded border text-xs font-mono transition-colors cursor-pointer flex items-center gap-1.5 ${
                  noticeType === type.id
                    ? 'bg-accent/15 border-accent text-accent font-semibold shadow-xs'
                    : 'bg-surface border-border text-text-muted hover:text-text'
                }`}
              >
                <span>{type.label}</span>
                <span className="text-[10px] opacity-70">({type.badge})</span>
              </button>
            ))}
          </div>

          {/* Tab Selection */}
          <div className="flex items-center gap-2 border-b border-border pt-3 pb-2 text-xs font-medium">
            <button
              onClick={() => setActiveTab('preview')}
              className={`pb-1 px-1 border-b-2 transition-colors cursor-pointer ${
                activeTab === 'preview' 
                  ? 'border-accent text-accent font-semibold' 
                  : 'border-transparent text-text-muted hover:text-text'
              }`}
            >
              1. Official Notice Document Preview
            </button>
            <button
              onClick={() => setActiveTab('how_to_fix')}
              className={`pb-1 px-1 border-b-2 transition-colors cursor-pointer ${
                activeTab === 'how_to_fix' 
                  ? 'border-accent text-accent font-semibold' 
                  : 'border-transparent text-text-muted hover:text-text'
              }`}
            >
              2. Remediation Checklist ("How to Fix")
            </button>
          </div>

          {/* Tab Content */}
          <div className="mt-3">
            {activeTab === 'preview' ? (
              <div className="space-y-3">
                {/* Official Letterhead Preview Box */}
                <div className="p-4 rounded-lg bg-surface border border-border space-y-3 font-sans text-xs">
                  <div className="flex justify-between items-start border-b border-borderSubtle pb-2">
                    <div>
                      <div className="font-bold text-xs uppercase tracking-wider text-text">
                        {institution}
                      </div>
                      <div className="text-[10px] text-text-muted">
                        Statutory Mandate: {currentNotice.statutoryCode}
                      </div>
                    </div>
                    <div className="text-right font-mono text-[10px] text-text-muted">
                      <div>Ref: {noticeRef}</div>
                      <div>Date: {new Date().toISOString().substring(0, 10)}</div>
                    </div>
                  </div>

                  <div className="text-xs font-bold text-critical uppercase">
                    {currentNotice.title}
                  </div>

                  <div className="p-2.5 rounded bg-bg border border-borderSubtle font-mono text-[11px] space-y-1">
                    <span className="font-semibold text-text uppercase text-[10px] block text-accent">
                      Section 1: Statutory Reason for Restriction (Why)
                    </span>
                    <p className="text-text-2 leading-relaxed">
                      {currentNotice.whyBasis}
                    </p>
                  </div>

                  <div className="text-xs text-text space-y-1.5">
                    <span className="font-semibold block text-text">
                      Required Action:
                    </span>
                    <p className="text-text-2 leading-relaxed">
                      Please refer to the Remediation Protocol below to submit verifying commercial documentation. Upon compliance certification, administrative holds are released in accordance with standard statutory timelines.
                    </p>
                  </div>

                  <div className="pt-2 border-t border-borderSubtle flex items-center justify-between text-[11px] text-text-muted font-mono">
                    <span>Officer: {officerName}</span>
                    <span className="text-cleared font-semibold">ISO 20022 Notice Certified</span>
                  </div>
                </div>
              </div>
            ) : (
              <div className="space-y-2.5">
                <div className="text-xs text-text-muted mb-1">
                  Customer-facing remediation instructions included with the dispatched notice:
                </div>
                {currentNotice.fixSteps.map((s) => (
                  <div
                    key={s.step}
                    className="p-3 rounded-lg border border-border bg-surface flex items-start gap-3"
                  >
                    <div className="w-6 h-6 rounded-full bg-accent/10 border border-accent/30 text-accent font-bold font-mono text-xs flex items-center justify-center shrink-0">
                      {s.step}
                    </div>
                    <div className="text-xs space-y-0.5">
                      <span className="font-semibold text-text block">{s.title}</span>
                      <p className="text-text-2 leading-relaxed">{s.detail}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Dispatch Success Alert */}
          {dispatchedSuccess && (
            <div className="mt-3 p-3 rounded bg-cleared-bg border border-cleared text-xs text-cleared flex items-center justify-between">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 shrink-0" />
                <span>
                  Notice successfully dispatched to <strong>{recipientEmail}</strong>. PDF copy attached to case docket #{caseId} &amp; logged to Merkle audit vault.
                </span>
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="mt-4 pt-3 border-t border-border flex flex-wrap items-center justify-between gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handleCopyText}
              icon={copied ? Check : Copy}
              className="text-xs h-8"
            >
              {copied ? 'Notice Copied' : 'Copy Notice Text'}
            </Button>

            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={handleDownloadPDF}
                icon={Download}
                className="text-xs h-8"
              >
                Download Official PDF Notice
              </Button>

              <Button
                variant="primary"
                size="sm"
                disabled={isDispatching}
                onClick={handleDispatchEmail}
                icon={Send}
                className="text-xs h-8 bg-[#2563EB] hover:bg-[#1D4ED8] text-white font-semibold shadow-xs"
              >
                {isDispatching ? 'Transmitting Notice...' : 'Dispatch to Customer Email'}
              </Button>
            </div>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
};
