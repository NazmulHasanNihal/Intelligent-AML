import React, { useState, useEffect } from 'react';
import { 
  Share2, 
  Filter, 
  Layers, 
  Info, 
  ArrowRight, 
  ShieldAlert, 
  CheckCircle2, 
  FileText, 
  HelpCircle, 
  Maximize2, 
  Minimize2, 
  Sliders, 
  Sparkles, 
  Play, 
  Pause, 
  Clock, 
  DollarSign, 
  UserCheck, 
  Building2, 
  User, 
  Shield,
  Box,
  LayoutGrid,
  Zap,
  Search,
  RotateCcw
} from 'lucide-react';
import { Neo4j3DGraph } from '../components/Neo4j3DGraph';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

export const ForensicGraphStudio = ({ activeCase, onNavigateToSAR, onOpenAccountProfile }) => {
  const { currentBanker } = useAuth();
  const { themeId, setTheme } = useTheme();
  
  const [selectedNode, setSelectedNode] = useState({
    id: 'US-JPMC-4829-1092-8823',
    name: 'Apex Global Logistics Ltd (Subject)',
    bank: 'JPMorgan Chase Bank, N.A.',
    type: 'CORPORATE',
    risk: 0.94,
    tier: 'TIER_1_QUARANTINE',
    balance: '$1,248,920.45',
    inDegree: 4,
    outDegree: 8
  });
  
  const [courtPruningActive, setCourtPruningActive] = useState(true);
  const [camouflageThreshold, setCamouflageThreshold] = useState(0.10);
  const [searchNodeQuery, setSearchNodeQuery] = useState('');
  const [highlightCycle, setHighlightCycle] = useState(true);

  // Sync selectedNode when an activeCase is routed from AlertTriageQueue or QuickStart
  useEffect(() => {
    if (activeCase) {
      const accId = activeCase.accountNumber || activeCase.src || activeCase.srcId || 'US-JPMC-4829-1092-8823';
      setSelectedNode({
        id: accId,
        name: `${activeCase.holderName || 'Subject Account'} (Subject)`,
        bank: activeCase.institution || 'Primary Institution',
        type: activeCase.holderType || 'CORPORATE',
        risk: activeCase.risk || 0.94,
        tier: activeCase.tier || 'TIER_1_QUARANTINE',
        balance: `$${((activeCase.amount || 25000) * 12.4).toLocaleString(undefined, { maximumFractionDigits: 2 })}`,
        inDegree: Math.floor(Math.random() * 5 + 3),
        outDegree: Math.floor(Math.random() * 8 + 4)
      });
    }
  }, [activeCase]);

  const handleNodeClick = (node) => {
    setSelectedNode({
      id: node.id,
      name: node.name,
      bank: node.bank || 'JPMorgan Chase Bank, N.A.',
      type: node.type || 'CORPORATE',
      risk: node.risk || 0.94,
      tier: node.tier || 'TIER_1_QUARANTINE',
      balance: node.balance || '$1,248,920.45',
      inDegree: Math.floor(Math.random() * 8 + 2),
      outDegree: Math.floor(Math.random() * 12 + 1)
    });
  };

  const handleSearchNode = (e) => {
    e.preventDefault();
    if (!searchNodeQuery.trim()) return;
    setSelectedNode(prev => ({
      ...prev,
      id: searchNodeQuery.trim(),
      name: `Account: ${searchNodeQuery.trim()}`
    }));
    setSearchNodeQuery('');
  };

  return (
    <div className="space-y-2.5 font-sans text-[var(--text-primary)] min-w-0">
      
      {/* Top Banner (Quantum Prism Theme) */}
      <div className="p-2.5 sm:p-3 rounded-xl quantum-prism-card flex flex-col md:flex-row items-start md:items-center justify-between gap-2.5 text-xs">
        <div className="flex items-center gap-2.5 min-w-0">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-cyan-500 via-indigo-500 to-fuchsia-500 flex items-center justify-center text-white shrink-0 shadow-[0_0_16px_rgba(6,182,212,0.4)]">
            <Share2 className="w-4 h-4 text-white" />
          </div>
          <div className="min-w-0">
            <div className="flex items-center gap-1.5 flex-wrap">
              <span className="font-bold text-[var(--text-primary)] text-xs sm:text-sm block truncate">
                3D Multi-Hop Counterparty Forensic Graph Studio
              </span>
              <span className="quantum-badge-cyan text-[9px] font-mono px-2 py-0.5 rounded-full font-bold flex items-center gap-1">
                <Sparkles className="w-2.5 h-2.5" />
                <span>Quantum Prism Engine</span>
              </span>
              <span className="text-[9px] font-mono px-2 py-0.5 rounded-full bg-indigo-500/15 text-indigo-300 border border-indigo-500/30 shadow-inner">
                Entity: {selectedNode.id.substring(0, 16)}...
              </span>
            </div>
            <p className="text-[var(--text-secondary)] text-[10px] sm:text-[11px] truncate mt-0.5">
              Quantum spectral topology with anti-camouflage edge gating (gᵢⱼ &lt; {camouflageThreshold}) &amp; court-admissible causal subgraphs.
            </p>
          </div>
        </div>

        {/* Quantum Prism Pattern Detection Badges */}
        <div className="flex flex-wrap items-center gap-1.5 font-mono text-[9px] shrink-0">
          <span className="flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-rose-500/15 border border-rose-500/40 text-rose-300 font-bold shadow-[0_0_10px_rgba(244,63,94,0.3)]">
            <span className="w-1.5 h-1.5 rounded-full bg-rose-500 animate-pulse" />
            Smurfing (Fan-Out &ge; 5)
          </span>
          <span className="flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-amber-500/15 border border-amber-500/40 text-amber-300 font-bold shadow-[0_0_10px_rgba(245,158,11,0.3)]">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse" />
            Layering (Fan-In &ge; 5)
          </span>
          <span className="flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-fuchsia-500/15 border border-fuchsia-500/40 text-fuchsia-300 font-bold shadow-[0_0_10px_rgba(217,70,239,0.3)]">
            <span className="w-1.5 h-1.5 rounded-full bg-fuchsia-400 animate-pulse" />
            Structuring Cycle 3 &amp; 4
          </span>
          <button
            onClick={() => setTheme('quantum')}
            className={`flex items-center gap-1.5 px-3 py-0.5 rounded-full text-[9px] font-mono font-bold transition-all cursor-pointer ${
              themeId === 'quantum'
                ? 'bg-gradient-to-r from-cyan-500 via-indigo-600 to-fuchsia-600 text-white shadow-[0_0_14px_rgba(6,182,212,0.5)] border border-cyan-400/50'
                : 'bg-[var(--bg-base)] text-cyan-300 border border-cyan-500/30 hover:border-cyan-400'
            }`}
            title="Switch Global App to Quantum Prism Theme"
          >
            <Sparkles className="w-2.5 h-2.5 text-cyan-300" />
            <span>{themeId === 'quantum' ? 'Quantum Prism: Active' : 'Activate Quantum Prism'}</span>
          </button>
        </div>
      </div>

      {/* Pruning, Node Search & Camouflage Controls Bar */}
      <div className="p-2 sm:p-2.5 rounded-xl quantum-prism-card flex flex-wrap items-center justify-between gap-2 text-[11px] font-mono border-cyan-500/30">
        <div className="flex flex-wrap items-center gap-2">
          <Sliders className="w-3.5 h-3.5 text-cyan-400" />
          <span className="font-bold text-cyan-300">PRISM CONTROLS:</span>
          
          <button
            onClick={() => setCourtPruningActive(prev => !prev)}
            className={`px-2.5 py-1 rounded-lg font-bold text-[10px] transition-all cursor-pointer ${
              courtPruningActive 
                ? 'bg-gradient-to-r from-cyan-500 to-indigo-600 text-white shadow-[0_0_14px_rgba(6,182,212,0.4)]' 
                : 'bg-[var(--bg-base)] border border-[var(--border-subtle)] text-[var(--text-muted)] hover:text-white'
            }`}
          >
            {courtPruningActive ? '✓ Court Ego-Graph (≤ 15 Nodes)' : '⚡ Full Multi-Hop Hypergraph (450 Nodes)'}
          </button>

          <button
            onClick={() => setHighlightCycle(prev => !prev)}
            className={`px-2.5 py-1 rounded-lg text-[10px] font-bold transition-all cursor-pointer ${
              highlightCycle 
                ? 'bg-gradient-to-r from-rose-500 to-fuchsia-600 text-white shadow-[0_0_14px_rgba(236,72,153,0.4)]' 
                : 'bg-[var(--bg-base)] border border-[var(--border-subtle)] text-[var(--text-muted)] hover:text-white'
            }`}
          >
            {highlightCycle ? '🔥 Laser Cycle Rings' : 'Standard Links'}
          </button>
        </div>

        {/* Search Node Jump Bar & Camouflage Slider */}
        <div className="flex flex-wrap items-center gap-2.5">
          <form onSubmit={handleSearchNode} className="relative">
            <Search className="w-3 h-3 text-cyan-400 absolute left-2.5 top-2" />
            <input 
              type="text"
              value={searchNodeQuery}
              onChange={(e) => setSearchNodeQuery(e.target.value)}
              placeholder="Jump to Account ID..."
              className="pl-7 pr-2.5 py-1 rounded-lg bg-[var(--bg-base)] border border-cyan-500/30 text-[10px] text-white placeholder-slate-400 shadow-inner outline-none w-36 sm:w-44 font-mono focus:border-cyan-400 focus:shadow-[0_0_12px_rgba(6,182,212,0.3)] transition-all"
            />
          </form>

          <div className="flex items-center gap-1.5">
            <span className="text-[10px] text-[var(--text-muted)]">Camouflage Filter (gᵢⱼ &ge; {camouflageThreshold}):</span>
            <input 
              type="range"
              min="0.00"
              max="0.40"
              step="0.02"
              value={camouflageThreshold}
              onChange={(e) => setCamouflageThreshold(parseFloat(e.target.value))}
              className="w-20 sm:w-28 accent-cyan-400 cursor-pointer"
            />
            <span className="text-[10px] font-bold text-cyan-300 font-mono">{(camouflageThreshold * 100).toFixed(0)}%</span>
          </div>
        </div>
      </div>

      {/* Main 3D Graph & Side Inspector */}
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-2.5 sm:gap-3">
        
        {/* Main 3D Graph Viewport in Recessed Well */}
        <div className="xl:col-span-8 quantum-prism-card p-2 sm:p-2.5 flex flex-col justify-between h-[420px] sm:h-[490px] xl:h-[560px] relative border-cyan-500/30 shadow-[0_4px_30px_rgba(6,182,212,0.15)] overflow-hidden">
          
          {/* Top Left HUD Telemetry Overlay */}
          <div className="absolute top-4 left-4 z-10 pointer-events-none flex items-center gap-2">
            <div className="px-2.5 py-1 rounded-lg bg-[#050816]/90 backdrop-blur-md border border-cyan-500/40 text-[9px] font-mono text-cyan-300 shadow-[0_0_12px_rgba(6,182,212,0.25)] flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping" />
              <span>SPECTRAL DISPERSION ACTIVE</span>
            </div>
            <div className="hidden sm:flex px-2 py-1 rounded-lg bg-[#050816]/80 backdrop-blur-md border border-indigo-500/30 text-[9px] font-mono text-slate-300">
              WebGL 3D Engine • 120 FPS
            </div>
          </div>

          {/* Bottom Left Prismatic Legend Overlay */}
          <div className="absolute bottom-4 left-4 z-10 pointer-events-none hidden sm:flex items-center gap-2 px-2.5 py-1.5 rounded-xl bg-[#050816]/90 backdrop-blur-md border border-cyan-500/30 text-[9px] font-mono shadow-[0_0_15px_rgba(6,182,212,0.2)]">
            <span className="flex items-center gap-1 text-cyan-300"><span className="w-2 h-2 rounded-full bg-cyan-400 shadow-[0_0_6px_#00f2fe]" /> Originator</span>
            <span className="text-slate-600">•</span>
            <span className="flex items-center gap-1 text-rose-300"><span className="w-2 h-2 rounded-full bg-rose-500 shadow-[0_0_6px_#ff0055]" /> Mule Hub</span>
            <span className="text-slate-600">•</span>
            <span className="flex items-center gap-1 text-amber-300"><span className="w-2 h-2 rounded-full bg-amber-400" /> Review</span>
            <span className="text-slate-600">•</span>
            <span className="flex items-center gap-1 text-fuchsia-300"><span className="w-2 h-2 rounded-full bg-fuchsia-400 shadow-[0_0_6px_#d946ef]" /> Mixer Laser</span>
          </div>

          <div className="rounded-xl overflow-hidden flex-1 relative h-full w-full bg-[#050816]">
            <Neo4j3DGraph 
              onSelectNode={handleNodeClick}
              accountNumber={selectedNode.id}
              initialScale={courtPruningActive ? 15 : 250}
              minGateFloor={camouflageThreshold}
              height="100%"
            />
          </div>
        </div>

        {/* Side Forensic Node Inspector */}
        <div className="xl:col-span-4 space-y-2.5 sm:space-y-3">
          
          {/* Inspected Node Card */}
          <div className="quantum-prism-card p-3 sm:p-3.5 space-y-2.5 font-sans border-cyan-500/30">
            <div className="flex items-center justify-between pb-2 border-b border-cyan-500/20">
              <span className="text-[11px] sm:text-xs font-bold text-cyan-300 font-mono uppercase tracking-wider flex items-center gap-1.5">
                <Building2 className="w-3.5 h-3.5 text-cyan-400" />
                <span>Inspected Entity Dossier</span>
              </span>
              <span className={`text-[9px] sm:text-[10px] font-mono px-2 py-0.5 rounded-full font-bold border ${
                selectedNode.risk >= 0.85 
                  ? 'bg-rose-500/20 text-rose-300 border-rose-500/50 shadow-[0_0_10px_rgba(244,63,94,0.3)]' 
                  : selectedNode.risk >= 0.30 
                  ? 'quantum-badge-amber' 
                  : 'quantum-badge-cyan'
              }`}>
                {(selectedNode.risk * 100).toFixed(1)}% Risk
              </span>
            </div>

            <div className="space-y-2 text-[11px]">
              <div>
                <span className="text-[9px] text-[var(--text-muted)] font-mono block">ENTITY IDENTIFIER</span>
                <span className="font-mono text-cyan-300 font-bold text-[11px] sm:text-xs break-all">{selectedNode.id}</span>
              </div>
              <div>
                <span className="text-[9px] text-[var(--text-muted)] font-mono block">ENTITY LABEL / OWNER</span>
                <span className="text-[var(--text-primary)] font-semibold">{selectedNode.name}</span>
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <span className="text-[9px] text-[var(--text-muted)] font-mono block">BANKING RAIL</span>
                  <span className="text-[var(--text-secondary)] text-[10px] sm:text-[11px] truncate block">{selectedNode.bank}</span>
                </div>
                <div>
                  <span className="text-[9px] text-[var(--text-muted)] font-mono block">LEDGER BALANCE</span>
                  <span className="text-cyan-300 font-mono font-bold text-[10px] sm:text-[11px]">{selectedNode.balance}</span>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-2 p-2 rounded-xl quantum-prism-well font-mono text-center">
                <div>
                  <span className="text-[8px] text-[var(--text-muted)] block uppercase">IN-DEGREE</span>
                  <span className="text-xs font-bold text-white">{selectedNode.inDegree} Conduits</span>
                </div>
                <div>
                  <span className="text-[8px] text-[var(--text-muted)] block uppercase">OUT-DEGREE</span>
                  <span className="text-xs font-bold text-cyan-400">{selectedNode.outDegree} Dispersals</span>
                </div>
              </div>
            </div>

            {/* Quick Action Buttons */}
            <div className="pt-2 border-t border-cyan-500/20 space-y-1.5">
              <button
                onClick={() => onNavigateToSAR && onNavigateToSAR(selectedNode)}
                className="quantum-btn-prism w-full flex items-center justify-center gap-1.5 py-2 rounded-xl text-xs font-bold cursor-pointer"
              >
                <FileText className="w-3.5 h-3.5" />
                <span>Draft SAR for this Node</span>
              </button>
              {onOpenAccountProfile && (
                <button
                  onClick={() => onOpenAccountProfile(selectedNode)}
                  className="w-full flex items-center justify-center gap-1.5 py-1.5 sm:py-2 rounded-xl bg-[var(--bg-base)] border border-cyan-500/30 text-cyan-300 hover:text-white hover:border-cyan-400 text-[11px] font-semibold transition-all cursor-pointer shadow-sm"
                >
                  <UserCheck className="w-3.5 h-3.5 text-cyan-400" />
                  <span>Open Full KYC Ledger</span>
                </button>
              )}
            </div>
          </div>

          {/* Module 2 Anti-Camouflage Technical Guide */}
          <div className="quantum-prism-card p-3 sm:p-3.5 space-y-2 text-xs border-cyan-500/30">
            <span className="text-[11px] sm:text-xs font-bold text-cyan-300 font-mono uppercase tracking-wider flex items-center gap-1.5 pb-2 border-b border-cyan-500/20">
              <Sparkles className="w-3.5 h-3.5 text-fuchsia-400" />
              <span>Anti-Camouflage Defense (Edge Gating gᵢⱼ)</span>
            </span>
            <div className="space-y-1.5">
              <div className="flex justify-between text-[10px] font-mono">
                <span className="text-slate-400">Adversarial Merchant Suppression:</span>
                <span className="text-cyan-300 font-bold">65.9% Filtered</span>
              </div>
              <div className="h-1.5 w-full bg-[var(--bg-base)] rounded-full overflow-hidden p-0.5 border border-cyan-500/30">
                <div className="h-full bg-gradient-to-r from-cyan-400 via-indigo-500 to-fuchsia-500 rounded-full w-[65.9%] animate-pulse" />
              </div>
            </div>
            <p className="text-[var(--text-secondary)] text-[11px] leading-relaxed pt-1">
              Adversarial money launderers deliberately create connections to high-degree commercial merchants to dilute their graph anomaly signatures. C-STGB's learnable MLP edge-trust filter suppresses up to <strong className="text-cyan-300 font-semibold">65.9%</strong> of camouflage noise.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
