'use client';

import React from 'react';
import { UserCheck, ShieldCheck, Lock, X } from 'lucide-react';
import { useAppStore } from '@/lib/store';
import { BANKER_PERSONAS, BankingRole } from '@/lib/auth/session';

export const RoleSwitchModal: React.FC = () => {
  const { isRoleModalOpen, setRoleModalOpen, currentBanker, switchBankerRole } = useAppStore();

  if (!isRoleModalOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-xs p-4 select-none">
      <div className="w-full max-w-xl rounded-xl bg-panel border border-panel-border shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        {/* Header */}
        <div className="p-4 bg-panel-raised border-b border-panel-border flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <UserCheck className="w-5 h-5 text-brand-accent" />
            <div>
              <h3 className="font-bold text-sm tracking-tight text-text-primary">
                Authorized Signatory Role Delegation (RBAC)
              </h3>
              <span className="text-xs font-mono text-text-muted">
                Keycloak OIDC / FIPS 140-2 Level 3 Persona Session
              </span>
            </div>
          </div>
          <button
            onClick={() => setRoleModalOpen(false)}
            className="p-1 rounded text-text-muted hover:text-text-primary transition-colors cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Personas List */}
        <div className="p-4 space-y-3 font-mono text-xs">
          {(Object.keys(BANKER_PERSONAS) as BankingRole[]).map((roleKey) => {
            const persona = BANKER_PERSONAS[roleKey];
            const isCurrent = currentBanker.role === roleKey;

            return (
              <div
                key={roleKey}
                onClick={() => switchBankerRole(roleKey)}
                className={`p-3 rounded-lg border cursor-pointer transition-all ${
                  isCurrent
                    ? 'bg-brand-accent/10 border-brand-accent shadow-xs ring-1 ring-brand-accent/40'
                    : 'bg-canvas hover:bg-panel-raised border-panel-border'
                }`}
              >
                <div className="flex items-start justify-between gap-2 mb-1">
                  <div className="flex items-center gap-2">
                    <div className="w-6 h-6 rounded-full bg-brand-accent/20 border border-brand-accent/40 text-brand-accent font-bold text-xs flex items-center justify-center">
                      {persona.avatar}
                    </div>
                    <div>
                      <span className="font-bold text-text-primary text-xs block">
                        {persona.name}
                      </span>
                      <span className="text-xs text-text-muted block">
                        {persona.institution}
                      </span>
                    </div>
                  </div>
                  <span
                    className={`px-2 py-0.5 rounded text-xs font-bold ${
                      isCurrent
                        ? 'bg-brand-accent text-white'
                        : 'bg-panel-raised text-text-dim border border-panel-border'
                    }`}
                  >
                    {isCurrent ? 'ACTIVE SESSION' : roleKey}
                  </span>
                </div>

                <div className="mt-2 text-xs text-text-secondary leading-tight">
                  <strong className="text-text-primary">{persona.roleTitle}</strong>
                </div>

                <div className="mt-2 pt-2 border-t border-panel-border/50 flex flex-wrap gap-1">
                  {persona.permissions.map((p) => (
                    <span
                      key={p}
                      className="px-1.5 py-0.2 rounded text-xs bg-panel-raised text-text-dim border border-panel-border"
                    >
                      {p}
                    </span>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
