import React, { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import { Sidebar } from './components/Sidebar';
import { TopNavbar } from './components/TopNavbar';
import { LiveStreamTicker } from './components/LiveStreamTicker';
import { WorkflowStageFooter } from './components/WorkflowStageFooter';
import { BankerHelpModal } from './components/BankerHelpModal';
import { InteractiveBankerTour } from './components/InteractiveBankerTour';
import { AccountProfileDrawer } from './components/AccountProfileDrawer';
import { CustomerNoticeModal } from './components/CustomerNoticeModal';
import { BankerActionModal } from './components/BankerActionModal';
import { BankerAuthModal } from './components/BankerAuthModal';
import { CommandPalette } from './components/CommandPalette';
import { checkHealth } from './api/client';

// Dynamic Code-Splitting: Lazy-load heavy consoles with Suspense
const UnifiedCommandCenter = React.lazy(() => import('./consoles/UnifiedCommandCenter').then(m => ({ default: m.UnifiedCommandCenter })));
const AlertTriageQueue = React.lazy(() => import('./consoles/AlertTriageQueue').then(m => ({ default: m.AlertTriageQueue })));
const ForensicGraphStudio = React.lazy(() => import('./consoles/ForensicGraphStudio').then(m => ({ default: m.ForensicGraphStudio })));
const MultiAgentSARWorkbench = React.lazy(() => import('./consoles/MultiAgentSARWorkbench').then(m => ({ default: m.MultiAgentSARWorkbench })));
const CounterfactualSandbox = React.lazy(() => import('./consoles/CounterfactualSandbox').then(m => ({ default: m.CounterfactualSandbox })));
const BenchmarkGovernanceHub = React.lazy(() => import('./consoles/BenchmarkGovernanceHub').then(m => ({ default: m.BenchmarkGovernanceHub })));

// Tactile Skeuomorphic Loading Skeleton during code chunk hydration
function TactileConsoleSkeleton() {
  return (
    <div className="space-y-3 sm:space-y-4 animate-pulse p-1 sm:p-2">
      {/* 4 Raised Skeuomorphic KPI Skeletons */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-2.5 sm:gap-3">
        {[1, 2, 3, 4].map(i => (
          <div key={i} className="h-20 sm:h-24 rounded-2xl skeuo-card p-3 flex flex-col justify-between">
            <div className="h-3 w-16 sm:w-24 bg-[var(--text-muted)]/20 rounded"></div>
            <div className="h-5 sm:h-6 w-24 sm:w-36 bg-[var(--accent-primary)]/20 rounded"></div>
          </div>
        ))}
      </div>
      {/* Main Visual Canvas Skeleton */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-3 sm:gap-4">
        <div className="lg:col-span-8 h-80 sm:h-96 rounded-2xl skeuo-card p-3 sm:p-4 flex flex-col justify-between">
          <div className="h-3 sm:h-4 w-32 sm:w-44 bg-[var(--text-muted)]/20 rounded"></div>
          <div className="h-64 sm:h-72 skeuo-well rounded-xl flex items-center justify-center">
            <div className="flex items-center gap-2 text-xs font-mono text-[var(--text-muted)]">
              <span className="w-2 h-2 rounded-full bg-[var(--accent-primary)] animate-ping" />
              <span>Hydrating Institutional Surface...</span>
            </div>
          </div>
        </div>
        <div className="lg:col-span-4 h-80 sm:h-96 rounded-2xl skeuo-card p-3 sm:p-4 flex flex-col gap-2.5 sm:gap-3">
          <div className="h-3 sm:h-4 w-28 sm:w-36 bg-[var(--text-muted)]/20 rounded"></div>
          <div className="h-16 sm:h-20 skeuo-well rounded-xl"></div>
          <div className="h-16 sm:h-20 skeuo-well rounded-xl"></div>
          <div className="h-16 sm:h-20 skeuo-well rounded-xl"></div>
        </div>
      </div>
    </div>
  );
}

function MainAppShell() {
  const { isAuthModalOpen, setIsAuthModalOpen } = useAuth();
  const [activeTab, setActiveTab] = useState('command-center');
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(() => typeof window !== 'undefined' && window.innerWidth < 1024);
  const [health, setHealth] = useState(null);
  const [isHelpOpen, setIsHelpOpen] = useState(false);
  const [isTourOpen, setIsTourOpen] = useState(false);
  const [tourStep, setTourStep] = useState(0);
  const [isLiveStreamActive, setIsLiveStreamActive] = useState(true);
  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState(false);

  // Modal State Controllers
  const [drawerAccount, setDrawerAccount] = useState(null);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [noticeAccount, setNoticeAccount] = useState(null);
  const [isNoticeOpen, setIsNoticeOpen] = useState(false);
  const [actionData, setActionData] = useState(null);
  const [isActionModalOpen, setIsActionModalOpen] = useState(false);

  // Single Source of Truth for Live Telemetry & Triage Counts
  const [globalStats, setGlobalStats] = useState({
    processed: 148312,
    quarantined: 1280,
    reviewQueue: 748,
    cleared: 146284,
    avgLatency: 0.45,
    p50: 0.38,
    p95: 0.62,
    p99: 0.82
  });

  useEffect(() => {
    const fetchHealth = async () => {
      const data = await checkHealth();
      setHealth(data);
    };
    fetchHealth();
  }, []);

  // Responsive sidebar collapse on smaller screens
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 1024) {
        setIsSidebarCollapsed(true);
      }
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Global Ctrl+K Command Palette and 1-6 Quick Console Switcher
  useEffect(() => {
    const handleKeyDown = (e) => {
      const targetTag = e.target?.tagName ? e.target.tagName.toLowerCase() : '';
      const isTyping = targetTag === 'input' || targetTag === 'textarea' || e.target?.isContentEditable;

      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setIsCommandPaletteOpen(prev => !prev);
        return;
      }

      // Quick Console Hotkeys: 1 to 6 (when not typing in form field)
      if (!isTyping && !e.ctrlKey && !e.metaKey && !e.altKey) {
        const consoleKeyMap = {
          '1': 'command-center',
          '2': 'alerts',
          '3': 'investigate',
          '4': 'cases',
          '5': 'recourse',
          '6': 'governance'
        };
        if (consoleKeyMap[e.key]) {
          e.preventDefault();
          setActiveTab(consoleKeyMap[e.key]);
        }
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleOpenAccountProfile = (account) => {
    setDrawerAccount(account);
    setIsDrawerOpen(true);
  };

  const handleOpenNoticeModal = (account) => {
    setNoticeAccount(account);
    setIsNoticeOpen(true);
  };

  const handleOpenActionModal = (action) => {
    setActionData(action);
    setIsActionModalOpen(true);
  };

  const handleStartTour = () => {
    setIsTourOpen(true);
    setTourStep(0);
    setActiveTab('command-center');
  };

  const handleNextTourStep = () => {
    const next = tourStep + 1;
    if (next < 6) {
      setTourStep(next);
      const tabMap = ['command-center', 'alerts', 'investigate', 'cases', 'recourse', 'governance'];
      setActiveTab(tabMap[next]);
    } else {
      setIsTourOpen(false);
      setTourStep(0);
    }
  };

  const handlePrevTourStep = () => {
    const prev = Math.max(0, tourStep - 1);
    setTourStep(prev);
    const tabMap = ['command-center', 'alerts', 'investigate', 'cases', 'recourse', 'governance'];
    setActiveTab(tabMap[prev]);
  };

  const handleJumpToTourTab = (tab, stepIdx) => {
    setActiveTab(tab);
    setTourStep(stepIdx);
  };

  return (
    <div className="flex h-screen bg-[var(--bg-base)] text-[var(--text-primary)] font-sans overflow-hidden transition-colors duration-300 relative">
      {/* Mobile Backdrop overlay when sidebar is open on small screens */}
      {!isSidebarCollapsed && (
        <div 
          className="fixed inset-0 bg-black/50 backdrop-blur-xs z-40 sm:hidden transition-opacity"
          onClick={() => setIsSidebarCollapsed(true)}
        />
      )}

      {/* Left Navigation Rail (Collapsible) */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        isTourActive={isTourOpen}
        onToggleTour={() => {
          if (isTourOpen) setIsTourOpen(false);
          else handleStartTour();
        }}
        onOpenHelp={() => setIsHelpOpen(true)}
        isCollapsed={isSidebarCollapsed}
        onToggleCollapse={() => setIsSidebarCollapsed(prev => !prev)}
      />

      {/* Main Content Workspace */}
      <div className="flex-1 flex flex-col h-screen overflow-y-auto bg-[var(--bg-base)] transition-colors duration-300">
        {/* Streamlined Top Navbar */}
        <TopNavbar
          activeTab={activeTab}
          onOpenHelp={() => setIsHelpOpen(true)}
          isSidebarCollapsed={isSidebarCollapsed}
          onToggleSidebar={() => setIsSidebarCollapsed(prev => !prev)}
          onOpenCommandPalette={() => setIsCommandPaletteOpen(true)}
        />

        {/* Central Consoles Workspace */}
        <main className="flex-1 p-2 sm:p-3 lg:p-3.5 space-y-2 sm:space-y-2.5 min-w-0">
          {/* Live Telemetry Ticker */}
          <LiveStreamTicker
            isActive={isLiveStreamActive}
            onSelectTx={() => setActiveTab('command-center')}
            sharedStats={globalStats}
            onStatsUpdate={setGlobalStats}
          />

          {/* Dynamic Console Switcher with Suspense Fallback */}
          <React.Suspense fallback={<TactileConsoleSkeleton />}>
            <div className="transition-opacity duration-200">
              {activeTab === 'command-center' && (
                <UnifiedCommandCenter
                  onNavigateToSAR={() => setActiveTab('cases')}
                  onNavigateToRecourse={() => setActiveTab('recourse')}
                  onOpenAccountProfile={handleOpenAccountProfile}
                  onOpenNoticeModal={handleOpenNoticeModal}
                  onOpenActionModal={handleOpenActionModal}
                />
              )}
              {activeTab === 'alerts' && (
                <AlertTriageQueue
                  onNavigateToGraph={() => setActiveTab('investigate')}
                  onNavigateToSAR={() => setActiveTab('cases')}
                  onOpenAccountProfile={handleOpenAccountProfile}
                  onOpenNoticeModal={handleOpenNoticeModal}
                  onOpenActionModal={handleOpenActionModal}
                  sharedStats={globalStats}
                />
              )}
              {activeTab === 'investigate' && (
                <ForensicGraphStudio
                  onNavigateToSAR={() => setActiveTab('cases')}
                  onOpenAccountProfile={handleOpenAccountProfile}
                />
              )}
              {activeTab === 'cases' && (
                <MultiAgentSARWorkbench
                  onOpenNoticeModal={handleOpenNoticeModal}
                  onOpenActionModal={handleOpenActionModal}
                />
              )}
              {activeTab === 'recourse' && (
                <CounterfactualSandbox
                  onOpenNoticeModal={handleOpenNoticeModal}
                />
              )}
              {activeTab === 'governance' && <BenchmarkGovernanceHub />}
            </div>
          </React.Suspense>

          {/* Workflow Stage Footer Navigation */}
          <WorkflowStageFooter activeTab={activeTab} setActiveTab={setActiveTab} />
        </main>
      </div>

      {/* Global Command Palette (Ctrl+K) */}
      <CommandPalette
        isOpen={isCommandPaletteOpen}
        onClose={() => setIsCommandPaletteOpen(false)}
        onNavigate={(tab) => {
          setActiveTab(tab);
          setIsCommandPaletteOpen(false);
        }}
      />

      {/* Account Profile Slide-Over Drawer */}
      <AccountProfileDrawer
        account={drawerAccount}
        isOpen={isDrawerOpen}
        onClose={() => setIsDrawerOpen(false)}
        onOpenGraph={() => {
          setIsDrawerOpen(false);
          setActiveTab('investigate');
        }}
        onOpenNotice={(acc) => {
          handleOpenNoticeModal(acc);
        }}
        onOpenActionModal={handleOpenActionModal}
      />

      {/* Customer Notice & Safe Retry Generator Modal */}
      <CustomerNoticeModal
        isOpen={isNoticeOpen}
        targetAccount={noticeAccount}
        onClose={() => setIsNoticeOpen(false)}
      />

      {/* Banker Operational Action Modal */}
      <BankerActionModal
        isOpen={isActionModalOpen}
        actionData={actionData}
        onClose={() => setIsActionModalOpen(false)}
      />

      {/* Banker Authentication & Role Switcher Modal */}
      <BankerAuthModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
      />

      {/* Banker Knowledge Center & Help Modal */}
      <BankerHelpModal
        isOpen={isHelpOpen}
        onClose={() => setIsHelpOpen(false)}
      />

      {/* Interactive Step-by-Step Banker Guided Tour */}
      <InteractiveBankerTour
        isOpen={isTourOpen}
        currentStep={tourStep}
        onNext={handleNextTourStep}
        onPrev={handlePrevTourStep}
        onClose={() => setIsTourOpen(false)}
        onJumpToTab={handleJumpToTourTab}
      />
    </div>
  );
}

export function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <MainAppShell />
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
