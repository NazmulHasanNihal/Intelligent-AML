'use client';

import React from 'react';
import { AlertTriangle, Inbox, RefreshCw } from 'lucide-react';

export interface EmptyStateProps {
  title?: string;
  description?: string;
  actionLabel?: string;
  onAction?: () => void;
  icon?: React.ElementType;
}

export function EmptyState({
  title = 'No Records Found',
  description = 'There are no active records matching the current filters or query criteria.',
  actionLabel,
  onAction,
  icon: Icon = Inbox
}: EmptyStateProps) {
  return (
    <div
      role="status"
      aria-live="polite"
      className="p-8 sm:p-12 text-center rounded-xl bg-[#0F172A]/40 border border-[#1E293B] flex flex-col items-center justify-center my-4"
    >
      <div className="w-12 h-12 rounded-xl bg-[#1E293B] text-slate-400 flex items-center justify-center mb-3">
        <Icon className="w-6 h-6" />
      </div>
      <h4 className="text-sm font-bold text-slate-200 mb-1">{title}</h4>
      <p className="text-xs text-slate-400 max-w-md font-sans mb-4">{description}</p>
      {actionLabel && onAction && (
        <button
          type="button"
          onClick={onAction}
          className="px-3.5 py-1.5 rounded-lg text-xs font-mono font-bold bg-[#1E293B] hover:bg-[#334155] text-emerald-400 border border-emerald-500/30 transition-all cursor-pointer"
        >
          {actionLabel}
        </button>
      )}
    </div>
  );
}

export interface LoadingStateProps {
  message?: string;
}

export function LoadingState({ message = 'Loading institutional telemetry...' }: LoadingStateProps) {
  return (
    <div
      role="status"
      aria-live="polite"
      className="p-8 sm:p-12 text-center rounded-xl bg-[#0F172A]/40 border border-[#1E293B] flex flex-col items-center justify-center my-4 animate-pulse"
    >
      <div className="w-10 h-10 rounded-full border-2 border-emerald-500/30 border-t-emerald-400 animate-spin mb-3" />
      <span className="text-xs font-mono text-slate-300 font-semibold">{message}</span>
    </div>
  );
}

export interface ErrorStateProps {
  title?: string;
  error?: string | Error;
  onRetry?: () => void;
}

export function ErrorState({
  title = 'Telemetry Ingestion Error',
  error = 'An unexpected error occurred while processing this compliance module.',
  onRetry
}: ErrorStateProps) {
  const errMsg = typeof error === 'string' ? error : error?.message || 'Unknown operational failure';

  return (
    <div
      role="alert"
      aria-live="assertive"
      className="p-6 sm:p-8 rounded-xl bg-rose-950/20 border border-rose-500/30 text-slate-200 my-4 flex flex-col items-center text-center"
    >
      <div className="w-10 h-10 rounded-xl bg-rose-500/10 text-rose-400 flex items-center justify-center mb-3">
        <AlertTriangle className="w-5 h-5" />
      </div>
      <h4 className="text-sm font-bold text-rose-300 mb-1">{title}</h4>
      <p className="text-xs text-slate-400 max-w-lg font-mono bg-[#0B0F17] p-2.5 rounded-lg border border-[#1E293B] my-2 text-left break-all">
        {errMsg}
      </p>
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="mt-3 px-3.5 py-1.5 rounded-lg text-xs font-mono font-bold bg-rose-950/60 hover:bg-rose-900/80 text-rose-200 border border-rose-600/50 transition-all cursor-pointer flex items-center gap-1.5"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Retry Module Execution</span>
        </button>
      )}
    </div>
  );
}
