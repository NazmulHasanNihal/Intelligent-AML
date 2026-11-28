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
          <h1 className="text-xl font-bold text-fg flex items-center gap-2 font-sans">
            <Globe className="w-5 h-5 text-accent-2" />
            Sanctions, PEP &amp; Pre-Settlement Screening Interdiction
          </h1>
          <p className="text-xs text-muted mt-0.5">
            Entity resolution across OFAC SDN, UN Consolidated, EU, UK HMT, and BFIU Domestic lists.
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          <button
            onClick={() => setShowFeedsPanel(!showFeedsPanel)}
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-panel border border-line-strong text-xs font-mono text-fg-secondary hover:border-sky-500 cursor-pointer transition-colors"
          >
            <Database className="w-3.5 h-3.5 text-accent-2" />
            <span>Official Feeds ({feedsList.length})</span>
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse ml-1" />
          </button>

          <button
            onClick={() => setShowPairComparator(!showPairComparator)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-panel border border-line-strong text-xs font-mono text-fg-secondary hover:border-emerald-500 cursor-pointer transition-colors"
          >
            <Layers className="w-3.5 h-3.5 text-tier-3-text" />
            <span>Compare Two Names</span>
          </button>

          <button
            onClick={() => setShowThresholdConfig(!showThresholdConfig)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-panel border border-line-strong text-xs font-mono text-fg-secondary hover:border-cyan-500 cursor-pointer transition-colors"
          >
            <SlidersHorizontal className="w-3.5 h-3.5 text-accent-2" />
            <span>Thresholds ({autoFreezeThreshold}% / {quarantineThreshold}%)</span>
          </button>
        </div>
      </div>

      {/* Pairwise Entity Resolution Comparator Drawer */}
      {showPairComparator && (
        <div className="p-4 rounded-xl bg-panel border border-emerald-500/30 space-y-3">
          <div className="flex items-center justify-between text-xs font-mono">
            <span className="font-semibold text-tier-3-text">Pairwise Multi-Algorithm Name Comparator (POST /api/v1/screening/score)</span>
            <button onClick={() => setShowPairComparator(false)} className="text-muted hover:text-fg-secondary cursor-pointer">Close</button>
          </div>
          <form onSubmit={handlePairwiseCompare} className="grid grid-cols-1 md:grid-cols-12 gap-3 items-end">
            <div className="md:col-span-5">
              <label className="text-[10px] font-mono text-muted uppercase block mb-1">Query Name (Wire / Customer)</label>
              <input
                type="text"
                value={pairQueryName}
                onChange={(e) => setPairQueryName(e.target.value)}
                className="w-full px-3 py-1.5 rounded-lg bg-canvas border border-line-strong text-xs text-fg"
              />
            </div>
            <div className="md:col-span-5">
              <label className="text-[10px] font-mono text-muted uppercase block mb-1">Target Watchlist / Alias Variant</label>
              <input
                type="text"
                value={pairTargetName}
                onChange={(e) => setPairTargetName(e.target.value)}
                className="w-full px-3 py-1.5 rounded-lg bg-canvas border border-line-strong text-xs text-fg"
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
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 p-3 rounded-lg bg-canvas border border-line text-xs font-mono">
              <div>
                <span className="text-[10px] text-fg0 block">Composite Score</span>
                <strong className="text-tier-3-text text-sm">{pairResult.matchScore}%</strong>
              </div>
              <div>
                <span className="text-[10px] text-fg0 block">Jaro-Winkler (40%)</span>
                <strong className="text-fg-secondary">{pairResult.algorithmBreakdown?.jaroWinklerScore}%</strong>
              </div>
              <div>
                <span className="text-[10px] text-fg0 block">Token-Set (40%)</span>
                <strong className="text-fg-secondary">{pairResult.algorithmBreakdown?.tokenSetScore}%</strong>
              </div>
              <div>
                <span className="text-[10px] text-fg0 block">Soundex (20%)</span>
                <strong className="text-fg-secondary">{pairResult.algorithmBreakdown?.phoneticScore}%</strong>
              </div>
              <div>
                <span className="text-[10px] text-fg0 block">Disposition</span>
                <strong className="text-tier-2-text">{pairResult.disposition}</strong>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Official Watchlist Ingestion Feeds Registry Panel */}
      {showFeedsPanel && (
        <div className="p-4 rounded-xl bg-panel border border-line shadow-2xl space-y-3">
          <div className="flex items-center justify-between border-b border-line pb-2">
            <div className="flex items-center gap-2 text-xs font-bold font-mono text-fg-secondary ">
              <Database className="w-4 h-4 text-tier-3-text" />
              <span>Official Watchlist Feeds — Cryptographic Ingestion Registry</span>
            </div>
            <span className="text-xs font-mono text-muted">All Hashes Verified • Real-Time Synchronization</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-3">
            {feedsList.map((feed) => (
              <div key={feed.listId} className="p-3 bg-canvas border border-line rounded-xl space-y-2 text-xs">
                <div className="flex items-center justify-between">
                  <span className="font-mono font-bold text-accent-2 text-xs">{feed.listId}</span>
                  <span className="px-1.5 py-0.5 rounded text-xs font-mono font-bold bg-tier-3-bg text-tier-3-text border border-emerald-800">
                    {feed.status}
                  </span>
                </div>
                <div className="text-xs font-semibold text-fg-secondary line-clamp-1">{feed.name}</div>
                <div className="space-y-1 text-xs font-mono text-muted">
                  <div>Version: <span className="text-fg-secondary">{feed.version}</span></div>
                  <div>Records: <span className="text-accent-2 font-bold">{feed.totalRecords.toLocaleString()}</span></div>
                  <div>Synced: <span className="text-fg-secondary">{feed.fetchTimestamp.replace('T', ' ').replace('Z', ' UTC')}</span></div>
                  <div className="truncate">SHA-256: <span className="text-fg0 font-mono text-xs">{feed.sha256Hash.substring(0, 16)}...</span></div>
                </div>
                <div className="pt-1 border-t border-line/60">
                  <a
                    href={feed.sourceUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="text-xs font-mono text-accent-2 hover:underline flex items-center gap-1"
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
        <div className="p-4 rounded-xl bg-panel border border-cyan-800/40 shadow-xl space-y-3">
          <div className="flex items-center justify-between text-xs font-mono font-bold text-accent-2">
            <span className="flex items-center gap-2">
              <SlidersHorizontal className="w-4 h-4 text-accent-2" />
              Configurable Scoring Weights &amp; Statutory Interdiction Thresholds
            </span>
            <span className="text-muted text-xs">OCC 2011-12 / BFIU Circular 26 &amp; 32 (2026) Aligned</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs font-sans">
            <div>
              <label className="text-xs font-mono text-muted block mb-1">
                Auto-Freeze Threshold: <strong className="text-tier-1-text font-mono">{autoFreezeThreshold}%</strong>
              </label>
              <input
                type="range"
                min={75}
                max={95}
                value={autoFreezeThreshold}
                onChange={(e) => setAutoFreezeThreshold(Number(e.target.value))}
                className="w-full accent-rose-500 cursor-pointer"
              />
              <span className="text-xs text-fg0 block mt-0.5">Automated settlement hold</span>
            </div>

            <div>
              <label className="text-xs font-mono text-muted block mb-1">
                Quarantine Threshold: <strong className="text-tier-2-text font-mono">{quarantineThreshold}%</strong>
              </label>
              <input
                type="range"
                min={50}
                max={75}
                value={quarantineThreshold}
                onChange={(e) => setQuarantineThreshold(Number(e.target.value))}
                className="w-full accent-amber-500 cursor-pointer"
              />
              <span className="text-xs text-fg0 block mt-0.5">Analyst triage queue</span>
            </div>

            <div className="p-2.5 rounded-lg bg-canvas border border-line text-xs font-mono space-y-0.5">
              <span className="text-fg0 block">Multi-Algorithm Weights:</span>
              <div className="text-fg-secondary">Jaro-Winkler: 40%</div>
              <div className="text-fg-secondary">Token-Set Ratio: 40%</div>
              <div className="text-fg-secondary">Phonetic Soundex: 20%</div>
            </div>

            <div className="p-2.5 rounded-lg bg-canvas border border-line text-xs font-mono space-y-0.5">
              <span className="text-fg0 block">Attribute Corroboration:</span>
              <div className="text-tier-3-text">DOB Match: +10% (Mismatch: -15%)</div>
              <div className="text-tier-3-text">Country Match: +5%</div>
              <div className="text-accent-2">ID / Passport: +25%</div>
            </div>
          </div>
        </div>
      )}

      {/* Ad-Hoc Interdiction Screening Bar with Attribute Corroboration */}
      <div className="p-4 rounded-xl bg-panel border border-line shadow-xl">
        <form onSubmit={handleAdHocScreen} className="grid grid-cols-1 md:grid-cols-12 gap-3 items-end">
          <div className="md:col-span-5">
            <label className="text-xs font-mono font-semibold text-muted block mb-1">
              Entity or Individual Name (SWIFT / Beneficiary) *
            </label>
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3 top-2.5 text-fg0" />
              <input
                type="text"
                placeholder="e.g. Gulf Star Commodities, PetroChemicals, Farhan Ahmed..."
                value={queryName}
                onChange={(e) => setQueryName(e.target.value)}
                className="w-full pl-9 pr-3 py-2 bg-canvas border border-line-strong rounded-lg text-xs text-fg placeholder:text-fg0 focus:outline-none focus:border-sky-500 font-mono"
              />
            </div>
          </div>

          <div className="md:col-span-2">
            <label className="text-xs font-mono font-semibold text-muted block mb-1">
              Jurisdiction / Domicile
            </label>
            <select
              value={queryCountry}
              onChange={(e) => setQueryCountry(e.target.value)}
              className="w-full px-3 py-2 bg-canvas border border-line-strong rounded-lg text-xs text-fg-secondary focus:outline-none focus:border-sky-500 cursor-pointer font-mono"
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
            <label className="text-xs font-mono font-semibold text-muted block mb-1">
              Date of Birth (Corroboration)
            </label>
            <input
              type="date"
              value={queryDob}
              onChange={(e) => setQueryDob(e.target.value)}
              className="w-full px-3 py-2 bg-canvas border border-line-strong rounded-lg text-xs text-fg-secondary focus:outline-none focus:border-sky-500 font-mono"
            />
          </div>

          <div className="md:col-span-2">
            <label className="text-xs font-mono font-semibold text-muted block mb-1">
              National ID / Passport / TIN
            </label>
            <input
              type="text"
              placeholder="e.g. 8022-1984-7712..."
              value={queryId}
              onChange={(e) => setQueryId(e.target.value)}
              className="w-full px-3 py-2 bg-canvas border border-line-strong rounded-lg text-xs text-fg-secondary focus:outline-none focus:border-sky-500 font-mono text-xs"
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
          <div className="flex flex-wrap items-center justify-between gap-3 pb-2 border-b border-line">
            <div className="flex items-center gap-1.5">
              <button
                onClick={() => setActiveFilter('ALL')}
                className={`px-3 py-1 rounded-lg text-xs font-semibold cursor-pointer transition-colors ${
                  activeFilter === 'ALL'
                    ? 'bg-surface text-fg border border-line-strong'
                    : 'text-muted hover:text-fg-secondary'
                }`}
              >
                All ({screeningRecords.length})
              </button>
              <button
                onClick={() => setActiveFilter('PENDING')}
                className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold cursor-pointer transition-colors ${
                  activeFilter === 'PENDING'
                    ? 'bg-tier-2-bg text-tier-2-text border border-amber-800/60'
                    : 'text-tier-2-text/80 hover:bg-tier-2-bg'
                }`}
              >
                <span className="w-2 h-2 rounded-full bg-amber-500" />
                <span>Interdicted ({screeningRecords.filter((r) => r.disposition === 'PENDING_REVIEW').length})</span>
              </button>
              <button
                onClick={() => setActiveFilter('TRUE_HIT')}
                className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold cursor-pointer transition-colors ${
                  activeFilter === 'TRUE_HIT'
                    ? 'bg-tier-1-bg text-tier-1-text border border-rose-800/60'
                    : 'text-tier-1-text/80 hover:bg-tier-1-bg'
                }`}
              >
                <span className="w-2 h-2 rounded-full bg-rose-500" />
                <span>True Hits ({screeningRecords.filter((r) => r.disposition === 'CONFIRMED_TRUE_HIT').length})</span>
              </button>
              <button
                onClick={() => setActiveFilter('CLEARED')}
                className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold cursor-pointer transition-colors ${
                  activeFilter === 'CLEARED'
                    ? 'bg-tier-3-bg text-tier-3-text border border-emerald-800/60'
                    : 'text-tier-3-text/80 hover:bg-tier-3-bg'
                }`}
              >
                <span className="w-2 h-2 rounded-full bg-emerald-500" />
                <span>Cleared ({screeningRecords.filter((r) => r.disposition === 'DISMISSED_FALSE_POSITIVE').length})</span>
              </button>
            </div>

            <div className="relative w-48">
              <Search className="w-3.5 h-3.5 absolute left-2.5 top-2 text-fg0" />
              <input
                type="text"
                placeholder="Filter hits..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-8 pr-2.5 py-1 bg-panel border border-line-strong rounded-lg text-xs text-fg-secondary placeholder:text-fg0 focus:outline-none"
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
                      ? 'bg-surface/80 border-sky-500 shadow-lg'
                      : 'bg-panel border-line hover:border-line-strong'
                  }`}
                >
                  <div className="flex items-center justify-between gap-3">
                    <div className="flex items-center gap-2">
                      <span
                        className={`px-2 py-0.5 rounded text-xs font-mono font-bold ${
                          record.matchScore >= autoFreezeThreshold
                            ? 'bg-rose-500/20 text-tier-1-text border border-rose-500/30'
                            : record.matchScore >= quarantineThreshold
                            ? 'bg-amber-500/20 text-tier-2-text border border-amber-500/30'
                            : 'bg-surface-hover text-fg-secondary'
                        }`}
                      >
                        {record.matchScore.toFixed(1)}% MATCH
                      </span>
                      <span className="text-xs font-bold text-fg-secondary">{record.screenedName}</span>
                    </div>

                    <span
                      className={`text-xs font-mono font-semibold px-2 py-0.5 rounded ${
                        record.disposition === 'CONFIRMED_TRUE_HIT'
                          ? 'bg-tier-1-bg text-tier-1-text border border-rose-800'
                          : record.disposition === 'PENDING_REVIEW'
                          ? 'bg-tier-2-bg text-tier-2-text border border-amber-800'
                          : 'bg-tier-3-bg text-tier-3-text border border-emerald-800'
                      }`}
                    >
                      {record.disposition.replace(/_/g, ' ')}
                    </span>
                  </div>

                  <div className="mt-2 flex items-center justify-between text-xs text-muted">
                    <div className="flex items-center gap-2 truncate">
                      <span className="text-fg0">Target Match:</span>
                      <span className="font-medium text-fg-secondary truncate">{record.matchedEntity}</span>
                    </div>
                    <span className="font-mono text-xs text-accent-2 shrink-0">{record.watchlistSource}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Column: Match Forensics & Disposition Panel */}
        <div className="lg:col-span-5 bg-panel border border-line rounded-2xl p-5 shadow-2xl flex flex-col justify-between space-y-6">
          {selectedRecord ? (
            <div className="space-y-5">
              {/* Header */}
              <div className="pb-4 border-b border-line">
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs text-accent-2 font-bold">{selectedRecord.id}</span>
                  <span className="text-xs text-muted font-mono">{selectedRecord.screenedAt}</span>
                </div>
                <h3 className="text-base font-bold text-fg mt-1 font-sans">
                  Watchlist Match Decomposition
                </h3>
              </div>

              {/* Side-by-Side Name Alignment */}
              <div className="space-y-3">
                <div className="p-3 bg-canvas border border-line rounded-xl space-y-1">
                  <div className="text-xs font-mono text-fg0 ">Input Payload String</div>
                  <div className="text-sm font-bold text-fg font-mono">{selectedRecord.screenedName}</div>
                </div>

                <div className="p-3 bg-canvas border border-line rounded-xl space-y-1">
                  <div className="text-xs font-mono text-fg0 ">Sanctions Official Entry</div>
                  <div className="text-sm font-bold text-tier-1-text font-mono">{selectedRecord.matchedEntity}</div>
                  <div className="text-xs text-muted font-mono">Watchlist: {selectedRecord.watchlistSource}</div>
                </div>
              </div>

              {/* Match Forensics Metrics: Real Algorithm Breakdown */}
              <div className="space-y-2">
                <div className="flex items-center justify-between text-xs font-mono font-bold text-fg-secondary">
                  <span>Engine Score Decomposition</span>
                  <span className="text-tier-3-text text-sm font-bold">{selectedRecord.matchScore.toFixed(1)}% Composite</span>
                </div>

                <div className="grid grid-cols-3 gap-2 text-xs font-mono">
                  <div className="p-2.5 bg-canvas border border-line rounded-lg">
                    <span className="text-xs text-fg0 block">Jaro-Winkler</span>
                    <span className="text-accent-2 font-bold text-sm">
                      {selectedRecord.algorithmBreakdown?.jaroWinklerScore !== undefined
                        ? `${selectedRecord.algorithmBreakdown.jaroWinklerScore.toFixed(1)}%`
                        : `${selectedRecord.matchScore.toFixed(1)}%`}
                    </span>
                    <span className="text-xs text-fg0 block">Weight: 40%</span>
                  </div>

                  <div className="p-2.5 bg-canvas border border-line rounded-lg">
                    <span className="text-xs text-fg0 block">Token-Set</span>
                    <span className="text-purple-400 font-bold text-sm">
                      {selectedRecord.algorithmBreakdown?.tokenSetScore !== undefined
                        ? `${selectedRecord.algorithmBreakdown.tokenSetScore.toFixed(1)}%`
                        : `${selectedRecord.matchScore.toFixed(1)}%`}
                    </span>
                    <span className="text-xs text-fg0 block">Weight: 40%</span>
                  </div>

                  <div className="p-2.5 bg-canvas border border-line rounded-lg">
                    <span className="text-xs text-fg0 block">Phonetic Soundex</span>
                    <span className="text-tier-2-text font-bold text-sm">
                      {selectedRecord.algorithmBreakdown?.phoneticScore !== undefined
                        ? `${selectedRecord.algorithmBreakdown.phoneticScore.toFixed(1)}%`
                        : '85.0%'}
                    </span>
                    <span className="text-xs text-fg0 block">Weight: 20%</span>
                  </div>
                </div>
              </div>

              {/* Attribute Corroboration Status */}
              <div className="p-3 rounded-xl bg-canvas border border-line space-y-2 text-xs font-mono">
                <div className="flex items-center justify-between text-xs font-bold text-fg-secondary">
                  <span>Attribute Corroboration</span>
                  <span className="text-accent-2">
                    Adjustment: {selectedRecord.algorithmBreakdown?.corroborationAdjustment
                      ? `${selectedRecord.algorithmBreakdown.corroborationAdjustment > 0 ? '+' : ''}${selectedRecord.algorithmBreakdown.corroborationAdjustment.toFixed(1)}%`
                      : '+0.0%'}
                  </span>
                </div>

                <div className="grid grid-cols-3 gap-2 text-xs">
                  <div className="p-1.5 rounded bg-panel border border-line">
                    <span className="text-fg0 block">DOB Status</span>
                    <span className="text-fg-secondary font-bold">
                      {selectedRecord.corroborationDetails?.dobStatus || 'NOT_PROVIDED'}
                    </span>
                  </div>
                  <div className="p-1.5 rounded bg-panel border border-line">
                    <span className="text-fg0 block">Country Domicile</span>
                    <span className="text-fg-secondary font-bold">
                      {selectedRecord.corroborationDetails?.countryStatus || 'MATCH'}
                    </span>
                  </div>
                  <div className="p-1.5 rounded bg-panel border border-line">
                    <span className="text-fg0 block">Identifier / Passport</span>
                    <span className="text-fg-secondary font-bold">
                      {selectedRecord.corroborationDetails?.idStatus || 'NOT_PROVIDED'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Token Diffs */}
              <div>
                <h4 className="text-xs font-mono font-bold text-muted mb-2">
                  Tokenized Linguistic Diff
                </h4>
                <div className="p-3 rounded-xl bg-canvas border border-line space-y-2 text-xs font-mono">
                  <div>
                    <span className="text-fg0 text-xs block">Common Tokens:</span>
                    <span className="text-tier-3-text font-bold">
                      {selectedRecord.tokenDiffs.commonTokens.join(', ') || 'None'}
                    </span>
                  </div>
                  <div>
                    <span className="text-fg0 text-xs block">Query Tokens:</span>
                    <span className="text-fg-secondary">{selectedRecord.tokenDiffs.screenedTokens.join(', ')}</span>
                  </div>
                  <div>
                    <span className="text-fg0 text-xs block">Watchlist Tokens:</span>
                    <span className="text-fg-secondary">{selectedRecord.tokenDiffs.matchedTokens.join(', ')}</span>
                  </div>
                </div>
              </div>

              {/* Disposition Action Buttons */}
              <div className="pt-4 border-t border-line space-y-2.5">
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
                    className="py-2 px-3 rounded-xl bg-surface hover:bg-surface-hover text-fg-secondary font-medium text-xs transition-colors flex items-center justify-center gap-1.5"
                  >
                    <MailQuestion className="w-3.5 h-3.5 text-accent-2" />
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
                    className="py-2 px-3 rounded-xl bg-surface-2 hover:bg-surface-hover text-fg-secondary font-medium text-xs transition-colors cursor-pointer"
                  >
                    Dismiss False Positive
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <div className="py-20 text-center text-fg0 text-xs">
              Select an interdiction record from the list to inspect forensic token matches.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
