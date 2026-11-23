'use client';

import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { BANKER_PERSONAS, BankingRole, BankerProfile } from '@/lib/auth/session';
import { backendClient, BackendConnectionError } from '@/lib/api/backendClient';
import { IS_ONPREM_MODE, APP_MODE } from '@/lib/config/env';
import {
  AuditBlock,
  createChainedAuditEntry,
  getAuditChain,
  setAuditChain,
  tamperAuditBlock,
  restoreAuditChain
} from '@/lib/audit/hashChain';
import { JurisdictionCode, JURISDICTIONS } from '@/lib/compliance/jurisdictions';
import {
  CommercialAlert,
  CommercialCase,
  CommercialCustomer,
  WatchlistScreeningRecord,
  CashThresholdReport,
  generateFullAlertQueue,
  INITIAL_CASES,
  INITIAL_CUSTOMERS,
  INITIAL_SCREENING_RECORDS,
  INITIAL_CTR_RECORDS
} from '@/lib/data/commercialSeed';
import { screenWatchlistCandidate } from '@/lib/screening/watchlistRegistry';

export interface ToastItem {
  id: string;
  title: string;
  message: string;
  type: 'info' | 'success' | 'critical' | 'accent';
}

export interface NotificationItem {
  id: string;
  timestamp: string;
  title: string;
  description: string;
  type: 'SLA_WARNING' | 'FOUR_EYES_REQUEST' | 'RFI_UPLOAD' | 'SANCTIONS_INTERDICTION';
  read: boolean;
  linkedHref?: string;
}

export interface UnifiedBankingState {
  // Density and Theme
  density: 'comfortable' | 'compact';
  densityMode: 'comfortable' | 'compact';
  setDensity: (mode: 'comfortable' | 'compact') => void;
  setDensityMode: (mode: 'comfortable' | 'compact') => void;

  // Multi-Jurisdiction Engine
  jurisdiction: JurisdictionCode;
  activeJurisdiction: JurisdictionCode;
  setJurisdiction: (j: JurisdictionCode) => void;
  setActiveJurisdiction: (j: JurisdictionCode) => void;

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

  // Global PII Masking with Audited 60-Second Reveal
  piiRevealedUntil: number;
  revealPii: () => Promise<void>;
  isPiiRevealed: () => boolean;

  // Toast Notifications & Bell Drawer
  toasts: ToastItem[];
  addToast: (title: string, message: string, type?: ToastItem['type']) => void;
  removeToast: (id: string) => void;
  notifications: NotificationItem[];
  markNotificationRead: (id: string) => void;
  clearAllNotifications: () => void;

  // Command Palette
  isCommandPaletteOpen: boolean;
  setCommandPaletteOpen: (open: boolean) => void;

  // Notification Drawer
  isNotificationDrawerOpen: boolean;
  setNotificationDrawerOpen: (open: boolean) => void;

  // Collections (Single Source of Truth)
  alerts: CommercialAlert[];
  cases: CommercialCase[];
  customers: CommercialCustomer[];
  screeningRecords: WatchlistScreeningRecord[];
  ctrRecords: CashThresholdReport[];
  auditLedger: AuditBlock[];

  // Cross-Module Operational Actions
  freezeAccount: (accountId: string, reason: string) => Promise<void>;
  assignAlert: (alertId: string, assignee: string) => void;
  batchAssignAlerts: (alertIds: string[], assignee: string) => void;
  dismissAlert: (alertId: string, reason: string) => void;
  batchDismissAlerts: (alertIds: string[], reason: string) => void;
  escalateToCase: (alertIds: string[] | string, title?: string, slaHours?: number) => CommercialCase;
  createCase: (caseData: any) => CommercialCase;
  addAuditEntry: (entryOrAction: string | { eventType?: string; action?: string; entityId?: string; targetAccount?: string; details: string; actionBy?: string }, details?: string, targetAccount?: string) => Promise<void>;
  injectAlert: (alert: CommercialAlert) => void;
  addCaseNote: (caseId: string, note: string) => void;
  updateCaseMilestone: (caseId: string, milestoneIndex: number, status: 'COMPLETE' | 'IN_PROGRESS' | 'PENDING') => void;
  dispositionScreening: (recordId: string, disposition: WatchlistScreeningRecord['disposition'], reason?: string) => void;
  addScreeningSearch: (name: string, account?: string, country?: string, dob?: string, nationalId?: string) => WatchlistScreeningRecord;
  updateCustomerRiskRating: (customerId: string, newRating: CommercialCustomer['riskRating'], reason: string) => void;
  triggerEddRefresh: (customerId: string) => void;

  // WORM Audit & Tamper Test
  logAuditAction: (action: string, details: string, targetAccount?: string, makerName?: string, checkerName?: string) => Promise<void>;
  simulateTamperTest: (blockSequence: number) => void;
  restoreValidChain: () => void;

  // Graph Studio Shared State
  camouflageDelta: number;
  setCamouflageDelta: (delta: number) => void;
  graphTimelineStep: number;
  setGraphTimelineStep: (step: number) => void;
  egoHopDistance: number;
  setEgoHopDistance: (hops: number) => void;

  // Operational Environment & Backend Sync
  appMode: 'demo' | 'onprem';
  backendStatus: 'connected' | 'disconnected' | 'syncing' | 'idle';
  backendError: string | null;
  syncWithBackend: () => Promise<void>;

  // Reset to Pristine Certified Clean Workspace
  resetWorkspaceData: () => void;
}

export const useAppStore = create<UnifiedBankingState>()(
  persist(
    (set, get) => ({
      // Operational Environment & Backend Sync
      appMode: APP_MODE,
      backendStatus: 'idle',
      backendError: null,
      syncWithBackend: async () => {
        if (!IS_ONPREM_MODE) {
          set({ backendStatus: 'idle', backendError: null });
          return;
        }
        set({ backendStatus: 'syncing', backendError: null });
        try {
          const [alertsData, casesData] = await Promise.all([
            backendClient.getAlerts({ limit: 100 }),
            backendClient.getCases()
          ]);
          if (alertsData && alertsData.alerts) {
            const mappedAlerts: CommercialAlert[] = alertsData.alerts.map((a) => {
              const isT1 = a.tier === 'Tier 1' || a.tier.includes('1');
              const isT2 = a.tier === 'Tier 2' || a.tier.includes('2');
              return {
                id: a.id,
                timestamp: a.timestamp,
                account: a.target_account,
                entityName: a.target_account.includes('EBLB') ? 'Meghna Industrial & Agro' : 'Commercial Trading Client',
                amount: a.amount_usd,
                amountBdt: a.amount_usd * 120.0,
                rail: 'ISO 20022 RTGS',
                bic: 'EBLBBDDH',
                counterparty: a.counterparty,
                counterpartyName: 'Gulf Star Commodities FZE',
                counterpartyBic: 'EBILAEAD',
                counterpartyCountry: 'UAE',
                tier: isT1 ? 'Tier 1 Hold' : isT2 ? 'Tier 2 Review' : 'Tier 3 Clear',
                tierCode: isT1 ? 1 : isT2 ? 2 : 3,
                riskScore: a.risk_score,
                status: a.status === 'PENDING' ? 'PENDING_TRIAGE' : 'UNDER_INVESTIGATION',
                assignee: a.assignee || 'Unassigned',
                typology: a.typology,
                typologyBadge: a.typology.split(' ')[0] || 'CONDUIT',
                decisionSet: (a.conformal_set && a.conformal_set.length > 0) ? a.conformal_set.join(', ') : 'PASS_THROUGH_CONDUIT',
                slaMinutesLeft: 45,
                whyFlagged: 'Automated spatio-temporal flow conservation trigger and BFIU MLPA 2012 compliance review',
                flowConservationRatio: 0.992,
                velocityBurstScore: 3.84
              };
            });
            set({ alerts: mappedAlerts });
          }
          set({ backendStatus: 'connected', backendError: null });
        } catch (err: any) {
          set({
            backendStatus: 'disconnected',
            backendError: err.message || 'Failed to connect to authoritative backend'
          });
          if (IS_ONPREM_MODE) {
            throw err;
          }
        }
      },
      // Density and Theme
      density: 'compact',
      densityMode: 'compact',
      setDensity: (mode) => set({ density: mode, densityMode: mode }),
      setDensityMode: (mode) => set({ density: mode, densityMode: mode }),

      // Active Jurisdiction (Default BFIU)
      jurisdiction: 'BD_BFIU',
      activeJurisdiction: 'BD_BFIU',
      setJurisdiction: (j) => set({ jurisdiction: j, activeJurisdiction: j }),
      setActiveJurisdiction: (j) => {
        set({ jurisdiction: j, activeJurisdiction: j });
        const jur = JURISDICTIONS[j];
        get().addToast(
          `Jurisdiction Switched: ${jur.shortCode}`,
          `Active statutory mandate: ${jur.statutoryAct}. CTR Limit: ${jur.currencySymbol}${jur.ctrThresholdNative.toLocaleString()} ${jur.currency}.`,
          'accent'
        );
      },

      // Active Banker Persona
      currentBanker: BANKER_PERSONAS.INVESTIGATOR_L2,
      session: {
        role: 'INVESTIGATOR_L2',
        userName: BANKER_PERSONAS.INVESTIGATOR_L2.name,
        institution: BANKER_PERSONAS.INVESTIGATOR_L2.institution
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
        get().addToast(
          'Officer Role Switched',
          `Active Signatory: ${profile.name} (${profile.roleTitle})`,
          'info'
        );
      },
      isRoleModalOpen: false,
      setRoleModalOpen: (open) => set({ isRoleModalOpen: open }),

      // 4-Eyes Dual Sign-off Modal
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

      // Ingestion Stream Controls
      isLiveStreamActive: true,
      isStreamRunning: true,
      streamSpeed: 1,
      toggleLiveStream: () => set((s) => ({ isLiveStreamActive: !s.isLiveStreamActive, isStreamRunning: !s.isStreamRunning })),
      toggleStreamRunning: () => set((s) => ({ isLiveStreamActive: !s.isLiveStreamActive, isStreamRunning: !s.isStreamRunning })),
      setStreamSpeed: (speed) => set({ streamSpeed: speed }),
      consumerLag: 0.82,
      liveTransactions: [],

      // Global PII Masking with Audited 60-Second Reveal
      piiRevealedUntil: 0,
      revealPii: async () => {
        const expiresAt = Date.now() + 60000; // 60 seconds
        set({ piiRevealedUntil: expiresAt });
        await get().logAuditAction(
          'PII_UNMASKED_AUDIT',
          'Sensitive customer identifiers (Account, NID, TIN) temporarily unmasked for 60 seconds by authorized officer.',
          'GLOBAL_PII'
        );
        get().addToast(
          'PII Unmasked (Audited)',
          'Customer identifiers unmasked for 60 seconds. Regulatory audit block appended to WORM chain.',
          'accent'
        );
      },
      isPiiRevealed: () => {
        return Date.now() < get().piiRevealedUntil;
      },

      // Toast Notifications & Bell Drawer
      toasts: [],
      addToast: (title, message, type = 'info') => {
        const id = `toast-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`;
        set((s) => ({ toasts: [...s.toasts, { id, title, message, type }] }));
        setTimeout(() => {
          get().removeToast(id);
        }, 4500);
      },
      removeToast: (id) => set((s) => ({ toasts: s.toasts.filter((t) => t.id !== id) })),

      notifications: [
        {
          id: 'NOTIF-1',
          timestamp: '10m ago',
          title: 'SLA Breach Warning (< 38m)',
          description: 'Tier 1 Hold alert ALT-994821 approaching 1-hour triage SLA threshold.',
          type: 'SLA_WARNING',
          read: false,
          linkedHref: '/triage'
        },
        {
          id: 'NOTIF-2',
          timestamp: '25m ago',
          title: '4-Eyes Ratification Required',
          description: 'Amina Rahman (Lead Investigator) submitted Emergency Account Freeze for Meghna Industrial.',
          type: 'FOUR_EYES_REQUEST',
          read: false,
          linkedHref: '/cases/CASE-2026-0881'
        },
        {
          id: 'NOTIF-3',
          timestamp: '45m ago',
          title: 'OFAC Sanctions Hit Flagged',
          description: 'Pre-settlement screening detected 94.6% Jaro-Winkler match for Gulf Star Commodities.',
          type: 'SANCTIONS_INTERDICTION',
          read: false,
          linkedHref: '/screening'
        }
      ],
      markNotificationRead: (id) => set((s) => ({
        notifications: s.notifications.map(n => n.id === id ? { ...n, read: true } : n)
      })),
      clearAllNotifications: () => set({ notifications: [] }),

      // Command Palette & Notification Drawer State
      isCommandPaletteOpen: false,
      setCommandPaletteOpen: (open) => set({ isCommandPaletteOpen: open }),
      isNotificationDrawerOpen: false,
      setNotificationDrawerOpen: (open) => set({ isNotificationDrawerOpen: open }),

      // Collections Initial State
      alerts: generateFullAlertQueue(),
      cases: INITIAL_CASES,
      customers: INITIAL_CUSTOMERS,
      screeningRecords: INITIAL_SCREENING_RECORDS,
      ctrRecords: INITIAL_CTR_RECORDS,
      auditLedger: getAuditChain(),

      // Cross-Module Operational Actions
      freezeAccount: async (accountId, reason) => {
        const banker = get().currentBanker;
        set((s) => ({
          customers: s.customers.map(c => c.accountNumber === accountId ? { ...c, accountStatus: 'FROZEN' } : c),
          alerts: s.alerts.map(a => a.account === accountId ? { ...a, status: 'QUARANTINED', tier: 'Tier 1 Hold', tierCode: 1 } : a)
        }));

        await get().logAuditAction(
          'ACCOUNT_FREEZE_EXECUTED',
          `Account ${accountId} administrative freeze ratified by ${banker.name} (${banker.role}). Rationale: ${reason}.`,
          accountId
        );

        get().addToast(
          'Account Administrative Freeze Ratified',
          `Account ${accountId} is now FROZEN. All outgoing wires and clearing settlement halted.`,
          'critical'
        );
      },

      assignAlert: (alertId, assignee) => {
        set((s) => ({
          alerts: s.alerts.map(a => a.id === alertId ? { ...a, assignee, status: 'UNDER_INVESTIGATION' } : a)
        }));
        get().addToast('Alert Reassigned', `Alert ${alertId} assigned to ${assignee}`, 'info');
      },

      batchAssignAlerts: (alertIds, assignee) => {
        const idSet = new Set(alertIds);
        set((s) => ({
          alerts: s.alerts.map(a => idSet.has(a.id) ? { ...a, assignee, status: 'UNDER_INVESTIGATION' } : a)
        }));
        get().addToast('Batch Assignment Complete', `${alertIds.length} alert(s) assigned to ${assignee}`, 'success');
      },

      dismissAlert: (alertId, reason) => {
        set((s) => ({
          alerts: s.alerts.map(a => a.id === alertId ? { ...a, status: 'FALSE_POSITIVE_DISMISSED' } : a)
        }));
        get().addToast('Alert Dismissed', `Alert ${alertId} closed as False Positive. Reason: ${reason}`, 'info');
      },

      batchDismissAlerts: (alertIds, reason) => {
        const idSet = new Set(alertIds);
        set((s) => ({
          alerts: s.alerts.map(a => idSet.has(a.id) ? { ...a, status: 'FALSE_POSITIVE_DISMISSED' } : a)
        }));
        get().addToast('Batch Dismissal Complete', `${alertIds.length} alert(s) marked False Positive.`, 'info');
      },

      escalateToCase: (alertIdsInput, title, slaHours = 72) => {
        const alertIds = Array.isArray(alertIdsInput) ? alertIdsInput : [alertIdsInput];
        const targetAlert = get().alerts.find(a => alertIds.includes(a.id)) || get().alerts[0]!;
        const newCaseId = `CASE-2026-${Math.floor(1000 + Math.random() * 9000)}`;
        const banker = get().currentBanker;

        const newCase: CommercialCase = {
          id: newCaseId,
          title: title || `Investigation: ${targetAlert.entityName}`,
          leadInvestigator: banker.name,
          createdAt: new Date().toISOString(),
          status: 'INVESTIGATION_OPEN',
          slaHours,
          slaDeadline: new Date(Date.now() + slaHours * 3600000).toISOString(),
          riskExposureUsd: targetAlert.amount,
          riskExposureBdt: targetAlert.amountBdt,
          targetAccount: targetAlert.account,
          entityName: targetAlert.entityName,
          primaryTypology: targetAlert.typology,
          milestonesCompleted: 2,
          milestonesTotal: 6,
          milestones: [
            { title: '1. Alert Quarantined', status: 'COMPLETE', time: targetAlert.timestamp, detail: 'Initial risk threshold hold' },
            { title: '2. Triage & Intake', status: 'COMPLETE', time: new Date().toISOString(), detail: `Assigned to ${banker.name}` },
            { title: '3. Compliance RFI Issued', status: 'PENDING', detail: 'Awaiting documentary proof of funds' },
            { title: '4. Evidence Hash Chain Sealed', status: 'PENDING', detail: 'Awaiting SHA-256 evidence hashing' },
            { title: '5. Regulatory SAR Drafted', status: 'PENDING', detail: 'Awaiting statutory narrative' },
            { title: '6. 4-Eyes CCO Sign-Off', status: 'PENDING', detail: 'Awaiting dual signatory ratification' }
          ],
          evidenceItems: [],
          notes: [
            {
              id: `NOTE-${Date.now()}`,
              author: banker.name,
              role: banker.role,
              timestamp: new Date().toISOString(),
              content: `Case escalated from alert(s): ${alertIds.join(', ')} under ${slaHours}h statutory SLA.`
            }
          ]
        };

        const idSet = new Set(alertIds);
        set((s) => ({
          cases: [newCase, ...s.cases],
          alerts: s.alerts.map(a => idSet.has(a.id) ? { ...a, caseId: newCaseId, status: 'UNDER_INVESTIGATION' } : a)
        }));

        get().addToast('Case Docketed', `Created Case ${newCaseId} linked to ${alertIds.length} alert(s)`, 'success');
        return newCase;
      },

      createCase: (caseData: any) => {
        const newCaseId = `CASE-2026-${Math.floor(1000 + Math.random() * 9000)}`;
        const banker = get().currentBanker;
        const newCase: CommercialCase = {
          id: newCaseId,
          title: caseData.title || `Investigation: ${caseData.subjectEntity || caseData.entityName || 'Commercial Docket'}`,
          leadInvestigator: caseData.assignedTo || caseData.leadInvestigator || banker.name,
          createdAt: new Date().toISOString(),
          status: 'INVESTIGATION_OPEN',
          slaHours: 72,
          slaDeadline: new Date(Date.now() + 72 * 3600000).toISOString(),
          riskExposureUsd: caseData.exposureUsd || caseData.riskExposureUsd || 100000,
          riskExposureBdt: (caseData.exposureUsd || 100000) * 121.5,
          targetAccount: caseData.targetAccount || 'AC-8812903',
          entityName: caseData.subjectEntity || caseData.entityName || 'Enterprise Subject',
          primaryTypology: caseData.primaryTypology || 'HIGH_VELOCITY_STRUCTURING',
          milestonesCompleted: 2,
          milestonesTotal: 6,
          milestones: [
            { title: '1. Alert Quarantined', status: 'COMPLETE', time: new Date().toISOString(), detail: 'Initial risk threshold hold' },
            { title: '2. Triage & Intake', status: 'COMPLETE', time: new Date().toISOString(), detail: `Assigned to ${caseData.assignedTo || banker.name}` },
            { title: '3. Compliance RFI Issued', status: 'PENDING', detail: 'Awaiting documentary proof of funds' },
            { title: '4. Evidence Hash Chain Sealed', status: 'PENDING', detail: 'Awaiting SHA-256 evidence hashing' },
            { title: '5. Regulatory SAR Drafted', status: 'PENDING', detail: 'Awaiting statutory narrative' },
            { title: '6. 4-Eyes CCO Sign-Off', status: 'PENDING', detail: 'Awaiting dual signatory ratification' }
          ],
          evidenceItems: [],
          notes: [
            {
              id: `NOTE-${Date.now()}`,
              author: banker.name,
              role: banker.role,
              timestamp: new Date().toISOString(),
              content: `Manual case docket created with initial exposure $${(caseData.exposureUsd || 100000).toLocaleString()}`
            }
          ]
        };

        set((s) => ({ cases: [newCase, ...s.cases] }));
        get().addToast('Case Created', `Institutional docket ${newCaseId} successfully registered.`, 'success');
        return newCase;
      },

      addAuditEntry: async (entryOrAction: any, details?: string, targetAccount?: string) => {
        if (typeof entryOrAction === 'object' && entryOrAction !== null) {
          const action = entryOrAction.eventType || entryOrAction.action || 'COMPLIANCE_ACTION';
          const desc = entryOrAction.details || '';
          const acc = entryOrAction.entityId || entryOrAction.targetAccount;
          const actor = entryOrAction.actionBy;
          await get().logAuditAction(action, desc, acc, actor);
        } else {
          await get().logAuditAction(entryOrAction, details || '', targetAccount);
        }
      },

      injectAlert: (newAlert) => {
        set((s) => ({
          alerts: [newAlert, ...s.alerts]
        }));
        get().addToast(
          'Simulated Alert Injected',
          `Injected ${newAlert.id} (${newAlert.tier}): ${newAlert.entityName} — $${newAlert.amount.toLocaleString()}`,
          newAlert.tierCode === 1 ? 'critical' : 'accent'
        );
      },

      addCaseNote: (caseId, note) => {
        const banker = get().currentBanker;
        set((s) => ({
          cases: s.cases.map(c => {
            if (c.id === caseId) {
              return {
                ...c,
                notes: [
                  ...c.notes,
                  {
                    id: `NOTE-${Date.now()}`,
                    author: banker.name,
                    role: banker.role,
                    timestamp: new Date().toISOString(),
                    content: note
                  }
                ]
              };
            }
            return c;
          })
        }));
        get().addToast('Case Note Recorded', 'Investigator observation added to dossier timeline.', 'info');
      },

      updateCaseMilestone: (caseId, milestoneIndex, status) => {
        set((s) => ({
          cases: s.cases.map(c => {
            if (c.id === caseId && c.milestones[milestoneIndex]) {
              const updatedMilestones = [...c.milestones];
              updatedMilestones[milestoneIndex] = {
                ...updatedMilestones[milestoneIndex]!,
                status,
                time: status === 'COMPLETE' ? new Date().toISOString() : undefined
              };
              const completed = updatedMilestones.filter(m => m.status === 'COMPLETE').length;
              return {
                ...c,
                milestones: updatedMilestones,
                milestonesCompleted: completed,
                status: completed === 6 ? 'CLOSED' : completed >= 5 ? 'PENDING_FOUR_EYES' : 'INVESTIGATION_OPEN'
              };
            }
            return c;
          })
        }));
      },

      dispositionScreening: (recordId, disposition, reason) => {
        const banker = get().currentBanker;
        set((s) => ({
          screeningRecords: s.screeningRecords.map(r => r.id === recordId ? { ...r, disposition, reviewedBy: banker.name } : r)
        }));
        get().addToast('Screening Disposition Saved', `Watchlist record ${recordId} set to ${disposition}`, 'info');
      },

      addScreeningSearch: (name, account = 'ADHOC_SEARCH', country, dob, nationalId) => {
        const id = `SCR-2026-${Math.floor(1000 + Math.random() * 9000)}`;
        const hits = screenWatchlistCandidate(name, { country, dob, nationalId });
        const topHit = hits[0];

        let record: WatchlistScreeningRecord;
        if (topHit) {
          record = {
            id,
            screenedName: name,
            screenedAccount: account,
            screenedAt: new Date().toISOString(),
            matchedEntity: `${topHit.officialPrimaryName} (${topHit.entityId})`,
            watchlistSource: topHit.watchlistName,
            matchScore: topHit.matchScore,
            matchAlgorithm: 'Jaro-Winkler + Token-Set + Phonetic Soundex',
            matchType: topHit.matchType,
            disposition: topHit.disposition,
            tokenDiffs: topHit.tokenDiffs,
            algorithmBreakdown: topHit.algorithmBreakdown,
            corroborationDetails: topHit.corroborationDetails
          };
        } else {
          record = {
            id,
            screenedName: name,
            screenedAccount: account,
            screenedAt: new Date().toISOString(),
            matchedEntity: 'No Sanctions or PEP Hit Detected (Clean)',
            watchlistSource: 'All Official Feeds (OFAC/UN/EU/UK/BFIU)',
            matchScore: 0.0,
            matchAlgorithm: 'Jaro-Winkler + Token-Set + Phonetic Soundex',
            matchType: 'NO_MATCH',
            disposition: 'DISMISSED_FALSE_POSITIVE',
            tokenDiffs: {
              screenedTokens: name.toLowerCase().split(/\s+/).filter(Boolean),
              matchedTokens: [],
              commonTokens: []
            },
            algorithmBreakdown: {
              jaroWinklerScore: 0.0,
              tokenSetScore: 0.0,
              phoneticScore: 0.0,
              corroborationAdjustment: 0.0
            },
            corroborationDetails: {
              dobStatus: 'NOT_PROVIDED',
              countryStatus: 'NOT_PROVIDED',
              idStatus: 'NOT_PROVIDED'
            }
          };
        }

        set((s) => ({ screeningRecords: [record, ...s.screeningRecords] }));
        return record;
      },

      updateCustomerRiskRating: (customerId, newRating, reason) => {
        const banker = get().currentBanker;
        set((s) => ({
          customers: s.customers.map(c => c.id === customerId ? { ...c, riskRating: newRating } : c)
        }));
        get().logAuditAction(
          'CUSTOMER_RISK_RATING_OVERRIDE',
          `Customer ${customerId} rating modified to ${newRating} by ${banker.name}. Reason: ${reason}.`,
          customerId
        );
        get().addToast('Customer Risk Rating Updated', `Rating changed to ${newRating}`, 'accent');
      },

      triggerEddRefresh: (customerId) => {
        set((s) => ({
          customers: s.customers.map(c => c.id === customerId ? { ...c, kycStatus: 'VERIFIED', nextReviewDate: '2027-09-30' } : c)
        }));
        get().addToast('Periodic EDD Refresh Triggered', 'Customer verification timeline renewed for 12 months.', 'success');
      },

      // WORM Audit Ledger Logging
      logAuditAction: async (action, details, targetAccount = 'GENERAL', makerName, checkerName) => {
        const current = get().currentBanker;
        const last = get().auditLedger[get().auditLedger.length - 1];
        const prevHash = last ? (last.currentHash || last.merkleHash) : '0'.repeat(64);
        const height = (last?.blockHeight || 1) + 1;

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

      simulateTamperTest: (blockSequence) => {
        tamperAuditBlock(blockSequence);
        set({ auditLedger: getAuditChain() });
        get().addToast(
          'Auditor Tamper Simulated',
          `Block #${blockSequence} payload mutated in memory. Re-verify chain to detect discrepancy.`,
          'critical'
        );
      },

      restoreValidChain: () => {
        restoreAuditChain();
        set({ auditLedger: getAuditChain() });
        get().addToast('WORM Chain Restored', 'Reverted in-memory mutation to certified pristine genesis chain.', 'success');
      },

      // Graph Studio Shared State
      camouflageDelta: 0.10,
      setCamouflageDelta: (delta) => set({ camouflageDelta: delta }),
      graphTimelineStep: 100,
      setGraphTimelineStep: (step) => set({ graphTimelineStep: step }),
      egoHopDistance: 2,
      setEgoHopDistance: (hops) => set({ egoHopDistance: hops }),

      // 1-Click Workspace Reset
      resetWorkspaceData: () => {
        restoreAuditChain();
        set({
          alerts: generateFullAlertQueue(),
          cases: INITIAL_CASES,
          customers: INITIAL_CUSTOMERS,
          screeningRecords: INITIAL_SCREENING_RECORDS,
          ctrRecords: INITIAL_CTR_RECORDS,
          auditLedger: getAuditChain(),
          piiRevealedUntil: 0
        });
        get().addToast('Workspace Reset', 'All alerts, cases, screening queues, and WORM ledger reset to certified pristine state.', 'success');
      }
    }),
    {
      name: 'intelligent-aml-workspace-v3',
      storage: createJSONStorage(() => (typeof window !== 'undefined' ? localStorage : {
        getItem: () => null,
        setItem: () => { },
        removeItem: () => { }
      })),
      partialize: (state) => ({
        activeJurisdiction: state.activeJurisdiction,
        densityMode: state.densityMode,
        alerts: state.alerts,
        cases: state.cases,
        customers: state.customers,
        screeningRecords: state.screeningRecords,
        ctrRecords: state.ctrRecords
      })
    }
  )
);

export const useBankingStore = useAppStore;
