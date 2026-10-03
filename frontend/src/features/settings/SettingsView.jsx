import React from 'react';
import { 
  Settings, 
  Sun, 
  Moon, 
  SlidersHorizontal, 
  ShieldCheck, 
  Sliders, 
  Lock, 
  UserCheck, 
  Globe 
} from 'lucide-react';
import { useTheme, THEMES } from '../../context/ThemeContext';
import { useAuth } from '../../context/AuthContext';
import { Card, CardHeader } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';

export const SettingsView = () => {
  const { theme, setTheme, density, setDensity } = useTheme();
  const { currentBanker, availableBankers, switchBanker } = useAuth();

  return (
    <div className="space-y-4 max-w-4xl">
      {/* Top Banner */}
      <div className="p-4 rounded-lg bg-surface border border-border">
        <h2 className="text-sm font-semibold text-text">Platform Settings &amp; Compliance Configuration</h2>
        <p className="text-xs text-text-2 mt-0.5">
          Configure interface density, visual themes, officer roles, and jurisdictional defaults.
        </p>
      </div>

      {/* Appearance & Interface Density */}
      <Card>
        <CardHeader
          title="Appearance &amp; Display Density"
          subtitle="Minimalist token-based styling settings"
        />

        <div className="space-y-4 mt-4 text-xs">
          {/* Theme Selector */}
          <div>
            <label className="text-xs font-semibold text-text block mb-2">Visual Theme</label>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
              {Object.values(THEMES).map((t) => {
                const isSelected = theme === t.id;
                return (
                  <button
                    key={t.id}
                    onClick={() => setTheme(t.id)}
                    className={`p-3 rounded border text-left transition-all cursor-pointer ${
                      isSelected 
                        ? 'border-accent bg-accent-subtle/50 font-semibold text-text shadow-sm' 
                        : 'border-border bg-bg hover:bg-surfaceHover text-text-2'
                    }`}
                  >
                    <div className="flex items-center gap-1.5 mb-1">
                      <span>{t.icon}</span>
                      <span className="text-xs font-semibold text-text">{t.name}</span>
                    </div>
                    <p className="text-[10px] text-text-muted leading-tight">{t.description}</p>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Density Selector */}
          <div className="pt-3 border-t border-borderSubtle">
            <label className="text-xs font-semibold text-text block mb-2">Interface Density</label>
            <div className="grid grid-cols-2 gap-2 max-w-md">
              <button
                onClick={() => setDensity('comfortable')}
                className={`p-3 rounded border text-left transition-all cursor-pointer ${
                  density === 'comfortable' 
                    ? 'border-accent bg-accent-subtle/50 font-semibold text-text' 
                    : 'border-border bg-bg hover:bg-surfaceHover text-text-2'
                }`}
              >
                <span className="font-semibold text-xs text-text block">Comfortable (Default)</span>
                <span className="text-[10px] text-text-muted">Standard padding for 1080p and touchscreens.</span>
              </button>

              <button
                onClick={() => setDensity('compact')}
                className={`p-3 rounded border text-left transition-all cursor-pointer ${
                  density === 'compact' 
                    ? 'border-accent bg-accent-subtle/50 font-semibold text-text' 
                    : 'border-border bg-bg hover:bg-surfaceHover text-text-2'
                }`}
              >
                <span className="font-semibold text-xs text-text block">Compact</span>
                <span className="text-[10px] text-text-muted">High-density rows for multi-monitor analyst desks.</span>
              </button>
            </div>
          </div>
        </div>
      </Card>

      {/* Authorized Signatory & Dual-Control Persona */}
      <Card>
        <CardHeader
          title="Authorized Compliance Officer Profile"
          subtitle="Active session signatory profile for Four-Eyes approvals"
        />

        <div className="space-y-3 mt-4 text-xs">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {(availableBankers || []).map((b) => {
              const isSelected = b.id === currentBanker.id;
              return (
                <div
                  key={b.id}
                  onClick={() => switchBanker(b.id)}
                  className={`p-3 rounded border flex items-center justify-between gap-2 cursor-pointer transition-colors ${
                    isSelected ? 'border-accent bg-accent-subtle/40' : 'border-border bg-bg hover:bg-surfaceHover'
                  }`}
                >
                  <div>
                    <span className="font-semibold text-text block">{b.name}</span>
                    <span className="text-text-muted text-[11px] block">{b.roleTitle}</span>
                    <span className="font-mono text-[10px] text-accent block mt-0.5">{b.id} • {b.role}</span>
                  </div>
                  {isSelected && <Badge variant="accent" size="sm">Active</Badge>}
                </div>
              );
            })}
          </div>
        </div>
      </Card>

      {/* Regulatory Retention & Data Governance */}
      <Card>
        <CardHeader
          title="Statutory Retention &amp; Cryptographic Storage Standards"
          subtitle="Mandatory Bank Secrecy Act (BSA) &amp; SEC 17a-4 record-keeping configuration"
        />

        <div className="space-y-2.5 mt-3 text-xs text-text-2 leading-relaxed">
          <div className="flex justify-between py-1.5 border-b border-borderSubtle">
            <span>Mandatory Case Retention:</span>
            <span className="font-mono font-semibold text-text">5 Years (31 CFR § 1010.430)</span>
          </div>
          <div className="flex justify-between py-1.5 border-b border-borderSubtle">
            <span>Append-Only Cryptographic Anchor:</span>
            <span className="font-mono font-semibold text-text">SHA-256 Chained Block Root</span>
          </div>
          <div className="flex justify-between py-1.5">
            <span>Evidentiary Self-Authentication:</span>
            <span className="font-mono font-semibold text-text">Federal Rules of Evidence 902(11) Certified</span>
          </div>
        </div>
      </Card>
    </div>
  );
};
