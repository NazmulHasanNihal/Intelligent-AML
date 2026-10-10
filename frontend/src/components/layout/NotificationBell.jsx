import React, { useState } from 'react';
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';
import { 
  Bell, 
  ShieldAlert, 
  FileText, 
  CheckCircle2, 
  AlertTriangle, 
  Clock, 
  CheckCheck, 
  Trash2,
  ExternalLink
} from 'lucide-react';
import { useAppStore } from '../../lib/store';
import { Badge } from '../ui/Badge';

export const NotificationBell = () => {
  const { 
    alerts, 
    cases, 
    auditLogs, 
    navigate,
    openDrawer,
    selectCase 
  } = useAppStore();

  const [isOpen, setIsOpen] = useState(false);
  const [notifications, setNotifications] = useState([
    {
      id: 'notif-1',
      type: 'critical',
      title: 'Tier 1 Automated Hold Active',
      message: 'Meghna Agro ACCT-8823: High anomaly score (0.982) on SWIFT LC drawdown.',
      time: '3m ago',
      route: 'alerts',
      read: false
    },
    {
      id: 'notif-2',
      type: 'warning',
      title: 'Four-Eyes Dual Sign-off Required',
      message: 'Docket CASE-2026-0881 requires Senior MLRO approval under FinCEN BSA.',
      time: '18m ago',
      route: 'cases',
      read: false
    },
    {
      id: 'notif-3',
      type: 'success',
      title: 'FRE 902(11) Cryptographic Seal Certified',
      message: 'Audit ledger Merkle root signed with HSM FIPS 140-2 token.',
      time: '1h ago',
      route: 'audit',
      read: false
    },
    {
      id: 'notif-4',
      type: 'info',
      title: 'RFI Evidence Document Ingested',
      message: 'Commercial Invoice & Clean On Board B/L uploaded for RFI-2026-1091.',
      time: '2h ago',
      route: 'requests',
      read: true
    }
  ]);

  const unreadCount = notifications.filter(n => !n.read).length;

  const markAllAsRead = () => {
    setNotifications(prev => prev.map(n => ({ ...n, read: true })));
  };

  const clearNotification = (id, e) => {
    e.stopPropagation();
    setNotifications(prev => prev.filter(n => n.id !== id));
  };

  const handleNotificationClick = (item) => {
    setNotifications(prev => prev.map(n => n.id === item.id ? { ...n, read: true } : n));
    if (item.route) {
      if (item.route === 'cases' && cases.length > 0) {
        selectCase(cases[0].id);
      } else {
        useAppStore.setState({ activeRoute: item.route, activeRouteParams: {} });
        navigate(item.route);
      }
    }
  };

  const getIcon = (type) => {
    switch (type) {
      case 'critical':
        return <ShieldAlert className="w-3.5 h-3.5 text-critical shrink-0" />;
      case 'warning':
        return <AlertTriangle className="w-3.5 h-3.5 text-review shrink-0" />;
      case 'success':
        return <CheckCircle2 className="w-3.5 h-3.5 text-cleared shrink-0" />;
      default:
        return <FileText className="w-3.5 h-3.5 text-accent shrink-0" />;
    }
  };

  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <button
          className="relative p-2 rounded hover:bg-surfaceHover text-text-muted hover:text-text transition-colors cursor-pointer outline-none focus-visible:ring-1 focus-visible:ring-accent"
          title="Notifications & System Activity"
          aria-label="Notifications"
        >
          <Bell className="w-4 h-4" />
          {unreadCount > 0 && (
            <span className="absolute top-1 right-1 flex h-3.5 w-3.5 items-center justify-center rounded-full bg-critical text-[9px] font-bold text-white shadow-xs animate-pulse">
              {unreadCount}
            </span>
          )}
        </button>
      </DropdownMenu.Trigger>

      <DropdownMenu.Portal>
        <DropdownMenu.Content
          align="end"
          sideOffset={8}
          className="z-50 w-80 sm:w-96 rounded-xl border border-border bg-popover p-0 text-foreground shadow-2xl animate-fadeIn focus:outline-none overflow-hidden select-none"
        >
          {/* Header */}
          <div className="p-3 bg-surfaceRaised border-b border-border flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold uppercase tracking-wider text-text">Compliance Feed</span>
              {unreadCount > 0 ? (
                <Badge variant="critical" size="sm">{unreadCount} New</Badge>
              ) : (
                <Badge variant="cleared" size="sm">All Clear</Badge>
              )}
            </div>

            {unreadCount > 0 && (
              <button
                onClick={markAllAsRead}
                className="text-[11px] text-accent hover:underline flex items-center gap-1 cursor-pointer font-medium"
              >
                <CheckCheck className="w-3 h-3" />
                <span>Mark read</span>
              </button>
            )}
          </div>

          {/* Notification List */}
          <div className="max-h-80 overflow-y-auto divide-y divide-borderSubtle">
            {notifications.length === 0 ? (
              <div className="py-8 text-center text-text-muted text-xs">
                No active notifications.
              </div>
            ) : (
              notifications.map((item) => (
                <DropdownMenu.Item
                  key={item.id}
                  onSelect={() => handleNotificationClick(item)}
                  className={`p-3 flex items-start gap-3 transition-colors cursor-pointer outline-none ${
                    !item.read ? 'bg-surfaceRaised/60 hover:bg-surfaceHover' : 'hover:bg-surfaceHover/50'
                  }`}
                >
                  <div className="mt-0.5">{getIcon(item.type)}</div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between gap-1">
                      <span className={`text-xs font-semibold truncate ${!item.read ? 'text-text' : 'text-text-2'}`}>
                        {item.title}
                      </span>
                      <span className="text-[10px] text-text-muted shrink-0 font-mono flex items-center gap-1">
                        <Clock className="w-2.5 h-2.5" />
                        {item.time}
                      </span>
                    </div>
                    <p className="text-[11px] text-text-muted mt-0.5 line-clamp-2 leading-relaxed">
                      {item.message}
                    </p>
                  </div>
                  <button
                    onClick={(e) => clearNotification(item.id, e)}
                    className="p-1 hover:text-critical text-text-muted/60 transition-colors shrink-0"
                    title="Dismiss notification"
                  >
                    <Trash2 className="w-3 h-3" />
                  </button>
                </DropdownMenu.Item>
              ))
            )}
          </div>

          {/* Footer */}
          <div className="p-2 bg-surfaceRaised border-t border-border flex items-center justify-between text-[11px] font-mono text-text-muted">
            <span>Enterprise FIU Ingestion Engine</span>
            <span className="text-cleared flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-cleared inline-block animate-ping" />
              Connected
            </span>
          </div>
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
};
