import React from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import { Command } from 'cmdk';
import { 
  Search, 
  LayoutDashboard, 
  AlertCircle, 
  Briefcase, 
  Share2, 
  FileText, 
  Mail, 
  ShieldCheck, 
  Cpu, 
  BarChart3, 
  Settings,
  Sun,
  Moon,
  SlidersHorizontal,
  X
} from 'lucide-react';
import { useAppStore } from '../../lib/store';
import { useTheme } from '../../context/ThemeContext';

export const CommandDialog = ({ isOpen, onClose, open, setOpen }) => {
  const isActualOpen = open !== undefined ? open : (isOpen || false);
  const handleOpenChange = (val) => {
    if (setOpen) setOpen(val);
    if (!val && onClose) onClose();
  };

  const { navigate, cases, alerts } = useAppStore();
  const { theme, toggleTheme, toggleDensity } = useTheme();

  const go = (route, params) => {
    navigate(route, params);
    handleOpenChange(false);
  };

  const isMac = typeof navigator !== 'undefined' && /Mac|iPhone|iPad/i.test(navigator.platform || navigator.userAgent);
  const shortcutHint = isMac ? '⌘K' : 'Ctrl K';

  return (
    <Dialog.Root open={isActualOpen} onOpenChange={handleOpenChange}>
      <Dialog.Portal>
        {/* Dimmed Overlay with subtle blur to focus attention */}
        <Dialog.Overlay className="fixed inset-0 z-50 bg-black/60 backdrop-blur-[2px] animate-fadeIn" />
        
        {/* Solid, 100% Opaque Dialog Content */}
        <Dialog.Content
          aria-describedby={undefined}
          className="fixed left-1/2 top-[16%] z-50 w-[min(640px,92vw)] -translate-x-1/2
                     overflow-hidden rounded-lg border border-border bg-popover
                     text-foreground shadow-2xl animate-fadeIn focus:outline-none"
        >
          <Dialog.Title className="sr-only">Command palette</Dialog.Title>
          <Command loop className="w-full flex flex-col">
            {/* Search Input Bar */}
            <div className="flex items-center px-3.5 border-b border-border bg-surfaceRaised">
              <Search className="w-4 h-4 text-muted shrink-0 mr-2.5" />
              <Command.Input
                id="global-command-palette-input"
                name="global-command-palette-input"
                aria-label="Search cases, accounts, or jump to a screen"
                placeholder="Search cases, accounts, or jump to a screen…"
                className="h-12 w-full bg-transparent text-sm text-foreground outline-none placeholder:text-muted"
              />
              <Dialog.Close asChild>
                <button 
                  className="p-1 rounded text-muted hover:text-foreground transition-colors ml-2 cursor-pointer"
                  title="Close command palette"
                  aria-label="Close command palette"
                >
                  <X className="w-4 h-4" />
                </button>
              </Dialog.Close>
            </div>

            {/* Command Results Grouped by Category */}
            <Command.List className="max-h-[360px] overflow-y-auto p-2">
              <Command.Empty className="p-6 text-center text-sm text-muted">
                No matching commands or entities found.
              </Command.Empty>

              <Command.Group heading="Go to">
                <Command.Item onSelect={() => go('overview')}>
                  <div className="flex items-center gap-2.5">
                    <LayoutDashboard className="w-4 h-4 text-muted shrink-0" />
                    <span>Overview</span>
                  </div>
                  <span className="text-[10px] font-mono text-muted">1</span>
                </Command.Item>
                <Command.Item onSelect={() => go('alerts')}>
                  <div className="flex items-center gap-2.5">
                    <AlertCircle className="w-4 h-4 text-muted shrink-0" />
                    <span>Alerts</span>
                  </div>
                  <span className="text-[10px] font-mono text-muted">2</span>
                </Command.Item>
                <Command.Item onSelect={() => go('cases')}>
                  <div className="flex items-center gap-2.5">
                    <Briefcase className="w-4 h-4 text-muted shrink-0" />
                    <span>Cases</span>
                  </div>
                  <span className="text-[10px] font-mono text-muted">3</span>
                </Command.Item>
                <Command.Item onSelect={() => go('network')}>
                  <div className="flex items-center gap-2.5">
                    <Share2 className="w-4 h-4 text-muted shrink-0" />
                    <span>Network Graph</span>
                  </div>
                  <span className="text-[10px] font-mono text-muted">4</span>
                </Command.Item>
                <Command.Item onSelect={() => go('filings')}>
                  <div className="flex items-center gap-2.5">
                    <FileText className="w-4 h-4 text-muted shrink-0" />
                    <span>SAR Filings</span>
                  </div>
                  <span className="text-[10px] font-mono text-muted">5</span>
                </Command.Item>
                <Command.Item onSelect={() => go('requests')}>
                  <div className="flex items-center gap-2.5">
                    <Mail className="w-4 h-4 text-muted shrink-0" />
                    <span>RFI Requests</span>
                  </div>
                  <span className="text-[10px] font-mono text-muted">6</span>
                </Command.Item>
                <Command.Item onSelect={() => go('audit')}>
                  <div className="flex items-center gap-2.5">
                    <ShieldCheck className="w-4 h-4 text-muted shrink-0" />
                    <span>Audit Vault</span>
                  </div>
                  <span className="text-[10px] font-mono text-muted">7</span>
                </Command.Item>
                <Command.Item onSelect={() => go('models')}>
                  <div className="flex items-center gap-2.5">
                    <Cpu className="w-4 h-4 text-muted shrink-0" />
                    <span>Engine Health &amp; Rail Status</span>
                  </div>
                  <span className="text-[10px] font-mono text-muted">8</span>
                </Command.Item>
                <Command.Item onSelect={() => go('settings')}>
                  <div className="flex items-center gap-2.5">
                    <Settings className="w-4 h-4 text-muted shrink-0" />
                    <span>Settings</span>
                  </div>
                  <span className="text-[10px] font-mono text-muted">9</span>
                </Command.Item>
              </Command.Group>

              {cases && cases.length > 0 && (
                <Command.Group heading="Cases">
                  {cases.map((c) => (
                    <Command.Item 
                      key={c.id} 
                      value={`${c.id} ${c.title} ${c.entityName || ''}`}
                      onSelect={() => go('case-detail', { caseId: c.id })}
                    >
                      <div className="flex items-center gap-2.5 min-w-0">
                        <Briefcase className="w-4 h-4 text-muted shrink-0" />
                        <span className="truncate">{c.id}: {c.title}</span>
                      </div>
                      <span className="text-[10px] font-mono text-muted uppercase shrink-0">
                        {c.tier || 'Tier 1'}
                      </span>
                    </Command.Item>
                  ))}
                </Command.Group>
              )}

              {alerts && alerts.length > 0 && (
                <Command.Group heading="Flagged Alerts">
                  {alerts.slice(0, 5).map((a) => (
                    <Command.Item 
                      key={a.id} 
                      value={`${a.id} ${a.entityName || ''} ${a.typology || ''}`}
                      onSelect={() => go('alerts')}
                    >
                      <div className="flex items-center gap-2.5 min-w-0">
                        <AlertCircle className="w-4 h-4 text-muted shrink-0" />
                        <span className="truncate">{a.id} — {a.entityName} (${a.amount?.toLocaleString()})</span>
                      </div>
                      <span className="text-[10px] font-mono text-muted uppercase shrink-0">
                        Tier {a.tierCode || 1}
                      </span>
                    </Command.Item>
                  ))}
                </Command.Group>
              )}

              <Command.Group heading="Preferences & Actions">
                <Command.Item onSelect={() => { toggleTheme(); handleOpenChange(false); }}>
                  <div className="flex items-center gap-2.5">
                    {theme === 'dark' ? <Sun className="w-4 h-4 text-muted shrink-0" /> : <Moon className="w-4 h-4 text-muted shrink-0" />}
                    <span>Toggle Theme ({theme === 'dark' ? 'Switch to Daylight' : 'Switch to Dark'})</span>
                  </div>
                </Command.Item>
                <Command.Item onSelect={() => { toggleDensity(); handleOpenChange(false); }}>
                  <div className="flex items-center gap-2.5">
                    <SlidersHorizontal className="w-4 h-4 text-muted shrink-0" />
                    <span>Toggle Density (Comfortable / Compact)</span>
                  </div>
                </Command.Item>
              </Command.Group>
            </Command.List>

            {/* Minimalist Footer with Navigation Hints */}
            <div className="border-t border-border bg-surfaceRaised px-4 py-2 text-xs text-muted flex items-center justify-between font-mono">
              <span>↑↓ navigate · ↵ select · esc close</span>
              <span className="text-[10px] bg-surface px-1.5 py-0.5 rounded border border-border">{shortcutHint}</span>
            </div>
          </Command>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
};
