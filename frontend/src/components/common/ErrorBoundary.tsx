'use client';

import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';

interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode;
  viewName?: string;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error, errorInfo: null };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    console.error(`[ErrorBoundary] Client-side fault in ${this.props.viewName || 'component'}:`, error, errorInfo);
    this.setState({ errorInfo });
  }

  handleReset = (): void => {
    this.setState({ hasError: false, error: null, errorInfo: null });
  };

  render(): ReactNode {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="w-full p-6 my-4 rounded-xl border border-tier-1-border bg-tier-1-bg text-fg">
          <div className="flex items-start gap-4">
            <div className="p-3 rounded-lg bg-panel text-tier-1-text shrink-0 border border-tier-1-border">
              <AlertTriangle className="w-6 h-6" aria-hidden="true" />
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="text-lg font-semibold text-tier-1-text">
                View Rendering Interrupted
              </h3>
              <p className="text-sm text-fg-secondary mt-1">
                An isolated client-side fault occurred while rendering {this.props.viewName || 'this module'}. Other application services remain operational.
              </p>

              {this.state.error && (
                <div className="mt-3 p-3 rounded-lg bg-panel border border-line text-xs font-mono text-tier-1-text overflow-x-auto">
                  {this.state.error.message || String(this.state.error)}
                </div>
              )}

              <div className="mt-4 flex items-center gap-3">
                <button
                  type="button"
                  onClick={this.handleReset}
                  className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium bg-tier-1 text-white hover:opacity-90 transition-opacity cursor-pointer"
                >
                  <RefreshCw className="w-3.5 h-3.5" aria-hidden="true" />
                  Retry view
                </button>
                <button
                  type="button"
                  onClick={() => {
                    this.handleReset();
                    if (typeof window !== 'undefined' && window.location.pathname !== '/') {
                      window.location.href = '/';
                    }
                  }}
                  className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium bg-surface hover:bg-surface-hover text-fg border border-line transition-colors cursor-pointer"
                >
                  <Home className="w-3.5 h-3.5" aria-hidden="true" />
                  Return to dashboard
                </button>
              </div>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
