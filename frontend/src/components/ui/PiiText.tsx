'use client';

import React, { useState } from 'react';
import { Eye, EyeOff, Shield } from 'lucide-react';
import { useAppStore } from '@/lib/store';

interface PiiTextProps {
  value: string;
  type?: 'account' | 'name' | 'id';
  className?: string;
}

export const PiiText: React.FC<PiiTextProps> = ({ value, type = 'account', className = '' }) => {
  const [isRevealed, setIsRevealed] = useState(false);
  const logAuditAction = useAppStore((state) => state.logAuditAction);
  const addToast = useAppStore((state) => state.addToast);

  const maskValue = (val: string): string => {
    if (!val) return '••••';
    if (type === 'account') {
      const parts = val.split('-');
      if (parts.length >= 3) {
        return `${parts[0]}-••••-••••-${parts[parts.length - 1]}`;
      }
      return val.length > 8 ? `${val.substring(0, 4)}••••${val.substring(val.length - 4)}` : '••••••••';
    }
    if (type === 'id') {
      return val.length > 6 ? `•••-••-${val.substring(val.length - 4)}` : '••••••';
    }
    // Name
    const names = val.split(' ');
    return names.map((n, i) => i === 0 ? n : '•••').join(' ');
  };

  const toggleReveal = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (!isRevealed) {
      logAuditAction(
        'UNMASK_PII_REQUESTED',
        `Officer unmasked sensitive customer PII for account/entity: ${value.substring(0, 4)}*** under FRE 902(11) supervision.`,
        value,
        'Active Compliance Officer'
      );
      addToast('PII Access Logged', 'Customer unmasking event permanently registered to audit vault.', 'info');
      setIsRevealed(true);
      setTimeout(() => setIsRevealed(false), 30000); // Auto-re-mask after 30 seconds
    } else {
      setIsRevealed(false);
    }
  };

  return (
    <span className={`inline-flex items-center gap-1.5 font-mono ${className}`}>
      <span className={isRevealed ? 'text-amber-400 font-semibold selection:bg-amber-500/20' : 'text-text-secondary'}>
        {isRevealed ? value : maskValue(value)}
      </span>
      <button
        onClick={toggleReveal}
        className="p-0.5 rounded hover:bg-panel-raised text-text-dim hover:text-text-primary transition-colors cursor-pointer"
        title={isRevealed ? "Re-mask PII" : "Reveal PII (Logged to WORM Audit Ledger)"}
        aria-label="Toggle PII visibility"
      >
        {isRevealed ? <EyeOff className="w-3 h-3 text-amber-400" /> : <Eye className="w-3 h-3" />}
      </button>
    </span>
  );
};
