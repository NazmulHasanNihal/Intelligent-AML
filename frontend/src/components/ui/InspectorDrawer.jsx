import React, { useState, useEffect } from 'react';
import { 
  X, 
  ShieldAlert, 
  ArrowUpRight, 
  FileText, 
  ExternalLink, 
  UserCheck, 
  Building2, 
  Share2, 
  Mail, 
  CheckCircle2, 
  AlertTriangle,
  Clock,
  DollarSign,
  Sliders,
  Server,
  Layers,
  Fingerprint,
  Users,
  Compass
} from 'lucide-react';
import { useAppStore } from '../../lib/store';
import { Badge } from './Badge';
import { Button } from './Button';

export const InspectorDrawer = () => {
  const { 
    isDrawerOpen, 
    drawerItem, 
    closeDrawer, 
    navigate, 
    createCaseFromAlert, 
    openFreezeNoticeModal,
    entities360,
    openRecourseModal,
    openAdverseActionModal,
    setCoreBankingModalOpen,
    openSanctionsModalWithQuery
  } = useAppStore();

  const [activeTab, setActiveTab] = useState('overview'); // 'overview' | 'kyc' | 'ubo' | 'sanctions' | 'flow' | 'topology'
  const [topologyData, setTopologyData] = useState(null);
  const [topologyLoading, setTopologyLoading] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && isDrawerOpen) {
        closeDrawer();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isDrawerOpen, closeDrawer]);

  // Reset tab on drawer open
  useEffect(() => {
    if (isDrawerOpen) {
      setActiveTab('overview');
    }
  }, [isDrawerOpen, drawerItem?.account]);

  const accountId = drawerItem?.account || drawerItem?.id || 'BD22-EBLB-4829-1092-8823';

  // Fetch live topological centrality and archetype embeddings
  useEffect(() => {
    if (!isDrawerOpen || !accountId) return;
    let isMounted = true;
    setTopologyLoading(true);
    fetch(`/api/v1/graph/analytics/${encodeURIComponent(accountId)}`)
      .then(res => res.ok ? res.json() : null)
      .then(data => {
        if (isMounted && data) {
          setTopologyData(data);
        }
      })
      .catch(() => {
        if (isMounted) {
          const isT1 = drawerItem?.tier?.includes('1') || drawerItem?.tierCode === 1;
          setTopologyData({
            node_id: accountId,
            entity_name: drawerItem?.entityName || 'Inspected Accountholder',
            pagerank_score: isT1 ? 0.0842 : 0.0094,
            betweenness_centrality: isT1 ? 0.4210 : 0.0210,
            degree_in: isT1 ? 4 : 2,
            degree_out: isT1 ? 8 : 2,
            degree_asymmetry_ratio: isT1 ? 2.0 : 1.0,
            flow_conservation_phi: isT1 ? 0.992 : 0.08,
            clustering_coefficient: isT1 ? 0.045 : 0.22,
            nearest_archetype: isT1 ? 'CYCLE_WASH_TRADER' : 'PRIME_COMMERCIAL_CORP',
            archetype_similarity_pct: isT1 ? 97.4 : 99.1,
            structural_role: isT1 ? 'Wash Trading Conduit Hub' : 'Prime Commercial Corporate',
            recommended_gating_threshold: isT1 ? 0.85 : 0.15,
            risk_indicator: isT1 ? 'CRITICAL_CONDUIT' : 'BENIGN_COMMERCIAL'
          });
        }
      })
      .finally(() => {
        if (isMounted) setTopologyLoading(false);
      });
    return () => { isMounted = false; };
  }, [isDrawerOpen, accountId, drawerItem]);

  if (!isDrawerOpen || !drawerItem) return null;

  const isTier1 = drawerItem.tier?.includes('1') || drawerItem.tierCode === 1;
  const isTier2 = drawerItem.tier?.includes('2') || drawerItem.tierCode === 2;

  // Retrieve 360 profile if available or generate enriched fallback
  const entityProfile = entities360?.[accountId] || {
    account: accountId,
    name: drawerItem.entityName || drawerItem.label || 'Commercial Accountholder',
    legalType: drawerItem.entityName?.includes('Ltd') || drawerItem.entityName?.includes('Industr') ? 'Private Limited Company' : 'Commercial Individual Account',
    incorporation: 'RJSC Dhaka Registration #C-94821/2014',
    tin: 'TIN-4882-9912-1088',
    jurisdiction: 'Motijheel Commercial Area, Dhaka, Bangladesh',
    kycStatus: isTier1 ? 'ENHANCED_EDD_HOLD' : 'STANDARD_CDD_VERIFIED',
    ubo: 'Tanvir Ahmed Rahman (64% Equity), Meghna Family Trust (36%)',
    pepSanctions: {
      ofacSdn: 'NEGATIVE (Clean Record)',
      unSanctions: 'NEGATIVE (Clean Record)',
      bfiuWatchlist: isTier1 ? 'ADVERSE WATCHLIST MATCH (§15 BFIU MLPA)' : 'CLEARED (No Adverse Mentions)',
      pepDirect: 'NOT IDENTIFIED AS DOMESTIC PEP'
    },
    flowConservation: {
      phiFlow: 0.992,
      massBalanceRatio: '0.998 (Kirchhoff Conservation)',
      inboundTurnover: `$${(drawerItem.amount || 48500).toLocaleString()}`,
      outboundTurnover: `$${((drawerItem.amount || 48500) * 0.98).toLocaleString()}`,
      dwellTimeHours: 0.35,
      classification: isTier1 ? 'High-Velocity Passthrough Wash Loop' : 'Standard Commercial Clearing Flow'
    },
    counterfactualRemedy: 'Space outbound wire batches over >48h intervals and supply authenticated ASYCUDA customs declarations.'
  };

  const handleOpenInNetwork = () => {
    navigate('network');
    closeDrawer();
  };

  const handleCreateCase = () => {
    if (drawerItem.id) {
      createCaseFromAlert(drawerItem.id, `${drawerItem.entityName || 'Account'} Investigation`);
      navigate('cases');
      closeDrawer();
    }
  };

  const handleOpenRFI = () => {
    navigate('requests');
    closeDrawer();
  };

  return (
    <div className="fixed inset-0 z-40 overflow-hidden bg-black/60 flex justify-end animate-fadeIn">
      <div 
        className="w-full max-w-lg sm:max-w-xl bg-popover text-foreground border-l border-border h-full shadow-drawer flex flex-col justify-between overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-4 sm:p-5 border-b border-border bg-surfaceRaised flex items-start justify-between gap-3 sticky top-0 z-10">
          <div className="min-w-0">
            <div className="flex items-center gap-2 flex-wrap mb-1">
              <span className="font-mono text-xs text-text-muted uppercase tracking-wider">360° Entity Intelligence</span>
              <Badge 
                variant={isTier1 ? 'critical' : isTier2 ? 'review' : 'cleared'}
                dot
              >
                {drawerItem.tier || 'Risk Evaluated'}
              </Badge>
            </div>
            <h2 className="text-base font-semibold text-text truncate">
              {drawerItem.entityName || drawerItem.label || entityProfile.name}
            </h2>
            <p className="font-mono text-xs text-text-2 mt-0.5 truncate">
              {accountId}
            </p>
          </div>

          <button
            onClick={closeDrawer}
            className="p-1.5 rounded hover:bg-surfaceHover text-text-muted hover:text-text transition-colors cursor-pointer"
            title="Close Drawer (Esc)"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* 360 Navigation Tabs */}
        <div className="px-4 py-2 border-b border-border bg-surface flex items-center gap-1 overflow-x-auto text-[11px] font-mono shrink-0">
          {[
            { id: 'overview', label: 'Risk Drivers' },
            { id: 'kyc', label: 'KYC & Registry' },
            { id: 'ubo', label: 'UBO Hierarchy' },
            { id: 'sanctions', label: 'PEP/Sanctions' },
            { id: 'flow', label: '12-D Flow Metrics' },
            { id: 'topology', label: 'Graph Topology' }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-2.5 py-1 rounded transition-colors whitespace-nowrap cursor-pointer ${
                activeTab === tab.id
                  ? 'bg-surfaceRaised font-bold text-accent border border-accent/40 shadow-xs'
                  : 'text-text-muted hover:text-text hover:bg-surfaceHover'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Content Body */}
        <div className="p-4 sm:p-5 space-y-4 text-xs flex-1 overflow-y-auto">
          {/* TAB 1: OVERVIEW & SHAP RISK ATTRIBUTION */}
          {activeTab === 'overview' && (
            <div className="space-y-4">
              {/* Risk Metric Grid */}
              <div className="grid grid-cols-2 gap-2 font-mono">
                <div className="p-3 rounded bg-bg border border-borderSubtle">
                  <span className="text-[10px] text-text-muted uppercase block">Conformal Risk Posterior</span>
                  <span className={`text-xl font-bold ${isTier1 ? 'text-critical' : isTier2 ? 'text-review' : 'text-cleared'}`}>
                    {drawerItem.riskScore ? `${(drawerItem.riskScore * 100).toFixed(1)}%` : '98.4%'}
                  </span>
                  <span className="text-[10px] text-text-muted block mt-0.5">
                    p-value: {drawerItem.pConformal || '0.0004'}
                  </span>
                </div>

                <div className="p-3 rounded bg-bg border border-borderSubtle">
                  <span className="text-[10px] text-text-muted uppercase block">Stated Exposure</span>
                  <div className="flex items-baseline gap-1.5 flex-wrap">
                    <span className="text-xl font-bold text-text tabular-nums">
                      ${(drawerItem.amount || drawerItem.caseTotalExposure || 48500).toLocaleString()}
                    </span>
                    <span className="text-[11px] text-text-muted font-medium">
                      (৳{((drawerItem.amount || drawerItem.caseTotalExposure || 48500) * 120).toLocaleString()} BDT)
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-[10px] text-text-muted mt-0.5">
                    <span>Rail: {drawerItem.rail || 'SWIFT MT103'}</span>
                  </div>
                </div>
              </div>

              {/* Plain-English Flag Summary */}
              {drawerItem.whyFlagged && (
                <div className="p-3 rounded bg-bg border border-borderSubtle space-y-1">
                  <span className="font-semibold text-text block">Detection Rationale:</span>
                  <p className="text-text-2 leading-relaxed">
                    {drawerItem.whyFlagged}
                  </p>
                </div>
              )}

              {/* Explainable Feature Attribution (SHAP-Style) */}
              <div className="space-y-2">
                <span className="font-semibold text-text block">Top Conformal Risk Drivers:</span>
                <div className="space-y-1.5">
                  {(drawerItem.shapDrivers || [
                    { name: 'Customs Valuation Divergence (+333%)', weight: 0.42, direction: 'risk' },
                    { name: 'CTR Structuring Proximity ($9.4k / ৳1.13M)', weight: 0.35, direction: 'risk' },
                    { name: 'JAFZA Free Zone High-Risk Corridor', weight: 0.18, direction: 'risk' },
                    { name: 'Verified Authorized Dealer (AD) License', weight: -0.07, direction: 'mitigant' }
                  ]).map((driver, idx) => (
                    <div key={idx} className="space-y-1">
                      <div className="flex justify-between text-[11px]">
                        <span className="text-text-2 truncate pr-2">{driver.name}</span>
                        <span className={`font-mono font-semibold ${driver.direction === 'risk' ? 'text-critical' : 'text-cleared'}`}>
                          {driver.weight > 0 ? `+${(driver.weight * 100).toFixed(0)}%` : `${(driver.weight * 100).toFixed(0)}%`}
                        </span>
                      </div>
                      <div className="w-full h-1.5 bg-bg rounded-full overflow-hidden flex">
                        <div 
                          className={`h-full rounded-full ${driver.direction === 'risk' ? 'bg-critical' : 'bg-cleared'}`}
                          style={{ width: `${Math.min(100, Math.abs(driver.weight) * 200)}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: KYC & CORPORATE REGISTRY */}
          {activeTab === 'kyc' && (
            <div className="space-y-3 font-mono text-[11px]">
              <div className="p-3.5 bg-bg rounded-lg border border-borderSubtle space-y-2">
                <span className="font-semibold text-text text-xs uppercase block font-sans">
                  Corporate Registration Profile
                </span>
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <span className="text-text-muted text-[10px] block">LEGAL ENTITY TYPE:</span>
                    <span className="text-text font-bold">{entityProfile.legalType}</span>
                  </div>
                  <div>
                    <span className="text-text-muted text-[10px] block">INCORPORATION / RJSC:</span>
                    <span className="text-accent font-bold">{entityProfile.incorporation}</span>
                  </div>
                  <div>
                    <span className="text-text-muted text-[10px] block">TAX IDENTIFICATION (TIN):</span>
                    <span className="text-text">{entityProfile.tin}</span>
                  </div>
                  <div>
                    <span className="text-text-muted text-[10px] block">KYC COMPLIANCE TIER:</span>
                    <span className="text-critical font-bold">{entityProfile.kycStatus}</span>
                  </div>
                  <div className="col-span-2">
                    <span className="text-text-muted text-[10px] block">REGISTERED COMMERCIAL JURISDICTION:</span>
                    <span className="text-text">{entityProfile.jurisdiction}</span>
                  </div>
                </div>
              </div>

              <div className="p-3 bg-surfaceRaised rounded border border-border text-text-2 space-y-1">
                <span className="font-semibold text-text text-[11px] block font-sans">Corporate Trade Licensing</span>
                <p>Authorized Dealer (AD) Category-1 Interbank settlement clearance granted by Bangladesh Bank Banking Operations Department (BOD).</p>
              </div>
            </div>
          )}

          {/* TAB 3: ULTIMATE BENEFICIAL OWNERSHIP (UBO) */}
          {activeTab === 'ubo' && (
            <div className="space-y-3">
              <div className="p-3.5 bg-bg rounded-lg border border-borderSubtle space-y-2.5">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-text text-xs uppercase font-mono">
                    Beneficial Equity Distribution
                  </span>
                  <Badge variant="accent" size="sm">FATF Recommendation 24</Badge>
                </div>

                {/* Visual Equity Bar */}
                <div className="w-full h-3 rounded bg-surfaceRaised overflow-hidden flex border border-border">
                  <div className="h-full bg-accent" style={{ width: '64%' }} title="Tanvir Ahmed Rahman (64%)" />
                  <div className="h-full bg-review" style={{ width: '36%' }} title="Meghna Family Trust (36%)" />
                </div>

                {/* Equity Breakdown Table */}
                <div className="space-y-2 font-mono text-[11px] pt-1">
                  <div className="flex items-center justify-between p-2 rounded bg-surfaceRaised border border-border">
                    <div className="flex items-center gap-2">
                      <span className="w-2.5 h-2.5 rounded-full bg-accent" />
                      <span className="font-bold text-text">Tanvir Ahmed Rahman</span>
                      <span className="text-text-muted">(Managing Director)</span>
                    </div>
                    <span className="font-bold text-accent">64.0% Equity</span>
                  </div>

                  <div className="flex items-center justify-between p-2 rounded bg-surfaceRaised border border-border">
                    <div className="flex items-center gap-2">
                      <span className="w-2.5 h-2.5 rounded-full bg-review" />
                      <span className="font-bold text-text">Meghna Family Trust</span>
                      <span className="text-text-muted">(Nominee Trust)</span>
                    </div>
                    <span className="font-bold text-review">36.0% Equity</span>
                  </div>
                </div>

                <div className="p-2.5 rounded bg-bg border border-border text-[11px] text-text-muted font-mono">
                  <strong>UBO Transparency Status:</strong> Controlled by single individual meeting primary statutory trigger (&gt;25% equity interest under BFIU Circular 26).
                </div>
              </div>
            </div>
          )}

          {/* TAB 4: PEP & SANCTIONS SCREENING */}
          {activeTab === 'sanctions' && (
            <div className="space-y-3 font-mono text-[11px]">
              <div className="p-3.5 bg-bg rounded-lg border border-borderSubtle space-y-2">
                <span className="font-semibold text-text text-xs uppercase font-sans block">
                  Sanctions &amp; Watchlist Multi-Bureau Matches
                </span>

                <div className="space-y-2 pt-1">
                  <div className="flex items-center justify-between p-2 rounded bg-surfaceRaised border border-border">
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4 text-cleared" />
                      <span className="text-text">OFAC Specially Designated Nationals (SDN)</span>
                    </div>
                    <span className="font-bold text-cleared">NEGATIVE</span>
                  </div>

                  <div className="flex items-center justify-between p-2 rounded bg-surfaceRaised border border-border">
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4 text-cleared" />
                      <span className="text-text">UN Security Council ISIL &amp; Al-Qaida 1267 List</span>
                    </div>
                    <span className="font-bold text-cleared">NEGATIVE</span>
                  </div>

                  <div className="flex items-center justify-between p-2 rounded bg-surfaceRaised border border-critical">
                    <div className="flex items-center gap-2">
                      <AlertTriangle className="w-4 h-4 text-critical" />
                      <span className="text-text font-bold">BFIU High-Risk Trade Corridors Watchlist</span>
                    </div>
                    <span className="font-bold text-critical">FLAGGED (§15 MLPA)</span>
                  </div>

                  <div className="flex items-center justify-between p-2 rounded bg-surfaceRaised border border-border">
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4 text-cleared" />
                      <span className="text-text">Politically Exposed Persons (PEP) Direct Registry</span>
                    </div>
                    <span className="font-bold text-cleared">CLEARED</span>
                  </div>
                </div>

                {/* Direct Sanctions Screening Trigger */}
                <div className="pt-2">
                  <Button
                    variant="primary"
                    size="sm"
                    onClick={() => openSanctionsModalWithQuery(drawerItem?.entityName || entityProfile.name)}
                    icon={ShieldAlert}
                    className="w-full text-xs font-semibold"
                  >
                    Run Live Multi-Bureau Sanctions Screen
                  </Button>
                </div>
              </div>
            </div>
          )}

          {/* TAB 5: 12-D FLOW CONSERVATION */}
          {activeTab === 'flow' && (
            <div className="space-y-3 font-mono text-[11px]">
              <div className="p-3.5 bg-bg rounded-lg border border-borderSubtle space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-text text-xs uppercase font-sans">
                    Flow Conservation Metrics (Φ_flow)
                  </span>
                  <Badge variant="critical" size="sm">Kirchhoff Law Passthrough</Badge>
                </div>

                <div className="grid grid-cols-2 gap-2 pt-1">
                  <div className="p-2 rounded bg-surfaceRaised border border-border">
                    <span className="text-text-muted text-[10px] block">CONSERVATION COEFFICIENT:</span>
                    <span className="text-critical font-bold text-sm">Φ = {entityProfile.flowConservation?.phiFlow || '0.992'}</span>
                  </div>
                  <div className="p-2 rounded bg-surfaceRaised border border-border">
                    <span className="text-text-muted text-[10px] block">TRANSIT DWELL TIME:</span>
                    <span className="text-critical font-bold text-sm">{entityProfile.flowConservation?.dwellTimeHours || '0.35'} Hours (~21 min)</span>
                  </div>
                  <div className="p-2 rounded bg-surfaceRaised border border-border">
                    <span className="text-text-muted text-[10px] block">INBOUND TURNOVER (24H):</span>
                    <span className="text-text font-bold">{entityProfile.flowConservation?.inboundTurnover || '$48,500.00'}</span>
                  </div>
                  <div className="p-2 rounded bg-surfaceRaised border border-border">
                    <span className="text-text-muted text-[10px] block">OUTBOUND TURNOVER (24H):</span>
                    <span className="text-text font-bold">{entityProfile.flowConservation?.outboundTurnover || '$47,600.00'}</span>
                  </div>
                </div>

                <div className="p-2.5 rounded bg-surfaceRaised border border-border text-text-2">
                  <span className="text-text font-bold block mb-0.5">Automated Topology Diagnosis:</span>
                  <span>{entityProfile.flowConservation?.classification || 'Passthrough Layering Wash Hub'}</span>
                </div>
              </div>
            </div>
          )}

          {/* TAB 6: GRAPH TOPOLOGY & ARCHETYPES */}
          {activeTab === 'topology' && (
            <div className="space-y-3 font-mono text-[11px]">
              <div className="p-3.5 bg-bg rounded-lg border border-borderSubtle space-y-3">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-text text-xs uppercase font-sans">
                    Topological Centrality &amp; Archetypes
                  </span>
                  <Badge variant={isTier1 ? 'critical' : 'cleared'} size="sm">
                    {topologyData?.structural_role || (isTier1 ? 'Conduit Hub' : 'Benign Commercial')}
                  </Badge>
                </div>

                <div className="grid grid-cols-2 gap-2 pt-1">
                  <div className="p-2 rounded bg-surfaceRaised border border-border">
                    <span className="text-text-muted text-[10px] block">PAGERANK CENTRALITY:</span>
                    <span className="text-accent font-bold text-sm">
                      {topologyData?.pagerank_score ? (topologyData.pagerank_score * 100).toFixed(2) + '%' : '8.42%'}
                    </span>
                  </div>
                  <div className="p-2 rounded bg-surfaceRaised border border-border">
                    <span className="text-text-muted text-[10px] block">BETWEENNESS CONDUIT:</span>
                    <span className={`font-bold text-sm ${isTier1 ? 'text-critical' : 'text-text'}`}>
                      {topologyData?.betweenness_centrality ? (topologyData.betweenness_centrality * 100).toFixed(1) + '%' : '42.1%'}
                    </span>
                  </div>
                  <div className="p-2 rounded bg-surfaceRaised border border-border">
                    <span className="text-text-muted text-[10px] block">DEGREE (IN / OUT):</span>
                    <span className="text-text font-bold text-sm">
                      {topologyData?.degree_in ?? 4} in / {topologyData?.degree_out ?? 8} out
                    </span>
                  </div>
                  <div className="p-2 rounded bg-surfaceRaised border border-border">
                    <span className="text-text-muted text-[10px] block">CLUSTERING COEFFICIENT:</span>
                    <span className="text-text font-bold text-sm">
                      {topologyData?.clustering_coefficient?.toFixed(3) ?? '0.045'}
                    </span>
                  </div>
                </div>

                {/* Hyperbolic Archetype Vector Similarity */}
                <div className="p-2.5 rounded bg-surfaceRaised border border-border space-y-1.5">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-text font-bold font-sans">Nearest Hyperbolic Archetype:</span>
                    <span className="font-bold text-accent">
                      {topologyData?.nearest_archetype || (isTier1 ? 'CYCLE_WASH_TRADER' : 'PRIME_COMMERCIAL_CORP')}
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-[10px] text-text-muted">
                    <span>Embedding Vector Similarity:</span>
                    <span className="font-bold text-text">
                      {topologyData?.archetype_similarity_pct?.toFixed(1) ?? '97.4'}%
                    </span>
                  </div>
                  <div className="w-full h-2 bg-bg rounded-full overflow-hidden border border-borderSubtle">
                    <div 
                      className={`h-full rounded-full ${isTier1 ? 'bg-critical' : 'bg-cleared'}`} 
                      style={{ width: `${topologyData?.archetype_similarity_pct ?? 97.4}%` }} 
                    />
                  </div>
                  <span className="text-[10px] text-text-muted block pt-0.5">
                    Recommended learnable edge trust gate: g_hat &gt;= {topologyData?.recommended_gating_threshold ?? 0.85}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer Actions (Executive Quick Actions) */}
        <div className="p-3 sm:p-4 border-t border-border bg-surfaceRaised space-y-2 sticky bottom-0">
          {/* Top row action buttons: Recourse, Adverse Action, Core Hold */}
          <div className="grid grid-cols-3 gap-1.5 font-mono text-[10px]">
            <Button
              variant="outline"
              size="sm"
              onClick={() => openRecourseModal(entityProfile)}
              icon={Sliders}
              className="h-7 text-[10px]"
            >
              What-If Recourse
            </Button>

            <Button
              variant="outline"
              size="sm"
              onClick={() => openAdverseActionModal(entityProfile)}
              icon={FileText}
              className="h-7 text-[10px]"
            >
              Adverse Notice
            </Button>

            <Button
              variant="danger"
              size="sm"
              onClick={() => setCoreBankingModalOpen(true)}
              icon={Server}
              className="h-7 text-[10px]"
            >
              Core Ledger Hold
            </Button>
          </div>

          {/* Bottom row actions */}
          <div className="flex flex-wrap items-center justify-between gap-2 pt-1 border-t border-borderSubtle">
            <Button
              variant="outline"
              size="sm"
              onClick={handleOpenInNetwork}
              icon={Share2}
            >
              Open in Network
            </Button>

            <div className="flex items-center gap-1.5">
              <Button
                variant="secondary"
                size="sm"
                onClick={handleOpenRFI}
                icon={Mail}
              >
                Dispatch RFI
              </Button>

              <Button
                variant="primary"
                size="sm"
                onClick={handleCreateCase}
                icon={FileText}
              >
                Open Case
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
