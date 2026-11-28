'use client';

import React, { useEffect, useState } from 'react';
import { usePathname } from 'next/navigation';
import { Keyboard, Sparkles, X } from 'lucide-react';
import { CommandHeader } from '@/components/shell/CommandHeader';
import { DemoDisclaimerBanner } from '@/components/shell/DemoDisclaimerBanner';
import { NavigationRail } from '@/components/shell/NavigationRail';
import { GlobalCommandPalette } from '@/components/shell/GlobalCommandPalette';
import { NotificationDrawer } from '@/components/shell/NotificationDrawer';
import { FourEyesApprovalModal } from '@/components/auth/FourEyesApprovalModal';
import { RoleSwitchModal } from '@/components/auth/RoleSwitchModal';
import { ToastViewport } from '@/components/ui/ToastViewport';
import { Dialog } from '@/components/ui/Overlay';
import { Button } from '@/components/ui/Button';
import { rehydrateWorkspace, useBankingStore } from '@/lib/store';
import { applyStoredTheme } from '@/lib/theme';

const SHORTCUTS = [
  { key: 'Ctrl+K / /', desc: 'Open global command palette' },
  { key: '1 – 9, 0', desc: 'Jump directly between compliance modules' },
  { key: '?', desc: 'Toggle keyboard shortcuts guide' },
  { key: 'Esc', desc: 'Close active dialog, drawer, or palette' },
];

export function AppShellWrapper({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const language = useBankingStore((s) => s.language);
  const [shortcutsOpen, setShortcutsOpen] = useState(false);
  const [showWelcome, setShowWelcome] = useState(false);

  useEffect(() => {
    void rehydrateWorkspace();
    applyStoredTheme();
    try {
      if (!localStorage.getItem('aml_tour_dismissed')) {
        setShowWelcome(true);
      }
    } catch {
      /* ignore */
    }
  }, []);

  useEffect(() => {
    if (typeof document !== 'undefined') {
      document.documentElement.lang = language === 'bn' ? 'bn' : 'en';
    }
  }, [language]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const target = e.target;
      if (
        target instanceof HTMLInputElement ||
        target instanceof HTMLTextAreaElement ||
        target instanceof HTMLSelectElement ||
        (target instanceof HTMLElement && target.isContentEditable)
      ) {
        return;
      }
      if (e.key === '?') {
        e.preventDefault();
        setShortcutsOpen((prev) => !prev);
      }
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, []);

  const dismissTour = () => {
    setShowWelcome(false);
    try {
      localStorage.setItem('aml_tour_dismissed', 'true');
    } catch {
      /* ignore */
    }
  };

  const isMarketing =
    pathname === '/' ||
    pathname.startsWith('/terms') ||
    pathname.startsWith('/privacy') ||
    pathname.startsWith('/cookies');

  if (isMarketing) {
    return (
      <main className="min-h-screen bg-canvas text-fg">
        {children}
        <ToastViewport />
      </main>
    );
  }

  return (
    <div className="app-surface min-h-screen bg-canvas text-fg">
      <div className="fixed top-0 left-0 right-0 z-40 bg-panel/95 backdrop-blur-md">
        <DemoDisclaimerBanner />
        <CommandHeader onOpenShortcuts={() => setShortcutsOpen(true)} />
      </div>

      <div className="flex pt-[5.25rem] min-h-[calc(100vh-5.25rem)]">
        <NavigationRail />

        <main className="flex-1 min-w-0 bg-canvas text-fg overflow-y-auto pb-16 md:pb-0">
          {showWelcome && pathname.startsWith('/app') && (
            <div className="mx-4 mt-4 sm:mx-6 flex flex-wrap items-center justify-between gap-3 rounded-xl border border-accent/30 bg-accent-subtle px-4 py-2.5 text-xs">
              <div className="flex items-center gap-2 text-fg">
                <Sparkles className="w-4 h-4 text-accent-text shrink-0" aria-hidden="true" />
                <span>
                  Welcome to Intelligent-AML v3.0. Press <kbd className="rounded border border-line bg-panel px-1.5 py-0.5 font-mono">1–9</kbd> to jump modules, <kbd className="rounded border border-line bg-panel px-1.5 py-0.5 font-mono">⌘K</kbd> to search, or <kbd className="rounded border border-line bg-panel px-1.5 py-0.5 font-mono">?</kbd> for shortcuts.
                </span>
              </div>
              <button
                type="button"
                onClick={dismissTour}
                aria-label="Dismiss welcome hint"
                className="inline-flex items-center gap-1 rounded-md px-2 py-1 text-xs font-medium text-muted hover:bg-surface-hover hover:text-fg cursor-pointer"
              >
                <X className="w-3.5 h-3.5" aria-hidden="true" />
                Dismiss
              </button>
            </div>
          )}
          {children}
        </main>
      </div>

      <GlobalCommandPalette />
      <NotificationDrawer />
      <FourEyesApprovalModal />
      <RoleSwitchModal />
      <ToastViewport />

      <Dialog
        open={shortcutsOpen}
        onClose={() => setShortcutsOpen(false)}
        title="Keyboard Shortcuts"
        description="Rapid workstation navigation across all 11 compliance modules."
      >
        <div className="space-y-2.5">
          {SHORTCUTS.map((s) => (
            <div key={s.key} className="flex items-center justify-between gap-4 rounded-lg border border-line bg-surface px-3 py-2 text-sm">
              <span className="text-fg-secondary">{s.desc}</span>
              <kbd className="rounded border border-line bg-panel px-2 py-0.5 text-xs font-mono text-fg shrink-0">
                {s.key}
              </kbd>
            </div>
          ))}
          <div className="pt-2 flex justify-end">
            <Button variant="primary" icon={Keyboard} onClick={() => setShortcutsOpen(false)}>
              Done
            </Button>
          </div>
        </div>
      </Dialog>
    </div>
  );
}
