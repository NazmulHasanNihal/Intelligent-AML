import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import { useAppStore } from './lib/store';
import { ErrorBoundary } from './components/common/ErrorBoundary';

// Layout Components
import { AppSidebar } from './components/layout/AppSidebar';
import { AppHeader } from './components/layout/AppHeader';
import { DemoBanner } from './components/layout/DemoBanner';
import { DemoToolsModal } from './components/DemoToolsModal';
import { SanctionsScreeningModal } from './components/SanctionsScreeningModal';
import { AccountFreezeNoticeModal } from './components/AccountFreezeNoticeModal';
import { WhatIfRecourseModal } from './components/WhatIfRecourseModal';
import { AdverseActionNoticeModal } from './components/AdverseActionNoticeModal';
import { RoleSwitchModal } from './components/RoleSwitchModal';
import { CoreBankingModal } from './components/CoreBankingModal';
import { PlainEnglishGuideModal } from './components/PlainEnglishGuideModal';
import { InspectorDrawer } from './components/ui/InspectorDrawer';
import { CommandDialog } from './components/ui/CommandDialog';
import { ToastContainer } from './components/ui/ToastContainer';

// Feature Views
import { OverviewView } from './features/overview/OverviewView';
import { MonitoringView } from './features/monitoring/MonitoringView';
import { ProfilesView } from './features/profiles/ProfilesView';
import { AlertsView } from './features/alerts/AlertsView';
import { CasesView } from './features/cases/CasesView';
import { CaseDetailView } from './features/cases/CaseDetailView';
import { NetworkView } from './features/network/NetworkView';
import { FilingsView } from './features/filings/FilingsView';
import { RequestsView } from './features/requests/RequestsView';
import { AuditView } from './features/audit/AuditView';
import { ModelsView } from './features/models/ModelsView';
import { SettingsView } from './features/settings/SettingsView';

function MainAppShell() {
  const routerNavigate = useNavigate();
  const location = useLocation();
  const activeRoute = useAppStore(state => state.activeRoute);
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(() => {
    return typeof window !== 'undefined' && window.innerWidth < 1024;
  });
  const [isCommandOpen, setIsCommandOpen] = useState(false);

  const validRoutes = ['overview', 'monitoring', 'profiles', 'alerts', 'cases', 'case-detail', 'network', 'filings', 'requests', 'audit', 'models', 'settings'];
  const rawPath = location.pathname.replace(/^\//, '') || 'overview';
  const resolvedRoute = validRoutes.includes(rawPath) ? rawPath : 'overview';

  // 1. Sync Browser URL changes (direct load, back/forward buttons) into Zustand
  useEffect(() => {
    if (useAppStore.getState().activeRoute !== resolvedRoute) {
      useAppStore.setState({ activeRoute: resolvedRoute, activeRouteParams: {} });
    }
  }, [resolvedRoute]);

  // 2. Sync programmatic Zustand updates (from modals, drawer buttons) to the Browser URL
  const isInitialMount = useRef(true);
  useEffect(() => {
    if (isInitialMount.current) {
      isInitialMount.current = false;
      return;
    }
    const currentPath = location.pathname.replace(/^\//, '') || 'overview';
    if (activeRoute && activeRoute !== currentPath) {
      const targetUrl = activeRoute === 'overview' ? '/' : `/${activeRoute}`;
      routerNavigate(targetUrl);
    }
  }, [activeRoute, location.pathname, routerNavigate]);

  // Global Keyboard Shortcuts (⌘K & Number Hotkeys 1-9)
  useEffect(() => {
    const handleKeyDown = (e) => {
      const isInput = e.target?.tagName === 'INPUT' || e.target?.tagName === 'TEXTAREA';

      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setIsCommandOpen(prev => !prev);
        return;
      }

      if (!isInput && !e.metaKey && !e.ctrlKey && !e.altKey) {
        const routeKeys = {
          '1': 'overview',
          'm': 'monitoring',
          'p': 'profiles',
          '2': 'alerts',
          '3': 'cases',
          '4': 'network',
          '5': 'filings',
          '6': 'requests',
          '7': 'audit',
          '8': 'models',
          '9': 'settings'
        };
        if (routeKeys[e.key]) {
          e.preventDefault();
          const target = routeKeys[e.key];
          const targetUrl = target === 'overview' ? '/' : `/${target}`;
          useAppStore.setState({ activeRoute: target, activeRouteParams: {} });
          routerNavigate(targetUrl);
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [routerNavigate]);

  return (
    <div className="flex h-screen bg-bg text-text font-sans overflow-hidden select-none">
      {/* Primary Navigation Sidebar */}
      <AppSidebar
        isCollapsed={isSidebarCollapsed}
        onToggleCollapse={() => setIsSidebarCollapsed(prev => !prev)}
      />

      {/* Main Content Workspace */}
      <div className="flex-1 flex flex-col h-screen overflow-y-auto bg-bg">
        {/* Modern Minimal Header */}
        <AppHeader onOpenCommandPalette={() => setIsCommandOpen(true)} />

        {/* Live Stream Simulation Banner */}
        <DemoBanner />

        {/* Dynamic Route Viewport */}
        <main className={`flex-1 w-full mx-auto transition-all ${
          activeRoute === 'network' ? 'p-2 sm:p-3 max-w-none' : 'p-4 sm:p-6 max-w-7xl'
        }`}>
          <div key={activeRoute} className="view-transition">
            {activeRoute === 'overview' && (
              <ErrorBoundary viewName="Overview Dashboard">
                <OverviewView />
              </ErrorBoundary>
            )}
            {activeRoute === 'monitoring' && (
              <ErrorBoundary viewName="Transaction Monitoring & Fraud Prevention Desk">
                <MonitoringView />
              </ErrorBoundary>
            )}
            {activeRoute === 'profiles' && (
              <ErrorBoundary viewName="Customer Profiles & Due Diligence Dossier">
                <ProfilesView />
              </ErrorBoundary>
            )}
            {activeRoute === 'alerts' && (
              <ErrorBoundary viewName="Alerts Triage Queue">
                <AlertsView />
              </ErrorBoundary>
            )}
            {activeRoute === 'cases' && (
              <ErrorBoundary viewName="Case Management Console">
                <CasesView />
              </ErrorBoundary>
            )}
            {activeRoute === 'case-detail' && (
              <ErrorBoundary viewName="Case Detail Dossier">
                <CaseDetailView />
              </ErrorBoundary>
            )}
            {activeRoute === 'network' && (
              <ErrorBoundary viewName="Network Graph Studio">
                <NetworkView />
              </ErrorBoundary>
            )}
            {activeRoute === 'filings' && (
              <ErrorBoundary viewName="Regulatory Filings Vault">
                <FilingsView />
              </ErrorBoundary>
            )}
            {activeRoute === 'requests' && (
              <ErrorBoundary viewName="RFI Compliance Desk">
                <RequestsView />
              </ErrorBoundary>
            )}
            {activeRoute === 'audit' && (
              <ErrorBoundary viewName="Cryptographic Audit Vault">
                <AuditView />
              </ErrorBoundary>
            )}
            {activeRoute === 'models' && (
              <ErrorBoundary viewName="Model Risk & Governance Console">
                <ModelsView />
              </ErrorBoundary>
            )}
            {activeRoute === 'settings' && (
              <ErrorBoundary viewName="Platform Governance Settings">
                <SettingsView />
              </ErrorBoundary>
            )}
          </div>
        </main>
      </div>

      {/* Shared Right-Side Inspector Drawer */}
      <InspectorDrawer />

      {/* Global ⌘K Command Dialog */}
      <CommandDialog
        isOpen={isCommandOpen}
        onClose={() => setIsCommandOpen(false)}
      />

      {/* Forensic Scenario & Attack Injector Modal */}
      <DemoToolsModal />

      {/* Automated Sanctions & PEP Compliance Screening Modal */}
      <SanctionsScreeningModal />

      {/* Statutory Account Freeze & Customer Remediation Notice Modal */}
      <AccountFreezeNoticeModal />

      {/* Counterfactual Behavioral Recourse Modal */}
      <WhatIfRecourseModal />

      {/* CFPB / FCRA Adverse Action Customer Notice Modal */}
      <AdverseActionNoticeModal />

      {/* Authorized Signatory Delegation Role Switch Modal */}
      <RoleSwitchModal />

      {/* Core Banking Freeze & Webhook Trigger Modal */}
      <CoreBankingModal />

      {/* Beginner-Friendly Plain-English Guide & Jargon Buster Modal */}
      <PlainEnglishGuideModal />

      {/* Minimalist Toast Notifications */}
      <ToastContainer />
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <ThemeProvider>
        <MainAppShell />
      </ThemeProvider>
    </AuthProvider>
  );
}
