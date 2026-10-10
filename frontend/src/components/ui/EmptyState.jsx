import React from 'react';
import { SearchX } from 'lucide-react';
import { Button } from './Button';

export const EmptyState = ({
  icon: Icon = SearchX,
  title = 'No records found',
  description = 'No items match your active filters or search terms.',
  actionLabel,
  onAction,
  secondaryLabel,
  onSecondaryAction,
  className = ''
}) => {
  return (
    <div className={`p-8 text-center flex flex-col items-center justify-center rounded-xl border border-dashed border-border bg-surface/40 my-4 select-none ${className}`}>
      <div className="w-12 h-12 rounded-full bg-surfaceRaised border border-border flex items-center justify-center text-text-muted mb-3 shadow-xs">
        <Icon className="w-6 h-6 text-accent/80" />
      </div>
      <h3 className="text-sm font-semibold text-text mb-1">{title}</h3>
      <p className="text-xs text-text-muted max-w-sm mb-4 leading-relaxed">
        {description}
      </p>
      {(actionLabel || secondaryLabel) && (
        <div className="flex items-center gap-2">
          {actionLabel && (
            <Button
              variant="secondary"
              size="sm"
              onClick={onAction}
            >
              {actionLabel}
            </Button>
          )}
          {secondaryLabel && (
            <Button
              variant="outline"
              size="sm"
              onClick={onSecondaryAction}
            >
              {secondaryLabel}
            </Button>
          )}
        </div>
      )}
    </div>
  );
};
