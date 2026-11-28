'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import {
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
  ChevronLeft,
  ChevronRight,
  RotateCcw
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';
import { TRANSLATIONS } from '@/lib/i18n/translations';

type NavKey = 'overview' | 'triage' | 'screening' | 'customers' | 'cases' | 'graph' | 'tbml' | 'sar' | 'rfi' | 'rules' | 'governance';

interface NavItem {
  href: string;
  key: NavKey;
  label: string;
  shortLabel: string;
  icon: React.ElementType;
  badge?: number | string;
  badgeColor?: 'crimson' | 'amber' | 'neutral' | 'emerald';
  shortcut: string;
}

export const NavigationRail: React.FC = () => {
  const pathname = usePathname();
  const router = useRouter();
  const [isCollapsed, setIsCollapsed] = useState(false);
  const { alerts, cases, screeningRecords, resetWorkspaceData, language } = useBankingStore();
  const dict = TRANSLATIONS[language] as Record<string, string>;
  const navLabel = (item: NavItem) => dict[`nav_${item.key}`] ?? item.label;
  const shortLabel = (item: NavItem) => dict[`short_${item.key}`] ?? item.shortLabel;

  const tier1Count = alerts.filter(a => a.tierCode === 1 && a.status !== 'FALSE_POSITIVE_DISMISSED').length;
  const pendingScreening = screeningRecords.filter(r => r.disposition === 'PENDING_REVIEW').length;
  const openCases = cases.filter(c => c.status === 'INVESTIGATION_OPEN').length;

  const NAV_ITEMS: NavItem[] = [
    { href: '/app', key: 'overview', label: '1. Executive Surveillance', shortLabel: 'Overview', icon: LayoutDashboard, shortcut: '1' },
    { href: '/app/triage', key: 'triage', label: '2. Alert Triage', shortLabel: 'Triage', icon: ShieldAlert, badge: tier1Count, badgeColor: 'crimson', shortcut: '2' },
    { href: '/app/screening', key: 'screening', label: '3. Sanctions & PEP', shortLabel: 'Screening', icon: UserCheck, badge: pendingScreening, badgeColor: 'crimson', shortcut: '3' },
    { href: '/app/customers', key: 'customers', label: '4. Customer 360° KYC', shortLabel: 'Customers', icon: Building2, shortcut: '4' },
    { href: '/app/cases', key: 'cases', label: '5. Institutional Cases', shortLabel: 'Cases', icon: Briefcase, badge: openCases, badgeColor: 'amber', shortcut: '5' },
    { href: '/app/graph', key: 'graph', label: '6. Forensic Cash Flow', shortLabel: 'Graph', icon: GitBranch, shortcut: '6' },
    { href: '/app/tbml', key: 'tbml', label: '7. Trade Finance TBML', shortLabel: 'TBML', icon: FileSpreadsheet, badge: '1', badgeColor: 'amber', shortcut: '7' },
    { href: '/app/sar', key: 'sar', label: '8. SAR & CTR Workbench', shortLabel: 'SAR/CTR', icon: FileCheck2, badge: '2', badgeColor: 'crimson', shortcut: '8' },
    { href: '/app/rfi', key: 'rfi', label: '9. Compliance RFI Hub', shortLabel: 'RFI', icon: Mail, badge: '3', badgeColor: 'neutral', shortcut: '9' },
    { href: '/app/rules', key: 'rules', label: '10. Rule Studio & Recourse', shortLabel: 'Rules', icon: Sliders, shortcut: '0' },
    { href: '/app/governance', key: 'governance', label: '11. Model Ops & WORM', shortLabel: 'Governance', icon: Scale, shortcut: '' },
  ];

  // Number keys jump between modules (1-9, 0). Ignored while typing or with a modifier held.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      const t = e.target;
      if (
        t instanceof HTMLInputElement ||
        t instanceof HTMLTextAreaElement ||
        t instanceof HTMLSelectElement ||
        (t instanceof HTMLElement && t.isContentEditable)
      ) {
        return;
      }
      const hit = NAV_ITEMS.find((n) => n.shortcut && n.shortcut === e.key);
      if (hit && pathname !== hit.href) {
        e.preventDefault();
        router.push(hit.href);
      }
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pathname, router]);

  return (
    <>
      {/* Desktop & Laptop Collapsible Sidebar */}
      <aside
        className={`border-r border-[#1E293B] bg-[#0F172A] hidden md:flex flex-col justify-between transition-all duration-200 select-none z-20 shrink-0 ${
          isCollapsed ? 'w-16' : 'w-64'
        }`}
      >
        {/* Top: Section Header & Collapse Toggle */}
        <div className="overflow-y-auto">
          <div className="h-10 px-3 flex items-center justify-between border-b border-[#1E293B]">
            {!isCollapsed && (
              <span className="text-xs font-mono font-bold text-slate-400">
                {language === 'bn' ? '১১টি মডিউল' : '11 modules'}
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
          <nav className="p-2 space-y-0.5">
            {NAV_ITEMS.map((item) => {
              const strippedItemHref = item.href.replace('/app', '') || '/app';
              const isActive = pathname === item.href || 
                (strippedItemHref !== '/app' && (pathname === strippedItemHref || pathname.startsWith(strippedItemHref))) ||
                (item.href !== '/app' && pathname.startsWith(item.href));
              const Icon = item.icon;

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center gap-2.5 px-2.5 py-1.5 rounded-lg text-xs font-mono font-medium transition-all group ${
                    isActive
                      ? 'bg-emerald-500/15 text-emerald-400 font-bold border border-emerald-500/30 shadow-xs'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-[#1E293B]'
                  }`}
                  title={navLabel(item)}
                >
                  <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-emerald-400' : 'text-slate-500 group-hover:text-slate-200'}`} />
                  {!isCollapsed && (
                    <div className="flex-1 flex items-center justify-between overflow-hidden">
                      <span className="truncate">{navLabel(item)}</span>
                      <div className="flex items-center gap-1.5 shrink-0">
                        {item.badge !== undefined && item.badge !== 0 && (
                          <span
                            className={`px-1.5 py-0.2 rounded text-xs font-bold tabular-nums ${
                              item.badgeColor === 'crimson'
                                ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
                                : item.badgeColor === 'amber'
                                ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40'
                                : 'bg-slate-700/40 text-slate-300 border border-slate-600/40'
                            }`}
                          >
                            {typeof item.badge === 'number' ? item.badge.toLocaleString() : item.badge}
                          </span>
                        )}
                        {item.shortcut && <kbd className="hidden lg:inline-block px-1 py-0.2 text-xs font-mono text-slate-500 bg-[#0B0F17] rounded border border-[#334155]">
                          {item.shortcut}
                        </kbd>}
                      </div>
                    </div>
                  )}
                </Link>
              );
            })}
          </nav>
        </div>

        {/* Bottom Actions: Reset Workspace Data */}
        <div className="p-2 border-t border-[#1E293B] bg-[#0B0F17]/80">
          <button
            type="button"
            onClick={resetWorkspaceData}
            className="w-full flex items-center gap-2 px-2.5 py-1.5 rounded-lg text-xs font-mono font-medium text-slate-400 hover:text-rose-300 hover:bg-rose-950/30 border border-transparent hover:border-rose-800/40 transition-all cursor-pointer"
            title="Reset Workspace to Certified Clean Demo State"
          >
            <RotateCcw className="w-3.5 h-3.5 text-slate-500 shrink-0" />
            {!isCollapsed && <span>Reset Workspace Data</span>}
          </button>
        </div>
      </aside>

      {/* Mobile Bottom Fixed Nav Bar (< 768px) */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 h-14 bg-[#0F172A] border-t border-[#1E293B] flex items-center justify-around z-30 px-2 select-none">
        {NAV_ITEMS.slice(0, 5).map((item) => {
          const strippedItemHref = item.href.replace('/app', '') || '/app';
          const isActive = pathname === item.href || (strippedItemHref !== '/app' && pathname === strippedItemHref);
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex flex-col items-center justify-center p-1 rounded transition-colors ${
                isActive ? 'text-emerald-400 font-bold' : 'text-slate-400'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span className="text-xs font-mono mt-0.5">{shortLabel(item)}</span>
            </Link>
          );
        })}
      </div>
    </>
  );
};
