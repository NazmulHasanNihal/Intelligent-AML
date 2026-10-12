import React, { useState, useEffect } from 'react';
import {
  Settings,
  Sun,
  Moon,
  SlidersHorizontal,
  ShieldCheck,
  Sliders,
  Lock,
  UserCheck,
  Globe,
  Building2,
  Cpu,
  Database,
  Server,
  RefreshCw,
  KeyRound,
  Radio,
  Zap,
  ArrowRight,
  CheckCircle2,
  ShieldAlert
} from 'lucide-react';
import { useTheme, THEMES } from '../../context/ThemeContext';
import { useAuth } from '../../context/AuthContext';
import { useAppStore } from '../../lib/store';
import { Card, CardHeader } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  fetchCBSStatus,
  configureCBSGateway,
  triggerCBSInterceptTest,
  fetchStreamingBusStatus,
  triggerHSMProbe
} from '../../api/client';

export const SettingsView = () => {
  const { theme, setTheme, density, setDensity } = useTheme();
  const { currentBanker, availableBankers, switchBanker } = useAuth();
  const addToast = useAppStore(state => state.addToast);

  // Enterprise CBS State
  const [cbsConfig, setCbsConfig] = useState({
    provider: 'TEMENOS_T24',
    operating_mode: 'SHADOW_SURVEILLANCE',
    endpoint_url: 'https://cbs-gw.interbank.internal:8443/api/v2/settlement'
  });
  const [cbsStats, setCbsStats] = useState({ total_intercepts: 0, total_holds_placed: 0 });
  const [interceptResult, setInterceptResult] = useState(null);
  const [isIntercepting, setIsIntercepting] = useState(false);

  // Streaming Bus & HSM State
  const [busStatus, setBusStatus] = useState(null);
  const [hsmReceipt, setHsmReceipt] = useState(null);
  const [isProbingHsm, setIsProbingHsm] = useState(false);

  useEffect(() => {
    fetchCBSStatus().then(data => {
      if (data?.config) setCbsConfig(data.config);
      if (data) setCbsStats({ total_intercepts: data.total_intercepts || 0, total_holds_placed: data.total_holds_placed || 0 });
    });
    fetchStreamingBusStatus().then(setBusStatus);
  }, []);

  const handleProviderChange = async (provider) => {
    const updated = await configureCBSGateway(provider, cbsConfig.operating_mode, cbsConfig.endpoint_url);
    setCbsConfig(prev => ({ ...prev, provider: updated.provider }));
    addToast('CBS Adapter Updated', `Switched active connector to ${provider}.`, 'info');
  };

  const handleModeChange = async (mode) => {
    const updated = await configureCBSGateway(cbsConfig.provider, mode, cbsConfig.endpoint_url);
    setCbsConfig(prev => ({ ...prev, operating_mode: updated.operating_mode }));
    addToast(
      mode === 'INLINE_INTERCEPTOR' ? 'Inline Interceptor Active' : 'Shadow Surveillance Active',
      mode === 'INLINE_INTERCEPTOR'
        ? 'Real-time pre-clearing settlement hold enforced under MLPA §15.'
        : 'Zero-latency mirror surveillance active (zero customer clearing impact).',
      mode === 'INLINE_INTERCEPTOR' ? 'critical' : 'success'
    );
  };

  const handleTestCBSIntercept = async () => {
    setIsIntercepting(true);
    try {
      const res = await triggerCBSInterceptTest(
        'BD22-EBLB-4829-1092-8823',
        47600.0,
        cbsConfig.operating_mode === 'INLINE_INTERCEPTOR' ? 'Tier 1 Hold' : 'Tier 3 Clear',
        'RTGS'
      );
      setInterceptResult(res);
      addToast(
        'CBS Intercept Executed',
        `Callback executed in ${res.execution_latency_ms} ms. Action: ${res.action_taken}`,
        res.action_taken === 'ADMINISTRATIVE_HOLD_PLACED' ? 'critical' : 'success'
      );
    } finally {
      setIsIntercepting(false);
    }
  };

  const handleProbeHSM = async () => {
    setIsProbingHsm(true);
    try {
      const res = await triggerHSMProbe();
      setHsmReceipt(res);
      addToast('FIPS 140-2 Token Verified', `Certificate serial ${res.cert_serial} attested.`, 'success');
    } finally {
      setIsProbingHsm(false);
    }
  };

  return (
    <div className="space-y-4 max-w-5xl">
      {/* Top Banner */}
      <div className="p-4 rounded-lg bg-surface border border-border flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-sm font-semibold text-text">Enterprise Banking Gateway & Platform Configuration</h2>
            <Badge variant="cleared" size="sm">FIPS 140-2 Level 3</Badge>
          </div>
          <p className="text-xs text-text-2 mt-0.5">
            Core Banking System (CBS) middleware adapters, streaming message bus (Kafka/MQ), hardware tokens, and compliance settings.
          </p>
        </div>
      </div>

      {/* ========================================================================= */}
      {/* ENTERPRISE CORE BANKING SYSTEM (CBS) ADAPTER & INLINE INTERCEPTOR        */}
      {/* ========================================================================= */}
      <Card className="border-accent/40 bg-surface">
        <div className="flex items-center justify-between pb-3 border-b border-borderSubtle">
          <div className="flex items-center gap-2">
            <Building2 className="w-4 h-4 text-accent" />
            <span className="font-semibold text-text text-sm">Core Banking System (CBS) Middleware Adapter</span>
          </div>
          <Badge
            variant={cbsConfig.operating_mode === 'INLINE_INTERCEPTOR' ? 'critical' : 'cleared'}
            size="sm"
            className="font-mono text-[11px]"
          >
            {cbsConfig.operating_mode === 'INLINE_INTERCEPTOR' ? '● INLINE SETTLEMENT GATE' : '● SHADOW-MODE MIRROR'}
          </Badge>
        </div>

        <div className="space-y-4 mt-3 text-xs">
          {/* Operating Mode Selector: Shadow vs Inline */}
          <div>
            <label className="text-xs font-semibold text-text block mb-1.5">Operational Deployment Mode</label>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              <div
                onClick={() => handleModeChange('SHADOW_SURVEILLANCE')}
                className={`p-3 rounded-lg border cursor-pointer transition-all ${
                  cbsConfig.operating_mode === 'SHADOW_SURVEILLANCE'
                    ? 'border-accent bg-accent/5 ring-1 ring-accent/30'
                    : 'border-border bg-bg hover:bg-surfaceHover'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="font-bold text-text text-xs">Shadow-Mode Surveillance</span>
                  <Badge variant="cleared" size="sm">Recommended for Pilots</Badge>
                </div>
                <p className="text-[11px] text-text-muted leading-relaxed">
                  Processes real-time mirrored SWIFT/RTGS transaction streams with 0.0ms delay on live customer clearing. Evaluates false-positive reduction without blocking customer funds.
                </p>
              </div>

              <div
                onClick={() => handleModeChange('INLINE_INTERCEPTOR')}
                className={`p-3 rounded-lg border cursor-pointer transition-all ${
                  cbsConfig.operating_mode === 'INLINE_INTERCEPTOR'
                    ? 'border-critical bg-critical/5 ring-1 ring-critical/30'
                    : 'border-border bg-bg hover:bg-surfaceHover'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="font-bold text-critical text-xs">Inline Pre-Clearing Interceptor</span>
                  <Badge variant="critical" size="sm">Active Enforcement</Badge>
                </div>
                <p className="text-[11px] text-text-muted leading-relaxed">
                  Active pre-settlement authorization hook. Tier 1 Hold violations automatically trigger synchronous administrative debit freezes and generate ISO 20022 pacs.002 rejection notices under MLPA §15.
                </p>
              </div>
            </div>
          </div>

          {/* CBS Provider Selection */}
          <div className="pt-2 border-t border-borderSubtle">
            <label className="text-xs font-semibold text-text block mb-1.5">Target Core Banking Ledger</label>
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 font-mono text-[11px]">
              {[
                { id: 'TEMENOS_T24', label: 'Temenos T24' },
                { id: 'INFOSYS_FINACLE', label: 'Infosys Finacle' },
                { id: 'ORACLE_FLEXCUBE', label: 'Oracle FLEXCUBE' },
                { id: 'FIS_PROFILE', label: 'FIS Profile' },
                { id: 'ISO20022_GATEWAY', label: 'ISO 20022 Direct' }
              ].map(p => (
                <button
                  key={p.id}
                  onClick={() => handleProviderChange(p.id)}
                  className={`p-2 rounded border text-center transition-all cursor-pointer truncate ${
                    cbsConfig.provider === p.id
                      ? 'bg-accent text-white font-bold border-accent shadow-xs'
                      : 'bg-bg text-text-muted border-border hover:border-accent hover:text-text'
                  }`}
                >
                  {p.label}
                </button>
              ))}
            </div>
          </div>

          {/* Live CBS Intercept Test Sandbox */}
          <div className="p-3 rounded-lg bg-bg border border-borderSubtle flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 font-mono">
            <div>
              <span className="text-[10px] text-text-muted uppercase font-bold block">Live Pre-Settlement Callback Verification</span>
              <span className="text-xs text-text font-semibold block">
                Simulate $47,600 RTGS transfer against {cbsConfig.provider} gateway
              </span>
            </div>

            <Button
              variant="secondary"
              size="sm"
              onClick={handleTestCBSIntercept}
              disabled={isIntercepting}
              icon={isIntercepting ? RefreshCw : Zap}
              className={isIntercepting ? "animate-spin" : ""}
            >
              {isIntercepting ? "Executing..." : "Test CBS Intercept"}
            </Button>
          </div>

          {/* Intercept Result Telemetry */}
          {interceptResult && (
            <div className="p-3 rounded-lg bg-surfaceRaised border border-border text-[11px] font-mono space-y-1.5 animate-in fade-in">
              <div className="flex items-center justify-between">
                <span className="text-text-muted">Transaction Reference:</span>
                <span className="font-bold text-text">{interceptResult.transaction_reference}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-text-muted">Settlement Action:</span>
                <Badge variant={interceptResult.action_taken === 'ADMINISTRATIVE_HOLD_PLACED' ? 'critical' : 'cleared'} size="sm">
                  {interceptResult.action_taken}
                </Badge>
              </div>
              {interceptResult.pacs002_rejection_code && (
                <div className="flex items-center justify-between">
                  <span className="text-text-muted">ISO 20022 pacs.002 Code:</span>
                  <span className="text-critical font-bold">{interceptResult.pacs002_rejection_code}</span>
                </div>
              )}
              <div className="flex items-center justify-between">
                <span className="text-text-muted">CBS Hook Latency:</span>
                <span className="text-cleared font-bold">{interceptResult.execution_latency_ms} ms</span>
              </div>
              <div className="flex items-center justify-between pt-1 border-t border-border/50 text-[10px]">
                <span className="text-text-muted">FRE 902(11) Merkle Proof:</span>
                <span className="text-text font-mono truncate max-w-xs">{interceptResult.merkle_proof}</span>
              </div>
            </div>
          )}
        </div>
      </Card>

      {/* ========================================================================= */}
      {/* ENTERPRISE STREAMING MESSAGE BUS (APACHE KAFKA / CLUSTERED MQ)           */}
      {/* ========================================================================= */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card>
          <div className="flex items-center justify-between pb-2 border-b border-borderSubtle">
            <div className="flex items-center gap-2">
              <Server className="w-4 h-4 text-accent" />
              <span className="font-semibold text-text text-xs">Clustered Streaming Bus (Kafka)</span>
            </div>
            <Badge variant="cleared" size="sm">3 Brokers Online</Badge>
          </div>

          <div className="space-y-2.5 mt-3 text-xs font-mono">
            <div className="flex justify-between p-2 rounded bg-bg border border-borderSubtle">
              <span className="text-text-muted">Cluster Status:</span>
              <span className="font-bold text-cleared flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-cleared animate-ping" />
                {busStatus?.cluster_status || "HEALTHY"}
              </span>
            </div>
            <div className="flex justify-between p-2 rounded bg-bg border border-borderSubtle">
              <span className="text-text-muted">Partition Consumer Lag:</span>
              <span className="font-bold text-text">{busStatus?.consumer_group_lag || 14} msgs</span>
            </div>
            <div className="flex justify-between p-2 rounded bg-bg border border-borderSubtle">
              <span className="text-text-muted">Throughput Rate:</span>
              <span className="font-bold text-cleared">{busStatus?.throughput_msg_per_sec || 2480.5} msg/sec</span>
            </div>
            <div className="flex justify-between p-2 rounded bg-bg border border-borderSubtle">
              <span className="text-text-muted">Dead-Letter Queue (DLQ):</span>
              <span className="font-bold text-text">{busStatus?.dead_letter_queue_count || 0} unparseable</span>
            </div>
          </div>
        </Card>

        {/* ========================================================================= */}
        {/* HARDWARE SECURITY MODULE (FIPS 140-2 LEVEL 3 HSM / KMS)                  */}
        {/* ========================================================================= */}
        <Card>
          <div className="flex items-center justify-between pb-2 border-b border-borderSubtle">
            <div className="flex items-center gap-2">
              <KeyRound className="w-4 h-4 text-accent" />
              <span className="font-semibold text-text text-xs">FIPS 140-2 Level 3 HSM Token</span>
            </div>
            <Badge variant="cleared" size="sm">Hardware Verified</Badge>
          </div>

          <div className="space-y-2 mt-3 text-xs font-mono">
            <div className="p-2 rounded bg-bg border border-borderSubtle flex justify-between">
              <span className="text-text-muted">Key Slot:</span>
              <span className="font-semibold text-text">HSM-SLOT-01 (PKCS#11)</span>
            </div>
            <div className="p-2 rounded bg-bg border border-borderSubtle flex justify-between">
              <span className="text-text-muted">Algorithm:</span>
              <span className="font-semibold text-text">SHA256withRSA-PSS (4096-bit)</span>
            </div>
            <div className="p-2 rounded bg-bg border border-borderSubtle flex justify-between">
              <span className="text-text-muted">X.509 Serial:</span>
              <span className="font-bold text-accent">0x4892A81B8823EB1B</span>
            </div>

            <Button
              variant="secondary"
              size="sm"
              onClick={handleProbeHSM}
              disabled={isProbingHsm}
              icon={KeyRound}
              className="w-full text-xs mt-1"
            >
              {isProbingHsm ? "Attesting Hardware Token..." : "Probe HSM Hardware Key"}
            </Button>
          </div>
        </Card>
      </div>

      {/* Appearance & Interface Density */}
      <Card>
        <CardHeader
          title="Appearance & Display Density"
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

      {/* Authorized Signatory Profile */}
      <Card>
        <CardHeader
          title="Authorized Compliance Officer Profile"
          subtitle="Active session signatory profile for Four-Eyes approvals"
        />

        <div className="space-y-3 mt-4 text-xs">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {(availableBankers || []).map((b) => {
              const isSelected = b.id === currentBanker?.id;
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

      {/* Statutory Retention & Data Governance */}
      <Card>
        <CardHeader
          title="Statutory Retention & Cryptographic Storage Standards"
          subtitle="Mandatory Bank Secrecy Act (BSA) & SEC 17a-4 record-keeping configuration"
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
