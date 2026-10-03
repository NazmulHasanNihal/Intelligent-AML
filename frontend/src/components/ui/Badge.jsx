import React from 'react';

export const Badge = ({
  children,
  variant = 'neutral', // 'critical' | 'review' | 'cleared' | 'accent' | 'neutral'
  size = 'md', // 'sm' | 'md'
  className = '',
  dot = false
}) => {
  const base = "inline-flex items-center font-medium font-mono select-none rounded-full";

  const sizeStyles = {
    sm: "text-[10px] px-2 py-0.5 gap-1 leading-none",
    md: "text-xs px-2.5 py-0.5 gap-1.5 leading-tight"
  };

  const variantStyles = {
    critical: "bg-critical-bg text-critical-text border border-critical-border font-semibold",
    review: "bg-review-bg text-review-text border border-review-border font-semibold",
    cleared: "bg-cleared-bg text-cleared-text border border-cleared-border font-semibold",
    accent: "bg-accent-subtle text-accent-text border border-accent/20 font-semibold",
    neutral: "bg-surfaceRaised text-text-2 border border-border"
  };

  const dotStyles = {
    critical: "bg-critical",
    review: "bg-review",
    cleared: "bg-cleared",
    accent: "bg-accent",
    neutral: "bg-text-muted"
  };

  return (
    <span className={`${base} ${sizeStyles[size]} ${variantStyles[variant]} ${className}`}>
      {dot && <span className={`w-1.5 h-1.5 rounded-full ${dotStyles[variant]}`} />}
      {children}
    </span>
  );
};
