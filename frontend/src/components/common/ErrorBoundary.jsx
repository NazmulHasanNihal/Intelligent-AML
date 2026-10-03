import React from 'react';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';

export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Uncaught exception caught by Intelligent-AML ErrorBoundary:", error, errorInfo);
    this.setState({ errorInfo });
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="w-full p-6 my-4 rounded-xl border border-red-500/30 bg-red-950/20 backdrop-blur-md text-text">
          <div className="flex items-start gap-4">
            <div className="p-3 rounded-lg bg-red-500/20 text-red-400">
              <AlertTriangle className="w-6 h-6" />
            </div>
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-red-300">
                View Rendering Interrupted
              </h3>
              <p className="text-sm text-text-muted mt-1">
                An isolated client-side fault occurred while rendering {this.props.viewName || 'this module'}. Other application services remain operational.
              </p>

              {this.state.error && (
                <div className="mt-3 p-3 rounded-lg bg-bg-card/80 border border-border text-xs font-mono text-red-200/90 overflow-x-auto">
                  {this.state.error.toString()}
                </div>
              )}

              <div className="mt-4 flex items-center gap-3">
                <button
                  onClick={this.handleReset}
                  className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium bg-red-600 hover:bg-red-500 text-white transition-colors"
                >
                  <RefreshCw className="w-3.5 h-3.5" />
                  Retry View
                </button>
                <button
                  onClick={() => {
                    this.handleReset();
                    if (window.location.pathname !== '/') {
                      window.history.pushState({}, '', '/');
                      window.dispatchEvent(new PopStateEvent('popstate'));
                    }
                  }}
                  className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium bg-bg-card hover:bg-bg-hover text-text border border-border transition-colors"
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
