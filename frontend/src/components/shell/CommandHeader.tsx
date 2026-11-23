'use client';

import React, { useState, useEffect } from 'react';
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
  Bell,
  Eye,
  EyeOff,
  RotateCcw,
  Check
} from 'lucide-react';
import { useTheme } from 'next-themes';
import { useBankingStore } from '@/lib/store';
import { JURISDICTIONS, JurisdictionCode } from '@/lib/compliance/jurisdictions';
import { APP_MODE, IS_ONPREM_MODE } from '@/lib/config/env';

export const CommandHeader: React.FC = () => {
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
    streamSpeed,
    setStreamSpeed,
    consumerLag,
    addToast,
    setCommandPaletteOpen,
    setNotificationDrawerOpen,
    notifications,
    revealPii,
    isPiiRevealed,
    resetWorkspaceData,
    language,
    toggleLanguage,
    displayCurrency,
    toggleDisplayCurrency
  } = useBankingStore();

  const [activePreset, setActivePreset] = useState<string>('TBML');
  const [isClient, setIsClient] = useState(false);
  const [isAirGap, setIsAirGap] = useState(false);

  useEffect(() => {
    setIsClient(true);
    if (typeof window !== 'undefined') {
      const host = window.location.hostname;
      setIsAirGap(host === 'localhost' || host === '127.0.0.1' || host.startsWith('192.168.') || host.startsWith('10.'));
    }
  }, []);

  const handleSelectPreset = (preset: string) => {
    setActivePreset(preset);
    addToast(
      'Operational Scenario Loaded',
      preset === 'TBML'
        ? 'Trade-Based Money Laundering: Over-invoicing +333.7% with rapid sub-$10,000 LC duplicate splitting.'
        : preset === 'STRUCTURING'
          ? 'Smurfing / Cash Structuring: Consecutive deposits of ৳954,000 BDT ($7,950) beneath ৳1,000,000 BDT statutory CTR ceiling (MLPA 2012 § 2(z) / BFIU Circular 26).'
          : preset === 'MULE'
            ? 'Mule Layering: Rapid pass-through across Dubai and Singapore corporate entities with zero overnight balance.'
            : 'Sanctions Evasion: High-risk counterparty flag in OFAC SDN / UN Security Council database.',
      'accent'
    );
  };

  const piiActive = isClient ? isPiiRevealed() : false;
  const unreadNotifCount = notifications.filter(n => !n.read).length;

  return (
    <header className="w-full h-14 px-3 sm:px-4 border-b border-[#1E293B] bg-[#0F172A]/95 backdrop-blur-md flex items-center justify-between gap-2 sm:gap-3 shrink-0 select-none max-w-full overflow-hidden">
      {/* Left: Brand Node, Environment Badge & Ingestion Stream */}
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

        {/* Mode & Deployment Badge */}
        <div className="hidden xl:flex items-center gap-1.5 px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-[#0B0F17] border border-[#334155] text-slate-300">
          <span className={`w-1.5 h-1.5 rounded-full ${IS_ONPREM_MODE ? 'bg-cyan-400' : 'bg-emerald-400'}`} />
          <span>{IS_ONPREM_MODE ? 'DEPLOYMENT: AIR-GAP INTRANET (ON-PREM)' : 'DEPLOYMENT: PUBLIC RESEARCH DEMO'}</span>
        </div>

        {/* Global Stream Control Pill */}
        <div className="flex items-center gap-1 bg-[#0B0F17] p-0.5 rounded border border-[#334155]">
          <button
            onClick={toggleStreamRunning}
            className={`px-2 py-1 rounded text-[11px] font-mono font-semibold cursor-pointer transition-colors flex items-center gap-1.5 shrink-0 ${isStreamRunning
              ? 'bg-emerald-500/20 text-emerald-300 hover:bg-emerald-500/30'
              : 'bg-amber-500/20 text-amber-300 hover:bg-amber-500/30'
              }`}
            title={isStreamRunning ? "Pause Ingestion Stream" : "Resume Ingestion Stream"}
          >
            <Zap className="w-3 h-3 shrink-0" />
            <span className="hidden sm:inline">{isStreamRunning ? 'STREAM: SIMULATED' : 'STREAM: PAUSED'}</span>
            <span className="sm:hidden">{isStreamRunning ? 'SIMULATED' : 'PAUSED'}</span>
          </button>

          {isStreamRunning && (
            <div className="hidden md:flex items-center text-[10px] font-mono pr-1 text-slate-400">
              {([1, 2, 5] as const).map(speed => (
                <button
                  key={speed}
                  onClick={() => setStreamSpeed(speed)}
                  className={`px-1.5 py-0.5 rounded cursor-pointer ${streamSpeed === speed ? 'bg-[#1E293B] text-emerald-400 font-bold' : 'hover:text-slate-200'
                    }`}
                >
                  {speed}x
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Scenarios Preset Dropdown */}
        <div className="hidden 2xl:flex items-center gap-1.5 px-2 py-1 rounded bg-[#0B0F17] border border-[#334155] text-xs font-mono">
          <Sparkles className="w-3.5 h-3.5 text-amber-400 shrink-0" />
          <select
            value={activePreset}
            onChange={(e) => handleSelectPreset(e.target.value)}
            className="bg-transparent text-slate-200 text-xs font-mono focus:outline-none cursor-pointer"
            title="Institutional Scenario Presets"
          >
            <option value="TBML" className="bg-[#0F172A] text-slate-200">Preset: TBML Over-Invoicing (+333.7%)</option>
            <option value="STRUCTURING" className="bg-[#0F172A] text-slate-200">Preset: Cash Smurfing (৳954,000 / $7,950)</option>
            <option value="MULE" className="bg-[#0F172A] text-slate-200">Preset: Pass-Through Mule Layering</option>
            <option value="SANCTION" className="bg-[#0F172A] text-slate-200">Preset: OFAC/UN Sanctions Match</option>
          </select>
        </div>
      </div>

      {/* Center: Command Palette Trigger */}
      <button
        type="button"
        onClick={() => setCommandPaletteOpen(true)}
        className="flex-1 max-w-xs px-3 py-1.5 rounded-lg bg-[#0B0F17] hover:bg-[#1E293B] border border-[#334155] text-xs text-slate-400 flex items-center justify-between gap-2 cursor-pointer transition-colors hidden md:flex"
      >
        <div className="flex items-center gap-2 truncate">
          <Search className="w-3.5 h-3.5 text-slate-500 shrink-0" />
          <span className="font-mono text-[11px] truncate">Search alerts, accounts, BICs (⌘K)...</span>
        </div>
        <kbd className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-[#0F172A] border border-[#334155] text-slate-400 shrink-0">
          ⌘K
        </kbd>
      </button>

      {/* Right: Jurisdiction, PII Reveal, Notification Bell, Theme & Officer Persona */}
      <div className="flex items-center gap-1.5 sm:gap-2 shrink-0">
        {/* Dynamic Jurisdiction Switcher */}
        <div className="flex items-center p-0.5 bg-[#0B0F17] rounded border border-[#334155] text-[11px] font-mono">
          {(['BD_BFIU', 'US_FINCEN', 'EU_AMLA'] as JurisdictionCode[]).map((jCode) => {
            const jur = JURISDICTIONS[jCode];
            const isSelected = activeJurisdiction === jCode;

            return (
              <button
                key={jCode}
                type="button"
                onClick={() => setActiveJurisdiction(jCode)}
                className={`px-2 py-0.5 rounded transition-colors cursor-pointer ${isSelected
                  ? 'bg-[#1E293B] font-bold text-emerald-400 border border-emerald-500/30 shadow-xs'
                  : 'text-slate-400 hover:text-slate-200'
                  }`}
                title={`${jur.name} (${jur.statutoryAct})`}
              >
                {jur.shortCode}
              </button>
            );
          })}
        </div>

        {/* Currency Switcher (BDT / USD) */}
        <button
          type="button"
          onClick={toggleDisplayCurrency}
          className="px-2 py-1 rounded text-xs font-mono font-bold bg-[#0B0F17] hover:bg-[#1E293B] text-emerald-400 border border-[#334155] transition-all cursor-pointer flex items-center gap-1"
          title={`Display Currency: ${displayCurrency}. Click to toggle BDT (৳) / USD ($) conversion.`}
        >
          <span>{displayCurrency === 'BDT' ? '৳ BDT' : '$ USD'}</span>
        </button>

        {/* Language Switcher (EN / BN) */}
        <button
          type="button"
          onClick={toggleLanguage}
          className="px-2 py-1 rounded text-xs font-mono font-bold bg-[#0B0F17] hover:bg-[#1E293B] text-slate-300 border border-[#334155] transition-all cursor-pointer flex items-center gap-1"
          title={`Active Language: ${language === 'en' ? 'English' : 'Bangla (বাংলা)'}. Click to switch.`}
        >
          <Globe className="w-3.5 h-3.5 text-cyan-400" />
          <span>{language === 'en' ? 'EN' : 'বাং'}</span>
        </button>

        {/* Link to Public Landing Page */}
        <Link
          href="/"
          className="px-2 py-1 rounded text-xs font-mono font-medium text-slate-400 hover:text-slate-100 border border-[#334155] hover:bg-[#1E293B] transition-all hidden xl:flex items-center gap-1.5"
          title="Exit to Public Marketing & Technical Landing Page"
        >
          <span>Public Site</span>
        </Link>

        {/* Audited 60-Second PII Reveal Button */}
        <button
          type="button"
          onClick={revealPii}
          className={`px-2 py-1 rounded text-xs font-mono font-semibold flex items-center gap-1.5 border transition-all cursor-pointer ${piiActive
            ? 'bg-amber-500/20 text-amber-300 border-amber-500/40 animate-pulse'
            : 'bg-[#0B0F17] text-slate-300 border-[#334155] hover:bg-[#1E293B]'
            }`}
          title={piiActive ? "PII is currently unmasked (Auto-expires in 60s)" : "Reveal PII globally for 60 seconds (Audited to WORM Ledger)"}
        >
          {piiActive ? <EyeOff className="w-3.5 h-3.5 text-amber-400" /> : <Eye className="w-3.5 h-3.5 text-slate-400" />}
          <span className="hidden xl:inline">{piiActive ? 'PII: UNMASKED' : 'Reveal PII'}</span>
        </button>

        {/* Operational Notification Bell */}
        <button
          type="button"
          onClick={() => setNotificationDrawerOpen(true)}
          className="relative p-1.5 sm:p-2 rounded hover:bg-[#1E293B] text-slate-400 hover:text-slate-200 border border-[#334155] transition-colors cursor-pointer"
          title="Open Operational Notifications"
        >
          <Bell className="w-3.5 h-3.5" />
          {unreadNotifCount > 0 && (
            <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-rose-600 text-white font-bold text-[9px] flex items-center justify-center font-mono">
              {unreadNotifCount}
            </span>
          )}
        </button>

        {/* Density Mode Toggle */}
        <button
          type="button"
          onClick={() => setDensityMode(densityMode === 'comfortable' ? 'compact' : 'comfortable')}
          className="p-1.5 sm:p-2 rounded hover:bg-[#1E293B] text-slate-400 hover:text-slate-200 border border-[#334155] transition-colors cursor-pointer hidden sm:block"
          title={`Switch to ${densityMode === 'comfortable' ? 'Compact' : 'Comfortable'} row density`}
        >
          <Sliders className="w-3.5 h-3.5" />
        </button>

        {/* Theme Switcher */}
        <button
          type="button"
          onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
          className="p-1.5 sm:p-2 rounded hover:bg-[#1E293B] text-slate-400 hover:text-slate-200 border border-[#334155] transition-colors cursor-pointer"
          title="Toggle Obsidian Dark / Institutional Light Theme"
        >
          {theme === 'dark' ? <Sun className="w-3.5 h-3.5 text-amber-400" /> : <Moon className="w-3.5 h-3.5 text-slate-700" />}
        </button>

        {/* Active Banker Persona & Step-Up Switcher */}
        <button
          type="button"
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
