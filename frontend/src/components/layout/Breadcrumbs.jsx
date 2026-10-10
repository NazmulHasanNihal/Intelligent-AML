import React from 'react';
import { ChevronRight, Home } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAppStore } from '../../lib/store';

export const Breadcrumbs = () => {
  const routerNavigate = useNavigate();
  const activeRoute = useAppStore(state => state.activeRoute);
  const activeRouteParams = useAppStore(state => state.activeRouteParams);

  const routeHierarchy = {
    overview: {
      category: 'Surveillance',
      title: 'Overview Dashboard'
    },
    alerts: {
      category: 'Surveillance',
      title: 'Alert Triage Queue'
    },
    cases: {
      category: 'Investigations',
      title: 'Case Management'
    },
    'case-detail': {
      category: 'Investigations',
      parentRoute: 'cases',
      parentTitle: 'Case Management',
      title: activeRouteParams?.caseId ? `Docket ${activeRouteParams.caseId}` : 'Case Dossier'
    },
    network: {
      category: 'Forensics',
      title: 'Network Graph Studio'
    },
    filings: {
      category: 'Regulatory Filings',
      title: 'Autonomous SAR Vault'
    },
    requests: {
      category: 'Customer Operations',
      title: 'RFI & CDD Desk'
    },
    audit: {
      category: 'Governance & Risk',
      title: 'WORM Cryptographic Vault'
    },
    models: {
      category: 'Governance & Risk',
      title: 'Engine & Health Telemetry'
    },
    settings: {
      category: 'Administration',
      title: 'Platform Settings'
    }
  };

  const current = routeHierarchy[activeRoute] || { category: 'Surveillance', title: 'Intelligence Suite' };

  const handleNavigate = (route) => {
    const targetUrl = route === 'overview' ? '/' : `/${route}`;
    useAppStore.setState({ activeRoute: route, activeRouteParams: {} });
    routerNavigate(targetUrl);
  };

  return (
    <nav aria-label="Breadcrumb" className="flex items-center gap-1.5 text-xs select-none">
      <button
        onClick={() => handleNavigate('overview')}
        className="flex items-center gap-1 text-text-muted hover:text-text transition-colors cursor-pointer"
        title="Go to Overview Dashboard"
      >
        <Home className="w-3.5 h-3.5 text-text-muted" />
        <span className="hidden sm:inline font-medium">FIU</span>
      </button>

      <ChevronRight className="w-3 h-3 text-border shrink-0" />

      <span className="text-text-muted hidden md:inline truncate max-w-[120px]">
        {current.category}
      </span>

      {current.parentRoute && (
        <>
          <ChevronRight className="w-3 h-3 text-border shrink-0 hidden md:inline" />
          <button
            onClick={() => handleNavigate(current.parentRoute)}
            className="text-text-muted hover:text-text hover:underline transition-colors cursor-pointer truncate max-w-[120px]"
          >
            {current.parentTitle}
          </button>
        </>
      )}

      <ChevronRight className="w-3 h-3 text-border shrink-0" />

      <span className="font-semibold text-text truncate max-w-[160px] sm:max-w-[220px]">
        {current.title}
      </span>
    </nav>
  );
};
