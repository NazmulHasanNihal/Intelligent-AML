import React from 'react';
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';
import { 
  Search, 
  Command, 
  Sun, 
  Moon, 
  SlidersHorizontal, 
  UserCheck, 
  Check, 
  ChevronDown,
  ShieldAlert
} from 'lucide-react';
import { useAppStore } from '../../lib/store';
import { useTheme } from '../../context/ThemeContext';
import { useAuth } from '../../context/AuthContext';

export const AppHeader = ({ onOpenCommandPalette }) => {
  const { activeRoute, activeRouteParams, setRoleModalOpen, setSanctionsModalOpen } = useAppStore();
  const { theme, toggleTheme, density, toggleDensity } = useTheme();
  const { currentBanker, availableBankers, switchBanker } = useAuth();

  const isMac = typeof navigator !== 'undefined' && /Mac|iPhone|iPad/i.test(navigator.platform || navigator.userAgent);
  const shortcutHint = isMac ? '⌘K' : 'Ctrl K';

  const routeTitles = {
    overview: 'Surveillance Overview',
    alerts: 'Alert Triage Queue',
    cases: 'Case Management Workspace',
    'case-detail': activeRouteParams?.caseId ? `Case ${activeRouteParams.caseId}` : 'Case Investigation',
    network: 'Forensic Network Graph',
    filings: 'Autonomous SAR Filings',
    requests: 'Compliance RFI Requests',
    audit: 'Immutable Audit Vault',
    models: 'Surveillance Engine & Health',
    settings: 'Platform Settings'
  };

  return (
    <header className="h-14 px-4 sm:px-6 bg-surface border-b border-border flex items-center justify-between gap-3 text-foreground shrink-0 select-none sticky top-0 z-30">
      {/* Left: Breadcrumbs & Status */}
      <div className="flex items-center gap-3 min-w-0">
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold text-foreground truncate">
              {routeTitles[activeRoute] || 'Surveillance Console'}
            </span>
            <span className="text-[10px] text-muted hidden sm:inline">•</span>
            <span className="text-[11px] text-muted hidden sm:inline flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-cleared inline-block" />
              <span>Live Feed • Updated 2m ago</span>
            </span>
          </div>
        </div>
      </div>

      {/* Center: Command Palette Trigger (Platform Aware: Ctrl K on Win/Linux, ⌘K on Mac) */}
      <div className="hidden md:flex max-w-xs w-full">
        <button
          onClick={onOpenCommandPalette}
          className="w-full flex items-center justify-between px-3 py-1.5 rounded bg-background hover:bg-surfaceHover border border-border text-xs text-muted hover:text-foreground transition-colors cursor-pointer"
        >
          <div className="flex items-center gap-2 min-w-0">
            <Search className="w-3.5 h-3.5 text-muted" />
            <span className="truncate">Search cases, accounts, BICs...</span>
          </div>
          <kbd className="font-mono text-[10px] bg-surfaceRaised px-1.5 py-0.5 rounded border border-border text-muted flex items-center gap-1">
            {isMac && <Command className="w-2.5 h-2.5" />}
            <span>{shortcutHint}</span>
          </kbd>
        </button>
      </div>

      {/* Right Controls: Density, Theme, Officer Persona */}
      <div className="flex items-center gap-1.5 shrink-0">
        {/* Mobile Search */}
        <button
          onClick={onOpenCommandPalette}
          className="md:hidden p-2 rounded hover:bg-surfaceHover text-muted hover:text-foreground"
          title={`Search (${shortcutHint})`}
        >
          <Search className="w-4 h-4" />
        </button>

        {/* Real-Time Sanctions Screener Trigger */}
        <button
          onClick={() => setSanctionsModalOpen(true)}
          className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-critical/10 hover:bg-critical/20 border border-critical/30 text-critical text-xs font-mono font-medium transition-colors cursor-pointer"
          title="Open Automated Sanctions & PEP Compliance Screener"
        >
          <ShieldAlert className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">Sanctions Screen</span>
        </button>

        {/* Density Toggle (Comfortable vs Compact) */}
        <button
          onClick={toggleDensity}
          className="p-2 rounded hover:bg-surfaceHover text-muted hover:text-foreground transition-colors cursor-pointer"
          title={`Density: currently ${density}. Click to switch.`}
        >
          <SlidersHorizontal className="w-4 h-4" />
        </button>

        {/* Theme Switcher (Light / Dark) */}
        <button
          onClick={toggleTheme}
          className="p-2 rounded hover:bg-surfaceHover text-muted hover:text-foreground transition-colors cursor-pointer"
          title={`Theme: currently ${theme}. Click to toggle.`}
        >
          {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
        </button>

        {/* Officer Persona Switcher with Radix Dropdown Portal */}
        <DropdownMenu.Root>
          <DropdownMenu.Trigger asChild>
            <button
              className="flex items-center gap-2 pl-2 pr-2.5 py-1 rounded hover:bg-surfaceHover border border-border text-xs transition-colors cursor-pointer outline-none focus-visible:ring-1 focus-visible:ring-accent"
              title="Switch Authorized Signatory"
            >
              <div className="w-5 h-5 rounded bg-surfaceRaised text-foreground font-mono font-bold flex items-center justify-center text-[10px] border border-border">
                {currentBanker.avatar || 'O'}
              </div>
              <div className="text-left hidden lg:block leading-tight">
                <span className="font-semibold text-foreground text-xs block truncate max-w-[120px]">{currentBanker.name}</span>
                <span className="text-[10px] text-muted block font-mono">{currentBanker.role}</span>
              </div>
              <ChevronDown className="w-3 h-3 text-muted" />
            </button>
          </DropdownMenu.Trigger>

          <DropdownMenu.Portal>
            <DropdownMenu.Content
              align="end"
              sideOffset={8}
              className="z-50 min-w-[270px] rounded-lg border border-border bg-popover p-1.5 text-foreground shadow-2xl animate-fadeIn focus:outline-none"
            >
              {/* Authorized Signatory Header */}
              <div className="px-2 py-1 text-[10px] font-mono text-muted uppercase tracking-wider border-b border-border mb-1 flex items-center justify-between">
                <span>Active Signatory Delegation</span>
                <span className="text-[9px] px-1 py-0.2 rounded bg-accent/10 text-accent font-semibold">Four-Eyes Control</span>
              </div>

              {/* Signatory Options */}
              <div className="space-y-0.5">
                {(availableBankers || []).map((b) => {
                  const isSelected = b.id === currentBanker.id;
                  return (
                    <DropdownMenu.Item
                      key={b.id}
                      onSelect={() => switchBanker(b.id)}
                      className={`w-full flex items-center justify-between p-2 rounded text-left text-xs transition-colors cursor-pointer outline-none ${
                        isSelected 
                          ? 'bg-accent/10 text-accent font-semibold' 
                          : 'hover:bg-surfaceHover text-foreground focus:bg-surfaceHover'
                      }`}
                    >
                      <div className="min-w-0">
                        <div className="font-medium text-foreground truncate">{b.name}</div>
                        <div className="text-[10px] text-muted truncate">{b.roleTitle}</div>
                      </div>
                      {isSelected && <Check className="w-3.5 h-3.5 text-accent shrink-0 ml-2" />}
                    </DropdownMenu.Item>
                  );
                })}
              </div>

              <div className="pt-1.5 mt-1 border-t border-border">
                <button
                  onClick={() => setRoleModalOpen(true)}
                  className="w-full flex items-center justify-center gap-1.5 py-1 px-2 rounded bg-surfaceRaised hover:bg-surface text-text font-mono text-[10px] border border-border cursor-pointer transition-colors"
                >
                  <UserCheck className="w-3 h-3 text-accent" />
                  <span>Delegation &amp; Role-Switch Modal</span>
                </button>
              </div>
            </DropdownMenu.Content>
          </DropdownMenu.Portal>
        </DropdownMenu.Root>
      </div>
    </header>
  );
};
