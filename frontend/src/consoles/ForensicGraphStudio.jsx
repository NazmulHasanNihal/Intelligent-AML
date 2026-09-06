import React, { useState } from 'react';
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
  Zap
} from 'lucide-react';
import { Neo4j3DGraph } from '../components/Neo4j3DGraph';
import { useAuth } from '../context/AuthContext';

export const ForensicGraphStudio = ({ onNavigateToSAR, onOpenAccountProfile }) => {
  const { currentBanker } = useAuth();
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
  const [activePatternFilter, setActivePatternFilter] = useState('ALL'); // 'ALL', 'SMURFING', 'LAYERING', 'CIRCULAR'

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

  return (
    <div className="space-y-3 font-sans text-[var(--text-primary)]">
      {/* Top Banner (Skeuomorphic) */}
      <div className="p-2.5 sm:p-3 rounded-xl skeuo-card flex flex-col md:flex-row items-start md:items-center justify-between gap-2.5 text-xs">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 sm:w-9 sm:h-9 rounded-xl bg-gradient-to-b from-[#257843] to-[#144726] border border-[#113C21] flex items-center justify-center text-white shrink-0 shadow-[var(--skeuo-btn)]">
            <Share2 className="w-4 h-4 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-[var(--text-primary)] text-xs sm:text-sm block">3D Multi-Hop Counterparty Forensic Graph Studio</span>
              <span className="text-[9px] font-mono px-1.5 py-0.5 rounded font-bold bg-[var(--accent-primary)]/15 text-[var(--accent-primary)] border border-[var(--accent-primary)]/30 shadow-inner">
                WebGL 3D Engine
              </span>
            </div>
            <p className="text-[var(--text-secondary)] text-[10px] sm:text-[11px] mt-0.5">
              Interactive 3D topological visualization with learnable anti-camouflage pruning (gᵢⱼ &lt; 0.10) and court-admissible causal subgraph extraction.
            </p>
          </div>
        </div>

        {/* Topology Pattern Detection Badges */}
        <div className="flex flex-wrap items-center gap-1.5 font-mono text-[9px]">
          <span className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-rose-500/15 border border-rose-500/30 text-rose-600 dark:text-rose-400 font-bold shadow-inner">
            <span className="w-1.5 h-1.5 rounded-full bg-rose-500 animate-pulse" />
            Smurfing (Fan-Out n_out ≥ 5)
          </span>
          <span className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-amber-500/15 border border-amber-500/30 text-amber-700 dark:text-amber-300 font-bold shadow-inner">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse" />
            Layering (Fan-In n_in ≥ 5)
          </span>
          <span className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-indigo-500/15 border border-indigo-500/30 text-indigo-600 dark:text-indigo-400 font-bold shadow-inner">
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-500 animate-pulse" />
            Structuring Rings (Cycle 3 &amp; 4)
          </span>
        </div>
      </div>

      {/* Pruning & Camouflage Controls Bar */}
      <div className="p-2 sm:p-2.5 rounded-xl skeuo-card flex flex-wrap items-center justify-between gap-2 text-[11px] font-mono">
        <div className="flex items-center gap-2">
          <Sliders className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
          <span className="font-bold text-[var(--text-primary)]">TOPOLOGICAL CONTROLS:</span>
          <button
            onClick={() => setCourtPruningActive(prev => !prev)}
            className={`px-2.5 py-1 rounded-lg font-bold text-[10px] transition-all cursor-pointer ${
              courtPruningActive ? 'bg-gradient-to-b from-[#257843] to-[#174E2B] text-white shadow-[var(--skeuo-btn)]' : 'skeuo-btn text-[var(--text-muted)]'
            }`}
          >
            {courtPruningActive ? '✓ Court Pruning Active (≤ 15 Nodes)' : 'Full Multi-Hop Network (450 Nodes)'}
          </button>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-[10px] text-[var(--text-muted)]">Camouflage Filter (gᵢⱼ &ge; {camouflageThreshold}):</span>
          <input 
            type="range"
            min="0.00"
            max="0.40"
            step="0.02"
            value={camouflageThreshold}
            onChange={(e) => setCamouflageThreshold(parseFloat(e.target.value))}
            className="w-24 sm:w-32 accent-[var(--accent-primary)] cursor-pointer"
          />
          <span className="text-[10px] font-bold text-[var(--accent-primary)]">{(camouflageThreshold * 100).toFixed(0)}%</span>
        </div>
      </div>

      {/* Main 3D Graph & Side Inspector */}
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-2.5 sm:gap-3">
        
        {/* Main 3D Graph Viewport in Recessed Well */}
        <div className="xl:col-span-8 skeuo-card p-2 sm:p-2.5 flex flex-col justify-between h-[360px] sm:h-[440px] xl:h-[500px]">
          <div className="rounded-xl overflow-hidden skeuo-well flex-1 relative h-full w-full">
            <Neo4j3DGraph 
              onSelectNode={handleNodeClick}
              accountNumber="US-JPMC-4829-1092-8823"
              initialScale={courtPruningActive ? 15 : 250}
              minGateFloor={camouflageThreshold}
              height="100%"
            />
          </div>
        </div>

        {/* Side Forensic Node Inspector */}
        <div className="xl:col-span-4 space-y-2.5 sm:space-y-3">
          
          {/* Inspected Node Card */}
          <div className="skeuo-card p-3 sm:p-3.5 space-y-2.5 font-sans">
            <div className="flex items-center justify-between pb-2 border-b border-[var(--border-subtle)]">
              <span className="text-[11px] sm:text-xs font-bold text-[var(--text-primary)] font-mono uppercase tracking-wider flex items-center gap-1.5">
                <Building2 className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                <span>Inspected Entity Dossier</span>
              </span>
              <span className={`text-[9px] sm:text-[10px] font-mono px-2 py-0.5 rounded-full font-bold border ${
                selectedNode.risk >= 0.85 ? 'badge-tier1' : selectedNode.risk >= 0.30 ? 'badge-tier2' : 'badge-tier3'
              }`}>
                {(selectedNode.risk * 100).toFixed(1)}% Risk
              </span>
            </div>

            <div className="space-y-2 text-[11px]">
              <div>
                <span className="text-[9px] text-[var(--text-muted)] font-mono block">ENTITY IDENTIFIER</span>
                <span className="font-mono text-[var(--accent-primary)] font-bold text-[11px] sm:text-xs break-all">{selectedNode.id}</span>
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
                  <span className="text-[var(--accent-primary)] font-mono font-bold text-[10px] sm:text-[11px]">{selectedNode.balance}</span>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-2 p-2 rounded-xl skeuo-well font-mono text-center">
                <div>
                  <span className="text-[8px] text-[var(--text-muted)] block uppercase">IN-DEGREE</span>
                  <span className="text-xs font-bold text-[var(--text-primary)]">{selectedNode.inDegree} Conduits</span>
                </div>
                <div>
                  <span className="text-[8px] text-[var(--text-muted)] block uppercase">OUT-DEGREE</span>
                  <span className="text-xs font-bold text-[var(--accent-primary)]">{selectedNode.outDegree} Dispersals</span>
                </div>
              </div>
            </div>

            {/* Quick Action Buttons */}
            <div className="pt-2 border-t border-[var(--border-subtle)] space-y-1.5">
              <button
                onClick={() => onNavigateToSAR && onNavigateToSAR()}
                className="w-full flex items-center justify-center gap-1.5 py-1.5 sm:py-2 rounded-xl skeuo-btn skeuo-btn-primary text-[11px] font-semibold"
              >
                <FileText className="w-3.5 h-3.5" />
                <span>Draft SAR for this Node</span>
              </button>
              {onOpenAccountProfile && (
                <button
                  onClick={() => onOpenAccountProfile(selectedNode)}
                  className="w-full flex items-center justify-center gap-1.5 py-1.5 rounded-xl skeuo-btn skeuo-btn-secondary text-[11px] font-semibold"
                >
                  <UserCheck className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
                  <span>Open Full KYC Ledger</span>
                </button>
              )}
            </div>
          </div>

          {/* Module 2 Anti-Camouflage Technical Guide */}
          <div className="skeuo-card p-3 sm:p-3.5 space-y-2 text-xs">
            <span className="text-[11px] sm:text-xs font-bold text-[var(--text-primary)] font-mono uppercase tracking-wider flex items-center gap-1.5 pb-2 border-b border-[var(--border-subtle)]">
              <Sparkles className="w-3.5 h-3.5 text-amber-600 dark:text-amber-300" />
              <span>Anti-Camouflage Defense (Edge Gating gᵢⱼ)</span>
            </span>
            <p className="text-[var(--text-secondary)] text-[11px] leading-relaxed">
              Adversarial money launderers deliberately create connections to high-degree commercial merchants to dilute their graph anomaly signatures. C-STGB's learnable MLP edge-trust filter suppresses up to <strong className="text-[var(--accent-primary)] font-semibold">65.9%</strong> of camouflage noise.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
