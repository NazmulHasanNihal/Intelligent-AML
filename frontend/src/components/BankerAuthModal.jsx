import React from 'react';
import { 
  X, 
  UserCheck, 
  ShieldCheck, 
  Key, 
  Building2, 
  Check, 
  ChevronRight,
  Lock,
  Sparkles
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const BankerAuthModal = ({ isOpen, onClose }) => {
  const { currentBanker, bankerProfiles, switchBanker, selectedInstitution, setSelectedInstitution } = useAuth();
  if (!isOpen) return null;

  const INSTITUTIONS = [
    'JPMorgan Chase & Co. — Global FIU Operations',
    'Citibank N.A. — AML Surveillance Division',
    'Standard Chartered Bank — Financial Crime Threat Unit',
    'Barclays Bank PLC — EMEA Clearing Operations',
    'HSBC Holdings — Global Anti-Money Laundering Group'
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-black/60 backdrop-blur-sm animate-fadeIn select-none">
      <div className="w-full max-w-md bg-[var(--bg-card)] border border-[var(--border-card)] rounded-2xl shadow-2xl overflow-hidden flex flex-col skeuo-card max-h-[92vh] overflow-y-auto">
        
        {/* Header */}
        <div className="p-3.5 sm:p-4 bg-[var(--bg-card-elevated)] border-b border-[var(--border-subtle)] flex items-center justify-between">
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-b from-[#257843] to-[#144726] border border-[#113C21] flex items-center justify-center text-white shrink-0 shadow-[var(--skeuo-btn)]">
              <Key className="w-4 h-4 text-white" />
            </div>
            <div className="min-w-0">
              <h3 className="text-xs sm:text-sm font-bold text-[var(--text-primary)] font-sans truncate">Banker Auth &amp; Role Switcher</h3>
              <p className="text-[10px] text-[var(--text-muted)] font-sans truncate">
                Role-Based Access Control (RBAC) &amp; Compliance Attribution
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg skeuo-btn text-[var(--text-muted)] hover:text-[var(--text-primary)] cursor-pointer"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Body */}
        <div className="p-3.5 sm:p-4 space-y-3 font-sans text-xs">
          {/* Institution Selector */}
          <div>
            <label className="text-[10px] sm:text-[11px] font-semibold text-[var(--text-muted)] block mb-1 font-mono uppercase">
              Financial Institution / Branch:
            </label>
            <select
              value={selectedInstitution}
              onChange={e => setSelectedInstitution(e.target.value)}
              className="w-full bg-[var(--bg-base)] border border-[var(--border-card)] rounded-xl px-2.5 py-1.5 text-xs text-[var(--text-primary)] focus:outline-none focus:border-[var(--accent-primary)] font-medium shadow-inner"
            >
              {INSTITUTIONS.map(inst => (
                <option key={inst} value={inst}>{inst}</option>
              ))}
            </select>
          </div>

          {/* User Persona Profiles */}
          <div className="space-y-1.5">
            <label className="text-[10px] sm:text-[11px] font-semibold text-[var(--text-muted)] block font-mono uppercase">
              Select Active Officer Persona:
            </label>

            <div className="space-y-1.5">
              {bankerProfiles.map(profile => {
                const isActive = currentBanker.id === profile.id;
                return (
                  <div
                    key={profile.id}
                    onClick={() => {
                      switchBanker(profile.id);
                    }}
                    className={`p-2.5 rounded-xl border cursor-pointer transition-all flex items-center justify-between ${
                      isActive 
                        ? 'bg-[var(--accent-primary)]/15 border-[var(--accent-primary)] shadow-sm' 
                        : 'skeuo-card hover:bg-black/[0.02] dark:hover:bg-white/[0.03]'
                    }`}
                  >
                    <div className="flex items-center gap-2.5 min-w-0">
                      <div className={`w-8 h-8 rounded-lg flex items-center justify-center font-bold text-xs shrink-0 ${profile.badgeClass}`}>
                        {profile.avatar}
                      </div>
                      <div className="min-w-0">
                        <div className="flex items-center gap-1.5">
                          <span className="font-bold text-[var(--text-primary)] text-xs truncate">{profile.name}</span>
                          <span className="text-[9px] font-mono text-[var(--text-muted)]">({profile.id})</span>
                        </div>
                        <p className="text-[10px] sm:text-[11px] text-[var(--accent-primary)] font-sans truncate">{profile.roleTitle}</p>
                        <p className="text-[9px] sm:text-[10px] text-[var(--text-muted)] font-sans truncate">{profile.department}</p>
                      </div>
                    </div>

                    <div className="flex items-center gap-1.5 shrink-0 ml-2">
                      {isActive ? (
                        <div className="w-5 h-5 rounded-full bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-[var(--accent-primary)]">
                          <Check className="w-3 h-3" />
                        </div>
                      ) : (
                        <ChevronRight className="w-3.5 h-3.5 text-[var(--text-muted)]" />
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="p-2.5 rounded-xl skeuo-well flex items-center gap-2 text-[10px] sm:text-[11px] text-[var(--text-secondary)]">
            <Lock className="w-3.5 h-3.5 text-[var(--accent-primary)] shrink-0" />
            <span>
              All actions signed and attributed to <b>{currentBanker.name}</b> in the audit trail.
            </span>
          </div>
        </div>

        {/* Footer */}
        <div className="p-3 sm:p-3.5 bg-[var(--bg-card-elevated)] border-t border-[var(--border-subtle)] flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-lg skeuo-btn skeuo-btn-primary font-bold text-xs cursor-pointer shadow-md transition-all"
          >
            Confirm &amp; Proceed
          </button>
        </div>

      </div>
    </div>
  );
};
