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
  Eye,
  RotateCcw,
  type LucideIcon,
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';

type ModuleEntry = {
  path: string;
  label: string;
  icon: LucideIcon;
  tone: string;
  /** Extra search terms so people can type what they call it, not what we named it. */
  keywords: string[];
};

const MODULES: ModuleEntry[] = [
  { path: '/app', label: 'Executive surveillance', icon: LayoutDashboard, tone: 'text-emerald-400', keywords: ['dashboard', 'overview', 'home', 'sla'] },
  { path: '/triage', label: 'Alert triage', icon: ShieldAlert, tone: 'text-rose-400', keywords: ['alerts', 'queue', 'tier', 'review'] },
  { path: '/screening', label: 'Sanctions and PEP screening', icon: UserCheck, tone: 'text-rose-400', keywords: ['sanctions', 'pep', 'watchlist', 'ofac'] },
  { path: '/customers', label: 'Customer 360 KYC', icon: Building2, tone: 'text-cyan-400', keywords: ['kyc', 'edd', 'customer', 'dossier'] },
  { path: '/cases', label: 'Cases', icon: Briefcase, tone: 'text-amber-400', keywords: ['case', 'docket', 'investigation'] },
  { path: '/graph', label: 'Forensic cash flow', icon: GitBranch, tone: 'text-purple-400', keywords: ['graph', 'network', 'flow', 'forensic', 'hop'] },
  { path: '/tbml', label: 'Trade finance (TBML)', icon: FileSpreadsheet, tone: 'text-amber-400', keywords: ['tbml', 'trade', 'invoice', 'lc'] },
  { path: '/sar', label: 'SAR and CTR workbench', icon: FileCheck2, tone: 'text-rose-400', keywords: ['sar', 'ctr', 'str', 'filing', 'report'] },
  { path: '/rfi', label: 'Compliance RFI hub', icon: Mail, tone: 'text-blue-400', keywords: ['rfi', 'request', 'information', 'email'] },
  { path: '/rules', label: 'Rule studio', icon: Sliders, tone: 'text-teal-400', keywords: ['rules', 'shadow', 'whitelist', 'threshold'] },
  { path: '/governance', label: 'Model ops and audit ledger', icon: Scale, tone: 'text-cyan-400', keywords: ['governance', 'model', 'audit', 'ledger', 'worm', 'drift'] },
];

const ITEM =
  'flex cursor-pointer items-center gap-3 rounded-lg px-3 py-2 text-slate-200 hover:bg-[#1E293B] aria-selected:bg-[#1E293B]';
const GROUP =
  '[&_[cmdk-group-heading]]:px-3 [&_[cmdk-group-heading]]:py-1.5 [&_[cmdk-group-heading]]:text-xs [&_[cmdk-group-heading]]:font-medium [&_[cmdk-group-heading]]:text-slate-400';

export function GlobalCommandPalette() {
  const router = useRouter();
  const {
    isCommandPaletteOpen,
    setCommandPaletteOpen,
    alerts,
    customers,
    toggleStreamRunning,
    revealPii,
    resetWorkspaceData,
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
          // Ctrl/Cmd+K still toggles from inside a field; a bare "/" must not hijack typing.
          if (e.key === '/') return;
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

  const close = () => setCommandPaletteOpen(false);
  const navigateTo = (path: string) => {
    close();
    router.push(path);
  };

  if (!isCommandPaletteOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-start justify-center bg-black/70 px-4 pt-20"
      onClick={close}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-label="Command palette"
        className="w-full max-w-xl overflow-hidden rounded-xl border border-[#334155] bg-[#0F172A] text-slate-200 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <Command className="w-full bg-transparent" loop>
          <div className="flex items-center border-b border-[#1E293B] px-4">
            <Search className="mr-3 h-5 w-5 shrink-0 text-slate-400" aria-hidden />
            <Command.Input
              autoFocus
              placeholder="Search alerts, accounts, entities, or a page"
              aria-label="Search alerts, accounts, entities, or a page"
              className="h-12 w-full bg-transparent text-sm text-slate-100 placeholder:text-slate-500 focus:outline-none"
            />
            <kbd className="hidden rounded border border-[#334155] bg-[#1E293B] px-1.5 py-0.5 text-xs text-slate-400 sm:inline-block">
              Esc
            </kbd>
          </div>

          <Command.List className="max-h-96 overflow-y-auto p-2 text-sm">
            <Command.Empty className="py-8 text-center text-slate-400">
              Nothing matches that search.
            </Command.Empty>

            <Command.Group heading="Go to" className={GROUP}>
              {MODULES.map((m, i) => (
                <Command.Item
                  key={m.path}
                  value={`${m.label} ${m.path}`}
                  keywords={m.keywords}
                  onSelect={() => navigateTo(m.path)}
                  className={ITEM}
                >
                  <m.icon className={`h-4 w-4 ${m.tone}`} aria-hidden />
                  <span className="flex-1 font-medium">{m.label}</span>
                  {i < 9 && <kbd className="text-xs text-slate-500">{i + 1}</kbd>}
                </Command.Item>
              ))}
            </Command.Group>

            <Command.Group heading="Actions" className={GROUP}>
              <Command.Item
                value="Reveal personal data"
                keywords={['pii', 'unmask', 'show']}
                onSelect={() => {
                  void revealPii();
                  close();
                }}
                className={`${ITEM} !text-amber-300`}
              >
                <Eye className="h-4 w-4" aria-hidden />
                <span className="flex-1 font-medium">Reveal personal data for 60 seconds (audited)</span>
              </Command.Item>

              <Command.Item
                value="Pause or resume simulated feed"
                keywords={['stream', 'live', 'ingestion', 'toggle']}
                onSelect={() => {
                  toggleStreamRunning();
                  close();
                }}
                className={ITEM}
              >
                <Zap className="h-4 w-4 text-emerald-400" aria-hidden />
                <span className="flex-1 font-medium">Pause or resume the simulated feed</span>
              </Command.Item>

              <Command.Item
                value="Reset demo data"
                keywords={['reset', 'restore', 'clear', 'workspace']}
                onSelect={() => {
                  resetWorkspaceData();
                  close();
                }}
                className={`${ITEM} !text-rose-300`}
              >
                <RotateCcw className="h-4 w-4" aria-hidden />
                <span className="flex-1 font-medium">Reset demo data</span>
              </Command.Item>
            </Command.Group>

            <Command.Group heading="Alerts" className={GROUP}>
              {alerts.slice(0, 8).map((alert) => (
                <Command.Item
                  key={alert.id}
                  value={`${alert.id} ${alert.entityName}`}
                  onSelect={() => navigateTo(`/triage?alertId=${alert.id}`)}
                  className={ITEM}
                >
                  <ShieldAlert className="h-4 w-4 shrink-0 text-rose-400" aria-hidden />
                  <div className="flex-1 truncate">
                    <span className="font-medium text-slate-100">{alert.id}</span>
                    <span className="ml-2 text-slate-400">{alert.entityName}</span>
                  </div>
                </Command.Item>
              ))}
            </Command.Group>

            <Command.Group heading="Customers" className={GROUP}>
              {customers.map((cust) => (
                <Command.Item
                  key={cust.id}
                  value={`${cust.name} ${cust.accountNumber}`}
                  onSelect={() => navigateTo(`/customers?customerId=${cust.id}`)}
                  className={ITEM}
                >
                  <Building2 className="h-4 w-4 shrink-0 text-cyan-400" aria-hidden />
                  <div className="flex-1 truncate">
                    <span className="font-medium text-slate-100">{cust.name}</span>
                    <span className="ml-2 text-xs text-slate-400">{cust.accountNumber}</span>
                  </div>
                  <span className="rounded bg-slate-500/20 px-1.5 py-0.5 text-xs font-medium text-slate-300">
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
