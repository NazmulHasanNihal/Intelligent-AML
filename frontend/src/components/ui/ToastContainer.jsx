import React from 'react';
import { CheckCircle2, AlertCircle, Info, X } from 'lucide-react';
import { useAppStore } from '../../lib/store';

export const ToastContainer = () => {
  const { toasts, dismissToast } = useAppStore();

  if (!toasts || toasts.length === 0) return null;

  return (
    <div className="fixed bottom-4 right-4 z-[60] flex flex-col gap-2 max-w-sm w-full pointer-events-none">
      {toasts.map((t) => {
        const isSuccess = t.type === 'success';
        const isError = t.type === 'error';

        return (
          <div
            key={t.id}
            className="pointer-events-auto p-3.5 rounded-lg bg-popover border border-border shadow-xl flex items-start gap-3 transition-all animate-fadeIn"
          >
            {isSuccess ? (
              <CheckCircle2 className="w-4 h-4 text-cleared shrink-0 mt-0.5" />
            ) : isError ? (
              <AlertCircle className="w-4 h-4 text-critical shrink-0 mt-0.5" />
            ) : (
              <Info className="w-4 h-4 text-accent shrink-0 mt-0.5" />
            )}

            <div className="min-w-0 flex-1">
              <h4 className="text-xs font-semibold text-text">{t.title}</h4>
              {t.description && (
                <p className="text-[11px] text-text-2 mt-0.5 leading-snug">{t.description}</p>
              )}
            </div>

            <button
              onClick={() => dismissToast(t.id)}
              className="text-text-muted hover:text-text p-1"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        );
      })}
    </div>
  );
};
