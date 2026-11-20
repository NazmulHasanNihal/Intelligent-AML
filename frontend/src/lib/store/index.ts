'use client';

import { create } from 'zustand';
import { BANKER_PERSONAS, BankingRole, BankerProfile } from '@/lib/auth/session';
import { AuditBlock, createChainedAuditEntry, getAuditChain } from '@/lib/audit/hashChain';

export interface ToastItem {
  id: string;
  title: string;
  message: string;
  type: 'info' | 'success' | 'critical' | 'accent';
}

export interface UnifiedBankingState {
  // Density and Theme
  density: 'comfortable' | 'compact';
  densityMode: 'comfortable' | 'compact';
  setDensity: (mode: 'comfortable' | 'compact') => void;
  setDensityMode: (mode: 'comfortable' | 'compact') => void;

  // Active Jurisdiction
  jurisdiction: string;
  activeJurisdiction: 'US_FINCEN' | 'BD_BFIU' | 'UN_GOAML';
  setJurisdiction: (j: string) => void;
  setActiveJurisdiction: (j: 'US_FINCEN' | 'BD_BFIU' | 'UN_GOAML') => void;

  // Active Banker & Role Switcher
  currentBanker: BankerProfile;
  session: {
    role: BankingRole;
    userName: string;
    institution: string;
  };
  switchBankerRole: (role: BankingRole) => void;
  isRoleModalOpen: boolean;
  setRoleModalOpen: (open: boolean) => void;

  // 4-Eyes Dual Sign-off Modal
  isFourEyesModalOpen: boolean;
  fourEyesTargetAction: string | null;
  fourEyesTargetAccount: string | null;
  fourEyesDetails: any;
  fourEyesOnApproved: (() => void) | null;
  openFourEyesModal: (action: string, account: string, onApproved?: () => void) => void;
  closeFourEyesModal: () => void;
  setFourEyesModalOpen: (open: boolean, config?: any) => void;

  // Ingestion Stream Controls
  isLiveStreamActive: boolean;
  isStreamRunning: boolean;
  streamSpeed: number;
  toggleLiveStream: () => void;
  toggleStreamRunning: () => void;
  setStreamSpeed: (speed: number) => void;
  consumerLag: number;
  liveTransactions: any[];

  // Toast Notifications
  toasts: ToastItem[];
  addToast: (title: string, message: string, type?: ToastItem['type']) => void;
  removeToast: (id: string) => void;

  // WORM Audit Ledger
  auditLedger: AuditBlock[];
  logAuditAction: (action: string, details: string, targetAccount?: string, makerName?: string, checkerName?: string) => Promise<void>;

  // Graph Studio Shared State
  camouflageDelta: number;
  setCamouflageDelta: (delta: number) => void;
  graphTimelineStep: number;
  setGraphTimelineStep: (step: number) => void;
  egoHopDistance: number;
  setEgoHopDistance: (hops: number) => void;
}

export const useAppStore = create<UnifiedBankingState>((set, get) => ({
  density: 'compact',
  densityMode: 'compact',
  setDensity: (mode) => set({ density: mode, densityMode: mode }),
  setDensityMode: (mode) => set({ density: mode, densityMode: mode }),

  jurisdiction: 'BD_BFIU',
  activeJurisdiction: 'BD_BFIU',
  setJurisdiction: (j) => set({ jurisdiction: j, activeJurisdiction: j as any }),
  setActiveJurisdiction: (j) => set({ jurisdiction: j, activeJurisdiction: j }),

  currentBanker: BANKER_PERSONAS.INVESTIGATOR_L2,
  session: {
    role: 'INVESTIGATOR_L2',
    userName: 'Sarah L. Jenkins, CFE',
    institution: 'Citibank N.A. — High-Risk Surveillance Hub'
  },
  switchBankerRole: (role) => {
    const profile = BANKER_PERSONAS[role];
    set({
      currentBanker: profile,
      session: {
        role,
        userName: profile.name,
        institution: profile.institution
      }
    });
  },
  isRoleModalOpen: false,
  setRoleModalOpen: (open) => set({ isRoleModalOpen: open }),

  isFourEyesModalOpen: false,
  fourEyesTargetAction: null,
  fourEyesTargetAccount: null,
  fourEyesDetails: null,
  fourEyesOnApproved: null,
  openFourEyesModal: (action, account, onApproved) => set({
    isFourEyesModalOpen: true,
    fourEyesTargetAction: action,
    fourEyesTargetAccount: account,
    fourEyesOnApproved: onApproved || null
  }),
  closeFourEyesModal: () => set({
    isFourEyesModalOpen: false,
    fourEyesTargetAction: null,
    fourEyesTargetAccount: null,
    fourEyesDetails: null,
    fourEyesOnApproved: null
  }),
  setFourEyesModalOpen: (open, config) => set({
    isFourEyesModalOpen: open,
    fourEyesDetails: config || null,
    fourEyesTargetAction: config?.actionTitle || null,
    fourEyesTargetAccount: config?.targetId || null
  }),

  isLiveStreamActive: true,
  isStreamRunning: true,
  streamSpeed: 1,
  toggleLiveStream: () => set((s) => ({ isLiveStreamActive: !s.isLiveStreamActive, isStreamRunning: !s.isStreamRunning })),
  toggleStreamRunning: () => set((s) => ({ isLiveStreamActive: !s.isLiveStreamActive, isStreamRunning: !s.isStreamRunning })),
  setStreamSpeed: (speed) => set({ streamSpeed: speed }),
  consumerLag: 0.82,
  liveTransactions: [],

  toasts: [],
  addToast: (title, message, type = 'info') => {
    const id = `toast-${Date.now()}-${Math.random().toString(36).substr(2, 4)}`;
    set((s) => ({ toasts: [...s.toasts, { id, title, message, type }] }));
    setTimeout(() => {
      get().removeToast(id);
    }, 4500);
  },
  removeToast: (id) => set((s) => ({ toasts: s.toasts.filter((t) => t.id !== id) })),

  auditLedger: getAuditChain(),
  logAuditAction: async (action, details, targetAccount = 'GENERAL', makerName, checkerName) => {
    const last = get().auditLedger[get().auditLedger.length - 1];
    const prevHash = last ? (last.currentHash || last.merkleHash) : '0'.repeat(64);
    const height = (last?.blockHeight || 1) + 1;
    const current = get().currentBanker;

    const newBlock = await createChainedAuditEntry(
      prevHash,
      height,
      action,
      makerName || current.name,
      current.id,
      targetAccount,
      'REG_MANDATE',
      details,
      checkerName || null
    );

    set((s) => ({ auditLedger: [...s.auditLedger, newBlock] }));
  },

  camouflageDelta: 0.10,
  setCamouflageDelta: (delta) => set({ camouflageDelta: delta }),
  graphTimelineStep: 100,
  setGraphTimelineStep: (step) => set({ graphTimelineStep: step }),
  egoHopDistance: 2,
  setEgoHopDistance: (hops) => set({ egoHopDistance: hops })
}));

export const useBankingStore = useAppStore;
