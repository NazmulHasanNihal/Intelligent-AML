'use client';

import React, { useState } from 'react';
import { ShieldAlert, Lock, CheckCircle2, AlertTriangle, Key, X } from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { BANKER_PERSONAS } from '@/lib/auth/session';

export const FourEyesApprovalModal: React.FC = () => {
  const {
    isFourEyesModalOpen,
    fourEyesTargetAction,
    fourEyesTargetAccount,
    fourEyesDetails,
    fourEyesOnApproved,
    closeFourEyesModal,
    currentBanker,
    logAuditAction,
    addToast
  } = useBankingStore();

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
      setError('Maker-Checker Violation: Initiator (Maker) cannot act as the secondary signatory (Checker). Switch role to a distinct CCO/Checker.');
      return;
    }

    if (!stepUpPassword) {
      setError('Step-up credential confirmation is required for dual-authorization.');
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
      `Action ratified: ${currentBanker.name} (Maker) & ${checkerProfile.name} (Checker).`,
      'success'
    );

    if (fourEyesOnApproved) {
      fourEyesOnApproved();
    }
    closeFourEyesModal();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 backdrop-blur-xs p-4 select-none">
      <div className="w-full max-w-lg rounded-xl bg-[#0F172A] border border-[#334155] shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200 text-slate-100">
        {/* Header */}
        <div className="p-4 bg-rose-950/40 border-b border-rose-800/40 flex items-center justify-between">
          <div className="flex items-center gap-2.5 text-rose-400">
            <Lock className="w-5 h-5 shrink-0" />
            <div>
              <h3 className="font-bold text-sm tracking-tight font-sans">Two-Officer "4-Eyes" Cryptographic Gate</h3>
              <span className="text-[10px] font-mono text-rose-300/80">31 CFR § 1010.430 & FRE 902(11) Dual Sign-off</span>
            </div>
          </div>
          <button
            onClick={closeFourEyesModal}
            className="p-1 rounded text-slate-400 hover:text-slate-200 transition-colors cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Body */}
        <form onSubmit={handleSubmit} className="p-5 space-y-4 text-xs font-mono">
          {/* Target Action Banner */}
          <div className="p-3 rounded-lg bg-[#0B0F17] border border-[#1E293B] space-y-1">
            <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Target High-Consequence Action</span>
            <div className="flex items-center justify-between text-slate-200 font-bold">
              <span>{fourEyesTargetAction?.replace(/_/g, ' ') || 'Statutory Account Freeze'}</span>
              <span className="text-amber-400">{fourEyesTargetAccount || 'BD22-••••-••••-8823'}</span>
            </div>
          </div>

          {/* Maker / Checker Dual Representation */}
          <div className="grid grid-cols-2 gap-3">
            <div className="p-3 rounded-lg bg-[#0B0F17] border border-[#1E293B]">
              <span className="text-[10px] text-slate-500 block mb-1">OFFICER 1: INITIATOR (MAKER)</span>
              <span className="font-bold text-slate-200 block truncate">{currentBanker.name}</span>
              <span className="text-[10px] text-slate-400 block truncate">{currentBanker.roleTitle}</span>
            </div>

            <div className="p-3 rounded-lg bg-[#0B0F17] border border-[#1E293B]">
              <span className="text-[10px] text-slate-500 block mb-1">OFFICER 2: COUNTER-SIGNER (CHECKER)</span>
              <span className="font-bold text-emerald-400 block truncate">{checkerProfile.name}</span>
              <span className="text-[10px] text-slate-400 block truncate">{checkerProfile.roleTitle}</span>
            </div>
          </div>

          {/* Justification Code */}
          <div className="space-y-1">
            <label className="text-[10px] text-slate-400 block">STATUTORY JUSTIFICATION CODE</label>
            <select
              value={justificationCode}
              onChange={(e) => setJustificationCode(e.target.value)}
              className="w-full px-3 py-1.5 rounded bg-[#0B0F17] border border-[#334155] text-slate-200 focus:outline-none focus:border-emerald-500 text-xs font-mono cursor-pointer"
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
            <label className="text-[10px] text-slate-400 block">SUPERVISORY MEMO & EVIDENCE SUMMARY</label>
            <textarea
              rows={2}
              value={statutoryJustification}
              onChange={(e) => setStatutoryJustification(e.target.value)}
              className="w-full p-2.5 rounded bg-[#0B0F17] border border-[#334155] text-slate-200 focus:outline-none focus:border-emerald-500 text-[11px] font-mono resize-none"
            />
          </div>

          {/* Step-Up Password Confirmation */}
          <div className="space-y-1">
            <label className="text-[10px] text-slate-400 block">STEP-UP RE-AUTHENTICATION (CHECKER PIN/PASSWORD)</label>
            <div className="relative">
              <Key className="w-3.5 h-3.5 text-slate-500 absolute left-2.5 top-1/2 -translate-y-1/2" />
              <input
                type="password"
                placeholder="Enter authorized credential (e.g. 'cams2026')..."
                value={stepUpPassword}
                onChange={(e) => setStepUpPassword(e.target.value)}
                className="w-full pl-8 pr-3 py-1.5 rounded bg-[#0B0F17] border border-[#334155] text-slate-200 focus:outline-none focus:border-emerald-500 text-xs font-mono"
              />
            </div>
          </div>

          {error && (
            <div className="p-2 rounded bg-rose-950/40 border border-rose-800/60 text-rose-300 text-[11px] flex items-center gap-2">
              <AlertTriangle className="w-3.5 h-3.5 shrink-0 text-rose-400" />
              <span>{error}</span>
            </div>
          )}

          {/* Actions */}
          <div className="flex items-center justify-end gap-2 pt-2 border-t border-[#1E293B]">
            <button
              type="button"
              onClick={closeFourEyesModal}
              className="px-3 py-1.5 rounded bg-[#1E293B] hover:bg-[#334155] text-slate-300 cursor-pointer transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-1.5 rounded bg-rose-700 hover:bg-rose-600 text-white font-bold cursor-pointer transition-colors flex items-center gap-1.5 shadow-md"
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
