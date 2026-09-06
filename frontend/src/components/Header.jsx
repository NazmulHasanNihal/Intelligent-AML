import React from 'react';
import { Shield, Lock, CheckCircle2 } from 'lucide-react';

export const Header = ({ healthStatus }) => {
  return (
    <header className="border-b border-slate-800/80 bg-[#050b1a]/90 backdrop-blur-md sticky top-0 z-50 px-6 py-3.5">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 via-sky-500 to-indigo-600 flex items-center justify-center text-xl shadow-glow">
            🏛️
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-lg font-bold text-white tracking-tight">Intelligent-AML</h1>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-cyan-500/15 text-cyan-400 border border-cyan-500/30 font-mono font-bold">
                C-STGB v1.0
              </span>
            </div>
            <p className="text-[11px] text-slate-400 font-medium">Enterprise FIU Intelligence Suite</p>
          </div>
        </div>

        {/* Status Badges */}
        <div className="flex items-center gap-2.5 text-xs font-mono">
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 font-bold text-[11px]">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>SYSTEM ACTIVE</span>
          </div>

          <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/30 text-[11px]">
            <Lock className="w-3.5 h-3.5" />
            <span>SR 26-2 & FinCEN Form 111</span>
          </div>
        </div>
      </div>
    </header>
  );
};
