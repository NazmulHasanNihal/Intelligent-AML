import React, { useState } from 'react';
import { 
  Share2,
  Inbox, 
  Search, 
  Filter, 
  CheckCircle2, 
  AlertTriangle, 
  XCircle, 
  ArrowRight, 
  Clock, 
  Eye, 
  FileText, 
  ShieldAlert, 
  ExternalLink,
  ChevronRight,
  Zap,
  DollarSign,
  Shield,
  Layers,
  Activity,
  Sparkles,
  Database,
  GitBranch,
  Building2,
  User,
  UserCheck,
  Mail,
  Lock,
  Unlock,
  SlidersHorizontal,
  Download,
  UploadCloud
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { BatchCSVIngestModal } from '../components/BatchCSVIngestModal';

const ENTERPRISE_TRANSACTIONS = [
  {
    id: 'TX-994821',
    timestamp: '08:42:01 UTC',
    accountNumber: 'US-JPMC-4829-1092-8823',
    holderName: 'Apex Global Logistics Ltd',
    holderType: 'CORPORATE',
    institution: 'JPMorgan Chase Bank, N.A.',
    src: 'US-JPMC-4829-1092-8823',
    dst: 'GB-BARC-1109-8832-9011',
    counterpartyName: 'Elena Rostova (Transit Conduit)',
    amount: 48500,
    rail: 'SWIFT Wire (MT103)',
    jurisdiction: 'Offshore (Panama / BVI)',
    risk: 0.94,
    intervalLow: 0.884,
    intervalHigh: 0.972,
    gammaSet: '{1}',
    gammaLabel: 'Tier 1: Quarantine',
    tier: 'TIER_1_QUARANTINE',
    pattern: 'Apex Circular Wash Loop ($48,500 Total Exposure)',
    whyFlagged: 'Account received $48,500 from overseas and routed funds through 3 transit nodes in 21 mins with Φ_flow = 0.998, returning funds to originator with zero business absorption.',
    assignee: 'Sarah L. Jenkins, CFE',
    status: 'ESCALATED_SAR',
    featureDrivers: [
      { name: 'Flow Conservation (Φ=0.998)', impact: 38 },
      { name: 'Hawkes Velocity Spike', impact: 29 },
      { name: 'Offshore Route Corridor', impact: 19 },
      { name: 'Sub-Threshold Calibration', impact: 14 }
    ],
    burst: true,
    domain: 'Core Banking',
    slaDeadline: 'FinCEN 30-Day: 28d 14h left',
    slaUrgent: false
  },
  {
    id: 'TX-994819',
    timestamp: '08:41:58 UTC',
    accountNumber: 'bc1q9x4f8283a890cd3f71e920c83a9f828',
    holderName: 'Non-Custodial Transit Node (High-Risk Cluster)',
    holderType: 'CRYPTO_ENTITY',
    institution: 'On-Chain UTXO Ledger / Wasabi Protocol',
    src: 'bc1q9x4f8283a890cd3f71e920c83a9f828',
    dst: 'bc1qa58284919cd3f019a8b7c6d5e4f3a2b1c',
    counterpartyName: 'Anonymized Peeling Cluster #401',
    amount: 95000,
    rail: 'Bitcoin UTXO (Native SegWit)',
    jurisdiction: 'Decentralized (Unregistered)',
    risk: 0.98,
    intervalLow: 0.955,
    intervalHigh: 0.994,
    gammaSet: '{1}',
    gammaLabel: 'Tier 1: Quarantine',
    tier: 'TIER_1_QUARANTINE',
    pattern: 'Multi-Hop UTXO CoinJoin Peeling Chain',
    whyFlagged: 'Rapid peel chain splitting $95,000 across 7 micro-UTXO hops in under 4 minutes with high combinatorial entropy and privacy pool tags.',
    assignee: 'Sarah L. Jenkins, CFE',
    status: 'QUARANTINED',
    featureDrivers: [
      { name: 'Peeling Chain Entropy', impact: 44 },
      { name: 'CoinJoin Tag Match', impact: 32 },
      { name: 'Burst Velocity (λ=18.4)', impact: 24 }
    ],
    burst: true,
    domain: 'Crypto Assets',
    slaDeadline: 'BFIU 72-Hour: 18h 32m left',
    slaUrgent: true
  },
  {
    id: 'TX-994818',
    timestamp: '08:41:55 UTC',
    accountNumber: 'US-CITI-0019-4821-3901',
    holderName: 'Marcus Vance',
    holderType: 'RETAIL',
    institution: 'Citibank N.A. (New York)',
    src: 'US-CITI-0019',
    dst: 'SG-DBS-8819-4412-TRANSIT',
    counterpartyName: 'Marina Bay Trade Transit',
    amount: 4800,
    rail: 'ACH Direct Clearing',
    jurisdiction: 'Domestic (Clean)',
    risk: 0.52,
    intervalLow: 0.380,
    intervalHigh: 0.650,
    gammaSet: '{0, 1}',
    gammaLabel: 'Tier 2: Review Queue',
    tier: 'TIER_2_REVIEW_QUEUE',
    pattern: 'Dormant Account Rapid Activation ($4.8k)',
    whyFlagged: 'Account inactive for 14 months suddenly routed $4,800 to Singapore trade transit within 30 minutes of incoming deposit.',
    assignee: 'Musrat Jahan Gungun',
    status: 'UNDER_REVIEW',
    featureDrivers: [
      { name: 'Dormancy Delta (14 Mo)', impact: 46 },
      { name: 'Transit Velocity Ratio', impact: 34 },
      { name: 'Cross-Border Corridor', impact: 20 }
    ],
    burst: false,
    domain: 'Retail Banking',
    slaDeadline: 'FinCEN 30-Day: 29d 21h left',
    slaUrgent: false
  },
  {
    id: 'TX-994817',
    timestamp: '08:41:52 UTC',
    accountNumber: 'US-WF-0091-8841-2901',
    holderName: 'BlueWave Distribution Corp',
    holderType: 'CORPORATE',
    institution: 'Wells Fargo Bank, N.A.',
    src: 'US-WF-0091',
    dst: 'US-JPMC-2201-AMZN-AWS',
    counterpartyName: 'Amazon Web Services Inc',
    amount: 14250,
    rail: 'Fedwire Funds Service',
    jurisdiction: 'Domestic (Clean)',
    risk: 0.02,
    intervalLow: 0.005,
    intervalHigh: 0.045,
    gammaSet: '{0}',
    gammaLabel: 'Tier 3: Auto-Cleared',
    tier: 'TIER_3_STRAIGHT_THROUGH_CLEAR',
    pattern: 'Commercial Cloud Billing Settlement',
    whyFlagged: 'Matches standard recurring enterprise invoice history with verified AWS vendor credential.',
    assignee: 'Auto-Cleared',
    status: 'AUTO_CLEARED',
    featureDrivers: [
      { name: 'Verified Vendor Credential', impact: 85 },
      { name: 'Historical Baseline Match', impact: 15 }
    ],
    burst: false,
    domain: 'Commercial Banking',
    slaDeadline: 'Exempt / Auto-Cleared',
    slaUrgent: false
  },
  {
    id: 'TX-994816',
    timestamp: '08:41:48 UTC',
    accountNumber: 'DE-DB-9901-4412-8821',
    holderName: 'Rheinland Freight GmbH',
    holderType: 'CORPORATE',
    institution: 'Deutsche Bank (Frankfurt)',
    src: 'DE-DB-9901',
    dst: 'AE-SCBL-5512-8891-4412',
    counterpartyName: 'Horizon Trading DMCC',
    amount: 32400,
    rail: 'SEPA Cross-Border Wire',
    jurisdiction: 'EU / Middle East Corridor',
    risk: 0.42,
    intervalLow: 0.310,
    intervalHigh: 0.540,
    gammaSet: '{0, 1}',
    gammaLabel: 'Tier 2: Review Queue',
    tier: 'TIER_2_REVIEW_QUEUE',
    pattern: 'Cross-Border Supply Chain Settlement',
    whyFlagged: 'Intermediate amount transfer between regular corporate affiliates; low temporal Hawkes burst.',
    assignee: 'Musrat Jahan Gungun',
    status: 'UNDER_REVIEW',
    featureDrivers: [
      { name: 'Corridor Risk (Dubai Transit)', impact: 48 },
      { name: 'Affiliate Balance History', impact: 28 },
      { name: 'Standard Trade Cadence', impact: 24 }
    ],
    burst: false,
    domain: 'Commercial Banking',
    slaDeadline: 'goAML 5-Day: 4d 11h left',
    slaUrgent: false
  },
  {
    id: 'TX-994815',
    timestamp: '08:41:44 UTC',
    accountNumber: 'HK-HSBC-8812-9902-1144',
    holderName: 'Asia Pacific Trading Corp',
    holderType: 'CORPORATE',
    institution: 'HSBC Hong Kong',
    src: 'HK-HSBC-8812',
    dst: 'US-JPMC-4829-1092-8823',
    counterpartyName: 'Apex Global Logistics Ltd',
    amount: 47600,
    rail: 'SWIFT Wire (MT103)',
    jurisdiction: 'Hong Kong / US Corridor',
    risk: 0.96,
    intervalLow: 0.910,
    intervalHigh: 0.985,
    gammaSet: '{1}',
    gammaLabel: 'Tier 1: Quarantine',
    tier: 'TIER_1_QUARANTINE',
    pattern: 'Apex Coordinated Wash Return Leg ($47.6k)',
    whyFlagged: 'Feeder wire linked directly to Apex Global wash loop ring; completed return leg within 28 minutes of outbound transit.',
    assignee: 'Sarah L. Jenkins, CFE',
    status: 'QUARANTINED',
    featureDrivers: [
      { name: 'Loop Recurrence Factor', impact: 42 },
      { name: 'Velocity Acceleration (5.4x)', impact: 36 },
      { name: 'Volume Correlation', impact: 22 }
    ],
    burst: true,
    domain: 'Core Banking',
    slaDeadline: 'FinCEN 30-Day: 28d 14h left',
    slaUrgent: false
  }
];

export const AlertTriageQueue = ({ 
  onNavigateToGraph, 
  onNavigateToSAR, 
  onOpenAccountProfile,
  onOpenNoticeModal,
  onOpenActionModal,
  sharedStats 
}) => {
  const { currentBanker, logBankerAction } = useAuth();
  const [transactions, setTransactions] = useState(ENTERPRISE_TRANSACTIONS);
  const [activeTierFilter, setActiveTierFilter] = useState('ALL'); // 'ALL', 'TIER_1', 'TIER_2', 'TIER_3'
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTx, setSelectedTx] = useState(ENTERPRISE_TRANSACTIONS[0]);
  const [selectedTxIds, setSelectedTxIds] = useState(new Set());
  const [batchFeedback, setBatchFeedback] = useState(null);
  const [isBatchModalOpen, setIsBatchModalOpen] = useState(false);

  const handleImportBatch = (newTxs) => {
    setTransactions(prev => [...newTxs, ...prev]);
    if (newTxs.length > 0) {
      setSelectedTx(newTxs[0]);
    }
    setBatchFeedback(`✓ Successfully triaged and imported ${newTxs.length} flagged transactions into active queue.`);
    setTimeout(() => setBatchFeedback(null), 5000);
  };

  const toggleSelectTx = (id, e) => {
    e.stopPropagation();
    setSelectedTxIds(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const toggleSelectAll = () => {
    if (selectedTxIds.size === filteredTxs.length) {
      setSelectedTxIds(new Set());
    } else {
      setSelectedTxIds(new Set(filteredTxs.map(t => t.id)));
    }
  };

  const handleBatchQuarantine = () => {
    const count = selectedTxIds.size;
    logBankerAction(
      'BATCH_QUARANTINE_ASSETS',
      `Batch Four-Eyes Quarantine initiated for ${count} high-risk alerts. Core banking webhooks dispatched.`,
      { count, ids: Array.from(selectedTxIds) }
    );
    setBatchFeedback(`✓ Successfully initiated Four-Eyes Quarantine on ${count} accounts.`);
    setSelectedTxIds(new Set());
    setTimeout(() => setBatchFeedback(null), 4000);
  };

  const handleBatchRFI = () => {
    const count = selectedTxIds.size;
    logBankerAction(
      'BATCH_DISPATCH_RFI',
      `Automated Request for Information (RFI) dispatched to ${count} customer entities.`,
      { count, ids: Array.from(selectedTxIds) }
    );
    setBatchFeedback(`✉ Automated RFI questionnaires dispatched to ${count} counterparties.`);
    setSelectedTxIds(new Set());
    setTimeout(() => setBatchFeedback(null), 4000);
  };

  const handleBatchDismiss = () => {
    const count = selectedTxIds.size;
    logBankerAction(
      'BATCH_DISMISS_FALSE_POSITIVES',
      `Officer dismissed ${count} alerts as false-positives under EU AI Act oversight.`,
      { count, ids: Array.from(selectedTxIds) }
    );
    setBatchFeedback(`✓ Dismissed ${count} alerts as legitimate routine clearing.`);
    setSelectedTxIds(new Set());
    setTimeout(() => setBatchFeedback(null), 4000);
  };

  const filteredTxs = transactions.filter(tx => {
    const matchesTier = activeTierFilter === 'ALL' || tx.tier === activeTierFilter;
    const matchesSearch = 
      tx.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      tx.holderName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      tx.accountNumber.toLowerCase().includes(searchQuery.toLowerCase()) ||
      tx.pattern.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesTier && matchesSearch;
  });

  return (
    <div className="space-y-2.5 font-sans text-[var(--text-primary)] min-w-0">
      
      {/* Top Triage Metrics Header */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-2 sm:gap-2.5">
        <div className="skeuo-card p-2.5 sm:p-3 flex items-center justify-between">
          <div className="min-w-0 pr-1">
            <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] font-mono block uppercase truncate">TOTAL PROCESSED VOLUME</span>
            <span className="text-base sm:text-lg xl:text-xl font-bold text-[var(--text-primary)] font-mono block truncate">{sharedStats?.processed?.toLocaleString() || '148,312'} tx</span>
          </div>
          <div className="w-7 h-7 sm:w-8 sm:h-8 shrink-0 rounded-lg bg-gradient-to-b from-[#257843] to-[#144726] border border-[#113C21] flex items-center justify-center text-white shadow-[var(--skeuo-btn)]">
            <Zap className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-white" />
          </div>
        </div>

        <div className="skeuo-card p-2.5 sm:p-3 flex items-center justify-between border-rose-900/30">
          <div className="min-w-0 pr-1">
            <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] font-mono block uppercase truncate">TIER 1 QUARANTINED</span>
            <span className="text-base sm:text-lg xl:text-xl font-bold text-rose-600 dark:text-rose-400 font-mono block truncate">{sharedStats?.quarantined?.toLocaleString() || '1,280'} tx</span>
          </div>
          <div className="w-7 h-7 sm:w-8 sm:h-8 shrink-0 rounded-lg bg-rose-500/10 dark:bg-rose-950/40 border border-rose-500/30 flex items-center justify-center text-rose-600 dark:text-rose-400 shadow-[var(--skeuo-btn)]">
            <ShieldAlert className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
          </div>
        </div>

        <div className="skeuo-card p-2.5 sm:p-3 flex items-center justify-between border-amber-500/40">
          <div className="min-w-0 pr-1">
            <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] font-mono block uppercase truncate">TIER 2 REVIEW QUEUE</span>
            <span className="text-base sm:text-lg xl:text-xl font-bold text-amber-700 dark:text-amber-300 font-mono block truncate">{sharedStats?.reviewQueue?.toLocaleString() || '748'} tx</span>
          </div>
          <div className="w-7 h-7 sm:w-8 sm:h-8 shrink-0 rounded-lg bg-amber-500/10 dark:bg-amber-950/40 border border-amber-500/30 flex items-center justify-center text-amber-600 dark:text-amber-300 shadow-[var(--skeuo-btn)]">
            <AlertTriangle className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
          </div>
        </div>

        <div className="skeuo-card p-2.5 sm:p-3 flex items-center justify-between">
          <div className="min-w-0 pr-1">
            <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] font-mono block uppercase truncate">TIER 3 AUTO-CLEARED (&gt;98.6%)</span>
            <span className="text-base sm:text-lg xl:text-xl font-bold text-[var(--accent-primary)] font-mono block truncate">{sharedStats?.cleared?.toLocaleString() || '146,284'} tx</span>
          </div>
          <div className="w-7 h-7 sm:w-8 sm:h-8 shrink-0 rounded-lg bg-emerald-500/10 dark:bg-emerald-950/40 border border-emerald-500/30 flex items-center justify-center text-[var(--accent-primary)] shadow-[var(--skeuo-btn)]">
            <CheckCircle2 className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
          </div>
        </div>
      </div>

      {/* Main Grid: Data Table + Detail Inspector */}
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-2.5 sm:gap-3">
        
        {/* Left Column: Data Grid */}
        <div className="xl:col-span-8 skeuo-card p-2.5 sm:p-3 space-y-2 sm:space-y-2.5">
          
          {/* Controls Bar: Search & Filter Tabs & CSV Export */}
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 pb-2 border-b border-[var(--border-subtle)]">
            <div className="flex items-center gap-1 p-0.5 rounded-lg bg-[var(--bg-base)] border border-[var(--border-subtle)] overflow-x-auto w-full sm:w-auto shadow-inner">
              <button
                onClick={() => setActiveTierFilter('ALL')}
                className={`px-2 sm:px-2.5 py-1 rounded-md text-[10px] sm:text-[11px] font-semibold transition-all cursor-pointer ${
                  activeTierFilter === 'ALL' ? 'bg-gradient-to-b from-[#257843] to-[#174E2B] text-white font-bold shadow-[var(--skeuo-btn)]' : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
                }`}
              >
                Sample Queue ({filteredTxs.length})
              </button>
              <button
                onClick={() => setActiveTierFilter('TIER_1_QUARANTINE')}
                className={`px-2 sm:px-2.5 py-1 rounded-md text-[10px] sm:text-[11px] font-semibold transition-all cursor-pointer ${
                  activeTierFilter === 'TIER_1_QUARANTINE' ? 'bg-gradient-to-b from-rose-600 to-rose-800 text-white font-bold shadow-[var(--skeuo-btn)]' : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
                }`}
              >
                Tier 1 Quarantine
              </button>
              <button
                onClick={() => setActiveTierFilter('TIER_2_REVIEW_QUEUE')}
                className={`px-2 sm:px-2.5 py-1 rounded-md text-[10px] sm:text-[11px] font-semibold transition-all cursor-pointer ${
                  activeTierFilter === 'TIER_2_REVIEW_QUEUE' ? 'bg-gradient-to-b from-amber-600 to-amber-800 text-white font-bold shadow-[var(--skeuo-btn)]' : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
                }`}
              >
                Tier 2 Review
              </button>
            </div>

            <div className="flex items-center gap-1.5 w-full sm:w-auto">
              <button
                onClick={() => {
                  const headers = ['Transaction ID', 'Timestamp', 'Subject Name', 'Account Number', 'Amount USD', 'Rail', 'Jurisdiction', 'Risk Score', 'Conformal Tier', 'Assignee', 'Status', 'Typology'];
                  const rows = filteredTxs.map(t => [
                    t.id,
                    t.timestamp,
                    `"${t.holderName}"`,
                    t.accountNumber,
                    t.amount,
                    `"${t.rail}"`,
                    `"${t.jurisdiction}"`,
                    (t.risk * 100).toFixed(1) + '%',
                    t.tier,
                    `"${t.assignee || 'Unassigned'}"`,
                    t.status,
                    `"${t.pattern}"`
                  ]);
                  const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
                  const encodedUri = encodeURI(csvContent);
                  const link = document.createElement('a');
                  link.setAttribute('href', encodedUri);
                  link.setAttribute('download', `AML_Alert_Queue_${new Date().toISOString().substring(0, 10)}.csv`);
                  document.body.appendChild(link);
                  link.click();
                  document.body.removeChild(link);
                }}
                className="skeuo-btn skeuo-btn-secondary px-2.5 py-1 text-[11px] font-bold flex items-center gap-1.5 shrink-0 cursor-pointer"
                title="Export current filtered queue to CSV"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Export CSV</span>
              </button>

              <button
                onClick={() => setIsBatchModalOpen(true)}
                className="skeuo-btn skeuo-btn-primary px-2.5 py-1 text-[11px] font-bold flex items-center gap-1.5 shrink-0 cursor-pointer"
                title="Upload CSV or test pre-bundled batch datasets"
              >
                <UploadCloud className="w-3.5 h-3.5" />
                <span>Batch Ingest</span>
              </button>

              <div className="relative flex-1 sm:w-52">
                <Search className="w-3 h-3 text-[var(--accent-primary)] absolute left-2.5 top-2.5" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Filter transactions..."
                  className="w-full pl-8 pr-2.5 py-1 rounded-lg bg-[var(--bg-base)] border border-[var(--border-card)] focus:border-[var(--accent-primary)] text-[11px] text-[var(--text-primary)] placeholder-[var(--text-muted)] shadow-inner outline-none"
                />
              </div>
            </div>
          </div>

          {/* Batch Feedback Notification */}
          {batchFeedback && (
            <div className="p-2 rounded-lg bg-emerald-500/15 border border-emerald-500/30 text-emerald-700 dark:text-emerald-300 text-[11px] font-mono flex items-center gap-2">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
              <span>{batchFeedback}</span>
            </div>
          )}

          {/* Batch Operations Bar (Floats/renders when items selected) */}
          {selectedTxIds.size > 0 && (
            <div className="p-2 sm:p-2.5 rounded-xl bg-[var(--bg-card-elevated)] border border-[var(--accent-primary)]/40 flex flex-wrap items-center justify-between gap-2 text-[11px] font-mono shadow-md animate-fadeIn">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-[var(--accent-primary)] animate-ping" />
                <span className="font-bold text-[var(--text-primary)]">
                  BATCH ACTION: <span className="text-[var(--accent-primary)]">{selectedTxIds.size}</span> Alerts Selected
                </span>
              </div>
              <div className="flex flex-wrap items-center gap-1.5">
                <button
                  onClick={handleBatchQuarantine}
                  className="skeuo-btn skeuo-btn-danger px-2.5 py-1 text-[10px] font-bold flex items-center gap-1"
                >
                  <Lock className="w-3 h-3" />
                  <span>Batch Quarantine</span>
                </button>
                <button
                  onClick={handleBatchRFI}
                  className="skeuo-btn skeuo-btn-primary px-2.5 py-1 text-[10px] font-bold flex items-center gap-1"
                >
                  <Mail className="w-3 h-3" />
                  <span>Dispatch RFI</span>
                </button>
                <button
                  onClick={handleBatchDismiss}
                  className="skeuo-btn skeuo-btn-secondary px-2.5 py-1 text-[10px] font-bold flex items-center gap-1"
                >
                  <CheckCircle2 className="w-3 h-3 text-[var(--accent-primary)]" />
                  <span>Dismiss Selected</span>
                </button>
                <button
                  onClick={() => setSelectedTxIds(new Set())}
                  className="skeuo-btn px-2 py-1 text-[10px] text-[var(--text-muted)]"
                >
                  Clear
                </button>
              </div>
            </div>
          )}

          {/* Table Container in Recessed Well */}
          <div className="overflow-x-auto max-h-[380px] sm:max-h-[440px] overflow-y-auto rounded-xl skeuo-well">
            <table className="w-full text-left text-[11px] font-sans">
              <thead className="text-[9px] sm:text-[10px] font-mono text-[var(--text-muted)] uppercase bg-[var(--bg-card-elevated)] sticky top-0 z-10 border-b border-[var(--border-subtle)]">
                <tr>
                  <th className="py-2 px-2.5 w-7 text-center">
                    <input 
                      type="checkbox" 
                      checked={filteredTxs.length > 0 && selectedTxIds.size === filteredTxs.length}
                      onChange={toggleSelectAll}
                      className="accent-[var(--accent-primary)] cursor-pointer"
                      title="Select all"
                    />
                  </th>
                  <th className="py-2 px-2.5">Transaction</th>
                  <th className="py-2 px-2.5">Subject</th>
                  <th className="py-2 px-2.5">Amount</th>
                  <th className="py-2 px-2.5">Rail / Hub</th>
                  <th className="py-2 px-2.5">Assignee</th>
                  <th className="py-2 px-2.5">Status</th>
                  <th className="py-2 px-2.5">SLA Countdown</th>
                  <th className="py-2 px-2.5">Risk Band</th>
                  <th className="py-2 px-2.5 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[var(--border-subtle)]">
                {filteredTxs.map((tx) => {
                  const isSelected = selectedTx?.id === tx.id;
                  const isChecked = selectedTxIds.has(tx.id);
                  const isQuarantine = tx.tier === 'TIER_1_QUARANTINE';
                  const isReview = tx.tier === 'TIER_2_REVIEW_QUEUE';
                  return (
                    <tr
                      key={tx.id}
                      onClick={() => setSelectedTx(tx)}
                      className={`hover:bg-black/[0.02] dark:hover:bg-white/[0.04] transition-colors cursor-pointer ${
                        isSelected ? 'bg-[var(--accent-primary)]/15 border-l-4 border-[var(--accent-primary)]' : ''
                      }`}
                    >
                      <td className="py-1.5 px-2.5 text-center" onClick={(e) => e.stopPropagation()}>
                        <input 
                          type="checkbox"
                          checked={isChecked}
                          onChange={(e) => toggleSelectTx(tx.id, e)}
                          className="accent-[var(--accent-primary)] cursor-pointer"
                        />
                      </td>
                      <td className="py-1.5 px-2.5 font-mono font-bold text-[var(--text-primary)]">
                        <div>{tx.id}</div>
                        <div className="text-[9px] text-[var(--text-muted)] font-normal">{tx.timestamp}</div>
                      </td>
                      <td className="py-1.5 px-2.5">
                        <div className="font-semibold text-[var(--text-primary)] truncate max-w-[130px]">{tx.holderName}</div>
                        <div className="text-[9px] text-[var(--text-secondary)] font-mono truncate max-w-[120px]">{tx.accountNumber}</div>
                      </td>
                      <td className="py-1.5 px-2.5 font-mono font-bold text-[var(--text-primary)]">
                        ${tx.amount.toLocaleString()}
                      </td>
                      <td className="py-1.5 px-2.5 text-[10px] text-[var(--text-secondary)]">
                        <div>{tx.rail.split(' ')[0]}</div>
                        <div className="text-[9px] text-[var(--text-muted)]">{tx.jurisdiction.split(' ')[0]}</div>
                      </td>
                      <td className="py-1.5 px-2.5 font-mono text-[10px]">
                        <span className="text-[var(--text-secondary)] font-semibold truncate block max-w-[100px]">
                          {tx.assignee || 'Unassigned'}
                        </span>
                      </td>
                      <td className="py-1.5 px-2.5 font-mono text-[9px]">
                        <span className={`px-1.5 py-0.5 rounded font-bold ${
                          tx.status === 'QUARANTINED' ? 'bg-rose-500/20 text-rose-500 border border-rose-500/30' :
                          tx.status === 'UNDER_REVIEW' ? 'bg-amber-500/20 text-amber-500 border border-amber-500/30' :
                          tx.status === 'ESCALATED_SAR' ? 'bg-indigo-500/20 text-indigo-400 border border-indigo-500/30' :
                          'bg-emerald-500/20 text-emerald-500 border border-emerald-500/30'
                        }`}>
                          {tx.status}
                        </span>
                      </td>
                      <td className="py-1.5 px-2.5 font-mono text-[9px]">
                        <span className={`px-1.5 py-0.5 rounded font-semibold inline-flex items-center gap-1 ${
                          tx.slaUrgent ? 'bg-rose-500/20 text-rose-600 dark:text-rose-400 border border-rose-500/30 animate-pulse' :
                          tx.slaDeadline?.includes('Auto-Cleared') ? 'text-[var(--text-muted)]' :
                          'bg-amber-500/15 text-amber-700 dark:text-amber-300 border border-amber-500/30'
                        }`}>
                          <Clock className="w-2.5 h-2.5" />
                          {tx.slaDeadline}
                        </span>
                      </td>
                      <td className="py-1.5 px-2.5 font-mono">
                        <span className={`text-[9px] sm:text-[10px] px-2 py-0.5 rounded-full font-bold ${
                          isQuarantine ? 'badge-tier1' : isReview ? 'badge-tier2' : 'badge-tier3'
                        }`}>
                          {(tx.risk * 100).toFixed(0)}% • {tx.gammaSet}
                        </span>
                      </td>
                      <td className="py-1.5 px-2.5 text-right">
                        <ChevronRight className="w-3.5 h-3.5 text-[var(--accent-primary)] inline-block" />
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {/* Institutional Pagination & 24h Sample Disclosure */}
          <div className="flex flex-col sm:flex-row items-center justify-between gap-2 p-2 rounded-xl bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)] text-[10px] font-mono text-[var(--text-muted)]">
            <div className="flex items-center gap-1.5">
              <span>Showing <strong>1–{filteredTxs.length}</strong> of <strong>2,028</strong> flagged alerts</span>
              <span className="text-[var(--border-subtle)]">•</span>
              <span>24h Monitored Volume: <strong>148,312 tx</strong> (1.7 tx/s avg)</span>
            </div>
            <div className="flex items-center gap-1">
              <button className="px-2 py-0.5 rounded bg-[var(--bg-base)] border border-[var(--border-subtle)] text-[var(--text-muted)] cursor-not-allowed">
                &larr; Prev
              </button>
              <span className="px-2 py-0.5 rounded bg-[var(--accent-primary)] text-white font-bold">1</span>
              <button className="px-2 py-0.5 rounded bg-[var(--bg-base)] border border-[var(--border-subtle)] text-[var(--text-primary)] hover:border-[var(--accent-primary)] cursor-pointer">
                2
              </button>
              <button className="px-2 py-0.5 rounded bg-[var(--bg-base)] border border-[var(--border-subtle)] text-[var(--text-primary)] hover:border-[var(--accent-primary)] cursor-pointer">
                3
              </button>
              <span className="px-1 text-[var(--text-muted)]">...</span>
              <button className="px-2 py-0.5 rounded bg-[var(--bg-base)] border border-[var(--border-subtle)] text-[var(--text-primary)] hover:border-[var(--accent-primary)] cursor-pointer">
                338
              </button>
              <button className="px-2 py-0.5 rounded bg-[var(--bg-base)] border border-[var(--border-subtle)] text-[var(--text-primary)] hover:border-[var(--accent-primary)] cursor-pointer">
                Next &rarr;
              </button>
            </div>
          </div>
        </div>

        {/* Right Column: Selected Transaction Forensic Inspector */}
        <div className="xl:col-span-4 skeuo-card p-2.5 sm:p-3 space-y-2.5 flex flex-col justify-between">
          <div className="space-y-2">
            <div className="flex items-center justify-between pb-2 border-b border-[var(--border-subtle)]">
              <span className="text-[11px] sm:text-xs font-bold text-[var(--text-primary)] font-mono uppercase tracking-wider flex items-center gap-1.5">
                <Eye className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                <span>Forensic Inspector</span>
              </span>
              <span className={`text-[9px] sm:text-[10px] font-mono px-2 py-0.5 rounded-full font-bold border ${
                selectedTx?.tier === 'TIER_1_QUARANTINE' ? 'badge-tier1' : 'badge-tier2'
              }`}>
                {selectedTx?.gammaLabel}
              </span>
            </div>

            {/* Plain-English Why Flagged Card */}
            <div className="p-2.5 rounded-xl bg-amber-500/10 border border-amber-500/20 space-y-1">
              <span className="text-[10px] font-mono uppercase tracking-wider text-amber-600 dark:text-amber-400 font-bold flex items-center gap-1">
                <AlertTriangle className="w-3 h-3" />
                <span>Plain-English Triage Rationale</span>
              </span>
              <p className="text-[11px] text-[var(--text-primary)] leading-relaxed">
                {selectedTx?.whyFlagged || 'Account exhibited abnormal transaction velocity and cyclical routing differing from customer baseline.'}
              </p>
            </div>

            {/* Account Card Details */}
            <div className="p-2.5 rounded-xl bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)] space-y-1.5 text-[11px] shadow-inner">
              <div>
                <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] font-mono block">SUBJECT ACCOUNT</span>
                <span className="font-mono text-[var(--accent-primary)] font-bold text-xs truncate block">{selectedTx?.accountNumber}</span>
              </div>
              <div className="grid grid-cols-2 gap-1.5">
                <div>
                  <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] font-mono block">NAME</span>
                  <span className="text-[var(--text-primary)] font-semibold truncate block">{selectedTx?.holderName}</span>
                </div>
                <div>
                  <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] font-mono block">AMOUNT</span>
                  <span className="text-[var(--text-primary)] font-bold font-mono text-xs">${selectedTx?.amount?.toLocaleString()}</span>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-1.5">
                <div>
                  <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] font-mono block">INSTITUTION</span>
                  <span className="text-[var(--text-secondary)] text-[10px] truncate block">{selectedTx?.institution}</span>
                </div>
                <div>
                  <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] font-mono block">SLA DEADLINE</span>
                  <span className="text-amber-700 dark:text-amber-300 font-mono text-[10px] truncate block font-bold">{selectedTx?.slaDeadline}</span>
                </div>
              </div>
              <div>
                <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] font-mono block">TYPOLOGY PATTERN</span>
                <span className="text-amber-700 dark:text-amber-300 font-semibold text-[10px] block">{selectedTx?.pattern}</span>
              </div>
            </div>

            {/* SHAP Explainable Feature Drivers */}
            <div className="p-2.5 rounded-xl bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)] space-y-1.5 text-[11px] shadow-inner">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-mono text-[var(--text-muted)] uppercase font-bold">TOP RISK DRIVERS (SHAP)</span>
                <span className="text-[9px] font-mono text-[var(--accent-primary)] font-semibold">Local Attribution</span>
              </div>
              <div className="space-y-1">
                {(selectedTx?.featureDrivers || [
                  { name: 'Cyclic Conservation Φ', impact: 42 },
                  { name: 'Burst Hawkes λ', impact: 32 },
                  { name: 'Cross-Border Hop', impact: 18 }
                ]).map((fd, idx) => (
                  <div key={idx} className="space-y-0.5">
                    <div className="flex justify-between text-[10px] font-mono">
                      <span className="text-[var(--text-secondary)]">{fd.name}</span>
                      <span className="text-rose-500 font-bold">+{fd.impact}%</span>
                    </div>
                    <div className="w-full h-1.5 bg-black/10 dark:bg-white/10 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-gradient-to-r from-amber-500 to-rose-500 rounded-full" 
                        style={{ width: `${Math.min(100, fd.impact * 2)}%` }} 
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Conformal Prediction Set Analysis */}
            <div className="p-2.5 rounded-xl bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)] space-y-1 text-[11px] shadow-inner">
              <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] font-mono block">CONFORMAL RISK SET Γ(X)</span>
              <div className="flex items-center justify-between">
                <span className="text-[var(--text-primary)] font-mono font-bold text-xs">{selectedTx?.gammaSet} ({selectedTx?.gammaLabel})</span>
                <span className="text-[9px] sm:text-[10px] font-mono text-[var(--accent-primary)] font-semibold">Coverage &ge; 99.0%</span>
              </div>
              <p className="text-[10px] text-[var(--text-secondary)] pt-0.5">
                Distribution-free finite validity guaranteed under SR 11-7 model calibration standards.
              </p>
            </div>
          </div>

          {/* Action Triggers */}
          <div className="pt-2 border-t border-[var(--border-subtle)] space-y-1.5">
            <div className="grid grid-cols-2 gap-1.5">
              <button
                onClick={() => onOpenAccountProfile && onOpenAccountProfile({
                  id: selectedTx?.accountNumber,
                  name: selectedTx?.holderName,
                  bank: selectedTx?.institution,
                  risk: selectedTx?.risk,
                  tier: selectedTx?.tier,
                  balance: `$${(selectedTx?.amount * 12.4).toLocaleString(undefined, { maximumFractionDigits: 2 })}`
                })}
                className="flex items-center justify-center gap-1 py-1.5 rounded-lg skeuo-btn text-[10px] font-semibold"
              >
                <UserCheck className="w-3 h-3 text-[var(--accent-primary)]" />
                <span>KYC Profile</span>
              </button>

              <button
                onClick={() => onOpenNoticeModal && onOpenNoticeModal(selectedTx)}
                className="flex items-center justify-center gap-1 py-1.5 rounded-lg skeuo-btn text-[10px] font-semibold"
                title="Dispatch Compliant Source of Funds / Invoicing RFI (Anti-Tipping-Off Safeguard Active)"
              >
                <Mail className="w-3 h-3 text-amber-600 dark:text-amber-400" />
                <span>Request Info (RFI)</span>
              </button>
            </div>

            <button
              onClick={() => onOpenActionModal && onOpenActionModal(selectedTx)}
              className="w-full flex items-center justify-center gap-1.5 py-1.5 rounded-lg skeuo-btn skeuo-btn-danger text-[11px] font-bold"
            >
              <Shield className="w-3 h-3" />
              <span>⚡ Human Governance Authorization</span>
            </button>

            <button
              onClick={() => onNavigateToGraph && onNavigateToGraph(selectedTx)}
              className="w-full flex items-center justify-center gap-1.5 py-1.5 rounded-lg skeuo-btn skeuo-btn-secondary text-[11px] font-semibold cursor-pointer"
            >
              <Share2 className="w-3 h-3 text-[var(--accent-primary)]" />
              <span>Inspect in 3D Forensic Studio</span>
            </button>

            <button
              onClick={() => onNavigateToSAR && onNavigateToSAR(selectedTx)}
              className="w-full flex items-center justify-center gap-1.5 py-1.5 rounded-lg skeuo-btn skeuo-btn-primary text-[11px] font-semibold cursor-pointer"
            >
              <FileText className="w-3 h-3" />
              <span>Draft Official SAR Dossier</span>
            </button>
          </div>
        </div>
      </div>

      {/* Batch CSV Ingest Modal */}
      <BatchCSVIngestModal
        isOpen={isBatchModalOpen}
        onClose={() => setIsBatchModalOpen(false)}
        onImportToQueue={handleImportBatch}
      />
    </div>
  );
};
