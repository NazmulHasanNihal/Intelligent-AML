'use client';

import React, { useState, useMemo } from 'react';
import Link from 'next/link';
import {
  ShieldAlert,
  Search,
  UserCheck,
  AlertTriangle,
  Lock,
  MailQuestion,
  CheckCircle2,
  XCircle,
  FileText,
  Filter,
  Globe,
  Building,
  User,
  ExternalLink,
  ChevronRight,
  ShieldX
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { PiiText } from '@/components/ui/PiiText';
import { WatchlistScreeningRecord } from '@/lib/data/commercialSeed';

export default function SanctionsScreeningPage() {
  const {
    screeningRecords,
    dispositionScreening,
    addScreeningSearch,
    setFourEyesModalOpen,
    jurisdiction
  } = useBankingStore();

  const [activeFilter, setActiveFilter] = useState<'ALL' | 'PENDING' | 'TRUE_HIT' | 'CLEARED'>('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedRecordId, setSelectedRecordId] = useState<string>(screeningRecords[0]?.id || '');

  // Ad-hoc search inputs
  const [queryName, setQueryName] = useState('');
  const [queryCountry, setQueryCountry] = useState('Bangladesh');

  const filteredRecords = useMemo(() => {
    return screeningRecords.filter((rec) => {
      const matchesFilter =
        activeFilter === 'ALL' ||
        (activeFilter === 'PENDING' && rec.disposition === 'PENDING_REVIEW') ||
        (activeFilter === 'TRUE_HIT' && rec.disposition === 'CONFIRMED_TRUE_HIT') ||
        (activeFilter === 'CLEARED' && rec.disposition === 'DISMISSED_FALSE_POSITIVE');

      const matchesSearch =
        searchQuery === '' ||
        rec.screenedName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        rec.matchedEntity.toLowerCase().includes(searchQuery.toLowerCase()) ||
        rec.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
        rec.watchlistSource.toLowerCase().includes(searchQuery.toLowerCase());

      return matchesFilter && matchesSearch;
    });
  }, [screeningRecords, activeFilter, searchQuery]);

  const selectedRecord = useMemo(() => {
    return screeningRecords.find((r) => r.id === selectedRecordId) || screeningRecords[0];
  }, [screeningRecords, selectedRecordId]);

  const handleAdHocScreen = (e: React.FormEvent) => {
    e.preventDefault();
    if (!queryName.trim()) return;

    addScreeningSearch(queryName.trim(), 'ADHOC_BENEFICIARY_QUERY');
    setQueryName('');
  };

  return (
    <div className="p-4 sm:p-5 lg:p-6 max-w-[1750px] mx-auto space-y-5">
      {/* Page Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2 font-sans">
            <Globe className="w-5 h-5 text-sky-400" />
            Sanctions, PEP &amp; Pre-Settlement Screening Interdiction
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Real-time entity resolution against OFAC SDN, UN Consolidated, EU Financial Sanctions, UK HMT, and National BFIU Watchlists.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#0F172A] border border-[#334155] text-xs font-mono text-slate-300">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span>List Sync: <strong>LIVE (00:04:12 ago)</strong></span>
          </div>
        </div>
      </div>

      {/* Ad-Hoc Interdiction Screening Bar */}
      <div className="p-4 rounded-xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <form onSubmit={handleAdHocScreen} className="flex flex-wrap items-center gap-3">
          <div className="flex-1 min-w-[280px]">
            <label className="text-[10px] font-mono font-semibold text-slate-400 uppercase tracking-wider block mb-1">
              Entity or Individual Name (SWIFT / Beneficiary)
            </label>
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-500" />
              <input
                type="text"
                placeholder="e.g. Gulf Star Commodities, PetroChemicals, Al-Mansoor..."
                value={queryName}
                onChange={(e) => setQueryName(e.target.value)}
                className="w-full pl-9 pr-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-xs text-slate-100 placeholder:text-slate-500 focus:outline-none focus:border-sky-500 font-mono"
              />
            </div>
          </div>

          <div className="w-48">
            <label className="text-[10px] font-mono font-semibold text-slate-400 uppercase tracking-wider block mb-1">
              Jurisdiction / Domicile
            </label>
            <select
              value={queryCountry}
              onChange={(e) => setQueryCountry(e.target.value)}
              className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-xs text-slate-200 focus:outline-none focus:border-sky-500 cursor-pointer"
            >
              <option value="Bangladesh">Bangladesh</option>
              <option value="United Arab Emirates">United Arab Emirates</option>
              <option value="Singapore">Singapore</option>
              <option value="United Kingdom">United Kingdom</option>
              <option value="Switzerland">Switzerland</option>
            </select>
          </div>

          <div className="pt-5">
            <button
              type="submit"
              className="px-4 py-2 rounded-lg bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs transition-colors flex items-center gap-2 cursor-pointer shadow-lg shadow-sky-600/20"
            >
              <Search className="w-3.5 h-3.5" />
              <span>Execute Screening</span>
            </button>
          </div>
        </form>
      </div>

      {/* Main Split-Screen Workspace */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Left Column: Screening Hits Queue */}
        <div className="lg:col-span-7 space-y-3">
          {/* Filter Bar */}
          <div className="flex flex-wrap items-center justify-between gap-3 pb-2 border-b border-[#1E293B]">
            <div className="flex items-center gap-1.5">
              <button
                onClick={() => setActiveFilter('ALL')}
                className={`px-3 py-1 rounded-lg text-xs font-semibold cursor-pointer transition-colors ${
                  activeFilter === 'ALL'
                    ? 'bg-[#1E293B] text-slate-100 border border-[#334155]'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                All ({screeningRecords.length})
              </button>
              <button
                onClick={() => setActiveFilter('PENDING')}
                className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold cursor-pointer transition-colors ${
                  activeFilter === 'PENDING'
                    ? 'bg-amber-950/60 text-amber-300 border border-amber-800/60'
                    : 'text-amber-400/80 hover:bg-amber-950/20'
                }`}
              >
                <span className="w-2 h-2 rounded-full bg-amber-500" />
                <span>Interdicted ({screeningRecords.filter((r) => r.disposition === 'PENDING_REVIEW').length})</span>
              </button>
              <button
                onClick={() => setActiveFilter('TRUE_HIT')}
                className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold cursor-pointer transition-colors ${
                  activeFilter === 'TRUE_HIT'
                    ? 'bg-rose-950/60 text-rose-300 border border-rose-800/60'
                    : 'text-rose-400/80 hover:bg-rose-950/20'
                }`}
              >
                <span className="w-2 h-2 rounded-full bg-rose-500" />
                <span>True Hits ({screeningRecords.filter((r) => r.disposition === 'CONFIRMED_TRUE_HIT').length})</span>
              </button>
              <button
                onClick={() => setActiveFilter('CLEARED')}
                className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold cursor-pointer transition-colors ${
                  activeFilter === 'CLEARED'
                    ? 'bg-emerald-950/60 text-emerald-300 border border-emerald-800/60'
                    : 'text-emerald-400/80 hover:bg-emerald-950/20'
                }`}
              >
                <span className="w-2 h-2 rounded-full bg-emerald-500" />
                <span>Cleared ({screeningRecords.filter((r) => r.disposition === 'DISMISSED_FALSE_POSITIVE').length})</span>
              </button>
            </div>

            <div className="relative w-48">
              <Search className="w-3.5 h-3.5 absolute left-2.5 top-2 text-slate-500" />
              <input
                type="text"
                placeholder="Filter hits..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-8 pr-2.5 py-1 bg-[#0F172A] border border-[#334155] rounded-lg text-xs text-slate-200 placeholder:text-slate-500 focus:outline-none"
              />
            </div>
          </div>

          {/* Records List */}
          <div className="space-y-2 max-h-[680px] overflow-y-auto pr-1">
            {filteredRecords.map((record) => {
              const isSelected = selectedRecord?.id === record.id;
              return (
                <div
                  key={record.id}
                  onClick={() => setSelectedRecordId(record.id)}
                  className={`p-3.5 rounded-xl border transition-all cursor-pointer ${
                    isSelected
                      ? 'bg-[#1E293B]/80 border-sky-500 shadow-lg'
                      : 'bg-[#0F172A] border-[#1E293B] hover:border-[#334155]'
                  }`}
                >
                  <div className="flex items-center justify-between gap-3">
                    <div className="flex items-center gap-2">
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
                          record.matchScore >= 90
                            ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                            : record.matchScore >= 70
                            ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                            : 'bg-slate-700 text-slate-300'
                        }`}
                      >
                        {record.matchScore.toFixed(0)}% MATCH
                      </span>
                      <span className="text-xs font-bold text-slate-200">{record.screenedName}</span>
                    </div>

                    <span
                      className={`text-[10px] font-mono font-semibold px-2 py-0.5 rounded ${
                        record.disposition === 'CONFIRMED_TRUE_HIT'
                          ? 'bg-rose-950 text-rose-300 border border-rose-800'
                          : record.disposition === 'PENDING_REVIEW'
                          ? 'bg-amber-950 text-amber-300 border border-amber-800'
                          : 'bg-emerald-950 text-emerald-300 border border-emerald-800'
                      }`}
                    >
                      {record.disposition.replace(/_/g, ' ')}
                    </span>
                  </div>

                  <div className="mt-2 flex items-center justify-between text-xs text-slate-400">
                    <div className="flex items-center gap-2 truncate">
                      <span className="text-slate-500">Target Match:</span>
                      <span className="font-medium text-slate-200 truncate">{record.matchedEntity}</span>
                    </div>
                    <span className="font-mono text-[10px] text-sky-400 shrink-0">{record.watchlistSource}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Column: Match Forensics & Disposition Panel */}
        <div className="lg:col-span-5 bg-[#0F172A] border border-[#1E293B] rounded-2xl p-5 shadow-2xl flex flex-col justify-between space-y-6">
          {selectedRecord ? (
            <div className="space-y-5">
              {/* Header */}
              <div className="pb-4 border-b border-[#1E293B]">
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs text-sky-400 font-bold">{selectedRecord.id}</span>
                  <span className="text-xs text-slate-400 font-mono">{selectedRecord.screenedAt}</span>
                </div>
                <h3 className="text-base font-bold text-slate-100 mt-1 font-sans">
                  Watchlist Match Decomposition
                </h3>
              </div>

              {/* Side-by-Side Name Alignment */}
              <div className="space-y-3">
                <div className="p-3 bg-[#0B0F17] border border-[#1E293B] rounded-xl space-y-1">
                  <div className="text-[10px] font-mono text-slate-500 uppercase">Input Payload String</div>
                  <div className="text-sm font-bold text-slate-100 font-mono">{selectedRecord.screenedName}</div>
                </div>

                <div className="p-3 bg-[#0B0F17] border border-[#1E293B] rounded-xl space-y-1">
                  <div className="text-[10px] font-mono text-slate-500 uppercase">Sanctions Official Entry</div>
                  <div className="text-sm font-bold text-rose-300 font-mono">{selectedRecord.matchedEntity}</div>
                  <div className="text-[11px] text-slate-400 font-mono">Watchlist: {selectedRecord.watchlistSource}</div>
                </div>
              </div>

              {/* Match Forensics Metrics */}
              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="p-3 rounded-xl bg-[#0B0F17] border border-[#1E293B]">
                  <span className="text-slate-500 text-[10px] uppercase font-mono block">Algorithm Confidence</span>
                  <span className="text-lg font-mono font-bold text-emerald-400">
                    {selectedRecord.matchScore.toFixed(1)}%
                  </span>
                  <span className="text-[10px] text-slate-400 block mt-0.5">{selectedRecord.matchAlgorithm}</span>
                </div>

                <div className="p-3 rounded-xl bg-[#0B0F17] border border-[#1E293B]">
                  <span className="text-slate-500 text-[10px] uppercase font-mono block">Match Type</span>
                  <span className="text-xs font-mono font-bold text-rose-400 truncate block mt-1">
                    {selectedRecord.matchType}
                  </span>
                </div>
              </div>

              {/* Token Diffs */}
              <div>
                <h4 className="text-[11px] font-mono font-bold text-slate-400 uppercase tracking-wider mb-2">
                  Tokenized Linguistic Diff
                </h4>
                <div className="p-3 rounded-xl bg-[#0B0F17] border border-[#1E293B] space-y-2 text-xs font-mono">
                  <div>
                    <span className="text-slate-500 text-[10px] block">Common Tokens:</span>
                    <span className="text-emerald-400 font-bold">
                      {selectedRecord.tokenDiffs.commonTokens.join(', ') || 'None'}
                    </span>
                  </div>
                  <div>
                    <span className="text-slate-500 text-[10px] block">Query Tokens:</span>
                    <span className="text-slate-300">{selectedRecord.tokenDiffs.screenedTokens.join(', ')}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 text-[10px] block">Watchlist Tokens:</span>
                    <span className="text-slate-300">{selectedRecord.tokenDiffs.matchedTokens.join(', ')}</span>
                  </div>
                </div>
              </div>

              {/* Disposition Action Buttons */}
              <div className="pt-4 border-t border-[#1E293B] space-y-2.5">
                <button
                  onClick={() => {
                    setFourEyesModalOpen(true, {
                      actionType: 'ACCOUNT_FREEZE',
                      actionTitle: `Confirm Sanctions Match & Block Wire (${selectedRecord.matchedEntity})`,
                      targetId: selectedRecord.id,
                      details: `Confirm true hit on ${selectedRecord.watchlistSource} and immediately block settlement.`
                    });
                  }}
                  className="w-full py-2.5 px-4 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-semibold text-xs transition-colors flex items-center justify-center gap-2 cursor-pointer shadow-lg shadow-rose-600/20"
                >
                  <Lock className="w-4 h-4" />
                  <span>Confirm True Hit &amp; Block Payment (4-Eyes)</span>
                </button>

                <div className="grid grid-cols-2 gap-2">
                  <Link
                    href="/rfi"
                    className="py-2 px-3 rounded-xl bg-[#1E293B] hover:bg-[#334155] text-slate-200 font-medium text-xs transition-colors flex items-center justify-center gap-1.5"
                  >
                    <MailQuestion className="w-3.5 h-3.5 text-sky-400" />
                    <span>Request Customer RFI</span>
                  </Link>

                  <button
                    onClick={() => {
                      dispositionScreening(
                        selectedRecord.id,
                        'DISMISSED_FALSE_POSITIVE',
                        'Analyst confirmed distinct legal entity and differing UBO registry documents.'
                      );
                    }}
                    className="py-2 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium text-xs transition-colors cursor-pointer"
                  >
                    Dismiss False Positive
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <div className="py-20 text-center text-slate-500 text-xs">
              Select an interdiction record from the list to inspect forensic token matches.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
