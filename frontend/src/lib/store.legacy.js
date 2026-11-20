import { create } from 'zustand';
import { 
  RAW_TELEMETRY, 
  DERIVED_METRICS, 
  SEEDED_ALERTS, 
  SEEDED_CASES, 
  SEEDED_RFI_REQUESTS, 
  SEEDED_AUDIT_LOGS,
  SEEDED_ENTITIES_360
} from './seedData';
import { streamService } from './streamGenerator';

export const useAppStore = create((set, get) => ({
  // Active Navigation & Route
  activeRoute: 'overview', // 'overview' | 'alerts' | 'cases' | 'case-detail' | 'network' | 'filings' | 'requests' | 'audit' | 'models' | 'research' | 'settings'
  activeRouteParams: {},
  selectedCaseId: 'CASE-2026-0881',
  selectCase: (caseId) => set({ selectedCaseId: caseId, activeRoute: 'case-detail', activeRouteParams: { caseId } }),
  navigate: (route, params = {}) => set({ 
    activeRoute: route, 
    activeRouteParams: params,
    ...(params.caseId ? { selectedCaseId: params.caseId } : {})
  }),

  // Live Stream Simulation State & Controls
  isStreamRunning: true,
  streamSpeed: 1, // 1x, 2x, 5x
  liveTransactions: [
    {
      id: 'TX-BFIU-948201',
      sourceAccount: 'BD22-EBLB-4829-1092-8823',
      sourceEntity: 'Meghna Industrial & Agro Processing Ltd',
      targetAccount: 'AE-EBIL-4412-8819-3301',
      targetEntity: 'Gulf Star Commodities FZE (JAFZA Dubai)',
      amount: 9450.00,
      amountBdt: 1134000.00,
      currency: 'USD',
      rail: 'SWIFT MT700 (LC)',
      bic: 'EBLBBDDH',
      swiftReference: 'FT-LC-2026-CTG-88912',
      remittanceInfo: 'DOC-CREDIT DRAWDOWN UNDER LC-2026-CTG-88912 / COMBED COTTON YARN / ASYCUDA AUDIT',
      timestamp: '08:24:10 UTC',
      unixMs: Date.now() - 12000,
      riskScore: 0.982,
      tierCode: 1,
      tierLabel: 'Tier 1 Hold',
      conformalSet: 'Γ = {1}',
      conformalScore: 0.018,
      whyFlagged: 'Documentary LC declared valuation ($42.50/kg) diverges +333.7% from NBR ASYCUDA benchmark ($9.80/kg). Near-CTR sub-threshold allocation.'
    },
    {
      id: 'TX-BFIU-948202',
      sourceAccount: 'BD20-BSRM-7712-4491-0021',
      sourceEntity: 'BSRM Steels Limited',
      targetAccount: 'BD00-CPA-PORT-AUTH-02',
      targetEntity: 'Chittagong Port Authority Revenue Desk',
      amount: 3450000.00,
      amountBdt: 3450000.00,
      currency: 'BDT',
      rail: 'RTGS (BD Bank)',
      bic: 'EBLBBDDH',
      swiftReference: 'RTGS2026100249810291BD',
      remittanceInfo: 'RTGS INTERBANK CLEARING / INVOICE #INV-9912 / PORT WHARFAGE & BERTHING DUES',
      timestamp: '08:23:55 UTC',
      unixMs: Date.now() - 27000,
      riskScore: 0.008,
      tierCode: 3,
      tierLabel: 'Tier 3 Clear',
      conformalSet: 'Γ = {0}',
      conformalScore: 0.992,
      whyFlagged: 'Routine verified corporate commercial settlement. Historical baseline verified.'
    },
    {
      id: 'TX-BFIU-948203',
      sourceAccount: 'BD12-HSBC-2201-9940-1120',
      sourceEntity: 'Grameenphone Ltd (Corporate Treasury)',
      targetAccount: 'BD04-BRAC-0192-8821-4401',
      targetEntity: 'Beximco Pharmaceuticals Ltd',
      amount: 4250000.00,
      amountBdt: 4250000.00,
      currency: 'BDT',
      rail: 'BEFTN',
      bic: 'HSBCBDDH',
      swiftReference: 'ACH-PAYROLL-SEP26-492',
      remittanceInfo: 'CORPORATE SALARY DISBURSEMENT / BATCH #492 / 1,420 BENEFICIARIES / TDS 10%',
      timestamp: '08:23:40 UTC',
      unixMs: Date.now() - 42000,
      riskScore: 0.012,
      tierCode: 3,
      tierLabel: 'Tier 3 Clear',
      conformalSet: 'Γ = {0}',
      conformalScore: 0.988,
      whyFlagged: 'Routine verified corporate commercial settlement. Historical baseline verified.'
    },
    {
      id: 'TX-BFIU-948204',
      sourceAccount: 'BD22-EBLB-8831-2901-4412',
      sourceEntity: 'Shwapno Supermarket Ltd (Gulshan POS)',
      targetAccount: 'MFS-BKASH-0171-8840',
      targetEntity: 'Mohammad Rafiqul Islam (MFS Agent Desk)',
      amount: 14250.00,
      amountBdt: 14250.00,
      currency: 'BDT',
      rail: 'bKash MFS',
      bic: 'EBLBBDDH',
      swiftReference: 'BK8912048BD',
      remittanceInfo: 'MFS-QR-CHECKOUT TID:8912 / CONSUMER CART SETTLEMENT / PIN AUTH OK',
      timestamp: '08:23:25 UTC',
      unixMs: Date.now() - 57000,
      riskScore: 0.025,
      tierCode: 3,
      tierLabel: 'Tier 3 Clear',
      conformalSet: 'Γ = {0}',
      conformalScore: 0.975,
      whyFlagged: 'Routine verified corporate commercial settlement. Historical baseline verified.'
    },
    {
      id: 'TX-BFIU-948205',
      sourceAccount: 'BD18-CIBL-3312-8804-1290',
      sourceEntity: 'Square Fashion & Apparels Ltd',
      targetAccount: 'BD00-NBR-CUSTOMS-CTG-01',
      targetEntity: 'Customs House Chattogram (NBR Tariff)',
      amount: 842600.00,
      amountBdt: 842600.00,
      currency: 'BDT',
      rail: 'NBR e-Challan',
      bic: 'CIBLBDDH',
      swiftReference: 'CHL-NBR-2026-CTG-482910',
      remittanceInfo: 'NBR CUSTOMS TARIFF DUTY ASSESSMENT #88412 / TARIFF HEAD 5208.11 (Woven Cotton)',
      timestamp: '08:23:10 UTC',
      unixMs: Date.now() - 72000,
      riskScore: 0.015,
      tierCode: 3,
      tierLabel: 'Tier 3 Clear',
      conformalSet: 'Γ = {0}',
      conformalScore: 0.985,
      whyFlagged: 'Routine verified corporate commercial settlement. Historical baseline verified.'
    },
    {
      id: 'TX-BFIU-948206',
      sourceAccount: 'BD04-BRAC-1109-8421-4402',
      sourceEntity: 'Tanvir Ahmed Rahman (Trade Conduit)',
      targetAccount: 'GB-BARC-1109-8421-4402',
      targetEntity: 'Anglo-Bengal Textiles Ltd (Manchester)',
      amount: 18500.00,
      amountBdt: 2220000.00,
      currency: 'USD',
      rail: 'SWIFT MT103',
      bic: 'BRAKBDDH',
      swiftReference: '20261002SWFT481920',
      remittanceInfo: 'INV/2026/UK/481920 / COMMERCIAL RAW MATERIALS TRIAL SETTLEMENT',
      timestamp: '08:22:50 UTC',
      unixMs: Date.now() - 92000,
      riskScore: 0.542,
      tierCode: 2,
      tierLabel: 'Tier 2 Review Queue',
      conformalSet: 'Γ = {0,1}',
      conformalScore: 0.458,
      whyFlagged: 'New international cross-border counterparty relationship with elevated jurisdiction sensitivity. Conformal prediction interval spans both Licit and Illicit states.'
    },
    {
      id: 'TX-BFIU-948207',
      sourceAccount: 'GB-BARC-1109-8421-4402',
      sourceEntity: 'Anglo-Bengal Textiles Ltd (Manchester)',
      targetAccount: 'BD15-APEX-9912-3301-8842',
      targetEntity: 'Apex Footwear Limited',
      amount: 24800.00,
      amountBdt: 3844000.00,
      currency: 'GBP',
      rail: 'CHAPS',
      bic: 'BARCGB22',
      swiftReference: 'CHAPS-LON-992148',
      remittanceInfo: 'UK B2B COMMERCIAL CONTRACT SETTLEMENT / PO #88912 / AIR WAYBILL #074-9912048',
      timestamp: '08:22:30 UTC',
      unixMs: Date.now() - 112000,
      riskScore: 0.019,
      tierCode: 3,
      tierLabel: 'Tier 3 Clear',
      conformalSet: 'Γ = {0}',
      conformalScore: 0.981,
      whyFlagged: 'Routine verified corporate commercial settlement. Historical baseline verified.'
    },
    {
      id: 'TX-BFIU-948208',
      sourceAccount: 'BD18-CIBL-9921-4410-1129',
      sourceEntity: 'Aarong Flagship Outlet (Dhanmondi POS)',
      targetAccount: 'BD04-BRAC-0192-8821-4401',
      targetEntity: 'Beximco Pharmaceuticals Ltd',
      amount: 4850.50,
      amountBdt: 4850.50,
      currency: 'BDT',
      rail: 'NPSB Interbank',
      bic: 'CIBLBDDH',
      swiftReference: 'NPSB-POS-TID77124',
      remittanceInfo: 'NPSB CARD ACQUIRING BATCH CLEARING / TID:77124 / DUAL-CURRENCY POS AUTH',
      timestamp: '08:22:15 UTC',
      unixMs: Date.now() - 127000,
      riskScore: 0.005,
      tierCode: 3,
      tierLabel: 'Tier 3 Clear',
      conformalSet: 'Γ = {0}',
      conformalScore: 0.995,
      whyFlagged: 'Routine verified corporate commercial settlement. Historical baseline verified.'
    }
  ],
  camouflageDelta: 0.10, // Default calibrated edge gating threshold
  isDemoToolsOpen: false,
  isSanctionsModalOpen: false,
  isFreezeNoticeOpen: false,
  freezeNoticeTarget: null,

  setDemoToolsOpen: (isOpen) => set({ isDemoToolsOpen: isOpen }),
  setSanctionsModalOpen: (isOpen) => set({ isSanctionsModalOpen: isOpen }),
  setCamouflageDelta: (delta) => set({ camouflageDelta: delta }),

  openFreezeNoticeModal: (target) => set({ 
    isFreezeNoticeOpen: true, 
    freezeNoticeTarget: target || {
      accountNumber: 'BD22-EBLB-4829-1092-8823',
      holderName: 'Meghna Industrial & Agro Processing Ltd',
      amount: 9450,
      caseId: 'CASE-2026-0881',
      rail: 'SWIFT MT700 (LC)'
    } 
  }),
  closeFreezeNoticeModal: () => set({ isFreezeNoticeOpen: false, freezeNoticeTarget: null }),

  toggleStreamRunning: () => set((state) => {
    const nextState = !state.isStreamRunning;
    if (nextState) {
      streamService.start();
    } else {
      streamService.stop();
    }
    return { isStreamRunning: nextState };
  }),

  setStreamSpeed: (speed) => {
    streamService.setSpeed(speed);
    set({ streamSpeed: speed });
  },

  injectScenario: (scenarioId) => {
    const results = streamService.injectPredefinedScenario(scenarioId);
    get().logAuditAction(
      'SCENARIO_INJECTED',
      `Forensic scenario '${scenarioId}' simulated with ${results.length} transactions through Production Surveillance Engine.`,
      'Interbank Settlement Engine',
      'Chief Compliance Officer'
    );
    get().addToast(
      'Typology Simulated',
      `Simulated ${results.length} interbank events for ${scenarioId} through surveillance engine.`,
      'info'
    );
    return results;
  },

  processStreamTransaction: (txPayload) => set((state) => {
    const txList = Array.isArray(txPayload) ? txPayload : [txPayload];
    if (txList.length === 0) return {};

    const batchCount = txList.length;
    const newTotal = state.telemetry.totalProcessed24h + batchCount;
    let newT1 = state.telemetry.tier1Quarantined;
    let newT2 = state.telemetry.tier2ReviewQueue;
    let newAlerts = state.alerts;

    const now = Date.now();
    let lastToast = state.lastAlertToastTime || 0;

    for (const tx of txList) {
      const derivedBic = tx.bic || (tx.sourceAccount?.includes('BD04') ? 'BRAKBDDH' : tx.sourceAccount?.includes('BD22') ? 'EBLBBDDH' : tx.sourceAccount?.includes('MFS') ? 'BKASHBDD' : 'EBLBBDDH');

      if (tx.tierCode === 1) {
        newT1 += 1;
        const newAlert = {
          id: tx.id,
          entityName: tx.sourceEntity,
          account: tx.sourceAccount,
          bic: derivedBic,
          counterparty: tx.targetAccount || tx.target_account,
          counterpartyName: tx.targetEntity || tx.target_entity,
          counterpartyBic: (tx.targetAccount || '').includes('EBIL') ? 'EBILAEAD' : 'BRAKBDDH',
          amount: tx.amount,
          amountBdt: Number(tx.amountBdt || (Number(tx.amount || 0) * 120)),
          caseTotalExposure: Number(tx.amount || 0),
          rail: tx.rail,
          riskScore: tx.riskScore,
          tier: 'Tier 1 Hold',
          tierCode: 1,
          decisionSet: tx.conformalSet || 'Γ = {1}',
          whyFlagged: tx.whyFlagged || tx.reasons?.join('; ') || 'High-risk invariant violation',
          tbmlDetails: tx.tbmlDetails || tx.tbml_details || null,
          typology: tx.tbmlDetails ? 'TBML Over-Invoicing & Sub-Threshold Structuring' : 'High-Risk Invariant Violation',
          typologyBadge: (tx.rail || '').includes('LC') ? 'TBML Over-Invoice' : 'Structuring (<$10k)',
          date: tx.timestamp || 'Just now',
          status: 'QUARANTINED',
          slaMinutesLeft: 120
        };
        newAlerts = [newAlert, ...newAlerts.slice(0, 99)];

        // Rate-limit toast notifications to once per 8 seconds during rapid bank streaming
        if (now - lastToast > 8000) {
          lastToast = now;
          get().addToast(
            'Tier 1 Hold Detected',
            `${tx.sourceEntity}: $${Number(tx.amount).toLocaleString()} (৳${(Number(tx.amount) * 120).toLocaleString()} BDT)`,
            'critical'
          );
        }
      } else if (tx.tierCode === 2) {
        newT2 += 1;
        const newAlert = {
          id: tx.id,
          entityName: tx.sourceEntity,
          account: tx.sourceAccount,
          bic: derivedBic,
          counterparty: tx.targetAccount || tx.target_account,
          counterpartyName: tx.targetEntity || tx.target_entity,
          counterpartyBic: (tx.targetAccount || '').includes('EBIL') ? 'EBILAEAD' : 'BRAKBDDH',
          amount: tx.amount,
          amountBdt: Number(tx.amountBdt || (Number(tx.amount || 0) * 120)),
          caseTotalExposure: Number(tx.amount || 0),
          rail: tx.rail,
          riskScore: tx.riskScore,
          tier: 'Tier 2 Review',
          tierCode: 2,
          decisionSet: tx.conformalSet || 'Γ = {0, 1}',
          whyFlagged: tx.whyFlagged || tx.reasons?.join('; ') || 'Ambiguous conformal non-conformity set {0, 1}',
          tbmlDetails: tx.tbmlDetails || tx.tbml_details || null,
          typology: 'Ambiguous Conformal Review Trigger',
          typologyBadge: 'Borderline Invariant',
          date: tx.timestamp || 'Just now',
          status: 'REVIEW_REQUIRED',
          slaMinutesLeft: 240
        };
        newAlerts = [newAlert, ...newAlerts.slice(0, 99)];
      }
    }

    const newSTPCount = newTotal - newT1 - newT2;
    const newSTPRate = Number(((newSTPCount / newTotal) * 100).toFixed(1));
    const newQRate = Number(((newT1 / newTotal) * 100).toFixed(2));
    const newRRate = Number(((newT2 / newTotal) * 100).toFixed(2));

    const newTelemetry = {
      ...state.telemetry,
      totalProcessed24h: newTotal,
      tier1Quarantined: newT1,
      tier2ReviewQueue: newT2
    };

    const newMetrics = {
      ...state.metrics,
      stpRate: newSTPRate,
      quarantineRate: newQRate,
      reviewRate: newRRate
    };

    const newLiveTxs = [...[...txList].reverse(), ...state.liveTransactions].slice(0, 50);

    return {
      telemetry: newTelemetry,
      metrics: newMetrics,
      alerts: newAlerts,
      liveTransactions: newLiveTxs,
      lastAlertToastTime: lastToast
    };
  }),

  // Telemetry & Consistent Derived Metrics
  telemetry: RAW_TELEMETRY,
  metrics: DERIVED_METRICS,

  // Cases State (The missing core piece!)
  cases: SEEDED_CASES,
  selectedCaseId: 'CASE-2026-0881',
  selectCase: (caseId) => set({ selectedCaseId: caseId, activeRoute: 'case-detail', activeRouteParams: { caseId } }),

  addCaseNote: (caseId, text, author = 'Current Officer') => set((state) => ({
    cases: state.cases.map((c) => {
      if (c.id !== caseId) return c;
      const newNote = {
        id: `note-${Date.now()}`,
        author,
        time: new Date().toISOString().substring(11, 16) + ' UTC',
        text
      };
      return { ...c, notes: [newNote, ...c.notes] };
    })
  })),

  updateCaseStatus: (caseId, newStatus) => set((state) => ({
    cases: state.cases.map((c) => (c.id === caseId ? { ...c, status: newStatus } : c))
  })),

  addCaseAttachment: (caseId, attachment) => set((state) => ({
    cases: state.cases.map((c) => {
      if (c.id !== caseId) return c;
      const attachments = c.attachments || [];
      return { ...c, attachments: [attachment, ...attachments] };
    })
  })),

  // Four-Eyes Dual Sign-off enforcement
  fourEyesSignOffCase: (caseId, approverName) => {
    const state = get();
    const targetCase = state.cases.find(c => c.id === caseId);
    if (!targetCase) return { success: false, error: 'Case not found' };

    if (targetCase.fourEyesInitiator && targetCase.fourEyesInitiator.toLowerCase() === approverName.toLowerCase()) {
      return { 
        success: false, 
        error: 'Four-Eyes Dual Signatory Rule Violation: The approver must be distinct from the case initiator.' 
      };
    }

    set((state) => ({
      cases: state.cases.map((c) => {
        if (c.id !== caseId) return c;
        return {
          ...c,
          status: 'SAR_APPROVED_FILED',
          fourEyesApprover: approverName,
          fourEyesVerified: true
        };
      })
    }));

    // Record to append-only audit ledger
    get().logAuditAction(
      'FOUR_EYES_SAR_APPROVAL_CERTIFIED',
      `Dual-signatory sign-off certified by ${approverName} on case ${caseId}. Statutory filing transmitted.`,
      targetCase.subjectAccount,
      targetCase.fourEyesInitiator,
      approverName
    );

    return { success: true };
  },

  createCaseFromAlert: (alertId, title, assignee = 'Sarah Jenkins') => {
    const state = get();
    const alert = state.alerts.find(a => a.id === alertId);
    if (!alert) return;

    const newCaseId = `CASE-2026-088${state.cases.length + 1}`;
    const newCase = {
      id: newCaseId,
      title: title || `${alert.entityName} Investigation`,
      subjectEntity: alert.entityName,
      subjectAccount: alert.account,
      subjectBic: alert.bic,
      totalExposure: alert.amount,
      riskScore: alert.riskScore,
      tier: alert.tier,
      status: 'UNDER_INVESTIGATION',
      assignedTo: assignee,
      fourEyesInitiator: assignee,
      fourEyesApprover: null,
      fourEyesVerified: false,
      openedAt: new Date().toISOString().replace('T', ' ').substring(0, 19) + ' UTC',
      slaDeadline: new Date(Date.now() + 72 * 3600 * 1000).toISOString().replace('T', ' ').substring(0, 19) + ' UTC',
      statutoryJurisdiction: 'FinCEN Form 111 (US)',
      statutorySlaHours: 72,
      linkedAlertIds: [alert.id],
      timeline: [
        { id: 1, time: 'Just now', event: `Case created from alert ${alert.id} ($${alert.amount.toLocaleString()}).` }
      ],
      notes: [
        { id: 'note-1', author: assignee, time: 'Just now', text: `Initial case file opened for ${alert.typology}.` }
      ],
      sourcesUsed: [
        { id: 'SRC-1', claim: `Trigger transaction ${alert.amount.toLocaleString()} on ${alert.rail}`, ref: alert.id }
      ]
    };

    set((state) => ({
      cases: [newCase, ...state.cases],
      alerts: state.alerts.map(a => a.id === alertId ? { ...a, caseId: newCaseId, status: 'UNDER_INVESTIGATION' } : a)
    }));

    get().addToast('Case Created', `Case ${newCaseId} successfully generated from alert ${alertId}.`, 'success');
  },

  // Alerts State
  alerts: SEEDED_ALERTS,
  alertFilters: {
    tier: 'ALL',
    rail: 'ALL',
    status: 'ALL',
    search: ''
  },
  selectedAlertIds: [],

  setAlertFilters: (filters) => set((state) => ({
    alertFilters: { ...state.alertFilters, ...filters }
  })),

  toggleSelectAlert: (id) => set((state) => {
    const exists = state.selectedAlertIds.includes(id);
    return {
      selectedAlertIds: exists 
        ? state.selectedAlertIds.filter(x => x !== id)
        : [...state.selectedAlertIds, id]
    };
  }),

  selectAllAlerts: (selectAll) => set((state) => ({
    selectedAlertIds: selectAll ? state.alerts.map(a => a.id) : []
  })),

  dismissAlert: (id, reason) => set((state) => ({
    alerts: state.alerts.map(a => a.id === id ? { ...a, status: 'DISMISSED', dismissalReason: reason } : a)
  })),

  assignAlert: (id, assignee) => set((state) => ({
    alerts: state.alerts.map(a => a.id === id ? { ...a, assignee, status: 'ASSIGNED' } : a)
  })),

  bulkAssign: (assignee) => set((state) => ({
    alerts: state.alerts.map(a => state.selectedAlertIds.includes(a.id) ? { ...a, assignee, status: 'ASSIGNED' } : a),
    selectedAlertIds: []
  })),

  bulkDismiss: (reason) => set((state) => ({
    alerts: state.alerts.map(a => state.selectedAlertIds.includes(a.id) ? { ...a, status: 'DISMISSED', dismissalReason: reason } : a),
    selectedAlertIds: []
  })),

  // Inline Quick Actions on Alerts
  quickQuarantine: (alertId) => {
    set((state) => ({
      alerts: state.alerts.map(a => a.id === alertId ? { ...a, tier: 'Tier 1 Hold', tierCode: 1, status: 'QUARANTINED' } : a)
    }));
    get().logAuditAction(
      'QUICK_TIER1_HOLD',
      `Direct Tier 1 Quarantine hold placed on alert ${alertId}`,
      'Trading Desk',
      'Senior Compliance Officer'
    );
    get().addToast('Tier 1 Hold Applied', `Alert ${alertId} immediately placed on administrative hold.`, 'critical');
  },

  quickEscalate: (alertId) => {
    const alert = get().alerts.find(a => a.id === alertId);
    set((state) => ({
      alerts: state.alerts.map(a => a.id === alertId ? { ...a, status: 'UNDER_INVESTIGATION', assignee: 'Sarah Jenkins' } : a)
    }));
    get().logAuditAction(
      'ALERT_ESCALATED_TO_CASE',
      `Alert ${alertId} (${alert?.entityName || 'Entity'}) escalated to formal investigation`,
      alert?.account || 'Account',
      'Compliance Officer'
    );
    get().addToast('Escalated to Case', `Alert ${alertId} transferred to investigation desk.`, 'accent');
  },

  quickRFI: (alertId) => {
    const alert = get().alerts.find(a => a.id === alertId);
    if (alert) {
      get().createRFI({
        caseId: alert.caseId || 'CASE-2026-0881',
        targetAccount: alert.account,
        targetEntity: alert.entityName,
        amount: `$${Number(alert.amount).toLocaleString()} USD (৳${(Number(alert.amount) * 120).toLocaleString()} BDT)`,
        templateType: 'DOCUMENT_REQUEST_RFI',
        subject: `[SUPPORTING DOCUMENTATION] RFI Verification — Ref #${alert.id}`,
        complianceOfficer: 'Sarah Jenkins',
        dueDate: new Date(Date.now() + 5 * 24 * 3600 * 1000).toISOString().substring(0, 10),
        requiredDocs: [
          'Authenticated Export Monitoring (EXP) Form',
          'Certified Commercial Sales Invoice & Customs Declaration'
        ]
      });
      get().addToast('RFI Transmitted', `Document verification request dispatched for ${alert.entityName}.`, 'info');
    }
  },

  quickClear: (alertId) => {
    set((state) => ({
      alerts: state.alerts.map(a => a.id === alertId ? { ...a, status: 'CLEARED_BY_OFFICER', tier: 'Tier 3 Clear', tierCode: 3 } : a)
    }));
    get().logAuditAction(
      'ALERT_CLEARED_AS_LICIT',
      `Officer cleared alert ${alertId} following verified commercial counterparty check.`,
      'Clearing Desk',
      'Compliance Officer'
    );
    get().addToast('Cleared as Licit', `Alert ${alertId} marked legitimate under Rule CDD-26.`, 'success');
  },

  // Floating Bulk Action Bar Operations
  batchQuarantine: (alertIds) => {
    set((state) => ({
      alerts: state.alerts.map(a => alertIds.includes(a.id) ? { ...a, tier: 'Tier 1 Hold', tierCode: 1, status: 'QUARANTINED' } : a),
      selectedAlertIds: []
    }));
    get().logAuditAction(
      'BATCH_TIER1_HOLD',
      `Bulk administrative hold applied to ${alertIds.length} items (${alertIds.join(', ')})`,
      'Interbank Gateway',
      'Chief Compliance Officer'
    );
    get().addToast('Batch Quarantine Executed', `Placed ${alertIds.length} transactions on Tier-1 hold.`, 'critical');
  },

  batchRFI: (alertIds) => {
    const alertsToRfi = get().alerts.filter(a => alertIds.includes(a.id));
    alertsToRfi.forEach(al => {
      get().createRFI({
        caseId: al.caseId || 'CASE-2026-0881',
        targetAccount: al.account,
        targetEntity: al.entityName,
        amount: `$${Number(al.amount).toLocaleString()} USD`,
        templateType: 'DOCUMENT_REQUEST_RFI',
        subject: `[SUPPORTING DOCUMENTATION] RFI Verification — Ref #${al.id}`,
        complianceOfficer: 'Sarah Jenkins',
        dueDate: new Date(Date.now() + 5 * 24 * 3600 * 1000).toISOString().substring(0, 10),
        requiredDocs: ['Commercial Trade Invoice', 'Bill of Lading / Customs B/L']
      });
    });
    set({ selectedAlertIds: [] });
    get().addToast('Batch RFI Dispatched', `Issued ${alertIds.length} compliant document requests.`, 'info');
  },

  batchClear: (alertIds) => {
    set((state) => ({
      alerts: state.alerts.map(a => alertIds.includes(a.id) ? { ...a, status: 'CLEARED_BY_OFFICER', tier: 'Tier 3 Clear', tierCode: 3 } : a),
      selectedAlertIds: []
    }));
    get().logAuditAction(
      'BATCH_CLEARED_LICIT',
      `Batch clearance applied to ${alertIds.length} items.`,
      'Clearing Desk',
      'Compliance Officer'
    );
    get().addToast('Batch Clearance Executed', `Cleared ${alertIds.length} transactions as verified benign.`, 'success');
  },

  // Case Management Workspace Layout & Dossier Pinning
  caseViewMode: 'grid', // 'grid' | 'table'
  setCaseViewMode: (mode) => set({ caseViewMode: mode }),

  pinEvidence: (caseId, evidenceItem) => {
    const item = {
      id: `pin-${Date.now()}`,
      pinnedAt: new Date().toISOString().substring(11, 19) + ' UTC',
      pinnedBy: 'Nazmul Hasan, CAMS',
      ...evidenceItem
    };
    set((state) => ({
      cases: state.cases.map(c => c.id === caseId ? {
        ...c,
        pinnedEvidence: [item, ...(c.pinnedEvidence || [])]
      } : c)
    }));
    get().logAuditAction(
      'EVIDENCE_PINNED',
      `Pinned evidence '${item.title}' (${item.type}) to case ${caseId}`,
      caseId,
      'Compliance Officer'
    );
    get().addToast('Evidence Pinned', `Added '${item.title}' to Case Dossier.`, 'success');
  },

  unpinEvidence: (caseId, evidenceId) => set((state) => ({
    cases: state.cases.map(c => c.id === caseId ? {
      ...c,
      pinnedEvidence: (c.pinnedEvidence || []).filter(p => p.id !== evidenceId)
    } : c)
  })),

  // Forensic Network Graph Advanced Controls
  timelineStep: 0, // Initialized to 0 (Quiescent baseline)
  setTimelineStep: (step) => set((state) => ({ 
    timelineStep: typeof step === 'function' ? step(state.timelineStep) : Number(step) 
  })),
  egoHopDistance: 2, // 1, 2, 3
  setEgoHopDistance: (hops) => set({ egoHopDistance: hops }),
  maxVisibleNodes: 15,
  setMaxVisibleNodes: (max) => set({ maxVisibleNodes: max }),
  camouflageGatingEnabled: true,
  setCamouflageGatingEnabled: (val) => set({ camouflageGatingEnabled: val }),
  selectedGraphNode: null,
  setSelectedGraphNode: (node) => set({ selectedGraphNode: node }),
  entities360: SEEDED_ENTITIES_360,

  // Real-Time Ingestion Watermark & Consumer Lag
  consumerLagMsgs: 0, // 0 msgs behind head (synchronized)

  // Shared Right-Side Inspector Drawer (Used by Alerts & Network)
  isDrawerOpen: false,
  drawerItem: null,
  openDrawer: (item) => set({ isDrawerOpen: true, drawerItem: item }),
  closeDrawer: () => set({ isDrawerOpen: false, drawerItem: null }),

  // RFI Requests State & State Transitions
  rfiRequests: SEEDED_RFI_REQUESTS,
  createRFI: (rfiData) => set((state) => ({
    rfiRequests: [
      {
        id: `RFI-2026-${1090 + state.rfiRequests.length + 1}`,
        issuedDate: new Date().toISOString().substring(0, 10),
        status: 'PENDING_CUSTOMER_UPLOAD',
        uploadedDocs: [],
        ...rfiData
      },
      ...state.rfiRequests
    ]
  })),

  updateRFIStatus: (rfiId, newStatus) => {
    set((state) => ({
      rfiRequests: state.rfiRequests.map(r => r.id === rfiId ? { ...r, status: newStatus } : r)
    }));
    get().logAuditAction(
      'RFI_STATUS_TRANSITION',
      `RFI ${rfiId} status manually updated to ${newStatus}`,
      'CDD Portal',
      'Compliance Officer'
    );
    get().addToast('RFI Status Updated', `Case RFI #${rfiId} marked as ${newStatus}.`, 'info');
  },

  uploadRFIDocument: (rfiId, docMetadata) => {
    const newDoc = {
      id: `doc-${Date.now()}`,
      uploadedAt: new Date().toISOString().substring(11, 19) + ' UTC',
      status: 'VERIFIED_LEGAL_COPY',
      ...docMetadata
    };
    set((state) => ({
      rfiRequests: state.rfiRequests.map(r => r.id === rfiId ? {
        ...r,
        status: 'UNDER_OFFICER_REVIEW',
        uploadedDocs: [...(r.uploadedDocs || []), newDoc]
      } : r)
    }));
    get().logAuditAction(
      'CUSTOMER_DOCUMENT_INGESTED',
      `Customer uploaded document '${newDoc.name}' for RFI ${rfiId}`,
      'Secure Banking Portal',
      'Customer Portal Gateway'
    );
    get().addToast('Document Ingested', `Uploaded '${newDoc.name}' to RFI #${rfiId}.`, 'success');
  },

  sendCustomerReminder: (rfiId) => {
    const rfi = get().rfiRequests.find(r => r.id === rfiId);
    get().logAuditAction(
      'RFI_REMINDER_DISPATCHED',
      `Automated statutory reminder dispatched via SMS & ISO 20022 message for ${rfi?.targetEntity || 'Subject'}`,
      rfi?.targetAccount || 'Account',
      'Automated SLA Engine'
    );
    get().addToast('SLA Reminder Dispatched', `SMS & Email reminder sent for RFI #${rfiId}.`, 'info');
  },

  // Strategic Modals & Actions
  isPlainEnglishGuideOpen: false,
  setPlainEnglishGuideOpen: (open) => set({ isPlainEnglishGuideOpen: open }),

  isRoleModalOpen: false,
  setRoleModalOpen: (open) => set({ isRoleModalOpen: open }),

  isSanctionsModalOpen: false,
  setSanctionsModalOpen: (open) => set({ isSanctionsModalOpen: open }),
  sanctionsQuery: '',
  setSanctionsQuery: (q) => set({ sanctionsQuery: q }),
  openSanctionsModalWithQuery: (q) => set({ isSanctionsModalOpen: true, sanctionsQuery: q }),

  isRecourseModalOpen: false,
  setRecourseModalOpen: (open) => set({ isRecourseModalOpen: open }),
  recourseSubject: null,
  openRecourseModal: (subject) => set({ isRecourseModalOpen: true, recourseSubject: subject }),

  isAdverseActionOpen: false,
  setAdverseActionOpen: (open) => set({ isAdverseActionOpen: open }),
  adverseActionSubject: null,
  openAdverseActionModal: (subject) => set({ isAdverseActionOpen: true, adverseActionSubject: subject }),

  isCoreBankingModalOpen: false,
  setCoreBankingModalOpen: (open) => set({ isCoreBankingModalOpen: open }),
  coreBankingActionSubject: null,
  triggerCoreBankingHold: (account, amount, rail, actionType = 'TEMPORARY_DEBIT_HOLD') => {
    const authCode = `CORE-AUTH-${Math.floor(100000 + Math.random() * 900000)}`;
    get().logAuditAction(
      'CORE_BANKING_LEDGER_RESTRICTION',
      `Direct core banking ledger hold (${actionType}) applied to account ${account}. Auth Code: ${authCode}.`,
      account,
      'Core Ledger API Gateway'
    );
    get().addToast(
      'Core Ledger Restitution Applied',
      `Core API Webhook executed: ${actionType} confirmed for ${account}. Auth: ${authCode}`,
      'critical'
    );
    return { success: true, authCode };
  },

  // Cryptographic Audit Ledger State
  auditLogs: SEEDED_AUDIT_LOGS,
  logAuditAction: (action, details, targetAccount, initiator = 'System', approver = null) => set((state) => {
    const lastHash = state.auditLogs[state.auditLogs.length - 1]?.merkleHash || '00000000000000000000000000000000';
    const rawString = `${action}:${details}:${targetAccount}:${Date.now()}:${lastHash}`;
    let hash = 0;
    for (let i = 0; i < rawString.length; i++) {
      hash = ((hash << 5) - hash) + rawString.charCodeAt(i);
      hash |= 0;
    }
    const hex = Math.abs(hash).toString(16).padStart(8, '0');
    const newMerkleHash = `${hex}12c85d6e3f019a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d`.substring(0, 64);

    const newLog = {
      id: `LOG-${String(state.auditLogs.length + 1).padStart(3, '0')}`,
      action,
      targetAccount: targetAccount || 'Global Clearing Desk',
      bankerName: initiator,
      role: approver ? 'Dual Signatory Verified' : 'Compliance Officer',
      initiator,
      approver,
      fourEyesStatus: approver ? 'DUAL_CONTROL_VERIFIED' : 'INITIATED',
      timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19) + ' UTC',
      details,
      merkleHash: newMerkleHash,
      prevHash: lastHash
    };

    return { auditLogs: [...state.auditLogs, newLog] };
  }),

  // Transaction Monitoring & Fraud Detection Engine State
  blockedTransactions: [
    {
      id: 'TX-BLK-9012',
      txId: 'TX-BFIU-948201',
      account: 'BD22-EBLB-4829-1092-8823',
      entityName: 'Meghna Industrial & Agro Processing Ltd',
      counterparty: 'AE-EBIL-4412-8819-3301',
      counterpartyName: 'Gulf Star Commodities FZE',
      amount: 9450.00,
      currency: 'USD',
      rail: 'SWIFT MT700 (LC)',
      blockedAt: '2026-09-02 08:24:10 UTC',
      blockedBy: 'Automated Fraud Engine (Tier 1 Hold)',
      reason: 'Structuring ($9,450 directly beneath $10k CTR limit) + TBML Unit Price Divergence (+333.7%)',
      status: 'BLOCKED',
      riskScore: 0.982,
      ruleTriggered: 'RULE_STRUCTURING'
    },
    {
      id: 'TX-BLK-9013',
      txId: 'TX-BFIU-948190',
      account: 'BD04-BRAC-1109-8421-4402',
      entityName: 'Tanvir Ahmed Rahman (Trade Conduit)',
      counterparty: 'AE-EBIL-4412-8819-3301',
      counterpartyName: 'Gulf Star Commodities FZE',
      amount: 47600.00,
      currency: 'USD',
      rail: 'SWIFT MT103',
      blockedAt: '2026-09-02 08:22:15 UTC',
      blockedBy: 'Sarah Jenkins (Senior Investigator)',
      reason: 'High-Velocity Layering Outflow into Offshore JAFZA Free Zone Entity with Zero Account Dwell Time',
      status: 'BLOCKED',
      riskScore: 0.941,
      ruleTriggered: 'RULE_OFFSHORE_CORRIDOR'
    }
  ],

  fraudRules: [
    {
      id: 'RULE_STRUCTURING',
      code: 'FR-001',
      name: 'Sub-Threshold CTR Structuring Detector',
      description: 'Detects single or clustered transfers in the $9,000 to $9,950 range engineered to evade $10,000 regulatory reporting.',
      category: 'Structuring / Smurfing',
      severity: 'CRITICAL',
      status: 'ACTIVE',
      thresholdValue: '$9,000 - $9,950',
      action: 'AUTOMATIC_BLOCK',
      triggers24h: 14
    },
    {
      id: 'RULE_VELOCITY_SPIKE',
      code: 'FR-002',
      name: 'Rapid Interbank Velocity Spike Guard',
      description: 'Identifies sudden acceleration in transaction frequency exceeding 4.0 transfers/minute from non-clearing accounts.',
      category: 'Velocity Burst',
      severity: 'HIGH',
      status: 'ACTIVE',
      thresholdValue: '> 4.0 tx/min',
      action: 'HOLD_AND_REVIEW',
      triggers24h: 28
    },
    {
      id: 'RULE_OFFSHORE_CORRIDOR',
      code: 'FR-003',
      name: 'Non-Cooperative Offshore Corridor Restriction',
      description: 'Flags or blocks international wires routed to known secrecy jurisdictions or high-risk free-zone shell conduits without trade substantiation.',
      category: 'Jurisdictional Risk',
      severity: 'CRITICAL',
      status: 'ACTIVE',
      thresholdValue: 'High-Risk Jurisdictions',
      action: 'AUTOMATIC_BLOCK',
      triggers24h: 9
    },
    {
      id: 'RULE_DORMANT_AWAKENING',
      code: 'FR-004',
      name: 'Dormant Account High-Value Activation',
      description: 'Flags sudden outbound transfers > $5,000 from retail or agent accounts inactive for greater than 180 consecutive days.',
      category: 'Account Takeover / Mule',
      severity: 'HIGH',
      status: 'ACTIVE',
      thresholdValue: '> 180 Days Inactivity',
      action: 'STEP_UP_AUTH_HOLD',
      triggers24h: 6
    },
    {
      id: 'RULE_TBML_DIVERGENCE',
      code: 'FR-005',
      name: 'Trade-Based Pricing & Customs Divergence',
      description: 'Compares documentary Letter of Credit declared unit values against official ASYCUDA customs tariff databases.',
      category: 'Trade-Based AML (TBML)',
      severity: 'CRITICAL',
      status: 'ACTIVE',
      thresholdValue: '> 200% Price Divergence',
      action: 'AUTOMATIC_BLOCK',
      triggers24h: 3
    },
    {
      id: 'RULE_PASSTHROUGH_MULE',
      code: 'FR-006',
      name: 'Zero-Dwell Pass-Through Mule Ring',
      description: 'Detects rapid inbound-to-outbound fund matching with >95% flow conservation and dwell times under 30 minutes.',
      category: 'Mule Syndicates',
      severity: 'HIGH',
      status: 'ACTIVE',
      thresholdValue: '< 30 Min Dwell Time',
      action: 'HOLD_AND_REVIEW',
      triggers24h: 19
    }
  ],

  blockTransaction: (txId, reason, bankerName = 'Sarah Jenkins') => {
    const state = get();
    if (state.blockedTransactions.some(b => b.txId === txId && b.status === 'BLOCKED')) {
      return { success: false, error: 'Transaction is already blocked.' };
    }

    const tx = state.liveTransactions.find(t => t.id === txId) || 
               state.alerts.find(a => a.id === txId);
    
    const blockEntry = {
      id: `TX-BLK-${Date.now().toString().slice(-4)}`,
      txId: txId,
      account: tx?.sourceAccount || tx?.account || 'BD22-EBLB-4829-1092-8823',
      entityName: tx?.sourceEntity || tx?.entityName || 'Subject Entity',
      counterparty: tx?.targetAccount || tx?.counterparty || 'Beneficiary Account',
      counterpartyName: tx?.targetEntity || tx?.counterpartyName || 'Beneficiary Entity',
      amount: tx?.amount || 9450,
      currency: tx?.currency || 'USD',
      rail: tx?.rail || 'SWIFT MT103',
      blockedAt: new Date().toISOString().replace('T', ' ').substring(0, 19) + ' UTC',
      blockedBy: bankerName,
      reason: reason || 'Manual Compliance Stop: High-Risk Fraud Pattern Identified',
      status: 'BLOCKED',
      riskScore: tx?.riskScore || 0.95,
      ruleTriggered: 'MANUAL_OFFICER_OVERRIDE'
    };

    set((state) => ({
      blockedTransactions: [blockEntry, ...state.blockedTransactions],
      liveTransactions: state.liveTransactions.map(t => t.id === txId ? { ...t, tierLabel: 'Tier 1 Blocked', tierCode: 1 } : t)
    }));

    get().logAuditAction(
      'TRANSACTION_BLOCKED_STATUTORY_HOLD',
      `Administrative freeze placed on transaction ${txId} (${blockEntry.amount} ${blockEntry.currency}). Reason: ${blockEntry.reason}`,
      blockEntry.account,
      bankerName
    );

    get().addToast('Transaction Blocked', `Interbank wire ${txId} has been intercepted and blocked.`, 'critical');
    return { success: true, blockEntry };
  },

  unblockTransaction: (blockId, justification, approverName = 'Nazmul Hasan, CCO') => {
    const state = get();
    const target = state.blockedTransactions.find(b => b.id === blockId || b.txId === blockId);
    if (!target) return { success: false, error: 'Block record not found.' };

    set((state) => ({
      blockedTransactions: state.blockedTransactions.map(b => 
        (b.id === blockId || b.txId === blockId) 
          ? { ...b, status: 'RELEASED', unblockedAt: new Date().toISOString().replace('T', ' ').substring(0, 19) + ' UTC', unblockedBy: approverName, justification }
          : b
      )
    }));

    get().logAuditAction(
      'TRANSACTION_UNBLOCKED_RELEASED',
      `Four-Eyes dual release authorized for ${target.txId} by ${approverName}. Justification: ${justification}`,
      target.account,
      target.blockedBy,
      approverName
    );

    get().addToast('Transaction Released', `Administrative hold on ${target.txId} lifted under dual sign-off.`, 'success');
    return { success: true };
  },

  toggleFraudRule: (ruleId) => set((state) => ({
    fraudRules: state.fraudRules.map(r => r.id === ruleId ? { ...r, status: r.status === 'ACTIVE' ? 'DISABLED' : 'ACTIVE' } : r)
  })),

  // Toast Notification System
  toasts: [],
  addToast: (title, description, type = 'info') => {
    const id = `toast-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
    set((state) => ({
      toasts: [...state.toasts, { id, title, description, type }]
    }));
    setTimeout(() => {
      get().dismissToast(id);
    }, 4000);
  },
  dismissToast: (id) => set((state) => ({
    toasts: state.toasts.filter(t => t.id !== id)
  }))
}));
