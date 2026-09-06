import React, { useState } from 'react';
import { 
  X, 
  Lock, 
  Unlock, 
  ShieldAlert, 
  ShieldCheck, 
  Check, 
  AlertOctagon, 
  CheckCircle2, 
  FileText,
  Clock,
  Shield
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const BankerActionModal = ({ isOpen, onClose, actionData, onActionConfirmed }) => {
  const { currentBanker, logBankerAction } = useAuth();
  const [reasonCode, setReasonCode] = useState('STRUCTURING_CTR_EVASION');
  const [reason, setReason] = useState('');
  const [selectedChecker, setSelectedChecker] = useState('BNK-4029'); // Marcus Vance CCO
  const [coreWebhookAction, setCoreWebhookAction] = useState('WEBHOOK_DEBIT_HOLD');
  const [rfiDispatched, setRfiDispatched] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);

  if (!isOpen || !actionData) return null;

  const { type, target } = actionData;
  const targetLabel = target?.holderName || target?.src || target?.accountNumber || 'Account Target';
  const targetId = target?.accountNumber || target?.src || target?.id || 'ACC_8823';

  const REASON_CODES = [
    { code: 'STRUCTURING_CTR_EVASION', label: 'Structuring to Evade CTR (31 U.S.C. § 5324)' },
    { code: 'LAYERED_MULE_CIRCUIT', label: 'Layered Mule Conduit (Hawkes Burst λ > 10 tx/min)' },
    { code: 'OFAC_SDN_SANCTIONS_MATCH', label: 'OFAC SDN or International Watchlist Match' },
    { code: 'HIGH_RISK_CORRIDOR', label: 'Unregistered Offshore Corridor (BVI / Panama Transit)' },
    { code: 'CLEAN_COMMERCIAL_INVOICE', label: 'Verified Trade Documentation & Validated UBO' },
    { code: 'ROUTINE_PAYROLL_SWEEP', label: 'Corporate Liquidity Management / Verified Payroll' }
  ];

  const ACTION_CONFIGS = {
    FREEZE_ACCOUNT: {
      title: 'Emergency Account Quarantine & Fund Freeze',
      icon: <Lock className="w-5 h-5 text-rose-400" />,
      headerClass: 'bg-rose-950/40 border-rose-500/30',
      btnClass: 'bg-rose-600 hover:bg-rose-500 text-white',
      btnLabel: 'Execute Four-Eyes Quarantine',
      defaultReason: 'Flagged for cyclic wash trading loop and rapid structuring below CTR threshold.',
      statute: 'Bank Secrecy Act § 5318(g) / OFAC Freezing Standard'
    },
    RELEASE_HOLD: {
      title: 'Release Compliance Administrative Hold',
      icon: <Unlock className="w-5 h-5 text-emerald-400" />,
      headerClass: 'bg-emerald-950/40 border-emerald-500/30',
      btnClass: 'bg-emerald-600 hover:bg-emerald-500 text-white',
      btnLabel: 'Authorize Fund Release',
      defaultReason: 'Customer provided verified commercial invoice and legitimate source of funds.',
      statute: 'Verified KYC Tier-3 Clean Disposition'
    },
    WHITELIST_COUNTERPARTY: {
      title: 'Add Counterparty to Trusted Whitelist',
      icon: <ShieldCheck className="w-5 h-5 text-indigo-400" />,
      headerClass: 'bg-indigo-950/40 border-indigo-500/30',
      btnClass: 'bg-indigo-600 hover:bg-indigo-500 text-white',
      btnLabel: 'Add to Institution Whitelist',
      defaultReason: 'Regular verified business supplier with established 3-year track record.',
      statute: 'Trusted Beneficiary Clearing Rail'
    },
    MARK_FALSE_POSITIVE: {
      title: 'Dismiss Alert & Mark as False Positive',
      icon: <CheckCircle2 className="w-5 h-5 text-slate-300" />,
      headerClass: 'bg-slate-900 border-white/[0.08]',
      btnClass: 'bg-slate-700 hover:bg-slate-600 text-white',
      btnLabel: 'Dismiss & Calibrate Model',
      defaultReason: 'Known legitimate payroll batch or utility treasury sweep.',
      statute: 'Internal FIU Disposition Review'
    }
  };

  const config = ACTION_CONFIGS[type] || ACTION_CONFIGS.FREEZE_ACCOUNT;

  const isMakerOnly = currentBanker.id === 'BNK-7701'; // Analyst L1 needs Checker

  const handleDispatchRFI = () => {
    logBankerAction(
      'DISPATCH_SECURE_RFI_LINK',
      `Secure document upload link generated and dispatched to ${targetId}: https://compliance.bank.com/rfi/upload?token=9f8e4b7a12c8`,
      { accountId: targetId }
    );
    setRfiDispatched(true);
    setTimeout(() => setRfiDispatched(false), 3000);
  };

  const handleConfirm = () => {
    setIsSubmitting(true);
    const finalReason = `${reasonCode}: ${reason || config.defaultReason}`;

    logBankerAction({
      action: type,
      targetAccount: `${targetId} (${targetLabel})`,
      reason: finalReason,
      maker: `${currentBanker.name} (${currentBanker.id})`,
      checker: isMakerOnly ? `Pending Co-Signature by ${selectedChecker}` : 'Approved by Senior Compliance Officer',
      coreBankingWebhook: coreWebhookAction,
      merkleProof: '9f8e4b7a12c85d6e3f019a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d'
    });

    setTimeout(() => {
      setIsSubmitting(false);
      setSuccess(true);
      setTimeout(() => {
        setSuccess(false);
        setReason('');
        if (onActionConfirmed) onActionConfirmed(type, target);
        onClose();
      }, 1500);
    }, 600);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-black/60 backdrop-blur-sm animate-fadeIn select-none">
      <div className="w-full max-w-lg bg-[var(--bg-card)] border border-[var(--border-card)] rounded-2xl shadow-2xl overflow-hidden flex flex-col skeuo-card max-h-[92vh] overflow-y-auto">
        
        {/* Modal Header */}
        <div className={`p-3.5 sm:p-4 border-b flex items-center justify-between ${config.headerClass}`}>
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="p-2 rounded-lg bg-[var(--bg-card)] border border-[var(--border-subtle)] shadow-[var(--skeuo-btn)]">
              {config.icon}
            </div>
            <div className="min-w-0">
              <h3 className="text-xs sm:text-sm font-bold text-[var(--text-primary)] font-sans truncate">{config.title}</h3>
              <p className="text-[10px] text-[var(--text-muted)] font-sans truncate">{config.statute}</p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg skeuo-btn text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-all cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-3.5 sm:p-4 space-y-3 font-sans text-xs">
          {/* Subject Identification */}
          <div className="p-2.5 rounded-xl skeuo-well space-y-0.5 font-mono">
            <div className="text-[9px] text-[var(--text-muted)] uppercase">SUBJECT ENTITY:</div>
            <div className="font-bold text-[var(--text-primary)] text-xs truncate">{targetLabel}</div>
            <div className="text-[10px] sm:text-[11px] text-[var(--accent-primary)] truncate">{targetId}</div>
          </div>

          {/* Maker-Checker Governance Protocol */}
          <div className="p-2.5 rounded-xl bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)] space-y-2 font-mono text-[10px]">
            <div className="flex items-center justify-between font-bold text-[var(--text-primary)]">
              <span className="flex items-center gap-1.5">
                <Shield className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                MAKER-CHECKER DUAL AUTHORIZATION (FOUR-EYES)
              </span>
              <span className="text-[9px] px-1.5 py-0.2 rounded bg-[var(--accent-primary)]/10 text-[var(--accent-primary)] border border-[var(--accent-primary)]/20">
                EU AI Act Mandated
              </span>
            </div>

            <div className="grid grid-cols-2 gap-2 text-[10px]">
              <div className="p-2 rounded-lg skeuo-well">
                <span className="text-[8px] text-[var(--text-muted)] block">1. INITIATING MAKER:</span>
                <span className="font-bold text-[var(--text-primary)] block truncate">{currentBanker.name}</span>
                <span className="text-[8px] text-[var(--accent-primary)]">{currentBanker.id} • {currentBanker.roleTitle.split(' ')[0]}</span>
              </div>

              <div className="p-2 rounded-lg skeuo-well">
                <span className="text-[8px] text-[var(--text-muted)] block">2. MANAGERIAL CHECKER:</span>
                {isMakerOnly ? (
                  <select 
                    value={selectedChecker}
                    onChange={(e) => setSelectedChecker(e.target.value)}
                    className="w-full bg-[var(--bg-base)] border border-[var(--border-subtle)] rounded text-[9px] text-[var(--text-primary)] font-mono p-1 mt-0.5 outline-none"
                  >
                    <option value="BNK-4029">Marcus Vance (CCO L3)</option>
                    <option value="BNK-1044">Sarah Jenkins (Senior L2)</option>
                    <option value="BNK-3091">Dr. Evelyn Reed (Auditor)</option>
                  </select>
                ) : (
                  <div>
                    <span className="font-bold text-emerald-600 dark:text-emerald-400 block truncate">✓ Manager Co-Sign Ready</span>
                    <span className="text-[8px] text-[var(--text-muted)]">Authorized L2/L3 Clearance</span>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Standard Audit Reason Codes */}
          <div className="space-y-1 font-mono text-[10px]">
            <label className="text-[9px] text-[var(--text-secondary)] font-bold block uppercase">
              Standard Regulatory Reason Code:
            </label>
            <select
              value={reasonCode}
              onChange={(e) => setReasonCode(e.target.value)}
              className="w-full p-2 rounded-lg bg-[var(--bg-base)] border border-[var(--border-card)] text-[var(--text-primary)] text-[10px] font-mono focus:border-[var(--accent-primary)] outline-none shadow-inner"
            >
              {REASON_CODES.map((rc) => (
                <option key={rc.code} value={rc.code}>{rc.label}</option>
              ))}
            </select>
          </div>

          {/* Compliance Justification Memo */}
          <div className="space-y-1">
            <label className="text-[10px] sm:text-[11px] font-semibold text-[var(--text-secondary)] block font-mono">
              Officer Rationale &amp; Evidence Memo:
            </label>
            <textarea
              rows={2}
              placeholder={config.defaultReason}
              value={reason}
              onChange={e => setReason(e.target.value)}
              className="w-full p-2.5 rounded-xl bg-[var(--bg-base)] border border-[var(--border-card)] text-[var(--text-primary)] font-sans text-xs focus:outline-none focus:border-[var(--accent-primary)] placeholder-[var(--text-muted)] resize-none shadow-inner"
            />
          </div>

          {/* Core Banking Webhook Action Trigger */}
          <div className="p-2 rounded-xl bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)] space-y-1.5 font-mono text-[10px]">
            <div className="flex items-center justify-between">
              <span className="text-[9px] font-bold text-[var(--text-secondary)] uppercase">CORE BANKING API WEBHOOK:</span>
              <button
                type="button"
                onClick={handleDispatchRFI}
                className="text-[9px] text-[var(--accent-primary)] hover:underline font-bold"
              >
                {rfiDispatched ? '✓ RFI Upload Link Sent!' : 'Dispatch Customer RFI Link'}
              </button>
            </div>
            <div className="grid grid-cols-3 gap-1.5 text-[9px]">
              <label className={`p-1.5 rounded-lg border text-center cursor-pointer transition-all ${
                coreWebhookAction === 'WEBHOOK_DEBIT_HOLD' ? 'bg-rose-500/15 border-rose-500/40 text-rose-600 dark:text-rose-400 font-bold' : 'border-[var(--border-subtle)] text-[var(--text-muted)]'
              }`}>
                <input 
                  type="radio" 
                  name="webhook" 
                  checked={coreWebhookAction === 'WEBHOOK_DEBIT_HOLD'} 
                  onChange={() => setCoreWebhookAction('WEBHOOK_DEBIT_HOLD')}
                  className="sr-only"
                />
                Debit Hold (SWIFT)
              </label>

              <label className={`p-1.5 rounded-lg border text-center cursor-pointer transition-all ${
                coreWebhookAction === 'WEBHOOK_MONITORING' ? 'bg-amber-500/15 border-amber-500/40 text-amber-700 dark:text-amber-300 font-bold' : 'border-[var(--border-subtle)] text-[var(--text-muted)]'
              }`}>
                <input 
                  type="radio" 
                  name="webhook" 
                  checked={coreWebhookAction === 'WEBHOOK_MONITORING'} 
                  onChange={() => setCoreWebhookAction('WEBHOOK_MONITORING')}
                  className="sr-only"
                />
                Continuous Alarm
              </label>

              <label className={`p-1.5 rounded-lg border text-center cursor-pointer transition-all ${
                coreWebhookAction === 'WEBHOOK_RELEASE_FUNDS' ? 'bg-emerald-500/15 border-emerald-500/40 text-emerald-700 dark:text-emerald-300 font-bold' : 'border-[var(--border-subtle)] text-[var(--text-muted)]'
              }`}>
                <input 
                  type="radio" 
                  name="webhook" 
                  checked={coreWebhookAction === 'WEBHOOK_RELEASE_FUNDS'} 
                  onChange={() => setCoreWebhookAction('WEBHOOK_RELEASE_FUNDS')}
                  className="sr-only"
                />
                Release &amp; Whitelist
              </label>
            </div>
          </div>

          {success && (
            <div className="p-2 rounded-lg bg-emerald-500/20 border border-emerald-500/40 text-[var(--accent-primary)] text-xs font-mono text-center flex items-center justify-center gap-1.5">
              <Check className="w-3.5 h-3.5" />
              <span>Four-Eyes Authorization Stamped &amp; Webhooks Dispatched!</span>
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="p-3 sm:p-3.5 bg-[var(--bg-card-elevated)] border-t border-[var(--border-subtle)] flex items-center justify-end gap-2">
          <button
            onClick={onClose}
            className="px-3 py-1.5 rounded-lg skeuo-btn skeuo-btn-secondary text-xs font-medium cursor-pointer"
          >
            Cancel
          </button>

          <button
            onClick={handleConfirm}
            disabled={isSubmitting || success}
            className={`px-3.5 py-1.5 rounded-lg font-bold text-xs flex items-center gap-1.5 cursor-pointer transition-all active:scale-[0.98] ${
              type === 'FREEZE_ACCOUNT' ? 'skeuo-btn skeuo-btn-danger' : 'skeuo-btn skeuo-btn-primary'
            }`}
          >
            <span>{isSubmitting ? 'Recording Audit Stamp...' : config.btnLabel}</span>
          </button>
        </div>

      </div>
    </div>
  );
};
