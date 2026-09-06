import React, { useEffect, useRef, useState, useMemo } from 'react';
import ForceGraph3D from '3d-force-graph';
import * as THREE from 'three';
import { 
  Play, 
  Pause, 
  RotateCcw, 
  ZoomIn, 
  ZoomOut, 
  Layers, 
  Sparkles, 
  Filter, 
  Eye, 
  Search, 
  Maximize2, 
  Minimize2,
  Sliders,
  Compass,
  Activity,
  UserCheck,
  Zap,
  ShieldAlert
} from 'lucide-react';

// Generates synthetic high-scale real-world banking graph (up to thousands of transactions)
export function generateLargeBankingGraph(baseOriginator = 'US-JPMC-4829-1092-8823', nodeCount = 450) {
  const banks = ['JPMorgan Chase', 'Citibank', 'Standard Chartered', 'Barclays', 'Wells Fargo', 'HSBC', 'Deutsche Bank'];
  const nodeTypes = ['CORPORATE', 'RETAIL', 'OFFSHORE_SHELL', 'ATM_CASHOUT', 'CRYPTO_MIXER', 'MERCHANT_CHAFF'];
  
  const nodes = [];
  const links = [];

  // Seed Central Node (Account Holder)
  nodes.push({
    id: baseOriginator,
    name: 'Apex Global Logistics Ltd (Subject)',
    bank: 'JPMorgan Chase Bank, N.A.',
    type: 'CORPORATE',
    risk: 0.94,
    tier: 'TIER_1_QUARANTINE',
    val: 28,
    color: '#F43F5E',
    glowColor: '#FF2E63',
    balance: '$1,248,920.45',
    isOriginator: true
  });

  // Layer 1: Core Mules & Laundering Conduits (8 nodes)
  const coreMules = [
    { id: 'GB-BARC-1109-MULE-HUB', name: 'Elena Rostova (Conduit Hub)', bank: 'Barclays Bank PLC', risk: 0.96, tier: 'TIER_1_QUARANTINE', type: 'RETAIL' },
    { id: 'AE-SCBL-5512-HORIZON', name: 'Horizon Trading DMCC', bank: 'Standard Chartered Dubai', risk: 0.95, tier: 'TIER_1_QUARANTINE', type: 'CORPORATE' },
    { id: 'BVI-ESCROW-SOVEREIGN', name: 'BVI Sovereign Vault LP', bank: 'BVI Offshore Clearing', risk: 0.98, tier: 'TIER_1_QUARANTINE', type: 'OFFSHORE_SHELL' },
    { id: 'US-WF-4412-FEEDER-LLC', name: 'Pacific Coast Feeder LLC', bank: 'Wells Fargo N.A.', risk: 0.88, tier: 'TIER_1_QUARANTINE', type: 'CORPORATE' },
    { id: '0x3a9f-DARKNET-UTXO', name: 'Quantum Digital Mixer Gateway', bank: 'Tornado Anonymity Pool', risk: 0.99, tier: 'TIER_1_QUARANTINE', type: 'CRYPTO_MIXER' },
    { id: 'US-CITI-0019-DORMANT', name: 'Marcus Vance (Dormant Mule)', bank: 'Citibank N.A.', risk: 0.65, tier: 'TIER_2_REVIEW_QUEUE', type: 'RETAIL' },
    { id: 'SG-DBS-8819-TRANSIT', name: 'Marina Bay Trade Transit', bank: 'DBS Bank Singapore', risk: 0.58, tier: 'TIER_2_REVIEW_QUEUE', type: 'CORPORATE' },
    { id: 'DE-DB-9901-RHEINLAND', name: 'Rheinland Freight GmbH', bank: 'Deutsche Bank Frankfurt', risk: 0.42, tier: 'TIER_2_REVIEW_QUEUE', type: 'CORPORATE' },
  ];

  coreMules.forEach((m) => {
    const isHighRisk = m.risk >= 0.85;
    const isMed = m.risk >= 0.40;
    const color = isHighRisk ? '#F43F5E' : isMed ? '#F59E0B' : '#10B981';
    const glow = isHighRisk ? '#FF2E63' : isMed ? '#FFAA00' : '#00FFA3';

    nodes.push({
      id: m.id,
      name: m.name,
      bank: m.bank,
      type: m.type,
      risk: m.risk,
      tier: m.tier,
      val: 18,
      color,
      glowColor: glow,
      balance: `$${(Math.random() * 450000 + 20000).toLocaleString('en-US', { maximumFractionDigits: 2 })}`
    });

    // Connect to central
    links.push({
      source: baseOriginator,
      target: m.id,
      amount: Math.floor(Math.random() * 45000 + 4000),
      gate: isHighRisk ? 0.98 : 0.72,
      color: isHighRisk ? 'rgba(244, 63, 94, 0.85)' : 'rgba(245, 158, 11, 0.7)',
      particleSpeed: isHighRisk ? 0.008 : 0.004,
      particles: isHighRisk ? 4 : 2,
      isLaunderingLoop: isHighRisk
    });
  });

  // Closed Circular Wash Loop
  links.push({ source: 'GB-BARC-1109-MULE-HUB', target: 'AE-SCBL-5512-HORIZON', amount: 48100, gate: 0.98, color: '#F43F5E', particleSpeed: 0.01, particles: 5, isLaunderingLoop: true });
  links.push({ source: 'AE-SCBL-5512-HORIZON', target: 'BVI-ESCROW-SOVEREIGN', amount: 47900, gate: 0.99, color: '#F43F5E', particleSpeed: 0.01, particles: 5, isLaunderingLoop: true });
  links.push({ source: 'BVI-ESCROW-SOVEREIGN', target: baseOriginator, amount: 47600, gate: 0.99, color: '#F43F5E', particleSpeed: 0.012, particles: 6, isLaunderingLoop: true });

  // Generate extended background counterparties
  for (let i = 0; i < nodeCount; i++) {
    const roll = Math.random();
    const isClean = roll > 0.15;
    const isReview = !isClean && roll > 0.04;
    const isRisk = !isClean && !isReview;

    const riskScore = isRisk ? (0.85 + Math.random() * 0.14) : isReview ? (0.35 + Math.random() * 0.40) : (0.01 + Math.random() * 0.15);
    const color = isRisk ? '#F43F5E' : isReview ? '#F59E0B' : '#10B981';
    const glowColor = isRisk ? '#FF2E63' : isReview ? '#FFAA00' : '#00FFA3';
    const tier = isRisk ? 'TIER_1_QUARANTINE' : isReview ? 'TIER_2_REVIEW_QUEUE' : 'TIER_3_STRAIGHT_THROUGH_CLEAR';
    const type = isClean ? (Math.random() > 0.6 ? 'MERCHANT_CHAFF' : 'RETAIL') : (Math.random() > 0.5 ? 'CORPORATE' : 'OFFSHORE_SHELL');
    const bank = banks[Math.floor(Math.random() * banks.length)];

    const id = `ACC-${bank.substring(0, 3).toUpperCase()}-${Math.floor(1000 + Math.random() * 9000)}-${i}`;
    nodes.push({
      id,
      name: `${type.replace('_', ' ')} Node #${i + 1}`,
      bank,
      type,
      risk: Number(riskScore.toFixed(3)),
      tier,
      val: isRisk ? 14 : isReview ? 10 : 7,
      color,
      glowColor,
      balance: `$${Math.floor(Math.random() * 80000 + 500).toLocaleString()}`
    });

    // Random parent link with camouflage gate estimation
    const parentNode = nodes[Math.floor(Math.random() * Math.min(nodes.length - 1, 25))];
    const isCamouflage = type === 'MERCHANT_CHAFF';
    const gateWeight = isCamouflage ? 0.04 : isRisk ? 0.95 : 0.70;

    links.push({
      source: parentNode.id,
      target: id,
      amount: Math.floor(Math.random() * 15000 + 100),
      gate: gateWeight,
      color: isCamouflage ? 'rgba(100, 116, 139, 0.25)' : isRisk ? 'rgba(244, 63, 94, 0.75)' : 'rgba(16, 185, 129, 0.4)',
      particleSpeed: isRisk ? 0.006 : 0.002,
      particles: isRisk ? 3 : 1,
      isLaunderingLoop: isRisk
    });
  }

  return { nodes, links };
}

export const Neo4j3DGraph = ({ 
  onSelectNode, 
  accountNumber = 'US-JPMC-4829-1092-8823',
  initialScale = 450,
  minGateFloor = 0.00,
  height = '100%',
  showDenoiseSlider = true,
  resetTrigger = 0
}) => {
  const containerRef = useRef(null);
  const graphInstanceRef = useRef(null);
  const [isRotating, setIsRotating] = useState(true);
  const [scale, setScale] = useState(initialScale);
  const [activeFilter, setActiveFilter] = useState('ALL'); // 'ALL', 'WASH_CYCLE', 'TIER_1_ONLY'
  const [camouflageGateFloor, setCamouflageGateFloor] = useState(minGateFloor);
  const [highlightedPath, setHighlightedPath] = useState(true);

  // Sync camouflageGateFloor when prop changes
  useEffect(() => {
    setCamouflageGateFloor(minGateFloor);
  }, [minGateFloor]);

  // Generate Graph Data
  const rawGraphData = useMemo(() => {
    return generateLargeBankingGraph(accountNumber, scale);
  }, [accountNumber, scale]);

  // Apply filters including Learnable Edge Trust Camouflage Gating (Module 2)
  const filteredData = useMemo(() => {
    let filteredNodes = rawGraphData.nodes;
    let filteredLinks = rawGraphData.links;

    // Filter by camouflage gate floor (Module 2 Denoising)
    if (camouflageGateFloor > 0.00) {
      filteredLinks = filteredLinks.filter(l => l.gate >= camouflageGateFloor);
      const connectedNodeIds = new Set();
      filteredLinks.forEach(l => {
        connectedNodeIds.add(typeof l.source === 'object' ? l.source.id : l.source);
        connectedNodeIds.add(typeof l.target === 'object' ? l.target.id : l.target);
      });
      filteredNodes = filteredNodes.filter(n => n.isOriginator || connectedNodeIds.has(n.id));
    }

    // Filter by laundering typologies
    if (activeFilter === 'WASH_CYCLE') {
      filteredLinks = filteredLinks.filter(l => l.isLaunderingLoop);
      const loopNodeIds = new Set();
      filteredLinks.forEach(l => {
        loopNodeIds.add(typeof l.source === 'object' ? l.source.id : l.source);
        loopNodeIds.add(typeof l.target === 'object' ? l.target.id : l.target);
      });
      filteredNodes = filteredNodes.filter(n => loopNodeIds.has(n.id) || n.isOriginator);
    } else if (activeFilter === 'TIER_1_ONLY') {
      filteredNodes = filteredNodes.filter(n => n.tier === 'TIER_1_QUARANTINE' || n.isOriginator);
      const t1Ids = new Set(filteredNodes.map(n => n.id));
      filteredLinks = filteredLinks.filter(l => {
        const s = typeof l.source === 'object' ? l.source.id : l.source;
        const t = typeof l.target === 'object' ? l.target.id : l.target;
        return t1Ids.has(s) && t1Ids.has(t);
      });
    }

    return { nodes: filteredNodes, links: filteredLinks };
  }, [rawGraphData, activeFilter, camouflageGateFloor]);

  const onSelectNodeRef = useRef(onSelectNode);
  onSelectNodeRef.current = onSelectNode;

  const isRotatingRef = useRef(isRotating);
  isRotatingRef.current = isRotating;

  // Initialize ForceGraph3D ONCE on mount
  useEffect(() => {
    if (!containerRef.current) return;

    const container = containerRef.current;
    const initialWidth = container.clientWidth || 600;
    const initialHeight = container.clientHeight || 340;

    // Initialize 3D Force Graph WebGL Engine
    const Graph = ForceGraph3D()(container)
      .width(initialWidth)
      .height(initialHeight)
      .graphData(filteredData)
      .nodeLabel((node) => `
        <div style="background: rgba(16, 29, 21, 0.96); border: 1px solid rgba(0, 168, 107, 0.4); border-radius: 8px; padding: 8px 12px; color: #fff; font-family: Inter, sans-serif; box-shadow: 0 8px 24px rgba(0,0,0,0.8); font-size: 11px;">
          <strong style="color: #6EE7B7; font-size: 12px;">${node.name}</strong><br/>
          <span style="color: #94A3B8;">ID:</span> <span style="font-family: monospace;">${node.id}</span><br/>
          <span style="color: #94A3B8;">Bank:</span> ${node.bank}<br/>
          <span style="color: #94A3B8;">Balance:</span> <strong style="color: #34D399;">${node.balance}</strong><br/>
          <span style="color: #94A3B8;">ML Risk:</span> <strong style="color: ${node.risk >= 0.8 ? '#FB7185' : node.risk >= 0.3 ? '#FBBF24' : '#34D399'};">${(node.risk * 100).toFixed(1)}%</strong>
        </div>
      `)
      .nodeColor((node) => node.color)
      .nodeVal((node) => node.val)
      .nodeResolution(24)
      .linkWidth((link) => (link.isLaunderingLoop ? 2.5 : 1.0))
      .linkColor((link) => link.color)
      .linkDirectionalParticles((link) => (link.particles || 1))
      .linkDirectionalParticleSpeed((link) => (link.particleSpeed || 0.003))
      .linkDirectionalParticleWidth((link) => (link.isLaunderingLoop ? 3.5 : 1.5))
      .backgroundColor('#0A140D')
      .showNavInfo(false)
      .onNodeClick((node) => {
        if (onSelectNodeRef.current) onSelectNodeRef.current(node);
      });

    // Custom Glowing Halo Mesh on Central Originator and High-Risk Nodes
    Graph.nodeThreeObjectExtend(true);
    Graph.nodeThreeObject((node) => {
      if (node.isOriginator || node.risk >= 0.90) {
        const sphereRadius = node.isOriginator ? 7 : 4.5;
        const geometry = new THREE.SphereGeometry(sphereRadius, 16, 16);
        const material = new THREE.MeshBasicMaterial({
          color: node.glowColor || '#FF2E63',
          transparent: true,
          opacity: 0.35,
          wireframe: true
        });
        return new THREE.Mesh(geometry, material);
      }
      return false;
    });

    // Center camera on the origin
    Graph.cameraPosition({ x: 0, y: 100, z: 360 }, { x: 0, y: 0, z: 0 }, 500);

    // Responsive ResizeObserver to prevent canvas overflow
    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        if (entry.contentRect.width > 0 && entry.contentRect.height > 0) {
          Graph.width(entry.contentRect.width);
          Graph.height(entry.contentRect.height);
        }
      }
    });
    resizeObserver.observe(container);

    // Auto-Camera Orbit with Tab Visibility Throttling (Saves GPU/CPU when tab is blurred or hidden)
    let angle = 0;
    const distance = 380;
    let animId = null;
    let isTabVisible = typeof document !== 'undefined' ? !document.hidden : true;

    const handleVisibilityChange = () => {
      isTabVisible = typeof document !== 'undefined' ? !document.hidden : true;
      if (Graph) {
        if (!isTabVisible) {
          if (typeof Graph.pauseAnimation === 'function') Graph.pauseAnimation();
        } else {
          if (typeof Graph.resumeAnimation === 'function') Graph.resumeAnimation();
        }
      }
    };
    if (typeof document !== 'undefined') {
      document.addEventListener('visibilitychange', handleVisibilityChange);
    }

    const animateOrbit = () => {
      if (isTabVisible && isRotatingRef.current) {
        angle += 0.002;
        const x = distance * Math.sin(angle);
        const z = distance * Math.cos(angle);
        Graph.cameraPosition({ x, y: 100, z }, { x: 0, y: 0, z: 0 });
      }
      animId = requestAnimationFrame(animateOrbit);
    };

    animId = requestAnimationFrame(animateOrbit);
    graphInstanceRef.current = Graph;

    return () => {
      if (typeof document !== 'undefined') {
        document.removeEventListener('visibilitychange', handleVisibilityChange);
      }
      if (animId) cancelAnimationFrame(animId);
      resizeObserver.disconnect();
      if (graphInstanceRef.current) {
        if (typeof graphInstanceRef.current._destructor === 'function') {
          graphInstanceRef.current._destructor();
        }
        graphInstanceRef.current = null;
      }
      if (container) {
        container.innerHTML = '';
      }
    };
  }, []);

  // Dynamically update data without re-creating WebGL renderer
  useEffect(() => {
    if (graphInstanceRef.current) {
      graphInstanceRef.current.graphData(filteredData);
    }
  }, [filteredData]);

  const handleResetCamera = () => {
    if (graphInstanceRef.current) {
      graphInstanceRef.current.cameraPosition({ x: 0, y: 100, z: 360 }, { x: 0, y: 0, z: 0 }, 800);
    }
  };

  useEffect(() => {
    if (resetTrigger > 0 && graphInstanceRef.current) {
      handleResetCamera();
    }
  }, [resetTrigger]);

  const handleZoomIn = () => {
    if (graphInstanceRef.current) {
      const pos = graphInstanceRef.current.cameraPosition();
      graphInstanceRef.current.cameraPosition({ x: pos.x * 0.8, y: pos.y * 0.8, z: pos.z * 0.8 }, { x: 0, y: 0, z: 0 }, 300);
    }
  };

  const handleZoomOut = () => {
    if (graphInstanceRef.current) {
      const pos = graphInstanceRef.current.cameraPosition();
      graphInstanceRef.current.cameraPosition({ x: pos.x * 1.25, y: pos.y * 1.25, z: pos.z * 1.25 }, { x: 0, y: 0, z: 0 }, 300);
    }
  };

  return (
    <div className="relative overflow-hidden flex flex-col font-sans w-full h-full" style={{ height }}>
      {/* 3D Canvas Viewport */}
      <div ref={containerRef} className="w-full h-full cursor-grab active:cursor-grabbing overflow-hidden" />

      {/* Top Overlay Controls Bar */}
      <div className="absolute top-2 left-2 right-2 flex flex-wrap items-center justify-between gap-1.5 pointer-events-none z-10">
        
        {/* Left: Active Filter Buttons */}
        <div className="flex items-center gap-1 p-1 rounded-lg skeuo-card bg-[var(--bg-surface)]/95 border border-[var(--border-card)] pointer-events-auto shadow-sm">
          <button
            onClick={() => setActiveFilter('ALL')}
            className={`px-2 py-0.5 rounded-md text-[10px] sm:text-[11px] font-semibold transition-all cursor-pointer ${
              activeFilter === 'ALL' ? 'skeuo-btn skeuo-btn-primary' : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
            }`}
          >
            All ({filteredData.nodes.length})
          </button>
          <button
            onClick={() => setActiveFilter('WASH_CYCLE')}
            className={`px-2 py-0.5 rounded-md text-[10px] sm:text-[11px] font-semibold transition-all cursor-pointer ${
              activeFilter === 'WASH_CYCLE' ? 'bg-rose-600 text-white shadow-sm' : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
            }`}
          >
            Laundering Loops
          </button>
          <button
            onClick={() => setActiveFilter('TIER_1_ONLY')}
            className={`px-2 py-0.5 rounded-md text-[10px] sm:text-[11px] font-semibold transition-all cursor-pointer ${
              activeFilter === 'TIER_1_ONLY' ? 'bg-amber-600 text-white shadow-sm' : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
            }`}
          >
            Tier 1 Block
          </button>
        </div>

        {/* Right: Camera Controls */}
        <div className="flex items-center gap-1 p-1 rounded-lg skeuo-card bg-[var(--bg-surface)]/95 border border-[var(--border-card)] pointer-events-auto shadow-sm">
          <button
            onClick={() => setIsRotating(prev => !prev)}
            className={`p-1 rounded-md text-[11px] transition-colors cursor-pointer ${
              isRotating ? 'text-[var(--accent-primary)] bg-[var(--accent-primary)]/15' : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
            }`}
            title={isRotating ? 'Pause Camera Orbit' : 'Resume Auto-Orbit'}
          >
            {isRotating ? <Pause className="w-3 h-3" /> : <Play className="w-3 h-3" />}
          </button>
          <button
            onClick={handleResetCamera}
            className="p-1 rounded-md text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-black/[0.05] dark:hover:bg-white/[0.05] transition-colors cursor-pointer"
            title="Reset Camera Angle"
          >
            <RotateCcw className="w-3 h-3" />
          </button>
          <button
            onClick={handleZoomIn}
            className="p-1 rounded-md text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-black/[0.05] dark:hover:bg-white/[0.05] transition-colors cursor-pointer"
            title="Zoom In"
          >
            <ZoomIn className="w-3 h-3" />
          </button>
          <button
            onClick={handleZoomOut}
            className="p-1 rounded-md text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-black/[0.05] dark:hover:bg-white/[0.05] transition-colors cursor-pointer"
            title="Zoom Out"
          >
            <ZoomOut className="w-3 h-3" />
          </button>
        </div>
      </div>

      {/* Bottom Interactive Camouflage Edge Trust Filter Slider (Module 2) */}
      {showDenoiseSlider && (
        <div className="absolute bottom-2 left-2 right-2 p-2 rounded-xl skeuo-card bg-[var(--bg-surface)]/95 border border-[var(--border-card)] pointer-events-auto z-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-2 text-xs shadow-md">
          <div className="flex items-center gap-2">
            <Sliders className="w-4 h-4 text-[var(--accent-primary)] shrink-0" />
            <div>
              <span className="font-bold text-[var(--text-primary)] text-[11px] block font-mono">Module 2: Camouflage Edge Denoising (gᵢⱼ)</span>
              <span className="text-[10px] text-[var(--text-muted)]">Prunes spurious retail noise to suppress graph over-smoothing</span>
            </div>
          </div>

          <div className="flex items-center gap-3 w-full md:w-auto">
            <input
              type="range"
              min="0.00"
              max="0.50"
              step="0.02"
              value={camouflageGateFloor}
              onChange={(e) => setCamouflageGateFloor(Number(e.target.value))}
              className="w-full md:w-36 accent-[#1B4D3E] cursor-pointer"
            />
            <span className="text-[11px] font-mono text-[var(--accent-primary)] font-bold shrink-0 min-w-[70px]">
              Floor: {camouflageGateFloor.toFixed(2)}
            </span>
            <span className="text-[10px] font-mono text-[var(--accent-primary)] bg-[var(--accent-primary)]/10 px-2 py-0.5 rounded border border-[var(--accent-primary)]/20 shrink-0">
              {camouflageGateFloor > 0.05 ? '65.9% Pruned' : 'Raw Topology'}
            </span>
          </div>
        </div>
      )}
    </div>
  );
};
