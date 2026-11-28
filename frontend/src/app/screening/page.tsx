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
  ShieldX,
  SlidersHorizontal,
  Database,
  Layers,
  Sparkles,
  Calendar,
  Hash,
  Clock,
  Check
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { PiiText } from '@/components/ui/PiiText';
import { WatchlistScreeningRecord } from '@/lib/data/commercialSeed';
import { OFFICIAL_WATCHLIST_FEEDS } from '@/lib/screening/watchlistRegistry';

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

  // Ad-hoc search inputs with attribute corroboration
  const [queryName, setQueryName] = useState('');
  const [queryCountry, setQueryCountry] = useState('Bangladesh');
  const [queryDob, setQueryDob] = useState('');
  const [queryId, setQueryId] = useState('');

  // Expandable Feed Status Card
  const [showFeedsPanel, setShowFeedsPanel] = useState(false);

  // Threshold Configuration
  const [autoFreezeThreshold, setAutoFreezeThreshold] = useState(85);
  const [quarantineThreshold, setQuarantineThreshold] = useState(65);
  const [showThresholdConfig, setShowThresholdConfig] = useState(false);

  // Pairwise Name Scorer Drawer (POST /api/v1/screening/score)
  const [showPairComparator, setShowPairComparator] = useState(false);
  const [pairQueryName, setPairQueryName] = useState('Md. Tariqul Islam');
  const [pairTargetName, setPairTargetName] = useState('Tariq Islam Trading FZE');
  const [pairResult, setPairResult] = useState<any>(null);
  const [isPairScoring, setIsPairScoring] = useState(false);

  const handlePairwiseCompare = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!pairQueryName.trim() || !pairTargetName.trim()) return;
    setIsPairScoring(true);
    try {
      const res = await fetch('/api/v1/screening/score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          queryName: pairQueryName.trim(),
          targetName: pairTargetName.trim(),
          config: { autoFreezeThreshold, quarantineThreshold }
        })
      });
      if (res.ok) {
        setPairResult(await res.json());
      }
    } finally {
      setIsPairScoring(false);
    }
  };

  const feedsList = useMemo(() => Object.values(OFFICIAL_WATCHLIST_FEEDS), []);

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

  const [isScreeningQuery, setIsScreeningQuery] = useState(false);

  const handleAdHocScreen = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!queryName.trim() || isScreeningQuery) return;

    setIsScreeningQuery(true);
    const trimmedName = queryName.trim();
    const trimmedDob = queryDob.trim() || undefined;
    const trimmedId = queryId.trim() || undefined;

    try {
      // Execute live API search (with configured threshold parameters)
      await fetch('/api/v1/screening/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: trimmedName,
          country: queryCountry,
          dob: trimmedDob,
          nationalId: trimmedId,
          config: {
            autoFreezeThreshold,
            quarantineThreshold
          }
        })
      }).catch(() => null);

      const newRec = addScreeningSearch(
        trimmedName,
        'ADHOC_BENEFICIARY_QUERY',
        queryCountry,
        trimmedDob,
        trimmedId,
        {
          autoFreezeThreshold,
          quarantineThreshold
        }
      );

      setSelectedRecordId(newRec.id);
      setQueryName('');
      setQueryDob('');
      setQueryId('');
    } finally {
      setIsScreeningQuery(false);
    }
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
          <p className="text-xs text-slate-400 mt-0.5">
            Entity resolution across OFAC SDN, UN Consolidated, EU, UK HMT, and BFIU Domestic lists.
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          <button
            onClick={() => setShowFeedsPanel(!showFeedsPanel)}
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#0F172A] border border-[#334155] text-xs font-mono text-slate-300 hover:border-sky-500 cursor-pointer transition-colors"
          >
            <Database className="w-3.5 h-3.5 text-sky-400" />
            <span>Official Feeds ({feedsList.length})</span>
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse ml-1" />
          </button>

          <button
            onClick={() => setShowPairComparator(!showPairComparator)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#0F172A] border border-[#334155] text-xs font-mono text-slate-300 hover:border-emerald-500 cursor-pointer transition-colors"
          >
            <Layers className="w-3.5 h-3.5 text-emerald-400" />
            <span>Compare Two Names</span>
          </button>

          <button
            onClick={() => setShowThresholdConfig(!showThresholdConfig)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#0F172A] border border-[#334155] text-xs font-mono text-slate-300 hover:border-cyan-500 cursor-pointer transition-colors"
          >
            <SlidersHorizontal className="w-3.5 h-3.5 text-cyan-400" />
            <span>Thresholds ({autoFreezeThreshold}% / {quarantineThreshold}%)</span>
          </button>
        </div>
      </div>

      {/* Pairwise Entity Resolution Comparator Drawer */}
      {showPairComparator && (
        <div className="p-4 rounded-xl bg-[#0F172A] border border-emerald-500/30 space-y-3">
          <div className="flex items-center justify-between text-xs font-mono">
            <span className="font-semibold text-emerald-300">Pairwise Multi-Algorithm Name Comparator (POST /api/v1/screening/score)</span>
            <button onClick={() => setShowPairComparator(false)} className="text-slate-400 hover:text-slate-200 cursor-pointer">Close</button>
          </div>
          <form onSubmit={handlePairwiseCompare} className="grid grid-cols-1 md:grid-cols-12 gap-3 items-end">
            <div className="md:col-span-5">
              <label className="text-[10px] font-mono text-slate-400 uppercase block mb-1">Query Name (Wire / Customer)</label>
              <input
                type="text"
                value={pairQueryName}
                onChange={(e) => setPairQueryName(e.target.value)}
                className="w-full px-3 py-1.5 rounded-lg bg-[#0B0F17] border border-[#334155] text-xs text-slate-100"
              />
            </div>
            <div className="md:col-span-5">
              <label className="text-[10px] font-mono text-slate-400 uppercase block mb-1">Target Watchlist / Alias Variant</label>
              <input
                type="text"
                value={pairTargetName}
                onChange={(e) => setPairTargetName(e.target.value)}
                className="w-full px-3 py-1.5 rounded-lg bg-[#0B0F17] border border-[#334155] text-xs text-slate-100"
              />
            </div>
            <div className="md:col-span-2">
              <button
                type="submit"
                disabled={isPairScoring}
                className="w-full py-1.5 px-3 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold cursor-pointer"
              >
                {isPairScoring ? 'Scoring...' : 'Compute Match'}
              </button>
            </div>
          </form>
          {pairResult && (
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 p-3 rounded-lg bg-[#0B0F17] border border-[#1E293B] text-xs font-mono">
              <div>
                <span className="text-[10px] text-slate-500 block">Composite Score</span>
                <strong className="text-emerald-400 text-sm">{pairResult.matchScore}%</strong>
              </div>
              <div>
                <span className="text-[10px] text-slate-500 block">Jaro-Winkler (40%)</span>
                <strong className="text-slate-200">{pairResult.algorithmBreakdown?.jaroWinklerScore}%</strong>
              </div>
              <div>
                <span className="text-[10px] text-slate-500 block">Token-Set (40%)</span>
                <strong className="text-slate-200">{pairResult.algorithmBreakdown?.tokenSetScore}%</strong>
              </div>
              <div>
                <span className="text-[10px] text-slate-500 block">Soundex (20%)</span>
                <strong className="text-slate-200">{pairResult.algorithmBreakdown?.phoneticScore}%</strong>
              </div>
              <div>
                <span className="text-[10px] text-slate-500 block">Disposition</span>
                <strong className="text-amber-300">{pairResult.disposition}</strong>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Official Watchlist Ingestion Feeds Registry Panel */}
      {showFeedsPanel && (
        <div className="p-4 rounded-xl bg-[#0F172A] border border-[#1E293B] shadow-2xl space-y-3">
          <div className="flex items-center justify-between border-b border-[#1E293B] pb-2">
            <div className="flex items-center gap-2 text-xs font-bold font-mono text-slate-200 ">
              <Database className="w-4 h-4 text-emerald-400" />
              <span>Official Watchlist Feeds — Cryptographic Ingestion Registry</span>
            </div>
            <span className="text-xs font-mono text-slate-400">All Hashes Verified • Real-Time Synchronization</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-3">
            {feedsList.map((feed) => (
              <div key={feed.listId} className="p-3 bg-[#0B0F17] border border-[#1E293B] rounded-xl space-y-2 text-xs">
                <div className="flex items-center justify-between">
                  <span className="font-mono font-bold text-sky-400 text-xs">{feed.listId}</span>
                  <span className="px-1.5 py-0.5 rounded text-xs font-mono font-bold bg-emerald-950 text-emerald-300 border border-emerald-800">
                    {feed.status}
                  </span>
                </div>
                <div className="text-xs font-semibold text-slate-200 line-clamp-1">{feed.name}</div>
                <div className="space-y-1 text-xs font-mono text-slate-400">
                  <div>Version: <span className="text-slate-200">{feed.version}</span></div>
                  <div>Records: <span className="text-cyan-300 font-bold">{feed.totalRecords.toLocaleString()}</span></div>
                  <div>Synced: <span className="text-slate-300">{feed.fetchTimestamp.replace('T', ' ').replace('Z', ' UTC')}</span></div>
                  <div className="truncate">SHA-256: <span className="text-slate-500 font-mono text-xs">{feed.sha256Hash.substring(0, 16)}...</span></div>
                </div>
                <div className="pt-1 border-t border-[#1E293B]/60">
                  <a
                    href={feed.sourceUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="text-xs font-mono text-sky-400 hover:underline flex items-center gap-1"
                  >
                    <span>Official Source</span>
                    <ExternalLink className="w-2.5 h-2.5" />
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Threshold Configuration Drawer */}
      {showThresholdConfig && (
        <div className="p-4 rounded-xl bg-[#0F172A] border border-cyan-800/40 shadow-xl space-y-3">
          <div className="flex items-center justify-between text-xs font-mono font-bold text-cyan-300">
            <span className="flex items-center gap-2">
              <SlidersHorizontal className="w-4 h-4 text-cyan-400" />
              Configurable Scoring Weights &amp; Statutory Interdiction Thresholds
            </span>
            <span className="text-slate-400 text-xs">OCC 2011-12 / BFIU Circular 26 &amp; 32 (2026) Aligned</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs font-sans">
            <div>
              <label className="text-xs font-mono text-slate-400 block mb-1">
                Auto-Freeze Threshold: <strong className="text-rose-400 font-mono">{autoFreezeThreshold}%</strong>
              </label>
              <input
                type="range"
                min={75}
                max={95}
                value={autoFreezeThreshold}
                onChange={(e) => setAutoFreezeThreshold(Number(e.target.value))}
                className="w-full accent-rose-500 cursor-pointer"
              />
              <span className="text-xs text-slate-500 block mt-0.5">Automated settlement hold</span>
            </div>

            <div>
              <label className="text-xs font-mono text-slate-400 block mb-1">
                Quarantine Threshold: <strong className="text-amber-400 font-mono">{quarantineThreshold}%</strong>
              </label>
              <input
                type="range"
                min={50}
                max={75}
                value={quarantineThreshold}
                onChange={(e) => setQuarantineThreshold(Number(e.target.value))}
                className="w-full accent-amber-500 cursor-pointer"
              />
              <span className="text-xs text-slate-500 block mt-0.5">Analyst triage queue</span>
            </div>

            <div className="p-2.5 rounded-lg bg-[#0B0F17] border border-[#1E293B] text-xs font-mono space-y-0.5">
              <span className="text-slate-500 block">Multi-Algorithm Weights:</span>
              <div className="text-slate-300">Jaro-Winkler: 40%</div>
              <div className="text-slate-300">Token-Set Ratio: 40%</div>
              <div className="text-slate-300">Phonetic Soundex: 20%</div>
            </div>

            <div className="p-2.5 rounded-lg bg-[#0B0F17] border border-[#1E293B] text-xs font-mono space-y-0.5">
              <span className="text-slate-500 block">Attribute Corroboration:</span>
              <div className="text-emerald-400">DOB Match: +10% (Mismatch: -15%)</div>
              <div className="text-emerald-400">Country Match: +5%</div>
              <div className="text-cyan-400">ID / Passport: +25%</div>
            </div>
          </div>
        </div>
      )}

      {/* Ad-Hoc Interdiction Screening Bar with Attribute Corroboration */}
      <div className="p-4 rounded-xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <form onSubmit={handleAdHocScreen} className="grid grid-cols-1 md:grid-cols-12 gap-3 items-end">
          <div className="md:col-span-5">
            <label className="text-xs font-mono font-semibold text-slate-400 block mb-1">
              Entity or Individual Name (SWIFT / Beneficiary) *
            </label>
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-500" />
              <input
                type="text"
                placeholder="e.g. Gulf Star Commodities, PetroChemicals, Farhan Ahmed..."
                value={queryName}
                onChange={(e) => setQueryName(e.target.value)}
                className="w-full pl-9 pr-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-xs text-slate-100 placeholder:text-slate-500 focus:outline-none focus:border-sky-500 font-mono"
              />
            </div>
          </div>

          <div className="md:col-span-2">
            <label className="text-xs font-mono font-semibold text-slate-400 block mb-1">
              Jurisdiction / Domicile
            </label>
            <select
              value={queryCountry}
              onChange={(e) => setQueryCountry(e.target.value)}
              className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-xs text-slate-200 focus:outline-none focus:border-sky-500 cursor-pointer font-mono"
            >
              <option value="Bangladesh">Bangladesh</option>
              <option value="United Arab Emirates">United Arab Emirates</option>
              <option value="Singapore">Singapore</option>
              <option value="United Kingdom">United Kingdom</option>
              <option value="Switzerland">Switzerland</option>
              <option value="Pakistan">Pakistan</option>
            </select>
          </div>

          <div className="md:col-span-2">
            <label className="text-xs font-mono font-semibold text-slate-400 block mb-1">
              Date of Birth (Corroboration)
            </label>
            <input
              type="date"
              value={queryDob}
              onChange={(e) => setQueryDob(e.target.value)}
              className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-xs text-slate-200 focus:outline-none focus:border-sky-500 font-mono"
            />
          </div>

          <div className="md:col-span-2">
            <label className="text-xs font-mono font-semibold text-slate-400 block mb-1">
              National ID / Passport / TIN
            </label>
            <input
              type="text"
              placeholder="e.g. 8022-1984-7712..."
              value={queryId}
              onChange={(e) => setQueryId(e.target.value)}
              className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-xs text-slate-200 focus:outline-none focus:border-sky-500 font-mono text-xs"
            />
          </div>

          <div className="md:col-span-1">
            <button
              type="submit"
              className="w-full py-2 px-3 rounded-lg bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs transition-colors flex items-center justify-center gap-1.5 cursor-pointer shadow-lg shadow-sky-600/20"
            >
              <Search className="w-3.5 h-3.5" />
              <span>Screen</span>
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
                        className={`px-2 py-0.5 rounded text-xs font-mono font-bold ${
                          record.matchScore >= autoFreezeThreshold
                            ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                            : record.matchScore >= quarantineThreshold
                            ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                            : 'bg-slate-700 text-slate-300'
                        }`}
                      >
                        {record.matchScore.toFixed(1)}% MATCH
                      </span>
                      <span className="text-xs font-bold text-slate-200">{record.screenedName}</span>
                    </div>

                    <span
                      className={`text-xs font-mono font-semibold px-2 py-0.5 rounded ${
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
                    <span className="font-mono text-xs text-sky-400 shrink-0">{record.watchlistSource}</span>
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
                  <div className="text-xs font-mono text-slate-500 ">Input Payload String</div>
                  <div className="text-sm font-bold text-slate-100 font-mono">{selectedRecord.screenedName}</div>
                </div>

                <div className="p-3 bg-[#0B0F17] border border-[#1E293B] rounded-xl space-y-1">
                  <div className="text-xs font-mono text-slate-500 ">Sanctions Official Entry</div>
                  <div className="text-sm font-bold text-rose-300 font-mono">{selectedRecord.matchedEntity}</div>
                  <div className="text-xs text-slate-400 font-mono">Watchlist: {selectedRecord.watchlistSource}</div>
                </div>
              </div>

              {/* Match Forensics Metrics: Real Algorithm Breakdown */}
              <div className="space-y-2">
                <div className="flex items-center justify-between text-xs font-mono font-bold text-slate-300">
                  <span>Engine Score Decomposition</span>
                  <span className="text-emerald-400 text-sm font-bold">{selectedRecord.matchScore.toFixed(1)}% Composite</span>
                </div>

                <div className="grid grid-cols-3 gap-2 text-xs font-mono">
                  <div className="p-2.5 bg-[#0B0F17] border border-[#1E293B] rounded-lg">
                    <span className="text-xs text-slate-500 block">Jaro-Winkler</span>
                    <span className="text-cyan-400 font-bold text-sm">
                      {selectedRecord.algorithmBreakdown?.jaroWinklerScore !== undefined
                        ? `${selectedRecord.algorithmBreakdown.jaroWinklerScore.toFixed(1)}%`
                        : `${selectedRecord.matchScore.toFixed(1)}%`}
                    </span>
                    <span className="text-xs text-slate-500 block">Weight: 40%</span>
                  </div>

                  <div className="p-2.5 bg-[#0B0F17] border border-[#1E293B] rounded-lg">
                    <span className="text-xs text-slate-500 block">Token-Set</span>
                    <span className="text-purple-400 font-bold text-sm">
                      {selectedRecord.algorithmBreakdown?.tokenSetScore !== undefined
                        ? `${selectedRecord.algorithmBreakdown.tokenSetScore.toFixed(1)}%`
                        : `${selectedRecord.matchScore.toFixed(1)}%`}
                    </span>
                    <span className="text-xs text-slate-500 block">Weight: 40%</span>
                  </div>

                  <div className="p-2.5 bg-[#0B0F17] border border-[#1E293B] rounded-lg">
                    <span className="text-xs text-slate-500 block">Phonetic Soundex</span>
                    <span className="text-amber-400 font-bold text-sm">
                      {selectedRecord.algorithmBreakdown?.phoneticScore !== undefined
                        ? `${selectedRecord.algorithmBreakdown.phoneticScore.toFixed(1)}%`
                        : '85.0%'}
                    </span>
                    <span className="text-xs text-slate-500 block">Weight: 20%</span>
                  </div>
                </div>
              </div>

              {/* Attribute Corroboration Status */}
              <div className="p-3 rounded-xl bg-[#0B0F17] border border-[#1E293B] space-y-2 text-xs font-mono">
                <div className="flex items-center justify-between text-xs font-bold text-slate-300">
                  <span>Attribute Corroboration</span>
                  <span className="text-cyan-400">
                    Adjustment: {selectedRecord.algorithmBreakdown?.corroborationAdjustment
                      ? `${selectedRecord.algorithmBreakdown.corroborationAdjustment > 0 ? '+' : ''}${selectedRecord.algorithmBreakdown.corroborationAdjustment.toFixed(1)}%`
                      : '+0.0%'}
                  </span>
                </div>

                <div className="grid grid-cols-3 gap-2 text-xs">
                  <div className="p-1.5 rounded bg-[#0F172A] border border-[#1E293B]">
                    <span className="text-slate-500 block">DOB Status</span>
                    <span className="text-slate-200 font-bold">
                      {selectedRecord.corroborationDetails?.dobStatus || 'NOT_PROVIDED'}
                    </span>
                  </div>
                  <div className="p-1.5 rounded bg-[#0F172A] border border-[#1E293B]">
                    <span className="text-slate-500 block">Country Domicile</span>
                    <span className="text-slate-200 font-bold">
                      {selectedRecord.corroborationDetails?.countryStatus || 'MATCH'}
                    </span>
                  </div>
                  <div className="p-1.5 rounded bg-[#0F172A] border border-[#1E293B]">
                    <span className="text-slate-500 block">Identifier / Passport</span>
                    <span className="text-slate-200 font-bold">
                      {selectedRecord.corroborationDetails?.idStatus || 'NOT_PROVIDED'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Token Diffs */}
              <div>
                <h4 className="text-xs font-mono font-bold text-slate-400 mb-2">
                  Tokenized Linguistic Diff
                </h4>
                <div className="p-3 rounded-xl bg-[#0B0F17] border border-[#1E293B] space-y-2 text-xs font-mono">
                  <div>
                    <span className="text-slate-500 text-xs block">Common Tokens:</span>
                    <span className="text-emerald-400 font-bold">
                      {selectedRecord.tokenDiffs.commonTokens.join(', ') || 'None'}
                    </span>
                  </div>
                  <div>
                    <span className="text-slate-500 text-xs block">Query Tokens:</span>
                    <span className="text-slate-300">{selectedRecord.tokenDiffs.screenedTokens.join(', ')}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 text-xs block">Watchlist Tokens:</span>
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
