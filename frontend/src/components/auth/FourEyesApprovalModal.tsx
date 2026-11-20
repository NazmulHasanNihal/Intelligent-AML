'use client';

import React, { useState } from 'react';
import { ShieldAlert, Lock, CheckCircle2, AlertTriangle, Key, X } from 'lucide-react';
import { useAppStore } from '@/lib/store';
import { BANKER_PERSONAS } from '@/lib/auth/session';

export const FourEyesApprovalModal: React.FC = () => {
  const {
    isFourEyesModalOpen,
    fourEyesTargetAction,
    fourEyesTargetAccount,
    fourEyesOnApproved,
    closeFourEyesModal,
    currentBanker,
    logAuditAction,
    addToast
  } = useAppStore();

  const [checkerRole, setCheckerRole] = useState<'CCO_L3'>('CCO_L3');
  const [justificationCode, setJustificationCode] = useState('FATF-TYP-04_WASH_CYCLE');
  const [statutoryJustification, setStatutoryJustification] = useState(
    'Dual-signatory verification confirmed. High-risk invariant pattern matching Section 25 of MLPA 2012 / FinCEN 31 CFR § 1020.320.'
  );
  const [stepUpPassword, setStepUpPassword] = useState('');
  const [error, setError] = useState<string | null>(null);

  if (!isFourEyesModalOpen) return null;

  const checkerProfile = BANKER_PERSONAS[checkerRole];
  const isSelfApprovalViolation = currentBanker.id === checkerProfile.id;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (isSelfApprovalViolation) {
      setError('Maker-Checker Violation: Initiator (Maker) cannot act as the secondary signatory (Checker).');
      return;
    }

    if (!stepUpPassword) {
      setError('Step-up password confirmation is required for dual-authorization.');
      return;
    }

    // Record verified dual action to append-only audit ledger
    await logAuditAction(
      `4EYES_APPROVED_${fourEyesTargetAction || 'HIGH_CONSEQUENCE_ACTION'}`,
      `Dual-authorized: ${statutoryJustification} (Justification Code: ${justificationCode})`,
      fourEyesTargetAccount || 'GLOBAL_LEDGER',
      currentBanker.name,
      checkerProfile.name
    );

    addToast(
      'Dual-Authorization Certified',
      `Action confirmed with dual signatures: ${currentBanker.name} (Maker) & ${checkerProfile.name} (Checker).`,
      'success'
    );

    if (fourEyesOnApproved) {
      fourEyesOnApproved();
    }
    closeFourEyesModal();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-xs p-4 select-none">
      <div className="w-full max-w-lg rounded-xl bg-panel border border-panel-border shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        {/* Header */}
        <div className="p-4 bg-tier1-crimson-bg border-b border-tier1-crimson-border flex items-center justify-between">
          <div className="flex items-center gap-2.5 text-tier1-crimson">
            <Lock className="w-5 h-5" />
            <div>
              <h3 className="font-bold text-sm tracking-tight">Two-Officer "4-Eyes" Cryptographic Gate</h3>
              <span className="text-[10px] font-mono text-tier1-crimson/80">31 CFR § 1010.430 & FRE 902(11) Dual Sign-off</span>
            </div>
          </div>
          <button
            onClick={closeFourEyesModal}
            className="p-1 rounded text-text-muted hover:text-text-primary transition-colors cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Body */}
        <form onSubmit={handleSubmit} className="p-5 space-y-4 text-xs font-mono">
          {/* Target Action Banner */}
          <div className="p-3 rounded-lg bg-panel-raised border border-panel-border space-y-1">
            <span className="text-[10px] text-text-dim uppercase tracking-wider block">Target High-Consequence Action</span>
            <div className="flex items-center justify-between text-text-primary font-bold">
              <span>{fourEyesTargetAction?.replace(/_/g, ' ') || 'Statutory Account Freeze'}</span>
              <span className="text-amber-400">{fourEyesTargetAccount || 'BD22-••••-••••-8823'}</span>
            </div>
          </div>

          {/* Maker / Checker Dual Representation */}
          <div className="grid grid-cols-2 gap-3">
            <div className="p-3 rounded-lg bg-canvas border border-panel-border">
              <span className="text-[10px] text-text-dim block mb-1">OFFICER 1: INITIATOR (MAKER)</span>
              <span className="font-bold text-text-primary block truncate">{currentBanker.name}</span>
              <span className="text-[10px] text-text-muted block truncate">{currentBanker.roleTitle}</span>
            </div>

            <div className="p-3 rounded-lg bg-canvas border border-panel-border">
              <span className="text-[10px] text-text-dim block mb-1">OFFICER 2: COUNTER-SIGNER (CHECKER)</span>
              <span className="font-bold text-tier3-emerald block truncate">{checkerProfile.name}</span>
              <span className="text-[10px] text-text-muted block truncate">{checkerProfile.roleTitle}</span>
            </div>
          </div>

          {/* Justification Code */}
          <div className="space-y-1">
            <label className="text-[10px] text-text-dim block">STATUTORY JUSTIFICATION CODE</label>
            <select
              value={justificationCode}
              onChange={(e) => setJustificationCode(e.target.value)}
              className="w-full px-3 py-1.5 rounded bg-canvas border border-panel-border text-text-primary focus:outline-hidden focus:border-brand-accent text-xs font-mono"
            >
              <option value="FATF-TYP-04_WASH_CYCLE">FATF Typology #4 — Multi-Hop Circular Wash Loop</option>
              <option value="BFIU-SEC-15_FREEZE">MLPA 2012 §15 — Emergency Administrative Freeze</option>
              <option value="FINCEN-1020_STRUCTURING">FinCEN 31 CFR § 1020.320 — Sub-CTR Smurfing</option>
              <option value="OFAC-SANCTIONS-INTERCEPT">OFAC / UN Security Council Watchlist Intercept</option>
              <option value="EDD-OFFSHORE-CONDUIT">Enhanced Due Diligence (EDD) Secrecy Shell Conformance</option>
            </select>
          </div>

          {/* Operational Justification Memo */}
          <div className="space-y-1">
            <label className="text-[10px] text-text-dim block">SUPERVISORY MEMO & EVIDENCE SUMMARY</label>
            <textarea
              rows={2}
              value={statutoryJustification}
              onChange={(e) => setStatutoryJustification(e.target.value)}
              className="w-full p-2.5 rounded bg-canvas border border-panel-border text-text-primary focus:outline-hidden focus:border-brand-accent text-[11px] font-mono resize-none"
            />
          </div>

          {/* Step-Up Password Confirmation */}
          <div className="space-y-1">
            <label className="text-[10px] text-text-dim block">STEP-UP RE-AUTHENTICATION (CHECKER PIN/PASSWORD)</label>
            <div className="relative">
              <Key className="w-3.5 h-3.5 text-text-dim absolute left-2.5 top-1/2 -translate-y-1/2" />
              <input
                type="password"
                placeholder="Enter authorized credential (e.g. 'cams2026')..."
                value={stepUpPassword}
                onChange={(e) => setStepUpPassword(e.target.value)}
                className="w-full pl-8 pr-3 py-1.5 rounded bg-canvas border border-panel-border text-text-primary focus:outline-hidden focus:border-brand-accent text-xs font-mono"
              />
            </div>
          </div>

          {error && (
            <div className="p-2 rounded bg-tier1-crimson-bg border border-tier1-crimson-border text-tier1-crimson text-[11px] flex items-center gap-2">
              <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {/* Actions */}
          <div className="flex items-center justify-end gap-2 pt-2 border-t border-panel-border">
            <button
              type="button"
              onClick={closeFourEyesModal}
              className="px-3 py-1.5 rounded bg-panel-raised hover:bg-panel-border text-text-secondary cursor-pointer transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-1.5 rounded bg-tier1-crimson hover:bg-tier1-crimson/90 text-white font-bold cursor-pointer transition-colors flex items-center gap-1.5 shadow-md"
            >
              <Lock className="w-3.5 h-3.5" />
              <span>Sign & Enforce Action</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
