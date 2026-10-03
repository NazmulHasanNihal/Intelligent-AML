import React from 'react';

export function SkeletonLoader({ className = '', variant = 'card', count = 1 }) {
  const items = Array.from({ length: count });

  if (variant === 'metric') {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {items.map((_, i) => (
          <div key={i} className="p-4 rounded-xl border border-border bg-bg-card/40 animate-pulse">
            <div className="h-3 w-24 bg-border/60 rounded mb-3"></div>
            <div className="h-7 w-32 bg-border/80 rounded mb-2"></div>
            <div className="h-3 w-16 bg-border/40 rounded"></div>
          </div>
        ))}
      </div>
    );
  }

  if (variant === 'table') {
    return (
      <div className="w-full rounded-xl border border-border bg-bg-card/40 p-4 animate-pulse">
        <div className="h-6 w-48 bg-border/70 rounded mb-4"></div>
        <div className="space-y-3">
          {items.map((_, i) => (
            <div key={i} className="flex items-center gap-4 py-2 border-b border-border/30 last:border-0">
              <div className="h-4 w-28 bg-border/60 rounded"></div>
              <div className="h-4 w-40 bg-border/40 rounded flex-1"></div>
              <div className="h-4 w-20 bg-border/50 rounded"></div>
              <div className="h-4 w-16 bg-border/70 rounded"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (variant === 'graph') {
    return (
      <div className="w-full h-96 rounded-xl border border-border bg-bg-card/30 flex items-center justify-center animate-pulse">
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-full border-2 border-primary/30 border-t-primary animate-spin mx-auto"></div>
          <div className="h-3 w-40 bg-border/60 rounded mx-auto"></div>
        </div>
      </div>
    );
  }

  return (
    <div className={`rounded-xl border border-border bg-bg-card/40 p-4 animate-pulse ${className}`}>
      <div className="h-4 w-1/3 bg-border/60 rounded mb-3"></div>
      <div className="h-3 w-2/3 bg-border/40 rounded"></div>
    </div>
  );
}
