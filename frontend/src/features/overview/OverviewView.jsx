import React, { useState, useMemo } from 'react';
import ReactECharts from 'echarts-for-react';
import { 
  ShieldAlert, 
  Clock, 
  CheckCircle2, 
  AlertTriangle, 
  ArrowUpRight, 
  Zap, 
  ChevronRight,
  TrendingUp,
  Cpu,
  ShieldCheck,
  Share2,
  UserCheck,
  Activity,
  Server,
  Search,
  Filter,
  ExternalLink,
  Eye,
  Radio
} from 'lucide-react';
import { useAppStore } from '../../lib/store';
import { Card, CardHeader } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';

export const OverviewView = () => {
  const { 
    telemetry, 
    metrics, 
    alerts, 
    cases, 
    liveTransactions,
    navigate, 
    openDrawer,
    quickQuarantine,
    setRoleModalOpen,
    consumerLagMsgs
  } = useAppStore();

  const [railFilter, setRailFilter] = useState('ALL');
  const [tierFilter, setTierFilter] = useState('ALL');
  const [txSearch, setTxSearch] = useState('');

  const urgentItems = alerts
    .filter(a => a.tierCode === 1 || a.tierCode === 2)
    .slice(0, 5);

  // ECharts Theme: Neutral grid, muted axes, throughput line + small alert bars beneath
  const chartOption = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    },
    grid: [
      { left: '7%', right: '4%', top: '12%', height: '50%' },
      { left: '7%', right: '4%', top: '72%', height: '20%' }
    ],
    xAxis: [
      {
        type: 'category',
        data: ['00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00', 'Now'],
        gridIndex: 0,
        axisLine: { lineStyle: { color: 'rgba(128, 128, 128, 0.2)' } },
        axisLabel: { color: '#717A8C', fontSize: 10, fontFamily: 'monospace' }
      },
      {
        type: 'category',
        data: ['00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00', 'Now'],
        gridIndex: 1,
        axisLine: { lineStyle: { color: 'rgba(128, 128, 128, 0.2)' } },
        axisLabel: { show: false }
      }
    ],
    yAxis: [
      {
        type: 'value',
        name: 'Throughput (tx/s)',
        gridIndex: 0,
        splitLine: { lineStyle: { color: 'rgba(128, 128, 128, 0.12)' } },
        axisLabel: { color: '#717A8C', fontSize: 10, fontFamily: 'monospace' },
        nameTextStyle: { color: '#717A8C', fontSize: 10, padding: [0, 0, 4, 0] }
      },
      {
        type: 'value',
        name: 'Flagged Alerts',
        nameLocation: 'end',
        gridIndex: 1,
        splitLine: { show: false },
        axisLabel: { color: '#717A8C', fontSize: 9, fontFamily: 'monospace' },
        nameTextStyle: { color: '#717A8C', fontSize: 9, padding: [0, 0, 2, 28] }
      }
    ],
    series: [
      {
        name: 'Throughput (tx/s)',
        type: 'line',
        smooth: true,
        showSymbol: false,
        xAxisIndex: 0,
        yAxisIndex: 0,
        data: [410, 395, 480, 520, 640, 580, 510, 490, 500],
        itemStyle: { color: '#4C8DF6' },
        lineStyle: { width: 2 }
      },
      {
        name: 'Flagged Alerts',
        type: 'bar',
        xAxisIndex: 1,
        yAxisIndex: 1,
        data: [4, 2, 7, 12, 18, 14, 9, 6, 8],
        itemStyle: { color: '#F2555A', borderRadius: [2, 2, 0, 0] },
        barWidth: '35%'
      }
    ]
  };

  return (
    <div className="space-y-4 select-none">
      {/* Real-Time Pipeline Telemetry & Consumer Lag Indicator Banner */}
      <div className="p-3 rounded-lg bg-surfaceRaised border border-border flex flex-wrap items-center justify-between gap-3 text-xs font-mono">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-cleared animate-ping" />
            <span className="font-semibold text-text">Kafka Streaming Gateway:</span>
          </div>
          <div className="flex items-center gap-2 text-text-2">
            <span>Lag: <strong className="text-cleared font-bold">{consumerLagMsgs} msgs</strong> behind head</span>
            <span>•</span>
            <span>Latency: <strong className="text-text font-bold">0.12 ms</strong></span>
            <span>•</span>
            <span className="hidden sm:inline">Watermark: <strong className="text-text">Partition 0/Offset 148,312</strong></span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setRoleModalOpen(true)}
            icon={UserCheck}
            className="h-7 text-xs font-mono"
          >
            Role Delegation (Maker/Checker)
          </Button>
        </div>
      </div>

      {/* 4 Plain, Elegant KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        <Card className="flex flex-col justify-between">
          <div>
            <span className="text-xs text-text-muted font-medium block">24h Processed Volume</span>
            <div className="text-xl sm:text-2xl font-bold text-text mt-1 tabular-nums font-mono">
              {telemetry.totalProcessed24h.toLocaleString()}
            </div>
          </div>
          <div className="flex items-center gap-1.5 text-xs text-cleared font-mono mt-3">
            <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
            <span className="font-semibold">{metrics.stpRate}% STP Cleared</span>
          </div>
        </Card>

        <Card className="flex flex-col justify-between">
          <div>
            <span className="text-xs text-text-muted font-medium block">Tier 1 Auto-Quarantine</span>
            <div className="text-xl sm:text-2xl font-bold text-critical mt-1 tabular-nums font-mono">
              {telemetry.tier1Quarantined.toLocaleString()}
            </div>
          </div>
          <div className="flex items-center gap-1.5 text-xs text-text-2 font-mono mt-3">
            <span className="w-1.5 h-1.5 rounded-full bg-critical" />
            <span>{metrics.quarantineRate}% of Total Volume</span>
          </div>
        </Card>

        <Card className="flex flex-col justify-between">
          <div>
            <span className="text-xs text-text-muted font-medium block">Tier 2 Review Queue</span>
            <div className="text-xl sm:text-2xl font-bold text-review mt-1 tabular-nums font-mono">
              {telemetry.tier2ReviewQueue.toLocaleString()}
            </div>
          </div>
          <div className="flex items-center gap-1.5 text-xs text-text-2 font-mono mt-3">
            <span className="w-1.5 h-1.5 rounded-full bg-review" />
            <span>{metrics.reviewRate}% Analyst Queue</span>
          </div>
        </Card>

        <Card className="flex flex-col justify-between">
          <div>
            <span className="text-xs text-text-muted font-medium block">Quarantined Illicit Capital</span>
            <div className="text-xl sm:text-2xl font-bold text-critical mt-1 tabular-nums font-mono">
              $1,482,900
            </div>
            <span className="text-[11px] font-mono text-text-muted">৳177,948,000 BDT</span>
          </div>
          <div className="flex items-center gap-1.5 text-xs text-cleared font-mono mt-3">
            <ShieldCheck className="w-3.5 h-3.5 shrink-0 text-cleared" />
            <span>100% Held (BFIU §15 Order)</span>
          </div>
        </Card>
      </div>

      {/* Main Grid: Telemetry Chart & Attention List */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        {/* Left: Single-Focus Telemetry Chart */}
        <Card className="lg:col-span-8 flex flex-col justify-between min-h-[380px]">
          <CardHeader
            title="Stream Telemetry &amp; Detection Volume"
            subtitle="Throughput velocity (tx/s) with flagged anomalous event counts"
            badge={<Badge variant="neutral" size="sm">24-Hour Horizon</Badge>}
            action={
              <span className="text-xs font-mono text-text-muted">
                Avg: {telemetry.avgThroughputTxPerSec} tx/s • Peak: {telemetry.peakThroughputTxPerSec} tx/s
              </span>
            }
          />
          <div className="h-72 w-full mt-2">
            <ReactECharts option={chartOption} style={{ height: '100%', width: '100%' }} />
          </div>
        </Card>

        {/* Right: Urgent Attention Queue with Immediate Action Triggers */}
        <Card className="lg:col-span-4 flex flex-col justify-between">
          <div>
            <CardHeader
              title="Needs Attention Today"
              subtitle={`${urgentItems.length} priority items awaiting disposition`}
              badge={<Badge variant="critical" size="sm">Urgent</Badge>}
              action={
                <Button variant="ghost" size="sm" onClick={() => navigate('alerts')}>
                  View All
                </Button>
              }
            />

            <div className="divide-y divide-borderSubtle mt-2">
              {urgentItems.map((item) => (
                <div
                  key={item.id}
                  onClick={() => openDrawer(item)}
                  className="py-2.5 px-1 hover:bg-surfaceHover rounded transition-colors cursor-pointer flex flex-col gap-2"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="min-w-0">
                      <div className="flex items-center gap-1.5">
                        <span className="font-semibold text-text text-xs truncate max-w-[140px]">{item.entityName}</span>
                        <Badge variant={item.tierCode === 1 ? 'critical' : 'review'} size="sm">
                          {item.tierCode === 1 ? 'Tier 1' : 'Tier 2'}
                        </Badge>
                      </div>
                      <p className="font-mono text-[11px] text-text-muted mt-0.5 truncate">
                        ${item.amount.toLocaleString()} (৳{(item.amount * 120).toLocaleString()}) • {item.rail}
                      </p>
                    </div>

                    <div className="text-right shrink-0">
                      <span className="font-mono text-xs font-semibold text-text tabular-nums block">
                        {(item.riskScore * 100).toFixed(1)}%
                      </span>
                      <span className="text-[10px] text-review font-mono block">
                        {item.slaMinutesLeft}m left
                      </span>
                    </div>
                  </div>

                  {/* Immediate Action Triggers: Open Subgraph & Hold Transaction */}
                  <div 
                    className="flex items-center justify-end gap-1.5 pt-1"
                    onClick={(e) => e.stopPropagation()}
                  >
                    <button
                      onClick={() => navigate('network')}
                      className="px-2 py-0.5 rounded bg-surface hover:bg-surfaceHover border border-border text-[10px] font-mono text-text cursor-pointer transition-colors flex items-center gap-1"
                    >
                      <Share2 className="w-3 h-3 text-accent" />
                      <span>Open Subgraph</span>
                    </button>

                    <button
                      onClick={() => quickQuarantine(item.id)}
                      className="px-2 py-0.5 rounded bg-critical/10 hover:bg-critical/20 border border-critical/30 text-[10px] font-mono text-critical font-bold cursor-pointer transition-colors flex items-center gap-1"
                    >
                      <ShieldAlert className="w-3 h-3 text-critical" />
                      <span>Hold (T1)</span>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="pt-3 border-t border-borderSubtle flex items-center justify-between text-xs">
            <Button
              variant="outline"
              size="sm"
              className="w-full"
              onClick={() => navigate('cases')}
              icon={ArrowUpRight}
            >
              Open Case Workspace
            </Button>
          </div>
        </Card>
      </div>

      {/* Live Interbank Transaction Stream & Multi-Rail Clearing Feed */}
      <Card className="mt-4">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pb-3 border-b border-borderSubtle">
          <div>
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-cleared animate-ping" />
              <h3 className="text-sm font-semibold text-text">Live Multi-Rail Transaction Stream</h3>
              <Badge variant="neutral" size="sm" className="font-mono">
                {liveTransactions.length} Ingested Events
              </Badge>
            </div>
            <p className="text-xs text-text-muted mt-0.5">
              Real-time banking settlement across SWIFT MT103/700, Bangladesh Bank RTGS, BEFTN ACH, bKash & Nagad MFS, NBR e-Challan, and NPSB cards.
            </p>
          </div>

          <div className="flex items-center gap-2 flex-wrap text-xs">
            {/* Search Box */}
            <div className="relative">
              <Search className="w-3.5 h-3.5 text-text-muted absolute left-2.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={txSearch}
                onChange={(e) => setTxSearch(e.target.value)}
                placeholder="Search memo, account, ref..."
                className="pl-8 pr-2.5 py-1 text-xs rounded bg-surface border border-border text-text placeholder:text-text-muted focus:outline-none focus:border-accent w-48 font-mono"
              />
            </div>
          </div>
        </div>

        {/* Rail and Tier Filter Pills */}
        <div className="flex flex-wrap items-center justify-between gap-2 py-2.5 border-b border-borderSubtle text-[11px] font-mono">
          <div className="flex items-center gap-1.5 flex-wrap">
            <span className="text-text-muted mr-1">Clearing Rail:</span>
            {[
              { id: 'ALL', label: 'All Rails' },
              { id: 'MT700', label: 'SWIFT LC' },
              { id: 'MT103', label: 'SWIFT Wire' },
              { id: 'RTGS', label: 'RTGS' },
              { id: 'BEFTN', label: 'BEFTN ACH' },
              { id: 'MFS', label: 'bKash / Nagad' },
              { id: 'Challan', label: 'NBR Customs' },
              { id: 'NPSB', label: 'NPSB POS' },
              { id: 'CHAPS', label: 'CHAPS / SEPA' }
            ].map((r) => (
              <button
                key={r.id}
                onClick={() => setRailFilter(r.id)}
                className={`px-2 py-0.5 rounded transition-colors cursor-pointer ${
                  railFilter === r.id
                    ? 'bg-accent text-white font-semibold'
                    : 'bg-surface hover:bg-surfaceHover text-text-2 border border-border'
                }`}
              >
                {r.label}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-1.5">
            <span className="text-text-muted mr-1">Triage Tier:</span>
            {[
              { id: 'ALL', label: 'All' },
              { id: '1', label: 'T1 Hold', color: 'text-critical' },
              { id: '2', label: 'T2 Review', color: 'text-review' },
              { id: '3', label: 'T3 Clear', color: 'text-cleared' }
            ].map((t) => (
              <button
                key={t.id}
                onClick={() => setTierFilter(t.id)}
                className={`px-2 py-0.5 rounded transition-colors cursor-pointer ${
                  tierFilter === t.id
                    ? 'bg-surfaceRaised font-bold border border-accent text-text'
                    : `bg-surface hover:bg-surfaceHover border border-border ${t.color || 'text-text-2'}`
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>
        </div>

        {/* Live Transaction Ledger Table */}
        <div className="overflow-x-auto mt-2">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-borderSubtle text-[11px] font-mono text-text-muted">
                <th className="py-2 px-2 font-medium">Time &amp; Reference</th>
                <th className="py-2 px-2 font-medium">Payment Rail</th>
                <th className="py-2 px-2 font-medium">Originator &rarr; Beneficiary</th>
                <th className="py-2 px-2 font-medium text-right">Settlement Amount</th>
                <th className="py-2 px-2 font-medium">Remittance Narrative</th>
                <th className="py-2 px-2 font-medium text-center">Conformal Calibration</th>
                <th className="py-2 px-2 font-medium text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-borderSubtle font-mono text-[11px]">
              {liveTransactions
                .filter((tx) => {
                  if (railFilter !== 'ALL') {
                    if (railFilter === 'MFS' && !tx.rail?.includes('bKash') && !tx.rail?.includes('Nagad')) return false;
                    if (railFilter === 'CHAPS' && !tx.rail?.includes('CHAPS') && !tx.rail?.includes('SEPA')) return false;
                    if (railFilter !== 'MFS' && railFilter !== 'CHAPS' && !tx.rail?.includes(railFilter)) return false;
                  }
                  if (tierFilter !== 'ALL') {
                    if (String(tx.tierCode) !== tierFilter) return false;
                  }
                  if (txSearch) {
                    const q = txSearch.toLowerCase();
                    const match = (tx.sourceEntity || '').toLowerCase().includes(q) ||
                                  (tx.targetEntity || '').toLowerCase().includes(q) ||
                                  (tx.remittanceInfo || '').toLowerCase().includes(q) ||
                                  (tx.swiftReference || '').toLowerCase().includes(q) ||
                                  (tx.rail || '').toLowerCase().includes(q) ||
                                  (tx.id || '').toLowerCase().includes(q);
                    if (!match) return false;
                  }
                  return true;
                })
                .map((tx) => {
                  const railColor = 
                    tx.rail?.includes('LC') ? 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20' :
                    tx.rail?.includes('MT103') || tx.rail?.includes('COV') ? 'bg-blue-500/10 text-blue-400 border-blue-500/20' :
                    tx.rail?.includes('RTGS') ? 'bg-amber-500/10 text-amber-400 border-amber-500/20' :
                    tx.rail?.includes('BEFTN') ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' :
                    tx.rail?.includes('bKash') || tx.rail?.includes('Nagad') ? 'bg-rose-500/10 text-rose-400 border-rose-500/20' :
                    tx.rail?.includes('Challan') ? 'bg-purple-500/10 text-purple-400 border-purple-500/20' :
                    tx.rail?.includes('NPSB') ? 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20' :
                    'bg-teal-500/10 text-teal-400 border-teal-500/20';

                  return (
                    <tr 
                      key={tx.id || tx.swiftReference}
                      onClick={() => openDrawer({
                        account: tx.sourceAccount,
                        entityName: tx.sourceEntity,
                        tier: tx.tierLabel,
                        tierCode: tx.tierCode,
                        amount: tx.amount,
                        riskScore: tx.riskScore,
                        whyFlagged: tx.whyFlagged || 'Live stream evaluated transaction'
                      })}
                      className="hover:bg-surfaceHover transition-colors cursor-pointer"
                    >
                      {/* Time & Reference */}
                      <td className="py-2.5 px-2 whitespace-nowrap">
                        <span className="text-text block font-semibold">{tx.timestamp || 'Just now'}</span>
                        <span className="text-[10px] text-accent block truncate max-w-[130px]">{tx.swiftReference || tx.id}</span>
                      </td>

                      {/* Payment Rail Badge */}
                      <td className="py-2.5 px-2 whitespace-nowrap">
                        <span className={`px-2 py-0.5 rounded border text-[10px] font-semibold ${railColor}`}>
                          {tx.rail}
                        </span>
                      </td>

                      {/* Originator -> Beneficiary */}
                      <td className="py-2.5 px-2 max-w-[240px]">
                        <div className="truncate">
                          <span className="font-semibold text-text">{tx.sourceEntity}</span>
                        </div>
                        <div className="text-[10px] text-text-muted truncate flex items-center gap-1">
                          <span>&rarr;</span>
                          <span>{tx.targetEntity}</span>
                        </div>
                      </td>

                      {/* Amount Dual Currency */}
                      <td className="py-2.5 px-2 text-right whitespace-nowrap">
                        <span className="font-bold text-text tabular-nums block">
                          {tx.currency === 'USD' ? `$${Number(tx.amount).toLocaleString(undefined, { minimumFractionDigits: 2 })}` :
                           tx.currency === 'EUR' ? `€${Number(tx.amount).toLocaleString(undefined, { minimumFractionDigits: 2 })}` :
                           tx.currency === 'GBP' ? `£${Number(tx.amount).toLocaleString(undefined, { minimumFractionDigits: 2 })}` :
                           `৳${Number(tx.amount).toLocaleString(undefined, { minimumFractionDigits: 2 })}`}
                        </span>
                        {tx.currency !== 'BDT' && (
                          <span className="text-[10px] text-text-muted tabular-nums block">
                            ৳{Number(tx.amountBdt || tx.amount * 120).toLocaleString(undefined, { maximumFractionDigits: 0 })} BDT
                          </span>
                        )}
                      </td>

                      {/* Remittance Narrative */}
                      <td className="py-2.5 px-2 max-w-[260px]">
                        <p className="text-[11px] text-text-2 line-clamp-2 leading-tight">
                          {tx.remittanceInfo || 'Commercial settlement under statutory monitoring'}
                        </p>
                      </td>

                      {/* Conformal Calibration */}
                      <td className="py-2.5 px-2 text-center whitespace-nowrap">
                        <Badge 
                          variant={tx.tierCode === 1 ? 'critical' : tx.tierCode === 2 ? 'review' : 'cleared'}
                          size="sm"
                          className="font-mono"
                        >
                          {tx.tierCode === 1 ? 'Tier 1 Hold' : tx.tierCode === 2 ? 'Tier 2 Review' : 'Tier 3 Clear'}
                        </Badge>
                        <span className="text-[9px] text-text-muted block mt-0.5">
                          {tx.conformalSet || (tx.tierCode === 1 ? 'Γ={1}' : tx.tierCode === 2 ? 'Γ={0,1}' : 'Γ={0}')}
                        </span>
                      </td>

                      {/* Actions */}
                      <td className="py-2.5 px-2 text-right whitespace-nowrap" onClick={(e) => e.stopPropagation()}>
                        <button
                          onClick={() => openDrawer({
                            account: tx.sourceAccount,
                            entityName: tx.sourceEntity,
                            tier: tx.tierLabel,
                            tierCode: tx.tierCode,
                            amount: tx.amount,
                            riskScore: tx.riskScore,
                            whyFlagged: tx.whyFlagged || 'Live stream evaluated transaction'
                          })}
                          className="p-1 rounded hover:bg-surface border border-border text-text-muted hover:text-accent transition-colors"
                          title="Inspect complete transaction telemetry in drawer"
                        >
                          <Eye className="w-3.5 h-3.5" />
                        </button>
                      </td>
                    </tr>
                  );
                })}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
