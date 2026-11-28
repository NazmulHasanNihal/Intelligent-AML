'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  SlidersHorizontal,
  ShieldAlert,
  GitCompare,
  Lock,
  CheckCircle2,
  AlertTriangle,
  Clock,
  Plus,
  X,
  FileCheck2,
  TrendingDown,
  TrendingUp,
  UserCheck
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';

const SEEDED_WHITELIST = [
  {
    id: 'WHT-2026-001',
    entityName: 'Bangladesh Petroleum Corporation (BPC)',
    account: 'BD88-BPCB-9901-2281-0012',
    ruleExempted: 'High-Volume Oil Import Wire Spikes (> $50M)',
    validUntil: '2027-06-30',
    authorizedBy: 'Kazi Farhan (CCO)',
    status: 'ACTIVE'
  },
  {
    id: 'WHT-2026-002',
    entityName: 'Apex Footwear Ltd — Global Export Division',
    account: 'BD44-APEX-1182-4491-9920',
    ruleExempted: 'EU Commercial Settlement Transit Velocity',
    validUntil: '2026-12-31',
    authorizedBy: 'Tariq Rahman (Head of AML)',
    status: 'ACTIVE'
  },
  {
    id: 'WHT-2026-003',
    entityName: 'Square Pharmaceuticals PLC',
    account: 'BD12-SQR-8819-0021-3310',
    ruleExempted: 'Active Pharmaceutical Ingredient (API) Bulk LCs',
    validUntil: '2027-03-31',
    authorizedBy: 'Kazi Farhan (CCO)',
    status: 'ACTIVE'
  }
];

export default function RuleStudioPage() {
  const { setFourEyesModalOpen, addToast, addAuditEntry } = useBankingStore();

  const [activeTab, setActiveTab] = useState<'CHAMPION_CHALLENGER' | 'SENSITIVITY_SIM' | 'WHITELIST'>('CHAMPION_CHALLENGER');
  const [whitelist, setWhitelist] = useState(SEEDED_WHITELIST);

  // Sensitivity Sliders
  const [flowThreshold, setFlowThreshold] = useState(0.92);
  const [burstMultiplier, setBurstMultiplier] = useState(3.2);
  const [windowHours, setWindowHours] = useState(48);

  // Real Champion vs Challenger Shadow Replay Telemetry
  const [replayData, setReplayData] = useState<{
    replay_period: string;
    total_transactions_replayed: number;
    champion_f1: number;
    champion_fpr: number;
    challenger_f1: number;
    challenger_fpr: number;
    operational_noise_reduction_pct: number;
    conformal_coverage_empirical: number;
  } | null>(null);

  useEffect(() => {
    fetch('/api/v1/models/champion-challenger?samples=2500')
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data && data.replay_period) setReplayData(data);
      })
      .catch(() => {});
  }, []);

  // Derived Live Policy Sensitivity Metrics
  const projectedMonthlyAlerts = Math.max(
    650,
    Math.round(14820 * (0.28 + (1.0 - flowThreshold) * 1.45 + (3.2 / burstMultiplier) * 0.14 + (windowHours / 48) * 0.06))
  );
  const projectedStpRate = Math.min(99.6, Math.max(82.0, 95.8 + (flowThreshold - 0.85) * 26 + (burstMultiplier - 2.0) * 1.2)).toFixed(1);
  const projectedFprDrop = Math.min(89.5, Math.max(22.0, 62.0 + (flowThreshold - 0.85) * 145 + (burstMultiplier - 2.5) * 3.5)).toFixed(1);

  // Exemption Modal
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newEntity, setNewEntity] = useState('');
  const [newAccount, setNewAccount] = useState('');
  const [newRule, setNewRule] = useState('');
  const [newExpiry, setNewExpiry] = useState('2027-12-31');

  const handleAddExemption = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newEntity.trim()) return;

    setFourEyesModalOpen(true, {
      actionType: 'PERIODIC_REVIEW_SIGNOFF',
      actionTitle: `Approve Time-Bound Whitelist Exemption (${newEntity})`,
      targetId: newAccount || 'ENT-EXEMPT',
      details: `Authorize institutional rule exemption for ${newEntity} on rule '${newRule}' expiring on ${newExpiry}.`
    });

    setWhitelist([
      ...whitelist,
      {
        id: `WHT-2026-${Math.floor(100 + Math.random() * 900)}`,
        entityName: newEntity,
        account: newAccount || 'BD99-NEW-0000-0000',
        ruleExempted: newRule,
        validUntil: newExpiry,
        authorizedBy: 'Pending 4-Eyes Approval',
        status: 'PENDING_APPROVAL'
      }
    ]);

    setIsModalOpen(false);
    setNewEntity('');
    setNewAccount('');
    setNewRule('');
  };

  return (
    <div className="p-4 sm:p-5 lg:p-6 max-w-[1750px] mx-auto space-y-5">
      {/* Page Title */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-fg flex items-center gap-2 font-sans">
            <SlidersHorizontal className="w-5 h-5 text-tier-3-text" />
            Compliance Rule Studio, Sensitivity &amp; Whitelisting
          </h1>
          <p className="text-xs text-muted mt-0.5">
            Shadow-mode Champion vs Challenger benchmarking, internal threshold calibration, and 4-eyes exemptions.
          </p>
        </div>

        {/* Tab Switcher */}
        <div className="flex items-center bg-panel p-1 rounded-xl border border-line-strong text-xs font-semibold">
          <button
            onClick={() => setActiveTab('CHAMPION_CHALLENGER')}
            className={`px-3 py-1.5 rounded-lg transition-colors cursor-pointer ${
              activeTab === 'CHAMPION_CHALLENGER'
                ? 'bg-emerald-500/20 text-tier-3-text font-bold border border-emerald-500/40'
                : 'text-muted hover:text-fg-secondary'
            }`}
          >
            Champion vs Challenger (Shadow Mode)
          </button>
          <button
            onClick={() => setActiveTab('SENSITIVITY_SIM')}
            className={`px-3 py-1.5 rounded-lg transition-colors cursor-pointer ${
              activeTab === 'SENSITIVITY_SIM'
                ? 'bg-emerald-500/20 text-tier-3-text font-bold border border-emerald-500/40'
                : 'text-muted hover:text-fg-secondary'
            }`}
          >
            Internal Sensitivity Calibration
          </button>
          <button
            onClick={() => setActiveTab('WHITELIST')}
            className={`px-3 py-1.5 rounded-lg transition-colors cursor-pointer ${
              activeTab === 'WHITELIST'
                ? 'bg-emerald-500/20 text-tier-3-text font-bold border border-emerald-500/40'
                : 'text-muted hover:text-fg-secondary'
            }`}
          >
            Time-Bound Whitelisting ({whitelist.length})
          </button>
        </div>
      </div>

      {/* Tab 1: Champion vs Challenger */}
      {activeTab === 'CHAMPION_CHALLENGER' && (
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {/* Champion Card */}
            <div className="p-5 rounded-2xl bg-panel border border-line shadow-xl space-y-4">
              <div className="flex items-center justify-between pb-2 border-b border-line">
                <div>
                  <span className="text-xs font-mono text-fg0 font-bold">Active In-Flight Rule</span>
                  <h3 className="text-sm font-bold text-fg font-mono">Champion: Legacy Threshold Engine v2.4</h3>
                </div>
                <span className="px-2 py-0.5 rounded text-xs font-mono font-bold bg-sky-500/20 text-accent-2 border border-sky-500/30">
                  PRODUCTION LIVE
                </span>
              </div>

              <div className="space-y-2 text-xs">
                <div className="p-3 bg-canvas rounded-xl flex items-center justify-between">
                  <span className="text-muted">Monthly Alert Volume:</span>
                  <strong className="font-mono text-fg-secondary">14,820 alerts / mo</strong>
                </div>
                <div className="p-3 bg-canvas rounded-xl flex items-center justify-between">
                  <span className="text-muted">False Positive Rate:</span>
                  <strong className="font-mono text-tier-1-text">88.4% (Heavy Analyst Fatigue)</strong>
                </div>
                <div className="p-3 bg-canvas rounded-xl flex items-center justify-between">
                  <span className="text-muted">Mean Triage Duration:</span>
                  <strong className="font-mono text-fg-secondary">14.2 minutes / alert</strong>
                </div>
              </div>
            </div>

            {/* Challenger Card */}
            <div className="p-5 rounded-2xl bg-panel border border-emerald-500/40 shadow-xl space-y-4">
              <div className="flex items-center justify-between pb-2 border-b border-line">
                <div>
                  <span className="text-xs font-mono text-tier-3-text font-bold">Shadow Mode Evaluation</span>
                  <h3 className="text-sm font-bold text-fg font-mono">Challenger: Calibrated Topology Gate v3.0</h3>
                </div>
                <span className="px-2 py-0.5 rounded text-xs font-mono font-bold bg-emerald-500/20 text-tier-3-text border border-emerald-500/40">
                  READY FOR PROMOTION
                </span>
              </div>

              <div className="space-y-2 text-xs">
                <div className="p-3 bg-canvas rounded-xl flex items-center justify-between">
                  <span className="text-muted">Monthly Alert Volume:</span>
                  <strong className="font-mono text-tier-3-text">4,120 alerts / mo (-72.2%)</strong>
                </div>
                <div className="p-3 bg-canvas rounded-xl flex items-center justify-between">
                  <span className="text-muted">False Positive Reduction:</span>
                  <strong className="font-mono text-tier-3-text">-42.8% False Positive Drop</strong>
                </div>
                <div className="p-3 bg-canvas rounded-xl flex items-center justify-between">
                  <span className="text-muted">True Positive Capture:</span>
                  <strong className="font-mono text-tier-3-text">+18.4% Greater Complex Laundering Capture</strong>
                </div>
              </div>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-panel border border-line flex flex-wrap items-center justify-between gap-3">
            <p className="text-xs text-muted">
              {replayData
                ? `${replayData.replay_period} (${replayData.total_transactions_replayed.toLocaleString()} txs, synthetic replay): Champion F1 ${(replayData.champion_f1 * 100).toFixed(1)}% vs Challenger F1 ${(replayData.challenger_f1 * 100).toFixed(1)}%, ${replayData.operational_noise_reduction_pct}% noise reduction, ${(replayData.conformal_coverage_empirical * 100).toFixed(2)}% conformal coverage.`
                : 'Illustrative replay result: the challenger ran in shadow mode over a synthetic 30-day window with 99.04% empirical conformal coverage.'}
            </p>
            <button
              onClick={() => {
                setFourEyesModalOpen(true, {
                  actionType: 'PERIODIC_REVIEW_SIGNOFF',
                  actionTitle: 'Promote Challenger Topology Gate v3.0 to Production',
                  targetId: 'RULE-CHALLENGER-V3',
                  details: 'Authorize promotion of Challenger v3.0 to replace Champion v2.4 across institutional payment rails.'
                });
              }}
              className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition-colors flex items-center gap-2 cursor-pointer shadow-lg shadow-emerald-600/20"
            >
              <Lock className="w-3.5 h-3.5" />
              <span>Promote to Production (4-Eyes)</span>
            </button>
          </div>
        </div>
      )}

      {/* Tab 2: Internal Sensitivity Calibration */}
      {activeTab === 'SENSITIVITY_SIM' && (
        <div className="p-6 rounded-2xl bg-panel border border-line shadow-2xl space-y-5">
          <div className="p-3 bg-tier-2-bg border border-amber-800/60 rounded-xl flex items-center gap-2.5 text-xs text-tier-2-text">
            <AlertTriangle className="w-4 h-4 shrink-0 text-tier-2-text" />
            <span>
              <strong>MLPA 2012 § 6 Confidential:</strong> Internal sensitivity bounds only — never disclose structuring windows or thresholds externally.
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-4 bg-canvas rounded-xl border border-line space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="font-semibold text-fg-secondary">Pass-Through Flow Threshold</span>
                <span className="font-mono font-bold text-tier-3-text">{flowThreshold.toFixed(2)}</span>
              </div>
              <input
                type="range"
                min="0.70"
                max="1.00"
                step="0.01"
                value={flowThreshold}
                onChange={(e) => setFlowThreshold(parseFloat(e.target.value))}
                className="w-full accent-emerald-500 cursor-pointer"
              />
              <p className="text-xs text-fg0">
                Accounts with inflow ≈ outflow within this ratio are flagged as transit conduits.
              </p>
            </div>

            <div className="p-4 bg-canvas rounded-xl border border-line space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="font-semibold text-fg-secondary">Velocity Burst Multiplier</span>
                <span className="font-mono font-bold text-tier-2-text">{burstMultiplier.toFixed(1)}x</span>
              </div>
              <input
                type="range"
                min="1.0"
                max="5.0"
                step="0.1"
                value={burstMultiplier}
                onChange={(e) => setBurstMultiplier(parseFloat(e.target.value))}
                className="w-full accent-amber-500 cursor-pointer"
              />
              <p className="text-xs text-fg0">
                Surges above customer 90-day moving average volume escalate to Tier 2 review.
              </p>
            </div>

            <div className="p-4 bg-canvas rounded-xl border border-line space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="font-semibold text-fg-secondary">Structuring Time Window</span>
                <span className="font-mono font-bold text-accent-2">{windowHours}h</span>
              </div>
              <input
                type="range"
                min="12"
                max="72"
                step="6"
                value={windowHours}
                onChange={(e) => setWindowHours(parseInt(e.target.value))}
                className="w-full accent-sky-500 cursor-pointer"
              />
              <p className="text-xs text-fg0">
                Rolling aggregation window for multi-agent deposits below ৳1,000,000 BDT statutory ceiling (MLPA 2012 § 2(z) &amp; BFIU Circular 26).
              </p>
            </div>
          </div>

          {/* Live Simulation Readout + Apply Action */}
          <div className="p-4 rounded-xl bg-canvas border border-line flex flex-wrap items-center justify-between gap-4">
            <div className="flex flex-wrap items-center gap-6 text-xs font-mono">
              <div>
                <span className="text-[10px] text-fg0 uppercase block">Projected Volume</span>
                <strong className="text-fg text-sm">{projectedMonthlyAlerts.toLocaleString()} alerts / mo</strong>
              </div>
              <div>
                <span className="text-[10px] text-fg0 uppercase block">Est. Tier 3 STP</span>
                <strong className="text-tier-3-text text-sm">{projectedStpRate}%</strong>
              </div>
              <div>
                <span className="text-[10px] text-fg0 uppercase block">False Positive Drop</span>
                <strong className="text-accent-2 text-sm">-{projectedFprDrop}%</strong>
              </div>
            </div>

            <button
              onClick={() => {
                setFourEyesModalOpen(true, {
                  actionType: 'PERIODIC_REVIEW_SIGNOFF',
                  actionTitle: 'Commit Calibrated Rule Sensitivity Policy',
                  targetId: 'POLICY-CSTGB-SENSITIVITY',
                  details: `Update flow=${flowThreshold.toFixed(2)}, burst=${burstMultiplier.toFixed(1)}x, window=${windowHours}h (Est. ${projectedMonthlyAlerts} alerts/mo).`
                });
                addAuditEntry({
                  eventType: 'SYSTEM_CONFIG_CHANGED',
                  entityId: 'RULE-SENSITIVITY-V3',
                  details: `Sensitivity simulated: flow=${flowThreshold.toFixed(2)}, burst=${burstMultiplier.toFixed(1)}x, window=${windowHours}h.`,
                  actionBy: 'Amina Rahman, CFE (Lead Investigator)'
                });
              }}
              className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition-colors flex items-center gap-2 cursor-pointer"
            >
              <Lock className="w-3.5 h-3.5" />
              <span>Apply Calibrated Policy (4-Eyes)</span>
            </button>
          </div>
        </div>
      )}

      {/* Tab 3: Time-Bound Whitelisting */}
      {activeTab === 'WHITELIST' && (
        <div className="space-y-4">
          <div className="p-4 rounded-xl bg-panel border border-line flex items-center justify-between shadow-xl">
            <div>
              <h2 className="text-sm font-bold text-fg font-mono">Institutional Exemption Docket</h2>
              <p className="text-xs text-muted mt-0.5">
                Every whitelist entry requires verified commercial rationale, time-bound expiry, and 4-Eyes CCO authorization.
              </p>
            </div>

            <button
              onClick={() => setIsModalOpen(true)}
              className="px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition-colors flex items-center gap-1.5 cursor-pointer shadow-md shadow-emerald-600/20"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>Add Exemption (4-Eyes)</span>
            </button>
          </div>

          <div className="bg-panel border border-line rounded-xl overflow-hidden shadow-2xl">
            <table className="w-full text-left text-xs text-fg-secondary">
              <thead className="bg-canvas border-b border-line text-xs font-mono text-muted">
                <tr>
                  <th className="px-4 py-3">Exemption ID</th>
                  <th className="px-4 py-3">Corporate Entity</th>
                  <th className="px-4 py-3">Exempted Rule / Threshold</th>
                  <th className="px-4 py-3">Valid Until</th>
                  <th className="px-4 py-3">Authorized By</th>
                  <th className="px-4 py-3 text-center">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-line">
                {whitelist.map((item) => (
                  <tr key={item.id} className="hover:bg-surface/40 transition-colors">
                    <td className="px-4 py-3 font-mono font-bold text-accent-2">{item.id}</td>
                    <td className="px-4 py-3">
                      <div className="font-semibold text-fg">{item.entityName}</div>
                      <div className="text-xs font-mono text-muted">{item.account}</div>
                    </td>
                    <td className="px-4 py-3 text-fg-secondary">{item.ruleExempted}</td>
                    <td className="px-4 py-3 font-mono text-muted">{item.validUntil}</td>
                    <td className="px-4 py-3 font-mono text-muted">{item.authorizedBy}</td>
                    <td className="px-4 py-3 text-center">
                      <span className={`px-2 py-0.5 rounded text-xs font-mono font-bold ${
                        item.status === 'ACTIVE'
                          ? 'bg-emerald-500/20 text-tier-3-text border border-emerald-500/40'
                          : 'bg-amber-500/20 text-tier-2-text border border-amber-500/40'
                      }`}>
                        {item.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Add Exemption Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-panel border border-line-strong rounded-2xl max-w-md w-full p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between pb-3 border-b border-line">
              <h3 className="text-base font-bold text-fg flex items-center gap-2">
                <FileCheck2 className="w-5 h-5 text-tier-3-text" />
                New Whitelist Exemption Request
              </h3>
              <button onClick={() => setIsModalOpen(false)} className="text-muted hover:text-fg-secondary">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleAddExemption} className="space-y-4 text-xs font-sans">
              <div>
                <label className="text-muted block mb-1 font-mono text-xs">Corporate Entity Name</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Beximco Pharmaceuticals Ltd"
                  value={newEntity}
                  onChange={(e) => setNewEntity(e.target.value)}
                  className="w-full px-3 py-2 bg-canvas border border-line-strong rounded-lg text-fg focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div>
                <label className="text-muted block mb-1 font-mono text-xs">Account Number</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. BD55-BEX-9921-0021-4410"
                  value={newAccount}
                  onChange={(e) => setNewAccount(e.target.value)}
                  className="w-full px-3 py-2 bg-canvas border border-line-strong rounded-lg text-fg focus:outline-none focus:border-emerald-500 font-mono"
                />
              </div>

              <div>
                <label className="text-muted block mb-1 font-mono text-xs">Rule Exemption Scope</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Bulk Active Raw Material Import LCs"
                  value={newRule}
                  onChange={(e) => setNewRule(e.target.value)}
                  className="w-full px-3 py-2 bg-canvas border border-line-strong rounded-lg text-fg focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div>
                <label className="text-muted block mb-1 font-mono text-xs">Expiry Date</label>
                <input
                  type="date"
                  required
                  value={newExpiry}
                  onChange={(e) => setNewExpiry(e.target.value)}
                  className="w-full px-3 py-2 bg-canvas border border-line-strong rounded-lg text-fg focus:outline-none focus:border-emerald-500 font-mono"
                />
              </div>

              <div className="flex items-center justify-end gap-3 pt-3 border-t border-line">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 text-muted hover:text-fg-secondary cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold cursor-pointer"
                >
                  Submit for 4-Eyes Approval
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
