'use client';

import React, { useState, useMemo, useRef } from 'react';
import Link from 'next/link';
import { useVirtualizer } from '@tanstack/react-virtual';
import {
  ShieldAlert,
  Clock,
  CheckCircle2,
  Filter,
  Search,
  Layers,
  ChevronDown,
  Download,
  AlertTriangle,
  FileText,
  GitFork,
  Lock,
  ArrowUpDown,
  MailQuestion,
  CheckSquare,
  Square
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { SEEDED_ALERTS } from '@/lib/seedData';
import { PiiText } from '@/components/ui/PiiText';

export default function AlertTriagePage() {
  const { density, setDensity, setFourEyesModalOpen } = useBankingStore();
  const [selectedTier, setSelectedTier] = useState<'ALL' | 1 | 2 | 3>('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedRowIds, setSelectedRowIds] = useState<Set<string>>(new Set());

  // Filter alerts based on active tab and search query
  const filteredAlerts = useMemo(() => {
    return SEEDED_ALERTS.filter((alert) => {
      const matchesTier = selectedTier === 'ALL' || alert.tierCode === selectedTier;
      const matchesSearch =
        searchQuery === '' ||
        alert.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
        alert.entityName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        alert.account.toLowerCase().includes(searchQuery.toLowerCase()) ||
        alert.rail.toLowerCase().includes(searchQuery.toLowerCase());
      return matchesTier && matchesSearch;
    });
  }, [selectedTier, searchQuery]);

  // Virtualization setup
  const parentRef = useRef<HTMLDivElement>(null);
  const rowHeight = density === 'compact' ? 36 : 48;

  const rowVirtualizer = useVirtualizer({
    count: filteredAlerts.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => rowHeight,
    overscan: 10,
  });

  const toggleSelectAll = () => {
    if (selectedRowIds.size === filteredAlerts.length) {
      setSelectedRowIds(new Set());
    } else {
      setSelectedRowIds(new Set(filteredAlerts.map((a) => a.id)));
    }
  };

  const toggleSelectRow = (id: string) => {
    setSelectedRowIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const selectedAlerts = filteredAlerts.filter((a) => selectedRowIds.has(a.id));
  const totalSelectedExposure = selectedAlerts.reduce((sum, a) => sum + a.amount, 0);

  return (
    <div className="p-6 max-w-[1700px] mx-auto space-y-5">
      {/* Header and Controls */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-rose-500" />
            Alert Triage Queue — Conformal Risk Gating (CRC α=0.01)
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Institutional high-throughput alert management with class-conditional finite sample coverage guarantees (≥ 99.0%).
          </p>
        </div>

        <div className="flex items-center gap-3">
          {/* Density Toggle */}
          <div className="flex items-center bg-[#0F172A] p-1 rounded-lg border border-[#334155]">
            <button
              onClick={() => setDensity('compact')}
              className={`px-2.5 py-1 rounded text-xs font-medium transition-all ${
                density === 'compact'
                  ? 'bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/40'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Compact (32px)
            </button>
            <button
              onClick={() => setDensity('comfortable')}
              className={`px-2.5 py-1 rounded text-xs font-medium transition-all ${
                density === 'comfortable'
                  ? 'bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/40'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Comfortable (44px)
            </button>
          </div>

          {/* Export CSV Button */}
          <button
            onClick={() => alert('Exporting signed regulatory CSV...')}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#0F172A] hover:bg-[#1E293B] border border-[#334155] text-xs font-medium text-slate-200 transition-colors"
          >
            <Download className="w-3.5 h-3.5 text-slate-400" />
            <span>Export CSV</span>
          </button>
        </div>
      </div>

      {/* Tabs and Search Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-2 border-b border-[#1E293B]">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setSelectedTier('ALL')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              selectedTier === 'ALL'
                ? 'bg-[#1E293B] text-slate-100 border border-[#334155]'
                : 'text-slate-400 hover:text-slate-200 hover:bg-[#0F172A]'
            }`}
          >
            All Alerts ({SEEDED_ALERTS.length})
          </button>
          <button
            onClick={() => setSelectedTier(1)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              selectedTier === 1
                ? 'bg-rose-950/60 text-rose-300 border border-rose-800/60'
                : 'text-rose-400/80 hover:bg-rose-950/20'
            }`}
          >
            <span className="w-2 h-2 rounded-full bg-rose-500" />
            <span>Tier 1 Hold ({SEEDED_ALERTS.filter((a) => a.tierCode === 1).length})</span>
          </button>
          <button
            onClick={() => setSelectedTier(2)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              selectedTier === 2
                ? 'bg-amber-950/60 text-amber-300 border border-amber-800/60'
                : 'text-amber-400/80 hover:bg-amber-950/20'
            }`}
          >
            <span className="w-2 h-2 rounded-full bg-amber-500" />
            <span>Tier 2 Review ({SEEDED_ALERTS.filter((a) => a.tierCode === 2).length})</span>
          </button>
          <button
            onClick={() => setSelectedTier(3)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              selectedTier === 3
                ? 'bg-emerald-950/60 text-emerald-300 border border-emerald-800/60'
                : 'text-emerald-400/80 hover:bg-emerald-950/20'
            }`}
          >
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
            <span>Tier 3 Clear ({SEEDED_ALERTS.filter((a) => a.tierCode === 3).length})</span>
          </button>
        </div>

        {/* Search */}
        <div className="relative min-w-[280px]">
          <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-500" />
          <input
            type="text"
            placeholder="Search by ID, Entity, Account, Rail..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 bg-[#0F172A] border border-[#334155] rounded-lg text-xs text-slate-100 placeholder:text-slate-500 focus:outline-none focus:border-emerald-500"
          />
        </div>
      </div>

      {/* TanStack Virtualized High-Density Table */}
      <div className="bg-[#0F172A] border border-[#1E293B] rounded-xl overflow-hidden shadow-2xl">
        {/* Table Header */}
        <div className="grid grid-cols-12 gap-2 px-4 py-2.5 bg-[#0B0F17] border-b border-[#1E293B] text-[11px] font-semibold text-slate-400 uppercase tracking-wider items-center select-none">
          <div className="col-span-1 flex items-center gap-2">
            <button onClick={toggleSelectAll} className="text-slate-400 hover:text-slate-200">
              {selectedRowIds.size === filteredAlerts.length && filteredAlerts.length > 0 ? (
                <CheckSquare className="w-4 h-4 text-emerald-400" />
              ) : (
                <Square className="w-4 h-4" />
              )}
            </button>
            <span>Alert ID</span>
          </div>
          <div className="col-span-3">Entity & Masked Account</div>
          <div className="col-span-2 text-right">Amount (USD / BDT)</div>
          <div className="col-span-1">Rail</div>
          <div className="col-span-1 text-center">CRC Tier</div>
          <div className="col-span-1 text-center">Conformal Set</div>
          <div className="col-span-1 text-center">Risk Score</div>
          <div className="col-span-1 text-center">SLA</div>
          <div className="col-span-1 text-right">Actions</div>
        </div>

        {/* Virtualized Body */}
        <div
          ref={parentRef}
          className="overflow-y-auto max-h-[620px] divide-y divide-[#1E293B]/60"
        >
          <div
            style={{
              height: `${rowVirtualizer.getTotalSize()}px`,
              width: '100%',
              position: 'relative',
            }}
          >
            {rowVirtualizer.getVirtualItems().map((virtualRow) => {
              const alert = filteredAlerts[virtualRow.index];
              if (!alert) return null;
              const isSelected = selectedRowIds.has(alert.id);

              return (
                <div
                  key={alert.id}
                  style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: `${virtualRow.size}px`,
                    transform: `translateY(${virtualRow.start}px)`,
                  }}
                  className={`grid grid-cols-12 gap-2 px-4 items-center text-xs transition-colors ${
                    isSelected ? 'bg-emerald-950/20' : 'hover:bg-[#1E293B]/40'
                  }`}
                >
                  {/* Select + Alert ID */}
                  <div className="col-span-1 flex items-center gap-2">
                    <button
                      onClick={() => toggleSelectRow(alert.id)}
                      className="text-slate-400 hover:text-slate-200"
                    >
                      {isSelected ? (
                        <CheckSquare className="w-3.5 h-3.5 text-emerald-400" />
                      ) : (
                        <Square className="w-3.5 h-3.5" />
                      )}
                    </button>
                    <span className="font-mono font-bold text-slate-200 text-[11px] truncate">
                      {alert.id}
                    </span>
                  </div>

                  {/* Entity & Account */}
                  <div className="col-span-3 truncate">
                    <div className="font-medium text-slate-100 truncate">{alert.entityName}</div>
                    <div className="text-[10px] text-slate-400 font-mono flex items-center gap-1.5">
                      <PiiText value={alert.account} type="account" className="text-slate-400" />
                      <span>•</span>
                      <span>BIC: {alert.bic}</span>
                    </div>
                  </div>

                  {/* Amount */}
                  <div className="col-span-2 text-right">
                    <div className="font-mono font-bold text-slate-100">
                      ${alert.amount.toLocaleString(undefined, { minimumFractionDigits: 2 })}
                    </div>
                    <div className="text-[10px] font-mono text-slate-500">
                      ৳{alert.amountBdt.toLocaleString()}
                    </div>
                  </div>

                  {/* Rail */}
                  <div className="col-span-1 text-[11px] font-mono text-slate-300 truncate">
                    {alert.rail}
                  </div>

                  {/* CRC Tier Badge */}
                  <div className="col-span-1 text-center">
                    <span
                      className={`inline-block px-1.5 py-0.5 rounded text-[10px] font-mono font-bold ${
                        alert.tierCode === 1
                          ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                          : alert.tierCode === 2
                          ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                          : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                      }`}
                    >
                      Tier {alert.tierCode}
                    </span>
                  </div>

                  {/* Conformal Set */}
                  <div className="col-span-1 text-center font-mono text-[11px] text-slate-300">
                    {alert.decisionSet}
                  </div>

                  {/* Risk Score */}
                  <div className="col-span-1 text-center font-mono font-bold text-[11px] text-slate-200">
                    {alert.riskScore}
                  </div>

                  {/* SLA */}
                  <div className="col-span-1 text-center font-mono text-[10px] text-slate-400">
                    {alert.slaMinutesLeft}m
                  </div>

                  {/* Actions */}
                  <div className="col-span-1 flex items-center justify-end gap-1.5">
                    <Link
                      href={`/graph?node=${encodeURIComponent(alert.account)}`}
                      title="Inspect Ego-Graph"
                      className="p-1 rounded bg-[#1E293B] hover:bg-[#334155] text-slate-300 transition-colors"
                    >
                      <GitFork className="w-3.5 h-3.5" />
                    </Link>
                    <Link
                      href={`/cases/${alert.caseId}`}
                      title="Open Case File"
                      className="p-1 rounded bg-[#1E293B] hover:bg-[#334155] text-slate-300 transition-colors"
                    >
                      <FileText className="w-3.5 h-3.5" />
                    </Link>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Sticky Floating Bulk Action Drawer */}
      {selectedRowIds.size > 0 && (
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-40 bg-[#0F172A] border border-[#334155] shadow-2xl rounded-2xl px-6 py-3 flex items-center gap-6 text-xs text-slate-200 animate-in slide-in-from-bottom duration-200">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="font-semibold text-slate-100">
              {selectedRowIds.size} Alerts Selected
            </span>
            <span className="text-slate-400">
              (Total Exposure: <strong className="font-mono text-emerald-400">${totalSelectedExposure.toLocaleString()}</strong>)
            </span>
          </div>

          <div className="h-4 w-px bg-[#334155]" />

          <div className="flex items-center gap-2">
            <button
              onClick={() => {
                setFourEyesModalOpen(true, {
                  actionType: 'SAR_FILING',
                  actionTitle: `Batch 4-Eyes Escalation (${selectedRowIds.size} items)`,
                  targetId: Array.from(selectedRowIds).join(', '),
                  details: `Execute batch escalation and SAR filing for selected alerts. Total exposure: $${totalSelectedExposure.toLocaleString()}`
                });
              }}
              className="px-3 py-1.5 rounded-lg bg-rose-950/60 hover:bg-rose-900/80 text-rose-300 border border-rose-800/60 font-semibold transition-colors flex items-center gap-1.5"
            >
              <AlertTriangle className="w-3.5 h-3.5" />
              <span>Batch 4-Eyes Escalate</span>
            </button>

            <Link
              href="/rfi"
              className="px-3 py-1.5 rounded-lg bg-[#1E293B] hover:bg-[#334155] text-slate-200 font-medium transition-colors flex items-center gap-1.5"
            >
              <MailQuestion className="w-3.5 h-3.5 text-indigo-400" />
              <span>Initiate Batch RFI</span>
            </Link>

            <button
              onClick={() => setSelectedRowIds(new Set())}
              className="px-2.5 py-1.5 text-slate-400 hover:text-slate-200"
            >
              Clear
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
