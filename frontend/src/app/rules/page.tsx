'use client';

import React, { useState } from 'react';
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
    ruleExempted: 'High-Volume Oil Import Wire Spikes (&gt; $50M)',
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
          <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2 font-sans">
            <SlidersHorizontal className="w-5 h-5 text-emerald-400" />
            Compliance Rule Studio, Sensitivity &amp; Whitelisting
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Shadow-mode Champion vs Challenger evaluation, internal threshold calibration, and audited time-bound institutional exemptions.
          </p>
        </div>

        {/* Tab Switcher */}
        <div className="flex items-center bg-[#0F172A] p-1 rounded-xl border border-[#334155] text-xs font-semibold">
          <button
            onClick={() => setActiveTab('CHAMPION_CHALLENGER')}
            className={`px-3 py-1.5 rounded-lg transition-colors cursor-pointer ${
              activeTab === 'CHAMPION_CHALLENGER'
                ? 'bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/40'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Champion vs Challenger (Shadow Mode)
          </button>
          <button
            onClick={() => setActiveTab('SENSITIVITY_SIM')}
            className={`px-3 py-1.5 rounded-lg transition-colors cursor-pointer ${
              activeTab === 'SENSITIVITY_SIM'
                ? 'bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/40'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Internal Sensitivity Calibration
          </button>
          <button
            onClick={() => setActiveTab('WHITELIST')}
            className={`px-3 py-1.5 rounded-lg transition-colors cursor-pointer ${
              activeTab === 'WHITELIST'
                ? 'bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/40'
                : 'text-slate-400 hover:text-slate-200'
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
            <div className="p-5 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl space-y-4">
              <div className="flex items-center justify-between pb-2 border-b border-[#1E293B]">
                <div>
                  <span className="text-[10px] font-mono text-slate-500 uppercase font-bold">Active In-Flight Rule</span>
                  <h3 className="text-sm font-bold text-slate-100 font-mono">Champion: Legacy Threshold Engine v2.4</h3>
                </div>
                <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-sky-500/20 text-sky-300 border border-sky-500/30">
                  PRODUCTION LIVE
                </span>
              </div>

              <div className="space-y-2 text-xs">
                <div className="p-3 bg-[#0B0F17] rounded-xl flex items-center justify-between">
                  <span className="text-slate-400">Monthly Alert Volume:</span>
                  <strong className="font-mono text-slate-200">14,820 alerts / mo</strong>
                </div>
                <div className="p-3 bg-[#0B0F17] rounded-xl flex items-center justify-between">
                  <span className="text-slate-400">False Positive Rate:</span>
                  <strong className="font-mono text-rose-400">88.4% (Heavy Analyst Fatigue)</strong>
                </div>
                <div className="p-3 bg-[#0B0F17] rounded-xl flex items-center justify-between">
                  <span className="text-slate-400">Mean Triage Duration:</span>
                  <strong className="font-mono text-slate-200">14.2 minutes / alert</strong>
                </div>
              </div>
            </div>

            {/* Challenger Card */}
            <div className="p-5 rounded-2xl bg-[#0F172A] border border-emerald-500/40 shadow-xl space-y-4">
              <div className="flex items-center justify-between pb-2 border-b border-[#1E293B]">
                <div>
                  <span className="text-[10px] font-mono text-emerald-400 uppercase font-bold">Shadow Mode Evaluation</span>
                  <h3 className="text-sm font-bold text-slate-100 font-mono">Challenger: Calibrated Topology Gate v3.0</h3>
                </div>
                <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                  READY FOR PROMOTION
                </span>
              </div>

              <div className="space-y-2 text-xs">
                <div className="p-3 bg-[#0B0F17] rounded-xl flex items-center justify-between">
                  <span className="text-slate-400">Monthly Alert Volume:</span>
                  <strong className="font-mono text-emerald-400">4,120 alerts / mo (-72.2%)</strong>
                </div>
                <div className="p-3 bg-[#0B0F17] rounded-xl flex items-center justify-between">
                  <span className="text-slate-400">False Positive Reduction:</span>
                  <strong className="font-mono text-emerald-400">-42.8% False Positive Drop</strong>
                </div>
                <div className="p-3 bg-[#0B0F17] rounded-xl flex items-center justify-between">
                  <span className="text-slate-400">True Positive Capture:</span>
                  <strong className="font-mono text-emerald-400">+18.4% Greater Complex Laundering Capture</strong>
                </div>
              </div>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-[#0F172A] border border-[#1E293B] flex items-center justify-between">
            <p className="text-xs text-slate-400">
              Challenger rule has operated in shadow mode for 30 consecutive calendar days with zero missed Tier 1 regulatory incidents.
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
        <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-2xl space-y-6">
          <div className="p-3.5 bg-amber-950/30 border border-amber-800/60 rounded-xl flex items-start gap-2.5 text-xs text-amber-300">
            <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5 text-amber-400" />
            <div>
              <strong>Confidential Internal Analyst Workspace:</strong> Under Section 27 of the Money Laundering Prevention Act 2012 (MLPA 2012 § 27), sensitivity parameters and threshold configurations are strictly internal bank work product. Disclosing minimum structuring amounts or evasion guidance to customers is a criminal offense punishable by up to 2 years imprisonment.
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-4 bg-[#0B0F17] rounded-xl border border-[#1E293B] space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="font-semibold text-slate-300">Pass-Through Flow Threshold</span>
                <span className="font-mono font-bold text-emerald-400">{flowThreshold.toFixed(2)}</span>
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
              <p className="text-[11px] text-slate-500">
                Accounts with inflow ≈ outflow within this ratio are flagged as transit conduits.
              </p>
            </div>

            <div className="p-4 bg-[#0B0F17] rounded-xl border border-[#1E293B] space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="font-semibold text-slate-300">Velocity Burst Multiplier</span>
                <span className="font-mono font-bold text-amber-400">{burstMultiplier.toFixed(1)}x</span>
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
              <p className="text-[11px] text-slate-500">
                Surges above customer 90-day moving average volume trigger immediate Tier 2 review.
              </p>
            </div>

            <div className="p-4 bg-[#0B0F17] rounded-xl border border-[#1E293B] space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="font-semibold text-slate-300">Structuring Time Window</span>
                <span className="font-mono font-bold text-sky-400">{windowHours}h</span>
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
              <p className="text-[11px] text-slate-500">
                Rolling aggregation window for multi-agent deposits below ৳1,000,000 BDT statutory ceiling (MLPA 2012 § 2(z) &amp; BFIU Circular 26).
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Tab 3: Time-Bound Whitelisting */}
      {activeTab === 'WHITELIST' && (
        <div className="space-y-4">
          <div className="p-4 rounded-xl bg-[#0F172A] border border-[#1E293B] flex items-center justify-between shadow-xl">
            <div>
              <h2 className="text-sm font-bold text-slate-100 font-mono">Institutional Exemption Docket</h2>
              <p className="text-xs text-slate-400 mt-0.5">
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

          <div className="bg-[#0F172A] border border-[#1E293B] rounded-xl overflow-hidden shadow-2xl">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-[#0B0F17] border-b border-[#1E293B] text-[11px] font-mono uppercase text-slate-400">
                <tr>
                  <th className="px-4 py-3">Exemption ID</th>
                  <th className="px-4 py-3">Corporate Entity</th>
                  <th className="px-4 py-3">Exempted Rule / Threshold</th>
                  <th className="px-4 py-3">Valid Until</th>
                  <th className="px-4 py-3">Authorized By</th>
                  <th className="px-4 py-3 text-center">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1E293B]">
                {whitelist.map((item) => (
                  <tr key={item.id} className="hover:bg-[#1E293B]/40 transition-colors">
                    <td className="px-4 py-3 font-mono font-bold text-sky-400">{item.id}</td>
                    <td className="px-4 py-3">
                      <div className="font-semibold text-slate-100">{item.entityName}</div>
                      <div className="text-[11px] font-mono text-slate-400">{item.account}</div>
                    </td>
                    <td className="px-4 py-3 text-slate-300">{item.ruleExempted}</td>
                    <td className="px-4 py-3 font-mono text-slate-400">{item.validUntil}</td>
                    <td className="px-4 py-3 font-mono text-slate-400">{item.authorizedBy}</td>
                    <td className="px-4 py-3 text-center">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
                        item.status === 'ACTIVE'
                          ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                          : 'bg-amber-500/20 text-amber-300 border border-amber-500/40'
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
          <div className="bg-[#0F172A] border border-[#334155] rounded-2xl max-w-md w-full p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between pb-3 border-b border-[#1E293B]">
              <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
                <FileCheck2 className="w-5 h-5 text-emerald-400" />
                New Whitelist Exemption Request
              </h3>
              <button onClick={() => setIsModalOpen(false)} className="text-slate-400 hover:text-slate-200">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleAddExemption} className="space-y-4 text-xs font-sans">
              <div>
                <label className="text-slate-400 block mb-1 font-mono uppercase text-[10px]">Corporate Entity Name</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Beximco Pharmaceuticals Ltd"
                  value={newEntity}
                  onChange={(e) => setNewEntity(e.target.value)}
                  className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-100 focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div>
                <label className="text-slate-400 block mb-1 font-mono uppercase text-[10px]">Account Number</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. BD55-BEX-9921-0021-4410"
                  value={newAccount}
                  onChange={(e) => setNewAccount(e.target.value)}
                  className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-100 focus:outline-none focus:border-emerald-500 font-mono"
                />
              </div>

              <div>
                <label className="text-slate-400 block mb-1 font-mono uppercase text-[10px]">Rule Exemption Scope</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Bulk Active Raw Material Import LCs"
                  value={newRule}
                  onChange={(e) => setNewRule(e.target.value)}
                  className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-100 focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div>
                <label className="text-slate-400 block mb-1 font-mono uppercase text-[10px]">Expiry Date</label>
                <input
                  type="date"
                  required
                  value={newExpiry}
                  onChange={(e) => setNewExpiry(e.target.value)}
                  className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-100 focus:outline-none focus:border-emerald-500 font-mono"
                />
              </div>

              <div className="flex items-center justify-end gap-3 pt-3 border-t border-[#1E293B]">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 text-slate-400 hover:text-slate-200 cursor-pointer"
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
