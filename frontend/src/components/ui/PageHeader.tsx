import React from 'react';
import type { LucideIcon } from 'lucide-react';

export interface PageHeaderProps {
  title: string;
  subtitle?: string;
  eyebrow?: string;
  icon?: LucideIcon;
  actions?: React.ReactNode;
  className?: string;
}

export function PageHeader({
  title,
  subtitle,
  eyebrow,
  icon: Icon,
  actions,
  className = '',
}: PageHeaderProps) {
  return (
    <div
      className={`flex flex-col gap-3 border-b border-line pb-4 sm:flex-row sm:items-center sm:justify-between ${className}`}
    >
      <div className="min-w-0 space-y-1">
        {eyebrow && (
          <div className="flex items-center gap-1.5 text-xs font-medium text-accent-text">
            {Icon && <Icon className="w-3.5 h-3.5 shrink-0" aria-hidden="true" />}
            <span>{eyebrow}</span>
          </div>
        )}
        <h1 className="text-xl sm:text-2xl font-semibold tracking-tight text-fg leading-tight">
          {title}
        </h1>
        {subtitle && (
          <p className="text-sm text-muted max-w-2xl leading-snug line-clamp-1">
            {subtitle}
          </p>
        )}
      </div>
      {actions && (
        <div className="flex flex-wrap items-center gap-2 shrink-0">{actions}</div>
      )}
    </div>
  );
}
