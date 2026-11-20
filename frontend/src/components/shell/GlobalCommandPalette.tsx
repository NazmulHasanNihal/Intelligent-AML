'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Command } from 'cmdk';
import {
  Search,
  LayoutDashboard,
  ShieldAlert,
  FolderGit2,
  GitFork,
  FileCheck2,
  MailQuestion,
  RotateCcw,
  Scale,
  UserCheck,
  Zap,
  Lock,
  Layers,
  CheckCircle2,
  AlertTriangle
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { canExecuteAction } from '@/lib/auth/session';

export function GlobalCommandPalette() {
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const { session, density, setDensity, setFourEyesModalOpen, isLiveStreamActive, toggleLiveStream } = useBankingStore();

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
        setOpen((prev) => !prev);
      }
    };

    document.addEventListener('keydown', down);
    return () => document.removeEventListener('keydown', down);
  }, []);

  const navigateTo = (path: string) => {
    setOpen(false);
    router.push(path);
  };

  if (!open) return null;

  const isCco = canExecuteAction(session.role, 'EMERGENCY_QUARANTINE');

  return (
    <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-start justify-center pt-24 px-4 animate-in fade-in duration-150">
      <div 
        className="w-full max-w-2xl bg-[#0F172A] border border-[#334155] rounded-xl shadow-2xl overflow-hidden text-slate-200"
        onClick={(e) => e.stopPropagation()}
      >
        <Command className="w-full bg-transparent">
          <div className="flex items-center px-4 border-b border-[#1E293B]">
            <Search className="w-5 h-5 text-slate-400 mr-3 shrink-0" />
            <Command.Input
              autoFocus
              placeholder="Type a command, search account/BIC, or navigate (e.g. 'triage', 'ALT-994821', 'SAR')..."
              className="w-full h-12 bg-transparent text-sm text-slate-100 placeholder:text-slate-500 focus:outline-none font-sans"
            />
            <kbd className="hidden sm:inline-block px-1.5 py-0.5 text-[10px] font-mono font-medium text-slate-400 bg-[#1E293B] border border-[#334155] rounded">
              ESC
            </kbd>
          </div>

          <Command.List className="max-h-96 overflow-y-auto p-2 space-y-2 text-xs">
            <Command.Empty className="py-8 text-center text-slate-400">
              No matching institutional commands or records found.
            </Command.Empty>

            <Command.Group heading="Navigation (Global Jump)" className="px-2 py-1.5 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
              <Command.Item
                onSelect={() => navigateTo('/')}
                className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-slate-200 aria-selected:bg-[#1E293B]"
              >
                <LayoutDashboard className="w-4 h-4 text-emerald-400" />
                <span className="flex-1 font-medium">Surveillance Overview</span>
                <kbd className="font-mono text-[10px] text-slate-500">G 1</kbd>
              </Command.Item>

              <Command.Item
                onSelect={() => navigateTo('/triage')}
                className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-slate-200 aria-selected:bg-[#1E293B]"
              >
                <ShieldAlert className="w-4 h-4 text-amber-400" />
                <span className="flex-1 font-medium">Alert Triage Queue (CRC Risk Sets)</span>
                <kbd className="font-mono text-[10px] text-slate-500">G 2</kbd>
              </Command.Item>

              <Command.Item
                onSelect={() => navigateTo('/cases')}
                className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-slate-200 aria-selected:bg-[#1E293B]"
              >
                <FolderGit2 className="w-4 h-4 text-blue-400" />
                <span className="flex-1 font-medium">Institutional Case Management</span>
                <kbd className="font-mono text-[10px] text-slate-500">G 3</kbd>
              </Command.Item>

              <Command.Item
                onSelect={() => navigateTo('/graph')}
                className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-slate-200 aria-selected:bg-[#1E293B]"
              >
                <GitFork className="w-4 h-4 text-purple-400" />
                <span className="flex-1 font-medium">Forensic Cash Flow Studio (2D / 3D)</span>
                <kbd className="font-mono text-[10px] text-slate-500">G 4</kbd>
              </Command.Item>

              <Command.Item
                onSelect={() => navigateTo('/sar')}
                className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-slate-200 aria-selected:bg-[#1E293B]"
              >
                <FileCheck2 className="w-4 h-4 text-rose-400" />
                <span className="flex-1 font-medium">Autonomous SAR Workbench (BFIU / FinCEN / goAML)</span>
                <kbd className="font-mono text-[10px] text-slate-500">G 5</kbd>
              </Command.Item>

              <Command.Item
                onSelect={() => navigateTo('/rfi')}
                className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-slate-200 aria-selected:bg-[#1E293B]"
              >
                <MailQuestion className="w-4 h-4 text-indigo-400" />
                <span className="flex-1 font-medium">Compliance RFI Hub (Anti-Tipping-Off Safe)</span>
                <kbd className="font-mono text-[10px] text-slate-500">G 6</kbd>
              </Command.Item>

              <Command.Item
                onSelect={() => navigateTo('/recourse')}
                className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-slate-200 aria-selected:bg-[#1E293B]"
              >
                <RotateCcw className="w-4 h-4 text-teal-400" />
                <span className="flex-1 font-medium">Counterfactual Recourse & Adverse Action</span>
                <kbd className="font-mono text-[10px] text-slate-500">G 7</kbd>
              </Command.Item>

              <Command.Item
                onSelect={() => navigateTo('/governance')}
                className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-slate-200 aria-selected:bg-[#1E293B]"
              >
                <Scale className="w-4 h-4 text-cyan-400" />
                <span className="flex-1 font-medium">Model Governance, SR 11-7 & Audit Ledger</span>
                <kbd className="font-mono text-[10px] text-slate-500">G 8</kbd>
              </Command.Item>
            </Command.Group>

            <Command.Group heading="Tactical Actions" className="px-2 py-1.5 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
              <Command.Item
                onSelect={() => {
                  setDensity(density === 'compact' ? 'comfortable' : 'compact');
                  setOpen(false);
                }}
                className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-slate-200 aria-selected:bg-[#1E293B]"
              >
                <Layers className="w-4 h-4 text-slate-400" />
                <span className="flex-1">Toggle Table Density ({density === 'compact' ? 'Comfortable 44px' : 'Compact 32px'})</span>
              </Command.Item>

              <Command.Item
                onSelect={() => {
                  toggleLiveStream();
                  setOpen(false);
                }}
                className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-[#1E293B] text-slate-200 aria-selected:bg-[#1E293B]"
              >
                <Zap className="w-4 h-4 text-amber-400" />
                <span className="flex-1">{isLiveStreamActive ? 'Pause Ingestion Stream' : 'Resume Live Ingestion Stream'}</span>
              </Command.Item>

              {isCco && (
                <Command.Item
                  onSelect={() => {
                    setOpen(false);
                    setFourEyesModalOpen(true, {
                      actionType: 'EMERGENCY_QUARANTINE',
                      actionTitle: 'Emergency Global Network Quarantine Triggered',
                      targetId: 'CORRIDOR-UAE-BD-EXP',
                      details: 'Immediate circuit breaker execution for suspicious high-risk trade corridors.'
                    });
                  }}
                  className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer hover:bg-rose-950/40 text-rose-300 aria-selected:bg-rose-950/40"
                >
                  <AlertTriangle className="w-4 h-4 text-rose-500" />
                  <span className="flex-1 font-semibold">Emergency High-Risk Corridor Quarantine (4-Eyes Gate)</span>
                  <span className="px-1.5 py-0.5 text-[9px] font-mono bg-rose-500/20 text-rose-300 rounded border border-rose-500/30">CCO L3</span>
                </Command.Item>
              )}
            </Command.Group>
          </Command.List>

          <div className="px-4 py-2 bg-[#0B0F17] border-t border-[#1E293B] flex items-center justify-between text-[11px] text-slate-500">
            <div className="flex items-center gap-2">
              <span>Active Persona:</span>
              <span className="font-mono text-emerald-400 font-semibold">{session.role} ({session.userName})</span>
            </div>
            <div className="flex items-center gap-3">
              <span>Air-Gapped Intranet Node</span>
              <span className="inline-block w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
            </div>
          </div>
        </Command>
      </div>
    </div>
  );
}
