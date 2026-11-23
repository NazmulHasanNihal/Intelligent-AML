'use client';

import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Command } from 'cmdk';
import {
  Search,
  LayoutDashboard,
  ShieldAlert,
  UserCheck,
  Building2,
  Briefcase,
  GitBranch,
  FileSpreadsheet,
  FileCheck2,
  Mail,
  Sliders,
  Scale,
  Zap,
  Lock,
  Eye,
  RotateCcw,
  Globe
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';

export function GlobalCommandPalette() {
  const router = useRouter();
  const {
    isCommandPaletteOpen,
    setCommandPaletteOpen,
    alerts,
    cases,
    customers,
    toggleStreamRunning,
    revealPii,
    resetWorkspaceData,
    setActiveJurisdiction
  } = useBankingStore();

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if ((e.key === 'k' && (e.metaKey || e.ctrlKey)) || e.key === '/') {
        if (
          (e.target instanceof HTMLElement && e.target.isContentEditable) ||
          e.target instanceof HTMLInputElement ||
          e.target instanceof HTMLTextAreaElement ||
          e.target instanceof HTMLSelectElement
        ) {
          return;
        }
        e.preventDefault();
        setCommandPaletteOpen(!isCommandPaletteOpen);
      }
      if (e.key === 'Escape' && isCommandPaletteOpen) {
        setCommandPaletteOpen(false);
      }
    };

    document.addEventListener('keydown', down);
    return () => document.removeEventListener('keydown', down);
  }, [isCommandPaletteOpen, setCommandPaletteOpen]);

  const navigateTo = (path: string) => {
    setCommandPaletteOpen(false);
    router.push(path);
  };

  if (!isCommandPaletteOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 bg-black/75 backdrop-blur-xs flex items-start justify-center pt-20 px-4 animate-in fade-in duration-150"
      onClick={() => setCommandPaletteOpen(false)}
    >
      <div 
        className="w-full max-w-2xl bg-[#0F172A] border border-[#334155] rounded-xl shadow-2xl overflow-hidden text-slate-200"
        onClick={(e) => e.stopPropagation()}
      >
        <Command className="w-full bg-transparent">
          <div className="flex items-center px-4 border-b border-[#1E293B]">
            <Search className="w-5 h-5 text-slate-400 mr-3 shrink-0" />
            <Command.Input
              autoFocus
              placeholder="Search alerts (ALT-994821), cases, accounts (BD22...), or type module..."
              className="w-full h-12 bg-transparent text-sm text-slate-100 placeholder:text-slate-500 focus:outline-none font-sans"
            />
            <kbd className="hidden sm:inline-block px-1.5 py-0.5 text-[10px] font-mono font-medium text-slate-400 bg-[#1E293B] border border-[#334155] rounded">
              ESC
            </kbd>
          </div>

          <Command.List className="max-h-96 overflow-y-auto p-2 space-y-2 text-xs">
            <Command.Empty className="py-8 text-center text-slate-400 font-mono">
              No matching institutional commands or customer records found.
            </Command.Empty>

            {/* Global Jump Navigation */}
            <Command.Group heading="11 Compliance Modules (Jump)" className="px-2 py-1.5 text-[11px] font-semibold text-slate-400 uppercase tracking-wider font-mono">
              <Command.Item
                onSelect={() => navigateTo('/')}
                className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-slate-200 aria-selected:bg-[#1E293B]"
              >
                <LayoutDashboard className="w-4 h-4 text-emerald-400" />
                <span className="flex-1 font-medium font-sans">1. Executive Surveillance & SLA Overview</span>
                <kbd className="font-mono text-[10px] text-slate-500">1</kbd>
              </Command.Item>

              <Command.Item
                onSelect={() => navigateTo('/triage')}
                className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-slate-200 aria-selected:bg-[#1E293B]"
              >
                <ShieldAlert className="w-4 h-4 text-rose-400" />
                <span className="flex-1 font-medium font-sans">2. Alert Triage Queue (2,028 Rows)</span>
                <kbd className="font-mono text-[10px] text-slate-500">2</kbd>
              </Command.Item>

              <Command.Item
                onSelect={() => navigateTo('/screening')}
                className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-slate-200 aria-selected:bg-[#1E293B]"
              >
                <UserCheck className="w-4 h-4 text-rose-400" />
                <span className="flex-1 font-medium font-sans">3. Sanctions, PEP & Pre-Settlement Screening</span>
                <kbd className="font-mono text-[10px] text-slate-500">3</kbd>
              </Command.Item>

              <Command.Item
                onSelect={() => navigateTo('/customers')}
                className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-slate-200 aria-selected:bg-[#1E293B]"
              >
                <Building2 className="w-4 h-4 text-cyan-400" />
                <span className="flex-1 font-medium font-sans">4. Customer 360° KYC/EDD Dossier</span>
                <kbd className="font-mono text-[10px] text-slate-500">4</kbd>
              </Command.Item>

              <Command.Item
                onSelect={() => navigateTo('/cases')}
                className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-slate-200 aria-selected:bg-[#1E293B]"
              >
                <Briefcase className="w-4 h-4 text-amber-400" />
                <span className="flex-1 font-medium font-sans">5. Institutional Cases Docket</span>
                <kbd className="font-mono text-[10px] text-slate-500">5</kbd>
              </Command.Item>

              <Command.Item
                onSelect={() => navigateTo('/graph')}
                className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-slate-200 aria-selected:bg-[#1E293B]"
              >
                <GitBranch className="w-4 h-4 text-purple-400" />
                <span className="flex-1 font-medium font-sans">6. Forensic Cash Flow Studio (2D/3D)</span>
                <kbd className="font-mono text-[10px] text-slate-500">6</kbd>
              </Command.Item>

              <Command.Item
                onSelect={() => navigateTo('/tbml')}
                className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-slate-200 aria-selected:bg-[#1E293B]"
              >
                <FileSpreadsheet className="w-4 h-4 text-amber-400" />
                <span className="flex-1 font-medium font-sans">7. Trade Finance TBML Workspace</span>
                <kbd className="font-mono text-[10px] text-slate-500">7</kbd>
              </Command.Item>

              <Command.Item
                onSelect={() => navigateTo('/sar')}
                className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-slate-200 aria-selected:bg-[#1E293B]"
              >
                <FileCheck2 className="w-4 h-4 text-rose-400" />
                <span className="flex-1 font-medium font-sans">8. SAR Filings Studio & CTR Aggregator</span>
                <kbd className="font-mono text-[10px] text-slate-500">8</kbd>
              </Command.Item>

              <Command.Item
                onSelect={() => navigateTo('/rfi')}
                className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-slate-200 aria-selected:bg-[#1E293B]"
              >
                <Mail className="w-4 h-4 text-blue-400" />
                <span className="flex-1 font-medium font-sans">9. Compliance RFI Hub (Anti-Tipping Guard)</span>
                <kbd className="font-mono text-[10px] text-slate-500">9</kbd>
              </Command.Item>

              <Command.Item
                onSelect={() => navigateTo('/rules')}
                className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-slate-200 aria-selected:bg-[#1E293B]"
              >
                <Sliders className="w-4 h-4 text-teal-400" />
                <span className="flex-1 font-medium font-sans">10. Rule Studio Shadow Mode & Whitelisting</span>
                <kbd className="font-mono text-[10px] text-slate-500">0</kbd>
              </Command.Item>

              <Command.Item
                onSelect={() => navigateTo('/governance')}
                className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-slate-200 aria-selected:bg-[#1E293B]"
              >
                <Scale className="w-4 h-4 text-cyan-400" />
                <span className="flex-1 font-medium font-sans">11. Model Ops & WORM Audit Ledger</span>
                <kbd className="font-mono text-[10px] text-slate-500">G</kbd>
              </Command.Item>
            </Command.Group>

            {/* Quick Actions */}
            <Command.Group heading="Executive Quick Actions" className="px-2 py-1.5 text-[11px] font-semibold text-slate-400 uppercase tracking-wider font-mono">
              <Command.Item
                onSelect={() => {
                  revealPii();
                  setCommandPaletteOpen(false);
                }}
                className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-amber-300 aria-selected:bg-[#1E293B]"
              >
                <Eye className="w-4 h-4" />
                <span className="flex-1 font-medium font-sans">Reveal PII Globally for 60 Seconds (Audited)</span>
              </Command.Item>

              <Command.Item
                onSelect={() => {
                  toggleStreamRunning();
                  setCommandPaletteOpen(false);
                }}
                className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-slate-200 aria-selected:bg-[#1E293B]"
              >
                <Zap className="w-4 h-4 text-emerald-400" />
                <span className="flex-1 font-medium font-sans">Toggle Real-Time Ingestion Stream (Live/Paused)</span>
              </Command.Item>

              <Command.Item
                onSelect={() => {
                  resetWorkspaceData();
                  setCommandPaletteOpen(false);
                }}
                className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-rose-300 aria-selected:bg-[#1E293B]"
              >
                <RotateCcw className="w-4 h-4" />
                <span className="flex-1 font-medium font-sans">Reset Workspace Data to Pristine Certified State</span>
              </Command.Item>
            </Command.Group>

            {/* Active Alerts Match */}
            <Command.Group heading="Priority Alerts" className="px-2 py-1.5 text-[11px] font-semibold text-slate-400 uppercase tracking-wider font-mono">
              {alerts.slice(0, 4).map(alert => (
                <Command.Item
                  key={alert.id}
                  onSelect={() => navigateTo(`/triage?alertId=${alert.id}`)}
                  className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-slate-200 aria-selected:bg-[#1E293B]"
                >
                  <ShieldAlert className="w-4 h-4 text-rose-400 shrink-0" />
                  <div className="flex-1 truncate">
                    <span className="font-mono font-bold text-slate-100">{alert.id}</span>
                    <span className="text-slate-400 ml-2 truncate">{alert.entityName}</span>
                  </div>
                  <span className="font-mono font-bold text-rose-400 shrink-0">
                    ${alert.amount.toLocaleString()}
                  </span>
                </Command.Item>
              ))}
            </Command.Group>

            {/* Active Customers */}
            <Command.Group heading="Customer Directory" className="px-2 py-1.5 text-[11px] font-semibold text-slate-400 uppercase tracking-wider font-mono">
              {customers.map(cust => (
                <Command.Item
                  key={cust.id}
                  onSelect={() => navigateTo(`/customers?customerId=${cust.id}`)}
                  className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-slate-200 aria-selected:bg-[#1E293B]"
                >
                  <Building2 className="w-4 h-4 text-cyan-400 shrink-0" />
                  <div className="flex-1 truncate">
                    <span className="font-bold text-slate-100">{cust.name}</span>
                    <span className="text-slate-400 font-mono text-[10px] ml-2">{cust.accountNumber}</span>
                  </div>
                  <span className="px-1.5 py-0.2 rounded text-[9px] font-bold font-mono bg-rose-500/20 text-rose-300">
                    {cust.riskRating}
                  </span>
                </Command.Item>
              ))}
            </Command.Group>
          </Command.List>
        </Command>
      </div>
    </div>
  );
}
