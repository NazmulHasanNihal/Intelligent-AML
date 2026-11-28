'use client';

import React, { useState } from 'react';
import { Eye, EyeOff } from 'lucide-react';
import { useAppStore } from '@/lib/store';

interface PiiTextProps {
  value: string;
  type?: 'account' | 'name' | 'id';
  className?: string;
}

export const PiiText: React.FC<PiiTextProps> = ({ value, type = 'account', className = '' }) => {
  const [localRevealed, setLocalRevealed] = useState(false);
  const logAuditAction = useAppStore((state) => state.logAuditAction);
  const addToast = useAppStore((state) => state.addToast);
  const isGlobalRevealed = useAppStore((state) => state.isPiiRevealed());

  const isRevealed = localRevealed || isGlobalRevealed;

  const maskValue = (val: string): string => {
    if (!val) return '••••';
    if (type === 'account') {
      const parts = val.split('-');
      if (parts.length >= 3) {
        return `${parts[0]}-****-****-${parts[parts.length - 1]}`;
      }
      return val.length > 8 ? `${val.substring(0, 4)}****${val.substring(val.length - 4)}` : '••••••••';
    }
    if (type === 'id') {
      return val.length > 6 ? `***-**-${val.substring(val.length - 4)}` : '••••••';
    }
    const names = val.split(' ');
    return names.map((n, i) => (i === 0 ? n : '•••')).join(' ');
  };

  const toggleReveal = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (!localRevealed) {
      void logAuditAction(
        'UNMASK_PII_REQUESTED',
        `Officer unmasked sensitive customer PII for account/entity: ${value.substring(0, 4)}*** under supervision.`,
        value,
        'Active Compliance Officer'
      );
      addToast('PII access logged', 'Customer unmasking event permanently registered to audit vault.', 'info');
      setLocalRevealed(true);
      setTimeout(() => setLocalRevealed(false), 60000);
    } else {
      setLocalRevealed(false);
    }
  };

  return (
    <span className={`inline-flex items-center gap-1 font-mono tabular-aml group/pii ${className}`}>
      <span className={isRevealed ? 'text-tier-2-text font-semibold' : ''}>
        {isRevealed ? value : maskValue(value)}
      </span>
      <button
        type="button"
        onClick={toggleReveal}
        aria-label={isRevealed ? 'Re-mask customer PII' : 'Reveal customer PII for 60 seconds'}
        className="opacity-70 hover:opacity-100 p-0.5 rounded hover:bg-surface-hover text-muted hover:text-fg transition-opacity cursor-pointer"
        title={isRevealed ? 'Click to re-mask customer PII' : 'Reveal PII (Audited 60s Access)'}
      >
        {isRevealed ? (
          <EyeOff className="w-3.5 h-3.5 text-tier-2-text" aria-hidden="true" />
        ) : (
          <Eye className="w-3.5 h-3.5 text-muted group-hover/pii:text-fg" aria-hidden="true" />
        )}
      </button>
    </span>
  );
};
