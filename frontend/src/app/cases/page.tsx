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
  GitFork
} from 'lucide-react';
import { SEEDED_CASES } from '@/lib/seedData';
import { PiiText } from '@/components/ui/PiiText';

export default function CasesPage() {
  const [statusFilter, setStatusFilter] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');

  const filteredCases = SEEDED_CASES.filter((c) => {
    const matchesStatus = statusFilter === 'ALL' || c.status === statusFilter;
    const matchesSearch =
      searchQuery === '' ||
      c.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.subjectEntity.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.assignedTo.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesStatus && matchesSearch;
  });

  return (
    <div className="p-6 max-w-[1700px] mx-auto space-y-6">
      {/* Page Title & Controls */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <FolderGit2 className="w-5 h-5 text-blue-400" />
            Institutional Case Management
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            WORM-audited investigation dossiers with cryptographic evidence preservation complying with FRE 902(11).
          </p>
        </div>

        <button
          onClick={() => alert('Opening new case dossier wizard...')}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold text-xs uppercase tracking-wide transition-all shadow-md"
        >
          <Plus className="w-4 h-4" />
          <span>Open New Case Dossier</span>
        </button>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-2 border-b border-[#1E293B]">
        <div className="flex items-center gap-2">
          {['ALL', 'INVESTIGATION_OPEN', 'SAR_DRAFTED', 'PENDING_FOUR_EYES', 'CLOSED'].map((st) => (
            <button
              key={st}
              onClick={() => setStatusFilter(st)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                statusFilter === st
                  ? 'bg-[#1E293B] text-slate-100 border border-[#334155]'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-[#0F172A]'
              }`}
            >
              {st === 'ALL' ? 'All Cases' : st.replace(/_/g, ' ')}
            </button>
          ))}
        </div>

        <div className="relative min-w-[280px]">
          <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-500" />
          <input
            type="text"
            placeholder="Search by Case ID, Subject, Assignee..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 bg-[#0F172A] border border-[#334155] rounded-lg text-xs text-slate-100 placeholder:text-slate-500 focus:outline-none focus:border-emerald-500"
          />
        </div>
      </div>

      {/* Cases Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {filteredCases.map((c) => (
          <div
            key={c.id}
            className="p-5 bg-[#0F172A] border border-[#1E293B] rounded-xl hover:border-[#334155] transition-all flex flex-col justify-between"
          >
            <div>
              {/* Header */}
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-slate-300 bg-[#0B0F17] px-2 py-0.5 rounded border border-[#1E293B]">
                  {c.id}
                </span>
                <span
                  className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
                    c.status === 'PENDING_FOUR_EYES'
                      ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                      : c.status === 'SAR_DRAFTED'
                      ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                      : 'bg-blue-500/20 text-blue-300 border border-blue-500/30'
                  }`}
                >
                  {c.status.replace(/_/g, ' ')}
                </span>
              </div>

              {/* Title & Subject */}
              <h3 className="text-sm font-semibold text-slate-100 mt-3 line-clamp-1">
                {c.title}
              </h3>
              <div className="flex items-center gap-2 text-xs text-slate-400 mt-1">
                <Building className="w-3.5 h-3.5 text-slate-500" />
                <span className="font-medium text-slate-300">{c.subjectEntity}</span>
              </div>

              {/* Financial Exposure */}
              <div className="mt-4 p-3 bg-[#0B0F17] rounded-lg border border-[#1E293B] flex items-center justify-between text-xs">
                <div>
                  <span className="text-[10px] text-slate-500 block uppercase">Total Exposure</span>
                  <span className="font-mono font-bold text-rose-400 text-sm">
                    ${c.totalExposure.toLocaleString(undefined, { minimumFractionDigits: 2 })}
                  </span>
                </div>
                <div className="text-right">
                  <span className="text-[10px] text-slate-500 block uppercase">Risk Tier</span>
                  <span className="font-mono font-bold text-amber-300 text-xs">
                    {c.tier}
                  </span>
                </div>
              </div>

              {/* Milestone Progress Indicator */}
              <div className="mt-4">
                <div className="flex items-center justify-between text-[11px] text-slate-400 mb-1">
                  <span>Investigation Milestones</span>
                  <span className="font-mono">{(c.milestones?.length || 4)} / 6 Complete</span>
                </div>
                <div className="w-full bg-[#1E293B] h-1.5 rounded-full overflow-hidden">
                  <div
                    className="bg-emerald-500 h-full rounded-full transition-all duration-300"
                    style={{ width: `${((c.milestones?.length || 4) / 6) * 100}%` }}
                  />
                </div>
              </div>
            </div>

            {/* Footer with Assignee and Link */}
            <div className="mt-5 pt-3 border-t border-[#1E293B] flex items-center justify-between text-xs">
              <div className="flex items-center gap-1.5 text-slate-400 text-[11px]">
                <User className="w-3.5 h-3.5 text-slate-500" />
                <span>{c.assignedTo}</span>
              </div>

              <Link
                href={`/cases/${c.id}`}
                className="flex items-center gap-1 text-emerald-400 hover:text-emerald-300 font-semibold"
              >
                <span>Open Dossier</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
