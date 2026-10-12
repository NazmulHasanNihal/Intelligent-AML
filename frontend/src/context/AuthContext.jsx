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
    initiatorName: 'Sarah L. Jenkins, CFE (Senior Investigator)',
    approverName: 'Nazmul Hasan, CAMS (Chief Compliance Officer)',
    fourEyesVerified: true,
    action: 'EMERGENCY_ACCOUNT_FREEZE',
    targetAccount: 'US-JPMC-4829-1092-8823 (Apex Global Logistics Ltd)',
    reason: 'Dual-Authorized: 4-hop wash loop ($48,500) matching FATF Typology #4 & FinCEN 31 CFR § 1020.320',
    reasonCode: 'FATF-TYP-04_WASH_CYCLE',
    merkleHash: '8f92a1c0d3e4b5a6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0'
  },
  {
    id: 'AUD-90123',
    timestamp: '2026-09-02 07:58:10 UTC',
    bankerId: 'BNK-4419',
    bankerName: 'Sarah L. Jenkins, CFE',
    role: 'investigator',
    roleTitle: 'Senior AML Compliance Officer',
    initiatorName: 'Sarah L. Jenkins, CFE (Senior Investigator)',
    approverName: 'Self-Authorized (L2 Delegation Limit)',
    fourEyesVerified: true,
    action: 'CUSTOMER_RFI_NOTICE_DISPATCHED',
    targetAccount: 'GB-BARC-1109-8832-9011 (Elena Rostova)',
    reason: 'Compliant Source of Funds & Invoicing RFI issued for $48,500 wire under 31 U.S.C. § 5318(g)(2) tipping-off safeguards',
    reasonCode: 'RFI_SOURCE_OF_FUNDS',
    merkleHash: '3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b'
  },
  {
    id: 'AUD-90122',
    timestamp: '2026-09-02 07:42:05 UTC',
    bankerId: 'BNK-7842',
    bankerName: 'Nazmul Hasan, CAMS',
    role: 'admin',
    roleTitle: 'Chief Compliance Officer (CCO)',
    initiatorName: 'Sarah L. Jenkins, CFE (Senior Investigator)',
    approverName: 'Nazmul Hasan, CAMS (Chief Compliance Officer)',
    fourEyesVerified: true,
    action: 'FINCEN_SAR_FORM111_APPROVED',
    targetAccount: 'AE-SCBL-5512-8891-4412 (Horizon Trading DMCC)',
    reason: 'Dual-Authorized: Verified pass-through conduit structuring $48,500. Form 111 XML signed under 31 CFR § 1020.320.',
    reasonCode: 'FINCEN_FORM111_DUAL_AUTH',
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

  const logBankerAction = (arg1, arg2, arg3) => {
    let action, targetAccount, reason, initiatorName, approverName, reasonCode, fourEyesVerified;

    if (typeof arg1 === 'object' && arg1 !== null) {
      ({ action, targetAccount, reason, initiatorName, approverName, reasonCode, fourEyesVerified } = arg1);
    } else {
      action = arg1;
      reason = typeof arg2 === 'string' ? arg2 : (arg2 ? JSON.stringify(arg2) : 'Action recorded by compliance officer');
      if (typeof arg3 === 'string') {
        targetAccount = arg3;
      } else if (typeof arg3 === 'object' && arg3 !== null) {
        targetAccount = arg3.targetAccount || arg3.accountId || (arg3.ids ? `Batch (${arg3.count || arg3.ids.length} items)` : (arg3.model ? `Model: ${arg3.model}` : JSON.stringify(arg3)));
      } else {
        targetAccount = 'GLOBAL_POLICY_GATEWAY';
      }
    }

    const bankerId = currentBanker?.id || 'BNK-7842';
    const bankerName = currentBanker?.name || 'Authorized Compliance Officer';
    const bankerRole = currentBanker?.role || 'admin';
    const bankerRoleTitle = currentBanker?.roleTitle || 'Compliance Officer';

    const newLog = {
      id: `AUD-${Math.floor(10000 + Math.random() * 90000)}`,
      timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19) + ' UTC',
      bankerId,
      bankerName,
      role: bankerRole,
      roleTitle: bankerRoleTitle,
      initiatorName: initiatorName || (bankerRole === 'admin' ? 'Sarah L. Jenkins, CFE (Senior Investigator)' : `${bankerName} (${bankerRoleTitle})`),
      approverName: approverName || (bankerRole === 'admin' ? `${bankerName} (CCO Dual-Approval)` : 'Nazmul Hasan, CAMS (CCO Counter-Signature)'),
      fourEyesVerified: fourEyesVerified ?? true,
      reasonCode: reasonCode || 'COMPLIANCE_OPERATIONAL_LOG',
      action: action || 'COMPLIANCE_ACTION_LOGGED',
      targetAccount: targetAccount || 'ACCOUNT_TRANSACTION_EVENT',
      reason: reason || 'Operation recorded under regulatory compliance framework.',
      merkleHash: Array.from({ length: 64 }, () => Math.floor(Math.random() * 16).toString(16)).join('')
    };

    setAuditLogs(prev => [newLog, ...prev]);
    return newLog;
  };

  const hasPermission = (permission) => {
    if (!currentBanker || !currentBanker.permissions) return true;
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
