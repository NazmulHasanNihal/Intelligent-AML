import React, { useState, useMemo } from 'react';
import { 
  Building2, 
  User, 
  ShieldAlert, 
  ShieldCheck, 
  Search, 
  Download, 
  Lock, 
  Unlock, 
  FileText, 
  Share2, 
  Clock, 
  CreditCard, 
  DollarSign, 
  Phone, 
  Mail, 
  MapPin, 
  Calendar, 
  CheckCircle2, 
  AlertTriangle, 
  ArrowUpRight, 
  ArrowDownLeft, 
  ExternalLink, 
  Sparkles,
  ChevronRight,
  Shield,
  Layers,
  History
} from 'lucide-react';
import { useAppStore } from '../../lib/store';
import { Card, CardHeader } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';

export const ProfilesView = () => {
  const { 
    entities360, 
    openFreezeNoticeModal, 
    openSanctionsModalWithQuery, 
    navigate, 
    addToast 
  } = useAppStore();

  const entityList = useMemo(() => {
    return Object.values(entities360);
  }, [entities360]);

  const [selectedAccount, setSelectedAccount] = useState('BD22-EBLB-4829-1092-8823');
  const [profileSearch, setProfileSearch] = useState('');
  const [activeProfileTab, setActiveProfileTab] = useState('ledger'); // 'ledger' | 'kyc' | 'activity' | 'flow'
  const [ledgerFilter, setLedgerFilter] = useState('ALL'); // 'ALL' | 'IN' | 'OUT'

  // Filtered customer list
  const filteredCustomers = useMemo(() => {
    return entityList.filter(e => {
      if (!profileSearch) return true;
      const q = profileSearch.toLowerCase();
      return (
        (e.name || '').toLowerCase().includes(q) ||
        (e.account || '').toLowerCase().includes(q) ||
        (e.tin || '').toLowerCase().includes(q) ||
        (e.jurisdiction || '').toLowerCase().includes(q) ||
        (e.legalType || '').toLowerCase().includes(q)
      );
    });
  }, [entityList, profileSearch]);

  const selectedEntity = entities360[selectedAccount] || entityList[0];

  // Filtered ledger for selected entity
  const filteredLedger = useMemo(() => {
    const list = selectedEntity.ledger || [];
    if (ledgerFilter === 'ALL') return list;
    return list.filter(tx => tx.type === ledgerFilter);
  }, [selectedEntity, ledgerFilter]);

  // Export Customer Ledger to CSV
  const handleExportLedgerCSV = () => {
    const list = selectedEntity.ledger || [];
    if (list.length === 0) return;

    const headers = ['Transaction ID', 'Date', 'Direction', 'Counterparty', 'Counterparty Account', 'Amount USD', 'Amount BDT', 'Clearing Rail', 'Status', 'Memo'];
    const rows = list.map(tx => [
      tx.id,
      tx.date,
      tx.type,
      `"${tx.counterparty || ''}"`,
      tx.counterpartyAccount,
      tx.amount,
      tx.amountBdt,
      tx.rail,
      tx.status,
      `"${tx.memo || ''}"`
    ]);

    const csvContent = [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${selectedEntity.name.replace(/\s+/g, '_')}_Ledger_${Date.now()}.csv`;
    link.click();
    URL.revokeObjectURL(url);
    addToast('Ledger Exported', `Exported ${list.length} ledger records for ${selectedEntity.name}.`, 'success');
  };

  const isCorp = selectedEntity.legalType?.includes('Company') || selectedEntity.legalType?.includes('Corporate') || selectedEntity.legalType?.includes('Establishment');

  return (
    <div className="space-y-4 select-none">
      {/* Top Banner */}
      <div className="p-4 rounded-lg bg-surface border border-border flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div>
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded bg-accent/15 text-accent flex items-center justify-center font-bold">
              <User className="w-4 h-4" />
            </div>
            <h2 className="text-sm font-semibold text-text">Customer Profiles & Entity Due Diligence Dossier</h2>
            <Badge variant="neutral" size="sm">360° Comprehensive Dossier</Badge>
          </div>
          <p className="text-xs text-text-muted mt-0.5">
            Complete customer KYC background, beneficial ownership, historical transaction ledger, and tamper-evident activity logs.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => openSanctionsModalWithQuery(selectedEntity.name)}
            icon={Shield}
          >
            Screen Sanctions & PEP
          </Button>
          <Button
            variant="critical"
            size="sm"
            onClick={() => openFreezeNoticeModal({
              accountNumber: selectedEntity.account,
              holderName: selectedEntity.name,
              amount: 48500,
              rail: 'SWIFT MT700 (LC)'
            })}
            icon={Lock}
          >
            Place Account Freeze
          </Button>
        </div>
      </div>

      {/* Main Grid: Customer Directory (Left) + Detailed Dossier (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        {/* Left Column: Customer Directory */}
        <div className="lg:col-span-4 space-y-3">
          <Card padding={false} className="overflow-hidden">
            <div className="p-3 border-b border-border bg-surfaceRaised">
              <span className="text-xs font-bold text-text uppercase tracking-wider font-mono block mb-2">
                Customer Directory ({entityList.length})
              </span>
              <div className="relative">
                <Search className="w-3.5 h-3.5 absolute left-2.5 top-1/2 -translate-y-1/2 text-text-muted" />
                <input
                  type="text"
                  placeholder="Search customer, TIN, or account..."
                  value={profileSearch}
                  onChange={(e) => setProfileSearch(e.target.value)}
                  className="ui-input pl-8 h-7.5 w-full text-xs font-mono"
                />
              </div>
            </div>

            <div className="divide-y divide-borderSubtle max-h-[580px] overflow-y-auto">
              {filteredCustomers.map((cust) => {
                const isSelected = cust.account === selectedAccount;
                const isHighRisk = cust.riskScore > 0.80;
                const isMedRisk = cust.riskScore > 0.30 && cust.riskScore <= 0.80;

                return (
                  <div
                    key={cust.account}
                    onClick={() => setSelectedAccount(cust.account)}
                    className={`p-3 transition-colors cursor-pointer flex items-center justify-between gap-2.5 ${
                      isSelected ? 'bg-accent/10 border-l-3 border-accent' : 'hover:bg-surfaceHover'
                    }`}
                  >
                    <div className="min-w-0 flex items-start gap-2.5">
                      <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 font-bold ${
                        isHighRisk ? 'bg-critical/15 text-critical' : isMedRisk ? 'bg-review/15 text-review' : 'bg-cleared/15 text-cleared'
                      }`}>
                        {cust.legalType?.includes('Corporate') || cust.legalType?.includes('Company') ? (
                          <Building2 className="w-4 h-4" />
                        ) : (
                          <User className="w-4 h-4" />
                        )}
                      </div>

                      <div className="min-w-0">
                        <h4 className="text-xs font-bold text-text truncate">{cust.name}</h4>
                        <p className="text-[10px] text-text-muted font-mono truncate">{cust.account}</p>
                        <p className="text-[10px] text-text-2 truncate">{cust.jurisdiction?.split(',')[0]}</p>
                      </div>
                    </div>

                    <div className="text-right shrink-0">
                      <span className={`text-[10px] font-mono font-bold block ${
                        isHighRisk ? 'text-critical' : isMedRisk ? 'text-review' : 'text-cleared'
                      }`}>
                        {(cust.riskScore * 100).toFixed(0)}%
                      </span>
                      <span className="text-[9px] text-text-muted font-mono block">
                        {isHighRisk ? 'Hold' : isMedRisk ? 'Review' : 'Clear'}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </Card>
        </div>

        {/* Right Column: Complete Entity Profile Dossier */}
        <div className="lg:col-span-8 space-y-4">
          {/* Header Card */}
          <Card className="space-y-4">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pb-3 border-b border-borderSubtle">
              <div className="flex items-center gap-3">
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center font-bold text-white shadow-md ${
                  selectedEntity.riskScore > 0.80 ? 'bg-critical' : selectedEntity.riskScore > 0.30 ? 'bg-amber-600' : 'bg-cleared'
                }`}>
                  {isCorp ? <Building2 className="w-6 h-6" /> : <User className="w-6 h-6" />}
                </div>

                <div>
                  <div className="flex items-center gap-2 flex-wrap">
                    <h3 className="text-base font-bold text-text">{selectedEntity.name}</h3>
                    <Badge variant={selectedEntity.riskScore > 0.80 ? 'critical' : selectedEntity.riskScore > 0.30 ? 'review' : 'cleared'} size="sm">
                      {selectedEntity.riskRating || (selectedEntity.riskScore > 0.80 ? 'Tier 1 Hold' : 'Tier 3 Clear')}
                    </Badge>
                  </div>
                  <p className="text-xs text-text-muted font-mono mt-0.5">{selectedEntity.account} • {selectedEntity.institution || 'Partner Bank'}</p>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => navigate('network')}
                  icon={Share2}
                >
                  Network Studio
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => navigate('requests')}
                  icon={FileText}
                >
                  Issue RFI
                </Button>
              </div>
            </div>

            {/* Quick Metrics Bar */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs font-mono">
              <div className="p-2.5 rounded bg-bg border border-borderSubtle">
                <span className="text-[10px] text-text-muted uppercase block">Current Balance</span>
                <span className="font-bold text-text text-sm truncate block mt-0.5">{selectedEntity.balance || '$1,240,000 USD'}</span>
              </div>

              <div className="p-2.5 rounded bg-bg border border-borderSubtle">
                <span className="text-[10px] text-text-muted uppercase block">Account Age</span>
                <span className="font-semibold text-text truncate block mt-0.5">{selectedEntity.accountAge || '4 Years'}</span>
                <span className="text-[9px] text-text-muted block">Since {selectedEntity.openDate || '2022'}</span>
              </div>

              <div className="p-2.5 rounded bg-bg border border-borderSubtle">
                <span className="text-[10px] text-text-muted uppercase block">Tax Identification</span>
                <span className="font-semibold text-text truncate block mt-0.5">{selectedEntity.tin || 'TIN-Verified'}</span>
                <span className="text-[9px] text-cleared block">Verified TIN</span>
              </div>

              <div className="p-2.5 rounded bg-bg border border-borderSubtle">
                <span className="text-[10px] text-text-muted uppercase block">KYC Tier</span>
                <span className="font-semibold text-accent truncate block mt-0.5">{selectedEntity.kycTier?.split(' ')[0] || 'Tier-3'}</span>
                <span className="text-[9px] text-text-muted block">EDD Verified</span>
              </div>
            </div>
          </Card>

          {/* Dossier Tabs: Ledger | KYC | Activity Logs | Flow Profile */}
          <div className="flex items-center gap-1 border-b border-border text-xs font-mono">
            <button
              onClick={() => setActiveProfileTab('ledger')}
              className={`px-3 py-2 border-b-2 font-semibold transition-colors cursor-pointer flex items-center gap-1.5 ${
                activeProfileTab === 'ledger'
                  ? 'border-accent text-accent'
                  : 'border-transparent text-text-muted hover:text-text'
              }`}
            >
              <CreditCard className="w-3.5 h-3.5" />
              <span>Transaction History ({selectedEntity.ledger?.length || 0})</span>
            </button>

            <button
              onClick={() => setActiveProfileTab('kyc')}
              className={`px-3 py-2 border-b-2 font-semibold transition-colors cursor-pointer flex items-center gap-1.5 ${
                activeProfileTab === 'kyc'
                  ? 'border-accent text-accent'
                  : 'border-transparent text-text-muted hover:text-text'
              }`}
            >
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>KYC & Beneficial Ownership</span>
            </button>

            <button
              onClick={() => setActiveProfileTab('activity')}
              className={`px-3 py-2 border-b-2 font-semibold transition-colors cursor-pointer flex items-center gap-1.5 ${
                activeProfileTab === 'activity'
                  ? 'border-accent text-accent'
                  : 'border-transparent text-text-muted hover:text-text'
              }`}
            >
              <History className="w-3.5 h-3.5" />
              <span>Activity & Audit Trail ({selectedEntity.activityLogs?.length || 0})</span>
            </button>

            <button
              onClick={() => setActiveProfileTab('flow')}
              className={`px-3 py-2 border-b-2 font-semibold transition-colors cursor-pointer flex items-center gap-1.5 ${
                activeProfileTab === 'flow'
                  ? 'border-accent text-accent'
                  : 'border-transparent text-text-muted hover:text-text'
              }`}
            >
              <Layers className="w-3.5 h-3.5" />
              <span>Turnover & Flow Ratios</span>
            </button>
          </div>

          {/* TAB 1: TRANSACTION HISTORY LEDGER */}
          {activeProfileTab === 'ledger' && (
            <Card padding={false} className="overflow-hidden">
              <div className="p-3 border-b border-border bg-surfaceRaised flex flex-wrap items-center justify-between gap-2.5 text-xs font-mono">
                <div className="flex items-center gap-1">
                  <span className="text-text-muted text-[11px] mr-1">Filter Direction:</span>
                  {[
                    { id: 'ALL', label: 'All Transfers' },
                    { id: 'IN', label: 'Inbound Only' },
                    { id: 'OUT', label: 'Outbound Only' }
                  ].map(f => (
                    <button
                      key={f.id}
                      onClick={() => setLedgerFilter(f.id)}
                      className={`px-2 py-0.5 rounded text-[11px] transition-colors cursor-pointer ${
                        ledgerFilter === f.id
                          ? 'bg-accent text-white font-bold'
                          : 'bg-surface text-text-muted border border-border hover:text-text'
                      }`}
                    >
                      {f.label}
                    </button>
                  ))}
                </div>

                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleExportLedgerCSV}
                  icon={Download}
                >
                  Export Customer Ledger (CSV)
                </Button>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs border-collapse">
                  <thead>
                    <tr className="bg-surfaceRaised border-b border-border text-[11px] font-mono text-text-muted uppercase">
                      <th className="py-2.5 px-3">Date & Time</th>
                      <th className="py-2.5 px-3">Dir</th>
                      <th className="py-2.5 px-3">Transaction ID</th>
                      <th className="py-2.5 px-3">Counterparty & Account</th>
                      <th className="py-2.5 px-3 text-right">Amount (USD / BDT)</th>
                      <th className="py-2.5 px-3">Rail</th>
                      <th className="py-2.5 px-3">Status</th>
                      <th className="py-2.5 px-3">Memo / Narrative</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-borderSubtle font-mono text-[11px]">
                    {filteredLedger.map((tx) => (
                      <tr key={tx.id} className="hover:bg-surfaceHover transition-colors">
                        <td className="py-2.5 px-3 whitespace-nowrap text-text-muted">
                          {tx.date}
                        </td>

                        <td className="py-2.5 px-3 whitespace-nowrap">
                          {tx.type === 'IN' ? (
                            <span className="inline-flex items-center gap-0.5 text-cleared font-bold text-[10px]">
                              <ArrowDownLeft className="w-3 h-3" />
                              IN
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-0.5 text-amber-500 font-bold text-[10px]">
                              <ArrowUpRight className="w-3 h-3" />
                              OUT
                            </span>
                          )}
                        </td>

                        <td className="py-2.5 px-3 whitespace-nowrap font-bold text-accent">
                          {tx.id}
                        </td>

                        <td className="py-2.5 px-3 max-w-[200px]">
                          <span className="font-semibold text-text truncate block">{tx.counterparty}</span>
                          <span className="text-[10px] text-text-muted truncate block">{tx.counterpartyAccount}</span>
                        </td>

                        <td className="py-2.5 px-3 text-right whitespace-nowrap">
                          <span className="font-bold text-text tabular-nums block">
                            ${Number(tx.amount).toLocaleString(undefined, { minimumFractionDigits: 2 })}
                          </span>
                          <span className="text-[10px] text-text-muted block">
                            ৳{Number(tx.amountBdt || tx.amount * 120).toLocaleString(undefined, { maximumFractionDigits: 0 })}
                          </span>
                        </td>

                        <td className="py-2.5 px-3 whitespace-nowrap">
                          <Badge variant="neutral" size="sm">
                            {tx.rail}
                          </Badge>
                        </td>

                        <td className="py-2.5 px-3 whitespace-nowrap">
                          {tx.status === 'BLOCKED' ? (
                            <Badge variant="critical" size="sm">BLOCKED</Badge>
                          ) : tx.status === 'FLAGGED' ? (
                            <Badge variant="review" size="sm">FLAGGED</Badge>
                          ) : (
                            <Badge variant="cleared" size="sm">COMPLETED</Badge>
                          )}
                        </td>

                        <td className="py-2.5 px-3 max-w-[220px]">
                          <span className="text-[11px] text-text-2 truncate block" title={tx.memo}>
                            {tx.memo || 'Commercial settlement'}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Card>
          )}

          {/* TAB 2: KYC & DUE DILIGENCE */}
          {activeProfileTab === 'kyc' && (
            <div className="space-y-3">
              <Card className="space-y-3">
                <CardHeader
                  title="Entity Legal Structure & Identification"
                  subtitle="Registrar of Joint Stock Companies & Corporate Registry Validation"
                />

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs font-mono">
                  <div className="p-2.5 rounded bg-bg border border-borderSubtle">
                    <span className="text-[10px] text-text-muted uppercase block">Legal Entity Type</span>
                    <span className="font-semibold text-text">{selectedEntity.legalType}</span>
                  </div>

                  <div className="p-2.5 rounded bg-bg border border-borderSubtle">
                    <span className="text-[10px] text-text-muted uppercase block">Registration / Trade License</span>
                    <span className="font-semibold text-text">{selectedEntity.incorporation}</span>
                  </div>

                  <div className="p-2.5 rounded bg-bg border border-borderSubtle">
                    <span className="text-[10px] text-text-muted uppercase block">Registered Corporate Address</span>
                    <span className="font-semibold text-text">{selectedEntity.address || selectedEntity.jurisdiction}</span>
                  </div>

                  <div className="p-2.5 rounded bg-bg border border-borderSubtle">
                    <span className="text-[10px] text-text-muted uppercase block">Official Contact Desk</span>
                    <span className="font-semibold text-text">{selectedEntity.phone} • {selectedEntity.email}</span>
                  </div>
                </div>
              </Card>

              <Card className="space-y-3">
                <CardHeader
                  title="Beneficial Ownership (UBO) & Sanctions Screening"
                  subtitle="Automated OFAC, UN Security Council, and BFIU Watchlist Match Results"
                />

                <div className="p-3 rounded bg-bg border border-borderSubtle font-mono text-xs space-y-2">
                  <div>
                    <span className="text-[10px] text-text-muted uppercase block">Ultimate Beneficial Owners (UBO)</span>
                    <span className="font-bold text-text text-sm">{selectedEntity.ubo}</span>
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2 pt-2 border-t border-borderSubtle">
                    <div>
                      <span className="text-[9px] text-text-muted uppercase block">OFAC SDN List</span>
                      <span className="font-semibold text-cleared text-[11px]">{selectedEntity.pepSanctions?.ofacSdn}</span>
                    </div>

                    <div>
                      <span className="text-[9px] text-text-muted uppercase block">UN Sanctions</span>
                      <span className="font-semibold text-cleared text-[11px]">{selectedEntity.pepSanctions?.unSanctions}</span>
                    </div>

                    <div>
                      <span className="text-[9px] text-text-muted uppercase block">BFIU Watchlist</span>
                      <span className={`font-semibold text-[11px] ${
                        selectedEntity.pepSanctions?.bfiuWatchlist?.includes('CLEAN') || selectedEntity.pepSanctions?.bfiuWatchlist?.includes('NEGATIVE')
                          ? 'text-cleared'
                          : 'text-critical'
                      }`}>
                        {selectedEntity.pepSanctions?.bfiuWatchlist}
                      </span>
                    </div>

                    <div>
                      <span className="text-[9px] text-text-muted uppercase block">PEP Classification</span>
                      <span className="font-semibold text-text text-[11px]">{selectedEntity.pepSanctions?.pepDirect}</span>
                    </div>
                  </div>
                </div>
              </Card>
            </div>
          )}

          {/* TAB 3: ACTIVITY & AUDIT TRAIL */}
          {activeProfileTab === 'activity' && (
            <Card padding={false} className="overflow-hidden">
              <div className="p-3 border-b border-border bg-surfaceRaised flex items-center justify-between text-xs font-mono">
                <span className="font-bold text-text uppercase tracking-wider">
                  Customer Compliance Event Ledger
                </span>
                <span className="text-text-muted">Immutable Merkle-Chained Events</span>
              </div>

              <div className="divide-y divide-borderSubtle">
                {(selectedEntity.activityLogs || []).map((log) => (
                  <div key={log.id} className="p-3.5 hover:bg-surfaceHover transition-colors flex items-start gap-3 text-xs">
                    <div className="w-7 h-7 rounded-lg bg-surfaceRaised border border-border flex items-center justify-center shrink-0 font-bold text-text font-mono text-[10px]">
                      {log.id.slice(-3)}
                    </div>

                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between gap-2">
                        <span className="font-bold text-text font-mono text-xs">{log.action.replace(/_/g, ' ')}</span>
                        <span className="text-[10px] text-text-muted font-mono">{log.timestamp}</span>
                      </div>
                      <p className="text-xs text-text-2 mt-1 leading-relaxed">
                        {log.details}
                      </p>
                      <span className="text-[10px] text-text-muted font-mono mt-1 block">
                        Logged by: <strong className="text-text">{log.officer}</strong>
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* TAB 4: TURNOVER & FLOW RATIOS */}
          {activeProfileTab === 'flow' && (
            <Card className="space-y-4">
              <CardHeader
                title="Monetary Turnover & Pass-Through Behavior"
                subtitle="Assessment of account velocity, flow retention, and dwell time"
              />

              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono">
                <div className="p-3 rounded bg-bg border border-borderSubtle">
                  <span className="text-[10px] text-text-muted uppercase block">30-Day Inbound Turnover</span>
                  <span className="font-bold text-cleared text-sm block mt-1">{selectedEntity.flowConservation?.inboundTurnover}</span>
                </div>

                <div className="p-3 rounded bg-bg border border-borderSubtle">
                  <span className="text-[10px] text-text-muted uppercase block">30-Day Outbound Turnover</span>
                  <span className="font-bold text-amber-500 text-sm block mt-1">{selectedEntity.flowConservation?.outboundTurnover}</span>
                </div>

                <div className="p-3 rounded bg-bg border border-borderSubtle">
                  <span className="text-[10px] text-text-muted uppercase block">Pass-Through Retention Ratio</span>
                  <span className="font-bold text-text text-sm block mt-1">{selectedEntity.flowConservation?.massBalanceRatio}</span>
                </div>

                <div className="p-3 rounded bg-bg border border-borderSubtle">
                  <span className="text-[10px] text-text-muted uppercase block">Average Dwell Time</span>
                  <span className="font-bold text-critical text-sm block mt-1">{selectedEntity.flowConservation?.dwellTimeHours} Hours</span>
                </div>
              </div>

              <div className="p-3.5 rounded bg-surfaceRaised border border-border text-xs space-y-1.5">
                <span className="font-bold text-text block">Remediation & Compliance Guidance:</span>
                <p className="text-text-2 text-xs leading-relaxed">
                  {selectedEntity.counterfactualRemedy}
                </p>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
