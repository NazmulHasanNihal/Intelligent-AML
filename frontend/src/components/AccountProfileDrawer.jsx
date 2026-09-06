import React from 'react';
import { 
  X, 
  Building2, 
  User, 
  ShieldCheck, 
  AlertTriangle, 
  Clock, 
  CreditCard, 
  DollarSign, 
  ArrowUpRight, 
  ArrowDownLeft, 
  Globe, 
  ExternalLink, 
  FileText, 
  Lock, 
  Share2,
  Mail,
  Phone,
  MapPin,
  Calendar,
  CheckCircle2
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const AccountProfileDrawer = ({ account, isOpen, onClose, onOpenGraph, onOpenNotice, onOpenActionModal }) => {
  const { hasPermission } = useAuth();
  if (!isOpen || !account) return null;

  const isCorp = account.holderType === 'CORPORATE' || account.src?.includes('CORP') || account.holderName?.includes('Ltd') || account.holderName?.includes('LLC') || account.holderName?.includes('DMCC');

  // Default enriched data for realistic banking display
  const profile = {
    accountNumber: account.accountNumber || account.src || 'US-JPMC-4829-1092-8823',
    holderName: account.holderName || (isCorp ? 'Apex Global Logistics Ltd' : 'Sarah L. Jenkins'),
    holderType: isCorp ? 'Corporate Business Account' : 'Verified Retail Checking',
    institution: account.institution || 'JPMorgan Chase Bank, N.A.',
    accountAge: account.accountAge || '4 Years, 7 Months',
    openDate: account.openDate || '2021-11-14',
    taxId: account.taxId || 'EIN-XX-9481923',
    kycTier: account.kycTier || 'Tier-3 Enhanced Due Diligence (EDD Verified)',
    address: account.address || (isCorp ? '1200 Brickell Ave, Suite 1800, Miami, FL 33131' : '742 Evergreen Terrace, Seattle, WA 98101'),
    phone: account.phone || '+1 (305) 892-4410',
    email: account.email || (isCorp ? 'compliance@apexlogistics.com' : 's.jenkins@outlook.com'),
    balance: account.balance || '$1,248,920.45 USD',
    riskScore: account.risk || 0.94,
    decisionTier: account.gammaLabel || 'Tier 1: High-Risk Quarantine',
    pepStatus: account.pepStatus || 'Negative (Clean Sanctions Screen)',
    monthlyInflow: account.monthlyInflow || '$482,000.00 USD',
    monthlyOutflow: account.monthlyOutflow || '$479,500.00 USD',
    recentLedger: account.recentLedger || [
      { id: 'TX-88491', date: '2026-09-02 08:42', type: 'OUT', to: 'GB-BARC-1109-MULE-HUB', amount: '$9,450.00', rail: 'SWIFT Wire', status: 'FLAGGED' },
      { id: 'TX-88488', date: '2026-09-02 08:14', type: 'IN', from: 'US-WF-4412-FEEDER-LLC', amount: '$9,800.00', rail: 'Fedwire', status: 'COMPLETED' },
      { id: 'TX-88482', date: '2026-09-01 16:30', type: 'IN', from: 'AE-SCBL-9921-PANAMA', amount: '$48,500.00', rail: 'SWIFT Wire', status: 'FLAGGED' },
      { id: 'TX-88470', date: '2026-08-30 11:20', type: 'OUT', to: 'MERCHANT-CHOP-RETAIL', amount: '$45.20', rail: 'Visa POS', status: 'CLEARED' },
      { id: 'TX-88461', date: '2026-08-28 09:15', type: 'IN', from: 'PAYROLL-DIRECT-DEP', amount: '$12,400.00', rail: 'ACH Direct', status: 'CLEARED' },
    ]
  };

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-black/60 backdrop-blur-sm animate-fadeIn">
      <div className="absolute inset-y-0 right-0 max-w-full flex">
        <div className="w-full sm:w-[500px] max-w-full bg-[var(--bg-card)] border-l border-[var(--border-card)] shadow-2xl flex flex-col justify-between overflow-y-auto">
          
          {/* Header */}
          <div>
            <div className="p-3.5 sm:p-4 bg-[var(--bg-card-elevated)] border-b border-[var(--border-subtle)] flex items-start justify-between">
              <div className="flex items-center gap-2.5 min-w-0">
                <div className={`w-9 h-9 sm:w-10 sm:h-10 rounded-xl flex items-center justify-center text-white font-bold shrink-0 shadow-[var(--skeuo-btn)] ${
                  profile.riskScore >= 0.70 ? 'bg-rose-950/80 border border-rose-500/60 text-rose-300' :
                  profile.riskScore >= 0.30 ? 'bg-amber-950/80 border border-amber-500/60 text-amber-300' :
                  'bg-gradient-to-b from-[#257843] to-[#144726] border border-[#113C21] text-white'
                }`}>
                  {isCorp ? <Building2 className="w-5 h-5" /> : <User className="w-5 h-5" />}
                </div>
                <div className="min-w-0">
                  <div className="flex items-center gap-1.5 flex-wrap">
                    <h2 className="text-xs sm:text-sm font-bold text-[var(--text-primary)] font-sans truncate">{profile.holderName}</h2>
                    <span className="text-[9px] px-1.5 py-0.5 rounded-full font-mono font-bold bg-[var(--accent-primary)]/15 text-[var(--accent-primary)] border border-[var(--accent-primary)]/30 shadow-inner">
                      {isCorp ? 'CORP' : 'RETAIL'}
                    </span>
                  </div>
                  <p className="text-[10px] sm:text-[11px] font-mono text-[var(--accent-primary)] truncate mt-0.5">{profile.accountNumber}</p>
                  <p className="text-[10px] text-[var(--text-muted)] font-sans truncate">{profile.institution}</p>
                </div>
              </div>

              <button
                onClick={onClose}
                className="p-1.5 rounded-lg skeuo-btn text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-all cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Quick Status Bar in Recessed Wells */}
            <div className="grid grid-cols-3 gap-2 p-2.5 sm:p-3 bg-[var(--bg-base)] border-b border-[var(--border-subtle)] text-xs font-mono">
              <div className="p-2 rounded-xl skeuo-well text-center">
                <span className="text-[9px] text-[var(--text-muted)] block uppercase">RISK</span>
                <span className={`text-xs sm:text-sm font-extrabold ${profile.riskScore >= 0.70 ? 'text-rose-500' : profile.riskScore >= 0.30 ? 'text-amber-500' : 'text-[var(--accent-primary)]'}`}>
                  {(profile.riskScore * 100).toFixed(1)}%
                </span>
              </div>
              <div className="p-2 rounded-xl skeuo-well text-center">
                <span className="text-[9px] text-[var(--text-muted)] block uppercase">BALANCE</span>
                <span className="text-xs sm:text-sm font-bold text-[var(--text-primary)] truncate block">{profile.balance.split(' ')[0]}</span>
              </div>
              <div className="p-2 rounded-xl skeuo-well text-center">
                <span className="text-[9px] text-[var(--text-muted)] block uppercase">KYC</span>
                <span className="text-[10px] sm:text-[11px] font-semibold text-[var(--accent-primary)] truncate block">L3 Verified</span>
              </div>
            </div>

            {/* Account Details & Compliance Profile */}
            <div className="p-3 sm:p-4 space-y-3 sm:space-y-3.5">
              {/* Profile Meta Cards */}
              <div className="space-y-2">
                <h3 className="text-[11px] font-bold text-[var(--text-primary)] uppercase tracking-wider font-mono flex items-center gap-1.5">
                  <ShieldCheck className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                  <span>Verification Profile &amp; PEP Sanctions Screening</span>
                </h3>

                <div className="grid grid-cols-2 gap-2 text-[11px]">
                  <div className="p-2 rounded-lg skeuo-well space-y-0.5">
                    <span className="text-[9px] text-[var(--text-muted)] block font-mono">TAX ID / EIN:</span>
                    <span className="text-[var(--text-primary)] font-mono font-medium truncate block">{profile.taxId}</span>
                  </div>
                  <div className="p-2 rounded-lg skeuo-well space-y-0.5">
                    <span className="text-[9px] text-[var(--text-muted)] block font-mono">TENURE:</span>
                    <span className="text-[var(--text-primary)] font-medium truncate block">{profile.accountAge}</span>
                  </div>
                  <div className="p-2 rounded-lg skeuo-well space-y-0.5 col-span-2">
                    <span className="text-[9px] text-[var(--text-muted)] block font-mono">REGISTERED LEGAL ADDRESS:</span>
                    <span className="text-[var(--text-secondary)] font-sans text-[10px] leading-tight block truncate">{profile.address}</span>
                  </div>
                </div>

                {/* PEP & Sanctions Screening Verification Box */}
                <div className="p-2.5 rounded-xl bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)] space-y-1 text-[11px] shadow-sm">
                  <div className="flex items-center justify-between">
                    <span className="text-[9px] font-mono text-[var(--text-muted)] uppercase">WATCHLISTS: OFAC SDN, EU, UN, UK HMT</span>
                    <span className="text-[9px] font-mono font-bold px-1.5 py-0.2 rounded bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30">
                      CLEARED (0 DIRECT MATCHES)
                    </span>
                  </div>
                  <p className="text-[10px] text-[var(--text-secondary)]">
                    Identity cross-checked against 24 international regulatory sanction and Politically Exposed Persons (PEP) watchlists. No direct asset freezes currently active.
                  </p>
                </div>
              </div>

              {/* 12-D Flow Invariants Card (C-STGB Deep Topology) */}
              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <h3 className="text-[11px] font-bold text-[var(--text-primary)] uppercase tracking-wider font-mono flex items-center gap-1.5">
                    <Globe className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                    <span>12-D Flow Invariants (Physics-Informed)</span>
                  </h3>
                  <span className="text-[9px] font-mono text-[var(--accent-primary)] font-semibold">C-STGB Calibrated</span>
                </div>

                <div className="p-2.5 rounded-xl skeuo-well space-y-2 font-mono text-[10px]">
                  <div className="grid grid-cols-2 gap-2">
                    <div className="p-1.5 rounded-lg bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)]">
                      <span className="text-[8px] text-[var(--text-muted)] block">MASS CONSERVATION Φ_flow</span>
                      <span className="text-xs font-bold text-rose-600 dark:text-rose-400">0.998 (In ≈ Out)</span>
                      <span className="text-[8px] text-[var(--text-muted)] block">Kirchhoff Structuring</span>
                    </div>
                    <div className="p-1.5 rounded-lg bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)]">
                      <span className="text-[8px] text-[var(--text-muted)] block">HAWKES ARRIVAL RATE</span>
                      <span className="text-xs font-bold text-amber-600 dark:text-amber-400">18.4 tx / min</span>
                      <span className="text-[8px] text-[var(--text-muted)] block">High Burst Clustering</span>
                    </div>
                  </div>

                  <div className="grid grid-cols-3 gap-1.5 text-center text-[9px]">
                    <div className="p-1 rounded bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)]">
                      <span className="text-[8px] text-[var(--text-muted)] block">CYCLE-3 MOTIF</span>
                      <span className="font-bold text-[var(--text-primary)]">4.2 / hr</span>
                    </div>
                    <div className="p-1 rounded bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)]">
                      <span className="text-[8px] text-[var(--text-muted)] block">CYCLE-4 MOTIF</span>
                      <span className="font-bold text-[var(--text-primary)]">1.8 / hr</span>
                    </div>
                    <div className="p-1 rounded bg-[var(--bg-card-elevated)] border border-[var(--border-subtle)]">
                      <span className="text-[8px] text-[var(--text-muted)] block">FUSION WEIGHT α_u</span>
                      <span className="font-bold text-[var(--accent-primary)]">0.88 GNN</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Monthly Flow Volumes */}
              <div className="space-y-1.5">
                <h3 className="text-[11px] font-bold text-[var(--text-primary)] uppercase tracking-wider font-mono flex items-center gap-1.5">
                  <DollarSign className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                  <span>Monthly Activity</span>
                </h3>
                <div className="grid grid-cols-2 gap-2 font-mono text-xs">
                  <div className="p-2 rounded-lg skeuo-well flex items-center justify-between">
                    <div>
                      <span className="text-[9px] text-[var(--text-muted)] block">Inflow (30d)</span>
                      <span className="text-xs sm:text-sm font-bold text-[var(--accent-primary)] truncate block">{profile.monthlyInflow}</span>
                    </div>
                    <ArrowDownLeft className="w-4 h-4 text-[var(--accent-primary)] shrink-0" />
                  </div>
                  <div className="p-2 rounded-lg skeuo-well flex items-center justify-between">
                    <div>
                      <span className="text-[9px] text-[var(--text-muted)] block">Outflow (30d)</span>
                      <span className="text-xs sm:text-sm font-bold text-rose-500 truncate block">{profile.monthlyOutflow}</span>
                    </div>
                    <ArrowUpRight className="w-4 h-4 text-rose-500 shrink-0" />
                  </div>
                </div>
              </div>

              {/* Transaction History */}
              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <h3 className="text-[11px] font-bold text-[var(--text-primary)] uppercase tracking-wider font-mono flex items-center gap-1.5">
                    <Clock className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                    <span>Transaction History</span>
                  </h3>
                  <span className="text-[9px] text-[var(--text-muted)] font-mono">Recent 5 records</span>
                </div>

                <div className="rounded-xl overflow-hidden skeuo-well max-h-[180px] overflow-y-auto">
                  <table className="w-full text-left text-[11px] font-sans">
                    <thead className="bg-[var(--bg-card-elevated)] text-[var(--text-muted)] font-mono text-[9px] border-b border-[var(--border-subtle)] sticky top-0">
                      <tr>
                        <th className="py-1.5 px-2">Date / ID</th>
                        <th className="py-1.5 px-2">Counterparty</th>
                        <th className="py-1.5 px-2 text-right">Amount</th>
                        <th className="py-1.5 px-2 text-right">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[var(--border-subtle)] font-mono text-[10px]">
                      {profile.recentLedger.map((tx, idx) => (
                        <tr key={idx} className="hover:bg-black/[0.02] dark:hover:bg-white/[0.03] transition-colors">
                          <td className="py-1.5 px-2">
                            <span className="font-bold text-[var(--text-primary)] block truncate">{tx.id}</span>
                            <span className="text-[8px] text-[var(--text-muted)]">{tx.date.split(' ')[1]}</span>
                          </td>
                          <td className="py-1.5 px-2 text-[var(--accent-primary)] text-[10px] truncate max-w-[120px]">
                            {tx.type === 'IN' ? `From: ${tx.from}` : `To: ${tx.to}`}
                          </td>
                          <td className="py-1.5 px-2 text-right font-bold text-[var(--text-primary)]">{tx.amount}</td>
                          <td className="py-1.5 px-2 text-right">
                            <span className={`text-[8px] px-1.5 py-0.5 rounded-full font-bold shadow-inner ${
                              tx.status === 'FLAGGED' ? 'bg-rose-500/20 text-rose-600 dark:text-rose-400 border border-rose-500/30' :
                              'bg-emerald-500/20 text-[var(--accent-primary)] border border-emerald-500/30'
                            }`}>
                              {tx.status}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>

          {/* Bottom Action Footer */}
          <div className="p-2.5 sm:p-3 bg-[var(--bg-card-elevated)] border-t border-[var(--border-subtle)] grid grid-cols-3 gap-2 font-mono text-xs">
            <button
              onClick={() => {
                onClose();
                if (onOpenGraph) onOpenGraph(profile);
              }}
              className="py-1.5 px-2 rounded-lg skeuo-btn skeuo-btn-secondary text-[10px] sm:text-[11px] font-semibold"
            >
              <Share2 className="w-3 h-3 text-[var(--accent-primary)]" />
              <span>3D Graph</span>
            </button>

            <button
              onClick={() => {
                if (onOpenNotice) onOpenNotice(profile);
              }}
              className="py-1.5 px-2 rounded-lg skeuo-btn skeuo-btn-secondary text-[10px] sm:text-[11px] font-semibold"
            >
              <Mail className="w-3 h-3 text-amber-500" />
              <span>Notice</span>
            </button>

            <button
              onClick={() => {
                if (onOpenActionModal) onOpenActionModal({ type: 'FREEZE_ACCOUNT', target: profile });
              }}
              className="py-1.5 px-2 rounded-lg skeuo-btn skeuo-btn-danger text-[10px] sm:text-[11px] font-bold"
            >
              <Lock className="w-3 h-3" />
              <span>Freeze</span>
            </button>
          </div>

        </div>
      </div>
    </div>
  );
};
