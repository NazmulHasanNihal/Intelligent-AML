import React, { useState, useRef, useEffect } from 'react';
import { 
  Building2,
  ChevronRight, 
  BookOpen, 
  Sparkles, 
  UserCheck, 
  ShieldCheck, 
  Key, 
  Menu, 
  PanelLeftClose, 
  PanelLeft, 
  Bell, 
  Search, 
  Palette, 
  Check, 
  ChevronDown, 
  Command, 
  HelpCircle, 
  Shield, 
  Activity, 
  Database, 
  Cpu
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

const DATASET_OPTIONS = [
  { id: 'ibm_amlsim', name: 'SWIFT Wire (Banking Rails)', domain: 'SWIFT / Fedwire', scale: '300k nodes / 550k txs', scenario: 'Corporate Structuring Loop' },
  { id: 'paysim_bkash', name: 'MFS / bKash (Mobile Money)', domain: 'MFS Wallets', scale: '1.04M nodes / 1.04M txs', scenario: 'High-Velocity Smurfing Fan-Out' },
  { id: 'elliptic_v1', name: 'MiCA Crypto (Bitcoin UTXO)', domain: 'UTXO Ledger', scale: '203k nodes / 234k txs', scenario: 'Darknet UTXO Peeling Chain' },
  { id: 'eth_phishing', name: 'MiCA Crypto (Ethereum DeFi)', domain: 'Smart Contracts', scale: '2.97M nodes / 3.50M txs', scenario: 'ERC-20 Phishing Mesh' },
  { id: 'saml_d', name: 'SAML-D (15-Bank Clearing)', domain: 'Inter-Bank RTGS', scale: '980k nodes / 1.45M txs', scenario: 'Cross-Border Layering Cycle' },
];

export const TopNavbar = ({ activeTab, onOpenHelp, isSidebarCollapsed, onToggleSidebar, onOpenCommandPalette }) => {
  const { currentBanker, setIsAuthModalOpen, switchBanker, availableBankers } = useAuth();
  const { currentTheme, themeId, setTheme, availableThemes } = useTheme();
  
  const [selectedDataset, setSelectedDataset] = useState(DATASET_OPTIONS[0]);
  const [isDatasetOpen, setIsDatasetOpen] = useState(false);
  const [isThemeDropdownOpen, setIsThemeDropdownOpen] = useState(false);
  const [isPersonaOpen, setIsPersonaOpen] = useState(false);
  
  const themeDropdownRef = useRef(null);
  const datasetDropdownRef = useRef(null);
  const personaDropdownRef = useRef(null);

  // Close dropdowns on outside click
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (themeDropdownRef.current && !themeDropdownRef.current.contains(event.target)) {
        setIsThemeDropdownOpen(false);
      }
      if (datasetDropdownRef.current && !datasetDropdownRef.current.contains(event.target)) {
        setIsDatasetOpen(false);
      }
      if (personaDropdownRef.current && !personaDropdownRef.current.contains(event.target)) {
        setIsPersonaOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <header className="h-16 px-3 sm:px-4 sticky top-0 z-40 flex items-center justify-between gap-2.5 bg-[var(--bg-surface)] border-b border-[var(--border-subtle)] text-[var(--text-primary)] font-sans transition-colors duration-300 shadow-sm shrink-0">
      
      {/* Left: Brand / Sidebar Toggle + Active Scenario Stream Selector */}
      <div className="flex items-center gap-2 sm:gap-3 min-w-0">
        <button
          onClick={onToggleSidebar}
          className="p-2 rounded-xl bg-[var(--bg-card)] hover:bg-[var(--bg-card-hover)] text-[var(--text-secondary)] hover:text-[var(--text-primary)] border border-[var(--border-subtle)] transition-all cursor-pointer shadow-[var(--skeuo-btn)] active:translate-y-0.5 shrink-0"
          title={isSidebarCollapsed ? 'Expand Navigation Sidebar (Hotkeys: 1-6)' : 'Collapse Navigation Sidebar'}
        >
          {isSidebarCollapsed ? <PanelLeft className="w-4 h-4 text-[var(--accent-primary)]" /> : <PanelLeftClose className="w-4 h-4" />}
        </button>

        {/* Institutional Branding Banner */}
        <div className="flex items-center gap-2 pr-3 border-r border-[var(--border-subtle)] shrink-0">
          <div className="w-7 h-7 rounded-lg bg-gradient-to-b from-[#257843] to-[#144726] border border-[#113C21] flex items-center justify-center text-white shadow-sm">
            <Shield className="w-4 h-4 text-white" />
          </div>
          <div className="hidden md:block">
            <div className="flex items-center gap-1.5">
              <span className="font-bold text-xs font-mono text-[var(--text-primary)] uppercase tracking-wider block">Intelligent-AML</span>
              <span className="text-[8px] font-mono px-1 py-0.2 rounded bg-[var(--accent-primary)]/15 text-[var(--accent-primary)] font-bold border border-[var(--accent-primary)]/30">C-STGB</span>
            </div>
            <span className="text-[9px] text-[var(--text-muted)] font-mono block">Enterprise Surveillance Desk</span>
          </div>
        </div>

        {/* Scenario / Stream Selector (SWIFT, MFS/bKash, MiCA Crypto) */}
        <div className="relative shrink-0" ref={datasetDropdownRef}>
          <button
            onClick={() => setIsDatasetOpen(prev => !prev)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl skeuo-well text-xs font-mono text-[var(--text-primary)] transition-all cursor-pointer group hover:border-[var(--accent-primary)]"
          >
            <Database className="w-3.5 h-3.5 text-[var(--accent-primary)] shrink-0" />
            <span className="hidden sm:inline text-[var(--text-muted)] font-sans text-[11px]">Scenario:</span>
            <span className="font-bold text-[var(--accent-primary)] truncate max-w-[110px] sm:max-w-[180px] xl:max-w-none">{selectedDataset.name}</span>
            <ChevronDown className={`w-3.5 h-3.5 text-[var(--text-muted)] transition-transform ${isDatasetOpen ? 'rotate-180' : ''}`} />
          </button>

          {isDatasetOpen && (
            <div className="absolute left-0 mt-2 w-80 sm:w-96 p-2 rounded-2xl bg-[var(--bg-card-elevated)] border border-[var(--border-card)] shadow-[var(--skeuo-card-elevated)] z-50 animate-fadeIn backdrop-blur-2xl">
              <div className="px-2.5 py-1.5 text-[10px] font-mono text-[var(--text-muted)] uppercase tracking-wider border-b border-[var(--border-subtle)] mb-1.5 flex items-center justify-between">
                <span>Select Surveillance Scenario</span>
                <span className="text-[9px] text-[var(--accent-primary)] font-bold">5 Active Rails</span>
              </div>
              <div className="space-y-1">
                {DATASET_OPTIONS.map((ds) => {
                  const isSelected = ds.id === selectedDataset.id;
                  return (
                    <button
                      key={ds.id}
                      onClick={() => {
                        setSelectedDataset(ds);
                        setIsDatasetOpen(false);
                      }}
                      className={`w-full flex items-start justify-between p-2 rounded-xl text-left transition-all cursor-pointer ${
                        isSelected 
                          ? 'bg-[var(--accent-primary)]/15 border border-[var(--accent-primary)]/40 text-[var(--text-primary)] font-semibold shadow-sm' 
                          : 'hover:bg-black/[0.03] dark:hover:bg-white/[0.04] text-[var(--text-secondary)] border border-transparent'
                      }`}
                    >
                      <div className="min-w-0 pr-2">
                        <div className="text-xs font-bold text-[var(--text-primary)] flex items-center gap-1.5">
                          <span className="truncate">{ds.name}</span>
                          {isSelected && <Check className="w-3.5 h-3.5 text-[var(--accent-primary)] shrink-0" />}
                        </div>
                        <p className="text-[10px] text-[var(--accent-primary)] font-mono truncate">{ds.scenario}</p>
                        <span className="text-[9px] text-[var(--text-muted)] font-mono">{ds.scale}</span>
                      </div>
                      <span className="text-[8px] font-mono px-1.5 py-0.5 rounded bg-black/[0.05] dark:bg-white/[0.08] text-[var(--text-secondary)] uppercase shrink-0">
                        {ds.domain}
                      </span>
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>

        {/* Real-Time Live Server Latency Telemetry & Mode Indicator */}
        <div className="hidden md:flex items-center gap-1.5 lg:gap-2 text-[10px] font-mono shrink-0">
          <span className="flex items-center gap-1.5 px-2.5 py-1 rounded-full skeuo-well text-[var(--text-primary)] font-semibold">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="hidden xl:inline">Telemetry:</span>
            <strong className="text-[var(--accent-primary)] font-mono">p99 &lt; 0.85ms</strong>
            <span className="text-[var(--text-muted)] hidden 2xl:inline">(avg: 0.42ms)</span>
          </span>
          <span className="hidden lg:flex px-2.5 py-1 rounded-full skeuo-well text-emerald-600 dark:text-emerald-400 font-semibold items-center gap-1">
            <Activity className="w-3 h-3" />
            <span>500 tx/s</span>
          </span>
          {/* Institutional Mode Badge (Synthetic Rails vs Live Stream) */}
          <span 
            className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-700 dark:text-emerald-300 font-semibold cursor-help"
            title="Operational Mode: Active Scenario Playback & Benchmark Engine. Sub-millisecond clearing active."
          >
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping" />
            <span className="text-[9px] tracking-wide uppercase">Synthetic Rails Active</span>
          </span>
        </div>
      </div>

      {/* Center: Recessed Skeuomorphic Search Well (Ctrl+K) */}
      <div className="hidden xl:flex shrink min-w-[160px] max-w-[220px] 2xl:max-w-xs mx-1">
        <button
          onClick={onOpenCommandPalette}
          className="w-full flex items-center justify-between px-3 py-1.5 rounded-xl bg-[var(--bg-base)] hover:border-[var(--accent-primary)] border border-[var(--border-subtle)] text-xs text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-all cursor-pointer skeuo-well group"
        >
          <div className="flex items-center gap-2 min-w-0">
            <Search className="w-3.5 h-3.5 text-[var(--accent-primary)] shrink-0" />
            <span className="text-[11px] text-[var(--text-muted)] group-hover:text-[var(--text-secondary)] truncate">Search entities, BICs...</span>
          </div>
          <div className="flex items-center gap-0.5 font-mono text-[9px] text-[var(--text-muted)] bg-[var(--bg-surface)] px-1.5 py-0.5 rounded border border-[var(--border-subtle)] shadow-inner shrink-0">
            <Command className="w-2.5 h-2.5" />
            <span>K</span>
          </div>
        </button>
      </div>

      {/* Mobile/Tablet Quick Search Icon */}
      <button
        onClick={onOpenCommandPalette}
        className="flex xl:hidden p-1.5 rounded-lg bg-[var(--bg-card)] hover:bg-[var(--bg-card-hover)] text-[var(--text-secondary)] hover:text-[var(--text-primary)] border border-[var(--border-subtle)] transition-all cursor-pointer shadow-[var(--skeuo-btn)] active:translate-y-0.5 shrink-0"
        title="Quick Search (Ctrl+K)"
      >
        <Search className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
      </button>

      {/* Right: Theme Switcher, Banker Profile & Knowledge Guide */}
      <div className="flex items-center gap-1.5 shrink-0">
        
        {/* Theme Switcher Dropdown */}
        <div className="relative" ref={themeDropdownRef}>
          <button
            onClick={() => setIsThemeDropdownOpen(prev => !prev)}
            className="flex items-center gap-1 px-2 sm:px-2.5 py-1 rounded-lg bg-[var(--bg-card)] hover:bg-[var(--bg-card-hover)] border border-[var(--border-card)] hover:border-[var(--accent-primary)] text-[11px] text-[var(--text-primary)] transition-all cursor-pointer shadow-[var(--skeuo-btn)] active:translate-y-0.5"
            title="Switch Aesthetic Theme"
          >
            <span className="text-xs">{currentTheme.icon}</span>
            <span className="hidden lg:inline-block font-semibold text-[10px] text-[var(--text-primary)]">{currentTheme.name}</span>
            <ChevronDown className={`w-3 h-3 text-[var(--text-muted)] transition-transform ${isThemeDropdownOpen ? 'rotate-180' : ''}`} />
          </button>

          {isThemeDropdownOpen && (
            <div className="absolute right-0 mt-1.5 w-72 sm:w-80 p-2 rounded-xl bg-[var(--bg-card-elevated)] border border-[var(--border-card)] shadow-[var(--skeuo-card-elevated)] z-50 animate-fadeIn backdrop-blur-2xl">
              <div className="px-2 py-1 text-[9px] font-mono text-[var(--text-muted)] uppercase tracking-wider border-b border-[var(--border-subtle)] mb-1 flex items-center justify-between">
                <span>Select Financial Theme</span>
                <Sparkles className="w-3 h-3 text-[var(--accent-primary)]" />
              </div>
              <div className="space-y-0.5">
                {Object.values(availableThemes).map((theme) => {
                  const isSelected = theme.id === themeId;
                  return (
                    <button
                      key={theme.id}
                      onClick={() => {
                        setTheme(theme.id);
                        setIsThemeDropdownOpen(false);
                      }}
                      className={`w-full flex items-start gap-2 p-1.5 rounded-lg text-left transition-all cursor-pointer ${
                        isSelected 
                          ? 'bg-[var(--accent-primary)]/15 border border-[var(--accent-primary)]/50 text-[var(--text-primary)] shadow-sm' 
                          : 'hover:bg-black/[0.03] dark:hover:bg-white/[0.04] text-[var(--text-secondary)] border border-transparent'
                      }`}
                    >
                      <span className="text-base mt-0.5">{theme.icon}</span>
                      <div className="flex-1">
                        <div className="flex items-center justify-between">
                          <span className="text-[11px] font-bold text-[var(--text-primary)]">{theme.name}</span>
                          {isSelected && <Check className="w-3 h-3 text-[var(--accent-primary)]" />}
                        </div>
                        <p className="text-[9px] text-[var(--text-muted)] mt-0.2">{theme.tagline}</p>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>

        {/* Active Banker Profile Badge & Quick Persona Switcher */}
        <div className="relative" ref={personaDropdownRef}>
          <button
            onClick={() => setIsPersonaOpen(prev => !prev)}
            className="flex items-center gap-1.5 px-2.5 sm:px-3 py-1.5 rounded-xl bg-[var(--bg-card)] hover:bg-[var(--bg-card-hover)] border border-[var(--border-card)] hover:border-[var(--accent-primary)] text-xs text-[var(--text-primary)] transition-all cursor-pointer shadow-[var(--skeuo-btn)] active:translate-y-0.5 group"
            title="Switch Officer Persona (Analyst L1, Investigator L2, CCO L3, Model Auditor)"
          >
            <div className={`w-5 h-5 rounded-md flex items-center justify-center text-[10px] font-bold ${currentBanker.badgeClass}`}>
              {currentBanker.avatar}
            </div>
            <div className="text-left font-sans hidden sm:block">
              <div className="text-[11px] font-bold text-[var(--text-primary)] group-hover:text-[var(--accent-primary)] flex items-center gap-1.5">
                <span className="truncate max-w-[120px]">{currentBanker.name}</span>
                <span className="text-[9px] px-1.5 py-0.5 rounded font-mono font-bold bg-black/[0.05] dark:bg-white/[0.08] text-[var(--text-secondary)] uppercase">
                  {currentBanker.role}
                </span>
              </div>
            </div>
            <ChevronDown className={`w-3 h-3 text-[var(--text-muted)] transition-transform ${isPersonaOpen ? 'rotate-180' : ''}`} />
          </button>

          {isPersonaOpen && (
            <div className="absolute right-0 mt-2 w-72 sm:w-80 p-2 rounded-2xl bg-[var(--bg-card-elevated)] border border-[var(--border-card)] shadow-[var(--skeuo-card-elevated)] z-50 animate-fadeIn backdrop-blur-2xl">
              <div className="px-2.5 py-1.5 text-[10px] font-mono text-[var(--text-muted)] uppercase tracking-wider border-b border-[var(--border-subtle)] mb-1.5 flex items-center justify-between">
                <span>Switch Banker Persona</span>
                <UserCheck className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
              </div>
              <div className="space-y-1">
                {(availableBankers || []).map((banker) => {
                  const isSelected = banker.id === currentBanker.id;
                  return (
                    <button
                      key={banker.id}
                      onClick={() => {
                        switchBanker(banker.id);
                        setIsPersonaOpen(false);
                      }}
                      className={`w-full flex items-center justify-between p-2 rounded-xl text-left transition-all cursor-pointer ${
                        isSelected 
                          ? 'bg-[var(--accent-primary)]/15 border border-[var(--accent-primary)]/40 text-[var(--text-primary)] font-semibold shadow-sm' 
                          : 'hover:bg-black/[0.03] dark:hover:bg-white/[0.04] text-[var(--text-secondary)] border border-transparent'
                      }`}
                    >
                      <div className="flex items-center gap-2 min-w-0">
                        <div className={`w-6 h-6 rounded-md flex items-center justify-center text-[10px] font-bold shrink-0 ${banker.badgeClass}`}>
                          {banker.avatar}
                        </div>
                        <div className="min-w-0">
                          <div className="text-xs font-bold text-[var(--text-primary)] truncate">{banker.name}</div>
                          <div className="text-[10px] text-[var(--text-muted)] truncate">{banker.roleTitle}</div>
                        </div>
                      </div>
                      {isSelected && <Check className="w-3.5 h-3.5 text-[var(--accent-primary)] shrink-0 ml-1.5" />}
                    </button>
                  );
                })}
              </div>
              <div className="pt-2 mt-1.5 border-t border-[var(--border-subtle)]">
                <button
                  onClick={() => {
                    setIsPersonaOpen(false);
                    setIsAuthModalOpen(true);
                  }}
                  className="w-full py-1.5 px-2 rounded-lg skeuo-btn text-xs text-[var(--accent-primary)] font-semibold text-center block"
                >
                  Manage Branch Credentials & Auth Key
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Knowledge Guide Button */}
        <button
          onClick={onOpenHelp}
          className="skeuo-btn skeuo-btn-primary px-2 sm:px-2.5 py-1 text-[11px] font-semibold shadow-sm"
          title="Banker Knowledge Center & Reference Manual"
        >
          <BookOpen className="w-3 h-3 text-white" />
          <span className="hidden md:inline-block text-[10px]">Manual</span>
        </button>
      </div>
    </header>
  );
};
