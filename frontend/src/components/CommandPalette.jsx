import React, { useState, useEffect, useRef } from 'react';
import { 
  Search, 
  Command, 
  Zap, 
  Inbox, 
  Share2, 
  FileText, 
  UserCheck, 
  BarChart3, 
  Sparkles, 
  ShieldAlert, 
  ArrowRight, 
  X,
  Palette,
  Shield,
  Activity,
  Download,
  Play
} from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { useAuth } from '../context/AuthContext';

export const CommandPalette = ({ isOpen, onClose, onNavigate, onOpenSAR, onOpenRecourse, onSimulateAttack }) => {
  const { currentTheme, setTheme, availableThemes } = useTheme();
  const { currentBanker, setIsAuthModalOpen } = useAuth();
  const [debouncedQuery, setDebouncedQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef(null);

  // Debounce search query
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedQuery(query);
      setSelectedIndex(0);
    }, 120);
    return () => clearTimeout(handler);
  }, [query]);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
      setQuery('');
      setDebouncedQuery('');
      setSelectedIndex(0);
    }
  }, [isOpen]);

  // Comprehensive entity & transaction index for real-time compliance querying
  const commands = [
    // Navigation Across All 6 Consoles
    { id: 'nav-command', category: 'Consoles', title: '1. Unified Surveillance Command Center', desc: 'Real-time transaction stream, dual C-STGB scoring & live gauges', icon: Zap, action: () => onNavigate('command-center'), keys: ['1'] },
    { id: 'nav-alerts', category: 'Consoles', title: '2. Conformal Risk Clearing & Triage Hub', desc: 'Class-conditional CRC 3-tier queue (α = 0.001)', icon: Inbox, action: () => onNavigate('alerts'), keys: ['2'] },
    { id: 'nav-graph', category: 'Consoles', title: '3. 3D Forensic Graph Studio', desc: 'WebGL topological network visualizer with camouflage pruning', icon: Share2, action: () => onNavigate('investigate'), keys: ['3'] },
    { id: 'nav-cases', category: 'Consoles', title: '4. Autonomous Multi-Agent SAR Drafter', desc: '4-agent LLM swarm, FinCEN 111, goAML XML & PDF dossiers', icon: FileText, action: () => onNavigate('cases'), keys: ['4'] },
    { id: 'nav-recourse', category: 'Consoles', title: '5. Customer Recourse & Remediation Hub', desc: 'Causal GNN counterfactual optimizer & CFPB adverse notice', icon: UserCheck, action: () => onNavigate('recourse'), keys: ['5'] },
    { id: 'nav-gov', category: 'Consoles', title: '6. Model Risk & SR 11-7 Governance Vault', desc: '13-model benchmark scorecard, ACI drift & SHA-256 Merkle proofs', icon: BarChart3, action: () => onNavigate('governance'), keys: ['6'] },

    // Forensic Accounts & Legal Entities
    { id: 'acc-apex', category: 'Customer Accounts', title: 'Apex Global Logistics Ltd', desc: 'Account: US-JPMC-4829-1092-8823 | BIC: CHASUS33 | Tier 1 Quarantine (Smurfing Ring)', icon: ShieldAlert, action: () => onNavigate('command-center'), bic: 'CHASUS33', accountId: 'US-JPMC-4829-1092-8823' },
    { id: 'acc-elena', category: 'Customer Accounts', title: 'Elena Rostova (Conduit Hub)', desc: 'Account: GB-BARC-1109-MULE-HUB | BIC: BARCGB22 | Pass-through intermediary', icon: ShieldAlert, action: () => onNavigate('alerts'), bic: 'BARCGB22', accountId: 'GB-BARC-1109-MULE-HUB' },
    { id: 'acc-darknet', category: 'Customer Accounts', title: 'Quantum Digital Assets Fund', desc: 'Account: 0x3a9f-4829-DARK-0012 | BIC: BINACEYZ | Wasabi CoinJoin Peeling Chain', icon: ShieldAlert, action: () => onNavigate('investigate'), bic: 'BINACEYZ', accountId: '0x3a9f-4829-DARK-0012' },
    { id: 'acc-horizon', category: 'Customer Accounts', title: 'Horizon Trading DMCC', desc: 'Account: US-CITI-4412-PANAMA-FEEDER | BIC: CITIUS33 | Offshore Wash Loop', icon: ShieldAlert, action: () => onNavigate('cases'), bic: 'CITIUS33', accountId: 'US-CITI-4412-PANAMA-FEEDER' },
    { id: 'acc-marcus', category: 'Customer Accounts', title: 'Marcus Vance', desc: 'Account: US-CITI-0019-DORMANT-MULE | BIC: CITIUS33 | Tier 2 Rapid Activation Hold', icon: ShieldAlert, action: () => onNavigate('alerts'), bic: 'CITIUS33', accountId: 'US-CITI-0019-DORMANT-MULE' },
    { id: 'acc-clean', category: 'Customer Accounts', title: 'BlueWave Distribution Corp', desc: 'Account: US-WF-0091-8841-CLEAN | BIC: WFBUS6S | Tier 3 Straight-Through Clear', icon: Activity, action: () => onNavigate('alerts'), bic: 'WFBUS6S', accountId: 'US-WF-0091-8841-CLEAN' },
    { id: 'acc-rhein', category: 'Customer Accounts', title: 'Rheinland Freight GmbH', desc: 'Account: DE-DB-9901-RHEINLAND-LLC | BIC: DEUTDEFF | SEPA Instant High-Velocity', icon: Activity, action: () => onNavigate('alerts'), bic: 'DEUTDEFF', accountId: 'DE-DB-9901-RHEINLAND-LLC' },

    // Transaction Hashes
    { id: 'tx-994821', category: 'Transaction Hashes', title: 'TX-994821 ($9,450.00 SWIFT)', desc: 'US-JPMC-4829 -> GB-BARC-1109 | BIC: CHASUS33 -> BARCGB22 | Smurfing Flag', icon: FileText, action: () => onNavigate('alerts'), txHash: 'TX-994821' },
    { id: 'tx-994819', category: 'Transaction Hashes', title: 'TX-994819 ($95,000.00 Bitcoin UTXO)', desc: '0x3a9f-4829 -> 0x7b12-MIXER-POOL | CoinJoin Multi-Hop Cluster', icon: FileText, action: () => onNavigate('investigate'), txHash: 'TX-994819' },
    { id: 'tx-994818', category: 'Transaction Hashes', title: 'TX-994818 ($4,800.00 ACH Direct)', desc: 'US-CITI-0019 -> SG-DBS-8819 | BIC: CITIUS33 -> DBSSSGSG | Dormant Flare', icon: FileText, action: () => onNavigate('alerts'), txHash: 'TX-994818' },
    { id: 'tx-994817', category: 'Transaction Hashes', title: 'TX-994817 ($14,250.00 Fedwire Funds)', desc: 'US-WF-0091 -> US-JPMC-2201 | Amazon AWS Settlement | Clean Clearance', icon: CheckCircle2, action: () => onNavigate('alerts'), txHash: 'TX-994817' },
    { id: 'tx-994816', category: 'Transaction Hashes', title: 'TX-994816 ($6,200.00 SEPA Instant)', desc: 'DE-DB-9901 -> FR-BNP-3312 | BIC: DEUTDEFF -> BNPAFRPA | Velocity Review', icon: FileText, action: () => onNavigate('alerts'), txHash: 'TX-994816' },
    { id: 'tx-994815', category: 'Transaction Hashes', title: 'TX-994815 ($47,600.00 SWIFT Wire)', desc: 'HK-HSBC-8812 -> US-JPMC-4829 | BIC: HSBCHKHH -> CHASUS33 | Wash Return Loop', icon: ShieldAlert, action: () => onNavigate('command-center'), txHash: 'TX-994815' },

    // Theme Switchers
    { id: 'theme-money', category: 'Themes & Aesthetics', title: 'Switch to Federal Money Green & White (Default)', desc: 'Tactile intaglio currency skeuomorphism with specular highlights', icon: Palette, action: () => setTheme('money-green-skeuo') },
    { id: 'theme-vault', category: 'Themes & Aesthetics', title: 'Switch to Vault Midnight & Steel Theme', desc: 'Dark executive bank vault with brushed steel & phosphor mint', icon: Palette, action: () => setTheme('vault-midnight-skeuo') },
    { id: 'theme-botanical', category: 'Themes & Aesthetics', title: 'Switch to Botanical Emerald Clay Theme', desc: 'Deep forest #2A7C13, leaf #76C457 on custard #FFF8CF', icon: Palette, action: () => setTheme('botanical-clay') },
    { id: 'theme-quantum', category: 'Themes & Aesthetics', title: 'Switch to Quantum Cyber Clay Theme', desc: 'Deep carbon & electric cyan glow', icon: Palette, action: () => setTheme('quantum') },
    { id: 'theme-gold', category: 'Themes & Aesthetics', title: 'Switch to Swiss Private Gold Clay Theme', desc: 'Midnight navy & refined champagne gold', icon: Palette, action: () => setTheme('swiss-gold') },

    // Quick Compliance Actions
    { id: 'act-role', category: 'Officer Actions', title: 'Switch Banker Persona / Branch Profile', desc: `Current: ${currentBanker.name} (${currentBanker.roleTitle})`, icon: Shield, action: () => setIsAuthModalOpen(true) },
    { id: 'act-sar-fincen', category: 'Officer Actions', title: 'Generate FinCEN Form 111 XML Dossier', desc: 'Autonomous multi-agent evidence synthesis', icon: FileText, action: () => onNavigate('cases') },
  ];

  const searchTarget = debouncedQuery.toLowerCase().trim();
  const filteredCommands = commands.filter(c => {
    if (!searchTarget) return true;
    return (
      c.title.toLowerCase().includes(searchTarget) || 
      c.desc.toLowerCase().includes(searchTarget) ||
      c.category.toLowerCase().includes(searchTarget) ||
      (c.bic && c.bic.toLowerCase().includes(searchTarget)) ||
      (c.accountId && c.accountId.toLowerCase().includes(searchTarget)) ||
      (c.txHash && c.txHash.toLowerCase().includes(searchTarget))
    );
  });

  const handleKeyDown = (e) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex(prev => (prev + 1) % Math.max(1, filteredCommands.length));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex(prev => (prev - 1 + filteredCommands.length) % Math.max(1, filteredCommands.length));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (filteredCommands[selectedIndex]) {
        filteredCommands[selectedIndex].action();
        onClose();
      }
    } else if (e.key === 'Escape') {
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-10 sm:pt-16 px-2.5 sm:px-4 bg-black/60 backdrop-blur-sm animate-fadeIn">
      <div 
        className="w-full max-w-xl bg-[var(--bg-card)] border border-[var(--border-card)] rounded-2xl shadow-2xl overflow-hidden text-[var(--text-primary)] font-sans skeuo-card"
      >
        {/* Search Bar Input */}
        <div className="flex items-center px-3.5 py-2.5 sm:py-3 border-b border-[var(--border-subtle)] bg-[var(--bg-card-elevated)]">
          <Search className="w-4 h-4 text-[var(--accent-primary)] mr-2.5 shrink-0" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => { setQuery(e.target.value); setSelectedIndex(0); }}
            onKeyDown={handleKeyDown}
            placeholder="Type a command, search accounts (e.g. 'Apex', '0x3a9f')..."
            className="w-full bg-transparent text-xs sm:text-sm text-[var(--text-primary)] placeholder-[var(--text-muted)] focus:outline-none"
          />
          <div className="flex items-center gap-1.5 ml-2">
            <span className="text-[9px] font-mono px-1.5 py-0.5 rounded-md bg-[var(--bg-base)] text-[var(--text-secondary)] border border-[var(--border-subtle)] shadow-inner">ESC</span>
          </div>
        </div>

        {/* Command List */}
        <div className="max-h-80 sm:max-h-96 overflow-y-auto p-1.5 space-y-1">
          {filteredCommands.length === 0 ? (
            <div className="py-6 text-center text-[var(--text-muted)] text-xs">
              No matching commands or entities found for <span className="text-[var(--accent-primary)] font-mono">"{query}"</span>
            </div>
          ) : (
            filteredCommands.map((cmd, idx) => {
              const Icon = cmd.icon;
              const isSelected = idx === selectedIndex;
              return (
                <button
                  key={cmd.id}
                  onClick={() => { cmd.action(); onClose(); }}
                  onMouseEnter={() => setSelectedIndex(idx)}
                  className={`w-full flex items-center justify-between p-2 sm:p-2.5 rounded-xl text-left transition-all cursor-pointer ${
                    isSelected 
                      ? 'bg-gradient-to-b from-[#257843] to-[#144726] text-white border border-[#113C21] shadow-[var(--skeuo-btn)]' 
                      : 'hover:bg-black/[0.03] dark:hover:bg-white/[0.04] text-[var(--text-secondary)] border border-transparent'
                  }`}
                >
                  <div className="flex items-center gap-2.5 min-w-0">
                    <div className={`w-7 h-7 sm:w-8 sm:h-8 rounded-lg flex items-center justify-center shrink-0 ${
                      isSelected ? 'bg-white/20 text-white' : 'bg-[var(--bg-base)] text-[var(--text-muted)] border border-[var(--border-subtle)]'
                    }`}>
                      <Icon className="w-3.5 h-3.5" />
                    </div>
                    <div className="min-w-0">
                      <div className="text-xs font-semibold flex items-center gap-1.5">
                        <span className={isSelected ? 'text-white' : 'text-[var(--text-primary)]'}>{cmd.title}</span>
                        <span className={`text-[8px] font-mono px-1.5 py-0.2 rounded uppercase ${
                          isSelected ? 'bg-white/20 text-white' : 'bg-[var(--bg-base)] text-[var(--text-muted)]'
                        }`}>
                          {cmd.category}
                        </span>
                      </div>
                      <p className={`text-[10px] sm:text-[11px] truncate ${isSelected ? 'text-emerald-100' : 'text-[var(--text-muted)]'}`}>{cmd.desc}</p>
                    </div>
                  </div>
                  {isSelected && <ArrowRight className="w-3.5 h-3.5 text-white shrink-0 ml-2" />}
                </button>
              );
            })
          )}
        </div>

        {/* Footer Navigation Hints */}
        <div className="px-3.5 py-1.5 sm:py-2 bg-[var(--bg-base)] border-t border-[var(--border-subtle)] flex items-center justify-between text-[10px] sm:text-[11px] text-[var(--text-secondary)] font-mono">
          <div className="flex items-center gap-2.5">
            <span><strong className="text-[var(--text-primary)]">↑ ↓</strong> Navigate</span>
            <span><strong className="text-[var(--text-primary)]">↵</strong> Select</span>
            <span><strong className="text-[var(--text-primary)]">ESC</strong> Close</span>
          </div>
          <div className="text-[var(--accent-primary)] flex items-center gap-1 font-sans text-[10px]">
            <Sparkles className="w-3 h-3" />
            <span>Active: <strong>{currentTheme.name}</strong></span>
          </div>
        </div>
      </div>
    </div>
  );
};
