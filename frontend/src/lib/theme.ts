'use client';

import { useSyncExternalStore } from 'react';

export type ThemeName = 'dark' | 'light';

const STORAGE_KEY = 'aml-theme';
const listeners = new Set<() => void>();

const read = (): ThemeName =>
  typeof document !== 'undefined' && document.documentElement.dataset.theme === 'light' ? 'light' : 'dark';

const notify = () => listeners.forEach((l) => l());

/** Apply the saved choice once on the client. The server always renders dark, so this never mismatches. */
export function applyStoredTheme(): void {
  let saved: string | null = null;
  try {
    saved = localStorage.getItem(STORAGE_KEY);
  } catch {
    /* storage unavailable: stay on dark */
  }
  document.documentElement.dataset.theme = saved === 'light' ? 'light' : 'dark';
  notify();
}

export function setTheme(next: ThemeName): void {
  document.documentElement.dataset.theme = next;
  try {
    localStorage.setItem(STORAGE_KEY, next);
  } catch {
    /* ignore */
  }
  notify();
}

export function useTheme(): { theme: ThemeName; setTheme: (t: ThemeName) => void } {
  const theme = useSyncExternalStore(
    (cb) => {
      listeners.add(cb);
      return () => listeners.delete(cb);
    },
    read,
    () => 'dark' as ThemeName,
  );
  return { theme, setTheme };
}
