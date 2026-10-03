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

As part of our standard transaction authorization safeguards at ${institution}, your recent outbound transfer of ${amount} initiated from account ${accountNum} has been temporarily placed in pending status awaiting security verification.

Next Steps to Complete Processing:
1. Please log into your Secure Commercial Banking Portal and navigate to "Pending Authorizations".
2. Confirm the authorized beneficiary name, routing number, and settlement purpose.
3. If this was submitted by an authorized corporate signatory, please verify the dual-control token approval.

If you or your authorized representatives did not initiate this payment instruction, please contact our 24/7 Treasury Operations Support desk immediately at 1-800-555-0199.

Sincerely,
${currentBanker.name} (${currentBanker.roleTitle})
Operations & Risk Controls
${institution}`
    },
    DOCUMENT_REQUEST_RFI: {
      subject: `[SUPPORTING DOCUMENTATION] Request for Information (RFI) — Reference #${accountNum.slice(-6)}`,
      body: `Dear ${holderName},

Thank you for your commercial banking relationship with ${institution}.

In accordance with standard institutional due diligence procedures, we request supporting documentation regarding the recent commercial settlement instruction of ${amount} (Ref: #${accountNum.slice(-6)}).

Please furnish the following documentation within 5 business days:
• Executed commercial invoice or sales contract matching the stated transfer amount.
• Bill of Lading, airway bill, or official customs export documentation (if trade-related).
• Corporate authorization or board resolution confirming beneficiary authority.

Documents may be uploaded securely through the Corporate Treasury Portal under "Compliance & Documentation" or transmitted directly to your dedicated Relationship Manager.

Sincerely,
${currentBanker.name} (${currentBanker.roleTitle})
Commercial Due Diligence Operations
${institution}`
    },
    SOURCE_OF_FUNDS_DECLARATION: {
      subject: `[DUE DILIGENCE] Source of Funds & Purpose of Remittance Declaration`,
      body: `Dear ${holderName},

Under our institutional Customer Due Diligence (CDD) framework and periodic risk review standards, ${institution} requires a verified Source of Funds declaration for high-value activity associated with account ${accountNum}.

Required Submission Items:
1. Completed and signed Source of Wealth / Funds Declaration Form (Form CDD-701).
2. Audited corporate financial statements or certified bank confirmation of originating capital.
3. Description of commercial underlying economic activity corresponding to transaction ${amount}.

Please upload the executed declaration package to the Corporate Portal within 7 business days to prevent operational holds on future settlements.

Sincerely,
${currentBanker.name} (${currentBanker.roleTitle})
Compliance Operations & Customer Due Diligence
${institution}`
    },
    BENEFICIARY_ENTITY_VALIDATION: {
      subject: `[BENEFICIARY VERIFICATION] Corporate Entity Validation Required`,
      body: `Dear ${holderName},

Your pending payment instruction of ${amount} requires counterparty entity validation prior to final settlement.

Required Counterparty Validation:
• Beneficiary Legal Entity Identifier (LEI) or Certificate of Good Standing.
• Confirmation of Ultimate Beneficial Ownership (UBO) for entity holding >25% equity.
• Stated commercial relationship between originating entity and receiving beneficiary.

Please transmit this verification via your secure relationship portal.

Sincerely,
${currentBanker.name} (${currentBanker.roleTitle})
Treasury Settlements & Counterparty Risk
${institution}`
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
      action: `CUSTOMER_RFI_DISPATCHED (${noticeType})`,
      targetAccount: `${accountNum} (${holderName})`,
      reason: `Official bank RFI notice dispatched via secure customer portal: ${activeNotice.subject}`
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
              <h3 className="text-xs sm:text-sm font-bold text-[var(--text-primary)] font-sans truncate">Client Due Diligence &amp; Request for Information (RFI)</h3>
              <p className="text-[10px] text-[var(--text-muted)] font-sans truncate">
                Compliant institutional notice issued by {currentBanker.name}
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

        {/* Anti-Tipping-Off Statutory Safeguard Banner */}
        <div className="mx-3.5 sm:mx-4 mt-3 p-2 rounded-lg bg-rose-500/10 border border-rose-500/30 flex items-start gap-2 text-[10px] font-sans">
          <AlertCircle className="w-4 h-4 text-rose-500 shrink-0 mt-0.5" />
          <div className="text-rose-700 dark:text-rose-300">
            <strong className="font-mono uppercase font-bold">Anti-Tipping-Off Mandatory Rule (31 U.S.C. § 5318(g)(2)):</strong>
            <span className="block mt-0.5 text-[9.5px] leading-tight text-rose-800/90 dark:text-rose-300/90">
              Do not disclose AML detection algorithms, suspicious activity indicators, or internal tripwires to the customer. All communications must follow standard verification and document request (RFI) procedures.
            </span>
          </div>
        </div>

        {/* Content Body */}
        <div className="p-3.5 sm:p-4 space-y-2.5 sm:space-y-3 font-sans text-xs">
          {/* Notice Type Selector */}
          <div>
            <label className="text-[10px] sm:text-[11px] font-semibold text-[var(--text-muted)] block mb-1 font-mono uppercase">
              Select Official RFI / Notice Template:
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
                1. Authorization
              </button>

              <button
                onClick={() => setNoticeType('DOCUMENT_REQUEST_RFI')}
                className={`p-1.5 rounded-lg text-left cursor-pointer transition-all ${
                  noticeType === 'DOCUMENT_REQUEST_RFI'
                    ? 'bg-gradient-to-b from-[#257843] to-[#144726] text-white font-bold border border-[#113C21] shadow-[var(--skeuo-btn)]'
                    : 'skeuo-btn text-[var(--text-secondary)]'
                }`}
              >
                2. Invoices / Trade
              </button>

              <button
                onClick={() => setNoticeType('SOURCE_OF_FUNDS_DECLARATION')}
                className={`p-1.5 rounded-lg text-left cursor-pointer transition-all ${
                  noticeType === 'SOURCE_OF_FUNDS_DECLARATION'
                    ? 'bg-gradient-to-b from-[#257843] to-[#144726] text-white font-bold border border-[#113C21] shadow-[var(--skeuo-btn)]'
                    : 'skeuo-btn text-[var(--text-secondary)]'
                }`}
              >
                3. Source of Funds
              </button>

              <button
                onClick={() => setNoticeType('BENEFICIARY_ENTITY_VALIDATION')}
                className={`p-1.5 rounded-lg text-left cursor-pointer transition-all ${
                  noticeType === 'BENEFICIARY_ENTITY_VALIDATION'
                    ? 'bg-gradient-to-b from-[#257843] to-[#144726] text-white font-bold border border-[#113C21] shadow-[var(--skeuo-btn)]'
                    : 'skeuo-btn text-[var(--text-secondary)]'
                }`}
              >
                4. UBO / Beneficiary
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
