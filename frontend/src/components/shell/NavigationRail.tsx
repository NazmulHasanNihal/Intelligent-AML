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
  RotateCcw,
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

  const tier1Count = alerts.filter((a) => a.tierCode === 1 && a.status !== 'FALSE_POSITIVE_DISMISSED').length;
  const pendingScreening = screeningRecords.filter((r) => r.disposition === 'PENDING_REVIEW').length;
  const openCases = cases.filter((c) => c.status === 'INVESTIGATION_OPEN').length;

  const NAV_ITEMS: NavItem[] = [
    { href: '/app', key: 'overview', label: '1. Executive Surveillance', shortLabel: 'Overview', icon: LayoutDashboard, shortcut: '1' },
    { href: '/app/triage', key: 'triage', label: '2. Alert Triage', shortLabel: 'Triage', icon: ShieldAlert, badge: tier1Count, badgeColor: 'crimson', shortcut: '2' },
    { href: '/app/screening', key: 'screening', label: '3. Sanctions & PEP', shortLabel: 'Screening', icon: UserCheck, badge: pendingScreening, badgeColor: 'crimson', shortcut: '3' },
    { href: '/app/customers', key: 'customers', label: '4. Customer 360 KYC', shortLabel: 'Customers', icon: Building2, shortcut: '4' },
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
      <aside
        aria-label="Workspace modules"
        className={`border-r border-line bg-panel hidden md:flex flex-col justify-between transition-all duration-200 select-none z-20 shrink-0 ${
          isCollapsed ? 'w-16' : 'w-64'
        }`}
      >
        <div className="overflow-y-auto">
          <div className="h-10 px-3 flex items-center justify-between border-b border-line">
            {!isCollapsed && (
              <span className="text-xs font-mono font-semibold text-muted">
                {language === 'bn' ? '১১টি মডিউল' : '11 modules'}
              </span>
            )}
            <button
              type="button"
              onClick={() => setIsCollapsed(!isCollapsed)}
              className="p-1.5 rounded-md hover:bg-surface-hover text-muted hover:text-fg transition-colors cursor-pointer ml-auto"
              title={isCollapsed ? 'Expand navigation rail' : 'Collapse navigation rail'}
              aria-label={isCollapsed ? 'Expand navigation rail' : 'Collapse navigation rail'}
            >
              {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
            </button>
          </div>

          <nav className="p-2 space-y-0.5">
            {NAV_ITEMS.map((item) => {
              const strippedItemHref = item.href.replace('/app', '') || '/app';
              const isActive =
                pathname === item.href ||
                (strippedItemHref !== '/app' && (pathname === strippedItemHref || pathname.startsWith(strippedItemHref))) ||
                (item.href !== '/app' && pathname.startsWith(item.href));
              const Icon = item.icon;

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  aria-current={isActive ? 'page' : undefined}
                  className={`flex items-center gap-2.5 px-2.5 py-2 rounded-lg text-xs font-mono font-medium transition-colors group ${
                    isActive
                      ? 'bg-accent-subtle text-accent-text font-semibold border border-accent/30'
                      : 'text-fg-secondary hover:text-fg hover:bg-surface-hover border border-transparent'
                  }`}
                  title={navLabel(item)}
                >
                  <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-accent-text' : 'text-muted group-hover:text-fg'}`} aria-hidden="true" />
                  {!isCollapsed && (
                    <div className="flex-1 flex items-center justify-between overflow-hidden gap-1">
                      <span className="truncate">{navLabel(item)}</span>
                      <div className="flex items-center gap-1.5 shrink-0">
                        {item.badge !== undefined && item.badge !== 0 && (
                          <span
                            className={`px-1.5 py-0.5 rounded text-xs font-semibold tabular-aml ${
                              item.badgeColor === 'crimson'
                                ? 'bg-tier-1-bg text-tier-1-text border border-tier-1-border'
                                : item.badgeColor === 'amber'
                                ? 'bg-tier-2-bg text-tier-2-text border border-tier-2-border'
                                : 'bg-surface text-fg-secondary border border-line'
                            }`}
                          >
                            {typeof item.badge === 'number' ? item.badge.toLocaleString() : item.badge}
                          </span>
                        )}
                        {item.shortcut && (
                          <kbd className="hidden lg:inline-block px-1 py-0.5 text-xs font-mono text-muted bg-canvas rounded border border-line">
                            {item.shortcut}
                          </kbd>
                        )}
                      </div>
                    </div>
                  )}
                </Link>
              );
            })}
          </nav>
        </div>

        <div className="p-2 border-t border-line bg-surface/60">
          <button
            type="button"
            onClick={resetWorkspaceData}
            className="w-full flex items-center gap-2 px-2.5 py-2 rounded-lg text-xs font-mono font-medium text-muted hover:text-tier-1-text hover:bg-tier-1-bg border border-transparent hover:border-tier-1-border transition-colors cursor-pointer"
            title="Reset Workspace to Certified Clean Demo State"
          >
            <RotateCcw className="w-3.5 h-3.5 shrink-0" aria-hidden="true" />
            {!isCollapsed && <span>Reset Workspace Data</span>}
          </button>
        </div>
      </aside>

      {/* Mobile Bottom Fixed Nav Bar (< 768px) */}
      <nav
        aria-label="Mobile workspace bar"
        className="md:hidden fixed bottom-0 left-0 right-0 h-14 bg-panel border-t border-line flex items-center justify-around z-30 px-2 select-none"
      >
        {NAV_ITEMS.slice(0, 5).map((item) => {
          const strippedItemHref = item.href.replace('/app', '') || '/app';
          const isActive = pathname === item.href || (strippedItemHref !== '/app' && pathname === strippedItemHref);
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              aria-current={isActive ? 'page' : undefined}
              className={`flex flex-col items-center justify-center p-1.5 rounded-md transition-colors ${
                isActive ? 'text-accent-text font-semibold' : 'text-muted'
              }`}
            >
              <Icon className="w-4 h-4" aria-hidden="true" />
              <span className="text-xs font-mono mt-0.5">{shortLabel(item)}</span>
            </Link>
          );
        })}
      </nav>
    </>
  );
};
