import React from 'react';
import { 
  UserCheck, 
  X, 
  ShieldCheck, 
  Check, 
  Shield, 
  Lock,
  ArrowRight
} from 'lucide-react';
import { useAppStore } from '../lib/store';
import { useAuth } from '../context/AuthContext';
import { Button } from './ui/Button';
import { Badge } from './ui/Badge';

export const RoleSwitchModal = () => {
  const { isRoleModalOpen, setRoleModalOpen, addToast, logAuditAction } = useAppStore();
  const { currentBanker, availableBankers, switchBanker } = useAuth();

  if (!isRoleModalOpen) return null;

  const handleSelectRole = (bankerId) => {
    const selected = availableBankers.find(b => b.id === bankerId);
    if (!selected) return;

    switchBanker(bankerId);
    logAuditAction(
      'SESSION_SIGNATORY_ROLE_SWITCH',
      `Officer session delegated to ${selected.name} (${selected.roleTitle}). Delegation certified under Four-Eyes Dual Control.`,
      'Session Governance',
      selected.name
    );
    addToast('Signatory Role Switched', `Active session switched to ${selected.name} (${selected.roleTitle}).`, 'success');
    setRoleModalOpen(false);
  };

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-black/60 backdrop-blur-xs flex items-center justify-center p-4 animate-fadeIn">
      <div 
        className="w-full max-w-lg bg-surface border border-border rounded-xl shadow-2xl overflow-hidden flex flex-col text-xs"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-4 bg-surfaceRaised border-b border-border flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-accent/15 border border-accent/30 text-accent flex items-center justify-center font-bold">
              <UserCheck className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-semibold text-text text-sm">Authorized Signatory Delegation</h3>
                <Badge variant="accent" size="sm">Four-Eyes Dual Control</Badge>
              </div>
              <p className="text-[11px] text-text-muted mt-0.5">
                Switch between Maker (Investigator) and Checker (Chief Compliance Officer) roles.
              </p>
            </div>
          </div>
          <button 
            onClick={() => setRoleModalOpen(false)}
            className="p-1 rounded text-text-muted hover:text-text hover:bg-surface transition-colors cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Current Active Persona Banner */}
        <div className="px-5 py-3 bg-bg border-b border-borderSubtle flex items-center justify-between">
          <div>
            <span className="text-[10px] font-mono uppercase text-text-muted block">Active Signed-In Signatory</span>
            <span className="font-semibold text-text text-sm">{currentBanker.name}</span>
            <span className="text-[11px] text-accent block font-mono">{currentBanker.roleTitle}</span>
          </div>
          <Badge variant="cleared" size="sm">Active Session</Badge>
        </div>

        {/* Role Options */}
        <div className="p-5 space-y-3">
          <p className="text-text-2 text-xs">
            Select an authorized signatory identity to test dual-control sign-off workflows or maker-checker segregation of duties:
          </p>

          <div className="space-y-2">
            {(availableBankers || []).map((b) => {
              const isCurrent = b.id === currentBanker.id;
              const isMaker = b.role?.includes('INVESTIGATOR') || b.role?.includes('MAKER') || b.id.includes('jenkins') || b.name.includes('Sarah');

              return (
                <div
                  key={b.id}
                  onClick={() => handleSelectRole(b.id)}
                  className={`p-3.5 rounded-lg border transition-all cursor-pointer flex items-center justify-between gap-3 ${
                    isCurrent
                      ? 'bg-accent/10 border-accent shadow-xs'
                      : 'bg-surfaceRaised hover:bg-surfaceHover border-border'
                  }`}
                >
                  <div className="flex items-center gap-3 min-w-0">
                    <div className={`w-8 h-8 rounded-lg flex items-center justify-center font-bold text-xs font-mono shrink-0 ${
                      isCurrent ? 'bg-accent text-white' : 'bg-surface border border-border text-text'
                    }`}>
                      {b.avatar || (isMaker ? 'M' : 'C')}
                    </div>
                    <div className="min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-text text-xs truncate">{b.name}</span>
                        <Badge variant={isMaker ? 'accent' : 'critical'} size="sm">
                          {isMaker ? 'Maker (Level 1)' : 'Checker (Four-Eyes)'}
                        </Badge>
                      </div>
                      <p className="text-[11px] text-text-muted truncate mt-0.5">{b.roleTitle}</p>
                    </div>
                  </div>

                  <div className="shrink-0">
                    {isCurrent ? (
                      <span className="flex items-center gap-1 font-mono text-[11px] font-bold text-accent">
                        <Check className="w-3.5 h-3.5" />
                        <span>Active</span>
                      </span>
                    ) : (
                      <Button variant="outline" size="sm" className="h-7 text-xs">
                        Switch
                      </Button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Statutory Separation of Duties Notice */}
          <div className="p-3 rounded-lg bg-bg border border-border flex items-start gap-2 text-[11px] text-text-muted font-mono leading-relaxed mt-4">
            <Lock className="w-3.5 h-3.5 text-accent shrink-0 mt-0.5" />
            <div>
              <strong>Segregation of Duties (SOX § 404 / BFIU Circular 26):</strong> An investigator who initiates an alert or drafts a SAR cannot ratify their own filing. Dual-control requires a distinct Checker identity.
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 bg-surfaceRaised border-t border-border flex justify-end">
          <Button
            variant="secondary"
            size="sm"
            onClick={() => setRoleModalOpen(false)}
          >
            Close
          </Button>
        </div>
      </div>
    </div>
  );
};
