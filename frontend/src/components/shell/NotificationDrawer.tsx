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
  ArrowRight
} from 'lucide-react';
import { useBankingStore } from '@/lib/store';

export const NotificationDrawer: React.FC = () => {
  const {
    isNotificationDrawerOpen,
    setNotificationDrawerOpen,
    notifications,
    markNotificationRead,
    clearAllNotifications
  } = useBankingStore();

  if (!isNotificationDrawerOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-black/60 backdrop-blur-xs flex justify-end animate-in fade-in duration-150">
      <div
        className="w-full max-w-md bg-[#0F172A] border-l border-[#1E293B] shadow-2xl h-full flex flex-col justify-between select-none"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-4 border-b border-[#1E293B] flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Bell className="w-4 h-4 text-emerald-400" />
            <h2 className="text-sm font-bold text-slate-100 font-sans">
              Operational Notification Center
            </h2>
            <span className="px-1.5 py-0.2 rounded text-[10px] font-mono font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">
              {notifications.filter(n => !n.read).length} Unread
            </span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={clearAllNotifications}
              className="text-[11px] text-slate-400 hover:text-slate-200 transition-colors cursor-pointer"
            >
              Clear All
            </button>
            <button
              onClick={() => setNotificationDrawerOpen(false)}
              className="p-1 rounded hover:bg-[#1E293B] text-slate-400 hover:text-slate-200 transition-colors cursor-pointer"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Notification List */}
        <div className="flex-1 overflow-y-auto p-3 space-y-2 text-xs">
          {notifications.length === 0 ? (
            <div className="py-12 text-center text-slate-500">
              <CheckCircle2 className="w-8 h-8 mx-auto mb-2 text-slate-600" />
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
                  className={`p-3 rounded-xl border transition-all cursor-pointer ${
                    notif.read
                      ? 'bg-[#0B0F17]/60 border-[#1E293B] opacity-75'
                      : isSla
                      ? 'bg-rose-950/20 border-rose-800/40'
                      : isFourEyes
                      ? 'bg-amber-950/20 border-amber-800/40'
                      : 'bg-emerald-950/20 border-emerald-800/40'
                  }`}
                >
                  <div className="flex items-start gap-2.5">
                    <div className="p-1.5 rounded-lg shrink-0 mt-0.5">
                      {isSla ? (
                        <AlertTriangle className="w-4 h-4 text-rose-400" />
                      ) : isFourEyes ? (
                        <Lock className="w-4 h-4 text-amber-400" />
                      ) : isSanctions ? (
                        <ShieldAlert className="w-4 h-4 text-rose-400" />
                      ) : (
                        <FileCheck2 className="w-4 h-4 text-emerald-400" />
                      )}
                    </div>

                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-slate-200">
                          {notif.title}
                        </span>
                        <span className="text-[10px] font-mono text-slate-500 flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          {notif.timestamp}
                        </span>
                      </div>

                      <p className="text-slate-400 text-[11px] mt-1 leading-relaxed">
                        {notif.description}
                      </p>

                      {notif.linkedHref && (
                        <Link
                          href={notif.linkedHref}
                          onClick={() => setNotificationDrawerOpen(false)}
                          className="inline-flex items-center gap-1 mt-2 text-[10px] font-mono font-bold text-emerald-400 hover:text-emerald-300"
                        >
                          <span>Open Investigation</span>
                          <ArrowRight className="w-3 h-3" />
                        </Link>
                      )}
                    </div>
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Footer */}
        <div className="p-3 border-t border-[#1E293B] bg-[#0B0F17] flex items-center justify-between text-[11px] text-slate-400 font-mono">
          <span>Real-time Event Broker: Connected</span>
          <span className="text-emerald-400 font-bold">P99 &lt; 0.82ms</span>
        </div>
      </div>
    </div>
  );
};
