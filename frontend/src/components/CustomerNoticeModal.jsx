import React, { useState } from 'react';
import { 
  X, 
  Mail, 
  Send, 
  Copy, 
  Check, 
  FileText, 
  ShieldCheck, 
  AlertCircle, 
  Download, 
  HelpCircle,
  Clock,
  ArrowRight,
  RotateCcw
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const CustomerNoticeModal = ({ isOpen, onClose, targetAccount, onNoticeDispatched }) => {
  const { currentBanker, logBankerAction } = useAuth();
  const [noticeType, setNoticeType] = useState('VERIFICATION_REQUIRED');
  const [copied, setCopied] = useState(false);
  const [dispatched, setDispatched] = useState(false);

  if (!isOpen || !targetAccount) return null;

  const holderName = targetAccount.holderName || 'Apex Global Logistics Ltd';
  const accountNum = targetAccount.accountNumber || targetAccount.src || 'US-JPMC-4829-1092-8823';
  const amount = targetAccount.amount ? `$${targetAccount.amount.toLocaleString()}` : '$9,450.00 USD';
  const institution = currentBanker.institution || 'JPMorgan Chase & Co.';

  const NOTICE_TEMPLATES = {
    VERIFICATION_REQUIRED: {
      subject: `[ACTION REQUIRED] Security Verification for Your Pending Transfer (${amount})`,
      body: `Dear Valued Customer (${holderName}),

As part of our standard automated security safeguards at ${institution}, we have placed a temporary administrative review hold on your outbound wire transfer of ${amount} initiated from account ${accountNum}.

Why this occurred:
Our continuous monitoring system noted an unusual transaction velocity or destination routing pattern that differs from your typical profile. This is a routine security check to ensure your account remains protected against unauthorized activity.

How to verify and release this transaction:
1. Please log into your Secure Business Banking Portal and navigate to "Pending Authorizations".
2. Confirm the authorized beneficiary details and corporate invoice reference.
3. If this was submitted by an authorized officer, you may upload a signed purchase order or trade agreement to expedite processing.

If you did not authorize this transfer, please immediately contact our 24/7 Global Fraud Operations Center at 1-800-555-0199.

Sincerely,
${currentBanker.name} (${currentBanker.roleTitle})
${currentBanker.department}
${institution}`
    },
    DOCUMENT_REQUEST_RFI: {
      subject: `[SUPPORTING DOCUMENTATION] Request for Source of Funds — Transfer #${accountNum.slice(-6)}`,
      body: `Dear ${holderName},

Thank you for your continued banking relationship with ${institution}. 

Regarding your recent high-volume settlement of ${amount}, our Compliance and Risk Operations team requires standard supporting documentation to complete the clearance of these funds in accordance with federal banking regulations.

Requested Documents (Please provide within 5 business days):
• Commercial invoice or sales contract detailing the counterparty relationship.
• Bill of Lading, airway bill, or customs declaration (if trade-related).
• Corporate board resolution authorizing the signatory.

You may securely submit these documents via the Banker Document Portal or by replying directly to your assigned Relationship Manager.

Sincerely,
${currentBanker.name} (${currentBanker.roleTitle})
${institution}`
    },
    SAFE_RETRY_GUIDANCE: {
      subject: `[TRANSACTION ADVICE] How to Safely Complete Your Pending Payment`,
      body: `Dear ${holderName},

We noticed that your recent transfer attempt of ${amount} from account ${accountNum} could not be cleared automatically due to destination routing restrictions.

Recommended Steps to Safely Complete this Transfer:
1. Single Transfer Splitting: Avoid submitting multiple high-volume transactions in rapid succession under round thresholds, as this triggers automated clearing tripwires.
2. Verified Counterparty Beneficiary: Ensure your beneficiary's full Legal Entity Identifier (LEI) and SWIFT BIC code are precisely registered in your address book.
3. Standard Clearing Windows: Submit wire instructions during standard banking hours (08:00–16:00 EST) to enable straight-through processing.

Once updated, you may re-submit the transaction through online banking.

Sincerely,
${currentBanker.name}
${currentBanker.department}
${institution}`
    },
    CFPB_FCRA_ADVERSE_ACTION: {
      subject: `[STATUTORY NOTICE] Statement of Adverse Action & Specific Principal Reasons (12 CFR § 1002.9)`,
      body: `STATEMENT OF ADVERSE ACTION & STATUTORY DISCLOSURE
Issued pursuant to the Equal Credit Opportunity Act (ECOA / Regulation B) and Fair Credit Reporting Act (FCRA)

Date: September 2, 2026
Applicant / Account Holder: ${holderName}
Account Number: ${accountNum}
Financial Institution: ${institution}

Description of Adverse Action Taken:
Administrative restriction, wire hold, or denial of funds transfer in the amount of ${amount}.

Principal Reason(s) for Adverse Action:
1. Automated Anti-Money Laundering (AML) Algorithmic Model Anomaly: Transaction exhibited cyclic flow conservation (Phi ≈ 1.0) and high-velocity transit indicative of pass-through layering.
2. Structuring Alert: Transaction sequence features rapid sub-threshold allocations falling within federal monitoring trigger bands (31 U.S.C. § 5324).
3. Counterparty Transparency Requirement: Insufficient public registry verification for intermediate recipient nodes in high-risk jurisdictions.

Your Rights Under Federal Law:
Under the Fair Credit Reporting Act and Dodd-Frank Act Section 1071, you have the right to know the information contained in your file and the specific mathematical factors contributing to this determination. You may request a human compliance review within 60 days by writing to:

Compliance Governance Department
${institution}
Reference Dossier ID: AML-FCRA-${accountNum.slice(-6)}

Sincerely,
${currentBanker.name} (${currentBanker.roleTitle})
Model Governance & Compliance Oversight`
    }
  };

  const activeNotice = NOTICE_TEMPLATES[noticeType] || NOTICE_TEMPLATES.VERIFICATION_REQUIRED;

  const handleCopy = () => {
    navigator.clipboard.writeText(`Subject: ${activeNotice.subject}\n\n${activeNotice.body}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDispatch = () => {
    logBankerAction({
      action: `CUSTOMER_NOTICE_DISPATCHED (${noticeType})`,
      targetAccount: `${accountNum} (${holderName})`,
      reason: `Official bank letter dispatched via secure customer portal: ${activeNotice.subject}`
    });

    setDispatched(true);
    setTimeout(() => {
      setDispatched(false);
      if (onNoticeDispatched) onNoticeDispatched();
      onClose();
    }, 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-black/60 backdrop-blur-sm animate-fadeIn select-none">
      <div className="w-full max-w-xl bg-[var(--bg-card)] border border-[var(--border-card)] rounded-2xl shadow-2xl overflow-hidden flex flex-col skeuo-card max-h-[92vh] overflow-y-auto">
        
        {/* Header */}
        <div className="p-3.5 sm:p-4 bg-[var(--bg-card-elevated)] border-b border-[var(--border-subtle)] flex items-center justify-between">
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-b from-[#257843] to-[#144726] border border-[#113C21] flex items-center justify-center text-white shrink-0 shadow-[var(--skeuo-btn)]">
              <Mail className="w-4 h-4 text-white" />
            </div>
            <div className="min-w-0">
              <h3 className="text-xs sm:text-sm font-bold text-[var(--text-primary)] font-sans truncate">Customer Security Notice &amp; Guidance Letter</h3>
              <p className="text-[10px] text-[var(--text-muted)] font-sans truncate">
                Professional communication issued by {currentBanker.name}
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg skeuo-btn text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-all cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-3.5 sm:p-4 space-y-2.5 sm:space-y-3 font-sans text-xs">
          {/* Notice Type Selector */}
          <div>
            <label className="text-[10px] sm:text-[11px] font-semibold text-[var(--text-muted)] block mb-1 font-mono uppercase">
              Select Official Notice Template:
            </label>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-1.5 font-mono text-[10px]">
              <button
                onClick={() => setNoticeType('VERIFICATION_REQUIRED')}
                className={`p-1.5 rounded-lg text-left cursor-pointer transition-all ${
                  noticeType === 'VERIFICATION_REQUIRED'
                    ? 'bg-gradient-to-b from-[#257843] to-[#144726] text-white font-bold border border-[#113C21] shadow-[var(--skeuo-btn)]'
                    : 'skeuo-btn text-[var(--text-secondary)]'
                }`}
              >
                1. Verification
              </button>

              <button
                onClick={() => setNoticeType('DOCUMENT_REQUEST_RFI')}
                className={`p-1.5 rounded-lg text-left cursor-pointer transition-all ${
                  noticeType === 'DOCUMENT_REQUEST_RFI'
                    ? 'bg-gradient-to-b from-amber-600 to-amber-800 text-white font-bold border border-amber-900 shadow-[var(--skeuo-btn)]'
                    : 'skeuo-btn text-[var(--text-secondary)]'
                }`}
              >
                2. Request (RFI)
              </button>

              <button
                onClick={() => setNoticeType('SAFE_RETRY_GUIDANCE')}
                className={`p-1.5 rounded-lg text-left cursor-pointer transition-all ${
                  noticeType === 'SAFE_RETRY_GUIDANCE'
                    ? 'bg-gradient-to-b from-[#257843] to-[#144726] text-white font-bold border border-[#113C21] shadow-[var(--skeuo-btn)]'
                    : 'skeuo-btn text-[var(--text-secondary)]'
                }`}
              >
                3. Safe Retry
              </button>

              <button
                onClick={() => setNoticeType('CFPB_FCRA_ADVERSE_ACTION')}
                className={`p-1.5 rounded-lg text-left cursor-pointer transition-all ${
                  noticeType === 'CFPB_FCRA_ADVERSE_ACTION'
                    ? 'bg-gradient-to-b from-rose-600 to-rose-800 text-white font-bold border border-rose-900 shadow-[var(--skeuo-btn)]'
                    : 'skeuo-btn text-[var(--text-secondary)]'
                }`}
              >
                4. CFPB / FCRA
              </button>
            </div>
          </div>

          {/* Subject Field */}
          <div className="p-2 rounded-lg skeuo-well space-y-0.5">
            <span className="text-[9px] font-mono text-[var(--text-muted)] uppercase">SUBJECT LINE:</span>
            <div className="font-semibold text-[var(--accent-primary)] text-[11px] truncate">{activeNotice.subject}</div>
          </div>

          {/* Letter Body Preview */}
          <div className="space-y-0.5">
            <span className="text-[9px] font-mono text-[var(--text-muted)] uppercase">OFFICIAL LETTER TEXT:</span>
            <textarea
              readOnly
              rows={6}
              value={activeNotice.body}
              className="w-full p-2.5 rounded-xl skeuo-well text-[var(--text-primary)] font-mono text-[10px] sm:text-[11px] leading-relaxed resize-none focus:outline-none"
            />
          </div>

          <div className="p-2 sm:p-2.5 rounded-lg bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)] flex items-center justify-between text-[10px] sm:text-[11px] text-[var(--text-secondary)] font-sans">
            <div className="flex items-center gap-1.5 truncate">
              <ShieldCheck className="w-3.5 h-3.5 text-[var(--accent-primary)] shrink-0" />
              <span className="truncate">Stamped: <b>{currentBanker.id}</b> • Audit Logged</span>
            </div>
            <span className="text-[var(--text-muted)] font-mono text-[9px] shrink-0">ISO 20022 Std</span>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="p-3 sm:p-3.5 bg-[var(--bg-card-elevated)] border-t border-[var(--border-subtle)] flex items-center justify-between gap-2">
          <button
            onClick={handleCopy}
            className="px-2.5 py-1.5 rounded-lg skeuo-btn skeuo-btn-secondary text-[10px] sm:text-[11px] font-mono flex items-center gap-1.5 cursor-pointer"
          >
            {copied ? <Check className="w-3 h-3 text-[var(--accent-primary)]" /> : <Copy className="w-3 h-3" />}
            <span>{copied ? 'Copied' : 'Copy Text'}</span>
          </button>

          <div className="flex items-center gap-1.5">
            <button
              onClick={onClose}
              className="px-3 py-1.5 rounded-lg skeuo-btn skeuo-btn-secondary text-xs font-medium cursor-pointer"
            >
              Cancel
            </button>

            <button
              onClick={handleDispatch}
              disabled={dispatched}
              className="px-3 sm:px-3.5 py-1.5 rounded-lg skeuo-btn skeuo-btn-primary text-xs font-bold flex items-center gap-1.5 cursor-pointer transition-all active:scale-[0.98]"
            >
              {dispatched ? <Check className="w-3.5 h-3.5" /> : <Send className="w-3.5 h-3.5" />}
              <span>{dispatched ? 'Dispatched!' : 'Dispatch Notice'}</span>
            </button>
          </div>
        </div>

      </div>
    </div>
  );
};
