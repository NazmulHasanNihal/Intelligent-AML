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
    // Name
    const names = val.split(' ');
    return names.map((n, i) => i === 0 ? n : '•••').join(' ');
  };

  const toggleReveal = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (!localRevealed) {
      logAuditAction(
        'UNMASK_PII_REQUESTED',
        `Officer unmasked sensitive customer PII for account/entity: ${value.substring(0, 4)}*** under supervision.`,
        value,
        'Active Compliance Officer'
      );
      addToast('PII Access Logged', 'Customer unmasking event permanently registered to audit vault.', 'info');
      setLocalRevealed(true);
      setTimeout(() => setLocalRevealed(false), 60000); // 60 seconds
    } else {
      setLocalRevealed(false);
    }
  };

  return (
    <span className={`inline-flex items-center gap-1 font-mono group/pii ${className}`}>
      <span className={isRevealed ? 'text-amber-300 font-bold' : ''}>
        {isRevealed ? value : maskValue(value)}
      </span>
      <button
        type="button"
        onClick={toggleReveal}
        className="opacity-60 hover:opacity-100 p-0.5 rounded hover:bg-[#1E293B] text-slate-400 hover:text-slate-200 transition-opacity cursor-pointer"
        title={isRevealed ? "Click to re-mask customer PII" : "Reveal PII (Audited 60s Access)"}
      >
        {isRevealed ? (
          <EyeOff className="w-3 h-3 text-amber-400" />
        ) : (
          <Eye className="w-3 h-3 text-slate-500 group-hover/pii:text-slate-300" />
        )}
      </button>
    </span>
  );
};
