import React, { createContext, useContext, useState } from 'react';

const BANKER_PROFILES = [
  {
    id: 'BNK-7842',
    name: 'Nazmul Hasan, CAMS',
    role: 'admin',
    roleTitle: 'Chief Compliance Officer (CCO)',
    department: 'Global Financial Crimes Division',
    institution: 'JPMorgan Chase & Co.',
    avatar: 'NH',
    badgeClass: 'bg-indigo-500/20 text-indigo-300 border-indigo-500/40',
    permissions: ['all', 'freeze_funds', 'release_funds', 'file_sar', 'send_notices', 'model_governance', 'manage_users']
  },
  {
    id: 'BNK-4419',
    name: 'Sarah L. Jenkins, CFE',
    role: 'investigator',
    roleTitle: 'Senior AML Compliance Officer',
    department: 'Special Investigations Unit (SIU)',
    institution: 'Citibank N.A.',
    avatar: 'SJ',
    badgeClass: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40',
    permissions: ['triage', 'freeze_funds', 'release_funds', 'draft_sar', 'send_notices', 'rfi_request']
  },
  {
    id: 'BNK-1092',
    name: 'Musrat Jahan Gungun',
    role: 'analyst',
    roleTitle: 'Tier-1 Triage Analyst (Analyst L1)',
    department: 'First-Line Surveillance Desk',
    institution: 'Standard Chartered Bank',
    avatar: 'MJ',
    badgeClass: 'bg-amber-500/20 text-amber-300 border-amber-500/40',
    permissions: ['triage_read', 'investigate_read', 'draft_notes']
  },
  {
    id: 'BNK-3091',
    name: 'Dr. Evelyn Reed, PhD',
    role: 'auditor',
    roleTitle: 'Model Risk & Supervisory Auditor (Auditor)',
    department: 'Model Risk Management (SR 11-7)',
    institution: 'Federal Reserve Supervisory Desk',
    avatar: 'ER',
    badgeClass: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40',
    permissions: ['all_read', 'model_governance', 'audit_inspect', 'export_scorecard']
  }
];

const INITIAL_AUDIT_LOGS = [
  {
    id: 'AUD-90124',
    timestamp: '2026-09-02 08:14:22 UTC',
    bankerId: 'BNK-7842',
    bankerName: 'Nazmul Hasan, CAMS',
    role: 'admin',
    roleTitle: 'Chief Compliance Officer (CCO)',
    action: 'EMERGENCY_ACCOUNT_FREEZE',
    targetAccount: 'US-JPMC-4829-1092-8823 (Apex Global Logistics)',
    reason: 'Suspicious 3-hop layering wash loop matching FATF Red Flag #4',
    merkleHash: '8f92a1c0d3e4b5a6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0'
  },
  {
    id: 'AUD-90123',
    timestamp: '2026-09-02 07:58:10 UTC',
    bankerId: 'BNK-4419',
    bankerName: 'Sarah L. Jenkins, CFE',
    role: 'investigator',
    roleTitle: 'Senior AML Compliance Officer',
    action: 'CUSTOMER_RFI_NOTICE_DISPATCHED',
    targetAccount: 'GB-BARC-9921-3841-1109 (Elena Rostova)',
    reason: 'Requested Commercial Invoice & Bill of Lading for $82,000 pending wire',
    merkleHash: '3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b'
  },
  {
    id: 'AUD-90122',
    timestamp: '2026-09-02 07:42:05 UTC',
    bankerId: 'BNK-7842',
    bankerName: 'Nazmul Hasan, CAMS',
    role: 'admin',
    roleTitle: 'Chief Compliance Officer (CCO)',
    action: 'FINCEN_SAR_FORM111_APPROVED',
    targetAccount: 'AE-SCBL-5512-8891-4412 (Horizon Trading DMCC)',
    reason: 'Confirmed multi-layer pass-through conduit structuring $48,500',
    merkleHash: '9f8e4b7a12c85d6e3f019a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d'
  }
];

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [currentBanker, setCurrentBanker] = useState(BANKER_PROFILES[0]);
  const [auditLogs, setAuditLogs] = useState(INITIAL_AUDIT_LOGS);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [selectedInstitution, setSelectedInstitution] = useState('JPMorgan Chase & Co. — Global FIU Operations');

  const switchBanker = (bankerId) => {
    const found = BANKER_PROFILES.find(b => b.id === bankerId);
    if (found) {
      setCurrentBanker(found);
      logBankerAction({
        action: 'BANKER_SESSION_AUTHENTICATED',
        targetAccount: 'SYSTEM_CONSOLE',
        reason: `Officer ${found.name} (${found.roleTitle}) assumed active compliance session.`
      });
    }
  };

  const logBankerAction = ({ action, targetAccount, reason }) => {
    const newLog = {
      id: `AUD-${Math.floor(10000 + Math.random() * 90000)}`,
      timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19) + ' UTC',
      bankerId: currentBanker.id,
      bankerName: currentBanker.name,
      role: currentBanker.role,
      roleTitle: currentBanker.roleTitle,
      action,
      targetAccount,
      reason,
      merkleHash: Array.from({ length: 64 }, () => Math.floor(Math.random() * 16).toString(16)).join('')
    };

    setAuditLogs(prev => [newLog, ...prev]);
    return newLog;
  };

  const hasPermission = (permission) => {
    if (currentBanker.permissions.includes('all')) return true;
    return currentBanker.permissions.includes(permission);
  };

  return (
    <AuthContext.Provider
      value={{
        currentBanker,
        bankerProfiles: BANKER_PROFILES,
        availableBankers: BANKER_PROFILES,
        switchBanker,
        auditLogs,
        logBankerAction,
        hasPermission,
        isAuthModalOpen,
        setIsAuthModalOpen,
        selectedInstitution,
        setSelectedInstitution
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
