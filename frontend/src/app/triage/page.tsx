'use client';

import React, { useState, useMemo, useRef, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
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
  Square,
  SlidersHorizontal,
  ShieldX,
  UserCheck,
  X,
  Send,
  Eye,
  FileSpreadsheet,
  AlertOctagon,
  RefreshCw,
  ExternalLink,
  ChevronRight,
  User,
  Sliders,
  Sparkles,
  HelpCircle,
  Activity
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { PiiText } from '@/components/ui/PiiText';
import { CommercialAlert } from '@/lib/data/commercialSeed';

export default function AlertTriagePage() {
  const router = useRouter();
  const {
    alerts,
    jurisdiction,
    displayCurrency,
    densityMode,
    setDensityMode,
    setFourEyesModalOpen,
    assignAlert,
    batchAssignAlerts,
    dismissAlert,
    overrideAlertScore,
    escalateToCase,
    freezeAccount,
    addAuditEntry
  } = useBankingStore();

  const [selectedTier, setSelectedTier] = useState<'ALL' | 1 | 2 | 3>('ALL');
  const [selectedStatus, setSelectedStatus] = useState<'ALL' | 'PENDING_TRIAGE' | 'UNDER_INVESTIGATION' | 'SAR_DRAFTED' | 'QUARANTINED' | 'FALSE_POSITIVE_DISMISSED' | 'OVERRIDDEN'>('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedRowIds, setSelectedRowIds] = useState<Set<string>>(new Set());
  const [focusedIndex, setFocusedIndex] = useState<number>(0);
  const [inspectingAlert, setInspectingAlert] = useState<CommercialAlert | null>(null);
  const [assigneeTarget, setAssigneeTarget] = useState<string>('Amina Rahman, CFE (Lead Investigator)');
  const [dismissReasonModalOpen, setDismissReasonModalOpen] = useState(false);
  const [dismissReason, setDismissReason] = useState('');
  const [showExplainability, setShowExplainability] = useState(false);
  const [overrideModalOpen, setOverrideModalOpen] = useState(false);
  const [overrideScore, setOverrideScore] = useState(0.12);
  const [overrideTier, setOverrideTier] = useState<'Tier 1 Hold' | 'Tier 2 Review' | 'Tier 3 Clear'>('Tier 3 Clear');
  const [overrideJustification, setOverrideJustification] = useState('DOCUMENTED_TRADE_INVOICE');
  const [overrideNotes, setOverrideNotes] = useState('Verified genuine commercial LC with ASYCUDA customs stamp.');
  const [isSubmittingOverride, setIsSubmittingOverride] = useState(false);

  // Filter alerts based on active tab, status, and search query
  const filteredAlerts = useMemo(() => {
    return alerts.filter((alert) => {
      const matchesTier = selectedTier === 'ALL' || alert.tierCode === selectedTier;
      const matchesStatus = selectedStatus === 'ALL' || alert.status === selectedStatus;
      const matchesSearch =
        searchQuery === '' ||
        alert.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
        alert.entityName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        alert.account.toLowerCase().includes(searchQuery.toLowerCase()) ||
        alert.rail.toLowerCase().includes(searchQuery.toLowerCase()) ||
        alert.typology.toLowerCase().includes(searchQuery.toLowerCase()) ||
        alert.assignee.toLowerCase().includes(searchQuery.toLowerCase());
      return matchesTier && matchesStatus && matchesSearch;
    });
  }, [alerts, selectedTier, selectedStatus, searchQuery]);

  // Virtualization setup
  const parentRef = useRef<HTMLDivElement>(null);
  const rowHeight = densityMode === 'compact' ? 54 : 68;

  useEffect(() => {
    if (!inspectingAlert) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setInspectingAlert(null);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [inspectingAlert]);

  const rowVirtualizer = useVirtualizer({
    count: filteredAlerts.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => rowHeight,
    overscan: 15,
  });

  useEffect(() => {
    rowVirtualizer.measure();
  }, [densityMode, rowVirtualizer]);

  // Keyboard navigation: J/K, Enter, G, F, E, R
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Don't intercept if typing in an input
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes((e.target as HTMLElement).tagName)) {
        return;
      }

      if (e.key === 'j' || e.key === 'ArrowDown') {
        e.preventDefault();
        setFocusedIndex((prev) => Math.min(prev + 1, filteredAlerts.length - 1));
      } else if (e.key === 'k' || e.key === 'ArrowUp') {
        e.preventDefault();
        setFocusedIndex((prev) => Math.max(prev - 1, 0));
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (filteredAlerts[focusedIndex]) {
          setInspectingAlert(filteredAlerts[focusedIndex]);
        }
      } else if (e.key.toLowerCase() === 'g') {
        e.preventDefault();
        if (filteredAlerts[focusedIndex]) {
          router.push(`/graph?node=${encodeURIComponent(filteredAlerts[focusedIndex].account)}`);
        }
      } else if (e.key.toLowerCase() === 'f') {
        e.preventDefault();
        const current = filteredAlerts[focusedIndex];
        if (current) {
          setFourEyesModalOpen(true, {
            actionType: 'ACCOUNT_FREEZE',
            actionTitle: `Emergency Administrative Account Freeze (${current.entityName})`,
            targetId: current.account,
            details: `Execute regulatory freeze on account ${current.account} across SWIFT/RTGS clearing rails pursuant to statutory freeze powers.`
          });
        }
      } else if (e.key.toLowerCase() === 'e') {
        e.preventDefault();
        const current = filteredAlerts[focusedIndex];
        if (current) {
          escalateToCase(current.id);
        }
      } else if (e.key.toLowerCase() === 'x') {
        e.preventDefault();
        const current = filteredAlerts[focusedIndex];
        if (current) {
          toggleSelectRow(current.id);
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [filteredAlerts, focusedIndex, router, setFourEyesModalOpen, escalateToCase]);

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

  // Bulk actions
  const handleBatchAssign = () => {
    if (selectedRowIds.size === 0) return;
    batchAssignAlerts(Array.from(selectedRowIds), assigneeTarget);
    setSelectedRowIds(new Set());
  };

  const handleBatchEscalate = () => {
    if (selectedRowIds.size === 0) return;
    selectedRowIds.forEach((id) => escalateToCase(id));
    setSelectedRowIds(new Set());
  };

  const handleBatchDismiss = () => {
    if (selectedRowIds.size === 0) return;
    setDismissReasonModalOpen(true);
  };

  const confirmBatchDismiss = () => {
    selectedRowIds.forEach((id) => {
      dismissAlert(id, dismissReason || 'Classified as legitimate commercial activity after analyst triage.');
    });
    setDismissReasonModalOpen(false);
    setDismissReason('');
    setSelectedRowIds(new Set());
  };

  const handleConfirmOverride = async () => {
    if (!inspectingAlert) return;
    setIsSubmittingOverride(true);
    await overrideAlertScore(
      inspectingAlert.id,
      overrideScore,
      overrideTier,
      overrideJustification,
      overrideNotes
    );
    setIsSubmittingOverride(false);
    setOverrideModalOpen(false);
    setInspectingAlert(null);
  };

  const exportCsv = () => {
    const dataToExport = selectedAlerts.length > 0 ? selectedAlerts : filteredAlerts;
    const headers = ['Alert ID', 'Entity Name', 'Account', 'BIC', 'Amount USD', 'Amount BDT', 'Rail', 'Tier', 'Status', 'Typology', 'Assigned To'];
    const rows = dataToExport.map((a) => [
      a.id,
      `"${a.entityName.replace(/"/g, '""')}"`,
      `"${a.account}"`,
      a.bic,
      a.amount,
      a.amountBdt,
      a.rail,
      a.tierCode,
      a.status,
      `"${a.typology}"`,
      `"${a.assignee}"`
    ]);

    const csvContent = [headers.join(','), ...rows.map((r) => r.join(','))].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `AML_Alert_Queue_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const exportJson = () => {
    const dataToExport = selectedAlerts.length > 0 ? selectedAlerts : filteredAlerts;
    const blob = new Blob([JSON.stringify(dataToExport, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `AML_Alert_Queue_${new Date().toISOString().slice(0, 10)}.json`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="p-4 sm:p-5 lg:p-6 max-w-[1750px] mx-auto space-y-4">
      {/* Header and Controls */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2 font-sans">
            <ShieldAlert className="w-5 h-5 text-rose-500" />
            High-Throughput Alert Triage Queue
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Real-time calibrated risk prioritization for multi-rail clearing (SWIFT MT, ISO 20022 pacs, BEFTN, MFS). {alerts.length.toLocaleString()} total live alerts loaded.
          </p>
        </div>

        <div className="flex items-center gap-3">
          {/* Quick Shortcuts Pill */}
          <div className="hidden xl:flex items-center gap-2 px-3 py-1 bg-[#0F172A] border border-[#334155] rounded-lg text-xs text-slate-400 font-mono">
            <span><kbd className="px-1.5 py-0.5 rounded bg-[#1E293B] text-slate-200">J</kbd>/<kbd className="px-1.5 py-0.5 rounded bg-[#1E293B] text-slate-200">K</kbd> Navigate</span>
            <span>•</span>
            <span><kbd className="px-1.5 py-0.5 rounded bg-[#1E293B] text-slate-200">Enter</kbd> Inspect Wire</span>
            <span>•</span>
            <span><kbd className="px-1.5 py-0.5 rounded bg-[#1E293B] text-slate-200">G</kbd> Graph</span>
            <span>•</span>
            <span><kbd className="px-1.5 py-0.5 rounded bg-[#1E293B] text-slate-200">F</kbd> Freeze</span>
            <span>•</span>
            <span><kbd className="px-1.5 py-0.5 rounded bg-[#1E293B] text-slate-200">E</kbd> Escalate</span>
          </div>

          {/* Export Actions */}
          <div className="flex items-center gap-1.5 bg-[#0F172A] p-1 rounded-lg border border-[#334155]">
            <button
              onClick={exportCsv}
              title="Export CSV"
              className="px-2.5 py-1 rounded text-xs font-medium text-slate-300 hover:text-white hover:bg-[#1E293B] flex items-center gap-1.5 cursor-pointer"
            >
              <FileSpreadsheet className="w-3.5 h-3.5 text-emerald-400" />
              <span>CSV</span>
            </button>
            <button
              onClick={exportJson}
              title="Export JSON"
              className="px-2.5 py-1 rounded text-xs font-medium text-slate-300 hover:text-white hover:bg-[#1E293B] flex items-center gap-1.5 cursor-pointer"
            >
              <Download className="w-3.5 h-3.5 text-sky-400" />
              <span>JSON</span>
            </button>
          </div>

          {/* Density Mode Sync */}
          <div className="flex items-center bg-[#0F172A] p-1 rounded-lg border border-[#334155] text-xs font-mono">
            <button
              onClick={() => setDensityMode('compact')}
              className={`px-2.5 py-1 rounded transition-all cursor-pointer ${densityMode === 'compact'
                ? 'bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/40'
                : 'text-slate-400 hover:text-slate-200'
                }`}
            >
              Compact
            </button>
            <button
              onClick={() => setDensityMode('comfortable')}
              className={`px-2.5 py-1 rounded transition-all cursor-pointer ${densityMode === 'comfortable'
                ? 'bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/40'
                : 'text-slate-400 hover:text-slate-200'
                }`}
            >
              Comfortable
            </button>
          </div>
        </div>
      </div>

      {/* Filter Tabs and Search Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-1 border-b border-[#1E293B]">
        {/* Tier Filter Tabs */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setSelectedTier('ALL')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${selectedTier === 'ALL'
              ? 'bg-[#1E293B] text-slate-100 border border-[#334155]'
              : 'text-slate-400 hover:text-slate-200'
              }`}
          >
            All Alerts ({alerts.length})
          </button>
          <button
            onClick={() => setSelectedTier(1)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${selectedTier === 1
              ? 'bg-rose-950/60 text-rose-300 border border-rose-800/60'
              : 'text-rose-400/80 hover:bg-rose-950/20'
              }`}
          >
            <span className="w-2 h-2 rounded-full bg-rose-500" />
            <span>Tier 1 Hold ({alerts.filter((a) => a.tierCode === 1).length})</span>
          </button>
          <button
            onClick={() => setSelectedTier(2)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${selectedTier === 2
              ? 'bg-amber-950/60 text-amber-300 border border-amber-800/60'
              : 'text-amber-400/80 hover:bg-amber-950/20'
              }`}
          >
            <span className="w-2 h-2 rounded-full bg-amber-500" />
            <span>Tier 2 Review ({alerts.filter((a) => a.tierCode === 2).length})</span>
          </button>
          <button
            onClick={() => setSelectedTier(3)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${selectedTier === 3
              ? 'bg-emerald-950/60 text-emerald-300 border border-emerald-800/60'
              : 'text-emerald-400/80 hover:bg-emerald-950/20'
              }`}
          >
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
            <span>Tier 3 Clear ({alerts.filter((a) => a.tierCode === 3).length})</span>
          </button>
        </div>

        {/* Status Dropdown & Search */}
        <div className="flex items-center gap-3">
          <select
            value={selectedStatus}
            onChange={(e) => setSelectedStatus(e.target.value as any)}
            className="px-3 py-1.5 bg-[#0F172A] border border-[#334155] rounded-lg text-xs text-slate-300 focus:outline-none focus:border-emerald-500 cursor-pointer"
          >
            <option value="ALL">All Statuses</option>
            <option value="PENDING_TRIAGE">Pending Triage</option>
            <option value="UNDER_INVESTIGATION">Under Investigation</option>
            <option value="SAR_DRAFTED">SAR Drafted</option>
            <option value="QUARANTINED">Quarantined (Hold)</option>
            <option value="FALSE_POSITIVE_DISMISSED">Dismissed (FP)</option>
          </select>

          <div className="relative min-w-[300px]">
            <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-500" />
            <input
              type="text"
              placeholder="Search by ID, Entity, Account, BIC, Typology..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 bg-[#0F172A] border border-[#334155] rounded-lg text-xs text-slate-100 placeholder:text-slate-500 focus:outline-none focus:border-emerald-500"
            />
          </div>
        </div>
      </div>

      {/* TanStack Virtualized High-Density Table */}
      <div className="bg-[#0F172A] border border-[#1E293B] rounded-xl overflow-hidden shadow-2xl">
        <div className="overflow-x-auto">
          <div className="min-w-[1100px]" role="table" aria-label="Alert triage queue" aria-rowcount={filteredAlerts.length}>
            {/* Table Header */}
            <div role="row" className="grid grid-cols-[118px_minmax(200px,1fr)_120px_112px_104px_64px_64px_minmax(96px,0.5fr)_84px] gap-2 px-4 py-2.5 bg-[#0B0F17] border-b border-[#1E293B] text-xs font-medium text-slate-400 items-center select-none">
              <div className="flex items-center gap-2">
                <button onClick={toggleSelectAll} className="text-slate-400 hover:text-slate-200 cursor-pointer">
                  {selectedRowIds.size === filteredAlerts.length && filteredAlerts.length > 0 ? (
                    <CheckSquare className="w-4 h-4 text-emerald-400" />
                  ) : (
                    <Square className="w-4 h-4" />
                  )}
                </button>
                <span>Alert ID</span>
              </div>
              <div className="">Entity</div>
              <div className="text-right">Amount</div>
              <div className="">Rail</div>
              <div className="text-center">Tier</div>
              <div className="text-center">Score</div>
              <div className="text-center">SLA</div>
              <div className="">Assignee</div>
              <div className="text-right">Actions</div>
            </div>

            {/* Virtualized Body */}
            <div
              ref={parentRef}
              className="overflow-y-auto max-h-[640px] divide-y divide-[#1E293B]/60"
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
                  const isFocused = virtualRow.index === focusedIndex;

                  return (
                    <div
                      key={alert.id}
                      role="row"
                      aria-rowindex={virtualRow.index + 2}
                      aria-selected={isFocused}
                      onClick={() => setFocusedIndex(virtualRow.index)}
                      onDoubleClick={() => setInspectingAlert(alert)}
                      style={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        width: '100%',
                        height: `${virtualRow.size}px`,
                        transform: `translateY(${virtualRow.start}px)`,
                      }}
                      className={`grid grid-cols-[118px_minmax(200px,1fr)_120px_112px_104px_64px_64px_minmax(96px,0.5fr)_84px] gap-2 px-4 items-center overflow-hidden text-xs transition-colors group cursor-pointer ${isSelected
                        ? 'bg-emerald-950/20'
                        : isFocused
                          ? 'bg-[#1E293B]/60 ring-1 ring-inset ring-sky-500/40'
                          : 'hover:bg-[#1E293B]/40'
                        }`}
                    >
                      {/* Select + Alert ID */}
                      <div className="flex items-center gap-2">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            toggleSelectRow(alert.id);
                          }}
                          className="text-slate-400 hover:text-slate-200 cursor-pointer"
                        >
                          {isSelected ? (
                            <CheckSquare className="w-3.5 h-3.5 text-emerald-400" />
                          ) : (
                            <Square className="w-3.5 h-3.5" />
                          )}
                        </button>
                        <span className="font-semibold text-slate-200 text-xs tabular-nums whitespace-nowrap">
                          {alert.id}
                        </span>
                      </div>

                      {/* Entity & Account */}
                      <div className="truncate">
                        <div className="font-medium text-slate-100 truncate flex items-center gap-1.5">
                          <span className="truncate min-w-0">{alert.entityName}</span>
                          {alert.status === 'UNDER_INVESTIGATION' && (
                            <span className="shrink-0 px-1.5 py-0.2 rounded text-xs bg-purple-500/20 text-purple-300 border border-purple-500/30 font-mono">
                              Case
                            </span>
                          )}
                          {alert.status === 'FALSE_POSITIVE_DISMISSED' && (
                            <span className="shrink-0 px-1.5 py-0.2 rounded text-xs bg-slate-700 text-slate-300 font-mono">
                              Dismissed
                            </span>
                          )}
                        </div>
                        <div className="text-xs text-slate-400 font-mono flex items-center gap-1.5 truncate">
                          <PiiText value={alert.account} type="account" className="text-slate-400" />
                          <span>•</span>
                          <span className="text-slate-500 truncate">{alert.typology}</span>
                        </div>
                      </div>

                      {/* Amount */}
                      <div className="text-right min-w-0">
                        <div className="font-semibold text-slate-100 tabular-nums truncate">
                          {displayCurrency === 'USD' ? `$${alert.amount.toLocaleString('en-US')}` : `৳${alert.amountBdt.toLocaleString('en-US')}`}
                        </div>
                        <div className="text-xs text-slate-500 tabular-nums truncate">
                          {displayCurrency === 'USD' ? `৳${alert.amountBdt.toLocaleString('en-US')}` : `$${alert.amount.toLocaleString('en-US')}`}
                        </div>
                      </div>

                      {/* Rail & BIC */}
                      <div className="text-xs text-slate-300 leading-tight truncate">
                        <div className="truncate">{alert.rail}</div>
                        <div className="text-xs text-slate-500 truncate">{alert.bic}</div>
                      </div>

                      {/* Risk Tier Badge */}
                      <div className="text-center">
                        <span
                          className={`inline-block px-2 py-0.5 rounded text-xs font-mono font-bold whitespace-nowrap border-l-2 ${alert.tierCode === 1
                            ? 'bg-rose-500/15 text-rose-300 border border-rose-500/30 border-l-rose-500'
                            : alert.tierCode === 2
                              ? 'bg-amber-500/15 text-amber-300 border border-amber-500/30 border-l-amber-500'
                              : 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 border-l-emerald-500'
                            }`}
                        >
                          Tier {alert.tierCode} · {alert.tierCode === 1 ? 'Hold' : alert.tierCode === 2 ? 'Review' : 'Clear'}
                        </span>
                      </div>

                      {/* Calibrated Risk Score & Decision Set */}
                      <div className="text-center font-mono text-xs">
                        <div className="font-bold text-slate-200 tabular-nums">{alert.riskScore}</div>
                        <div className={`text-xs ${alert.tierCode === 1 ? 'text-rose-400' : alert.tierCode === 2 ? 'text-amber-400' : 'text-emerald-400'}`}>
                          {alert.decisionSet}
                        </div>
                      </div>

                      {/* SLA Countdown */}
                      <div className="text-center font-mono text-xs tabular-nums">
                        <span
                          className={`px-1.5 py-0.5 rounded ${alert.slaMinutesLeft < 60
                            ? 'bg-rose-950/60 text-rose-400 font-bold border border-rose-800/40 animate-pulse'
                            : alert.slaMinutesLeft < 180
                              ? 'bg-amber-950/60 text-amber-400'
                              : 'text-slate-400'
                            }`}
                        >
                          {alert.slaMinutesLeft}m
                        </span>
                      </div>

                      {/* Assignee */}
                      <div className="text-xs text-slate-300 truncate font-mono">
                        {alert.assignee}
                      </div>

                      {/* Action Buttons */}
                      <div className="flex items-center justify-end gap-1.5" onClick={(e) => e.stopPropagation()}>
                        <button
                          onClick={() => setInspectingAlert(alert)}
                          title="Inspect Raw SWIFT / ISO Message"
                          className="p-1 rounded bg-[#1E293B] hover:bg-[#334155] text-slate-300 hover:text-white transition-colors cursor-pointer"
                        >
                          <FileText className="w-3.5 h-3.5 text-sky-400" />
                        </button>
                        <Link
                          href={`/graph?node=${encodeURIComponent(alert.account)}`}
                          title="Inspect Multi-Hop Flow Graph"
                          className="p-1 rounded bg-[#1E293B] hover:bg-[#334155] text-slate-300 hover:text-white transition-colors"
                        >
                          <GitFork className="w-3.5 h-3.5 text-emerald-400" />
                        </Link>
                        {alert.caseId && (
                          <Link
                            href={`/cases/${alert.caseId}`}
                            title="Open Linked Case Dossier"
                            className="p-1 rounded bg-[#1E293B] hover:bg-[#334155] text-slate-300 hover:text-white transition-colors"
                          >
                            <ExternalLink className="w-3.5 h-3.5 text-purple-400" />
                          </Link>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Sticky Floating Bulk Action Drawer */}
      {selectedRowIds.size > 0 && (
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-40 bg-[#0F172A] border border-[#334155] shadow-2xl rounded-2xl px-5 sm:px-6 py-3 flex flex-wrap items-center gap-4 sm:gap-6 text-xs text-slate-200 animate-in slide-in-from-bottom duration-200">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="font-semibold text-slate-100">
              {selectedRowIds.size} Alerts Selected
            </span>
            <span className="text-slate-400 hidden sm:inline">
              (Total Exposure: <strong className="font-mono text-emerald-400 tabular-nums">${totalSelectedExposure.toLocaleString()}</strong>)
            </span>
          </div>

          <div className="h-4 w-px bg-[#334155] hidden sm:block" />

          {/* Assignee Selector */}
          <div className="flex items-center gap-2">
            <select
              value={assigneeTarget}
              onChange={(e) => setAssigneeTarget(e.target.value)}
              className="px-2.5 py-1 bg-[#1E293B] border border-[#334155] rounded text-slate-200 text-xs focus:outline-none"
            >
              <option value="Amina Rahman, CFE (Lead Investigator)">Amina Rahman, CFE (Lead Investigator)</option>
              <option value="Tanvir Ahmed (Triage Analyst)">Tanvir Ahmed (Triage Analyst)</option>
              <option value="Nadia Hossain (Trade Specialist)">Nadia Hossain (Trade Specialist)</option>
              <option value="Kazi Rafiqul Islam, CAMS (Demo CCO)">Kazi Rafiqul Islam, CAMS (Demo CCO)</option>
            </select>
            <button
              onClick={handleBatchAssign}
              className="px-3 py-1 rounded bg-[#1E293B] hover:bg-[#334155] text-slate-200 font-semibold border border-[#334155] cursor-pointer"
            >
              Assign
            </button>
          </div>

          <div className="h-4 w-px bg-[#334155] hidden sm:block" />

          {/* Action Buttons */}
          <div className="flex items-center gap-2">
            <button
              onClick={() => {
                setFourEyesModalOpen(true, {
                  actionType: 'ACCOUNT_FREEZE',
                  actionTitle: `Batch Administrative Freeze (${selectedRowIds.size} Accounts)`,
                  targetId: Array.from(selectedRowIds).join(', '),
                  details: `Execute regulatory freeze on ${selectedRowIds.size} flagged accounts across payment rails. Total exposure: $${totalSelectedExposure.toLocaleString()}`
                });
              }}
              className="px-3 py-1.5 rounded-lg bg-rose-950/60 hover:bg-rose-900/80 text-rose-300 border border-rose-800/60 font-semibold transition-colors flex items-center gap-1.5 cursor-pointer"
            >
              <Lock className="w-3.5 h-3.5" />
              <span>Freeze (4-Eyes)</span>
            </button>

            <button
              onClick={handleBatchEscalate}
              className="px-3 py-1.5 rounded-lg bg-purple-950/60 hover:bg-purple-900/80 text-purple-300 border border-purple-800/60 font-semibold transition-colors flex items-center gap-1.5 cursor-pointer"
            >
              <ShieldAlert className="w-3.5 h-3.5" />
              <span>Escalate to Case</span>
            </button>

            <Link
              href="/rfi"
              className="px-3 py-1.5 rounded-lg bg-[#1E293B] hover:bg-[#334155] text-slate-200 font-medium transition-colors flex items-center gap-1.5"
            >
              <MailQuestion className="w-3.5 h-3.5 text-indigo-400" />
              <span>Dispatch RFI</span>
            </Link>

            <button
              onClick={handleBatchDismiss}
              className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 font-medium cursor-pointer"
            >
              Dismiss (FP)
            </button>

            <button
              onClick={() => setSelectedRowIds(new Set())}
              className="px-2.5 py-1.5 text-slate-400 hover:text-slate-200 cursor-pointer"
            >
              Clear
            </button>
          </div>
        </div>
      )}

      {/* Raw SWIFT MT700 / ISO 20022 Wire Inspector Slide-Over */}
      {inspectingAlert && (
        <div role="dialog" aria-modal="true" aria-label="Raw wire inspector" className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex justify-end animate-in fade-in duration-200">
          <div className="w-full max-w-2xl bg-[#0F172A] border-l border-[#1E293B] h-full flex flex-col shadow-2xl overflow-hidden">
            {/* Slide-Over Header */}
            <div className="p-5 bg-[#0B0F17] border-b border-[#1E293B] flex items-center justify-between">
              <div>
                <div className="flex items-center gap-2">
                  <span className={`px-2 py-0.5 rounded text-xs font-mono font-bold ${inspectingAlert.tierCode === 1 ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40' : 'bg-amber-500/20 text-amber-300 border border-amber-500/40'
                    }`}>
                    TIER {inspectingAlert.tierCode} HOLD
                  </span>
                  <h2 className="text-base font-bold text-slate-100 font-mono">
                    {inspectingAlert.id} — Raw Wire Inspector
                  </h2>
                </div>
                <p className="text-xs text-slate-400 mt-1">
                  Interbank clearing telemetry • Rail: <strong className="text-slate-200">{inspectingAlert.rail}</strong> • BIC: <strong className="text-slate-200">{inspectingAlert.bic}</strong>
                </p>
              </div>

              <button
                onClick={() => setInspectingAlert(null)}
                aria-label="Close inspector"
                className="p-1.5 rounded-lg hover:bg-[#1E293B] text-slate-400 hover:text-slate-100 cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Slide-Over Body */}
            <div className="p-5 space-y-6 flex-1 overflow-y-auto font-sans">
              {/* Highlight Ribbon */}
              <div className="p-4 rounded-xl bg-[#0B0F17] border border-[#1E293B] space-y-2">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-400">Flagged Entity:</span>
                  <span className="font-semibold text-slate-100">{inspectingAlert.entityName}</span>
                </div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-400">Account Number:</span>
                  <PiiText value={inspectingAlert.account} type="account" className="font-mono text-slate-200" />
                </div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-400">Amount &amp; Currency:</span>
                  <span className="font-mono font-bold text-emerald-400 text-sm">
                    ${inspectingAlert.amount.toLocaleString(undefined, { minimumFractionDigits: 2 })} USD
                    <span className="text-slate-500 text-xs ml-1">(৳{inspectingAlert.amountBdt.toLocaleString()} BDT)</span>
                  </span>
                </div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-400">Typology Match:</span>
                  <span className="font-mono text-rose-300">{inspectingAlert.typology}</span>
                </div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-400">SLA Countdown:</span>
                  <span className="font-mono text-amber-400 font-bold">{inspectingAlert.slaMinutesLeft} minutes remaining</span>
                </div>
              </div>

              {/* Wire Message Payload Decomposition */}
              <div>
                <h3 className="text-xs font-bold text-slate-300 mb-2 font-mono flex items-center justify-between">
                  <span>Decomposed Clearing Payload ({inspectingAlert.wirePayload?.messageType || 'SWIFT MT700'})</span>
                  <span className="text-xs text-emerald-400 font-normal">Validated Syntax</span>
                </h3>

                <div className="bg-[#0B0F17] border border-[#1E293B] rounded-xl p-4 font-mono text-xs space-y-2 text-slate-300">
                  {inspectingAlert.wirePayload ? (
                    <>
                      <div className="flex items-start gap-3 py-1 border-b border-[#1E293B]/40">
                        <span className="text-sky-400 font-bold w-28 shrink-0">Message Rail:</span>
                        <span className="text-slate-100">{inspectingAlert.wirePayload.messageType}</span>
                      </div>
                      <div className="flex items-start gap-3 py-1 border-b border-[#1E293B]/40">
                        <span className="text-sky-400 font-bold w-28 shrink-0">Ordering Party:</span>
                        <span className="text-slate-200">{inspectingAlert.wirePayload.orderingCustomer}</span>
                      </div>
                      <div className="flex items-start gap-3 py-1 border-b border-[#1E293B]/40">
                        <span className="text-sky-400 font-bold w-28 shrink-0">Ordering Bank:</span>
                        <span className="text-slate-200">{inspectingAlert.wirePayload.orderingInstitution}</span>
                      </div>
                      <div className="flex items-start gap-3 py-1 border-b border-[#1E293B]/40">
                        <span className="text-sky-400 font-bold w-28 shrink-0">Beneficiary:</span>
                        <span className="text-slate-200">{inspectingAlert.wirePayload.beneficiaryCustomer}</span>
                      </div>
                      <div className="flex items-start gap-3 py-1 border-b border-[#1E293B]/40">
                        <span className="text-sky-400 font-bold w-28 shrink-0">Remittance:</span>
                        <span className="text-emerald-400">{inspectingAlert.wirePayload.remittanceInfo}</span>
                      </div>
                      <div className="pt-1 text-xs text-rose-400">
                        Regulatory Indicators: {inspectingAlert.wirePayload.regulatoryFlags.join(' • ')}
                      </div>
                    </>
                  ) : (
                    <div className="text-slate-400">Standard Clearing Payload Verified</div>
                  )}
                </div>
              </div>

              {/* Feature Attribution & Explainability (12 Topological Invariants / SHAP) */}
              <div className="p-4 rounded-xl bg-[#0B0F17] border border-[#1E293B] space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Sparkles className="w-4 h-4 text-cyan-400" />
                    <span className="text-xs font-bold text-slate-100 font-mono">
                      C-STGB Model Explainability (12 Invariants)
                    </span>
                  </div>
                  <button
                    onClick={() => setShowExplainability(!showExplainability)}
                    className="text-xs font-mono text-cyan-400 hover:text-cyan-300 underline cursor-pointer"
                  >
                    {showExplainability ? 'Hide Attribution Details' : 'Show SHAP Waterfall (12 Invariants)'}
                  </button>
                </div>

                {showExplainability && (
                  <div className="space-y-3 pt-2 text-xs font-mono border-t border-[#1E293B]">
                    <div className="p-2.5 rounded-lg bg-sky-950/20 border border-sky-800/40 text-xs text-sky-300">
                      <strong>Dominant Typology:</strong> {inspectingAlert.typology} &bull; Expected Benign Baseline: E[Y] = 0.052 &bull; Calibrated Risk: {(inspectingAlert.riskScore * 100).toFixed(1)}%
                    </div>

                    <div className="space-y-2">
                      <div className="p-2.5 rounded-lg bg-[#0F172A] border border-[#1E293B] flex items-center justify-between">
                        <div>
                          <div className="font-bold text-slate-200">Pass-Through Net Flow Ratio (φ_flow)</div>
                          <div className="text-xs text-slate-400">Observed: 0.94 • Baseline: 0.12 • BFIU MC 26 § 4.3</div>
                        </div>
                        <span className="px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 font-bold text-xs">
                          +0.285 (RISK_ELEVATING)
                        </span>
                      </div>

                      <div className="p-2.5 rounded-lg bg-[#0F172A] border border-[#1E293B] flex items-center justify-between">
                        <div>
                          <div className="font-bold text-slate-200">15-Minute Rapid Fund Dispersion (δ_disp)</div>
                          <div className="text-xs text-slate-400">Observed: 0.93 • Baseline: 0.05 • Instantaneous Outflows</div>
                        </div>
                        <span className="px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 font-bold text-xs">
                          +0.241 (RISK_ELEVATING)
                        </span>
                      </div>

                      <div className="p-2.5 rounded-lg bg-[#0F172A] border border-[#1E293B] flex items-center justify-between">
                        <div>
                          <div className="font-bold text-slate-200">Structuring Proximity (s_struct)</div>
                          <div className="text-xs text-slate-400">Observed: 0.91 • Band: ৳800k–৳999k CTR Ceiling Proximity</div>
                        </div>
                        <span className="px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 font-bold text-xs">
                          +0.201 (RISK_ELEVATING)
                        </span>
                      </div>

                      <div className="p-2.5 rounded-lg bg-[#0F172A] border border-[#1E293B] flex items-center justify-between">
                        <div>
                          <div className="font-bold text-slate-200">Velocity Burst Acceleration (λ_u)</div>
                          <div className="text-xs text-slate-400">Observed: 0.88 • Baseline: 0.15 • Smurfing Frequency Spike</div>
                        </div>
                        <span className="px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 font-bold text-xs">
                          +0.163 (RISK_ELEVATING)
                        </span>
                      </div>
                    </div>

                    {/* Internal Sensitivity Driver (Strictly Non-Customer-Facing) */}
                    <div className="p-3 bg-emerald-950/20 border border-emerald-800/40 rounded-lg space-y-1 text-xs">
                      <span className="font-bold text-emerald-300 block">Internal Sensitivity Threshold Note (Non-Customer-Facing):</span>
                      <p className="text-slate-300 font-sans">
                        Sensitivity baseline: if counterparty dispersion window exceeds 48h and structuring proximity falls below ৳800,000, model score attenuates to 0.142 (-80.0%) within Tier 3 bounds.
                      </p>
                    </div>
                  </div>
                )}
              </div>

              {/* Action Buttons Inside Drawer */}
              <div className="pt-2 flex flex-wrap items-center gap-3">
                <button
                  onClick={() => {
                    setOverrideScore(0.12);
                    setOverrideTier('Tier 3 Clear');
                    setOverrideJustification('DOCUMENTED_TRADE_INVOICE');
                    setOverrideModalOpen(true);
                  }}
                  className="px-4 py-2 rounded-lg bg-amber-600 hover:bg-amber-500 text-white font-semibold text-xs transition-colors flex items-center gap-2 cursor-pointer shadow-lg shadow-amber-600/20"
                >
                  <Sliders className="w-4 h-4" />
                  <span>Override Score (Supervisory)</span>
                </button>

                <button
                  onClick={() => {
                    setFourEyesModalOpen(true, {
                      actionType: 'ACCOUNT_FREEZE',
                      actionTitle: `Emergency Freeze (${inspectingAlert.entityName})`,
                      targetId: inspectingAlert.account,
                      details: `Execute regulatory freeze on account ${inspectingAlert.account} pursuant to anti-money laundering powers.`
                    });
                  }}
                  className="px-4 py-2 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-semibold text-xs transition-colors flex items-center gap-2 cursor-pointer"
                >
                  <Lock className="w-4 h-4" />
                  <span>Freeze Account (4-Eyes)</span>
                </button>

                <button
                  onClick={() => {
                    escalateToCase(inspectingAlert.id);
                    setInspectingAlert(null);
                  }}
                  className="px-4 py-2 rounded-lg bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs transition-colors flex items-center gap-2 cursor-pointer"
                >
                  <ShieldAlert className="w-4 h-4" />
                  <span>Escalate to Case</span>
                </button>

                <Link
                  href={`/graph?node=${encodeURIComponent(inspectingAlert.account)}`}
                  className="px-4 py-2 rounded-lg bg-[#1E293B] hover:bg-[#334155] text-slate-200 font-medium text-xs transition-colors flex items-center gap-2"
                >
                  <GitFork className="w-4 h-4 text-emerald-400" />
                  <span>Inspect Flow Graph</span>
                </Link>

                <Link
                  href="/rfi"
                  className="px-4 py-2 rounded-lg bg-[#1E293B] hover:bg-[#334155] text-slate-200 font-medium text-xs transition-colors flex items-center gap-2"
                >
                  <MailQuestion className="w-4 h-4 text-sky-400" />
                  <span>Dispatch RFI</span>
                </Link>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Dismiss Reason Modal */}
      {dismissReasonModalOpen && (
        <div role="dialog" aria-modal="true" aria-label="Dismiss alert reason" className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-[#0F172A] border border-[#334155] rounded-2xl max-w-md w-full p-6 space-y-4 shadow-2xl">
            <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
              <ShieldX className="w-5 h-5 text-amber-400" />
              Audited Alert Dismissal Memo
            </h3>
            <p className="text-xs text-slate-400">
              Provide mandatory compliance rationale for dismissing {selectedRowIds.size} selected alert(s) as False Positive. This entry will be cryptographically written to the WORM ledger.
            </p>

            <textarea
              value={dismissReason}
              onChange={(e) => setDismissReason(e.target.value)}
              placeholder="e.g. Verified ongoing LC trade documentation with genuine ASYCUDA customs clearance bills. Commercial rationale confirmed."
              className="w-full h-24 p-3 bg-[#0B0F17] border border-[#334155] rounded-xl text-xs text-slate-100 placeholder:text-slate-600 focus:outline-none focus:border-amber-500"
            />

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                onClick={() => setDismissReasonModalOpen(false)}
                className="px-4 py-2 text-xs text-slate-400 hover:text-slate-200 cursor-pointer"
              >
                Cancel
              </button>
              <button
                onClick={confirmBatchDismiss}
                className="px-4 py-2 rounded-lg bg-amber-600 hover:bg-amber-500 text-white font-semibold text-xs transition-colors cursor-pointer"
              >
                Confirm &amp; Write to Audit Trail
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Supervisory Override Modal */}
      {overrideModalOpen && inspectingAlert && (
        <div role="dialog" aria-modal="true" aria-label="Supervisory override" className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-[#0F172A] border border-[#334155] rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between pb-2 border-b border-[#1E293B]">
              <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
                <Sliders className="w-5 h-5 text-amber-400" />
                Supervisory Model Score Override
              </h3>
              <button
                onClick={() => setOverrideModalOpen(false)}
                className="text-slate-400 hover:text-slate-200 cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <p className="text-xs text-slate-400 leading-relaxed">
              Enforce supervisory override on alert <strong>{inspectingAlert.id}</strong> ({inspectingAlert.entityName}).
              This modification will be cryptographically sealed into the WORM ledger with full officer accountability.
            </p>

            <div className="space-y-3 text-xs font-mono">
              <div>
                <label className="text-xs text-slate-400 block mb-1">Original Model Score</label>
                <div className="p-2.5 bg-[#0B0F17] rounded-lg border border-[#1E293B] text-rose-400 font-bold">
                  {(inspectingAlert.riskScore * 100).toFixed(1)}% &bull; {inspectingAlert.tier}
                </div>
              </div>

              <div>
                <label className="text-xs text-slate-400 block mb-1">
                  Adjusted Risk Score: {(overrideScore * 100).toFixed(1)}%
                </label>
                <input
                  type="range"
                  min="0.01"
                  max="0.99"
                  step="0.01"
                  value={overrideScore}
                  onChange={(e) => setOverrideScore(parseFloat(e.target.value))}
                  className="w-full accent-amber-500 cursor-pointer"
                />
              </div>

              <div>
                <label className="text-xs text-slate-400 block mb-1">New Triage Tier</label>
                <select
                  value={overrideTier}
                  onChange={(e) => setOverrideTier(e.target.value as 'Tier 1 Hold' | 'Tier 2 Review' | 'Tier 3 Clear')}
                  className="w-full p-2.5 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-200 text-xs focus:outline-none focus:border-amber-500"
                >
                  <option value="Tier 3 Clear">Tier 3 Clear (Straight-Through)</option>
                  <option value="Tier 2 Review">Tier 2 Review (Standard SLA Queue)</option>
                  <option value="Tier 1 Hold">Tier 1 Hold (Escrow Containment)</option>
                </select>
              </div>

              <div>
                <label className="text-xs text-slate-400 block mb-1">Justification Code (Mandatory)</label>
                <select
                  value={overrideJustification}
                  onChange={(e) => setOverrideJustification(e.target.value)}
                  className="w-full p-2.5 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-200 text-xs focus:outline-none focus:border-amber-500"
                >
                  <option value="DOCUMENTED_TRADE_INVOICE">DOCUMENTED_TRADE_INVOICE — Verified Trade LC &amp; Customs Bill</option>
                  <option value="VERIFIED_PAYROLL_SPIKE">VERIFIED_PAYROLL_SPIKE — Certified Multi-Party Corporate Payroll</option>
                  <option value="ESTABLISHED_INTRA_GROUP_TRANSFER">ESTABLISHED_INTRA_GROUP_TRANSFER — Inter-Company Treasury Sweep</option>
                  <option value="GOVERNMENT_DIPLOMATIC_EXEMPTION">GOVERNMENT_DIPLOMATIC_EXEMPTION — Sovereign or Diplomatic Protocol</option>
                  <option value="FALSE_POSITIVE_HOMONYM_CONFIRMED">FALSE_POSITIVE_HOMONYM_CONFIRMED — Non-Target Individual Verified</option>
                </select>
              </div>

              <div>
                <label className="text-xs text-slate-400 block mb-1">Supervisory Compliance Notes</label>
                <textarea
                  value={overrideNotes}
                  onChange={(e) => setOverrideNotes(e.target.value)}
                  rows={3}
                  className="w-full p-2.5 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-200 text-xs focus:outline-none focus:border-amber-500"
                  placeholder="Mandatory reasoning under SR 11-7 model-risk supervisory standards..."
                />
              </div>
            </div>

            <div className="flex items-center justify-end gap-3 pt-2 border-t border-[#1E293B]">
              <button
                onClick={() => setOverrideModalOpen(false)}
                className="px-4 py-2 text-xs text-slate-400 hover:text-slate-200 cursor-pointer"
              >
                Cancel
              </button>
              <button
                onClick={handleConfirmOverride}
                disabled={isSubmittingOverride || overrideNotes.trim().length < 5}
                className="px-4 py-2 rounded-lg bg-amber-600 hover:bg-amber-500 disabled:opacity-50 text-white font-semibold text-xs transition-colors cursor-pointer flex items-center gap-2"
              >
                {isSubmittingOverride ? 'Sealing in WORM...' : 'Sign & Seal Override'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
