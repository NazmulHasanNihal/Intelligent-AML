'use client';

import React from 'react';
import { UserCheck, X } from 'lucide-react';
import { useAppStore } from '@/lib/store';
import { BANKER_PERSONAS, BankingRole } from '@/lib/auth/session';

export const RoleSwitchModal: React.FC = () => {
  const { isRoleModalOpen, setRoleModalOpen, currentBanker, switchBankerRole } = useAppStore();

  if (!isRoleModalOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-xs p-4 select-none"
      onClick={() => setRoleModalOpen(false)}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-label="Authorized signatory role delegation"
        onClick={(e) => e.stopPropagation()}
        className="w-full max-w-xl rounded-xl bg-panel border border-line shadow-2xl overflow-hidden text-fg"
      >
        <div className="p-4 bg-surface border-b border-line flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <UserCheck className="w-5 h-5 text-accent-text" aria-hidden="true" />
            <div>
              <h3 className="font-semibold text-sm tracking-tight text-fg">
                Authorized Signatory Role Delegation (RBAC)
              </h3>
              <span className="text-xs font-mono text-muted">
                OIDC Maker-Checker Role Session
              </span>
            </div>
          </div>
          <button
            type="button"
            onClick={() => setRoleModalOpen(false)}
            aria-label="Close role switcher"
            className="p-1.5 rounded-lg text-muted hover:text-fg hover:bg-surface-hover transition-colors cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="p-4 space-y-3 font-mono text-xs max-h-[75vh] overflow-y-auto">
          {(Object.keys(BANKER_PERSONAS) as BankingRole[]).map((roleKey) => {
            const persona = BANKER_PERSONAS[roleKey];
            const isCurrent = currentBanker.role === roleKey;

            return (
              <button
                key={roleKey}
                type="button"
                onClick={() => switchBankerRole(roleKey)}
                className={`w-full text-left p-3 rounded-xl border cursor-pointer transition-colors ${
                  isCurrent
                    ? 'bg-accent-subtle border-accent/50 ring-1 ring-accent/30'
                    : 'bg-surface hover:bg-surface-hover border-line'
                }`}
              >
                <div className="flex items-start justify-between gap-2 mb-1">
                  <div className="flex items-center gap-2">
                    <div className="w-7 h-7 rounded-full bg-accent-subtle border border-accent/40 text-accent-text font-semibold text-xs flex items-center justify-center shrink-0">
                      {persona.avatar}
                    </div>
                    <div>
                      <span className="font-semibold text-fg text-xs block">{persona.name}</span>
                      <span className="text-xs text-muted block">{persona.institution}</span>
                    </div>
                  </div>
                  <span
                    className={`px-2 py-0.5 rounded-full text-xs font-semibold ${
                      isCurrent
                        ? 'bg-accent text-accent-fg'
                        : 'bg-panel text-muted border border-line'
                    }`}
                  >
                    {isCurrent ? 'ACTIVE' : roleKey}
                  </span>
                </div>

                <div className="mt-2 text-xs text-fg-secondary leading-tight">
                  <strong className="text-fg">{persona.roleTitle}</strong>
                </div>

                <div className="mt-2 pt-2 border-t border-line-subtle flex flex-wrap gap-1">
                  {persona.permissions.map((p) => (
                    <span
                      key={p}
                      className="px-1.5 py-0.5 rounded text-xs bg-panel text-muted border border-line"
                    >
                      {p}
                    </span>
                  ))}
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
};
