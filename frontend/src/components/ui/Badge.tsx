import React from 'react';

export type BadgeVariant = 'critical' | 'tier1' | 'review' | 'tier2' | 'cleared' | 'tier3' | 'accent' | 'neutral';

export function Badge({
  children,
  variant = 'neutral',
  size = 'md',
  className = '',
  dot = false,
}: {
  children: React.ReactNode;
  variant?: BadgeVariant;
  size?: 'sm' | 'md';
  className?: string;
  dot?: boolean;
}) {
  const sizeStyles = size === 'sm' ? 'text-xs px-2 py-0.5 gap-1' : 'text-xs px-2.5 py-0.5 gap-1.5';

  const variantMap: Record<BadgeVariant, string> = {
    critical: 'bg-tier-1-bg text-tier-1-text border border-tier-1-border font-semibold',
    tier1: 'bg-tier-1-bg text-tier-1-text border border-tier-1-border font-semibold',
    review: 'bg-tier-2-bg text-tier-2-text border border-tier-2-border font-semibold',
    tier2: 'bg-tier-2-bg text-tier-2-text border border-tier-2-border font-semibold',
    cleared: 'bg-tier-3-bg text-tier-3-text border border-tier-3-border font-semibold',
    tier3: 'bg-tier-3-bg text-tier-3-text border border-tier-3-border font-semibold',
    accent: 'bg-accent-subtle text-accent-text border border-accent/25 font-semibold',
    neutral: 'bg-surface text-fg-secondary border border-line',
  };

  const dotMap: Record<BadgeVariant, string> = {
    critical: 'bg-tier-1',
    tier1: 'bg-tier-1',
    review: 'bg-tier-2',
    tier2: 'bg-tier-2',
    cleared: 'bg-tier-3',
    tier3: 'bg-tier-3',
    accent: 'bg-accent',
    neutral: 'bg-muted',
  };

  return (
    <span className={`inline-flex items-center rounded-full font-mono select-none leading-tight ${sizeStyles} ${variantMap[variant]} ${className}`}>
      {dot && <span className={`w-1.5 h-1.5 rounded-full shrink-0 ${dotMap[variant]}`} aria-hidden="true" />}
      {children}
    </span>
  );
}

export function RiskPill({ tier }: { tier: 1 | 2 | 3 | 'Tier 1 Hold' | 'Tier 2 Review' | 'Tier 3 Clear' }) {
  const code = tier === 1 || tier === 'Tier 1 Hold' ? 1 : tier === 2 || tier === 'Tier 2 Review' ? 2 : 3;
  const label = code === 1 ? 'Tier 1 Hold' : code === 2 ? 'Tier 2 Review' : 'Tier 3 Clear';
  const variant: BadgeVariant = code === 1 ? 'tier1' : code === 2 ? 'tier2' : 'tier3';

  return (
    <Badge variant={variant} dot size="sm">
      {label}
    </Badge>
  );
}

export function StatusPill({ status }: { status: string }) {
  const norm = status.toUpperCase();
  const variant: BadgeVariant =
    norm.includes('QUARANTINED') || norm.includes('MATCH') || norm.includes('HOLD')
      ? 'tier1'
      : norm.includes('REVIEW') || norm.includes('PENDING') || norm.includes('INVESTIGATION') || norm.includes('DRAFT')
      ? 'tier2'
      : norm.includes('CLEAR') || norm.includes('VERIFIED') || norm.includes('DISMISSED') || norm.includes('SUBMITTED')
      ? 'tier3'
      : 'neutral';

  return (
    <Badge variant={variant} size="sm">
      {status.replace(/_/g, ' ')}
    </Badge>
  );
}
