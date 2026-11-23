'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import {
  FolderGit2,
  Search,
  Filter,
  Plus,
  ArrowRight,
  ShieldAlert,
  Clock,
  User,
  Building,
  CheckCircle2,
  FileText,
  AlertTriangle,
  GitFork,
  LayoutGrid,
  List,
  DollarSign,
  X,
  ExternalLink
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { PiiText } from '@/components/ui/PiiText';
import { formatCurrencyByJurisdiction } from '@/lib/compliance/jurisdictions';

export default function CasesPage() {
  const { cases, jurisdiction, createCase } = useBankingStore();
  const [statusFilter, setStatusFilter] = useState<string>('ALL');
  const [priorityFilter, setPriorityFilter] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [viewMode, setViewMode] = useState<'grid' | 'table'>('grid');

  // Modal State
  const [isNewCaseModalOpen, setIsNewCaseModalOpen] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newSubject, setNewSubject] = useState('');
  const [newExposure, setNewExposure] = useState('250000');
  const [newPriority, setNewPriority] = useState<'CRITICAL' | 'HIGH' | 'MEDIUM'>('HIGH');
  const [newAssignee, setNewAssignee] = useState('Amina Rahman, CFE (Lead Investigator)');

  const filteredCases = cases.filter((c) => {
    const matchesStatus = statusFilter === 'ALL' || c.status === statusFilter;
    const matchesSearch =
      searchQuery === '' ||
      c.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.entityName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.leadInvestigator.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesStatus && matchesSearch;
  });

  const handleCreateCase = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim() || !newSubject.trim()) return;

    createCase({
      title: newTitle.trim(),
      subjectEntity: newSubject.trim(),
      priority: newPriority,
      assignedTo: newAssignee,
      exposureUsd: parseFloat(newExposure) || 100000
    });

    setIsNewCaseModalOpen(false);
    setNewTitle('');
    setNewSubject('');
    setNewExposure('250000');
  };

  return (
    <div className="p-4 sm:p-5 lg:p-6 max-w-[1750px] mx-auto space-y-5">
      {/* Page Title & Controls */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2 font-sans">
            <FolderGit2 className="w-5 h-5 text-sky-400" />
            Institutional Case Management Docket
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            WORM-audited multi-stage investigation dossiers with cryptographic evidence preservation complying with FRE 902(11) &amp; BFIU reporting guidelines.
          </p>
        </div>

        <div className="flex items-center gap-3">
          {/* View Mode Switcher */}
          <div className="flex items-center bg-[#0F172A] p-1 rounded-lg border border-[#334155] text-xs">
            <button
              onClick={() => setViewMode('grid')}
              className={`flex items-center gap-1.5 px-2.5 py-1 rounded transition-all cursor-pointer ${
                viewMode === 'grid'
                  ? 'bg-sky-500/20 text-sky-300 font-bold border border-sky-500/40'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <LayoutGrid className="w-3.5 h-3.5" />
              <span>Grid</span>
            </button>
            <button
              onClick={() => setViewMode('table')}
              className={`flex items-center gap-1.5 px-2.5 py-1 rounded transition-all cursor-pointer ${
                viewMode === 'table'
                  ? 'bg-sky-500/20 text-sky-300 font-bold border border-sky-500/40'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <List className="w-3.5 h-3.5" />
              <span>Table</span>
            </button>
          </div>

          <button
            onClick={() => setIsNewCaseModalOpen(true)}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs uppercase tracking-wide transition-all shadow-lg shadow-emerald-600/20 cursor-pointer"
          >
            <Plus className="w-4 h-4" />
            <span>Open New Case</span>
          </button>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-2 border-b border-[#1E293B]">
        <div className="flex flex-wrap items-center gap-1.5">
          {['ALL', 'INVESTIGATION_OPEN', 'EVIDENCE_COLLECTED', 'SAR_DRAFTED', 'PENDING_FOUR_EYES', 'CLOSED'].map((st) => (
            <button
              key={st}
              onClick={() => setStatusFilter(st)}
              className={`px-3 py-1 rounded-lg text-xs font-semibold transition-colors cursor-pointer ${
                statusFilter === st
                  ? 'bg-[#1E293B] text-slate-100 border border-[#334155]'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {st === 'ALL' ? `All Cases (${cases.length})` : st.replace(/_/g, ' ')}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-3">
          <select
            value={priorityFilter}
            onChange={(e) => setPriorityFilter(e.target.value)}
            className="px-2.5 py-1 bg-[#0F172A] border border-[#334155] rounded-lg text-xs text-slate-300 cursor-pointer"
          >
            <option value="ALL">All Priorities</option>
            <option value="CRITICAL">Critical</option>
            <option value="HIGH">High</option>
            <option value="MEDIUM">Medium</option>
          </select>

          <div className="relative w-56">
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-2 text-slate-500" />
            <input
              type="text"
              placeholder="Search docket..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-8 pr-2.5 py-1 bg-[#0F172A] border border-[#334155] rounded-lg text-xs text-slate-200 placeholder:text-slate-500 focus:outline-none"
            />
          </div>
        </div>
      </div>

      {/* Case Views */}
      {viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredCases.map((c) => (
            <div
              key={c.id}
              className="p-5 rounded-2xl bg-[#0F172A] border border-[#1E293B] hover:border-[#334155] shadow-xl flex flex-col justify-between space-y-4 group transition-all"
            >
              <div>
                <div className="flex items-center justify-between gap-2">
                  <span className="font-mono text-xs font-bold text-sky-400">{c.id}</span>
                  <span
                    className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
                      c.slaHours <= 24
                        ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
                        : 'bg-amber-500/20 text-amber-300 border border-amber-500/40'
                    }`}
                  >
                    {c.slaHours}H SLA
                  </span>
                </div>

                <h3 className="text-sm font-bold text-slate-100 mt-2 group-hover:text-sky-300 transition-colors">
                  {c.title}
                </h3>

                <p className="text-xs text-slate-400 mt-1 flex items-center gap-1.5">
                  <Building className="w-3.5 h-3.5 text-slate-500" />
                  <span className="font-medium text-slate-300">{c.entityName}</span>
                </p>
              </div>

              {/* Status and Milestones Mini-Bar */}
              <div className="space-y-2 pt-2 border-t border-[#1E293B]">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-500">Status:</span>
                  <span className="font-mono font-semibold text-slate-200 text-[11px]">
                    {c.status.replace(/_/g, ' ')}
                  </span>
                </div>

                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-500">Total Exposure:</span>
                  <span className="font-mono font-bold text-emerald-400">
                    {formatCurrencyByJurisdiction(c.riskExposureUsd, jurisdiction)}
                  </span>
                </div>

                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-500">Assigned To:</span>
                  <span className="text-slate-300 text-[11px] font-mono">{c.leadInvestigator}</span>
                </div>
              </div>

              {/* Footer Links */}
              <div className="pt-2 flex items-center justify-between">
                <span className="text-[10px] font-mono text-slate-500">{c.createdAt}</span>
                <Link
                  href={`/cases/${c.id}`}
                  className="px-3 py-1 rounded-lg bg-[#1E293B] hover:bg-[#334155] text-slate-200 hover:text-white text-xs font-semibold flex items-center gap-1.5 transition-colors"
                >
                  <span>Dossier</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      ) : (
        /* Dense Table View */
        <div className="bg-[#0F172A] border border-[#1E293B] rounded-xl overflow-hidden shadow-2xl">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-[#0B0F17] border-b border-[#1E293B] text-[11px] font-mono uppercase text-slate-400">
                <tr>
                  <th className="px-4 py-3">Case ID</th>
                  <th className="px-4 py-3">Title &amp; Target Entity</th>
                  <th className="px-4 py-3">Priority</th>
                  <th className="px-4 py-3">Status</th>
                  <th className="px-4 py-3 text-right">Exposure</th>
                  <th className="px-4 py-3">Assigned Lead</th>
                  <th className="px-4 py-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1E293B]">
                {filteredCases.map((c) => (
                  <tr key={c.id} className="hover:bg-[#1E293B]/40 transition-colors">
                    <td className="px-4 py-3 font-mono font-bold text-sky-400">{c.id}</td>
                    <td className="px-4 py-3">
                      <div className="font-semibold text-slate-100">{c.title}</div>
                      <div className="text-[11px] text-slate-400">{c.entityName}</div>
                    </td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
                        c.slaHours <= 24 ? 'bg-rose-500/20 text-rose-300' : 'bg-amber-500/20 text-amber-300'
                      }`}>
                        {c.slaHours}H SLA
                      </span>
                    </td>
                    <td className="px-4 py-3 font-mono text-[11px]">{c.status.replace(/_/g, ' ')}</td>
                    <td className="px-4 py-3 text-right font-mono font-bold text-emerald-400 tabular-nums">
                      {formatCurrencyByJurisdiction(c.riskExposureUsd, jurisdiction)}
                    </td>
                    <td className="px-4 py-3 font-mono text-slate-400">{c.leadInvestigator}</td>
                    <td className="px-4 py-3 text-right">
                      <Link
                        href={`/cases/${c.id}`}
                        className="px-2.5 py-1 rounded bg-[#1E293B] hover:bg-[#334155] text-slate-200 text-xs font-semibold inline-flex items-center gap-1"
                      >
                        <span>Open</span>
                        <ArrowRight className="w-3 h-3" />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Open New Case Modal */}
      {isNewCaseModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-[#0F172A] border border-[#334155] rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between pb-3 border-b border-[#1E293B]">
              <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
                <FolderGit2 className="w-5 h-5 text-emerald-400" />
                Initialize Institutional Investigation Dossier
              </h3>
              <button
                onClick={() => setIsNewCaseModalOpen(false)}
                className="text-slate-400 hover:text-slate-200"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCreateCase} className="space-y-4 text-xs font-sans">
              <div>
                <label className="text-slate-400 block mb-1 font-mono uppercase text-[10px]">Case Title</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Meghna Multi-Hop TBML Export Structuring Investigation"
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-100 focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div>
                <label className="text-slate-400 block mb-1 font-mono uppercase text-[10px]">Subject Corporate Entity / Individual</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Meghna Global Trading Ltd / Al-Mansoor Freight"
                  value={newSubject}
                  onChange={(e) => setNewSubject(e.target.value)}
                  className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-100 focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-400 block mb-1 font-mono uppercase text-[10px]">Estimated Exposure (USD)</label>
                  <input
                    type="number"
                    required
                    value={newExposure}
                    onChange={(e) => setNewExposure(e.target.value)}
                    className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-100 focus:outline-none focus:border-emerald-500 font-mono"
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1 font-mono uppercase text-[10px]">Priority Band</label>
                  <select
                    value={newPriority}
                    onChange={(e) => setNewPriority(e.target.value as any)}
                    className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-100 cursor-pointer"
                  >
                    <option value="CRITICAL">CRITICAL (&lt; 24h SLA)</option>
                    <option value="HIGH">HIGH (&lt; 48h SLA)</option>
                    <option value="MEDIUM">MEDIUM (&lt; 72h SLA)</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="text-slate-400 block mb-1 font-mono uppercase text-[10px]">Assigned Senior Compliance Officer</label>
                <select
                  value={newAssignee}
                  onChange={(e) => setNewAssignee(e.target.value)}
                  className="w-full px-3 py-2 bg-[#0B0F17] border border-[#334155] rounded-lg text-slate-100 cursor-pointer"
                >
                  <option value="Amina Rahman, CFE (Lead Investigator)">Amina Rahman, CFE (Lead Investigator)</option>
                  <option value="Tanvir Ahmed (Triage Analyst)">Tanvir Ahmed (Triage Analyst)</option>
                  <option value="Kazi Rafiqul Islam, CAMS (Demo CCO)">Kazi Rafiqul Islam, CAMS (Demo CCO)</option>
                  <option value="Nadia Hossain (Trade Specialist)">Nadia Hossain (Trade Specialist)</option>
                </select>
              </div>

              <div className="flex items-center justify-end gap-3 pt-3 border-t border-[#1E293B]">
                <button
                  type="button"
                  onClick={() => setIsNewCaseModalOpen(false)}
                  className="px-4 py-2 text-slate-400 hover:text-slate-200 cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold cursor-pointer"
                >
                  Initialize Case Dossier
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
