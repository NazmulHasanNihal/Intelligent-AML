import React, { useState, useMemo } from 'react';
import { 
  Search, 
  Filter, 
  Download, 
  CheckSquare, 
  Square, 
  UserCheck, 
  Trash2, 
  FileText, 
  ArrowUpDown,
  ChevronLeft,
  ChevronRight,
  ShieldAlert,
  Clock,
  Sparkles,
  ShieldCheck,
  Mail,
  CheckCircle2,
  AlertTriangle,
  Flame,
  Layers,
  Zap,
  RotateCcw
} from 'lucide-react';
import { useAppStore } from '../../lib/store';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';

export const AlertsView = () => {
  const { 
    alerts, 
    alertFilters, 
    setAlertFilters, 
    selectedAlertIds, 
    toggleSelectAlert, 
    selectAllAlerts,
    bulkAssign,
    bulkDismiss,
    createCaseFromAlert,
    openDrawer,
    navigate,
    addToast,
    quickQuarantine,
    quickEscalate,
    quickRFI,
    quickClear,
    batchQuarantine,
    batchRFI,
    batchClear
  } = useAppStore();

  const [dismissReasonModal, setDismissReasonModal] = useState(false);
  const [selectedTypology, setSelectedTypology] = useState('ALL');
  const [selectedDecisionSet, setSelectedDecisionSet] = useState('ALL'); // 'ALL' | 'GAMMA_1' | 'GAMMA_01' | 'GAMMA_0'
  
  // High-Throughput Windowing / Virtual Pagination (prevents DOM re-render lag under 100+ tx/s)
  const [page, setPage] = useState(0);
  const pageSize = 12;

  // Multi-Filter Pipeline
  const filteredAlerts = useMemo(() => {
    return alerts.filter((alert) => {
      // Tier filter
      if (alertFilters.tier !== 'ALL') {
        if (alertFilters.tier === 'TIER1' && alert.tierCode !== 1) return false;
        if (alertFilters.tier === 'TIER2' && alert.tierCode !== 2) return false;
        if (alertFilters.tier === 'TIER3' && alert.tierCode !== 3) return false;
      }

      // Rail filter
      if (alertFilters.rail !== 'ALL') {
        if (!alert.rail.toLowerCase().includes(alertFilters.rail.toLowerCase())) return false;
      }

      // Decision Set Filter (CRC)
      if (selectedDecisionSet !== 'ALL') {
        if (selectedDecisionSet === 'GAMMA_1' && alert.decisionSet !== 'Γ = {1}' && alert.tierCode !== 1) return false;
        if (selectedDecisionSet === 'GAMMA_01' && alert.decisionSet !== 'Γ = {0,1}' && alert.tierCode !== 2) return false;
        if (selectedDecisionSet === 'GAMMA_0' && alert.decisionSet !== 'Γ = {0}' && alert.tierCode !== 3) return false;
      }

      // Typology Filter
      if (selectedTypology !== 'ALL') {
        const typText = (alert.typologyBadge || alert.typology || alert.whyFlagged || '').toLowerCase();
        if (!typText.includes(selectedTypology.toLowerCase())) return false;
      }

      // Search Query
      if (alertFilters.search) {
        const q = alertFilters.search.toLowerCase();
        const match = (alert.entityName || '').toLowerCase().includes(q) ||
                      (alert.account || '').toLowerCase().includes(q) ||
                      (alert.typology || alert.whyFlagged || '').toLowerCase().includes(q) ||
                      (alert.id || '').toLowerCase().includes(q);
        if (!match) return false;
      }

      return true;
    });
  }, [alerts, alertFilters, selectedDecisionSet, selectedTypology]);

  // Windowed Slice
  const totalPages = Math.ceil(filteredAlerts.length / pageSize) || 1;
  const paginatedAlerts = useMemo(() => {
    const start = page * pageSize;
    return filteredAlerts.slice(start, start + pageSize);
  }, [filteredAlerts, page, pageSize]);

  const allSelected = paginatedAlerts.length > 0 && paginatedAlerts.every(a => selectedAlertIds.includes(a.id));

  const handleExportCSV = () => {
    const headers = ['AlertID', 'CaseID', 'Timestamp', 'Account', 'EntityName', 'Amount', 'Rail', 'RiskScore', 'Tier', 'Status', 'Typology', 'DecisionSet'];
    const rows = filteredAlerts.map(a => [
      a.id, a.caseId || 'N/A', a.timestamp || a.date || 'N/A', a.account, a.entityName, a.amount, a.rail, a.riskScore, a.tier, a.status, `"${a.typologyBadge || a.typology || 'Flagged'}"`, `"${a.decisionSet || 'Γ={1}'}"`
    ]);
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `AML_Alert_Queue_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    addToast('CSV Exported', `Exported ${filteredAlerts.length} alerts to CSV.`, 'info');
  };

  return (
    <div className="space-y-3 select-none relative pb-16">
      {/* Top Filter Chips & Search Bar */}
      <div className="p-3.5 rounded-lg bg-surface border border-border space-y-3 text-xs">
        {/* Row 1: Search + Dropdowns */}
        <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">
          <div className="flex items-center gap-2 flex-wrap flex-1">
            {/* Search Box */}
            <div className="relative min-w-[200px] flex-1 sm:flex-initial">
              <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-text-muted" />
              <input
                id="alert-search-input"
                name="alert-search-input"
                aria-label="Filter alerts by account, entity, BIC, or alert ID"
                type="text"
                value={alertFilters.search}
                onChange={(e) => {
                  setAlertFilters({ search: e.target.value });
                  setPage(0);
                }}
                placeholder="Filter by account, entity, BIC, alert ID..."
                className="ui-input pl-8 w-full h-8 text-xs"
              />
            </div>

            {/* Tier Filter */}
            <select
              id="alert-tier-select"
              name="alert-tier-select"
              aria-label="Filter by alert tier"
              value={alertFilters.tier}
              onChange={(e) => {
                setAlertFilters({ tier: e.target.value });
                setPage(0);
              }}
              className="ui-input h-8 text-xs font-mono"
            >
              <option value="ALL">All Tiers (3-Tier)</option>
              <option value="TIER1">Tier 1 Hold (&gt;85%)</option>
              <option value="TIER2">Tier 2 Review Queue</option>
              <option value="TIER3">Tier 3 Clear (&lt;30%)</option>
            </select>

            {/* Rail Filter */}
            <select
              id="alert-rail-select"
              name="alert-rail-select"
              aria-label="Filter by clearing rail"
              value={alertFilters.rail}
              onChange={(e) => {
                setAlertFilters({ rail: e.target.value });
                setPage(0);
              }}
              className="ui-input h-8 text-xs font-mono"
            >
              <option value="ALL">All Clearing Rails</option>
              <option value="SWIFT">SWIFT (MT103 / MT700 LC)</option>
              <option value="RTGS">RTGS (BD Bank)</option>
              <option value="bKash">bKash MFS</option>
              <option value="BEFTN">BEFTN</option>
              <option value="Fedwire">Fedwire / CHAPS</option>
            </select>
          </div>

          {/* Right Actions */}
          <div className="flex items-center gap-2 shrink-0">
            <Button
              variant="outline"
              size="sm"
              onClick={handleExportCSV}
              icon={Download}
            >
              Export CSV
            </Button>
          </div>
        </div>

        {/* Row 2: Multi-Select Filter Chips (Typology & Decision Set) */}
        <div className="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-borderSubtle">
          {/* Rail & CRC Decision Chips */}
          <div className="flex items-center gap-1.5 flex-wrap">
            <span className="text-text-muted font-mono text-[10px] uppercase">Decision Set Γ:</span>
            {[
              { id: 'ALL', label: 'All Sets' },
              { id: 'GAMMA_1', label: 'Γ = {1} (Hold)' },
              { id: 'GAMMA_01', label: 'Γ = {0,1} (Review)' },
              { id: 'GAMMA_0', label: 'Γ = {0} (Clear)' }
            ].map(chip => (
              <button
                key={chip.id}
                onClick={() => { setSelectedDecisionSet(chip.id); setPage(0); }}
                className={`px-2 py-0.5 rounded text-[11px] font-mono transition-colors cursor-pointer ${
                  selectedDecisionSet === chip.id
                    ? 'bg-accent/15 border border-accent/40 font-bold text-accent'
                    : 'bg-bg text-text-muted border border-border hover:text-text'
                }`}
              >
                {chip.label}
              </button>
            ))}
          </div>

          {/* Typology Chips */}
          <div className="flex items-center gap-1.5 flex-wrap">
            <span className="text-text-muted font-mono text-[10px] uppercase">Typology:</span>
            {[
              { id: 'ALL', label: 'All Typologies' },
              { id: 'structuring', label: 'Structuring' },
              { id: 'smurfing', label: 'Smurfing' },
              { id: 'layering', label: 'Layering' },
              { id: 'over-invoicing', label: 'TBML Over-Invoice' }
            ].map(typ => (
              <button
                key={typ.id}
                onClick={() => { setSelectedTypology(typ.id); setPage(0); }}
                className={`px-2 py-0.5 rounded text-[11px] font-mono transition-colors cursor-pointer ${
                  selectedTypology === typ.id
                    ? 'bg-surfaceRaised border border-border font-bold text-text shadow-xs'
                    : 'bg-bg text-text-muted border border-border hover:text-text'
                }`}
              >
                {typ.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Full-Width Table with Inline Quick-Actions */}
      <Card padding={false} className="overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-surfaceRaised border-b border-border text-text-muted font-mono text-[11px] uppercase tracking-wider select-none">
              <tr>
                <th className="py-2.5 px-3 w-8">
                  <button
                    onClick={() => selectAllAlerts(!allSelected)}
                    className="p-1 hover:text-text cursor-pointer block"
                    title="Select All on Current Page"
                  >
                    {allSelected ? (
                      <CheckSquare className="w-3.5 h-3.5 text-accent" />
                    ) : (
                      <Square className="w-3.5 h-3.5 text-text-muted" />
                    )}
                  </button>
                </th>
                <th className="py-2.5 px-3">Alert ID</th>
                <th className="py-2.5 px-3">Entity / Account</th>
                <th className="py-2.5 px-3">Typology Badge</th>
                <th className="py-2.5 px-3">Amount (USD / BDT)</th>
                <th className="py-2.5 px-3">Rail</th>
                <th className="py-2.5 px-3">Risk Score</th>
                <th className="py-2.5 px-3">Decision Set</th>
                <th className="py-2.5 px-3">Status</th>
                <th className="py-2.5 px-3 text-right">Inline Quick Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-borderSubtle">
              {paginatedAlerts.length === 0 ? (
                <tr>
                  <td colSpan={10} className="py-8 text-center text-text-muted text-xs">
                    No alerts match the active filter criteria.
                  </td>
                </tr>
              ) : (
                paginatedAlerts.map((alert) => {
                  const isSelected = selectedAlertIds.includes(alert.id);
                  const isTier1 = alert.tierCode === 1;
                  const isTier2 = alert.tierCode === 2;

                  return (
                    <tr
                      key={alert.id}
                      onClick={() => openDrawer(alert)}
                      className={`hover:bg-surfaceHover/80 transition-colors cursor-pointer group ${
                        isSelected ? 'bg-accent/5' : ''
                      }`}
                    >
                      {/* Checkbox */}
                      <td 
                        className="py-2.5 px-3 w-8"
                        onClick={(e) => {
                          e.stopPropagation();
                          toggleSelectAlert(alert.id);
                        }}
                      >
                        {isSelected ? (
                          <CheckSquare className="w-3.5 h-3.5 text-accent" />
                        ) : (
                          <Square className="w-3.5 h-3.5 text-text-muted" />
                        )}
                      </td>

                      {/* Alert ID */}
                      <td className="py-2.5 px-3 font-mono font-medium text-text">
                        {alert.id}
                      </td>

                      {/* Entity & Account */}
                      <td className="py-2.5 px-3">
                        <div className="font-semibold text-text truncate max-w-[170px]">
                          {alert.entityName}
                        </div>
                        <div className="font-mono text-[10px] text-text-muted truncate max-w-[170px]">
                          {alert.account}
                        </div>
                      </td>

                      {/* Visual Typology Indicator Badge */}
                      <td className="py-2.5 px-3">
                        <span className={`inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-mono font-semibold border ${
                          isTier1 
                            ? 'bg-critical/10 text-critical border-critical/30' 
                            : isTier2 
                            ? 'bg-review/10 text-review border-review/30'
                            : 'bg-cleared/10 text-cleared border-cleared/30'
                        }`}>
                          <Sparkles className="w-2.5 h-2.5" />
                          <span>{alert.typologyBadge || alert.typology || 'Structuring (<$10k)'}</span>
                        </span>
                      </td>

                      {/* Amount */}
                      <td className="py-2.5 px-3 font-mono">
                        <span className="font-semibold text-text block">
                          ${alert.amount.toLocaleString()} USD
                        </span>
                        <span className="text-[10px] text-text-muted block">
                          ৳{(alert.amount * 120).toLocaleString()} BDT
                        </span>
                      </td>

                      {/* Rail */}
                      <td className="py-2.5 px-3 font-mono text-[11px] text-text-2">
                        {alert.rail}
                      </td>

                      {/* Risk Score */}
                      <td className="py-2.5 px-3 font-mono">
                        <span className={`font-bold ${isTier1 ? 'text-critical' : isTier2 ? 'text-review' : 'text-cleared'}`}>
                          {(alert.riskScore * 100).toFixed(1)}%
                        </span>
                      </td>

                      {/* Decision Set Γ */}
                      <td className="py-2.5 px-3 font-mono text-[11px]">
                        <span className="px-1.5 py-0.5 rounded bg-bg border border-borderSubtle font-semibold text-text">
                          {alert.decisionSet || (isTier1 ? 'Γ = {1}' : isTier2 ? 'Γ = {0,1}' : 'Γ = {0}')}
                        </span>
                      </td>

                      {/* Status */}
                      <td className="py-2.5 px-3 font-mono text-[10px]">
                        <Badge 
                          variant={isTier1 ? 'critical' : isTier2 ? 'review' : 'cleared'}
                          size="sm"
                          dot
                        >
                          {alert.status || (isTier1 ? 'QUARANTINED' : isTier2 ? 'PENDING_REVIEW' : 'CLEARED')}
                        </Badge>
                      </td>

                      {/* Inline Quick Action Buttons */}
                      <td className="py-2.5 px-3 text-right">
                        <div 
                          className="flex items-center justify-end gap-1"
                          onClick={(e) => e.stopPropagation()}
                        >
                          {/* Quarantine Action */}
                          <button
                            onClick={() => quickQuarantine(alert.id)}
                            title="Quarantine (Apply Tier-1 Hold)"
                            className="p-1 rounded bg-surface hover:bg-critical/15 text-text-muted hover:text-critical border border-border transition-colors cursor-pointer"
                          >
                            <ShieldAlert className="w-3.5 h-3.5" />
                          </button>

                          {/* Escalate to Case */}
                          <button
                            onClick={() => quickEscalate(alert.id)}
                            title="Escalate to Case Docket"
                            className="p-1 rounded bg-surface hover:bg-accent/15 text-text-muted hover:text-accent border border-border transition-colors cursor-pointer"
                          >
                            <FileText className="w-3.5 h-3.5" />
                          </button>

                          {/* Dispatch RFI */}
                          <button
                            onClick={() => quickRFI(alert.id)}
                            title="Dispatch Document Verification RFI"
                            className="p-1 rounded bg-surface hover:bg-review/15 text-text-muted hover:text-review border border-border transition-colors cursor-pointer"
                          >
                            <Mail className="w-3.5 h-3.5" />
                          </button>

                          {/* Clear as Licit */}
                          <button
                            onClick={() => quickClear(alert.id)}
                            title="Clear as Licit (Tier-3 Rule CDD-26)"
                            className="p-1 rounded bg-surface hover:bg-cleared/15 text-text-muted hover:text-cleared border border-border transition-colors cursor-pointer"
                          >
                            <CheckCircle2 className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>

        {/* Table Virtual Windowing / Pagination Footer */}
        <div className="p-3 border-t border-border bg-surfaceRaised flex items-center justify-between text-xs text-text-muted font-mono">
          <div>
            Showing {filteredAlerts.length === 0 ? 0 : page * pageSize + 1}–
            {Math.min((page + 1) * pageSize, filteredAlerts.length)} of {filteredAlerts.length} queue entries
          </div>

          <div className="flex items-center gap-1.5">
            <button
              onClick={() => setPage(prev => Math.max(0, prev - 1))}
              disabled={page === 0}
              className="p-1 rounded border border-border hover:bg-surface disabled:opacity-40 cursor-pointer disabled:cursor-not-allowed transition-colors"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="px-2 font-bold text-text">
              Page {page + 1} of {totalPages}
            </span>
            <button
              onClick={() => setPage(prev => Math.min(totalPages - 1, prev + 1))}
              disabled={page >= totalPages - 1}
              className="p-1 rounded border border-border hover:bg-surface disabled:opacity-40 cursor-pointer disabled:cursor-not-allowed transition-colors"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </Card>

      {/* Floating Sticky Bulk Action Dock at Bottom (When Rows Checked) */}
      {selectedAlertIds.length > 0 && (
        <div className="fixed bottom-4 left-1/2 -translate-x-1/2 z-40 bg-surfaceRaised/95 backdrop-blur-md border border-accent shadow-2xl rounded-xl p-2.5 px-4 flex items-center gap-3 animate-fadeIn text-xs">
          <div className="flex items-center gap-2 border-r border-border pr-3">
            <Badge variant="accent" size="sm">
              {selectedAlertIds.length} Selected
            </Badge>
            <span className="text-text font-medium hidden sm:inline">Bulk Actions:</span>
          </div>

          <div className="flex items-center gap-2">
            <Button
              variant="danger"
              size="sm"
              onClick={() => batchQuarantine(selectedAlertIds)}
              icon={ShieldAlert}
              className="text-xs h-7"
            >
              Batch Tier-1 Freeze
            </Button>

            <Button
              variant="secondary"
              size="sm"
              onClick={() => batchRFI(selectedAlertIds)}
              icon={Mail}
              className="text-xs h-7"
            >
              Batch RFI Dispatch
            </Button>

            <Button
              variant="outline"
              size="sm"
              onClick={() => batchClear(selectedAlertIds)}
              icon={CheckCircle2}
              className="text-xs h-7 text-cleared hover:text-cleared"
            >
              Batch Clearance
            </Button>

            <button
              onClick={() => selectAllAlerts(false)}
              className="p-1 rounded hover:bg-surface text-text-muted hover:text-text text-[11px] font-mono cursor-pointer ml-1"
            >
              Deselect All
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
