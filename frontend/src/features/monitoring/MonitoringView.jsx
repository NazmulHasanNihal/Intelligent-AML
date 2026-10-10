import React, { useState, useMemo } from 'react';
import { 
  ShieldAlert, 
  ShieldCheck, 
  AlertTriangle, 
  Lock, 
  Unlock, 
  Sliders, 
  Activity, 
  Search, 
  Filter, 
  CheckCircle2, 
  XCircle, 
  RotateCcw, 
  Zap, 
  Layers, 
  ExternalLink, 
  ArrowUpRight, 
  FileText, 
  UserCheck, 
  Play, 
  Eye,
  Shield,
  HelpCircle,
  TrendingUp,
  Globe
} from 'lucide-react';
import { useAppStore } from '../../lib/store';
import { Card, CardHeader } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';

export const MonitoringView = () => {
  const { 
    liveTransactions, 
    blockedTransactions, 
    fraudRules, 
    blockTransaction, 
    unblockTransaction, 
    toggleFraudRule, 
    openDrawer,
    navigate,
    addToast
  } = useAppStore();

  const [activeTab, setActiveTab] = useState('live'); // 'live' | 'rules' | 'blocked' | 'screen'
  const [searchQuery, setSearchQuery] = useState('');
  const [ruleCategoryFilter, setRuleCategoryFilter] = useState('ALL');
  
  // Manual Block Modal State
  const [selectedTxToBlock, setSelectedTxToBlock] = useState(null);
  const [blockReason, setBlockReason] = useState('Sub-threshold CTR structuring pattern detected');
  const [isBlockModalOpen, setIsBlockModalOpen] = useState(false);

  // Unblock Modal State
  const [selectedBlockToRelease, setSelectedBlockToRelease] = useState(null);
  const [unblockJustification, setUnblockJustification] = useState('');
  const [isUnblockModalOpen, setIsUnblockModalOpen] = useState(false);

  // Simulation Tool State
  const [simAccount, setSimAccount] = useState('BD22-EBLB-4829-1092-8823');
  const [simAmount, setSimAmount] = useState('9450');
  const [simRail, setSimRail] = useState('SWIFT MT103');
  const [simResult, setSimResult] = useState(null);

  // Filtered Live Transactions
  const filteredLiveTxs = useMemo(() => {
    return liveTransactions.filter(tx => {
      if (!searchQuery) return true;
      const q = searchQuery.toLowerCase();
      return (
        (tx.id || '').toLowerCase().includes(q) ||
        (tx.sourceEntity || '').toLowerCase().includes(q) ||
        (tx.targetEntity || '').toLowerCase().includes(q) ||
        (tx.sourceAccount || '').toLowerCase().includes(q) ||
        (tx.rail || '').toLowerCase().includes(q) ||
        (tx.whyFlagged || '').toLowerCase().includes(q)
      );
    });
  }, [liveTransactions, searchQuery]);

  // Total Blocked Exposure Calculation
  const totalBlockedExposure = useMemo(() => {
    return blockedTransactions
      .filter(b => b.status === 'BLOCKED')
      .reduce((acc, curr) => acc + Number(curr.amount || 0), 0);
  }, [blockedTransactions]);

  const activeRulesCount = useMemo(() => {
    return fraudRules.filter(r => r.status === 'ACTIVE').length;
  }, [fraudRules]);

  // Execute Block Action
  const handleConfirmBlock = () => {
    if (!selectedTxToBlock) return;
    blockTransaction(selectedTxToBlock.id, blockReason, 'Sarah Jenkins (Compliance Desk)');
    setIsBlockModalOpen(false);
    setSelectedTxToBlock(null);
  };

  // Execute Unblock Action
  const handleConfirmUnblock = () => {
    if (!selectedBlockToRelease || !unblockJustification.trim()) {
      addToast('Justification Required', 'Please enter a valid regulatory justification for release.', 'error');
      return;
    }
    unblockTransaction(selectedBlockToRelease.id, unblockJustification, 'Nazmul Hasan, Chief Compliance Officer');
    setIsUnblockModalOpen(false);
    setSelectedBlockToRelease(null);
    setUnblockJustification('');
  };

  // Execute Simulation Screen
  const handleRunSimulation = (e) => {
    e.preventDefault();
    const amountNum = parseFloat(simAmount) || 0;
    
    // Evaluate against active fraud rules
    const matches = [];
    if (amountNum >= 9000 && amountNum <= 9950) {
      matches.push({ rule: 'FR-001 (Structuring)', severity: 'CRITICAL', text: 'Transfer clustered in $9,000–$9,950 range directly beneath $10k reporting limit' });
    }
    if (simRail.includes('SWIFT') && amountNum > 40000) {
      matches.push({ rule: 'FR-003 (Offshore Corridor)', severity: 'CRITICAL', text: 'High-value outbound wire to offshore correspondent destination' });
    }
    if (amountNum > 100000) {
      matches.push({ rule: 'FR-002 (Velocity Spike)', severity: 'HIGH', text: 'Substantial single-ticket interbank exposure spike' });
    }

    const isBlocked = matches.some(m => m.severity === 'CRITICAL');
    setSimResult({
      evaluatedAt: new Date().toISOString().replace('T', ' ').substring(0, 19) + ' UTC',
      amount: amountNum,
      account: simAccount,
      rail: simRail,
      riskScore: matches.length > 0 ? (isBlocked ? 0.96 : 0.68) : 0.04,
      decision: isBlocked ? 'AUTOMATIC TIER 1 BLOCK' : matches.length > 0 ? 'TIER 2 MANUAL REVIEW' : 'TIER 3 CLEAR (STP)',
      status: isBlocked ? 'BLOCKED' : matches.length > 0 ? 'REVIEW' : 'CLEARED',
      matchedRules: matches
    });
  };

  return (
    <div className="space-y-4 select-none">
      {/* Top Banner: Transaction Monitoring & Fraud Prevention Desk */}
      <div className="p-4 rounded-lg bg-surface border border-border flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div>
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded bg-critical/15 text-critical flex items-center justify-center font-bold">
              <ShieldAlert className="w-4 h-4" />
            </div>
            <h2 className="text-sm font-semibold text-text">Transaction Monitoring & Fraud Prevention Desk</h2>
            <Badge variant="critical" size="sm">Active Interception Online</Badge>
          </div>
          <p className="text-xs text-text-muted mt-0.5">
            Real-time fraud rule evaluation, pre-clearing wire interception, and statutory four-eyes unblock controls.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setActiveTab('screen')}
            icon={Zap}
          >
            Instant Wire Screener
          </Button>
          <Button
            variant="secondary"
            size="sm"
            onClick={() => setActiveTab('blocked')}
            icon={Lock}
          >
            Blocked Vault ({blockedTransactions.filter(b => b.status === 'BLOCKED').length})
          </Button>
        </div>
      </div>

      {/* 4 Core KPI Summary Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        <Card className="flex flex-col justify-between">
          <div>
            <span className="text-xs text-text-muted font-medium block">Active Fraud Detection Rules</span>
            <div className="text-xl sm:text-2xl font-bold text-text mt-1 font-mono">
              {activeRulesCount} <span className="text-xs text-text-muted font-normal">/ {fraudRules.length} Active</span>
            </div>
          </div>
          <div className="mt-2 text-[11px] text-cleared flex items-center gap-1 font-mono">
            <CheckCircle2 className="w-3 h-3" />
            <span>Real-time rule engine healthy</span>
          </div>
        </Card>

        <Card className="flex flex-col justify-between">
          <div>
            <span className="text-xs text-text-muted font-medium block">Interception & Blocking Speed</span>
            <div className="text-xl sm:text-2xl font-bold text-cleared mt-1 font-mono">
              &lt; 0.45 ms
            </div>
          </div>
          <div className="mt-2 text-[11px] text-text-muted font-mono">
            <span>Pre-clearing settlement gateway</span>
          </div>
        </Card>

        <Card className="flex flex-col justify-between">
          <div>
            <span className="text-xs text-text-muted font-medium block">Currently Blocked Transfers</span>
            <div className="text-xl sm:text-2xl font-bold text-critical mt-1 font-mono">
              {blockedTransactions.filter(b => b.status === 'BLOCKED').length} Intercepted
            </div>
          </div>
          <div className="mt-2 text-[11px] text-critical flex items-center gap-1 font-mono">
            <Lock className="w-3 h-3" />
            <span>Administrative holds active</span>
          </div>
        </Card>

        <Card className="flex flex-col justify-between">
          <div>
            <span className="text-xs text-text-muted font-medium block">Total Exposure Protected</span>
            <div className="text-xl sm:text-2xl font-bold text-text mt-1 font-mono tabular-nums">
              ${totalBlockedExposure.toLocaleString()} USD
            </div>
          </div>
          <div className="mt-2 text-[11px] text-text-muted font-mono">
            <span>৳{(totalBlockedExposure * 120).toLocaleString()} BDT safeguarded</span>
          </div>
        </Card>
      </div>

      {/* Navigation Sub-Tabs */}
      <div className="flex items-center gap-1 border-b border-border text-xs font-mono">
        <button
          onClick={() => setActiveTab('live')}
          className={`px-3 py-2 border-b-2 font-semibold transition-colors cursor-pointer flex items-center gap-1.5 ${
            activeTab === 'live'
              ? 'border-accent text-accent'
              : 'border-transparent text-text-muted hover:text-text'
          }`}
        >
          <Activity className="w-3.5 h-3.5" />
          <span>Real-Time Stream Monitoring</span>
          <span className="px-1.5 py-0.2 rounded-full text-[10px] bg-surfaceRaised text-text border border-border">
            {liveTransactions.length}
          </span>
        </button>

        <button
          onClick={() => setActiveTab('blocked')}
          className={`px-3 py-2 border-b-2 font-semibold transition-colors cursor-pointer flex items-center gap-1.5 ${
            activeTab === 'blocked'
              ? 'border-accent text-accent'
              : 'border-transparent text-text-muted hover:text-text'
          }`}
        >
          <Lock className="w-3.5 h-3.5" />
          <span>Blocked Transactions Ledger</span>
          <span className="px-1.5 py-0.2 rounded-full text-[10px] bg-critical/15 text-critical border border-critical/30 font-bold">
            {blockedTransactions.filter(b => b.status === 'BLOCKED').length}
          </span>
        </button>

        <button
          onClick={() => setActiveTab('rules')}
          className={`px-3 py-2 border-b-2 font-semibold transition-colors cursor-pointer flex items-center gap-1.5 ${
            activeTab === 'rules'
              ? 'border-accent text-accent'
              : 'border-transparent text-text-muted hover:text-text'
          }`}
        >
          <Sliders className="w-3.5 h-3.5" />
          <span>Fraud Detection Rules ({fraudRules.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('screen')}
          className={`px-3 py-2 border-b-2 font-semibold transition-colors cursor-pointer flex items-center gap-1.5 ${
            activeTab === 'screen'
              ? 'border-accent text-accent'
              : 'border-transparent text-text-muted hover:text-text'
          }`}
        >
          <Zap className="w-3.5 h-3.5" />
          <span>Interactive Wire Screener</span>
        </button>
      </div>

      {/* TAB 1: REAL-TIME STREAM MONITORING & DIRECT BLOCKING */}
      {activeTab === 'live' && (
        <div className="space-y-3">
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2.5">
            <div className="relative flex-1 max-w-md">
              <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-text-muted" />
              <input
                type="text"
                placeholder="Search by transaction ID, entity, account, or clearing rail..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="ui-input pl-8 h-8 text-xs w-full font-mono"
              />
            </div>
            <div className="text-xs text-text-muted font-mono flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-cleared animate-ping" />
              <span>Evaluating live stream at ~500 tx/sec</span>
            </div>
          </div>

          <Card padding={false} className="overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="bg-surfaceRaised border-b border-border text-[11px] font-mono text-text-muted uppercase">
                    <th className="py-2.5 px-3">Timestamp & Ref</th>
                    <th className="py-2.5 px-3">Originator Account</th>
                    <th className="py-2.5 px-3">Beneficiary Account</th>
                    <th className="py-2.5 px-3">Rail</th>
                    <th className="py-2.5 px-3 text-right">Settlement Amount</th>
                    <th className="py-2.5 px-3 text-center">Fraud Risk</th>
                    <th className="py-2.5 px-3 text-center">Status / Hold</th>
                    <th className="py-2.5 px-3 text-right">Intervention</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-borderSubtle font-mono text-[11px]">
                  {filteredLiveTxs.map((tx, idx) => {
                    const isAlreadyBlocked = blockedTransactions.some(b => b.txId === tx.id && b.status === 'BLOCKED');
                    const isHighRisk = tx.tierCode === 1 || tx.riskScore > 0.85;

                    return (
                      <tr 
                        key={`${tx.id}-${idx}`}
                        className={`hover:bg-surfaceHover transition-colors ${
                          isAlreadyBlocked ? 'bg-critical/5' : isHighRisk ? 'bg-amber-500/5' : ''
                        }`}
                      >
                        <td className="py-2.5 px-3 whitespace-nowrap">
                          <span className="font-semibold text-text block">{tx.timestamp || '08:24 UTC'}</span>
                          <span className="text-[10px] text-accent block">{tx.swiftReference || tx.id}</span>
                        </td>

                        <td className="py-2.5 px-3 max-w-[180px]">
                          <span className="font-semibold text-text truncate block">{tx.sourceEntity}</span>
                          <span className="text-[10px] text-text-muted truncate block">{tx.sourceAccount}</span>
                        </td>

                        <td className="py-2.5 px-3 max-w-[180px]">
                          <span className="font-semibold text-text truncate block">{tx.targetEntity}</span>
                          <span className="text-[10px] text-text-muted truncate block">{tx.targetAccount}</span>
                        </td>

                        <td className="py-2.5 px-3 whitespace-nowrap">
                          <Badge variant="neutral" size="sm">
                            {tx.rail}
                          </Badge>
                        </td>

                        <td className="py-2.5 px-3 text-right whitespace-nowrap">
                          <span className="font-bold text-text tabular-nums block">
                            ${Number(tx.amount).toLocaleString(undefined, { minimumFractionDigits: 2 })}
                          </span>
                          <span className="text-[10px] text-text-muted block">
                            ৳{Number(tx.amountBdt || tx.amount * 120).toLocaleString(undefined, { maximumFractionDigits: 0 })}
                          </span>
                        </td>

                        <td className="py-2.5 px-3 text-center whitespace-nowrap">
                          <span className={`font-bold block ${
                            tx.riskScore > 0.85 ? 'text-critical' : tx.riskScore > 0.30 ? 'text-review' : 'text-cleared'
                          }`}>
                            {(tx.riskScore * 100).toFixed(1)}%
                          </span>
                          <span className="text-[9px] text-text-muted block">
                            {tx.tierCode === 1 ? 'High Risk' : tx.tierCode === 2 ? 'Borderline' : 'Standard'}
                          </span>
                        </td>

                        <td className="py-2.5 px-3 text-center whitespace-nowrap">
                          {isAlreadyBlocked ? (
                            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-bold bg-critical/15 text-critical border border-critical/30 animate-pulse">
                              <Lock className="w-2.5 h-2.5" />
                              BLOCKED
                            </span>
                          ) : tx.tierCode === 1 ? (
                            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/15 text-amber-500 border border-amber-500/30">
                              <AlertTriangle className="w-2.5 h-2.5" />
                              HOLD PENDING
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-semibold bg-cleared/10 text-cleared border border-cleared/20">
                              <CheckCircle2 className="w-2.5 h-2.5" />
                              CLEARED
                            </span>
                          )}
                        </td>

                        <td className="py-2.5 px-3 text-right whitespace-nowrap">
                          <div className="flex items-center justify-end gap-1.5">
                            <button
                              onClick={() => openDrawer({
                                account: tx.sourceAccount,
                                entityName: tx.sourceEntity,
                                tier: tx.tierLabel,
                                tierCode: tx.tierCode,
                                amount: tx.amount,
                                riskScore: tx.riskScore,
                                whyFlagged: tx.whyFlagged || 'Real-time evaluated telemetry'
                              })}
                              className="p-1.5 rounded hover:bg-surface border border-border text-text-muted hover:text-text cursor-pointer transition-colors"
                              title="Inspect Details"
                            >
                              <Eye className="w-3.5 h-3.5" />
                            </button>

                            {isAlreadyBlocked ? (
                              <button
                                onClick={() => {
                                  const block = blockedTransactions.find(b => b.txId === tx.id);
                                  setSelectedBlockToRelease(block);
                                  setIsUnblockModalOpen(true);
                                }}
                                className="px-2 py-1 rounded bg-cleared/10 text-cleared hover:bg-cleared/20 border border-cleared/30 font-semibold text-[10px] cursor-pointer flex items-center gap-1 transition-colors"
                                title="Release Administrative Hold"
                              >
                                <Unlock className="w-3 h-3" />
                                <span>Release</span>
                              </button>
                            ) : (
                              <button
                                onClick={() => {
                                  setSelectedTxToBlock(tx);
                                  setIsBlockModalOpen(true);
                                }}
                                className={`px-2 py-1 rounded font-semibold text-[10px] cursor-pointer flex items-center gap-1 transition-colors ${
                                  isHighRisk
                                    ? 'bg-critical text-white hover:bg-critical/90 shadow-xs'
                                    : 'bg-surface hover:bg-critical/10 text-text hover:text-critical border border-border hover:border-critical/30'
                                }`}
                                title="Block & Quarantine Transaction"
                              >
                                <Lock className="w-3 h-3" />
                                <span>Block</span>
                              </button>
                            )}
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </Card>
        </div>
      )}

      {/* TAB 2: BLOCKED TRANSACTIONS LEDGER */}
      {activeTab === 'blocked' && (
        <div className="space-y-3">
          <div className="p-3 rounded-lg bg-surfaceRaised border border-border flex flex-wrap items-center justify-between gap-3 text-xs font-mono">
            <div className="flex items-center gap-2">
              <Lock className="w-4 h-4 text-critical" />
              <span className="font-semibold text-text">Cryptographic Custody Ledger:</span>
              <span className="text-text-muted">All intercepted funds quarantined under BFIU §15 & FinCEN Order</span>
            </div>
            <div className="text-text-muted">
              Dual-Signatory Four-Eyes Approval strictly required for release.
            </div>
          </div>

          <Card padding={false} className="overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="bg-surfaceRaised border-b border-border text-[11px] font-mono text-text-muted uppercase">
                    <th className="py-2.5 px-3">Block Record ID</th>
                    <th className="py-2.5 px-3">Transaction Ref</th>
                    <th className="py-2.5 px-3">Entity / Account</th>
                    <th className="py-2.5 px-3 text-right">Quarantined Amount</th>
                    <th className="py-2.5 px-3">Clearing Rail</th>
                    <th className="py-2.5 px-3">Interception Reason</th>
                    <th className="py-2.5 px-3">Blocked Timestamp</th>
                    <th className="py-2.5 px-3 text-center">Status</th>
                    <th className="py-2.5 px-3 text-right">Release Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-borderSubtle font-mono text-[11px]">
                  {blockedTransactions.map((item) => (
                    <tr key={item.id} className="hover:bg-surfaceHover transition-colors">
                      <td className="py-2.5 px-3 whitespace-nowrap">
                        <span className="font-bold text-critical block">{item.id}</span>
                        <span className="text-[10px] text-text-muted block">SHA-256 Anchored</span>
                      </td>

                      <td className="py-2.5 px-3 whitespace-nowrap">
                        <span className="font-semibold text-text block">{item.txId}</span>
                        <span className="text-[10px] text-accent block">{item.ruleTriggered}</span>
                      </td>

                      <td className="py-2.5 px-3 max-w-[200px]">
                        <span className="font-semibold text-text truncate block">{item.entityName}</span>
                        <span className="text-[10px] text-text-muted truncate block">{item.account}</span>
                      </td>

                      <td className="py-2.5 px-3 text-right whitespace-nowrap">
                        <span className="font-bold text-critical tabular-nums block">
                          ${Number(item.amount).toLocaleString(undefined, { minimumFractionDigits: 2 })} {item.currency}
                        </span>
                        <span className="text-[10px] text-text-muted block">
                          ৳{(Number(item.amount) * 120).toLocaleString()} BDT
                        </span>
                      </td>

                      <td className="py-2.5 px-3 whitespace-nowrap">
                        <Badge variant="neutral" size="sm">
                          {item.rail}
                        </Badge>
                      </td>

                      <td className="py-2.5 px-3 max-w-[240px]">
                        <p className="text-[11px] text-text-2 line-clamp-2 leading-tight">
                          {item.reason}
                        </p>
                      </td>

                      <td className="py-2.5 px-3 whitespace-nowrap text-text-muted text-[10px]">
                        <div>{item.blockedAt}</div>
                        <div className="text-text-2">{item.blockedBy}</div>
                      </td>

                      <td className="py-2.5 px-3 text-center whitespace-nowrap">
                        {item.status === 'BLOCKED' ? (
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-bold bg-critical/15 text-critical border border-critical/30">
                            <Lock className="w-2.5 h-2.5" />
                            BLOCKED
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-bold bg-cleared/15 text-cleared border border-cleared/30">
                            <Unlock className="w-2.5 h-2.5" />
                            RELEASED
                          </span>
                        )}
                      </td>

                      <td className="py-2.5 px-3 text-right whitespace-nowrap">
                        {item.status === 'BLOCKED' ? (
                          <button
                            onClick={() => {
                              setSelectedBlockToRelease(item);
                              setIsUnblockModalOpen(true);
                            }}
                            className="px-2.5 py-1 rounded bg-cleared/15 text-cleared hover:bg-cleared/25 border border-cleared/40 font-semibold text-[11px] cursor-pointer flex items-center gap-1 transition-colors ml-auto"
                          >
                            <Unlock className="w-3.5 h-3.5" />
                            <span>Unblock / Release</span>
                          </button>
                        ) : (
                          <span className="text-[10px] text-text-muted">
                            Released by {item.unblockedBy?.split(' ')[0] || 'CCO'}
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        </div>
      )}

      {/* TAB 3: FRAUD DETECTION RULES ENGINE */}
      {activeTab === 'rules' && (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 p-3 rounded-lg bg-surfaceRaised border border-border">
            <div>
              <h3 className="text-xs font-bold text-text uppercase tracking-wider font-mono">
                Active Fraud Detection Rules ({activeRulesCount} of {fraudRules.length} Active)
              </h3>
              <p className="text-xs text-text-muted mt-0.5">
                Toggle rules in real time. Deactivated rules immediately bypass automatic hold triggers without service restart.
              </p>
            </div>
            <Badge variant="cleared" size="sm">Rule Engine Online</Badge>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {fraudRules.map((rule) => {
              const isActive = rule.status === 'ACTIVE';

              return (
                <Card 
                  key={rule.id}
                  className={`transition-all ${
                    isActive ? 'border-border' : 'border-borderSubtle opacity-60 bg-bg'
                  }`}
                >
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex items-center gap-2">
                      <div className={`w-8 h-8 rounded-lg flex items-center justify-center font-bold text-xs font-mono ${
                        rule.severity === 'CRITICAL' ? 'bg-critical/15 text-critical' : 'bg-amber-500/15 text-amber-500'
                      }`}>
                        {rule.code}
                      </div>
                      <div>
                        <h4 className="text-xs font-bold text-text">{rule.name}</h4>
                        <span className="text-[10px] text-text-muted font-mono">{rule.category}</span>
                      </div>
                    </div>

                    <button
                      onClick={() => toggleFraudRule(rule.id)}
                      className={`px-2.5 py-1 rounded text-xs font-mono font-bold cursor-pointer transition-colors border ${
                        isActive
                          ? 'bg-cleared/15 text-cleared border-cleared/40 hover:bg-cleared/25'
                          : 'bg-surface text-text-muted border-border hover:text-text'
                      }`}
                    >
                      {isActive ? 'ACTIVE' : 'DISABLED'}
                    </button>
                  </div>

                  <p className="text-xs text-text-2 mt-2.5 leading-relaxed">
                    {rule.description}
                  </p>

                  <div className="mt-3 pt-2.5 border-t border-borderSubtle grid grid-cols-3 gap-2 text-xs font-mono">
                    <div>
                      <span className="text-[10px] text-text-muted uppercase block">Sensitivity</span>
                      <span className="font-semibold text-text text-[11px]">{rule.thresholdValue}</span>
                    </div>

                    <div>
                      <span className="text-[10px] text-text-muted uppercase block">Enforcement</span>
                      <span className={`font-bold text-[11px] ${
                        rule.action === 'AUTOMATIC_BLOCK' ? 'text-critical' : 'text-amber-500'
                      }`}>
                        {rule.action.replace('_', ' ')}
                      </span>
                    </div>

                    <div className="text-right">
                      <span className="text-[10px] text-text-muted uppercase block">Triggers (24h)</span>
                      <span className="font-bold text-text text-[11px]">{rule.triggers24h} Events</span>
                    </div>
                  </div>
                </Card>
              );
            })}
          </div>
        </div>
      )}

      {/* TAB 4: INTERACTIVE WIRE SCREENER */}
      {activeTab === 'screen' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
          <Card className="lg:col-span-6 space-y-4">
            <CardHeader
              title="Instant Pre-Clearing Wire Screener"
              subtitle="Simulate and screen any planned transaction against active fraud detection rules"
              badge={<Badge variant="neutral" size="sm">Interactive Screener</Badge>}
            />

            <form onSubmit={handleRunSimulation} className="space-y-3 font-mono text-xs">
              <div>
                <label className="text-[11px] text-text-muted block mb-1">Originating Account Number</label>
                <input
                  type="text"
                  value={simAccount}
                  onChange={(e) => setSimAccount(e.target.value)}
                  className="ui-input h-8 w-full text-xs"
                  placeholder="e.g. BD22-EBLB-4829-1092-8823"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[11px] text-text-muted block mb-1">Transfer Amount (USD)</label>
                  <input
                    type="number"
                    step="0.01"
                    value={simAmount}
                    onChange={(e) => setSimAmount(e.target.value)}
                    className="ui-input h-8 w-full text-xs"
                    placeholder="9450"
                    required
                  />
                </div>

                <div>
                  <label className="text-[11px] text-text-muted block mb-1">Clearing Payment Rail</label>
                  <select
                    value={simRail}
                    onChange={(e) => setSimRail(e.target.value)}
                    className="ui-input h-8 w-full text-xs"
                  >
                    <option value="SWIFT MT103">SWIFT MT103 (Single Customer Wire)</option>
                    <option value="SWIFT MT700 (LC)">SWIFT MT700 (Documentary Credit)</option>
                    <option value="RTGS (BD Bank)">Bangladesh Bank RTGS</option>
                    <option value="bKash MFS">bKash MFS Commercial API</option>
                    <option value="BEFTN">BEFTN Electronic Clearing</option>
                    <option value="Fedwire">Fedwire Funds Service</option>
                  </select>
                </div>
              </div>

              <div className="pt-2">
                <Button
                  type="submit"
                  variant="primary"
                  size="md"
                  icon={Play}
                  className="w-full justify-center"
                >
                  Screen Transaction Now
                </Button>
              </div>
            </form>
          </Card>

          <Card className="lg:col-span-6 flex flex-col justify-between">
            <div>
              <CardHeader
                title="Screening Verdict & Fraud Assessment"
                subtitle="Live rule matching results and recommended action"
              />

              {simResult ? (
                <div className="space-y-3 mt-3 font-mono text-xs">
                  <div className="p-3 rounded-lg border bg-bg flex items-center justify-between">
                    <div>
                      <span className="text-[10px] text-text-muted uppercase block">DECISION VERDICT</span>
                      <span className={`text-base font-bold ${
                        simResult.status === 'BLOCKED' ? 'text-critical' : simResult.status === 'REVIEW' ? 'text-review' : 'text-cleared'
                      }`}>
                        {simResult.decision}
                      </span>
                    </div>

                    <div className="text-right">
                      <span className="text-[10px] text-text-muted uppercase block">RISK SCORE</span>
                      <span className="text-lg font-bold text-text">
                        {(simResult.riskScore * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>

                  <div>
                    <span className="text-[11px] font-semibold text-text block mb-1.5">
                      Matched Fraud Detection Rules ({simResult.matchedRules.length}):
                    </span>
                    {simResult.matchedRules.length === 0 ? (
                      <div className="p-3 rounded bg-cleared/10 border border-cleared/30 text-cleared text-xs">
                        No fraud patterns detected. Transaction qualifies for Straight-Through Processing (STP).
                      </div>
                    ) : (
                      <div className="space-y-2">
                        {simResult.matchedRules.map((m, i) => (
                          <div key={i} className="p-2.5 rounded bg-critical/10 border border-critical/30 text-critical text-xs space-y-1">
                            <div className="font-bold">{m.rule}</div>
                            <div className="text-text-2 text-[11px]">{m.text}</div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ) : (
                <div className="p-8 text-center text-text-muted font-mono text-xs mt-6">
                  Fill in transaction details on the left and click "Screen Transaction Now" to view real-time fraud assessment.
                </div>
              )}
            </div>

            <p className="text-[11px] text-text-muted mt-4 pt-3 border-t border-borderSubtle font-mono">
              * Compliant with Federal Reserve SR 11-7 and BFIU Circular 28 pre-clearing statutory obligations.
            </p>
          </Card>
        </div>
      )}

      {/* MODAL: MANUAL TRANSACTION BLOCK */}
      {isBlockModalOpen && selectedTxToBlock && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs animate-in fade-in duration-200">
          <div className="bg-surface border border-border rounded-xl shadow-2xl max-w-md w-full overflow-hidden font-mono text-xs">
            <div className="p-4 bg-surfaceRaised border-b border-border flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 rounded bg-critical/20 text-critical flex items-center justify-center font-bold">
                  <Lock className="w-3.5 h-3.5" />
                </div>
                <h3 className="font-bold text-text text-sm">Intercept & Block Transaction</h3>
              </div>
              <button 
                onClick={() => setIsBlockModalOpen(false)}
                className="text-text-muted hover:text-text cursor-pointer"
              >
                ✕
              </button>
            </div>

            <div className="p-4 space-y-3">
              <div className="p-3 rounded bg-critical/10 border border-critical/30 text-critical space-y-1">
                <div className="font-bold">Immediate Administrative Hold (§15 BFIU / OFAC Stop)</div>
                <div className="text-[11px] text-text-2">
                  This action intercepts the payment before final settlement. A cryptographic WORM audit hash will be permanently anchored.
                </div>
              </div>

              <div className="space-y-1.5 p-2.5 rounded bg-bg border border-borderSubtle text-[11px]">
                <div className="flex justify-between">
                  <span className="text-text-muted">Transaction ID:</span>
                  <span className="font-bold text-text">{selectedTxToBlock.id}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-text-muted">Amount:</span>
                  <span className="font-bold text-critical">${Number(selectedTxToBlock.amount).toLocaleString()} USD</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-text-muted">Entity:</span>
                  <span className="font-semibold text-text truncate max-w-[200px]">{selectedTxToBlock.sourceEntity}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-text-muted">Clearing Rail:</span>
                  <span className="font-semibold text-text">{selectedTxToBlock.rail}</span>
                </div>
              </div>

              <div>
                <label className="text-[11px] text-text-muted block mb-1">Regulatory Reason for Blocking</label>
                <select
                  value={blockReason}
                  onChange={(e) => setBlockReason(e.target.value)}
                  className="ui-input h-8 w-full text-xs"
                >
                  <option value="Sub-threshold CTR structuring pattern detected ($9k-$9.95k cluster)">
                    Sub-threshold CTR structuring pattern detected
                  </option>
                  <option value="High-Velocity Layering Outflow into Offshore Secrecy Jurisdiction">
                    High-Velocity Outflow into Offshore Shell Entity
                  </option>
                  <option value="Trade-Based Pricing Discrepancy >200% against Customs Benchmark">
                    Trade-Based Over-Invoicing / Customs Discrepancy
                  </option>
                  <option value="Pass-through mule zero-dwell rapid pass-through syndicate">
                    Pass-through mule ring zero-dwell velocity
                  </option>
                  <option value="Manual Suspicion: Inconsistent Customer Profile & Source of Wealth">
                    Inconsistent Customer Profile & Source of Wealth
                  </option>
                </select>
              </div>
            </div>

            <div className="p-4 bg-surfaceRaised border-t border-border flex justify-end gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setIsBlockModalOpen(false)}
              >
                Cancel
              </Button>
              <Button
                variant="critical"
                size="sm"
                onClick={handleConfirmBlock}
                icon={Lock}
              >
                Confirm Administrative Block
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* MODAL: UNBLOCK / RELEASE DUAL SIGN-OFF */}
      {isUnblockModalOpen && selectedBlockToRelease && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs animate-in fade-in duration-200">
          <div className="bg-surface border border-border rounded-xl shadow-2xl max-w-md w-full overflow-hidden font-mono text-xs">
            <div className="p-4 bg-surfaceRaised border-b border-border flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 rounded bg-cleared/20 text-cleared flex items-center justify-center font-bold">
                  <Unlock className="w-3.5 h-3.5" />
                </div>
                <h3 className="font-bold text-text text-sm">Four-Eyes Dual Control Release</h3>
              </div>
              <button 
                onClick={() => setIsUnblockModalOpen(false)}
                className="text-text-muted hover:text-text cursor-pointer"
              >
                ✕
              </button>
            </div>

            <div className="p-4 space-y-3">
              <div className="p-3 rounded bg-amber-500/10 border border-amber-500/30 text-amber-500 space-y-1">
                <div className="font-bold">Dual Signatory Verification Required</div>
                <div className="text-[11px] text-text-2">
                  Under statutory Four-Eyes controls, releasing an administrative hold requires Chief Compliance Officer sign-off and permanent cryptographic audit logging.
                </div>
              </div>

              <div className="space-y-1.5 p-2.5 rounded bg-bg border border-borderSubtle text-[11px]">
                <div className="flex justify-between">
                  <span className="text-text-muted">Block ID:</span>
                  <span className="font-bold text-text">{selectedBlockToRelease.id}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-text-muted">Original Reference:</span>
                  <span className="font-bold text-text">{selectedBlockToRelease.txId}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-text-muted">Quarantined Amount:</span>
                  <span className="font-bold text-cleared">${Number(selectedBlockToRelease.amount).toLocaleString()} USD</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-text-muted">Blocked By:</span>
                  <span className="font-semibold text-text">{selectedBlockToRelease.blockedBy}</span>
                </div>
              </div>

              <div>
                <label className="text-[11px] text-text-muted block mb-1">
                  Compliance Justification for Release <span className="text-critical">*</span>
                </label>
                <textarea
                  rows={3}
                  value={unblockJustification}
                  onChange={(e) => setUnblockJustification(e.target.value)}
                  placeholder="Enter verified documentary evidence (e.g. Verified Export Form EXP #9910 submitted and ASYCUDA customs valuation cleared)..."
                  className="ui-input w-full p-2 text-xs font-mono"
                  required
                />
              </div>
            </div>

            <div className="p-4 bg-surfaceRaised border-t border-border flex justify-end gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setIsUnblockModalOpen(false)}
              >
                Cancel
              </Button>
              <Button
                variant="primary"
                size="sm"
                onClick={handleConfirmUnblock}
                icon={Unlock}
              >
                Certify & Release Hold
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
