import React from 'react';
import { 
  Inbox, 
  Share2, 
  FileText, 
  ShieldCheck, 
  BarChart3, 
  BookOpen, 
  CheckCircle2, 
  Play, 
  Square,
  Building2,
  Lock,
  Search,
  UserCheck,
  HelpCircle,
  Sparkles,
  ShieldAlert,
  Zap,
  Activity,
  Layers,
  Scale,
  PanelLeftClose,
  PanelLeft,
  ChevronLeft,
  ChevronRight,
  Shield
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

const NAV_SECTIONS = [
  {
    category: 'Real-Time Surveillance',
    items: [
      {
        id: 'command-center',
        label: 'Surveillance & Telemetry',
        hotkey: '1',
        badge: 'Live Feed',
        badgeClass: 'bg-[#1B5E34]/15 text-[#1B5E34] dark:text-[#82C793] border-[#1B5E34]/30 shadow-sm font-semibold',
        desc: 'Streaming telemetry, risk gauges & scenarios',
        icon: Zap,
      },
    ],
  },
  {
    category: 'Risk Triage & Forensic Topology',
    items: [
      {
        id: 'alerts',
        label: 'Conformal Clearing Hub',
        hotkey: '2',
        badge: '3-Tier Triage',
        badgeClass: 'bg-amber-500/15 text-amber-800 dark:text-amber-300 border-amber-500/30 shadow-sm font-semibold',
        desc: 'Finite-sample risk control & queue matrix',
        icon: Inbox,
      },
      {
        id: 'investigate',
        label: '3D Forensic Graph Studio',
        hotkey: '3',
        badge: 'WebGL 3D',
        badgeClass: 'bg-[#1B5E34]/20 text-[#12381E] dark:text-[#82C793] border-[#1B5E34]/40 shadow-sm font-semibold',
        desc: 'Interactive peeling chains & wash loop visualizer',
        icon: Share2,
      },
    ],
  },
  {
    category: 'Statutory Filings & Recourse',
    items: [
      {
        id: 'cases',
        label: 'Autonomous SAR Drafter',
        hotkey: '4',
        badge: 'FinCEN 111',
        badgeClass: 'bg-rose-500/15 text-rose-800 dark:text-rose-300 border-rose-500/30 shadow-sm font-semibold',
        desc: 'Dual-copy legal dossiers & XML narratives',
        icon: FileText,
      },
      {
        id: 'recourse',
        label: 'Customer Recourse Sandbox',
        hotkey: '5',
        badge: 'Remediation',
        badgeClass: 'bg-[#1B5E34]/15 text-[#1B5E34] dark:text-[#82C793] border-[#1B5E34]/30 shadow-sm font-semibold',
        desc: 'Counterfactual optimizer & safe retry guides',
        icon: UserCheck,
      },
    ],
  },
  {
    category: 'Enterprise Model Governance',
    items: [
      {
        id: 'governance',
        label: 'Model Risk & SR 11-7 Vault',
        hotkey: '6',
        badge: 'Audited',
        badgeClass: 'bg-[#1B5E34]/25 text-[#12381E] dark:text-[#82C793] border-[#1B5E34]/50 shadow-sm font-semibold',
        desc: 'SHA-256 Merkle proofs & 13-benchmark scorecard',
        icon: BarChart3,
      },
    ],
  },
];

export const Sidebar = ({
  activeTab,
  setActiveTab,
  isTourActive,
  onToggleTour,
  onOpenHelp,
  isCollapsed,
  onToggleCollapse
}) => {
  const { currentBanker } = useAuth();
  const { currentTheme } = useTheme();

  const handleItemClick = (id) => {
    setActiveTab(id);
    if (typeof window !== 'undefined' && window.innerWidth < 640 && !isCollapsed) {
      onToggleCollapse();
    }
  };

  return (
    <aside className={`h-screen flex flex-col justify-between bg-[var(--bg-surface)] border-r border-[var(--border-subtle)] shrink-0 z-30 transition-all duration-300 ease-in-out ${
      isCollapsed ? 'hidden sm:flex sm:w-14' : 'fixed inset-y-0 left-0 z-50 w-64 xl:w-72 shadow-2xl sm:shadow-none sm:relative sm:z-30'
    }`}>
      {/* Top Brand Header */}
      <div>
        <div className={`p-2.5 sm:p-3 border-b border-[var(--border-subtle)] flex items-center justify-between ${
          isCollapsed ? 'px-2 justify-center' : ''
        }`}>
          {!isCollapsed ? (
            <div className="flex items-center gap-2.5 min-w-0">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-b from-[#257843] to-[#144726] border border-[#113C21] flex items-center justify-center text-white shadow-[var(--skeuo-btn)] shrink-0">
                <Shield className="w-4 h-4 text-white" />
              </div>
              <div className="min-w-0">
                <div className="flex items-center gap-1">
                  <span className="font-bold text-xs text-[var(--text-primary)] tracking-tight font-sans truncate">INTELLIGENT-AML</span>
                  <span className="text-[8px] font-mono px-1.5 py-0.5 rounded font-bold bg-[#1B5E34]/15 text-[#1B5E34] dark:text-[#82C793] border border-[#1B5E34]/30 shadow-sm shrink-0">
                    C-STGB
                  </span>
                </div>
                <span className="text-[9px] text-[var(--text-muted)] font-mono block">Enterprise Surveillance Desk</span>
              </div>
            </div>
          ) : (
            <div className="w-8 h-8 rounded-lg bg-gradient-to-b from-[#257843] to-[#144726] border border-[#113C21] flex items-center justify-center text-white shadow-[var(--skeuo-btn)]">
              <Shield className="w-4 h-4 text-white" />
            </div>
          )}

          <button
            onClick={onToggleCollapse}
            className={`p-1.5 rounded-lg skeuo-btn text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-all cursor-pointer ${
              isCollapsed ? 'hidden' : 'block'
            }`}
            title={isCollapsed ? 'Expand Navigation Sidebar (Hotkeys: 1-6)' : 'Collapse Navigation Sidebar'}
          >
            <PanelLeftClose className="w-4 h-4" />
          </button>
        </div>

        {/* Navigation Sections */}
        <nav className="p-1.5 sm:p-2 space-y-2 overflow-y-auto max-h-[calc(100vh-190px)]">
          {NAV_SECTIONS.map((section) => (
            <div key={section.category} className="space-y-1">
              {!isCollapsed && (
                <div className="px-2 pt-1 text-[9px] font-mono text-[var(--text-muted)] uppercase tracking-wider">
                  {section.category}
                </div>
              )}
              <div className="space-y-0.5">
                {section.items.map((item) => {
                  const Icon = item.icon;
                  const isActive = activeTab === item.id;
                  return (
                    <button
                      key={item.id}
                      onClick={() => handleItemClick(item.id)}
                      title={isCollapsed ? item.label : undefined}
                      className={`w-full flex items-center gap-2 px-2 py-1.5 rounded-lg text-left transition-all duration-150 cursor-pointer ${
                        isActive
                          ? 'bg-gradient-to-b from-[#257843] to-[#174E2B] border border-[#113C21] text-white shadow-[var(--skeuo-btn)] active:translate-y-0.5'
                          : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-black/[0.04] dark:hover:bg-white/[0.04] border border-transparent active:translate-y-0.5'
                      }`}
                    >
                      <div className={`p-1 rounded-md shrink-0 relative ${
                        isActive 
                          ? 'bg-black/20 text-white shadow-inner' 
                          : 'bg-black/[0.05] dark:bg-white/[0.08] text-[var(--text-secondary)]'
                      }`}>
                        <Icon className="w-3.5 h-3.5" />
                        {isActive && (
                          <span className="absolute -top-0.5 -right-0.5 w-1.5 h-1.5 rounded-full bg-emerald-400 shadow-[0_0_8px_#34d399] animate-pulse" />
                        )}
                      </div>
                      {!isCollapsed && (
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between gap-1">
                            <span className={`text-[11px] font-semibold truncate flex items-center gap-1.5 ${isActive ? 'text-white font-bold' : 'text-[var(--text-primary)]'}`}>
                              <span>{item.label}</span>
                              {isActive && (
                                <span className="w-1.5 h-1.5 rounded-full bg-emerald-300 shadow-sm animate-pulse" />
                              )}
                            </span>
                            <div className="flex items-center gap-1 shrink-0">
                              {item.hotkey && (
                                <span className={`text-[8px] font-mono px-1 py-0.2 rounded border ${isActive ? 'bg-white/10 border-white/20 text-white/90' : 'bg-black/[0.05] dark:bg-white/[0.05] text-[var(--text-muted)] border-[var(--border-subtle)]'}`}>
                                  {item.hotkey}
                                </span>
                              )}
                              {item.badge && (
                                <span className={`text-[8px] font-mono font-bold px-1.5 py-0.5 rounded border shrink-0 ${item.badgeClass}`}>
                                  {item.badge}
                                </span>
                              )}
                            </div>
                          </div>
                          <p className={`text-[9px] truncate ${isActive ? 'text-white/80' : 'text-[var(--text-muted)]'}`}>{item.desc}</p>
                        </div>
                      )}
                    </button>
                  );
                })}
              </div>
            </div>
          ))}
        </nav>
      </div>

      {/* Bottom Officer Status & System Telemetry */}
      <div className="p-2 border-t border-[var(--border-subtle)] bg-[var(--bg-card)]/50 space-y-1.5">
        {!isCollapsed && (
          <div className="p-1.5 rounded-lg bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)] flex items-center justify-between shadow-[var(--skeuo-card-shadow)] text-[10px]">
            <div className="flex items-center gap-1.5 truncate">
              <div className="w-1.5 h-1.5 rounded-full bg-[#1B5E34] dark:bg-[#82C793] animate-pulse shadow-sm shrink-0" />
              <span className="font-mono text-[var(--accent-primary)] font-semibold truncate">C-STGB Kernel Active</span>
            </div>
            <span className="font-mono text-[var(--text-secondary)] text-[9px] shrink-0">0.45ms</span>
          </div>
        )}

        <button
          onClick={onToggleTour}
          className={`w-full flex items-center justify-center gap-1.5 py-1.5 rounded-lg text-[11px] font-semibold transition-all cursor-pointer ${
            isTourActive
              ? 'bg-amber-500/20 text-amber-800 dark:text-amber-200 border border-amber-500/50 shadow-sm'
              : 'skeuo-btn skeuo-btn-secondary'
          }`}
          title="Interactive Step-by-Step Guided Tour"
        >
          <Sparkles className="w-3 h-3 text-[var(--accent-primary)]" />
          {!isCollapsed && <span>{isTourActive ? 'Exit Tour' : 'Banker Tour'}</span>}
        </button>
      </div>
    </aside>
  );
};
