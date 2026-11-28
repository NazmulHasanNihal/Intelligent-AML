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
  title = 'No records found',
  description = 'There are no active records matching the current filters or query criteria.',
  actionLabel,
  onAction,
  icon: Icon = Inbox,
}: EmptyStateProps) {
  return (
    <div
      role="status"
      aria-live="polite"
      className="p-8 sm:p-10 text-center rounded-xl bg-panel border border-line flex flex-col items-center justify-center my-4"
    >
      <div className="w-11 h-11 rounded-xl bg-surface text-muted flex items-center justify-center mb-3 border border-line">
        <Icon className="w-5 h-5" aria-hidden="true" />
      </div>
      <h4 className="text-sm font-semibold text-fg mb-1">{title}</h4>
      <p className="text-xs text-muted max-w-md mb-4">{description}</p>
      {actionLabel && onAction && (
        <button
          type="button"
          onClick={onAction}
          className="px-3.5 py-1.5 rounded-lg text-xs font-medium bg-surface hover:bg-surface-hover text-accent-text border border-accent/30 transition-colors cursor-pointer"
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
      className="p-8 sm:p-10 text-center rounded-xl bg-panel border border-line flex flex-col items-center justify-center my-4"
    >
      <div className="w-9 h-9 rounded-full border-2 border-accent/30 border-t-accent animate-spin mb-3" />
      <span className="text-xs font-mono text-fg-secondary font-medium">{message}</span>
    </div>
  );
}

export interface ErrorStateProps {
  title?: string;
  error?: string | Error;
  onRetry?: () => void;
}

export function ErrorState({
  title = 'Telemetry ingestion error',
  error = 'An unexpected error occurred while processing this compliance module.',
  onRetry,
}: ErrorStateProps) {
  const errMsg = typeof error === 'string' ? error : error?.message || 'Unknown operational failure';

  return (
    <div
      role="alert"
      aria-live="assertive"
      className="p-6 sm:p-8 rounded-xl bg-tier-1-bg border border-tier-1-border text-fg my-4 flex flex-col items-center text-center"
    >
      <div className="w-10 h-10 rounded-xl bg-panel text-tier-1-text flex items-center justify-center mb-3 border border-tier-1-border">
        <AlertTriangle className="w-5 h-5" aria-hidden="true" />
      </div>
      <h4 className="text-sm font-semibold text-tier-1-text mb-1">{title}</h4>
      <p className="text-xs text-muted max-w-lg font-mono bg-panel p-2.5 rounded-lg border border-line my-2 text-left break-all">
        {errMsg}
      </p>
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="mt-3 px-3.5 py-1.5 rounded-lg text-xs font-medium bg-panel hover:bg-surface-hover text-tier-1-text border border-tier-1-border transition-colors cursor-pointer flex items-center gap-1.5"
        >
          <RefreshCw className="w-3.5 h-3.5" aria-hidden="true" />
          <span>Retry module</span>
        </button>
      )}
    </div>
  );
}
