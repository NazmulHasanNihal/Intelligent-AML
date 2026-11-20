'use client';

import React, { useState } from 'react';
import Link from 'next/link';
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
  Globe,
  Menu,
  X
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
    consumerLag,
    addToast
  } = useAppStore();

  const [activePreset, setActivePreset] = useState<string>('TBML');

  const handleSelectPreset = (preset: string) => {
    setActivePreset(preset);
    addToast(
      'Demo Scenario Loaded',
      preset === 'TBML'
        ? 'Trade-Based Money Laundering: Over-invoicing +333.7% with near-CTR structuring ($9,450).'
        : preset === 'STRUCTURING'
        ? 'Structuring / Smurfing: Rapid sequential wires under $10,000 CTR reporting threshold.'
        : preset === 'MULE'
        ? 'Mule Layering: Rapid pass-through across Dubai and Cayman entities.'
        : 'Sanctions Evasion: High-risk counterparty flag in OFAC/SDN database.',
      'accent'
    );
  };

  return (
    <header className="fixed top-0 left-0 right-0 h-14 px-3 sm:px-4 border-b border-[#1E293B] bg-[#0F172A]/95 backdrop-blur-md flex items-center justify-between gap-2 sm:gap-3 shrink-0 z-40 select-none max-w-full overflow-hidden">
      {/* Left: Brand Node & Ingestion Stream */}
      <div className="flex items-center gap-2 sm:gap-3 shrink-0">
        <Link href="/" className="flex items-center gap-2 pr-2 sm:pr-3 border-r border-[#1E293B] cursor-pointer">
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse shrink-0" />
          <span className="font-bold text-xs uppercase tracking-wider text-slate-100 hidden sm:inline">
            Intelligent-AML
          </span>
          <span className="px-1.5 py-0.5 rounded text-[10px] font-mono font-semibold bg-[#1E293B] text-slate-300 border border-[#334155]">
            v3.0
          </span>
        </Link>

        {/* Global Stream Control Pill */}
        <button
          onClick={toggleStreamRunning}
          className={`px-2 py-1 rounded text-xs font-mono font-semibold cursor-pointer transition-colors flex items-center gap-1.5 border shrink-0 ${
            isStreamRunning
              ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30 hover:bg-emerald-500/25'
              : 'bg-amber-500/15 text-amber-300 border-amber-500/30 hover:bg-amber-500/25'
          }`}
          title={isStreamRunning ? "Pause Ingestion Stream" : "Resume Ingestion Stream"}
        >
          <Zap className="w-3 h-3 shrink-0" />
          <span className="hidden sm:inline">{isStreamRunning ? 'STREAM: LIVE' : 'STREAM: PAUSED'}</span>
          <span className="sm:hidden">{isStreamRunning ? 'LIVE' : 'PAUSED'}</span>
        </button>

        {/* Live Fast-Path Telemetry Pill (hidden on narrow screens) */}
        <div className="hidden xl:flex items-center gap-2 px-2.5 py-1 rounded bg-[#0B0F17] border border-[#334155] text-xs font-mono tabular-nums">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 shrink-0" />
          <span className="text-slate-400">C-STGB:</span>
          <span className="font-bold text-slate-100">0.45 ms</span>
          <span className="text-slate-500 text-[10px]">(P99 &lt; 0.82ms)</span>
          <span className="text-slate-600">•</span>
          <span className="text-slate-400">Lag: <strong className="text-emerald-400 font-bold">{consumerLag} msgs</strong></span>
        </div>

        {/* Unified Scenario Presets Dropdown */}
        <div className="hidden lg:flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#0B0F17] border border-[#334155] text-xs font-mono">
          <Sparkles className="w-3.5 h-3.5 text-amber-400 shrink-0" />
          <select
            value={activePreset}
            onChange={(e) => handleSelectPreset(e.target.value)}
            className="bg-transparent text-slate-200 text-xs font-mono focus:outline-none cursor-pointer"
            title="Institutional Scenario Presets"
          >
            <option value="TBML" className="bg-[#0F172A] text-slate-200">Preset: TBML Over-Invoicing (+333.7%)</option>
            <option value="STRUCTURING" className="bg-[#0F172A] text-slate-200">Preset: Smurfing / CTR Evasion ($9,450)</option>
            <option value="MULE" className="bg-[#0F172A] text-slate-200">Preset: Fast Mule Layering (Dubai-Cayman)</option>
            <option value="SANCTION" className="bg-[#0F172A] text-slate-200">Preset: Sanctions Flag (OFAC/SDN)</option>
          </select>
        </div>
      </div>

      {/* Center: Command Palette Trigger */}
      <button
        onClick={onOpenCommandPalette}
        className="flex-1 max-w-xs px-3 py-1.5 rounded-lg bg-[#0B0F17] hover:bg-[#1E293B] border border-[#334155] text-xs text-slate-400 flex items-center justify-between gap-2 cursor-pointer transition-colors hidden md:flex"
      >
        <div className="flex items-center gap-2 truncate">
          <Search className="w-3.5 h-3.5 text-slate-500 shrink-0" />
          <span className="font-mono text-[11px] truncate">Search or ⌘K...</span>
        </div>
        <kbd className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-[#0F172A] border border-[#334155] text-slate-400 shrink-0">
          ⌘K
        </kbd>
      </button>

      {/* Right: Jurisdiction, Density, Theme & Officer Persona */}
      <div className="flex items-center gap-1.5 sm:gap-2 shrink-0">
        {/* Jurisdiction Switcher */}
        <div className="hidden 2xl:flex items-center p-0.5 bg-[#0B0F17] rounded border border-[#334155] text-[11px] font-mono">
          {[
            { id: 'US_FINCEN', label: 'FinCEN' },
            { id: 'BD_BFIU', label: 'BFIU' },
            { id: 'UN_GOAML', label: 'goAML' }
          ].map(j => (
            <button
              key={j.id}
              onClick={() => setActiveJurisdiction(j.id as any)}
              className={`px-2 py-0.5 rounded transition-colors cursor-pointer ${
                activeJurisdiction === j.id
                  ? 'bg-[#1E293B] font-bold text-slate-100 shadow-xs'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {j.label}
            </button>
          ))}
        </div>

        {/* Density Mode Toggle */}
        <button
          onClick={() => setDensityMode(densityMode === 'comfortable' ? 'compact' : 'comfortable')}
          className="p-1.5 sm:p-2 rounded hover:bg-[#1E293B] text-slate-400 hover:text-slate-200 border border-[#334155] transition-colors cursor-pointer"
          title={`Switch to ${densityMode === 'comfortable' ? 'Compact' : 'Comfortable'} row density`}
        >
          <Sliders className="w-3.5 h-3.5" />
        </button>

        {/* Theme Switcher */}
        <button
          onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
          className="p-1.5 sm:p-2 rounded hover:bg-[#1E293B] text-slate-400 hover:text-slate-200 border border-[#334155] transition-colors cursor-pointer"
          title="Toggle Dark Terminal / Federal Banknote Theme"
        >
          {theme === 'dark' ? <Sun className="w-3.5 h-3.5 text-amber-400" /> : <Moon className="w-3.5 h-3.5 text-slate-700" />}
        </button>

        {/* Active Banker Persona & Step-Up Switcher */}
        <button
          onClick={() => setRoleModalOpen(true)}
          className="flex items-center gap-1.5 sm:gap-2 px-2 sm:px-2.5 py-1 rounded-lg bg-[#0B0F17] hover:bg-[#1E293B] border border-[#334155] cursor-pointer transition-all text-xs font-mono shrink-0"
          title="Switch Authorized Signatory Role (Maker/Checker)"
        >
          <div className="w-5 h-5 rounded-full bg-emerald-500/20 border border-emerald-500/40 text-emerald-400 font-bold text-[10px] flex items-center justify-center shrink-0">
            {currentBanker.avatar}
          </div>
          <div className="text-left hidden sm:block">
            <span className="font-semibold text-slate-100 block leading-tight truncate max-w-[100px] lg:max-w-[120px]">
              {currentBanker.name.split(',')[0]}
            </span>
            <span className="text-[9px] text-slate-400 block leading-tight uppercase font-mono">
              {currentBanker.role}
            </span>
          </div>
          <ChevronDown className="w-3 h-3 text-slate-400 shrink-0" />
        </button>
      </div>
    </header>
  );
};
