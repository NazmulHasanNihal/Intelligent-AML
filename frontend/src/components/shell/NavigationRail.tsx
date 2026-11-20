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
  icon: React.ElementType;
  badge?: string | number;
  badgeColor?: 'crimson' | 'amber' | 'neutral';
  shortcut: string;
}

const NAV_ITEMS: NavItem[] = [
  { href: '/', label: 'Overview', icon: LayoutDashboard, shortcut: '1' },
  { href: '/triage', label: 'Alert Triage', icon: ShieldAlert, badge: '1,280', badgeColor: 'crimson', shortcut: '2' },
  { href: '/cases', label: 'Cases Docket', icon: Briefcase, badge: '4', badgeColor: 'amber', shortcut: '3' },
  { href: '/graph', label: 'Cash Flow Graph', icon: GitBranch, shortcut: '4' },
  { href: '/sar', label: 'SAR Workbench', icon: FileCheck2, badge: '2', badgeColor: 'crimson', shortcut: '5' },
  { href: '/rfi', label: 'Compliance RFI', icon: Mail, badge: '5', badgeColor: 'neutral', shortcut: '6' },
  { href: '/recourse', label: 'What-If Recourse', icon: Sliders, shortcut: '7' },
  { href: '/governance', label: 'Governance & WORM', icon: Scale, shortcut: '8' },
];

export const NavigationRail: React.FC = () => {
  const pathname = usePathname();
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <aside
      className={`border-r border-panel-border bg-panel flex flex-col justify-between transition-all duration-200 select-none z-20 shrink-0 ${
        isCollapsed ? 'w-16' : 'w-60'
      }`}
    >
      {/* Top: Brand Header */}
      <div>
        <div className="h-14 px-4 flex items-center justify-between border-b border-panel-border">
          {!isCollapsed && (
            <div className="flex items-center gap-2">
              <span className="text-sm font-bold tracking-tight text-text-primary">
                AML Operating System
              </span>
            </div>
          )}
          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="p-1.5 rounded hover:bg-panel-raised text-text-muted hover:text-text-primary transition-colors cursor-pointer mx-auto"
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
                    ? 'bg-brand-accent/15 text-brand-accent font-bold border border-brand-accent/30 shadow-xs'
                    : 'text-text-secondary hover:text-text-primary hover:bg-panel-raised'
                }`}
                title={`${item.label} (Hotkey: G then ${item.shortcut})`}
              >
                <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-brand-accent' : 'text-text-dim group-hover:text-text-primary'}`} />
                {!isCollapsed && (
                  <div className="flex-1 flex items-center justify-between overflow-hidden">
                    <span className="truncate">{item.label}</span>
                    <div className="flex items-center gap-1.5 shrink-0">
                      {item.badge && (
                        <span
                          className={`px-1.5 py-0.2 rounded text-[10px] font-bold ${
                            item.badgeColor === 'crimson'
                              ? 'bg-tier1-crimson-bg text-tier1-crimson border border-tier1-crimson-border'
                              : item.badgeColor === 'amber'
                              ? 'bg-tier2-amber-bg text-tier2-amber border border-tier2-amber-border'
                              : 'bg-panel-raised text-text-dim border border-panel-border'
                          }`}
                        >
                          {item.badge}
                        </span>
                      )}
                      <kbd className="text-[9px] text-text-dim/60 font-mono hidden group-hover:inline">
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
      <div className="p-3 border-t border-panel-border">
        {!isCollapsed ? (
          <div className="p-2.5 rounded-lg bg-panel-raised border border-panel-border text-[11px] font-mono space-y-1">
            <div className="flex items-center gap-1.5 text-tier3-emerald font-bold">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>FRE 902(11) Certified</span>
            </div>
            <p className="text-[10px] text-text-dim leading-tight">
              Cryptographic WORM Audit Trail Active. Dual Control Enforced.
            </p>
          </div>
        ) : (
          <div className="flex justify-center" title="FRE 902(11) Certified WORM Audit Trail">
            <ShieldCheck className="w-4 h-4 text-tier3-emerald" />
          </div>
        )}
      </div>
    </aside>
  );
};
