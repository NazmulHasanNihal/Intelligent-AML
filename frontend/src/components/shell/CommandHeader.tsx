'use client';

import React from 'react';
import {
  Activity,
  Terminal,
  Sliders,
  Sun,
  Moon,
  Search,
  UserCheck,
  ShieldAlert,
  ChevronDown,
  Layers,
  Sparkles,
  Zap,
  Globe
} from 'lucide-react';
import { useTheme } from 'next-themes';
import { useAppStore } from '@/lib/store';
import { PiiText } from '@/components/ui/PiiText';

interface CommandHeaderProps {
  onOpenCommandPalette?: () => void;
}

export const CommandHeader: React.FC<CommandHeaderProps> = ({ onOpenCommandPalette = () => {} }) => {
  const { theme, setTheme } = useTheme();
  const {
    currentBanker,
    setRoleModalOpen,
    densityMode,
    setDensityMode,
    activeJurisdiction,
    setActiveJurisdiction,
    isStreamRunning,
    toggleStreamRunning,
    consumerLag
  } = useAppStore();

  return (
    <header className="h-14 px-4 border-b border-panel-border bg-panel/90 backdrop-blur-md flex items-center justify-between gap-3 shrink-0 z-30 select-none">
      {/* Left: Institution Node & Stream Telemetry */}
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 pr-3 border-r border-panel-border">
          <div className="w-2.5 h-2.5 rounded-full bg-tier3-emerald animate-pulse" />
          <span className="font-bold text-xs uppercase tracking-wider text-text-primary hidden sm:inline">
            Intelligent-AML
          </span>
          <span className="px-1.5 py-0.5 rounded text-[10px] font-mono font-semibold bg-panel-raised text-text-muted border border-panel-border">
            v3.0 PROD
          </span>
        </div>

        {/* Live Engine Telemetry Pill */}
        <div className="flex items-center gap-2 px-2.5 py-1 rounded bg-panel-raised border border-panel-border text-xs font-mono">
          <span className="w-1.5 h-1.5 rounded-full bg-tier3-emerald" />
          <span className="text-text-muted hidden md:inline">C-STGB Fast-Path:</span>
          <span className="font-bold text-text-primary">0.45 ms</span>
          <span className="text-text-dim text-[10px]">(P99 &lt; 0.82ms)</span>
          <span className="text-text-dim hidden lg:inline">•</span>
          <span className="text-text-muted hidden lg:inline">Lag: <strong className="text-tier3-emerald font-bold">{consumerLag} msgs</strong></span>
        </div>

        {/* Global Stream Controls */}
        <button
          onClick={toggleStreamRunning}
          className={`px-2 py-1 rounded text-xs font-mono font-semibold cursor-pointer transition-colors flex items-center gap-1.5 border ${
            isStreamRunning
              ? 'bg-tier3-emerald/15 text-tier3-emerald border-tier3-emerald/30 hover:bg-tier3-emerald/25'
              : 'bg-tier2-amber/15 text-tier2-amber border-tier2-amber/30 hover:bg-tier2-amber/25'
          }`}
          title={isStreamRunning ? "Pause Ingestion Stream" : "Resume Ingestion Stream"}
        >
          <Zap className="w-3 h-3" />
          <span>{isStreamRunning ? 'STREAM: LIVE' : 'STREAM: PAUSED'}</span>
        </button>
      </div>

      {/* Center: Command Palette Trigger */}
      <button
        onClick={onOpenCommandPalette}
        className="flex-1 max-w-sm px-3 py-1.5 rounded-lg bg-panel-raised hover:bg-panel-border border border-panel-border text-xs text-text-muted flex items-center justify-between gap-2 cursor-pointer transition-colors hidden md:flex"
      >
        <div className="flex items-center gap-2">
          <Search className="w-3.5 h-3.5 text-text-dim" />
          <span className="font-mono text-[11px]">Command Palette & Search...</span>
        </div>
        <kbd className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-canvas border border-panel-border text-text-dim">
          ⌘K
        </kbd>
      </button>

      {/* Right: Jurisdiction, Density, Theme & Officer Persona */}
      <div className="flex items-center gap-2">
        {/* Jurisdiction Switcher */}
        <div className="hidden xl:flex items-center p-0.5 bg-canvas rounded border border-panel-border text-[11px] font-mono">
          {[
            { id: 'US_FINCEN', label: 'FinCEN (US)' },
            { id: 'BD_BFIU', label: 'BFIU (BD)' },
            { id: 'UN_GOAML', label: 'goAML (UN)' }
          ].map(j => (
            <button
              key={j.id}
              onClick={() => setActiveJurisdiction(j.id as any)}
              className={`px-2 py-0.5 rounded transition-colors cursor-pointer ${
                activeJurisdiction === j.id
                  ? 'bg-panel font-bold text-text-primary shadow-xs'
                  : 'text-text-muted hover:text-text-primary'
              }`}
            >
              {j.label}
            </button>
          ))}
        </div>

        {/* Density Toggle */}
        <button
          onClick={() => setDensityMode(densityMode === 'comfortable' ? 'compact' : 'comfortable')}
          className="p-2 rounded hover:bg-panel-raised text-text-muted hover:text-text-primary border border-panel-border transition-colors cursor-pointer"
          title={`Switch to ${densityMode === 'comfortable' ? 'Compact' : 'Comfortable'} density`}
        >
          <Sliders className="w-3.5 h-3.5" />
        </button>

        {/* Theme Switcher */}
        <button
          onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
          className="p-2 rounded hover:bg-panel-raised text-text-muted hover:text-text-primary border border-panel-border transition-colors cursor-pointer"
          title="Toggle Dark Terminal / Federal Banknote Theme"
        >
          {theme === 'dark' ? <Sun className="w-3.5 h-3.5 text-amber-400" /> : <Moon className="w-3.5 h-3.5 text-slate-700" />}
        </button>

        {/* Active Banker Persona & Step-Up Switcher */}
        <button
          onClick={() => setRoleModalOpen(true)}
          className="flex items-center gap-2 px-2.5 py-1 rounded-lg bg-panel-raised hover:bg-panel-border border border-panel-border cursor-pointer transition-all text-xs font-mono"
          title="Click to Switch Authorized Signatory Role (Maker/Checker)"
        >
          <div className="w-5 h-5 rounded-full bg-brand-accent/20 border border-brand-accent/40 text-brand-accent font-bold text-[10px] flex items-center justify-center">
            {currentBanker.avatar}
          </div>
          <div className="text-left hidden sm:block">
            <span className="font-semibold text-text-primary block leading-tight truncate max-w-[120px]">
              {currentBanker.name.split(',')[0]}
            </span>
            <span className="text-[9px] text-text-dim block leading-tight uppercase font-mono">
              {currentBanker.role}
            </span>
          </div>
          <ChevronDown className="w-3 h-3 text-text-dim" />
        </button>
      </div>
    </header>
  );
};
