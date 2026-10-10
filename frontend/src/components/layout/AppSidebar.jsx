import React from 'react';
import { 
  LayoutDashboard, 
  AlertCircle, 
  Briefcase, 
  Share2, 
  FileText, 
  Mail, 
  ShieldCheck, 
  Cpu, 
  Settings,
  Shield,
  PanelLeftClose,
  PanelLeft,
  Users,
  ShieldAlert
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAppStore } from '../../lib/store';
import { Badge } from '../ui/Badge';

export const AppSidebar = ({ isCollapsed, onToggleCollapse }) => {
  const routerNavigate = useNavigate();
  const activeRoute = useAppStore(state => state.activeRoute);
  const alerts = useAppStore(state => state.alerts);
  const cases = useAppStore(state => state.cases);
  const blockedTransactions = useAppStore(state => state.blockedTransactions || []);

  const handleNavClick = (id) => {
    const targetUrl = id === 'overview' ? '/' : `/${id}`;
    useAppStore.setState({ activeRoute: id, activeRouteParams: {} });
    routerNavigate(targetUrl);
  };

  const primaryNav = [
    { id: 'overview', label: 'Overview', icon: LayoutDashboard, shortcut: '1' },
    { 
      id: 'monitoring', 
      label: 'Monitoring & Fraud', 
      icon: ShieldAlert, 
      shortcut: 'M',
      badge: `${blockedTransactions.filter(b => b.status === 'BLOCKED').length || 2}`
    },
    { 
      id: 'profiles', 
      label: 'Customer Profiles', 
      icon: Users, 
      shortcut: 'P' 
    },
    { 
      id: 'alerts', 
      label: 'Alerts', 
      icon: AlertCircle, 
      shortcut: '2',
      badge: `${alerts.filter(a => a.status !== 'DISMISSED' && a.status !== 'AUTO_CLEARED').length}` 
    },
    { 
      id: 'cases', 
      label: 'Cases', 
      icon: Briefcase, 
      shortcut: '3',
      badge: `${cases.length}` 
    },
    { id: 'network', label: 'Network', icon: Share2, shortcut: '4' },
    { id: 'filings', label: 'Filings', icon: FileText, shortcut: '5' },
    { id: 'requests', label: 'Requests (RFI)', icon: Mail, shortcut: '6' },
    { id: 'audit', label: 'Audit Vault', icon: ShieldCheck, shortcut: '7' }
  ];

  const secondaryNav = [
    { id: 'models', label: 'Engine & Health', icon: Cpu, shortcut: '8' },
    { id: 'settings', label: 'Settings', icon: Settings, shortcut: '9' }
  ];

  return (
    <aside className={`h-screen flex flex-col justify-between bg-surface border-r border-border shrink-0 z-30 transition-all duration-200 select-none ${
      isCollapsed ? 'w-14' : 'w-60'
    }`}>
      {/* Top: Brand Header */}
      <div>
        <div className="h-14 px-3.5 border-b border-border flex items-center justify-between">
          {!isCollapsed ? (
            <div className="flex items-center gap-2.5 min-w-0">
              <div className="w-7 h-7 rounded bg-accent flex items-center justify-center text-white shrink-0 shadow-sm">
                <Shield className="w-4 h-4 text-white" />
              </div>
              <div className="min-w-0">
                <h1 className="text-xs font-bold text-text truncate uppercase tracking-wider">
                  Intelligent-AML
                </h1>
                <p className="text-[10px] text-text-muted truncate">Enterprise Surveillance</p>
              </div>
            </div>
          ) : (
            <div className="w-7 h-7 rounded bg-accent flex items-center justify-center text-white mx-auto shadow-sm">
              <Shield className="w-4 h-4 text-white" />
            </div>
          )}

          <button
            onClick={onToggleCollapse}
            className="p-1 rounded hover:bg-surfaceHover text-text-muted hover:text-text block transition-colors cursor-pointer"
            title={isCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
            aria-label="Toggle sidebar collapse"
          >
            {isCollapsed ? <PanelLeft className="w-4 h-4" /> : <PanelLeftClose className="w-4 h-4" />}
          </button>
        </div>

        {/* Primary Navigation */}
        <div className="p-2 space-y-0.5">
          {!isCollapsed && (
            <div className="px-2 py-1 text-[10px] font-mono text-text-muted uppercase tracking-wider">
              Surveillance & Triage
            </div>
          )}

          {primaryNav.map((item) => {
            const Icon = item.icon;
            const isActive = activeRoute === item.id || (item.id === 'cases' && activeRoute === 'case-detail');

            return (
              <button
                key={item.id}
                onClick={() => handleNavClick(item.id)}
                className={`w-full flex items-center justify-between px-2.5 py-1.5 rounded text-xs transition-colors cursor-pointer group ${
                  isActive 
                    ? 'bg-accent-subtle text-accent-text font-semibold' 
                    : 'text-text-2 hover:bg-surfaceHover hover:text-text'
                } ${isCollapsed ? 'justify-center px-0' : ''}`}
                title={`${item.label} (Hotkey ${item.shortcut})`}
              >
                <div className="flex items-center gap-2.5 min-w-0">
                  <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-accent' : 'text-text-muted'}`} />
                  {!isCollapsed && <span className="truncate">{item.label}</span>}
                </div>

                {!isCollapsed && (
                  <div className="flex items-center gap-1.5">
                    {item.badge && (
                      <Badge variant={isActive ? 'accent' : 'neutral'} size="sm">
                        {item.badge}
                      </Badge>
                    )}
                    <kbd className="hidden group-hover:inline-block text-[9px] font-mono px-1 py-0.2 rounded bg-surfaceRaised text-text-muted border border-borderSubtle">
                      {item.shortcut}
                    </kbd>
                  </div>
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Bottom: Secondary / System Nav & Institutional Compliance Footer */}
      <div className="p-2 border-t border-border space-y-0.5">
        {!isCollapsed && (
          <div className="px-2 py-1 text-[10px] font-mono text-text-muted uppercase tracking-wider">
            Governance & Controls
          </div>
        )}

        {secondaryNav.map((item) => {
          const Icon = item.icon;
          const isActive = activeRoute === item.id;

          return (
            <button
              key={item.id}
              onClick={() => handleNavClick(item.id)}
              className={`w-full flex items-center justify-between px-2.5 py-1.5 rounded text-xs transition-colors cursor-pointer group ${
                isActive 
                  ? 'bg-accent-subtle text-accent-text font-semibold' 
                  : 'text-text-2 hover:bg-surfaceHover hover:text-text'
              } ${isCollapsed ? 'justify-center px-0' : ''}`}
              title={`${item.label} (Hotkey ${item.shortcut})`}
            >
              <div className="flex items-center gap-2.5 min-w-0">
                <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-accent' : 'text-text-muted'}`} />
                {!isCollapsed && <span className="truncate">{item.label}</span>}
              </div>

              {!isCollapsed && (
                <kbd className="hidden group-hover:inline-block text-[9px] font-mono px-1 py-0.2 rounded bg-surfaceRaised text-text-muted border border-borderSubtle">
                  {item.shortcut}
                </kbd>
              )}
            </button>
          );
        })}

        {!isCollapsed && (
          <div className="mt-2 p-2 rounded bg-surfaceRaised border border-borderSubtle text-[10px] text-text-muted font-mono leading-tight">
            <span>SR 11-7 / FRE 902(11)</span>
            <span className="block text-text-2 mt-0.5">Dual-Signatory Verified</span>
          </div>
        )}
      </div>
    </aside>
  );
};
