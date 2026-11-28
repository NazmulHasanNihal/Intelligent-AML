import React from 'react';
import Link from 'next/link';
import type { LucideIcon } from 'lucide-react';

export interface GlassPanelProps extends React.HTMLAttributes<HTMLDivElement> {
  elevated?: boolean;
  padding?: 'none' | 'sm' | 'md' | 'lg';
}

const PAD_MAP = {
  none: '',
  sm: 'p-3',
  md: 'p-4 sm:p-5',
  lg: 'p-5 sm:p-6',
};

export function GlassPanel({
  elevated = false,
  padding = 'md',
  className = '',
  children,
  ...rest
}: GlassPanelProps) {
  return (
    <div
      className={`${elevated ? 'glass-panel shadow-sm' : 'bg-panel border border-line'} rounded-xl ${PAD_MAP[padding]} ${className}`}
      {...rest}
    >
      {children}
    </div>
  );
}

export function Card({
  children,
  className = '',
  padding = true,
  hover = false,
  onClick,
}: {
  children: React.ReactNode;
  className?: string;
  padding?: boolean;
  hover?: boolean;
  onClick?: () => void;
}) {
  return (
    <div
      onClick={onClick}
      className={`bg-panel border border-line rounded-xl transition-colors ${
        hover ? 'hover:border-line-strong cursor-pointer' : ''
      } ${padding ? 'p-4 sm:p-5' : ''} ${className}`}
    >
      {children}
    </div>
  );
}

export function CardHeader({
  title,
  subtitle,
  badge,
  action,
  className = '',
}: {
  title: React.ReactNode;
  subtitle?: React.ReactNode;
  badge?: React.ReactNode;
  action?: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={`flex items-start justify-between gap-3 pb-3 border-b border-line-subtle ${className}`}>
      <div className="min-w-0">
        <div className="flex items-center gap-2 flex-wrap">
          <h3 className="text-sm font-semibold text-fg">{title}</h3>
          {badge}
        </div>
        {subtitle && <p className="text-xs text-muted mt-0.5">{subtitle}</p>}
      </div>
      {action && <div className="shrink-0">{action}</div>}
    </div>
  );
}

export function BentoGrid({
  children,
  columns = 3,
  className = '',
}: {
  children: React.ReactNode;
  columns?: 2 | 3 | 4;
  className?: string;
}) {
  const colClass =
    columns === 4
      ? 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-4'
      : columns === 2
      ? 'grid-cols-1 md:grid-cols-2'
      : 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3';

  return <div className={`grid ${colClass} gap-3 sm:gap-4 ${className}`}>{children}</div>;
}

export function BentoTile({
  children,
  colSpan = 1,
  rowSpan = 1,
  className = '',
}: {
  children: React.ReactNode;
  colSpan?: 1 | 2 | 3;
  rowSpan?: 1 | 2;
  className?: string;
}) {
  const colSpanClass = colSpan === 3 ? 'lg:col-span-3' : colSpan === 2 ? 'sm:col-span-2' : '';
  const rowSpanClass = rowSpan === 2 ? 'row-span-2' : '';

  return (
    <GlassPanel elevated padding="md" className={`flex flex-col justify-between ${colSpanClass} ${rowSpanClass} ${className}`}>
      {children}
    </GlassPanel>
  );
}

export interface KpiTileProps {
  label: string;
  value: string | number;
  note?: string;
  tone?: 'default' | 'tier1' | 'tier2' | 'tier3' | 'accent';
  icon?: LucideIcon;
  href?: string;
  onClick?: () => void;
  badge?: React.ReactNode;
}

const KPI_ACCENT = {
  default: 'border-line hover:border-line-strong',
  tier1: 'border-tier-1-border hover:border-tier-1',
  tier2: 'border-tier-2-border hover:border-tier-2',
  tier3: 'border-tier-3-border hover:border-tier-3',
  accent: 'border-accent/30 hover:border-accent',
};

const KPI_VAL_COLOR = {
  default: 'text-fg',
  tier1: 'text-tier-1-text',
  tier2: 'text-tier-2-text',
  tier3: 'text-tier-3-text',
  accent: 'text-accent-text',
};

export function KpiTile({
  label,
  value,
  note,
  tone = 'default',
  icon: Icon,
  href,
  onClick,
  badge,
}: KpiTileProps) {
  const content = (
    <div
      className={`bg-panel border ${KPI_ACCENT[tone]} rounded-xl p-4 flex flex-col justify-between transition-colors h-full`}
    >
      <div className="flex items-center justify-between gap-2">
        <span className="text-xs font-medium text-muted truncate">{label}</span>
        {Icon && <Icon className={`w-4 h-4 shrink-0 ${KPI_VAL_COLOR[tone]}`} aria-hidden="true" />}
      </div>
      <div className="mt-2 flex items-baseline justify-between gap-2">
        <span className={`text-xl font-semibold tracking-tight tabular-aml font-mono ${KPI_VAL_COLOR[tone]}`}>
          {value}
        </span>
        {badge}
      </div>
      {note && <p className="mt-1 text-xs text-muted truncate">{note}</p>}
    </div>
  );

  if (href) {
    return (
      <Link href={href} className="block focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent rounded-xl">
        {content}
      </Link>
    );
  }
  if (onClick) {
    return (
      <button
        type="button"
        onClick={onClick}
        className="block w-full text-left cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent rounded-xl"
      >
        {content}
      </button>
    );
  }
  return content;
}
