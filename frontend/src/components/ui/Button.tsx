'use client';

import React from 'react';
import { Loader2, type LucideIcon } from 'lucide-react';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger' | 'subtle';
  size?: 'sm' | 'md' | 'lg' | 'icon';
  loading?: boolean;
  icon?: LucideIcon;
}

const SIZE_STYLES: Record<NonNullable<ButtonProps['size']>, string> = {
  sm: 'min-h-8 px-2.5 py-1 text-xs gap-1.5',
  md: 'min-h-9 px-3.5 py-1.5 text-sm gap-2',
  lg: 'min-h-10 px-4 py-2 text-sm gap-2',
  icon: 'h-9 w-9 p-0',
};

const VARIANT_STYLES: Record<NonNullable<ButtonProps['variant']>, string> = {
  primary: 'bg-accent hover:bg-accent-hover text-accent-fg border border-transparent font-semibold shadow-sm',
  secondary: 'bg-surface hover:bg-surface-hover text-fg border border-line font-medium shadow-xs',
  outline: 'bg-transparent hover:bg-surface-hover text-fg border border-line font-medium',
  ghost: 'bg-transparent hover:bg-surface-hover text-muted hover:text-fg border border-transparent font-medium',
  danger: 'bg-tier-1 hover:opacity-90 text-white border border-transparent font-semibold shadow-sm',
  subtle: 'bg-accent-subtle text-accent-text hover:bg-accent/20 border border-accent/25 font-semibold',
};

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      children,
      variant = 'secondary',
      size = 'md',
      className = '',
      disabled = false,
      loading = false,
      type = 'button',
      icon: Icon,
      title,
      ...props
    },
    ref
  ) => {
    const isDisabled = disabled || loading;

    return (
      <button
        ref={ref}
        type={type}
        disabled={isDisabled}
        title={title}
        aria-busy={loading || undefined}
        className={`inline-flex items-center justify-center rounded-lg transition-colors duration-150 select-none cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-1 focus-visible:ring-offset-canvas disabled:opacity-50 disabled:pointer-events-none active:translate-y-px ${SIZE_STYLES[size]} ${VARIANT_STYLES[variant]} ${className}`}
        {...props}
      >
        {loading ? (
          <Loader2 className="w-4 h-4 shrink-0 animate-spin" aria-hidden="true" />
        ) : (
          Icon && <Icon className="w-4 h-4 shrink-0" aria-hidden="true" />
        )}
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';

export interface IconButtonProps extends Omit<ButtonProps, 'size' | 'children'> {
  'aria-label': string;
  icon: LucideIcon;
}

export const IconButton = React.forwardRef<HTMLButtonElement, IconButtonProps>(
  ({ variant = 'ghost', ...props }, ref) => (
    <Button ref={ref} variant={variant} size="icon" {...props} />
  )
);

IconButton.displayName = 'IconButton';
