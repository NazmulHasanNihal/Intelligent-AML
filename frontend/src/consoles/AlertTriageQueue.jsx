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
  Download
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const ENTERPRISE_TRANSACTIONS = [
  {
    id: 'TX-994821',
    timestamp: '08:42:01 UTC',
    accountNumber: 'US-JPMC-4829-1092-8823',
    holderName: 'Apex Global Logistics Ltd',
    holderType: 'CORPORATE',
    institution: 'JPMorgan Chase Bank, N.A.',
    src: 'US-JPMC-4829-1092-8823',
    dst: 'GB-BARC-1109-MULE-HUB',
    counterpartyName: 'Elena Rostova (Conduit Hub)',
    amount: 9450,
    rail: 'SWIFT Wire (MT103)',
    jurisdiction: 'Offshore (Panama / BVI)',
    risk: 0.94,
    intervalLow: 0.884,
    intervalHigh: 0.972,
    gammaSet: '{1}',
    gammaLabel: 'Tier 1: Quarantine',
    tier: 'TIER_1_QUARANTINE',
    pattern: 'Smurfing & Structuring ($9.45k < $10k Threshold)',
    status: 'QUARANTINED',
    burst: true,
    domain: 'Core Banking',
    slaDeadline: 'FinCEN 30-Day: 28d 14h left',
    slaUrgent: false
  },
  {
    id: 'TX-994819',
    timestamp: '08:41:58 UTC',
    accountNumber: '0x3a9f-4829-DARK-0012',
    holderName: 'Darknet UTXO Consolidation',
    holderType: 'CRYPTO_ENTITY',
    institution: 'Binance / Wasabi CoinJoin',
    src: '0x3a9f-4829',
    dst: '0x7b12-MIXER-POOL',
    counterpartyName: 'Mixer Liquidity Pool',
    amount: 95000,
    rail: 'Bitcoin UTXO DAG',
    jurisdiction: 'Decentralized (Unregistered)',
    risk: 0.98,
    intervalLow: 0.955,
    intervalHigh: 0.994,
    gammaSet: '{1}',
    gammaLabel: 'Tier 1: Quarantine',
    tier: 'TIER_1_QUARANTINE',
    pattern: 'Multi-Hop UTXO CoinJoin Peeling Chain',
    status: 'QUARANTINED',
    burst: true,
    domain: 'Crypto Assets',
    slaDeadline: 'BFIU 72-Hour: 18h 32m left',
    slaUrgent: true
  },
  {
    id: 'TX-994818',
    timestamp: '08:41:55 UTC',
    accountNumber: 'US-CITI-0019-DORMANT-MULE',
    holderName: 'Marcus Vance',
    holderType: 'RETAIL',
    institution: 'Citibank N.A. (New York)',
    src: 'US-CITI-0019',
    dst: 'SG-DBS-8819-TRANSIT',
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
    status: 'UNDER_REVIEW',
    burst: false,
    domain: 'Retail Banking',
    slaDeadline: 'FinCEN 30-Day: 29d 21h left',
    slaUrgent: false
  },
  {
    id: 'TX-994817',
    timestamp: '08:41:52 UTC',
    accountNumber: 'US-WF-0091-8841-CLEAN',
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
    status: 'AUTO_CLEARED',
    burst: false,
    domain: 'Commercial Banking',
    slaDeadline: 'Exempt / Auto-Cleared',
    slaUrgent: false
  },
  {
    id: 'TX-994816',
    timestamp: '08:41:48 UTC',
    accountNumber: 'DE-DB-9901-RHEINLAND-LLC',
    holderName: 'Rheinland Freight GmbH',
    holderType: 'CORPORATE',
    institution: 'Deutsche Bank (Frankfurt)',
    src: 'DE-DB-9901',
    dst: 'FR-BNP-3312-EURO-HUB',
    counterpartyName: 'Euro Logistics Clearing',
    amount: 6200,
    rail: 'SEPA Instant Credit',
    jurisdiction: 'EU Intra-Zone',
    risk: 0.44,
    intervalLow: 0.310,
    intervalHigh: 0.580,
    gammaSet: '{0, 1}',
    gammaLabel: 'Tier 2: Review Queue',
    tier: 'TIER_2_REVIEW_QUEUE',
    pattern: 'Cross-Border Velocity Shift ($6.2k)',
    status: 'UNDER_REVIEW',
    burst: false,
    domain: 'Core Banking',
    slaDeadline: 'EU FIU 5-Day: 3d 08h left',
    slaUrgent: false
  },
  {
    id: 'TX-994815',
    timestamp: '08:41:44 UTC',
    accountNumber: 'US-JPMC-4829-1092-8823',
    holderName: 'Apex Global Logistics Ltd',
    holderType: 'CORPORATE',
    institution: 'JPMorgan Chase Bank, N.A.',
    src: 'HK-HSBC-8812-ASIA-TRADING',
    dst: 'US-JPMC-4829-1092-8823',
    counterpartyName: 'Apex Global Logistics Ltd',
    amount: 47600,
    rail: 'SWIFT Wire (MT103)',
    jurisdiction: 'Offshore Corridor',
    risk: 0.96,
    intervalLow: 0.910,
    intervalHigh: 0.985,
    gammaSet: '{1}',
    gammaLabel: 'Tier 1: Quarantine',
    tier: 'TIER_1_QUARANTINE',
    pattern: 'Wash Trading Inbound Peeling Loop ($47.6k)',
    status: 'QUARANTINED',
    burst: true,
    domain: 'Core Banking',
    slaDeadline: 'FinCEN 30-Day: 27d 02h left',
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
  const [activeTierFilter, setActiveTierFilter] = useState('ALL'); // 'ALL', 'TIER_1', 'TIER_2', 'TIER_3'
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTx, setSelectedTx] = useState(ENTERPRISE_TRANSACTIONS[0]);
  const [selectedTxIds, setSelectedTxIds] = useState(new Set());
  const [batchFeedback, setBatchFeedback] = useState(null);

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

  const filteredTxs = ENTERPRISE_TRANSACTIONS.filter(tx => {
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
            <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] font-mono block uppercase truncate">TIER 3 AUTO-CLEARED (&gt;99.4%)</span>
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
          
          {/* Controls Bar: Search & Filter Tabs */}
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 pb-2 border-b border-[var(--border-subtle)]">
            <div className="flex items-center gap-1 p-0.5 rounded-lg bg-[var(--bg-base)] border border-[var(--border-subtle)] overflow-x-auto w-full sm:w-auto shadow-inner">
              <button
                onClick={() => setActiveTierFilter('ALL')}
                className={`px-2 sm:px-2.5 py-1 rounded-md text-[10px] sm:text-[11px] font-semibold transition-all cursor-pointer ${
                  activeTierFilter === 'ALL' ? 'bg-gradient-to-b from-[#257843] to-[#174E2B] text-white font-bold shadow-[var(--skeuo-btn)]' : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
                }`}
              >
                All ({ENTERPRISE_TRANSACTIONS.length})
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

            <div className="relative w-full sm:w-56">
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

            {/* Conformal Prediction Set Analysis */}
            <div className="p-2.5 rounded-xl bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)] space-y-1 text-[11px] shadow-inner">
              <span className="text-[9px] sm:text-[10px] text-[var(--text-muted)] font-mono block">CONFORMAL RISK SET Γ(X)</span>
              <div className="flex items-center justify-between">
                <span className="text-[var(--text-primary)] font-mono font-bold text-xs">{selectedTx?.gammaSet} ({selectedTx?.gammaLabel})</span>
                <span className="text-[9px] sm:text-[10px] font-mono text-[var(--accent-primary)] font-semibold">Coverage &ge; 99.0%</span>
              </div>
              <p className="text-[10px] text-[var(--text-secondary)] pt-0.5">
                Calibrated against holdout calibration split with exchangeability guarantees.
              </p>
            </div>
          </div>

          {/* Action Triggers: Full suite including Governance, KYC Drawer, SAR */}
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
              >
                <Mail className="w-3 h-3 text-amber-600 dark:text-amber-400" />
                <span>Adverse Notice</span>
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
              onClick={() => onNavigateToGraph && onNavigateToGraph()}
              className="w-full flex items-center justify-center gap-1.5 py-1.5 rounded-lg skeuo-btn skeuo-btn-secondary text-[11px] font-semibold"
            >
              <Share2 className="w-3 h-3 text-[var(--accent-primary)]" />
              <span>Inspect in 3D Forensic Studio</span>
            </button>

            <button
              onClick={() => onNavigateToSAR && onNavigateToSAR()}
              className="w-full flex items-center justify-center gap-1.5 py-1.5 rounded-lg skeuo-btn skeuo-btn-primary text-[11px] font-semibold"
            >
              <FileText className="w-3 h-3" />
              <span>Draft Official SAR Dossier</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
