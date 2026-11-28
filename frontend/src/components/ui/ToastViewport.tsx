'use client';

import React from 'react';
import { X, CheckCircle2, Info, ShieldAlert, Sparkles } from 'lucide-react';
import { useBankingStore } from '@/lib/store';

export function ToastViewport() {
  const { toasts, removeToast } = useBankingStore();

  if (!toasts || toasts.length === 0) return null;

  return (
    <div
      role="region"
      aria-label="Notifications"
      aria-live="polite"
      className="fixed bottom-4 right-4 z-50 flex flex-col gap-2 w-80 max-w-[calc(100vw-2rem)] pointer-events-none"
    >
      {toasts.slice(-4).map((toast) => {
        const tone =
          toast.type === 'critical'
            ? 'border-tier-1-border bg-panel text-fg'
            : toast.type === 'success'
            ? 'border-tier-3-border bg-panel text-fg'
            : 'border-accent/40 bg-panel text-fg';

        const Icon =
          toast.type === 'critical'
            ? ShieldAlert
            : toast.type === 'success'
            ? CheckCircle2
            : toast.type === 'accent'
            ? Sparkles
            : Info;

        const iconColor =
          toast.type === 'critical'
            ? 'text-tier-1-text'
            : toast.type === 'success'
            ? 'text-tier-3-text'
            : 'text-accent-text';

        return (
          <div
            key={toast.id}
            role="status"
            className={`pointer-events-auto rounded-xl border ${tone} p-3 shadow-2xl flex items-start gap-2.5`}
          >
            <Icon className={`w-4 h-4 shrink-0 mt-0.5 ${iconColor}`} aria-hidden="true" />
            <div className="min-w-0 flex-1">
              <p className="text-xs font-semibold text-fg">{toast.title}</p>
              {toast.message && <p className="text-xs text-muted mt-0.5 line-clamp-2">{toast.message}</p>}
            </div>
            <button
              type="button"
              onClick={() => removeToast(toast.id)}
              aria-label="Dismiss notification"
              className="p-0.5 rounded text-muted hover:text-fg hover:bg-surface-hover cursor-pointer"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        );
      })}
    </div>
  );
}
