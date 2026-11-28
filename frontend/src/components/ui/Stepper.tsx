import React from 'react';
import { Check, Clock } from 'lucide-react';

export interface StepItem {
  title: string;
  detail?: string;
  status: 'COMPLETE' | 'IN_PROGRESS' | 'PENDING';
}

export function Stepper({ steps }: { steps: StepItem[] }) {
  return (
    <ol className="space-y-3">
      {steps.map((step, i) => {
        const complete = step.status === 'COMPLETE';
        const active = step.status === 'IN_PROGRESS';
        return (
          <li key={`${step.title}-${i}`} className="flex items-start gap-3">
            <span
              className={`mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full border text-xs font-mono font-semibold ${
                complete
                  ? 'border-tier-3 bg-tier-3-bg text-tier-3-text'
                  : active
                  ? 'border-tier-2 bg-tier-2-bg text-tier-2-text'
                  : 'border-line bg-surface text-muted'
              }`}
            >
              {complete ? <Check className="w-3.5 h-3.5" aria-hidden="true" /> : active ? <Clock className="w-3.5 h-3.5" aria-hidden="true" /> : i + 1}
            </span>
            <div className="min-w-0 flex-1">
              <p className={`text-sm font-medium ${complete || active ? 'text-fg' : 'text-muted'}`}>
                {step.title}
              </p>
              {step.detail && <p className="text-xs text-muted mt-0.5">{step.detail}</p>}
            </div>
          </li>
        );
      })}
    </ol>
  );
}
