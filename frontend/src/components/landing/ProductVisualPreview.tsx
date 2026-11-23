'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import {
  ShieldAlert,
  ArrowRight,
  GitBranch,
  Layers,
  Activity,
  CheckCircle2,
  Lock,
  ChevronRight,
  Maximize2
} from 'lucide-react';

export const ProductVisualPreview: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'GRAPH' | 'TRIAGE'>('GRAPH');

  return (
    <div className="w-full max-w-6xl mx-auto rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-2xl overflow-hidden text-slate-100">
      {/* Chrome Window Header */}
      <div className="px-4 py-3 bg-[#0B0F17] border-b border-[#1E293B] flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-rose-500/80" />
          <div className="w-3 h-3 rounded-full bg-amber-500/80" />
          <div className="w-3 h-3 rounded-full bg-emerald-500/80" />
          <span className="ml-2 text-xs font-mono text-slate-400 hidden sm:inline">
            intelligent-aml-banking-os // production-preview
          </span>
        </div>

        {/* Tab Switcher */}
        <div className="flex items-center bg-[#070B12] p-0.5 rounded-lg border border-[#334155] text-[11px] font-mono">
          <button
            type="button"
            onClick={() => setActiveTab('GRAPH')}
            className={`px-2.5 py-1 rounded cursor-pointer transition-colors ${
              activeTab === 'GRAPH' ? 'bg-[#1E293B] text-emerald-400 font-bold' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Forensic Graph Studio
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('TRIAGE')}
            className={`px-2.5 py-1 rounded cursor-pointer transition-colors ${
              activeTab === 'TRIAGE' ? 'bg-[#1E293B] text-emerald-400 font-bold' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Virtualized Triage Desk
          </button>
        </div>

        <Link
          href="/app"
          className="px-3 py-1 rounded-lg text-xs font-mono font-bold bg-emerald-500 hover:bg-emerald-400 text-slate-950 transition-all flex items-center gap-1.5 cursor-pointer"
        >
          <span>Launch Live OS</span>
          <ArrowRight className="w-3 h-3" />
        </Link>
      </div>

      {/* Screen Frame */}
      {activeTab === 'GRAPH' ? (
        <div className="relative p-6 sm:p-8 bg-gradient-to-b from-[#0B0F17] to-[#070B12] min-h-[380px] flex flex-col justify-between overflow-hidden">
          {/* Subtle Grid Watermark */}
          <div className="absolute inset-0 bg-[radial-gradient(#1E293B_1px,transparent_1px)] [background-size:16px_16px] opacity-40 pointer-events-none" />

          {/* Top Bar inside Preview */}
          <div className="relative z-10 flex flex-wrap items-center justify-between gap-3 text-xs font-mono">
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/40 font-bold">
                SCENARIO: TBML OVER-INVOICING
              </span>
              <span className="text-slate-400">Root Node: BD22-EBLB-4829-1092-8823</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 rounded bg-[#1E293B] text-slate-300 border border-[#334155]">
                24 Causal Nodes
              </span>
              <span className="px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800">
                ĝ_ij Edge Gating &gt; 0.10
              </span>
            </div>
          </div>

          {/* Center Graphic Representation */}
          <div className="relative z-10 my-8 flex items-center justify-center">
            <div className="relative w-full max-w-lg h-44 flex items-center justify-center">
              {/* Outer Ring */}
              <div className="absolute inset-0 rounded-full border border-dashed border-[#334155]/60 animate-spin [animation-duration:40s]" />
              
              {/* Connecting Edges */}
              <div className="absolute w-48 h-0.5 bg-gradient-to-r from-rose-500 via-amber-500 to-cyan-500 rotate-45" />
              <div className="absolute w-48 h-0.5 bg-gradient-to-r from-emerald-500 via-cyan-500 to-indigo-500 -rotate-45" />

              {/* Central Target Node */}
              <div className="relative z-20 w-16 h-16 rounded-2xl bg-rose-950/80 border-2 border-rose-500 text-rose-300 flex flex-col items-center justify-center shadow-lg shadow-rose-950/50">
                <ShieldAlert className="w-6 h-6 animate-pulse" />
                <span className="text-[9px] font-mono font-bold mt-0.5">TARGET</span>
              </div>

              {/* Surrounding Nodes */}
              <div className="absolute -top-3 left-12 p-2 rounded-xl bg-[#0F172A] border border-[#334155] text-[10px] font-mono text-slate-300 shadow-md">
                Meghna Industrial (BD)
              </div>
              <div className="absolute -bottom-3 right-8 p-2 rounded-xl bg-[#0F172A] border border-[#334155] text-[10px] font-mono text-slate-300 shadow-md">
                Gulf Star FZE (Dubai)
              </div>
              <div className="absolute top-1/2 -right-4 -translate-y-1/2 p-2 rounded-xl bg-[#0F172A] border border-[#334155] text-[10px] font-mono text-slate-300 shadow-md">
                JAFZA Free Zone
              </div>
            </div>
          </div>

          {/* Bottom Bar inside Preview */}
          <div className="relative z-10 pt-4 border-t border-[#1E293B] flex flex-wrap items-center justify-between gap-3 text-xs font-mono text-slate-400">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
              <span>Barnes-Hut Repulsion Active</span>
            </div>
            <div className="flex items-center gap-4 text-[11px]">
              <span>Temporal Horizon: Δt = 72h</span>
              <span className="text-emerald-400 font-bold">12-D Invariant Attributions Computed</span>
            </div>
          </div>
        </div>
      ) : (
        /* Virtualized Triage Desk Preview */
        <div className="p-4 sm:p-6 bg-[#0B0F17] space-y-3 font-mono text-xs">
          <div className="flex items-center justify-between pb-3 border-b border-[#1E293B]">
            <span className="text-slate-300 font-bold">
              Queue Status: 2,028 Transactions Filtered
            </span>
            <span className="text-emerald-400 text-[11px]">
              84.2% Benign Noise Stripped Autonomously
            </span>
          </div>

          {/* Table Header */}
          <div className="grid grid-cols-12 gap-2 text-[10px] text-slate-500 uppercase px-3 py-1 bg-[#0F172A] rounded-lg">
            <span className="col-span-2">Alert ID</span>
            <span className="col-span-3">Target Entity</span>
            <span className="col-span-2 text-right">Amount (USD)</span>
            <span className="col-span-2 text-center">Conformal Set</span>
            <span className="col-span-3 text-right">Autonomous Action</span>
          </div>

          {/* Mock Rows */}
          <div className="space-y-1.5">
            <div className="grid grid-cols-12 gap-2 items-center px-3 py-2 rounded-lg bg-rose-950/20 border border-rose-800/40 text-slate-200">
              <span className="col-span-2 font-bold text-rose-400">ALT-001</span>
              <span className="col-span-3 truncate">Meghna Industrial & Agro</span>
              <span className="col-span-2 text-right font-bold text-rose-300">$945,000.00</span>
              <span className="col-span-2 text-center">
                <span className="px-1.5 py-0.5 rounded text-[10px] bg-rose-500/20 text-rose-300 border border-rose-500/40">
                  Γ = &#123;1&#125; HOLD
                </span>
              </span>
              <span className="col-span-3 text-right text-rose-400 text-[11px]">Settlement Frozen</span>
            </div>

            <div className="grid grid-cols-12 gap-2 items-center px-3 py-2 rounded-lg bg-amber-950/20 border border-amber-800/40 text-slate-200">
              <span className="col-span-2 font-bold text-amber-400">ALT-002</span>
              <span className="col-span-3 truncate">Tanvir MFS Merchant Hub</span>
              <span className="col-span-2 text-right font-bold text-amber-300">$7,950.00</span>
              <span className="col-span-2 text-center">
                <span className="px-1.5 py-0.5 rounded text-[10px] bg-amber-500/20 text-amber-300 border border-amber-500/40">
                  Γ = &#123;0, 1&#125; REVIEW
                </span>
              </span>
              <span className="col-span-3 text-right text-amber-400 text-[11px]">Analyst Docket</span>
            </div>

            <div className="grid grid-cols-12 gap-2 items-center px-3 py-2 rounded-lg bg-emerald-950/20 border border-emerald-800/40 text-slate-200">
              <span className="col-span-2 font-bold text-emerald-400">ALT-003</span>
              <span className="col-span-3 truncate">Apex Footwear Payroll</span>
              <span className="col-span-2 text-right font-bold text-emerald-300">$218,400.00</span>
              <span className="col-span-2 text-center">
                <span className="px-1.5 py-0.5 rounded text-[10px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                  Γ = &#123;0&#125; CLEAR
                </span>
              </span>
              <span className="col-span-3 text-right text-emerald-400 text-[11px]">Instant STP Clearance</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
