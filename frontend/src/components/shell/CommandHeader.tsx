'use client';

import React, { useEffect, useRef, useState } from 'react';
import Link from 'next/link';
import {
  Bell,
  Check,
  ChevronDown,
  Eye,
  EyeOff,
  Keyboard,
  Moon,
  Pause,
  Play,
  Plug,
  RotateCcw,
  Search,
  Settings2,
  Sun,
} from 'lucide-react';
import { useTheme } from '@/lib/theme';
import { useBankingStore } from '@/lib/store';
import { JURISDICTIONS, JurisdictionCode } from '@/lib/compliance/jurisdictions';
import { IS_ONPREM_MODE } from '@/lib/config/env';

const SCENARIOS = [
  { id: 'TBML', label: 'Trade over-invoicing', body: 'Trade-based laundering: +333.7% ASYCUDA raw cotton unit-price divergence on SWIFT MT700 LC ($48,500 / ৳5,820,000).' },
  { id: 'STRUCTURING', label: 'Cash structuring', body: 'Consecutive cash deposits of ৳9,54,000 ($7,950 USD) structured directly beneath the ৳10,00,000 BDT CTR limit.' },
  { id: 'MULE', label: 'Mule layering', body: 'Rapid pass-through across Dubai and Singapore entities with zero overnight balance.' },
  { id: 'SANCTION', label: 'Sanctions match', body: 'High-risk counterparty flagged against OFAC SDN and UN Security Council lists.' },
] as const;

function useDismiss(open: boolean, close: () => void) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!open) return;
    const onDown = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) close();
    };
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && close();
    document.addEventListener('mousedown', onDown);
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('mousedown', onDown);
      document.removeEventListener('keydown', onKey);
    };
  }, [open, close]);
  return ref;
}

const Segment: React.FC<{
  options: { value: string; label: string; title?: string }[];
  value: string;
  onChange: (v: string) => void;
  label: string;
}> = ({ options, value, onChange, label }) => (
  <div role="group" aria-label={label} className="inline-flex rounded-lg border border-line bg-surface p-0.5">
    {options.map((o) => (
      <button
        key={o.value}
        type="button"
        title={o.title}
        aria-pressed={value === o.value}
        onClick={() => onChange(o.value)}
        className={`rounded-md px-2.5 py-1 text-xs font-medium transition-colors cursor-pointer ${
          value === o.value ? 'bg-panel text-fg shadow-xs border border-line' : 'text-muted hover:text-fg border border-transparent'
        }`}
      >
        {o.label}
      </button>
    ))}
  </div>
);

const Row: React.FC<{ title: string; children: React.ReactNode }> = ({ title, children }) => (
  <div className="flex items-center justify-between gap-4 py-2">
    <span className="text-sm text-fg-secondary">{title}</span>
    {children}
  </div>
);

export const CommandHeader: React.FC<{ onOpenShortcuts?: () => void }> = ({ onOpenShortcuts }) => {
  const { theme, setTheme } = useTheme();
  const {
    currentBanker,
    setRoleModalOpen,
    densityMode,
    setDensityMode,
    activeJurisdiction,
    setActiveJurisdiction,
    isStreamRunning,
    toggleStreamRunning,
    streamSpeed,
    setStreamSpeed,
    addToast,
    setCommandPaletteOpen,
    setNotificationDrawerOpen,
    notifications,
    revealPii,
    isPiiRevealed,
    resetWorkspaceData,
    language,
    toggleLanguage,
    displayCurrency,
    toggleDisplayCurrency,
  } = useBankingStore();

  const [isClient, setIsClient] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [scenario, setScenario] = useState<string>('TBML');
  const menuRef = useDismiss(menuOpen, () => setMenuOpen(false));

  useEffect(() => setIsClient(true), []);

  const piiActive = isClient ? isPiiRevealed() : false;
  const unread = notifications.filter((n) => !n.read).length;
  const dark = theme !== 'light';

  const loadScenario = (id: string) => {
    setScenario(id);
    const s = SCENARIOS.find((x) => x.id === id);
    if (s) addToast('Scenario loaded', s.body, 'accent');
  };

  const iconBtn =
    'relative inline-flex h-9 w-9 items-center justify-center rounded-lg text-muted transition-colors hover:bg-surface-hover hover:text-fg cursor-pointer';

  return (
    <header className="flex h-14 w-full max-w-full shrink-0 items-center gap-3 border-b border-line bg-panel/95 px-3 backdrop-blur-md sm:px-4">
      <Link href="/app" className="flex shrink-0 items-center gap-2 pr-2" aria-label="Intelligent-AML home">
        <span className="h-2.5 w-2.5 rounded-full bg-accent" aria-hidden="true" />
        <span className="hidden text-sm font-semibold text-fg sm:inline">Intelligent-AML</span>
        <span className="hidden rounded border border-line bg-surface px-1.5 py-0.5 text-xs font-mono text-muted lg:inline">
          v3.0
        </span>
      </Link>

      <span
        className="hidden shrink-0 items-center gap-1.5 rounded-full border border-tier-2-border bg-tier-2-bg px-2.5 py-1 text-xs font-medium text-tier-2-text lg:inline-flex"
        title="Synthetic dataset unless FASTAPI_BACKEND_URL connects a live banking core."
      >
        {IS_ONPREM_MODE ? 'Intranet Node' : 'Cloud Sandbox'}
      </span>

      <button
        type="button"
        onClick={() => setCommandPaletteOpen(true)}
        className="hidden h-9 max-w-md flex-1 items-center gap-2 rounded-lg border border-line bg-surface px-3 text-sm text-muted transition-colors hover:border-line-strong hover:text-fg md:flex cursor-pointer"
      >
        <Search className="h-4 w-4 shrink-0" aria-hidden="true" />
        <span className="flex-1 truncate text-left">Search alerts, accounts, entities</span>
        <kbd className="rounded border border-line bg-panel px-1.5 text-xs font-mono text-muted">⌘K</kbd>
      </button>

      <div className="ml-auto flex shrink-0 items-center gap-1">
        <button
          type="button"
          onClick={() => setCommandPaletteOpen(true)}
          className={`${iconBtn} md:hidden`}
          aria-label="Search"
        >
          <Search className="h-4 w-4" />
        </button>

        <button
          type="button"
          onClick={toggleStreamRunning}
          className="inline-flex h-9 items-center gap-1.5 rounded-lg px-2.5 text-sm text-fg-secondary transition-colors hover:bg-surface-hover hover:text-fg cursor-pointer"
          title={isStreamRunning ? 'Pause the simulated feed' : 'Resume the simulated feed'}
          aria-label={isStreamRunning ? 'Pause simulated feed' : 'Resume simulated feed'}
        >
          {isStreamRunning ? <Pause className="h-4 w-4 text-tier-3-text" /> : <Play className="h-4 w-4 text-tier-2-text" />}
          <span className="hidden sm:inline">{isStreamRunning ? 'Live feed' : 'Paused'}</span>
        </button>

        {onOpenShortcuts && (
          <button
            type="button"
            onClick={onOpenShortcuts}
            className={`${iconBtn} hidden sm:inline-flex`}
            aria-label="Keyboard shortcuts"
            title="Keyboard shortcuts (?)"
          >
            <Keyboard className="h-4 w-4" />
          </button>
        )}

        <button
          type="button"
          onClick={() => setNotificationDrawerOpen(true)}
          className={iconBtn}
          aria-label={`Notifications${unread ? `, ${unread} unread` : ''}`}
          title="Notifications"
        >
          <Bell className="h-4 w-4" />
          {unread > 0 && (
            <span className="absolute right-1 top-1 flex h-4 min-w-4 items-center justify-center rounded-full bg-tier-1 px-1 text-xs font-semibold leading-none text-white">
              {unread}
            </span>
          )}
        </button>

        <div className="relative" ref={menuRef}>
          <button
            type="button"
            onClick={() => setMenuOpen((v) => !v)}
            className={iconBtn}
            aria-haspopup="dialog"
            aria-expanded={menuOpen}
            aria-label="Settings"
            title="Settings"
          >
            <Settings2 className="h-4 w-4" />
          </button>

          {menuOpen && (
            <div
              role="dialog"
              aria-label="Workspace settings"
              className="absolute right-0 top-11 z-50 w-[23rem] max-w-[calc(100vw-1.5rem)] rounded-xl border border-line bg-panel p-4 shadow-2xl"
            >
              <p className="mb-1 text-xs font-medium text-muted">Workspace</p>
              <div className="divide-y divide-line-subtle">
                <Row title="Theme">
                  <Segment
                    label="Theme"
                    value={dark ? 'dark' : 'light'}
                    onChange={(v) => setTheme(v === 'light' ? 'light' : 'dark')}
                    options={[
                      { value: 'dark', label: 'Dark' },
                      { value: 'light', label: 'Light' },
                    ]}
                  />
                </Row>
                <Row title="Density">
                  <Segment
                    label="Row density"
                    value={densityMode}
                    onChange={(v) => setDensityMode(v as 'comfortable' | 'compact')}
                    options={[
                      { value: 'comfortable', label: 'Roomy' },
                      { value: 'compact', label: 'Compact' },
                    ]}
                  />
                </Row>
                <Row title="Currency">
                  <Segment
                    label="Currency"
                    value={displayCurrency}
                    onChange={(v) => v !== displayCurrency && toggleDisplayCurrency()}
                    options={[
                      { value: 'BDT', label: '৳ BDT' },
                      { value: 'USD', label: '$ USD' },
                    ]}
                  />
                </Row>
                <Row title="Language">
                  <Segment
                    label="Language"
                    value={language}
                    onChange={(v) => v !== language && toggleLanguage()}
                    options={[
                      { value: 'en', label: 'English' },
                      { value: 'bn', label: 'বাংলা' },
                    ]}
                  />
                </Row>
                <Row title="Regulator">
                  <Segment
                    label="Regulatory regime"
                    value={activeJurisdiction}
                    onChange={(v) => setActiveJurisdiction(v as JurisdictionCode)}
                    options={(['BD_BFIU', 'US_FINCEN', 'EU_AMLA'] as JurisdictionCode[]).map((c) => ({
                      value: c,
                      label: JURISDICTIONS[c].shortCode,
                      title: `${JURISDICTIONS[c].name} (${JURISDICTIONS[c].statutoryAct})`,
                    }))}
                  />
                </Row>
                {isStreamRunning && (
                  <Row title="Feed speed">
                    <Segment
                      label="Feed speed"
                      value={String(streamSpeed)}
                      onChange={(v) => setStreamSpeed(Number(v) as 1 | 2 | 5)}
                      options={[
                        { value: '1', label: '1×' },
                        { value: '2', label: '2×' },
                        { value: '5', label: '5×' },
                      ]}
                    />
                  </Row>
                )}
              </div>

              <p className="mb-2 mt-4 text-xs font-medium text-muted">Load a scenario</p>
              <div className="grid grid-cols-2 gap-2">
                {SCENARIOS.map((s) => (
                  <button
                    key={s.id}
                    type="button"
                    onClick={() => loadScenario(s.id)}
                    className={`flex items-center justify-between rounded-lg border px-3 py-2 text-left text-xs font-medium transition-colors cursor-pointer ${
                      scenario === s.id
                        ? 'border-accent/50 bg-accent-subtle text-accent-text'
                        : 'border-line text-fg-secondary hover:bg-surface-hover'
                    }`}
                  >
                    <span>{s.label}</span>
                    {scenario === s.id && <Check className="h-3.5 w-3.5 shrink-0" aria-hidden="true" />}
                  </button>
                ))}
              </div>

              <div className="mt-3 rounded-lg border border-line bg-surface p-2.5 flex items-center justify-between gap-2 text-xs">
                <div className="flex items-center gap-2 text-fg-secondary">
                  <Plug className="w-3.5 h-3.5 text-accent-text shrink-0" aria-hidden="true" />
                  <span>Connectors: SWIFT / goAML / Core</span>
                </div>
                <Link
                  href="/app/governance#connectors"
                  onClick={() => setMenuOpen(false)}
                  className="font-mono font-semibold text-accent-text hover:underline"
                >
                  Configure
                </Link>
              </div>

              <div className="mt-4 flex items-center justify-between gap-2 border-t border-line pt-3">
                <button
                  type="button"
                  onClick={() => {
                    revealPii();
                    setMenuOpen(false);
                  }}
                  className="inline-flex items-center gap-2 rounded-lg px-2.5 py-1.5 text-xs font-medium text-fg-secondary hover:bg-surface-hover cursor-pointer"
                  title="Unmask personal data for 60 seconds. The action is logged to the audit ledger."
                >
                  {piiActive ? <EyeOff className="h-4 w-4 text-tier-2-text" /> : <Eye className="h-4 w-4" />}
                  {piiActive ? 'Personal data visible' : 'Reveal personal data'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    resetWorkspaceData();
                    setMenuOpen(false);
                  }}
                  className="inline-flex items-center gap-2 rounded-lg px-2.5 py-1.5 text-xs font-medium text-fg-secondary hover:bg-surface-hover cursor-pointer"
                >
                  <RotateCcw className="h-4 w-4" aria-hidden="true" />
                  Reset demo
                </button>
              </div>
            </div>
          )}
        </div>

        <button
          type="button"
          onClick={() => setTheme(dark ? 'light' : 'dark')}
          className={`${iconBtn} hidden sm:inline-flex`}
          aria-label={dark ? 'Switch to light theme' : 'Switch to dark theme'}
          title={dark ? 'Light theme' : 'Dark theme'}
        >
          {dark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
        </button>

        <button
          type="button"
          onClick={() => setRoleModalOpen(true)}
          className="ml-1 flex h-9 items-center gap-2 rounded-lg pl-1 pr-2 transition-colors hover:bg-surface-hover cursor-pointer"
          title="Switch role (maker / checker)"
          aria-label={`Signed in as ${currentBanker.name.split(',')[0]}. Switch role`}
        >
          <span className="flex h-7 w-7 items-center justify-center rounded-full bg-accent-subtle border border-accent/30 text-xs font-semibold text-accent-text">
            {currentBanker.avatar}
          </span>
          <span className="hidden text-left leading-tight lg:block">
            <span className="block max-w-[120px] truncate text-sm font-medium text-fg">
              {currentBanker.name.split(',')[0]}
            </span>
            <span className="block text-xs text-muted">{currentBanker.role}</span>
          </span>
          <ChevronDown className="hidden h-3.5 w-3.5 text-muted lg:block" aria-hidden="true" />
        </button>
      </div>
    </header>
  );
};
