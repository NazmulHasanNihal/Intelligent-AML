import React, { useState, useRef } from 'react';
import { ZoomIn, ZoomOut, RotateCcw, ArrowRight, ShieldAlert, Sparkles, Building2, User, Clock } from 'lucide-react';

export const Planar2DGraph = ({
  selectedNode,
  onSelectNode,
  camouflageThreshold = 0.10,
  highlightCycle = true,
  timelineMinute = 45, // 0 to 45 (representing 08:00 to 08:45 UTC)
  pathHighlight = false
}) => {
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [hoveredNode, setHoveredNode] = useState(null);

  // Core Wash Ring Nodes (Coordinates on 800x500 canvas)
  const ringNodes = [
    {
      id: 'BD22-EBLB-4829-1092-8823',
      name: 'Meghna Industrial & Agro Processing Ltd',
      shortName: 'Meghna Industrial (Hub)',
      bank: 'Eastern Bank PLC (EBL)',
      type: 'CORPORATE',
      risk: 0.94,
      tier: 'TIER_1_QUARANTINE',
      balance: '$1,248,920.45 (৳149.8M)',
      inDegree: 4,
      outDegree: 8,
      x: 400,
      y: 250,
      radius: 28,
      isCore: true,
      color: '#00F2FE'
    },
    {
      id: 'BD04-BRAC-1109-8832-9011',
      name: 'Tanvir Ahmed Rahman (Trade Conduit)',
      shortName: 'Tanvir Rahman (Mule)',
      bank: 'BRAC Bank PLC',
      type: 'RETAIL',
      risk: 0.96,
      tier: 'TIER_1_QUARANTINE',
      balance: '$420,118.00 (৳50.4M)',
      inDegree: 3,
      outDegree: 5,
      x: 230,
      y: 130,
      radius: 22,
      color: '#FF0055'
    },
    {
      id: 'AE-EBIL-5512-GULFSTAR',
      name: 'Gulf Star Commodities FZE',
      shortName: 'Gulf Star (Dubai JAFZA)',
      bank: 'Emirates NBD Dubai',
      type: 'CORPORATE',
      risk: 0.95,
      tier: 'TIER_1_QUARANTINE',
      balance: '$890,450.00',
      inDegree: 4,
      outDegree: 6,
      x: 570,
      y: 130,
      radius: 22,
      color: '#FF0055'
    },
    {
      id: 'SG-DBS-ESCROW-PACIFIC',
      name: 'Pacific Commodities Escrow Pte',
      shortName: 'Pacific Escrow (Singapore)',
      bank: 'DBS Bank Singapore',
      type: 'OFFSHORE_SHELL',
      risk: 0.98,
      tier: 'TIER_1_QUARANTINE',
      balance: '$3,150,000.00',
      inDegree: 2,
      outDegree: 4,
      x: 570,
      y: 370,
      radius: 22,
      color: '#D946EF'
    },
    {
      id: 'GB-BARC-1109-8421-4402',
      name: 'Anglo-Bengal Freight Clearing Ltd',
      shortName: 'Anglo-Bengal (London E1)',
      bank: 'Barclays Bank London',
      type: 'CORPORATE',
      risk: 0.91,
      tier: 'TIER_1_QUARANTINE',
      balance: '$750,000.00',
      inDegree: 2,
      outDegree: 3,
      x: 180,
      y: 360,
      radius: 20,
      color: '#D946EF'
    },
    {
      id: 'MFS-BKASH-0019-4821',
      name: 'Mohammad Rafiqul Islam (MFS)',
      shortName: 'Rafiqul (MFS Agent)',
      bank: 'bKash Agent Treasury',
      type: 'RETAIL',
      risk: 0.65,
      tier: 'TIER_2_REVIEW_QUEUE',
      balance: '$18,400.00 (৳2.2M)',
      inDegree: 2,
      outDegree: 3,
      x: 320,
      y: 410,
      radius: 18,
      color: '#F59E0B'
    },
    {
      id: 'BD18-CIBL-3312-SQUARE',
      name: 'Square Fashion & Apparels Ltd',
      shortName: 'Square Fashion (RMG)',
      bank: 'City Bank PLC Corporate',
      type: 'CORPORATE',
      risk: 0.58,
      tier: 'TIER_2_REVIEW_QUEUE',
      balance: '$640,000.00',
      inDegree: 3,
      outDegree: 4,
      x: 690,
      y: 250,
      radius: 18,
      color: '#F59E0B'
    },
    {
      id: 'DE-DB-9901-EUROTEXTILE',
      name: 'EuroTextile Importers GmbH',
      shortName: 'EuroTextile (Hamburg)',
      bank: 'Deutsche Bank Frankfurt',
      type: 'CORPORATE',
      risk: 0.42,
      tier: 'TIER_2_REVIEW_QUEUE',
      balance: '$320,000.00',
      inDegree: 5,
      outDegree: 5,
      x: 400,
      y: 70,
      radius: 17,
      color: '#F59E0B'
    }
  ];

  // Directed Flow Edges
  const edges = [
    {
      from: 'BD22-EBLB-4829-1092-8823',
      to: 'BD04-BRAC-1109-8832-9011',
      amount: '$48,500 (৳5.8M)',
      time: '08:10',
      minute: 10,
      isLoop: true,
      label: 'Step 1: RTGS Out ($48.5k)'
    },
    {
      from: 'BD04-BRAC-1109-8832-9011',
      to: 'AE-EBIL-5512-GULFSTAR',
      amount: '$48,100',
      time: '08:18',
      minute: 18,
      isLoop: true,
      label: 'Step 2: SWIFT Wire ($48.1k)'
    },
    {
      from: 'AE-EBIL-5512-GULFSTAR',
      to: 'SG-DBS-ESCROW-PACIFIC',
      amount: '$47,900',
      time: '08:24',
      minute: 24,
      isLoop: true,
      label: 'Step 3: Escrow Layer ($47.9k)'
    },
    {
      from: 'SG-DBS-ESCROW-PACIFIC',
      to: 'BD22-EBLB-4829-1092-8823',
      amount: '$47,600 (৳5.7M)',
      time: '08:31',
      minute: 31,
      isLoop: true,
      label: 'Step 4: LC Wash Return ($47.6k)'
    },
    {
      from: 'BD22-EBLB-4829-1092-8823',
      to: 'GB-BARC-1109-8421-4402',
      amount: '$95,000',
      time: '08:38',
      minute: 38,
      isLoop: false,
      label: 'London Freight Clearing ($95k)'
    },
    {
      from: 'BD22-EBLB-4829-1092-8823',
      to: 'MFS-BKASH-0019-4821',
      amount: '$4,800 (৳576k)',
      time: '08:05',
      minute: 5,
      isLoop: false,
      label: 'MFS Cash-Out Feeder'
    },
    {
      from: 'AE-EBIL-5512-GULFSTAR',
      to: 'BD18-CIBL-3312-SQUARE',
      amount: '$12,400',
      time: '08:28',
      minute: 28,
      isLoop: false,
      label: 'RMG Trade Transit'
    },
    {
      from: 'DE-DB-9901-EUROTEXTILE',
      to: 'AE-EBIL-5512-GULFSTAR',
      amount: '$32,400',
      time: '08:15',
      minute: 15,
      isLoop: false,
      label: 'Supply Chain Leg'
    }
  ];

  const nodeMap = new Map(ringNodes.map(n => [n.id, n]));

  const handleMouseDown = (e) => {
    setIsDragging(true);
    setDragStart({ x: e.clientX - pan.x, y: e.clientY - pan.y });
  };

  const handleMouseMove = (e) => {
    if (!isDragging) return;
    setPan({ x: e.clientX - dragStart.x, y: e.clientY - dragStart.y });
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  return (
    <div className="relative w-full h-full bg-[#050816] select-none overflow-hidden flex flex-col">
      {/* 2D Planar Top Controls */}
      <div className="absolute top-2.5 right-2.5 z-20 flex items-center gap-1.5 p-1 rounded-xl bg-[#090D1C]/90 backdrop-blur-md border border-cyan-500/30 shadow-md">
        <button
          onClick={() => setZoom(prev => Math.min(2.0, prev + 0.15))}
          className="p-1.5 rounded-lg text-slate-300 hover:text-cyan-300 hover:bg-white/5 transition-all cursor-pointer"
          title="Zoom In"
        >
          <ZoomIn className="w-3.5 h-3.5" />
        </button>
        <button
          onClick={() => setZoom(prev => Math.max(0.6, prev - 0.15))}
          className="p-1.5 rounded-lg text-slate-300 hover:text-cyan-300 hover:bg-white/5 transition-all cursor-pointer"
          title="Zoom Out"
        >
          <ZoomOut className="w-3.5 h-3.5" />
        </button>
        <button
          onClick={() => { setZoom(1); setPan({ x: 0, y: 0 }); }}
          className="p-1.5 rounded-lg text-slate-300 hover:text-cyan-300 hover:bg-white/5 transition-all cursor-pointer"
          title="Reset Viewport"
        >
          <RotateCcw className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* SVG Canvas */}
      <svg
        className="w-full h-full cursor-grab active:cursor-grabbing"
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
      >
        <defs>
          {/* Arrowhead Markers */}
          <marker id="arrow-pink" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="#FF007F" />
          </marker>
          <marker id="arrow-cyan" viewBox="0 0 10 10" refX="20" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="#00F2FE" />
          </marker>
          <marker id="arrow-dim" viewBox="0 0 10 10" refX="18" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="#475569" />
          </marker>

          {/* Gradients */}
          <radialGradient id="originatorGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#00F2FE" stopOpacity="0.8" />
            <stop offset="60%" stopColor="#0284C7" stopOpacity="0.3" />
            <stop offset="100%" stopColor="#0284C7" stopOpacity="0" />
          </radialGradient>
        </defs>

        <g transform={`translate(${pan.x}, ${pan.y}) scale(${zoom})`}>
          {/* Grid Background Lines for Tactical Clarity */}
          <g stroke="rgba(148, 163, 184, 0.05)" strokeWidth="1">
            {Array.from({ length: 16 }).map((_, i) => (
              <line key={`v-${i}`} x1={i * 60} y1="0" x2={i * 60} y2="600" />
            ))}
            {Array.from({ length: 11 }).map((_, i) => (
              <line key={`h-${i}`} x1="0" y1={i * 60} x2="900" y2={i * 60} />
            ))}
          </g>

          {/* Directed Edges */}
          {edges.map((edge, idx) => {
            const src = nodeMap.get(edge.from);
            const dst = nodeMap.get(edge.to);
            if (!src || !dst) return null;

            const isVisibleByTimeline = edge.minute <= timelineMinute;
            const isWashEdge = edge.isLoop;
            const isHighlighted = (highlightCycle && isWashEdge) || pathHighlight;

            const strokeColor = !isVisibleByTimeline 
              ? 'rgba(71, 85, 105, 0.2)' 
              : isHighlighted 
              ? '#FF007F' 
              : 'rgba(6, 182, 212, 0.5)';
            const strokeWidth = !isVisibleByTimeline ? 1 : isHighlighted ? 2.5 : 1.5;
            const markerEnd = !isVisibleByTimeline ? 'url(#arrow-dim)' : isHighlighted ? 'url(#arrow-pink)' : 'url(#arrow-cyan)';

            // Control point for smooth curved quadratic bezier
            const midX = (src.x + dst.x) / 2;
            const midY = (src.y + dst.y) / 2;
            const dx = dst.x - src.x;
            const dy = dst.y - src.y;
            const normalX = -dy * 0.15;
            const normalY = dx * 0.15;
            const cpX = midX + normalX;
            const cpY = midY + normalY;

            return (
              <g key={`edge-${idx}`} opacity={isVisibleByTimeline ? 1 : 0.25} className="transition-opacity duration-300">
                <path
                  d={`M ${src.x} ${src.y} Q ${cpX} ${cpY} ${dst.x} ${dst.y}`}
                  fill="none"
                  stroke={strokeColor}
                  strokeWidth={strokeWidth}
                  strokeDasharray={isHighlighted && isVisibleByTimeline ? '6 3' : 'none'}
                  markerEnd={markerEnd}
                />
                {/* Edge Amount Badge */}
                {isVisibleByTimeline && (
                  <g transform={`translate(${cpX}, ${cpY})`}>
                    <rect
                      x="-32"
                      y="-10"
                      width="64"
                      height="18"
                      rx="4"
                      fill="#070C1E"
                      stroke={isHighlighted ? '#FF007F' : '#0E7490'}
                      strokeWidth="1"
                    />
                    <text
                      x="0"
                      y="2"
                      textAnchor="middle"
                      dominantBaseline="middle"
                      fill={isHighlighted ? '#F43F5E' : '#38BDF8'}
                      fontSize="9"
                      fontFamily="monospace"
                      fontWeight="bold"
                    >
                      {edge.amount}
                    </text>
                  </g>
                )}
              </g>
            );
          })}

          {/* Graph Nodes */}
          {ringNodes.map((node) => {
            const isSelected = selectedNode?.id === node.id;
            const isHovered = hoveredNode?.id === node.id;
            const isHighRisk = node.risk >= 0.85;

            return (
              <g
                key={node.id}
                transform={`translate(${node.x}, ${node.y})`}
                onClick={() => onSelectNode(node)}
                onMouseEnter={() => setHoveredNode(node)}
                onMouseLeave={() => setHoveredNode(null)}
                className="cursor-pointer"
              >
                {/* Outer Glow on Selected / Core Node */}
                {(isSelected || node.isCore) && (
                  <circle
                    r={node.radius + 14}
                    fill="none"
                    stroke={node.isCore ? '#00F2FE' : '#FF0055'}
                    strokeWidth="1.5"
                    strokeDasharray="4 2"
                    opacity="0.8"
                    className="animate-spin"
                    style={{ animationDuration: '18s' }}
                  />
                )}

                {/* Primary Node Body */}
                <circle
                  r={node.radius}
                  fill={node.isCore ? '#003B5C' : isHighRisk ? '#3B081B' : '#0B293C'}
                  stroke={isSelected ? '#FFFFFF' : node.color}
                  strokeWidth={isSelected ? 3 : 2}
                  className="transition-all duration-200"
                />

                {/* Inner Icon / Letter */}
                <text
                  textAnchor="middle"
                  dominantBaseline="middle"
                  fill="#FFFFFF"
                  fontSize="10"
                  fontWeight="bold"
                  fontFamily="monospace"
                  pointerEvents="none"
                >
                  {node.type === 'CORPORATE' ? 'CORP' : node.type === 'CRYPTO_MIXER' ? 'UTXO' : node.type === 'OFFSHORE_SHELL' ? 'BVI' : 'RET'}
                </text>

                {/* Node Label Below */}
                <text
                  y={node.radius + 14}
                  textAnchor="middle"
                  fill={isSelected ? '#00F2FE' : '#E2E8F0'}
                  fontSize="10"
                  fontWeight={isSelected || node.isCore ? 'bold' : 'normal'}
                  fontFamily="Inter, sans-serif"
                  pointerEvents="none"
                >
                  {node.shortName}
                </text>

                {/* Risk Badge */}
                <g transform={`translate(0, ${node.radius + 25})`}>
                  <rect
                    x="-20"
                    y="-6"
                    width="40"
                    height="12"
                    rx="3"
                    fill={isHighRisk ? '#881337' : '#78350F'}
                    stroke={isHighRisk ? '#E11D48' : '#D97706'}
                    strokeWidth="0.8"
                  />
                  <text
                    x="0"
                    y="1"
                    textAnchor="middle"
                    dominantBaseline="middle"
                    fill="#FFFFFF"
                    fontSize="8"
                    fontFamily="monospace"
                    fontWeight="bold"
                  >
                    {(node.risk * 100).toFixed(0)}%
                  </text>
                </g>
              </g>
            );
          })}
        </g>
      </svg>

      {/* Node Hover Tooltip Card */}
      {hoveredNode && (
        <div 
          className="absolute pointer-events-none z-30 p-2.5 rounded-xl bg-[#090D1C]/95 backdrop-blur-md border border-cyan-500/40 text-[10px] font-mono text-white shadow-xl space-y-1 w-56"
          style={{ top: 12, left: 12 }}
        >
          <div className="flex items-center justify-between pb-1 border-b border-cyan-500/20">
            <span className="font-bold text-cyan-300 truncate max-w-[130px]">{hoveredNode.name}</span>
            <span className={`px-1.5 py-0.2 rounded font-bold ${hoveredNode.risk >= 0.85 ? 'text-rose-400 bg-rose-500/20' : 'text-amber-400 bg-amber-500/20'}`}>
              {(hoveredNode.risk * 100).toFixed(0)}%
            </span>
          </div>
          <div><span className="text-slate-400">Account:</span> <span className="break-all">{hoveredNode.id}</span></div>
          <div><span className="text-slate-400">Bank:</span> {hoveredNode.bank}</div>
          <div><span className="text-slate-400">Balance:</span> <span className="text-cyan-300">{hoveredNode.balance}</span></div>
          <div className="flex justify-between text-slate-400 pt-0.5">
            <span>In-Degree: {hoveredNode.inDegree}</span>
            <span>Out-Degree: {hoveredNode.outDegree}</span>
          </div>
        </div>
      )}
    </div>
  );
};
