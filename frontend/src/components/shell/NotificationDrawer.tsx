'use client';

import React from 'react';
import Link from 'next/link';
import {
  Bell,
  X,
  AlertTriangle,
  Lock,
  FileCheck2,
  CheckCircle2,
  Clock,
  ShieldAlert,
  ArrowRight,
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';

export const NotificationDrawer: React.FC = () => {
  const {
    isNotificationDrawerOpen,
    setNotificationDrawerOpen,
    notifications,
    markNotificationRead,
    clearAllNotifications,
  } = useBankingStore();

  if (!isNotificationDrawerOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 overflow-hidden bg-black/60 backdrop-blur-xs flex justify-end"
      onClick={() => setNotificationDrawerOpen(false)}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-label="Operational notification center"
        className="w-full max-w-md bg-panel border-l border-line shadow-2xl h-full flex flex-col justify-between select-none"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-4 border-b border-line flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Bell className="w-4 h-4 text-accent-text" aria-hidden="true" />
            <h2 className="text-sm font-semibold text-fg">
              Operational Notification Center
            </h2>
            <span className="px-2 py-0.5 rounded-full text-xs font-mono font-semibold bg-tier-1-bg text-tier-1-text border border-tier-1-border tabular-aml">
              {notifications.filter((n) => !n.read).length} Unread
            </span>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={clearAllNotifications}
              className="text-xs text-muted hover:text-fg transition-colors cursor-pointer"
            >
              Clear all
            </button>
            <button
              type="button"
              onClick={() => setNotificationDrawerOpen(false)}
              aria-label="Close notifications"
              className="p-1.5 rounded-lg hover:bg-surface-hover text-muted hover:text-fg transition-colors cursor-pointer"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-3 space-y-2 text-xs">
          {notifications.length === 0 ? (
            <div className="py-12 text-center text-muted">
              <CheckCircle2 className="w-8 h-8 mx-auto mb-2 opacity-60" aria-hidden="true" />
              <span>No pending SLA breach notices or approval requests.</span>
            </div>
          ) : (
            notifications.map((notif) => {
              const isSla = notif.type === 'SLA_WARNING';
              const isFourEyes = notif.type === 'FOUR_EYES_REQUEST';
              const isSanctions = notif.type === 'SANCTIONS_INTERDICTION';

              return (
                <div
                  key={notif.id}
                  onClick={() => markNotificationRead(notif.id)}
                  className={`p-3 rounded-xl border transition-colors cursor-pointer ${
                    notif.read
                      ? 'bg-surface/60 border-line opacity-75'
                      : isSla || isSanctions
                      ? 'bg-tier-1-bg border-tier-1-border'
                      : isFourEyes
                      ? 'bg-tier-2-bg border-tier-2-border'
                      : 'bg-tier-3-bg border-tier-3-border'
                  }`}
                >
                  <div className="flex items-start gap-2.5">
                    <div className="p-1 rounded-lg shrink-0 mt-0.5">
                      {isSla ? (
                        <AlertTriangle className="w-4 h-4 text-tier-1-text" aria-hidden="true" />
                      ) : isFourEyes ? (
                        <Lock className="w-4 h-4 text-tier-2-text" aria-hidden="true" />
                      ) : isSanctions ? (
                        <ShieldAlert className="w-4 h-4 text-tier-1-text" aria-hidden="true" />
                      ) : (
                        <FileCheck2 className="w-4 h-4 text-tier-3-text" aria-hidden="true" />
                      )}
                    </div>

                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between gap-2">
                        <span className="font-semibold text-fg truncate">
                          {notif.title}
                        </span>
                        <span className="text-xs font-mono text-muted flex items-center gap-1 shrink-0 tabular-aml">
                          <Clock className="w-3 h-3" aria-hidden="true" />
                          {notif.timestamp}
                        </span>
                      </div>

                      <p className="text-fg-secondary text-xs mt-1 leading-relaxed">
                        {notif.description}
                      </p>

                      {notif.linkedHref && (
                        <Link
                          href={notif.linkedHref}
                          onClick={() => setNotificationDrawerOpen(false)}
                          className="inline-flex items-center gap-1 mt-2 text-xs font-mono font-semibold text-accent-text hover:underline"
                        >
                          <span>Open investigation</span>
                          <ArrowRight className="w-3 h-3" aria-hidden="true" />
                        </Link>
                      )}
                    </div>
                  </div>
                </div>
              );
            })
          )}
        </div>

        <div className="p-3 border-t border-line bg-surface flex items-center justify-between text-xs text-muted font-mono">
          <span>Event broker: Ready</span>
          <span className="text-accent-text font-semibold">Target SLA &lt; 200 µs</span>
        </div>
      </div>
    </div>
  );
};
