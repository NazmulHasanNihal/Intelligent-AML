'use client';

import React, { useState } from 'react';
import { Lock, AlertTriangle, Key, X } from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { BANKER_PERSONAS } from '@/lib/auth/session';
import { JURISDICTIONS } from '@/lib/compliance/jurisdictions';

export const FourEyesApprovalModal: React.FC = () => {
  const {
    isFourEyesModalOpen,
    fourEyesTargetAction,
    fourEyesTargetAccount,
    fourEyesOnApproved,
    closeFourEyesModal,
    currentBanker,
    activeJurisdiction,
    logAuditAction,
    addToast,
  } = useBankingStore();

  const [checkerRole] = useState<'CCO_L3'>('CCO_L3');
  const [justificationCode, setJustificationCode] = useState('BFIU-SEC-15_FREEZE');
  const [statutoryJustification, setStatutoryJustification] = useState(
    'Dual-signatory verification confirmed under maker-checker controls.'
  );
  const [stepUpPassword, setStepUpPassword] = useState('');
  const [error, setError] = useState<string | null>(null);

  if (!isFourEyesModalOpen) return null;

  const jurProfile = JURISDICTIONS[activeJurisdiction] || JURISDICTIONS.BD_BFIU;
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
    <div
      role="dialog"
      aria-modal="true"
      aria-label="Four-eyes approval"
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 backdrop-blur-xs p-4 select-none"
    >
      <div className="w-full max-w-lg rounded-xl bg-panel border border-line shadow-2xl overflow-hidden text-fg">
        <div className="p-4 bg-tier-1-bg border-b border-tier-1-border flex items-center justify-between gap-3">
          <div className="flex items-center gap-2.5 text-tier-1-text min-w-0">
            <Lock className="w-5 h-5 shrink-0" aria-hidden="true" />
            <div className="min-w-0">
              <h3 className="font-semibold text-sm tracking-tight text-fg">Two-Officer &ldquo;4-Eyes&rdquo; Cryptographic Gate</h3>
              <span className="text-xs font-mono text-tier-1-text block truncate">
                {jurProfile.evidenceRule}
              </span>
            </div>
          </div>
          <button
            type="button"
            onClick={closeFourEyesModal}
            aria-label="Close approval gate"
            className="p-1.5 rounded-lg text-muted hover:text-fg hover:bg-surface-hover transition-colors cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-5 space-y-4 text-xs font-mono">
          <div className="p-3 rounded-lg bg-surface border border-line space-y-1">
            <span className="text-xs text-muted block">Target high-consequence action</span>
            <div className="flex items-center justify-between gap-2 text-fg font-semibold">
              <span>{fourEyesTargetAction?.replace(/_/g, ' ') || 'Statutory Account Freeze'}</span>
              <span className="text-tier-2-text">{fourEyesTargetAccount || 'BD22-••••-••••-8823'}</span>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div className="p-3 rounded-lg bg-surface border border-line">
              <span className="text-xs text-muted block mb-1">Officer 1 · Initiator (Maker)</span>
              <span className="font-semibold text-fg block truncate">{currentBanker.name}</span>
              <span className="text-xs text-muted block truncate">{currentBanker.roleTitle}</span>
            </div>

            <div className="p-3 rounded-lg bg-surface border border-line">
              <span className="text-xs text-muted block mb-1">Officer 2 · Checker</span>
              <span className="font-semibold text-accent-text block truncate">{checkerProfile.name}</span>
              <span className="text-xs text-muted block truncate">{checkerProfile.roleTitle}</span>
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-xs text-muted block">Statutory justification code</label>
            <select
              value={justificationCode}
              onChange={(e) => setJustificationCode(e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-surface border border-line text-fg focus:outline-none focus:border-accent text-xs font-mono cursor-pointer"
            >
              <option value="BFIU-SEC-15_FREEZE">MLPA 2012 § 15 — Administrative Hold / Freeze</option>
              <option value="FATF-TYP-04_WASH_CYCLE">FATF Typology #4 — Circular Pass-Through Conduit</option>
              <option value="BFIU-TBML-24">BFIU Circular 24 — TBML Over-Invoicing Divergence</option>
              <option value="OFAC-SANCTIONS-INTERCEPT">OFAC / UN Security Council Watchlist Intercept</option>
              <option value="EDD-OFFSHORE-CONDUIT">Enhanced Due Diligence (EDD) Conformance</option>
            </select>
          </div>

          <div className="space-y-1">
            <label className="text-xs text-muted block">Supervisory memo &amp; evidence summary</label>
            <textarea
              rows={2}
              value={statutoryJustification}
              onChange={(e) => setStatutoryJustification(e.target.value)}
              className="w-full p-2.5 rounded-lg bg-surface border border-line text-fg focus:outline-none focus:border-accent text-xs font-mono resize-none"
            />
          </div>

          <div className="space-y-1">
            <label className="text-xs text-muted block">Step-up re-authentication (Checker credential)</label>
            <div className="relative">
              <Key className="w-3.5 h-3.5 text-muted absolute left-3 top-1/2 -translate-y-1/2" aria-hidden="true" />
              <input
                type="password"
                placeholder="Enter authorized credential (e.g. 'cams2026')..."
                value={stepUpPassword}
                onChange={(e) => setStepUpPassword(e.target.value)}
                className="w-full pl-9 pr-3 py-2 rounded-lg bg-surface border border-line text-fg focus:outline-none focus:border-accent text-xs font-mono"
              />
            </div>
          </div>

          {error && (
            <div className="p-2.5 rounded-lg bg-tier-1-bg border border-tier-1-border text-tier-1-text text-xs flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 shrink-0" aria-hidden="true" />
              <span>{error}</span>
            </div>
          )}

          <div className="flex items-center justify-end gap-2 pt-3 border-t border-line">
            <button
              type="button"
              onClick={closeFourEyesModal}
              className="px-3 py-2 rounded-lg bg-surface hover:bg-surface-hover text-fg-secondary border border-line cursor-pointer transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 rounded-lg bg-tier-1 hover:opacity-90 text-white font-semibold cursor-pointer transition-opacity flex items-center gap-1.5 shadow-sm"
            >
              <Lock className="w-3.5 h-3.5" aria-hidden="true" />
              <span>Sign &amp; Enforce Action</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
