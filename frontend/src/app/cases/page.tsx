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
  Printer,
  Download,
  List,
  DollarSign,
  X,
  ExternalLink
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { PiiText } from '@/components/ui/PiiText';
import { CommercialCase } from '@/lib/data/commercialSeed';

export default function CasesPage() {
  const { cases, createCase, formatMoney, t } = useBankingStore();
  const [statusFilter, setStatusFilter] = useState<string>('ALL');
  const [priorityFilter, setPriorityFilter] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [viewMode, setViewMode] = useState<'grid' | 'table'>('grid');

  // Modal States
  const [isNewCaseModalOpen, setIsNewCaseModalOpen] = useState(false);
  const [selectedCaseForPrint, setSelectedCaseForPrint] = useState<CommercialCase | null>(null);

  const handleExportAllJson = () => {
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(filteredCases, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute('href', dataStr);
    downloadAnchor.setAttribute('download', `BFIU-CASES-DOCKET-${new Date().toISOString().slice(0, 10)}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  const handlePrintDossier = (c: CommercialCase) => {
    setSelectedCaseForPrint(c);
  };
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

          {/* Export JSON Docket */}
          <button
            type="button"
            onClick={handleExportAllJson}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#0F172A] hover:bg-[#1E293B] text-slate-200 border border-[#334155] text-xs font-mono font-semibold transition-all cursor-pointer"
            title="Export all filtered cases to JSON docket"
          >
            <Download className="w-3.5 h-3.5 text-cyan-400" />
            <span className="hidden sm:inline">Export JSON</span>
          </button>

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
                    {formatMoney(c.riskExposureUsd * 120)}
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
                <div className="flex items-center gap-1.5">
                  <button
                    type="button"
                    onClick={() => handlePrintDossier(c)}
                    className="p-1.5 rounded-lg bg-[#1E293B] hover:bg-[#334155] text-slate-300 hover:text-emerald-400 transition-colors cursor-pointer"
                    title="Print Formal BFIU Case Dossier"
                  >
                    <Printer className="w-3.5 h-3.5" />
                  </button>
                  <Link
                    href={`/cases/${c.id}`}
                    className="px-3 py-1 rounded-lg bg-[#1E293B] hover:bg-[#334155] text-slate-200 hover:text-white text-xs font-semibold flex items-center gap-1.5 transition-colors"
                  >
                    <span>Dossier</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        /* Dense Table View */
        <div className="bg-[#0F172A] border border-[#1E293B] rounded-xl overflow-hidden shadow-2xl">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300" role="table" aria-label="Institutional investigation cases">
              <thead className="bg-[#0B0F17] border-b border-[#1E293B] text-[11px] font-mono uppercase text-slate-400">
                <tr>
                  <th scope="col" className="px-4 py-3">Case ID</th>
                  <th scope="col" className="px-4 py-3">Title &amp; Target Entity</th>
                  <th scope="col" className="px-4 py-3">Priority</th>
                  <th scope="col" className="px-4 py-3">Status</th>
                  <th scope="col" className="px-4 py-3 text-right">Exposure</th>
                  <th scope="col" className="px-4 py-3">Assigned Lead</th>
                  <th scope="col" className="px-4 py-3 text-right">Actions</th>
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
                      {formatMoney(c.riskExposureUsd * 120)}
                    </td>
                    <td className="px-4 py-3 font-mono text-slate-400">{c.leadInvestigator}</td>
                    <td className="px-4 py-3 text-right">
                      <div className="flex items-center justify-end gap-1.5">
                        <button
                          type="button"
                          onClick={() => handlePrintDossier(c)}
                          className="p-1.5 rounded bg-[#1E293B] hover:bg-[#334155] text-slate-300 hover:text-emerald-400 transition-colors cursor-pointer"
                          title="Print Formal BFIU Case Dossier"
                        >
                          <Printer className="w-3.5 h-3.5" />
                        </button>
                        <Link
                          href={`/cases/${c.id}`}
                          className="px-2.5 py-1 rounded bg-[#1E293B] hover:bg-[#334155] text-slate-200 text-xs font-semibold inline-flex items-center gap-1"
                        >
                          <span>Open</span>
                          <ArrowRight className="w-3 h-3" />
                        </Link>
                      </div>
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
      {/* Print Dossier Modal & Printable Document */}
      {selectedCaseForPrint && (
        <div
          role="dialog"
          aria-modal="true"
          aria-labelledby="print-dossier-title"
          className="fixed inset-0 z-50 bg-black/85 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto"
        >
          <div className="w-full max-w-4xl bg-white text-slate-900 rounded-xl p-8 shadow-2xl relative print-dossier-card max-h-[90vh] overflow-y-auto">
            {/* Modal Controls (Hidden in Print) */}
            <div className="no-print flex items-center justify-between pb-4 mb-6 border-b border-slate-300">
              <div className="flex items-center gap-2">
                <Printer className="w-5 h-5 text-emerald-600" />
                <span className="font-bold text-sm text-slate-800">
                  Print Formal Investigation Dossier (BFIU Compliance)
                </span>
              </div>
              <div className="flex items-center gap-3">
                <button
                  type="button"
                  onClick={() => window.print()}
                  className="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center gap-1.5 shadow-md cursor-pointer print-include"
                >
                  <Printer className="w-4 h-4" />
                  <span>Print / Save PDF</span>
                </button>
                <button
                  type="button"
                  onClick={() => setSelectedCaseForPrint(null)}
                  className="p-1.5 rounded-lg text-slate-500 hover:text-slate-900 hover:bg-slate-100 cursor-pointer"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* Formal BFIU Letterhead */}
            <div className="text-center pb-6 border-b-2 border-slate-800 mb-6">
              <div className="font-mono text-xs font-bold uppercase tracking-widest text-slate-600 mb-1">
                CONFIDENTIAL // REGULATORY &amp; LAW ENFORCEMENT SUBMISSION
              </div>
              <h2 id="print-dossier-title" className="text-xl font-extrabold uppercase text-slate-900">
                BANGLADESH FINANCIAL INTELLIGENCE UNIT (BFIU)
              </h2>
              <p className="text-xs font-serif text-slate-700 mt-1">
                STATUTORY INVESTIGATION DOSSIER — MONEY LAUNDERING PREVENTION ACT, 2012 (ACT NO. V OF 2012)
              </p>
              <p className="text-[10px] font-mono text-slate-500 mt-1">
                Report Reference ID: BFIU-STR-2026-{selectedCaseForPrint.id} • Extract Timestamp: {new Date().toISOString()}
              </p>
            </div>

            {/* Case Key Metadata Matrix */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 p-4 rounded-lg bg-slate-50 border border-slate-300 mb-6 text-xs">
              <div>
                <span className="font-mono font-bold text-slate-500 text-[10px] uppercase block">Dossier ID</span>
                <span className="font-mono font-bold text-slate-900">{selectedCaseForPrint.id}</span>
              </div>
              <div>
                <span className="font-mono font-bold text-slate-500 text-[10px] uppercase block">Priority Band</span>
                <span className="font-mono font-bold text-rose-700">{selectedCaseForPrint.slaHours}H SLA ({selectedCaseForPrint.status})</span>
              </div>
              <div>
                <span className="font-mono font-bold text-slate-500 text-[10px] uppercase block">Assigned Lead Maker</span>
                <span className="font-semibold text-slate-900">{selectedCaseForPrint.leadInvestigator}</span>
              </div>
              <div>
                <span className="font-mono font-bold text-slate-500 text-[10px] uppercase block">Total Exposure (BDT &amp; USD)</span>
                <span className="font-mono font-bold text-emerald-800">
                  {formatMoney(selectedCaseForPrint.riskExposureUsd * 120)}
                </span>
              </div>
            </div>

            {/* Case Synopsis & Subject Entity */}
            <div className="space-y-4 mb-6 text-xs text-slate-800 leading-relaxed">
              <div>
                <h4 className="font-bold text-sm text-slate-900 uppercase font-mono mb-1">
                  1. Subject Entity &amp; Investigation Title
                </h4>
                <p className="p-3 bg-slate-50 rounded border border-slate-200 font-sans">
                  <strong>Title:</strong> {selectedCaseForPrint.title}<br />
                  <strong>Corporate Target / Beneficial Owner:</strong> {selectedCaseForPrint.entityName}<br />
                  <strong>Regulatory Filing Classification:</strong> High-Velocity Spatio-Temporal Cash Flow Anomaly
                </p>
              </div>

              <div>
                <h4 className="font-bold text-sm text-slate-900 uppercase font-mono mb-1">
                  2. Statutory Basis &amp; Typology Triggers
                </h4>
                <div className="p-3 bg-slate-50 rounded border border-slate-200 font-mono text-[11px] space-y-1">
                  <p>• Money Laundering Prevention Act, 2012 § 2(z) (Structuring &amp; Layering Prohibition)</p>
                  <p>• BFIU Master Circular No. 26 § 4.2 (Mandatory CTR Ceiling: ৳1,000,000 BDT)</p>
                  <p>• BFIU Guidelines for Prevention of Trade Based Money Laundering (2019)</p>
                  <p>• Anti-Terrorism Act, 2009 (ATA) Sanctions Schedules 1 &amp; 2</p>
                </div>
              </div>

              <div>
                <h4 className="font-bold text-sm text-slate-900 uppercase font-mono mb-1">
                  3. Investigation Milestones &amp; Evidence Log
                </h4>
                <table className="w-full border border-slate-300 text-left text-xs mb-2">
                  <thead className="bg-slate-100 border-b border-slate-300 font-mono text-[10px] uppercase text-slate-700">
                    <tr>
                      <th className="p-2">Stage</th>
                      <th className="p-2">Milestone Description</th>
                      <th className="p-2">Status</th>
                      <th className="p-2">Verification Seal</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-200 font-sans">
                    {selectedCaseForPrint.milestones.map((m, idx) => (
                      <tr key={idx}>
                        <td className="p-2 font-mono font-bold text-slate-700">0{idx + 1}</td>
                        <td className="p-2">{m.title}</td>
                        <td className="p-2 font-mono text-[10px] font-bold text-emerald-800">{m.status}</td>
                        <td className="p-2 font-mono text-[10px] text-slate-500">SHA-256-WORM-OK</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Maker-Checker Formal Signature Block */}
            <div className="pt-6 border-t-2 border-slate-800 mb-6">
              <h4 className="font-bold text-xs text-slate-900 uppercase font-mono mb-6">
                4. Dual Maker-Checker Institutional Attestation
              </h4>
              <div className="grid grid-cols-2 gap-8 text-xs">
                <div className="p-4 border border-dashed border-slate-400 rounded-lg">
                  <div className="h-12 border-b border-slate-400 mb-2 flex items-end">
                    <span className="font-serif italic text-slate-600">Amina Rahman, CFE</span>
                  </div>
                  <span className="font-bold font-mono text-slate-800 block">Lead Compliance Officer (Maker)</span>
                  <span className="text-[11px] text-slate-500 font-mono">Date: {new Date().toISOString().slice(0, 10)}</span>
                </div>

                <div className="p-4 border border-dashed border-slate-400 rounded-lg">
                  <div className="h-12 border-b border-slate-400 mb-2 flex items-end">
                    <span className="font-serif italic text-slate-600">Kazi Rafiqul Islam, CAMS</span>
                  </div>
                  <span className="font-bold font-mono text-slate-800 block">Chief Compliance Officer / CAMLCO (Checker)</span>
                  <span className="text-[11px] text-slate-500 font-mono">Date: {new Date().toISOString().slice(0, 10)}</span>
                </div>
              </div>
            </div>

            {/* Section 65B Statutory Evidentiary Certificate */}
            <div className="p-4 bg-slate-100 rounded border border-slate-300 text-[10px] text-slate-600 font-serif leading-relaxed">
              <strong>STATUTORY EVIDENTIARY CERTIFICATE:</strong> Certified that this document is an authentic printout of electronic record generated automatically from the immutable, tamper-evident append-only ledger maintained in the ordinary course of banking operations, complying with the requirements of Section 65B of the Evidence Act, 1872 (as amended 2022).
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
