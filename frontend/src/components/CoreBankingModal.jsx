import React, { useState } from 'react';
import { 
  Building2, 
  X, 
  ShieldAlert, 
  Lock, 
  CheckCircle2, 
  AlertTriangle, 
  Zap, 
  Server,
  ArrowRight,
  RefreshCw
} from 'lucide-react';
import { useAppStore } from '../lib/store';
import { Button } from './ui/Button';
import { Badge } from './ui/Badge';

export const CoreBankingModal = () => {
  const { 
    isCoreBankingModalOpen, 
    setCoreBankingModalOpen, 
    coreBankingActionSubject,
    triggerCoreBankingHold,
    addToast
  } = useAppStore();

  const [actionType, setActionType] = useState('TEMPORARY_DEBIT_HOLD');
  const [reasonCode, setReasonCode] = useState('MLPA_SECTION_15_ADMIN_HOLD');
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionResult, setExecutionResult] = useState(null);

  if (!isCoreBankingModalOpen) return null;

  const subject = coreBankingActionSubject ? {
    account: coreBankingActionSubject.account || coreBankingActionSubject.id || 'BD22-EBLB-4829-1092-8823',
    entityName: coreBankingActionSubject.entityName || coreBankingActionSubject.name || coreBankingActionSubject.label || 'Commercial Accountholder',
    amount: coreBankingActionSubject.amount || 48500,
    rail: coreBankingActionSubject.rail || 'SWIFT MT700 (Letter of Credit)',
    coreSystem: 'Finacle Core Banking v11.8 (EBL Motijheel Branch)'
  } : {
    account: 'BD22-EBLB-4829-1092-8823',
    entityName: 'Meghna Industrial & Agro Processing Ltd',
    amount: 48500,
    rail: 'SWIFT MT700 (Letter of Credit)',
    coreSystem: 'Finacle Core Banking v11.8 (EBL Motijheel Branch)'
  };

  const handleExecute = () => {
    setIsExecuting(true);
    setTimeout(() => {
      const res = triggerCoreBankingHold(subject.account, subject.amount, subject.rail, actionType);
      setIsExecuting(false);
      setExecutionResult(res);
    }, 700);
  };

  const handleClose = () => {
    setExecutionResult(null);
    setCoreBankingModalOpen(false);
  };

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-black/60 backdrop-blur-xs flex items-center justify-center p-4 animate-fadeIn">
      <div 
        className="w-full max-w-xl bg-surface border border-border rounded-xl shadow-2xl overflow-hidden flex flex-col text-xs"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-4 bg-surfaceRaised border-b border-border flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-critical/15 border border-critical/30 text-critical flex items-center justify-center font-bold">
              <Server className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-semibold text-text text-sm">Core Banking Ledger Integration</h3>
                <Badge variant="critical" size="sm">Live Webhook Dispatch</Badge>
              </div>
              <p className="text-[11px] text-text-muted mt-0.5">
                Execute direct debit restriction or restitution commands on connected core banking ledgers.
              </p>
            </div>
          </div>
          <button 
            onClick={handleClose}
            className="p-1 rounded text-text-muted hover:text-text hover:bg-surface transition-colors cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-5 space-y-4">
          {executionResult ? (
            <div className="p-4 rounded-lg bg-surfaceRaised border border-cleared space-y-3 animate-fadeIn">
              <div className="flex items-center gap-2 text-cleared font-semibold text-sm">
                <CheckCircle2 className="w-5 h-5" />
                <span>Core Ledger Webhook Acknowledged (HTTP 200 OK)</span>
              </div>
              <div className="space-y-1 font-mono text-[11px] bg-bg p-3 rounded border border-borderSubtle">
                <div className="flex justify-between">
                  <span className="text-text-muted">Target Account:</span>
                  <span className="text-text font-bold">{subject.account}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-text-muted">Ledger Action:</span>
                  <span className="text-critical font-bold">{actionType}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-text-muted">Authorization Code:</span>
                  <span className="text-accent font-bold">{executionResult.authCode}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-text-muted">Host Response:</span>
                  <span className="text-cleared font-bold">POST /api/v2/core-ledger/holds SUCCESS</span>
                </div>
              </div>
              <p className="text-text-2 text-[11px]">
                The transaction instruction and account debit privileges have been restricted on the core host. All corresponding clearing queues (RTGS, BEFTN, SWIFT) will reject debit settlement.
              </p>
            </div>
          ) : (
            <>
              {/* Target Entity Overview */}
              <div className="p-3.5 bg-bg rounded-lg border border-borderSubtle font-mono text-[11px] space-y-1.5">
                <div className="flex justify-between">
                  <span className="text-text-muted">Target Accountholder:</span>
                  <span className="font-semibold text-text">{subject.entityName}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-text-muted">Account Number:</span>
                  <span className="text-accent font-bold">{subject.account}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-text-muted">Connected Core Host:</span>
                  <span className="text-text">Finacle Core Banking v11.8 (EBL Cluster #04)</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-text-muted">Clearing Exposure:</span>
                  <span className="text-text font-bold">${Number(subject.amount || 48500).toLocaleString()} USD (৳{(Number(subject.amount || 48500) * 120).toLocaleString()} BDT)</span>
                </div>
              </div>

              {/* Action Selection */}
              <div className="space-y-2">
                <label className="text-text font-semibold text-xs block">
                  Select Ledger Command:
                </label>
                <div className="grid grid-cols-2 gap-2 font-mono text-[11px]">
                  <button
                    type="button"
                    onClick={() => setActionType('TEMPORARY_DEBIT_HOLD')}
                    className={`p-2.5 rounded border text-left cursor-pointer transition-all ${
                      actionType === 'TEMPORARY_DEBIT_HOLD'
                        ? 'bg-critical/10 border-critical text-critical font-bold'
                        : 'bg-surfaceRaised border-border text-text hover:bg-surfaceHover'
                    }`}
                  >
                    <span className="block font-sans font-semibold text-xs mb-0.5">Temporary Debit Hold</span>
                    <span className="text-[10px] text-text-muted block font-mono">Locks outgoing debits, credits permitted</span>
                  </button>

                  <button
                    type="button"
                    onClick={() => setActionType('TOTAL_LEDGER_FREEZE')}
                    className={`p-2.5 rounded border text-left cursor-pointer transition-all ${
                      actionType === 'TOTAL_LEDGER_FREEZE'
                        ? 'bg-critical/10 border-critical text-critical font-bold'
                        : 'bg-surfaceRaised border-border text-text hover:bg-surfaceHover'
                    }`}
                  >
                    <span className="block font-sans font-semibold text-xs mb-0.5">Total Account Freeze</span>
                    <span className="text-[10px] text-text-muted block font-mono">BFIU Section 15 total statutory block</span>
                  </button>
                </div>
              </div>

              {/* Reason Code */}
              <div className="space-y-1">
                <label htmlFor="core-banking-reason-code" className="text-text font-semibold text-xs block cursor-pointer">
                  Statutory Regulatory Justification:
                </label>
                <select
                  id="core-banking-reason-code"
                  name="core-banking-reason-code"
                  aria-label="Statutory Regulatory Justification"
                  value={reasonCode}
                  onChange={(e) => setReasonCode(e.target.value)}
                  className="ui-input w-full h-8 text-xs font-mono"
                >
                  <option value="MLPA_SECTION_15_ADMIN_HOLD">BFIU MLPA 2012 §15 — Administrative Pre-Filing Freeze (72h)</option>
                  <option value="CTR_STRUCTURING_HOLD">Structuring / Smurfing Pattern Trigger (31 CFR § 1010.311)</option>
                  <option value="TBML_NBR_ASYCUDA_OVERINVOICE">Trade-Based Money Laundering Valuation Discrepancy</option>
                  <option value="SANCTIONS_INTERDICTION">Correspondent Interdiction &amp; Sanctions Screening Positive</option>
                </select>
              </div>

              {/* Warning Notice */}
              <div className="p-3 rounded-lg bg-surfaceRaised border border-border flex items-start gap-2.5 text-[11px] text-text-2 leading-relaxed">
                <AlertTriangle className="w-4 h-4 text-review shrink-0 mt-0.5" />
                <div>
                  <strong>Live System Warning:</strong> Triggering this action dispatches an authenticated JSON webhook to the Core Banking host gateway. It immediately blocks clearing settlement on the core ledger.
                </div>
              </div>
            </>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 bg-surfaceRaised border-t border-border flex items-center justify-between">
          <Button
            variant="secondary"
            size="sm"
            onClick={handleClose}
          >
            {executionResult ? 'Close' : 'Cancel'}
          </Button>

          {!executionResult && (
            <Button
              variant="danger"
              size="sm"
              onClick={handleExecute}
              disabled={isExecuting}
              icon={Server}
            >
              {isExecuting ? 'Executing Core Webhook...' : 'Transmit Core Ledger Hold'}
            </Button>
          )}
        </div>
      </div>
    </div>
  );
};
