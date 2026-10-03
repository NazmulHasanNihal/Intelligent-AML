import React, { useEffect, useRef, useState, useMemo } from 'react';
import cytoscape from 'cytoscape';
import { 
  Maximize2, 
  ZoomIn, 
  ZoomOut, 
  Download, 
  Layers, 
  Filter,
  Route,
  ArrowRight,
  ShieldAlert,
  Sliders,
  CheckCircle2,
  Info,
  Play,
  Pause,
  RotateCcw,
  SkipForward,
  SkipBack,
  Eye,
  EyeOff,
  Clock,
  Sparkles
} from 'lucide-react';
import { useAppStore } from '../../lib/store';
import { evaluateEdgeTrust } from '../../lib/scoringEngine';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';

export const Cytoscape2DGraph = ({ onNodeSelect }) => {
  const containerRef = useRef(null);
  const cyRef = useRef(null);
  const { 
    openDrawer, 
    camouflageDelta, 
    setCamouflageDelta,
    timelineStep,
    setTimelineStep,
    egoHopDistance,
    setEgoHopDistance,
    maxVisibleNodes,
    setMaxVisibleNodes,
    camouflageGatingEnabled,
    setCamouflageGatingEnabled,
    setSelectedGraphNode
  } = useAppStore();

  const [pathSource, setPathSource] = useState('BD22-EBLB-4829-1092-8823');
  const [pathTarget, setPathTarget] = useState('BD04-BRAC-1109-8421-4402');
  const [isPathFound, setIsPathFound] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const playTimerRef = useRef(null);

  // Initial Seeded Ego-Network with Authentic Bangladeshi & Cross-Border Entities
  const allElements = [
    // Core Seed Nodes (Hop 1)
    { data: { id: 'BD22-EBLB-4829-1092-8823', label: 'Meghna Industrial & Agro (Hub)', tier: 'Tier 1 Hold', tierCode: 1, role: 'Trade Originator & Smurfing Hub', amount: 48500, riskScore: 0.984, hop: 1, timeStep: 0 } },
    { data: { id: 'BD04-BRAC-1109-8421-4402', label: 'Tanvir Ahmed Rahman (Conduit)', tier: 'Tier 1 Hold', tierCode: 1, role: 'Hundi & MFS Aggregator', amount: 38400, riskScore: 0.972, hop: 1, timeStep: 1 } },
    { data: { id: 'AE-EBIL-4412-8819-3301', label: 'Gulf Star Commodities (Dubai)', tier: 'Tier 1 Hold', tierCode: 1, role: 'JAFZA Free Zone Offshore Entity', amount: 47600, riskScore: 0.965, hop: 1, timeStep: 3 } },
    { data: { id: 'MFS-BKASH-0171-8840', label: 'Mohammad Rafiqul Islam (MFS)', tier: 'Tier 2 Review', tierCode: 2, role: 'MFS Agent Account', amount: 4800, riskScore: 0.642, hop: 1, timeStep: 1 } },
    { data: { id: 'BD04-BRAC-0192-8821-4401', label: 'Beximco Pharmaceuticals Ltd', tier: 'Tier 3 Clear', tierCode: 3, role: 'Prime Pharma Exporter', amount: 14250, riskScore: 0.012, hop: 1, timeStep: 0 } },
    { data: { id: 'BD12-HSBC-2201-9940', label: 'Grameenphone Corporate Treasury', tier: 'Tier 3 Clear', tierCode: 3, role: 'Telecom Settlement Gateway', amount: 14250, riskScore: 0.005, hop: 1, timeStep: 0 } },
    { data: { id: 'BD18-CIBL-3312-8804', label: 'Square Fashion & Apparels Ltd', tier: 'Tier 2 Review', tierCode: 2, role: 'RMG Commercial Exporter', amount: 6200, riskScore: 0.580, hop: 1, timeStep: 0 } },
    { data: { id: 'DE-DB-9901-7721-5540', label: 'EuroTextile Importers (Hamburg)', tier: 'Tier 3 Clear', tierCode: 3, role: 'Verified German Importer', amount: 6200, riskScore: 0.082, hop: 1, timeStep: 0 } },

    // Peripheral Retail POS Camouflage Chaff Nodes (Hop 2)
    { data: { id: 'BD-POS-SHWAPNO-01', label: 'Shwapno Supermarket POS', tier: 'Tier 3 Clear', tierCode: 3, role: 'Retail Merchant', amount: 12.0, riskScore: 0.01, isCamouflageNode: true, hop: 2, timeStep: 0 } },
    { data: { id: 'BD-BILL-GP-02', label: 'Grameenphone Corporate Bill', tier: 'Tier 3 Clear', tierCode: 3, role: 'Telecom Utility', amount: 4.8, riskScore: 0.01, isCamouflageNode: true, hop: 2, timeStep: 0 } },
    { data: { id: 'BD-POS-DARAZ-03', label: 'Daraz Online Shopping POS', tier: 'Tier 3 Clear', tierCode: 3, role: 'E-commerce POS', amount: 18.3, riskScore: 0.02, isCamouflageNode: true, hop: 2, timeStep: 0 } },
    { data: { id: 'BD-POS-PATHAO-04', label: 'Pathao Courier Logistics', tier: 'Tier 3 Clear', tierCode: 3, role: 'Urban Courier Logistics', amount: 2.8, riskScore: 0.01, isCamouflageNode: true, hop: 2, timeStep: 0 } },

    // 2-Hop and 3-Hop Extended Corridor Nodes
    { data: { id: 'SG-DBS-8819-3301', label: 'Pacific Commodities (Singapore)', tier: 'Tier 2 Review', tierCode: 2, role: 'Singapore Broker', amount: 4800, riskScore: 0.610, hop: 2, timeStep: 2 } },
    { data: { id: 'GB-BARC-1109-8421-4402', label: 'Anglo-Bengal Freight (London)', tier: 'Tier 1 Hold', tierCode: 1, role: 'UK Clearing Hub', amount: 47600, riskScore: 0.940, hop: 3, timeStep: 3 } },
    { data: { id: 'CH-UBS-4491-0021-9912', label: 'Helvetia Trade Nominee (Geneva)', tier: 'Tier 2 Review', tierCode: 2, role: 'Offshore Escrow', amount: 24000, riskScore: 0.540, hop: 3, timeStep: 4 } },

    // Flow Edges with Temporal Sequence Tagging
    // Step 1: Smurfing Inflow ($4,800 bKash to Mule)
    { data: { id: 'e6', source: 'MFS-BKASH-0171-8840', target: 'BD04-BRAC-1109-8421-4402', label: '$4,800 (bKash MFS)', amount: 4800, rail: 'bKash MFS', timeStep: 1, hop: 1 } },
    
    // Step 2: Layering Interbank ($47,600 RTGS from Meghna to Tanvir)
    { data: { id: 'e3', source: 'BD22-EBLB-4829-1092-8823', target: 'BD04-BRAC-1109-8421-4402', label: '$47,600 (RTGS)', amount: 47600, rail: 'RTGS (BD Bank)', isLoop: true, timeStep: 2, hop: 1 } },
    
    // Step 3: Integration Outflow ($47,600 SWIFT to Dubai Free Zone)
    { data: { id: 'e4', source: 'BD04-BRAC-1109-8421-4402', target: 'AE-EBIL-4412-8819-3301', label: '$47,600 (SWIFT Wire)', amount: 47600, rail: 'SWIFT MT103', isLoop: true, timeStep: 3, hop: 1 } },
    { data: { id: 'e10', source: 'AE-EBIL-4412-8819-3301', target: 'GB-BARC-1109-8421-4402', label: '$47,600 (CHAPS)', amount: 47600, rail: 'CHAPS', timeStep: 3, hop: 3 } },
    
    // Step 4: Cycle-3 Wash Return (SWIFT MT700 LC Wash Return to Meghna)
    { data: { id: 'e5', source: 'AE-EBIL-4412-8819-3301', target: 'BD22-EBLB-4829-1092-8823', label: '$47,600 (Cycle-3 Return)', amount: 47600, rail: 'SWIFT MT700 (LC)', isLoop: true, timeStep: 4, hop: 1 } },
    { data: { id: 'e1', source: 'BD22-EBLB-4829-1092-8823', target: 'AE-EBIL-4412-8819-3301', label: '$9,450 (SWIFT LC)', amount: 9450, rail: 'SWIFT MT700 (LC)', timeStep: 2, hop: 1 } },
    { data: { id: 'e2', source: 'BD22-EBLB-4829-1092-8823', target: 'AE-EBIL-4412-8819-3301', label: '$9,600 (SWIFT LC)', amount: 9600, rail: 'SWIFT MT700 (LC)', timeStep: 2, hop: 1 } },
    { data: { id: 'e11', source: 'MFS-BKASH-0171-8840', target: 'SG-DBS-8819-3301', label: '$4,800', amount: 4800, rail: 'SWIFT', timeStep: 2, hop: 2 } },
    { data: { id: 'e12', source: 'GB-BARC-1109-8421-4402', target: 'CH-UBS-4491-0021-9912', label: '$24,000', amount: 24000, rail: 'SEPA', timeStep: 4, hop: 3 } },

    // Legitimate Background Interbank Corridors
    { data: { id: 'e7', source: 'BD18-CIBL-3312-8804', target: 'DE-DB-9901-7721-5540', label: '$6,200 (Export Wire)', amount: 6200, rail: 'RTGS (BD Bank)', timeStep: 0, hop: 1 } },
    { data: { id: 'e8', source: 'BD04-BRAC-0192-8821-4401', target: 'BD12-HSBC-2201-9940', label: '$14,250 (Interbank)', amount: 14250, rail: 'SWIFT MT103', timeStep: 0, hop: 1 } },

    // Injected Camouflage Chaff Edges (Low-value retail noise to dilute GNN attention)
    { data: { id: 'e_chaff1', source: 'BD04-BRAC-1109-8421-4402', target: 'BD-POS-SHWAPNO-01', label: '$12.00', amount: 12.0, rail: 'POS Retail', isCamouflage: true, hop: 2, timeStep: 0 } },
    { data: { id: 'e_chaff2', source: 'BD04-BRAC-1109-8421-4402', target: 'BD-BILL-GP-02', label: '$4.80', amount: 4.8, rail: 'bKash MFS', isCamouflage: true, hop: 2, timeStep: 0 } },
    { data: { id: 'e_chaff3', source: 'BD04-BRAC-1109-8421-4402', target: 'BD-POS-DARAZ-03', label: '$18.30', amount: 18.3, rail: 'Visa Net BD', isCamouflage: true, hop: 2, timeStep: 0 } },
    { data: { id: 'e_chaff4', source: 'BD04-BRAC-1109-8421-4402', target: 'BD-POS-PATHAO-04', label: '$2.80', amount: 2.8, rail: 'Nagad MFS', isCamouflage: true, hop: 2, timeStep: 0 } }
  ];

  // Filter elements by egoHopDistance and maxVisibleNodes
  const visibleElements = useMemo(() => {
    // 1. Filter nodes by hop distance
    const nodes = allElements.filter(el => !el.data.source && el.data.hop <= egoHopDistance);
    
    // Sort nodes to prioritize high-risk nodes (Tier 1 then Tier 2) up to maxVisibleNodes
    nodes.sort((a, b) => (b.data.riskScore || 0) - (a.data.riskScore || 0));
    const cappedNodes = nodes.slice(0, maxVisibleNodes);
    const visibleNodeIds = new Set(cappedNodes.map(n => n.data.id));

    // 2. Filter edges whose source and target are both in visibleNodeIds
    const edges = allElements.filter(el => {
      if (!el.data.source) return false;
      return visibleNodeIds.has(el.data.source) && visibleNodeIds.has(el.data.target);
    });

    return [...cappedNodes, ...edges];
  }, [egoHopDistance, maxVisibleNodes]);

  // Timeline Step Metadata
  const TIMELINE_STEPS = [
    { step: 0, label: '08:00 UTC', title: 'Quiescent Baseline', desc: 'Pre-event interbank corridor status' },
    { step: 1, label: '08:14 UTC', title: 'Phase 1: MFS Smurfing', desc: 'bKash micro-transfers aggregated into Tanvir mule account' },
    { step: 2, label: '08:16 UTC', title: 'Phase 2: RTGS Layering', desc: 'Interbank layering burst: $47,600 RTGS into Meghna Industrial' },
    { step: 3, label: '08:22 UTC', title: 'Phase 3: Cross-Border Outflow', desc: 'SWIFT wire transferred to Gulf Star Commodities (Dubai JAFZA)' },
    { step: 4, label: '08:35 UTC', title: 'Phase 4: Cycle-3 Wash Return', desc: 'Documentary LC over-invoiced round-trip completes full wash ring' }
  ];

  // Initialize and Update Cytoscape Instance
  useEffect(() => {
    if (!containerRef.current) return;

    const cy = cytoscape({
      container: containerRef.current,
      elements: visibleElements,
      style: [
        {
          selector: 'node',
          style: {
            'label': 'data(label)',
            'font-size': '8.5px',
            'font-family': 'Inter, sans-serif',
            'font-weight': 600,
            'color': '#334155',
            'text-valign': 'bottom',
            'text-margin-y': 6,
            'text-wrap': 'wrap',
            'text-max-width': '95px',
            'background-color': '#FFFFFF',
            'border-width': 2,
            'border-color': '#E2E8F0',
            'width': 30,
            'height': 30,
            'min-zoomed-font-size': 7,
            'transition-property': 'background-color, border-color, width, height, opacity',
            'transition-duration': '0.25s'
          }
        },
        {
          selector: 'node[tierCode = 1]',
          style: {
            'background-color': '#FEF2F2',
            'border-color': '#EF4444',
            'color': '#B91C1C',
            'width': 34,
            'height': 34
          }
        },
        {
          selector: 'node[tierCode = 2]',
          style: {
            'background-color': '#FFFBEB',
            'border-color': '#F59E0B',
            'color': '#B45309',
            'width': 30,
            'height': 30
          }
        },
        {
          selector: 'node[tierCode = 3]',
          style: {
            'background-color': '#F0FDF4',
            'border-color': '#22C55E',
            'color': '#15803D'
          }
        },
        {
          selector: 'node[?isCamouflageNode]',
          style: {
            'background-color': '#F8FAFC',
            'border-color': '#CBD5E1',
            'color': '#64748B',
            'width': 22,
            'height': 22,
            'font-size': '7.5px'
          }
        },
        {
          selector: '.pruned-node',
          style: {
            'opacity': 0.18
          }
        },
        {
          selector: '.dimmed-temporal',
          style: {
            'opacity': 0.25
          }
        },
        {
          selector: '.active-temporal-node',
          style: {
            'border-width': 3.5,
            'border-color': '#EF4444',
            'underlay-color': '#EF4444',
            'underlay-padding': 6,
            'underlay-opacity': 0.35
          }
        },
        {
          selector: 'node:selected',
          style: {
            'border-width': 3.5,
            'border-color': '#2563EB',
            'border-opacity': 1,
            'underlay-color': '#2563EB',
            'underlay-padding': 5,
            'underlay-opacity': 0.25
          }
        },
        // Edge styling with Collision-Prevention & Occlusion Culling
        {
          selector: 'edge',
          style: {
            'width': 1.8,
            'line-color': '#CBD5E1',
            'target-arrow-color': '#94A3B8',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'arrow-scale': 0.85,
            'label': 'data(label)',
            'font-size': '8px',
            'font-family': 'JetBrains Mono, monospace',
            'font-weight': 600,
            'text-background-opacity': 0.95,
            'text-background-color': '#FFFFFF',
            'text-background-padding': '3px',
            'text-background-shape': 'roundrectangle',
            'text-border-width': 1,
            'text-border-color': '#E2E8F0',
            'text-border-opacity': 0.8,
            'edge-text-rotation': 'autorotate',
            'min-zoomed-font-size': 7,
            'color': '#475569',
            'transition-property': 'line-color, opacity, width, line-style',
            'transition-duration': '0.25s'
          }
        },
        {
          selector: 'edge[?isLoop]',
          style: {
            'line-color': '#EF4444',
            'target-arrow-color': '#EF4444',
            'width': 2.8,
            'font-weight': 700,
            'color': '#B91C1C',
            'text-border-color': '#FECACA'
          }
        },
        {
          selector: '.pruned-edge',
          style: {
            'line-color': '#E2E8F0',
            'target-arrow-color': '#E2E8F0',
            'line-style': 'dashed',
            'opacity': 0.15,
            'width': 1,
            'label': ''
          }
        },
        {
          selector: '.active-temporal-edge',
          style: {
            'line-color': '#EF4444',
            'target-arrow-color': '#EF4444',
            'width': 4.0,
            'opacity': 1.0,
            'font-weight': 800,
            'color': '#DC2626',
            'text-background-color': '#FEF2F2',
            'text-border-color': '#EF4444'
          }
        },
        {
          selector: '.dimmed-temporal-edge',
          style: {
            'opacity': 0.15
          }
        },
        {
          selector: '.highlighted-path',
          style: {
            'line-color': '#2563EB',
            'target-arrow-color': '#2563EB',
            'width': 3.5,
            'transition-duration': '0.2s'
          }
        },
        {
          selector: '.highlighted-node',
          style: {
            'border-color': '#2563EB',
            'border-width': 3.5
          }
        }
      ],
      layout: {
        name: 'cose',
        animate: false,
        nodeRepulsion: 22000, // Barnes-Hut charge repulsion preventing dense hub overlap
        idealEdgeLength: 150,
        nodeOverlap: 40,
        componentSpacing: 110,
        edgeElasticity: 100,
        nestingFactor: 1.2,
        gravity: 0.22,
        numIter: 1000,
        nodeDimensionsIncludeLabels: true
      }
    });

    cy.on('tap', 'node', (evt) => {
      const node = evt.target;
      const nodeData = node.data();
      setSelectedGraphNode(nodeData);
      openDrawer({
        account: nodeData.id,
        entityName: nodeData.label,
        tier: nodeData.tier,
        tierCode: nodeData.tierCode,
        amount: nodeData.amount,
        riskScore: nodeData.riskScore,
        whyFlagged: nodeData.isCamouflageNode 
          ? 'Peripheral retail POS merchant connected to suspected mule account.' 
          : `Entity exhibiting topology cluster signatures (${nodeData.role}) with multi-hop connectivity.`
      });
      if (onNodeSelect) onNodeSelect(nodeData);
    });

    cyRef.current = cy;

    return () => {
      if (cyRef.current) {
        try {
          cy.stop();
          cy.destroy();
        } catch (e) {
          // ignore cleanup errors during unmount
        }
        cyRef.current = null;
      }
    };
  }, [visibleElements]);

  // Update Cytoscape styles dynamically when camouflage gating changes
  useEffect(() => {
    if (!cyRef.current) return;
    const cy = cyRef.current;

    cy.edges().forEach((edge) => {
      const data = edge.data();
      if (data.isCamouflage && (camouflageGatingEnabled || camouflageDelta >= 0.04)) {
        edge.addClass('pruned-edge');
      } else {
        edge.removeClass('pruned-edge');
      }
    });

    cy.nodes('[?isCamouflageNode]').forEach((node) => {
      if (camouflageGatingEnabled || camouflageDelta >= 0.04) {
        node.addClass('pruned-node');
      } else {
        node.removeClass('pruned-node');
      }
    });
  }, [camouflageDelta, camouflageGatingEnabled]);

  // Update Cytoscape styles dynamically when timeline step changes
  useEffect(() => {
    if (!cyRef.current) return;
    const cy = cyRef.current;

    if (timelineStep === 0) {
      // Show full baseline
      cy.elements().removeClass('dimmed-temporal active-temporal-node dimmed-temporal-edge active-temporal-edge');
    } else {
      // Step-by-step sequential animation
      cy.edges().forEach((edge) => {
        const edgeStep = edge.data('timeStep');
        if (edgeStep === timelineStep) {
          edge.addClass('active-temporal-edge');
          edge.removeClass('dimmed-temporal-edge');
        } else if (edgeStep < timelineStep) {
          edge.removeClass('active-temporal-edge dimmed-temporal-edge');
        } else {
          edge.addClass('dimmed-temporal-edge');
          edge.removeClass('active-temporal-edge');
        }
      });

      cy.nodes().forEach((node) => {
        const nodeStep = node.data('timeStep');
        if (nodeStep === timelineStep) {
          node.addClass('active-temporal-node');
          node.removeClass('dimmed-temporal');
        } else if (nodeStep <= timelineStep) {
          node.removeClass('active-temporal-node dimmed-temporal');
        } else {
          node.addClass('dimmed-temporal');
          node.removeClass('active-temporal-node');
        }
      });
    }
  }, [timelineStep]);

  // Continuous Timeline Playback Timer
  useEffect(() => {
    if (isPlaying) {
      playTimerRef.current = setInterval(() => {
        setTimelineStep(prev => (prev >= 4 ? 0 : prev + 1));
      }, 1600);
    } else {
      if (playTimerRef.current) clearInterval(playTimerRef.current);
    }
    return () => {
      if (playTimerRef.current) clearInterval(playTimerRef.current);
    };
  }, [isPlaying, setTimelineStep]);

  const handleFit = () => cyRef.current?.fit(undefined, 35);
  const handleZoomIn = () => cyRef.current?.zoom(cyRef.current.zoom() * 1.2);
  const handleZoomOut = () => cyRef.current?.zoom(cyRef.current.zoom() * 0.8);

  const handleFindPath = () => {
    if (!cyRef.current) return;
    cyRef.current.elements().removeClass('highlighted-path highlighted-node');

    const sourceNode = cyRef.current.$(`node[id = "${pathSource}"]`);
    const targetNode = cyRef.current.$(`node[id = "${pathTarget}"]`);

    if (sourceNode.length && targetNode.length) {
      const dijkstra = cyRef.current.elements().dijkstra(sourceNode);
      const pathToTarget = dijkstra.pathTo(targetNode);

      if (pathToTarget.length > 0) {
        pathToTarget.addClass('highlighted-path');
        pathToTarget.nodes().addClass('highlighted-node');
        setIsPathFound(true);
      } else {
        setIsPathFound(false);
      }
    }
  };

  const handleExportPNG = () => {
    if (!cyRef.current) return;
    const png64 = cyRef.current.png({ full: true, quality: 1, scale: 2 });
    const downloadLink = document.createElement('a');
    downloadLink.href = png64;
    downloadLink.download = `AML_Forensic_Network_${Date.now()}.png`;
    downloadLink.click();
  };

  const currentStepMeta = TIMELINE_STEPS.find(s => s.step === timelineStep) || TIMELINE_STEPS[0];

  return (
    <div className="relative w-full h-[620px] sm:h-[680px] bg-surface rounded-lg border border-border overflow-hidden flex flex-col justify-between select-none">
      {/* Top Controls Toolbar: Radial Expansion, Max Node Cap, Path Finding */}
      <div className="p-3 border-b border-border bg-surfaceRaised flex flex-wrap items-center justify-between gap-2.5 z-10 text-xs">
        {/* Left: Ego Hop & Radial Expansion */}
        <div className="flex items-center gap-2 flex-wrap">
          <span className="font-semibold text-text">Ego Neighborhood:</span>
          <div className="flex items-center gap-1 font-mono text-[11px] p-0.5 bg-bg rounded border border-border">
            {[1, 2, 3].map(h => (
              <button
                key={h}
                onClick={() => setEgoHopDistance(h)}
                className={`px-2 py-0.5 rounded transition-colors cursor-pointer ${
                  egoHopDistance === h 
                    ? 'bg-surfaceRaised font-bold text-accent shadow-xs' 
                    : 'text-text-muted hover:text-text'
                }`}
              >
                {h}-Hop
              </button>
            ))}
          </div>

          <div className="w-px h-3.5 bg-border mx-1" />

          {/* Max Visible Entities Slider Cap (WebGL/DOM Protection) */}
          <div className="flex items-center gap-1.5 font-mono text-[11px]">
            <label htmlFor="graph-entity-cap-slider" className="text-text-muted cursor-pointer">Entity Cap:</label>
            <input 
              id="graph-entity-cap-slider"
              name="graph-entity-cap-slider"
              type="range"
              min="8"
              max="30"
              step="2"
              value={maxVisibleNodes}
              onChange={(e) => setMaxVisibleNodes(Number(e.target.value))}
              className="w-16 sm:w-20 h-1.5 bg-border rounded-lg appearance-none cursor-pointer accent-accent"
              title="Cap visible entities to protect frame rate"
            />
            <span className="font-bold text-text">{maxVisibleNodes}</span>
          </div>

          {/* Camouflage Edge Gating Toggle */}
          <div className="w-px h-3.5 bg-border mx-1" />
          <button
            onClick={() => setCamouflageGatingEnabled(!camouflageGatingEnabled)}
            className={`flex items-center gap-1.5 px-2 py-0.5 rounded border text-[11px] font-mono transition-colors cursor-pointer ${
              camouflageGatingEnabled 
                ? 'bg-cleared-bg text-cleared border-cleared font-semibold' 
                : 'bg-bg text-text-muted border-border hover:text-text'
            }`}
            title="Toggle learned edge-trust gating threshold (g_ij < 0.10)"
          >
            {camouflageGatingEnabled ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
            <span>Gate Chaff (g &lt; 0.10)</span>
          </button>
        </div>

        {/* Right: Path Finding Controls */}
        <div className="flex items-center gap-1.5 flex-wrap">
          <label htmlFor="graph-path-source-select" className="text-text-muted text-[11px] font-mono flex items-center gap-1 cursor-pointer">
            <Route className="w-3.5 h-3.5 text-accent" />
            <span>Trace:</span>
          </label>
          <select
            id="graph-path-source-select"
            name="graph-path-source-select"
            value={pathSource}
            onChange={(e) => setPathSource(e.target.value)}
            className="ui-input py-0.5 text-[11px] font-mono h-7 max-w-[130px] truncate"
          >
            <option value="BD22-EBLB-4829-1092-8823">Meghna Industrial</option>
            <option value="BD04-BRAC-1109-8421-4402">Tanvir Rahman</option>
            <option value="MFS-BKASH-0171-8840">Rafiqul (bKash)</option>
          </select>
          <ArrowRight className="w-3 h-3 text-text-muted" />
          <select
            id="graph-path-target-select"
            name="graph-path-target-select"
            value={pathTarget}
            onChange={(e) => setPathTarget(e.target.value)}
            className="ui-input py-0.5 text-[11px] font-mono h-7 max-w-[130px] truncate"
          >
            <option value="BD04-BRAC-1109-8421-4402">Tanvir Rahman</option>
            <option value="AE-EBIL-4412-8819-3301">Gulf Star (Dubai)</option>
            <option value="GB-BARC-1109-8421-4402">Anglo-Bengal (UK)</option>
          </select>
          <Button
            variant="secondary"
            size="sm"
            onClick={handleFindPath}
            className="text-xs h-7"
          >
            Find Path
          </Button>
        </div>
      </div>

      {/* Main Graph Viewport */}
      <div ref={containerRef} className="w-full flex-1 relative cursor-grab active:cursor-grabbing bg-bg" />

      {/* Temporal Timeline Scrubber Playback Bar */}
      <div className="p-3 border-t border-border bg-surfaceRaised/95 backdrop-blur-xs flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 z-10">
        {/* Playback Controls & Slider */}
        <div className="flex items-center gap-3 flex-1 min-w-0">
          {/* Play/Pause & Step Buttons */}
          <div className="flex items-center gap-1 shrink-0">
            <button
              onClick={() => setTimelineStep(prev => Math.max(0, prev - 1))}
              className="p-1.5 rounded hover:bg-surface text-text-2 hover:text-text border border-border cursor-pointer transition-colors"
              title="Step Backward (Δt - 1)"
            >
              <SkipBack className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className="p-1.5 rounded bg-accent text-white hover:bg-accent/90 cursor-pointer transition-colors shadow-xs"
              title={isPlaying ? 'Pause Playback' : 'Play Transaction Flow Sequence'}
            >
              {isPlaying ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
            </button>
            <button
              onClick={() => setTimelineStep(prev => Math.min(4, prev + 1))}
              className="p-1.5 rounded hover:bg-surface text-text-2 hover:text-text border border-border cursor-pointer transition-colors"
              title="Step Forward (Δt + 1)"
            >
              <SkipForward className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => { setIsPlaying(false); setTimelineStep(0); }}
              className="p-1.5 rounded hover:bg-surface text-text-muted hover:text-text border border-border cursor-pointer transition-colors"
              title="Reset Timeline to Baseline"
            >
              <RotateCcw className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Continuous-Time Range Slider */}
          <div className="flex-1 flex flex-col gap-1 min-w-[140px]">
            <input
              id="graph-timeline-playback-slider"
              name="graph-timeline-playback-slider"
              aria-label="Transaction playback timeline scrubber"
              type="range"
              min="0"
              max="4"
              step="1"
              value={timelineStep}
              onChange={(e) => {
                setIsPlaying(false);
                setTimelineStep(Number(e.target.value));
              }}
              className="w-full h-1.5 bg-border rounded-lg appearance-none cursor-pointer accent-accent"
            />
            {/* Step Markers */}
            <div className="flex justify-between text-[9px] font-mono text-text-muted">
              <span>t=0</span>
              <span>t₁ (Smurf)</span>
              <span>t₂ (Layer)</span>
              <span>t₃ (Outflow)</span>
              <span>t₄ (Loop)</span>
            </div>
          </div>
        </div>

        {/* Current Stage Indicator Banner */}
        <div className="flex items-center gap-2.5 px-3 py-1.5 rounded bg-bg border border-borderSubtle text-xs shrink-0 font-mono">
          <Clock className="w-3.5 h-3.5 text-accent animate-pulse" />
          <div>
            <div className="flex items-center gap-1.5">
              <span className="font-bold text-text">{currentStepMeta.label}:</span>
              <span className="text-accent font-semibold">{currentStepMeta.title}</span>
            </div>
            <span className="text-[10px] text-text-muted truncate max-w-[260px] block">
              {currentStepMeta.desc}
            </span>
          </div>
        </div>
      </div>

      {/* Floating Canvas Action Bar (Zoom, Fit, Export) */}
      <div className="absolute top-16 right-3 flex items-center gap-1.5 bg-surface border border-border shadow-md rounded p-1 z-10">
        <Button variant="ghost" size="icon" onClick={handleZoomIn} title="Zoom In">
          <ZoomIn className="w-4 h-4 text-text-2" />
        </Button>
        <Button variant="ghost" size="icon" onClick={handleZoomOut} title="Zoom Out">
          <ZoomOut className="w-4 h-4 text-text-2" />
        </Button>
        <Button variant="ghost" size="icon" onClick={handleFit} title="Fit to View">
          <Maximize2 className="w-4 h-4 text-text-2" />
        </Button>
        <div className="w-px h-4 bg-border mx-0.5" />
        <Button variant="ghost" size="icon" onClick={handleExportPNG} title="Export PNG">
          <Download className="w-4 h-4 text-text-2" />
        </Button>
      </div>

      {/* Floating Minimal Legend */}
      <div className="absolute bottom-20 left-3 bg-surface/95 backdrop-blur-xs border border-border shadow-sm rounded p-2 z-10 text-[10px] space-y-1 font-mono">
        <span className="font-semibold text-text text-[9px] uppercase tracking-wider block">Topology Tiers</span>
        <div className="flex items-center gap-2 text-text-2">
          <span className="w-2 h-2 rounded-full bg-critical border border-critical inline-block" />
          <span>Tier 1 Hold (&gt;85% Risk)</span>
        </div>
        <div className="flex items-center gap-2 text-text-2">
          <span className="w-2 h-2 rounded-full bg-review border border-review inline-block" />
          <span>Tier 2 Review Queue</span>
        </div>
        <div className="flex items-center gap-2 text-text-2">
          <span className="w-2 h-2 rounded-full bg-cleared border border-cleared inline-block" />
          <span>Tier 3 Straight-Through</span>
        </div>
      </div>
    </div>
  );
};
