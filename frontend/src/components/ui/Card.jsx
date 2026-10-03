import React from 'react';

export const Card = ({
  children,
  className = '',
  padding = true,
  hover = false,
  onClick
}) => {
  return (
    <div
      onClick={onClick}
      className={`bg-surface border border-border rounded-lg shadow-sm transition-colors ${
        hover ? 'hover:border-borderStrong cursor-pointer' : ''
      } ${padding ? 'p-4 sm:p-5' : ''} ${className}`}
    >
      {children}
    </div>
  );
};

export const CardHeader = ({
  title,
  subtitle,
  badge,
  action,
  className = ''
}) => {
  return (
    <div className={`flex items-start justify-between gap-3 pb-3 border-b border-borderSubtle ${className}`}>
      <div className="min-w-0">
        <div className="flex items-center gap-2 flex-wrap">
          <h3 className="text-sm font-semibold text-text truncate">{title}</h3>
          {badge}
        </div>
        {subtitle && <p className="text-xs text-text-2 mt-0.5">{subtitle}</p>}
      </div>
      {action && <div className="shrink-0">{action}</div>}
    </div>
  );
};
