'use client';

import React, { useState, useMemo } from 'react';
import Link from 'next/link';
import {
  Users,
  Search,
  Building2,
  User,
  ShieldAlert,
  AlertTriangle,
  CheckCircle2,
  TrendingUp,
  FileText,
  MailQuestion,
  GitFork,
  ExternalLink,
  RefreshCw,
  SlidersHorizontal,
  ChevronRight,
  ShieldCheck,
  Calendar,
  DollarSign
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { PiiText } from '@/components/ui/PiiText';
import { CommercialCustomer } from '@/lib/data/commercialSeed';
import { formatCurrencyByJurisdiction } from '@/lib/compliance/jurisdictions';

export default function CustomerDirectoryPage() {
  const { customers, updateCustomerRiskRating, jurisdiction, setFourEyesModalOpen } = useBankingStore();
  const [selectedCustomerId, setSelectedCustomerId] = useState<string>(customers[0]?.id || '');
  const [searchQuery, setSearchQuery] = useState('');
  const [riskFilter, setRiskFilter] = useState<'ALL' | 'HIGH_EDD' | 'MEDIUM' | 'LOW' | 'PROHIBITED'>('ALL');
  const [ratingModalOpen, setRatingModalOpen] = useState(false);
  const [newRating, setNewRating] = useState<'HIGH_EDD' | 'MEDIUM' | 'LOW'>('HIGH_EDD');
  const [ratingMemo, setRatingMemo] = useState('');

  const filteredCustomers = useMemo(() => {
    return customers.filter((cust) => {
      const matchesRisk = riskFilter === 'ALL' || cust.riskRating === riskFilter;
      const matchesSearch =
        searchQuery === '' ||
        cust.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        cust.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
        cust.accountNumber.toLowerCase().includes(searchQuery.toLowerCase());

      return matchesRisk && matchesSearch;
    });
  }, [customers, riskFilter, searchQuery]);

  const selectedCustomer = useMemo(() => {
    return customers.find((c) => c.id === selectedCustomerId) || customers[0];
  }, [customers, selectedCustomerId]);

  const handleUpdateRating = () => {
    if (!selectedCustomer) return;
    updateCustomerRiskRating(selectedCustomer.id, newRating, ratingMemo || 'Supervisory risk re-assessment.');
    setRatingModalOpen(false);
    setRatingMemo('');
  };

  return (
    <div className="p-4 sm:p-5 lg:p-6 max-w-[1750px] mx-auto space-y-5">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-fg flex items-center gap-2 font-sans">
            <Users className="w-5 h-5 text-tier-3-text" />
            Customer 360° KYC/EDD Institutional Profiles
          </h1>
          <p className="text-xs text-muted mt-0.5">
            EDD dossiers, Ultimate Beneficial Ownership (UBO), and expected turnover variance.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-panel border border-line-strong text-xs font-mono text-fg-secondary">
            <span>Customer Base: <strong>{customers.length} Entities</strong></span>
            <span>•</span>
            <span className="text-tier-1-text">
              <strong>{customers.filter((c) => c.riskRating === 'HIGH_EDD').length} High Risk (EDD)</strong>
            </span>
          </div>
        </div>
      </div>

      {/* Main Split Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Left Side: Customer Directory List */}
        <div className="lg:col-span-5 space-y-3">
          {/* Search and Risk Tabs */}
          <div className="flex flex-wrap items-center justify-between gap-2 pb-2 border-b border-line">
            <div className="flex items-center gap-1">
              {(['ALL', 'HIGH_EDD', 'MEDIUM', 'LOW'] as const).map((r) => (
                <button
                  key={r}
                  onClick={() => setRiskFilter(r)}
                  className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition-colors cursor-pointer ${
                    riskFilter === r
                      ? 'bg-surface text-fg border border-line-strong'
                      : 'text-muted hover:text-fg-secondary'
                  }`}
                >
                  {r === 'ALL' ? 'All' : r === 'HIGH_EDD' ? 'High (EDD)' : r}
                </button>
              ))}
            </div>

            <div className="relative w-44">
              <Search className="w-3.5 h-3.5 absolute left-2.5 top-2 text-fg0" />
              <input
                type="text"
                placeholder="Search entities..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-8 pr-2.5 py-1 bg-panel border border-line-strong rounded-lg text-xs text-fg-secondary placeholder:text-fg0 focus:outline-none"
              />
            </div>
          </div>

          {/* Customer Cards List */}
          <div className="space-y-2 max-h-[700px] overflow-y-auto pr-1">
            {filteredCustomers.map((cust) => {
              const isSelected = selectedCustomer?.id === cust.id;
              const variancePct = ((cust.actualMonthlyTurnoverUsd - cust.declaredMonthlyTurnoverUsd) / cust.declaredMonthlyTurnoverUsd) * 100;

              return (
                <div
                  key={cust.id}
                  onClick={() => setSelectedCustomerId(cust.id)}
                  className={`p-3.5 rounded-xl border transition-all cursor-pointer ${
                    isSelected
                      ? 'bg-surface/80 border-emerald-500 shadow-lg'
                      : 'bg-panel border-line hover:border-line-strong'
                  }`}
                >
                  <div className="flex items-center justify-between gap-2">
                    <div className="flex items-center gap-2">
                      <span
                        className={`px-2 py-0.5 rounded text-xs font-mono font-bold ${
                          cust.riskRating === 'HIGH_EDD'
                            ? 'bg-rose-500/20 text-tier-1-text border border-rose-500/30'
                            : cust.riskRating === 'MEDIUM'
                            ? 'bg-amber-500/20 text-tier-2-text border border-amber-500/30'
                            : 'bg-emerald-500/20 text-tier-3-text border border-emerald-500/30'
                        }`}
                      >
                        {cust.riskRating.replace(/_/g, ' ')}
                      </span>
                      <span className="text-xs font-bold text-fg">{cust.name}</span>
                    </div>

                    <span className="text-xs font-mono text-fg0">{cust.id}</span>
                  </div>

                  <div className="mt-2 flex items-center justify-between text-xs text-muted">
                    <span className="truncate">{cust.type}</span>
                    <span className={`font-mono text-xs font-semibold ${variancePct > 50 ? 'text-tier-1-text' : 'text-tier-3-text'}`}>
                      {variancePct > 0 ? `+${variancePct.toFixed(0)}%` : `${variancePct.toFixed(0)}%`} Volume Variance
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Side: Customer Dossier View */}
        <div className="lg:col-span-7 bg-panel border border-line rounded-2xl p-6 shadow-2xl space-y-6">
          {selectedCustomer ? (
            <div className="space-y-6">
              {/* Header Profile Bar */}
              <div className="flex flex-wrap items-start justify-between gap-4 pb-4 border-b border-line">
                <div>
                  <div className="flex items-center gap-2">
                    <span className={`px-2 py-0.5 rounded text-xs font-mono font-bold ${
                      selectedCustomer.riskRating === 'HIGH_EDD'
                        ? 'bg-rose-500/20 text-tier-1-text border border-rose-500/40'
                        : selectedCustomer.riskRating === 'MEDIUM'
                        ? 'bg-amber-500/20 text-tier-2-text border border-amber-500/40'
                        : 'bg-emerald-500/20 text-tier-3-text border border-emerald-500/40'
                    }`}>
                      {selectedCustomer.riskRating.replace(/_/g, ' ')}
                    </span>
                    <h2 className="text-lg font-bold text-fg font-sans">
                      {selectedCustomer.name}
                    </h2>
                  </div>
                  <p className="text-xs text-muted mt-1 flex flex-wrap items-center gap-x-1.5">
                    <span>Account:</span> <PiiText value={selectedCustomer.accountNumber} type="account" className="text-fg-secondary font-mono font-bold" /> <span>• Onboarded: <strong className="text-fg-secondary font-mono">{selectedCustomer.onboardedDate}</strong></span> <span>• Next Review: <strong className="text-fg-secondary font-mono">{selectedCustomer.nextReviewDate}</strong></span>
                  </p>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => {
                      setNewRating(selectedCustomer.riskRating === 'HIGH_EDD' ? 'HIGH_EDD' : selectedCustomer.riskRating === 'MEDIUM' ? 'MEDIUM' : 'LOW');
                      setRatingModalOpen(true);
                    }}
                    className="px-3 py-1.5 rounded-lg bg-surface hover:bg-surface-hover text-fg-secondary text-xs font-semibold border border-line-strong cursor-pointer"
                  >
                    Adjust Risk Rating
                  </button>

                  <Link
                    href={`/graph?node=${encodeURIComponent(selectedCustomer.accountNumber)}`}
                    className="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold flex items-center gap-1.5"
                  >
                    <GitFork className="w-3.5 h-3.5" />
                    <span>Inspect Graph</span>
                  </Link>
                </div>
              </div>

              {/* KYC Identification Matrix */}
              <div>
                <h3 className="text-xs font-bold text-fg-secondary mb-2 font-mono">
                  KYC &amp; Corporate Registration
                </h3>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
                  <div className="p-3 rounded-xl bg-canvas border border-line">
                    <span className="text-fg0 text-xs font-mono block">Trade License / Reg No</span>
                    <span className="font-mono font-bold text-fg-secondary mt-0.5 block">{selectedCustomer.registrationNo}</span>
                  </div>
                  <div className="p-3 rounded-xl bg-canvas border border-line">
                    <span className="text-fg0 text-xs font-mono block">Masked NID / TIN</span>
                    <PiiText value={selectedCustomer.maskedNidTin} type="account" className="font-mono font-bold text-fg-secondary mt-0.5 block" />
                  </div>
                  <div className="p-3 rounded-xl bg-canvas border border-line">
                    <span className="text-fg0 text-xs font-mono block">Account Status</span>
                    <span className={`font-mono font-bold mt-0.5 block ${selectedCustomer.accountStatus === 'FROZEN' ? 'text-tier-1-text' : 'text-tier-3-text'}`}>
                      {selectedCustomer.accountStatus}
                    </span>
                  </div>
                </div>
              </div>

              {/* Turnover Variance Analysis */}
              <div>
                <h3 className="text-xs font-bold text-fg-secondary mb-2 font-mono flex items-center justify-between">
                  <span>Declared vs Actual Monthly Turnover</span>
                  <span className="text-xs font-mono text-tier-2-text">
                    Threshold: &gt;50% Variance Triggers EDD
                  </span>
                </h3>

                <div className="p-4 rounded-xl bg-canvas border border-line space-y-3">
                  <div className="flex items-center justify-between text-xs">
                    <div>
                      <span className="text-muted">Declared Turnover: </span>
                      <strong className="text-fg-secondary font-mono">
                        ${selectedCustomer.declaredMonthlyTurnoverUsd.toLocaleString()} USD
                      </strong>
                    </div>
                    <div>
                      <span className="text-muted">Actual Trailing Turnover: </span>
                      <strong className="text-tier-3-text font-mono text-sm">
                        ${selectedCustomer.actualMonthlyTurnoverUsd.toLocaleString()} USD
                      </strong>
                    </div>
                  </div>

                  {/* Visual Progress Bar */}
                  <div className="w-full h-3 bg-surface rounded-full overflow-hidden flex">
                    <div
                      style={{
                        width: `${Math.min(
                          (selectedCustomer.declaredMonthlyTurnoverUsd / selectedCustomer.actualMonthlyTurnoverUsd) * 100,
                          100
                        )}%`,
                      }}
                      className="bg-sky-500 h-full"
                    />
                    <div
                      style={{
                        width: `${Math.max(
                          0,
                          100 - (selectedCustomer.declaredMonthlyTurnoverUsd / selectedCustomer.actualMonthlyTurnoverUsd) * 100
                        )}%`,
                      }}
                      className="bg-rose-500 h-full"
                    />
                  </div>

                  <div className="flex items-center justify-between text-xs text-muted font-mono">
                    <span>Blue: Declared Baseline</span>
                    <span className="text-tier-1-text font-bold">
                      Variance: +
                      {(
                        ((selectedCustomer.actualMonthlyTurnoverUsd - selectedCustomer.declaredMonthlyTurnoverUsd) /
                          selectedCustomer.declaredMonthlyTurnoverUsd) *
                        100
                      ).toFixed(0)}
                      % Surpassed
                    </span>
                  </div>
                </div>
              </div>

              {/* Ultimate Beneficial Ownership (UBO) Registry */}
              <div>
                <h3 className="text-xs font-bold text-fg-secondary mb-2 font-mono">
                  Ultimate Beneficial Ownership (UBO) Structure (&ge; 10% Ownership)
                </h3>
                <div className="space-y-2">
                  {selectedCustomer.uboHierarchy.map((owner, idx) => (
                    <div key={idx} className="p-3 bg-canvas border border-line rounded-xl flex items-center justify-between text-xs">
                      <div className="flex items-center gap-2">
                        <User className="w-4 h-4 text-muted" />
                        <div>
                          <div className="font-semibold text-fg-secondary">{owner.name}</div>
                          <div className="text-xs text-muted font-mono">
                            Jurisdiction: {owner.jurisdiction} • PEP Status: {owner.pepStatus ? 'POLITICALLY EXPOSED' : 'CLEARED'}
                          </div>
                        </div>
                      </div>

                      <div className="text-right">
                        <span className="font-mono font-bold text-tier-3-text text-sm">
                          {owner.shareholdingPct}%
                        </span>
                        <span className="text-xs text-fg0 block">Direct Equity</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Institutional Action Buttons */}
              <div className="pt-2 flex flex-wrap items-center gap-3">
                <button
                  onClick={() => {
                    setFourEyesModalOpen(true, {
                      actionType: 'PERIODIC_REVIEW_SIGNOFF',
                      actionTitle: `Mandatory Enhanced Due Diligence Review (${selectedCustomer.name})`,
                      targetId: selectedCustomer.id,
                      details: `Sign off on completed EDD review and renewed beneficial ownership disclosures.`
                    });
                  }}
                  className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs transition-colors flex items-center gap-2 cursor-pointer"
                >
                  <ShieldCheck className="w-4 h-4" />
                  <span>Execute EDD Sign-Off (4-Eyes)</span>
                </button>

                <Link
                  href="/rfi"
                  className="px-4 py-2 rounded-xl bg-surface hover:bg-surface-hover text-fg-secondary font-medium text-xs transition-colors flex items-center gap-2"
                >
                  <MailQuestion className="w-4 h-4 text-accent-2" />
                  <span>Dispatch KYC Inquiry (RFI)</span>
                </Link>
              </div>
            </div>
          ) : (
            <div className="py-20 text-center text-fg0 text-xs">
              Select a customer profile to view institutional KYC dossier.
            </div>
          )}
        </div>
      </div>

      {/* Adjust Risk Rating Modal */}
      {ratingModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-panel border border-line-strong rounded-2xl max-w-md w-full p-6 space-y-4 shadow-2xl">
            <h3 className="text-base font-bold text-fg flex items-center gap-2">
              <SlidersHorizontal className="w-5 h-5 text-tier-3-text" />
              Adjust Customer Risk Classification
            </h3>
            <p className="text-xs text-muted">
              Update institutional risk band for <strong>{selectedCustomer?.name}</strong>. This modification requires compliance rationale and will be appended to the WORM audit trail.
            </p>

            <div>
              <label className="text-xs font-mono text-muted block mb-1">New Risk Rating</label>
              <select
                value={newRating}
                onChange={(e) => setNewRating(e.target.value as any)}
                className="w-full px-3 py-2 bg-canvas border border-line-strong rounded-lg text-xs text-fg-secondary cursor-pointer"
              >
                <option value="HIGH_EDD">HIGH (Mandatory Quarterly EDD &amp; Live Wire Hold)</option>
                <option value="MEDIUM">MEDIUM (Standard Annual Review)</option>
                <option value="LOW">LOW (Simplified Due Diligence)</option>
              </select>
            </div>

            <div>
              <label className="text-xs font-mono text-muted block mb-1">Audit Rationale Memo</label>
              <textarea
                value={ratingMemo}
                onChange={(e) => setRatingMemo(e.target.value)}
                placeholder="e.g. Unexplained +312% export turnover variance and port diversion flagged during trade inspection."
                className="w-full h-20 p-3 bg-canvas border border-line-strong rounded-xl text-xs text-fg placeholder:text-slate-600 focus:outline-none"
              />
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                onClick={() => setRatingModalOpen(false)}
                className="px-4 py-2 text-xs text-muted hover:text-fg-secondary cursor-pointer"
              >
                Cancel
              </button>
              <button
                onClick={handleUpdateRating}
                className="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition-colors cursor-pointer"
              >
                Save &amp; Commit to Ledger
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
