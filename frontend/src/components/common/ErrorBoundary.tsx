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
        <div className="w-full p-6 my-4 rounded-xl border border-rose-500/30 bg-rose-950/20 backdrop-blur-md text-slate-100">
          <div className="flex items-start gap-4">
            <div className="p-3 rounded-lg bg-rose-500/20 text-rose-400 shrink-0">
              <AlertTriangle className="w-6 h-6" />
            </div>
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-rose-300">
                View Rendering Interrupted
              </h3>
              <p className="text-sm text-slate-400 mt-1">
                An isolated client-side fault occurred while rendering {this.props.viewName || 'this module'}. Other application services and regulatory functions remain operational.
              </p>

              {this.state.error && (
                <div className="mt-3 p-3 rounded-lg bg-[#0F172A] border border-[#1E293B] text-xs font-mono text-rose-300 overflow-x-auto">
                  {this.state.error.message || String(this.state.error)}
                </div>
              )}

              <div className="mt-4 flex items-center gap-3">
                <button
                  type="button"
                  onClick={this.handleReset}
                  className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium bg-rose-600 hover:bg-rose-500 text-white transition-colors cursor-pointer"
                >
                  <RefreshCw className="w-3.5 h-3.5" />
                  Retry View
                </button>
                <button
                  type="button"
                  onClick={() => {
                    this.handleReset();
                    if (typeof window !== 'undefined' && window.location.pathname !== '/') {
                      window.location.href = '/';
                    }
                  }}
                  className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium bg-[#1E293B] hover:bg-[#334155] text-slate-200 border border-[#334155] transition-colors cursor-pointer"
                >
                  <Home className="w-3.5 h-3.5" />
                  Return to Dashboard
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
