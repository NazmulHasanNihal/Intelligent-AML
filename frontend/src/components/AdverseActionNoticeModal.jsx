import React, { useState } from 'react';
import { 
  FileText, 
  X, 
  Download, 
  Printer, 
  ShieldCheck, 
  AlertTriangle, 
  Send, 
  Check, 
  Copy,
  Building2,
  Calendar,
  Phone
} from 'lucide-react';
import { useAppStore } from '../lib/store';
import { Button } from './ui/Button';
import { Badge } from './ui/Badge';

export const AdverseActionNoticeModal = () => {
  const { 
    isAdverseActionOpen, 
    setAdverseActionOpen, 
    adverseActionSubject,
    addToast,
    logAuditAction
  } = useAppStore();

  const [copied, setCopied] = useState(false);
  const [recipientEmail, setRecipientEmail] = useState('compliance-liaison@meghna-agro.com');

  if (!isAdverseActionOpen) return null;

  const subject = adverseActionSubject ? {
    account: adverseActionSubject.account || adverseActionSubject.id || 'BD22-EBLB-4829-1092-8823',
    entityName: adverseActionSubject.entityName || adverseActionSubject.name || adverseActionSubject.label || 'Commercial Accountholder',
    amount: adverseActionSubject.amount || 48500,
    caseId: adverseActionSubject.caseId || 'CASE-2026-0881',
    rail: adverseActionSubject.rail || 'SWIFT MT700 (Letter of Credit)',
    reasonCode: 'CDD-TBML-PRICE-DISCREPANCY'
  } : {
    account: 'BD22-EBLB-4829-1092-8823',
    entityName: 'Meghna Industrial & Agro Processing Ltd',
    amount: 48500,
    caseId: 'CASE-2026-0881',
    rail: 'SWIFT MT700 (Letter of Credit)',
    reasonCode: 'CDD-TBML-PRICE-DISCREPANCY'
  };

  const noticeDate = new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  const referenceCode = `ADV-ACT-${subject.caseId?.replace('CASE-', '') || '2026-0881'}-${Math.floor(1000 + Math.random() * 9000)}`;

  const letterText = `FORMAL NOTICE OF TEMPORARY TRANSACTION HOLD & ADVERSE ACTION
Reference Code: ${referenceCode}
Issuance Date: ${noticeDate}
Governing Regulation: Section 615(a) Fair Credit Reporting Act (15 U.S.C. § 1681m) / CFPB Circular 2022-03 / BFIU Circular 26

TO:
${subject.entityName}
Account Number: ${subject.account}

RE: NOTICE CONCERNING TEMPORARY PROCESSING RESTRICTION
Transaction Reference: Outbound Wire / Clearing Settlement
Amount: $${Number(subject.amount || 48500).toLocaleString()} USD (৳${(Number(subject.amount || 48500) * 120).toLocaleString()} BDT)
Clearing Rail: ${subject.rail || 'SWIFT Interbank Rail'}

Dear Valued Customer,

Pursuant to applicable commercial banking regulations and consumer protection transparency requirements, we are writing to notify you that our automated trade compliance verification system has placed a temporary administrative processing hold on the transaction referenced above.

REASON FOR ADVERSE ACTION / TEMPORARY HOLD:
Our institutional clearing network identified that the invoice valuation and commodity unit pricing submitted for Letter of Credit customs documentation diverge materially from prevailing market benchmarks established in national foreign trade records (NBR ASYCUDA customs valuation index). Additionally, high-frequency outbound settlement instructions across interbank conduits require enhanced customer due diligence (CDD).

YOUR RIGHT TO DISPUTE AND ADMINISTRATIVE APPEAL:
Under CFPB guidance and statutory trade regulations, you have the absolute right to know the basis of this temporary hold and to provide authenticating commercial documentation to rectify this determination without prejudice:

1. Right to File an Expedited Appeal:
   You may submit an administrative dispute or request for immediate reconsideration within thirty (30) business days from the receipt of this notice.

2. Supporting Documentation Required to Release Hold:
   To release this hold and enable Straight-Through Processing (STP) on your account, please submit:
   • Authenticated Export Monitoring (EXP) Form and original Bill of Lading.
   • Executed commercial sales invoice detailing itemized commodity specifications.
   • Proof of beneficial ownership and customs clearance certificates.

3. Submission Channels:
   • Secure Commercial Banking Portal: Upload directly via your authorized enterprise portal docket.
   • Institutional Compliance Desk: Email supporting documentation to cdd-appeals@bankclearing.com referencing docket ${referenceCode}.
   • Dedicated Appeals Hotline: +880 (2) 958-8812 / 1-800-492-8801.

STATEMENT OF REGULATORY NON-DISCRIMINATION:
The Federal Equal Credit Opportunity Act and Bangladesh Bank core banking regulations prohibit creditors and financial institutions from discriminating against applicants or accountholders on the basis of race, color, religion, national origin, sex, marital status, or age.

Sincerely,
Division of Institutional Compliance & Regulatory Governance
Authorized Dealer Correspondent Banking Network`;

  const handleCopyNotice = () => {
    navigator.clipboard.writeText(letterText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
    addToast('Notice Copied', 'Adverse action plain-language text copied.', 'info');
  };

  const handleDispatchNotice = () => {
    logAuditAction(
      'ADVERSE_ACTION_NOTICE_DISPATCHED',
      `CFPB / FCRA adverse action notice dispatched to ${subject.entityName} (${subject.account}) via secure channel. Ref: ${referenceCode}`,
      subject.account,
      'Compliance Officer'
    );
    addToast('Adverse Action Dispatched', `Notice successfully transmitted to customer email and core banking inbox.`, 'success');
    setAdverseActionOpen(false);
  };

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-black/60 backdrop-blur-xs flex items-center justify-center p-4 animate-fadeIn">
      <div 
        className="w-full max-w-3xl bg-surface border border-border rounded-xl shadow-2xl overflow-hidden flex flex-col text-xs"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-4 bg-surfaceRaised border-b border-border flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-cleared/15 border border-cleared/30 text-cleared flex items-center justify-center font-bold">
              <FileText className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-semibold text-text text-sm">Adverse Action &amp; Customer Appeal Notice</h3>
                <Badge variant="cleared" size="sm">CFPB / FCRA § 615(a) Compliant</Badge>
              </div>
              <p className="text-[11px] text-text-muted mt-0.5">
                Transparent statutory notice explaining transaction holds with customer appeal and dispute instructions.
              </p>
            </div>
          </div>
          <button 
            onClick={() => setAdverseActionOpen(false)}
            className="p-1 rounded text-text-muted hover:text-text hover:bg-surface transition-colors cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content Preview */}
        <div className="p-5 space-y-4 overflow-y-auto max-h-[70vh]">
          {/* Metadata Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 font-mono text-[11px] bg-bg p-3 rounded-lg border border-borderSubtle">
            <div>
              <span className="text-text-muted block text-[10px]">DOCKET REF</span>
              <span className="font-bold text-accent">{referenceCode}</span>
            </div>
            <div>
              <span className="text-text-muted block text-[10px]">AFFECTED AMOUNT</span>
              <span className="font-bold text-text">${Number(subject.amount || 48500).toLocaleString()} USD</span>
            </div>
            <div>
              <span className="text-text-muted block text-[10px]">APPEAL WINDOW</span>
              <span className="font-bold text-review">30 Business Days</span>
            </div>
            <div>
              <span className="text-text-muted block text-[10px]">TIPPING-OFF STATUS</span>
              <span className="font-bold text-cleared">Safe-Harbor Verified</span>
            </div>
          </div>

          {/* Letter Body Preview (Parchment Styled Card) */}
          <div className="p-5 rounded-lg bg-surfaceRaised border border-border font-mono text-[11px] leading-relaxed whitespace-pre-wrap select-text text-text">
            {letterText}
          </div>

          {/* Customer Delivery Config */}
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 p-3 bg-bg rounded-lg border border-border">
            <div className="flex items-center gap-2 flex-1">
              <label htmlFor="adverse-notice-email" className="text-text-muted font-medium shrink-0 cursor-pointer">Recipient Delivery:</label>
              <input 
                id="adverse-notice-email"
                name="adverse-notice-email"
                aria-label="Recipient Delivery Email"
                type="email"
                value={recipientEmail}
                onChange={(e) => setRecipientEmail(e.target.value)}
                className="ui-input h-7 text-xs font-mono flex-1"
                placeholder="customer@domain.com"
              />
            </div>
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={handleCopyNotice}
                icon={copied ? Check : Copy}
                className="h-7 text-xs"
              >
                {copied ? 'Copied' : 'Copy Text'}
              </Button>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 bg-surfaceRaised border-t border-border flex items-center justify-between">
          <Button
            variant="outline"
            size="sm"
            onClick={() => window.print()}
            icon={Printer}
          >
            Print Notice
          </Button>

          <div className="flex items-center gap-2">
            <Button
              variant="secondary"
              size="sm"
              onClick={() => setAdverseActionOpen(false)}
            >
              Close
            </Button>
            <Button
              variant="primary"
              size="sm"
              onClick={handleDispatchNotice}
              icon={Send}
            >
              Dispatch Notice to Customer
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};
