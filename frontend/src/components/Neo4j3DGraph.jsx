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
export function generateLargeBankingGraph(baseOriginator = 'BD22-EBLB-4829-1092-8823', nodeCount = 450) {
  const banks = ['Eastern Bank PLC', 'BRAC Bank PLC', 'Emirates NBD Dubai', 'Dutch-Bangla Bank', 'Barclays Bank UK', 'DBS Bank Singapore', 'Islami Bank Bangladesh'];
  const nodeTypes = ['CORPORATE', 'RETAIL', 'OFFSHORE_SHELL', 'MFS_AGENT', 'COMMERCIAL_CONDUIT', 'MERCHANT_CHAFF'];
  
  const nodes = [];
  const links = [];

  // Seed Central Node (Account Holder)
  nodes.push({
    id: baseOriginator,
    name: 'Meghna Industrial & Agro Processing Ltd (Subject)',
    bank: 'Eastern Bank PLC (EBL)',
    type: 'CORPORATE',
    risk: 0.984,
    tier: 'TIER_1_QUARANTINE',
    val: 30,
    color: '#00F2FE', // Quantum Electric Cyan Core
    glowColor: '#8B5CF6', // Ultraviolet Prismatic Halo
    balance: '$1,248,920.45 (৳149.8M)',
    isOriginator: true
  });

  // Layer 1: Core Conduits & Laundering Ring (8 nodes)
  const coreMules = [
    { id: 'BD04-BRAC-1109-8421-4402', name: 'Tanvir Ahmed Rahman (Trade Conduit)', bank: 'BRAC Bank PLC', risk: 0.96, tier: 'TIER_1_QUARANTINE', type: 'COMMERCIAL_CONDUIT' },
    { id: 'AE-EBIL-4412-8819-3301', name: 'Gulf Star Commodities FZE (JAFZA Dubai)', bank: 'Emirates NBD Dubai', risk: 0.95, tier: 'TIER_1_QUARANTINE', type: 'OFFSHORE_SHELL' },
    { id: 'SG-DBS-8819-3301', name: 'Pacific Commodities Escrow Pte', bank: 'DBS Bank Singapore', risk: 0.98, tier: 'TIER_1_QUARANTINE', type: 'OFFSHORE_SHELL' },
    { id: 'GB-BARC-1109-8421-4402', name: 'Anglo-Bengal Textiles Ltd (Manchester)', bank: 'Barclays Bank UK', risk: 0.88, tier: 'TIER_1_QUARANTINE', type: 'CORPORATE' },
    { id: 'MFS-BKASH-0171-8840', name: 'Mohammad Rafiqul Islam (bKash Agent)', bank: 'bKash Limited', risk: 0.78, tier: 'TIER_1_QUARANTINE', type: 'MFS_AGENT' },
    { id: 'BD91-DBBL-4401-2299-1184', name: 'Sadia Sultana (Dormant Payroll)', bank: 'Dutch-Bangla Bank PLC', risk: 0.65, tier: 'TIER_2_REVIEW_QUEUE', type: 'RETAIL' },
    { id: 'BD18-CIBL-3312-8804-1290', name: 'Square Fashion & Apparels Ltd', bank: 'City Bank PLC', risk: 0.03, tier: 'TIER_3_CLEARED', type: 'CORPORATE' },
    { id: 'BD04-BRAC-0192-8821-4401', name: 'Beximco Pharmaceuticals Ltd', bank: 'BRAC Bank PLC', risk: 0.02, tier: 'TIER_3_CLEARED', type: 'CORPORATE' },
  ];

  coreMules.forEach((m) => {
    const isHighRisk = m.risk >= 0.85;
    const isMed = m.risk >= 0.40;
    const color = isHighRisk 
      ? (m.type === 'OFFSHORE_SHELL' ? '#D946EF' : '#FF0055') 
      : isMed ? '#F59E0B' : '#00F2FE';
    const glow = isHighRisk ? '#EC4899' : isMed ? '#FBBF24' : '#38BDF8';

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

    // Connect to central with Prismatic Laser Link
    links.push({
      source: baseOriginator,
      target: m.id,
      amount: Math.floor(Math.random() * 45000 + 4000),
      gate: isHighRisk ? 0.98 : 0.72,
      color: isHighRisk ? 'rgba(255, 0, 85, 0.9)' : 'rgba(245, 158, 11, 0.8)',
      particleSpeed: isHighRisk ? 0.010 : 0.005,
      particles: isHighRisk ? 5 : 2,
      isLaunderingLoop: isHighRisk
    });
  });

  // Closed Circular Wash Loop (Hyper-Luminescent Neon Pink Laser)
  links.push({ source: baseOriginator, target: 'BD04-BRAC-1109-8421-4402', amount: 47600, gate: 0.98, color: '#FF007F', particleSpeed: 0.012, particles: 6, isLaunderingLoop: true });
  links.push({ source: 'BD04-BRAC-1109-8421-4402', target: 'AE-EBIL-4412-8819-3301', amount: 47600, gate: 0.99, color: '#FF007F', particleSpeed: 0.012, particles: 6, isLaunderingLoop: true });
  links.push({ source: 'AE-EBIL-4412-8819-3301', target: baseOriginator, amount: 47600, gate: 0.99, color: '#FF007F', particleSpeed: 0.014, particles: 7, isLaunderingLoop: true });

  // Generate extended background counterparties
  for (let i = 0; i < nodeCount; i++) {
    const roll = Math.random();
    const isClean = roll > 0.15;
    const isReview = !isClean && roll > 0.04;
    const isRisk = !isClean && !isReview;

    const riskScore = isRisk ? (0.85 + Math.random() * 0.14) : isReview ? (0.35 + Math.random() * 0.40) : (0.01 + Math.random() * 0.15);
    const color = isRisk ? '#FF0055' : isReview ? '#F59E0B' : '#00F2FE';
    const glowColor = isRisk ? '#EC4899' : isReview ? '#FBBF24' : '#38BDF8';
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
      color: type === 'MERCHANT_CHAFF' ? 'rgba(148, 163, 184, 0.45)' : color,
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
      color: isCamouflage ? 'rgba(99, 102, 241, 0.18)' : isRisk ? 'rgba(255, 0, 85, 0.75)' : 'rgba(6, 182, 212, 0.45)',
      particleSpeed: isRisk ? 0.008 : 0.003,
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
  showDenoiseSlider = false,
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
        <div style="background: rgba(8, 12, 32, 0.96); backdrop-filter: blur(16px); border: 1px solid rgba(6, 182, 212, 0.5); box-shadow: 0 0 24px rgba(6, 182, 212, 0.3), 0 0 40px rgba(139, 92, 246, 0.2); border-radius: 10px; padding: 10px 14px; color: #fff; font-family: Inter, sans-serif; font-size: 11px; min-width: 210px;">
          <div style="height: 2px; background: linear-gradient(90deg, #00F2FE, #8B5CF6, #EC4899); margin-bottom: 8px; border-radius: 2px;"></div>
          <strong style="color: #00F2FE; font-size: 12px; display: block; margin-bottom: 4px;">${node.name}</strong>
          <div style="font-family: monospace; font-size: 10px; color: #94A3B8; margin-bottom: 6px;">ID: <span style="color: #E2E8F0;">${node.id}</span></div>
          <div style="display: flex; justify-content: space-between; margin-bottom: 3px;"><span style="color: #94A3B8;">Rail/Bank:</span> <span style="color: #E2E8F0;">${node.bank}</span></div>
          <div style="display: flex; justify-content: space-between; margin-bottom: 3px;"><span style="color: #94A3B8;">Ledger:</span> <strong style="color: #00F2FE;">${node.balance}</strong></div>
          <div style="display: flex; justify-content: space-between; margin-top: 6px; padding-top: 6px; border-top: 1px solid rgba(255,255,255,0.1);">
            <span style="color: #94A3B8;">C-STGB Risk:</span> 
            <strong style="color: ${node.risk >= 0.8 ? '#FF0055' : node.risk >= 0.3 ? '#F59E0B' : '#00F2FE'}; font-weight: bold;">
              ${(node.risk * 100).toFixed(1)}% (${node.tier ? node.tier.replace(/_/g, ' ') : 'TIER'})
            </strong>
          </div>
        </div>
      `)
      .nodeColor((node) => node.color)
      .nodeVal((node) => node.val)
      .nodeResolution(24)
      .linkWidth((link) => (link.isLaunderingLoop ? 2.8 : 1.0))
      .linkColor((link) => link.color)
      .linkDirectionalParticles((link) => (link.particles || 1))
      .linkDirectionalParticleSpeed((link) => (link.particleSpeed || 0.003))
      .linkDirectionalParticleWidth((link) => (link.isLaunderingLoop ? 3.8 : 1.5))
      .backgroundColor('#050816')
      .showNavInfo(false)
      .onNodeClick((node) => {
        if (onSelectNodeRef.current) onSelectNodeRef.current(node);
      });

    // Custom Prismatic Glowing Halo Mesh on Central Originator and High-Risk Nodes
    Graph.nodeThreeObjectExtend(true);
    Graph.nodeThreeObject((node) => {
      if (node.isOriginator) {
        // Dual Prismatic Three.js Halo for Subject Core
        const group = new THREE.Group();
        const innerGeo = new THREE.IcosahedronGeometry(7.5, 2);
        const innerMat = new THREE.MeshBasicMaterial({
          color: 0x00f2fe,
          transparent: true,
          opacity: 0.5,
          wireframe: true
        });
        group.add(new THREE.Mesh(innerGeo, innerMat));

        const outerGeo = new THREE.IcosahedronGeometry(11, 1);
        const outerMat = new THREE.MeshBasicMaterial({
          color: 0x8b5cf6,
          transparent: true,
          opacity: 0.25,
          wireframe: true
        });
        group.add(new THREE.Mesh(outerGeo, outerMat));
        return group;
      }
      if (node.risk >= 0.85) {
        // Pulsing Neon Crimson Halo for Laundering Nodes
        const sphereRadius = 5.0;
        const geometry = new THREE.SphereGeometry(sphereRadius, 16, 16);
        const material = new THREE.MeshBasicMaterial({
          color: 0xff0055,
          transparent: true,
          opacity: 0.4,
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

      {/* Top Overlay Controls Bar (Anchored Right to prevent HUD badge overlap) */}
      <div className="absolute top-2 right-2 flex flex-wrap items-center justify-end gap-1.5 pointer-events-none z-10">
        
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
