'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  ShieldAlert,
  Briefcase,
  GitBranch,
  FileCheck2,
  Mail,
  Sliders,
  Scale,
  ChevronLeft,
  ChevronRight,
  ShieldCheck,
  Lock,
  UserCheck
} from 'lucide-react';

interface NavItem {
  href: string;
  label: string;
  shortLabel: string;
  icon: React.ElementType;
  badge?: string | number;
  badgeColor?: 'crimson' | 'amber' | 'neutral';
  shortcut: string;
}

const NAV_ITEMS: NavItem[] = [
  { href: '/', label: 'Overview', shortLabel: 'Overview', icon: LayoutDashboard, shortcut: '1' },
  { href: '/triage', label: 'Alert Triage', shortLabel: 'Triage', icon: ShieldAlert, badge: '1,280', badgeColor: 'crimson', shortcut: '2' },
  { href: '/cases', label: 'Cases Docket', shortLabel: 'Cases', icon: Briefcase, badge: '4', badgeColor: 'amber', shortcut: '3' },
  { href: '/graph', label: 'Cash Flow Graph', shortLabel: 'Graph', icon: GitBranch, shortcut: '4' },
  { href: '/sar', label: 'SAR Workbench', shortLabel: 'SAR', icon: FileCheck2, badge: '2', badgeColor: 'crimson', shortcut: '5' },
  { href: '/rfi', label: 'Compliance RFI', shortLabel: 'RFI', icon: Mail, badge: '5', badgeColor: 'neutral', shortcut: '6' },
  { href: '/recourse', label: 'What-If Recourse', shortLabel: 'Recourse', icon: Sliders, shortcut: '7' },
  { href: '/governance', label: 'Governance & WORM', shortLabel: 'Governance', icon: Scale, shortcut: '8' },
];

export const NavigationRail: React.FC = () => {
  const pathname = usePathname();
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <>
      {/* Desktop & Laptop Collapsible Sidebar */}
      <aside
        className={`border-r border-[#1E293B] bg-[#0F172A] hidden md:flex flex-col justify-between transition-all duration-200 select-none z-20 shrink-0 ${
          isCollapsed ? 'w-16' : 'w-60'
        }`}
      >
        {/* Top: Section Header & Collapse Toggle */}
        <div>
          <div className="h-10 px-3 flex items-center justify-between border-b border-[#1E293B]">
            {!isCollapsed && (
              <span className="text-[11px] font-mono font-bold uppercase tracking-wider text-slate-400">
                Navigation Rail
              </span>
            )}
            <button
              onClick={() => setIsCollapsed(!isCollapsed)}
              className="p-1 rounded hover:bg-[#1E293B] text-slate-400 hover:text-slate-200 transition-colors cursor-pointer ml-auto"
              title={isCollapsed ? "Expand Navigation Rail" : "Collapse Navigation Rail"}
            >
              {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
            </button>
          </div>

          {/* Nav Links */}
          <nav className="p-2 space-y-1">
            {NAV_ITEMS.map((item) => {
              const isActive = pathname === item.href || (item.href !== '/' && pathname.startsWith(item.href));
              const Icon = item.icon;

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-mono font-medium transition-all group ${
                    isActive
                      ? 'bg-emerald-500/15 text-emerald-400 font-bold border border-emerald-500/30 shadow-xs'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-[#1E293B]'
                  }`}
                  title={`${item.label} (Hotkey: G then ${item.shortcut})`}
                >
                  <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-emerald-400' : 'text-slate-500 group-hover:text-slate-200'}`} />
                  {!isCollapsed && (
                    <div className="flex-1 flex items-center justify-between overflow-hidden">
                      <span className="truncate">{item.label}</span>
                      <div className="flex items-center gap-1.5 shrink-0">
                        {item.badge && (
                          <span
                            className={`px-1.5 py-0.2 rounded text-[10px] font-bold tabular-nums ${
                              item.badgeColor === 'crimson'
                                ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
                                : item.badgeColor === 'amber'
                                ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40'
                                : 'bg-[#1E293B] text-slate-400 border border-[#334155]'
                            }`}
                          >
                            {item.badge}
                          </span>
                        )}
                        <kbd className="text-[9px] text-slate-600 font-mono hidden group-hover:inline">
                          G{item.shortcut}
                        </kbd>
                      </div>
                    </div>
                  )}
                </Link>
              );
            })}
          </nav>
        </div>

        {/* Bottom: Institutional Security Shield */}
        <div className="p-3 border-t border-[#1E293B]">
          {!isCollapsed ? (
            <div className="p-2.5 rounded-lg bg-[#0B0F17] border border-[#1E293B] text-[11px] font-mono space-y-1">
              <div className="flex items-center gap-1.5 text-emerald-400 font-bold">
                <ShieldCheck className="w-3.5 h-3.5 shrink-0" />
                <span>FRE 902(11) Certified</span>
              </div>
              <p className="text-[10px] text-slate-400 leading-tight">
                Cryptographic WORM Audit Trail Active. Dual Control Enforced.
              </p>
            </div>
          ) : (
            <div className="flex justify-center" title="FRE 902(11) Certified WORM Audit Trail">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
            </div>
          )}
        </div>
      </aside>

      {/* Mobile Bottom Navigation Bar (Visible only on < md) */}
      <nav className="flex md:hidden fixed bottom-0 left-0 right-0 h-14 bg-[#0F172A]/95 backdrop-blur-md border-t border-[#1E293B] z-30 px-1 justify-around items-center">
        {NAV_ITEMS.slice(0, 5).map((item) => {
          const isActive = pathname === item.href || (item.href !== '/' && pathname.startsWith(item.href));
          const Icon = item.icon;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex flex-col items-center justify-center py-1 px-2 rounded text-[10px] font-mono transition-colors ${
                isActive ? 'text-emerald-400 font-bold' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Icon className="w-4 h-4 mb-0.5" />
              <span className="truncate max-w-[56px] text-center">{item.shortLabel}</span>
            </Link>
          );
        })}
      </nav>
    </>
  );
};
