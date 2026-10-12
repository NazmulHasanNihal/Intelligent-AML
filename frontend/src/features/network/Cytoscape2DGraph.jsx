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
  Sparkles,
  Zap,
  Repeat,
  Crosshair,
  Activity,
  AlertTriangle
} from 'lucide-react';
import { useAppStore } from '../../lib/store';
import { evaluateEdgeTrust } from '../../lib/scoringEngine';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';

const getLayoutConfig = (mode) => {
  if (mode === 'sugiyama') {
    return {
      name: 'breadthfirst',
      directed: true,
      roots: ['BD22-EBLB-4829-1092-8823', 'MFS-BKASH-0171-8840'],
      padding: 24,
      spacingFactor: 1.1,
      animate: false
    };
  }
  if (mode === 'orbital') {
    return {
      name: 'concentric',
      concentric: (node) => {
        const tier = node.data('tierCode') || 3;
        return 4 - tier; // Tier 1 center (3), Tier 2 middle (2), Tier 3 outer (1)
      },
      levelWidth: () => 1,
      padding: 24,
      animate: false
    };
  }
  if (mode === 'circle') {
    return {
      name: 'circle',
      padding: 24,
      animate: false
    };
  }
  return {
    name: 'cose',
    animate: false,
    nodeRepulsion: 20000,
    idealEdgeLength: 140,
    nodeOverlap: 35,
    componentSpacing: 100,
    edgeElasticity: 100,
    nestingFactor: 1.2,
    gravity: 0.22,
    numIter: 1000,
    nodeDimensionsIncludeLabels: true
  };
};

export const Cytoscape2DGraph = ({
  onNodeSelect,
  layoutMode: externalLayoutMode = 'sugiyama',
  onLayoutChange,
  selectedNodeId,
  showTopControls = true,
  externalCamouflageDelta,
  className
}) => {
  const containerRef = useRef(null);
  const animCanvasRef = useRef(null);
  const animFrameRef = useRef(null);
  const cyRef = useRef(null);
  const [internalLayout, setInternalLayout] = useState('sugiyama');
  const activeLayout = externalLayoutMode || internalLayout;

  const handleLayoutSwitch = (mode) => {
    setInternalLayout(mode);
    if (onLayoutChange) onLayoutChange(mode);
  };
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

  const effectiveCamouflageDelta = externalCamouflageDelta !== undefined ? externalCamouflageDelta : camouflageDelta;

  const [pathSource, setPathSource] = useState('BD22-EBLB-4829-1092-8823');
  const [pathTarget, setPathTarget] = useState('BD04-BRAC-1109-8421-4402');
  const [isPathFound, setIsPathFound] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(1); // 0.5x, 1x, 2x
  const [playbackMode, setPlaybackMode] = useState('cumulative'); // 'cumulative' | 'single'
  const [autoLoop, setAutoLoop] = useState(true);
  const [trackCamera, setTrackCamera] = useState(false);
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

  // Timeline Step Metadata with Full Forensic Flow Profiles
  const TIMELINE_STEPS = [
    {
      step: 0,
      label: '08:00 UTC',
      title: 'Quiescent Baseline',
      desc: 'All interbank corridors operating within normal Poisson intensity baseline. Zero invariant alerts.',
      activeTx: null
    },
    {
      step: 1,
      label: '08:14 UTC',
      title: 'Phase 1: MFS Smurfing Inflow',
      desc: 'bKash micro-transfers aggregated from MFS retail agents into Tanvir mule account to evade single-ticket CTR thresholds.',
      activeTx: {
        edgeId: 'e6',
        sourceId: 'MFS-BKASH-0171-8840',
        targetId: 'BD04-BRAC-1109-8421-4402',
        sourceName: 'Mohammad Rafiqul Islam (MFS)',
        targetName: 'Tanvir Ahmed Rahman (Conduit)',
        amount: '$4,800.00 USD',
        amountBdt: '৳576,000 BDT',
        rail: 'bKash MFS',
        typology: 'Sub-CTR Smurfing',
        conformalSet: 'Tier 1 Hold (High Risk)',
        hawkes: 'Velocity: 4.8 tx/min (Spike)',
        color: '#F59E0B'
      }
    },
    {
      step: 2,
      label: '08:16 UTC',
      title: 'Phase 2: RTGS Layering Injection',
      desc: 'Corporate treasury executes $47,600 high-speed interbank RTGS transfer into conduit aggregator within 120 seconds.',
      activeTx: {
        edgeId: 'e3',
        sourceId: 'BD22-EBLB-4829-1092-8823',
        targetId: 'BD04-BRAC-1109-8421-4402',
        sourceName: 'Meghna Industrial & Agro (Hub)',
        targetName: 'Tanvir Ahmed Rahman (Conduit)',
        amount: '$47,600.00 USD',
        amountBdt: '৳5,712,000 BDT',
        rail: 'RTGS (BD Bank)',
        typology: 'Interbank Rapid Layering',
        conformalSet: 'Tier 1 Hold (High Risk)',
        hawkes: 'Velocity: 9.1 tx/min (Critical)',
        color: '#EF4444'
      }
    },
    {
      step: 3,
      label: '08:22 UTC',
      title: 'Phase 3: Cross-Border SWIFT Outflow',
      desc: 'Layered funds wired to JAFZA Free Zone shell entity in Dubai via international telegraphic wire to obscure ownership.',
      activeTx: {
        edgeId: 'e4',
        sourceId: 'BD04-BRAC-1109-8421-4402',
        targetId: 'AE-EBIL-4412-8819-3301',
        sourceName: 'Tanvir Ahmed Rahman (Conduit)',
        targetName: 'Gulf Star Commodities (Dubai)',
        amount: '$47,600.00 USD',
        amountBdt: '৳5,712,000 BDT',
        rail: 'SWIFT MT103',
        typology: 'Offshore Capital Flight',
        conformalSet: 'Tier 1 Hold (High Risk)',
        hawkes: 'Velocity: 11.2 tx/min (High)',
        color: '#EC4899'
      }
    },
    {
      step: 4,
      label: '08:35 UTC',
      title: 'Phase 4: Cycle-3 Trade Wash Return',
      desc: 'Documentary credit import settlement under over-invoiced trade bills completes full circular wash ring back to origin hub.',
      activeTx: {
        edgeId: 'e5',
        sourceId: 'AE-EBIL-4412-8819-3301',
        targetId: 'BD22-EBLB-4829-1092-8823',
        sourceName: 'Gulf Star Commodities (Dubai)',
        targetName: 'Meghna Industrial & Agro (Hub)',
        amount: '$47,600.00 USD',
        amountBdt: '৳5,712,000 BDT',
        rail: 'SWIFT MT700 (LC)',
        typology: 'TBML Circular Wash Loop',
        conformalSet: 'Tier 1 Hold (High Risk)',
        hawkes: 'Velocity: 14.8 tx/min (Ring Closed)',
        color: '#8B5CF6'
      }
    }
  ];

  // Current Timeline Step Meta hoisted above hooks to eliminate TDZ ReferenceErrors
  const currentStepMeta = useMemo(() => {
    return TIMELINE_STEPS.find(s => s.step === timelineStep) || TIMELINE_STEPS[0];
  }, [timelineStep]);

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
          selector: '.completed-temporal-edge',
          style: {
            'line-color': '#F87171',
            'target-arrow-color': '#EF4444',
            'width': 3.2,
            'opacity': 0.88,
            'font-weight': 700,
            'color': '#B91C1C',
            'text-background-opacity': 0.95,
            'text-background-color': '#FEF2F2',
            'text-border-color': '#FCA5A5',
            'text-border-width': 1
          }
        },
        {
          selector: '.active-temporal-edge',
          style: {
            'line-color': '#EF4444',
            'target-arrow-color': '#EF4444',
            'width': 4.5,
            'opacity': 1.0,
            'font-weight': 800,
            'color': '#DC2626',
            'text-background-color': '#FEF2F2',
            'text-border-color': '#EF4444',
            'text-border-width': 1.5,
            'line-style': 'dashed',
            'line-dash-pattern': [8, 4],
            'z-index': 99
          }
        },
        {
          selector: '.active-sender-node',
          style: {
            'border-width': 4,
            'border-color': '#F59E0B',
            'underlay-color': '#F59E0B',
            'underlay-padding': 8,
            'underlay-opacity': 0.35,
            'z-index': 100
          }
        },
        {
          selector: '.active-receiver-node',
          style: {
            'border-width': 4,
            'border-color': '#EF4444',
            'underlay-color': '#EF4444',
            'underlay-padding': 10,
            'underlay-opacity': 0.45,
            'z-index': 100
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
      layout: getLayoutConfig(activeLayout)
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
    setTimeout(() => {
      if (cyRef.current) cyRef.current.fit(undefined, 25);
    }, 150);

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

  // Dynamic layout engine switching with smooth animated transition
  useEffect(() => {
    if (!cyRef.current) return;
    const cy = cyRef.current;
    const config = { ...getLayoutConfig(activeLayout), animate: true, animationDuration: 400 };
    try {
      cy.layout(config).run();
      setTimeout(() => {
        if (cyRef.current) cyRef.current.fit(undefined, 25);
      }, 420);
    } catch (e) {
      console.warn('Cytoscape layout update error:', e);
    }
  }, [activeLayout]);

  // Sync external selectedNodeId
  useEffect(() => {
    if (!cyRef.current) return;
    const cy = cyRef.current;
    cy.nodes().unselect();
    if (selectedNodeId) {
      const match = cy.$(`node[id = "${selectedNodeId}"]`);
      if (match.length > 0) {
        match.select();
      }
    }
  }, [selectedNodeId]);

  // Update Cytoscape styles dynamically when camouflage gating changes
  useEffect(() => {
    if (!cyRef.current) return;
    const cy = cyRef.current;

    cy.edges().forEach((edge) => {
      const data = edge.data();
      if (data.isCamouflage && (camouflageGatingEnabled || effectiveCamouflageDelta >= 0.04)) {
        edge.addClass('pruned-edge');
      } else {
        edge.removeClass('pruned-edge');
      }
    });

    cy.nodes('[?isCamouflageNode]').forEach((node) => {
      if (camouflageGatingEnabled || effectiveCamouflageDelta >= 0.04) {
        node.addClass('pruned-node');
      } else {
        node.removeClass('pruned-node');
      }
    });
  }, [effectiveCamouflageDelta, camouflageGatingEnabled]);

  // Update Cytoscape styles dynamically when timeline step changes
  useEffect(() => {
    if (!cyRef.current) return;
    const cy = cyRef.current;
    const activeTx = currentStepMeta?.activeTx;

    if (timelineStep === 0) {
      // Show full baseline
      cy.elements().removeClass('dimmed-temporal active-temporal-node dimmed-temporal-edge active-temporal-edge completed-temporal-edge active-sender-node active-receiver-node');
    } else {
      // Step-by-step or cumulative sequential animation
      cy.edges().forEach((edge) => {
        const edgeStep = edge.data('timeStep');
        edge.removeClass('active-temporal-edge dimmed-temporal-edge completed-temporal-edge');

        if (edgeStep === timelineStep) {
          edge.addClass('active-temporal-edge');
        } else if (edgeStep < timelineStep && edgeStep > 0) {
          if (playbackMode === 'cumulative') {
            edge.addClass('completed-temporal-edge');
          } else {
            edge.addClass('dimmed-temporal-edge');
          }
        } else {
          edge.addClass('dimmed-temporal-edge');
        }
      });

      cy.nodes().forEach((node) => {
        const nodeId = node.data('id');
        const isActiveSender = activeTx && activeTx.sourceId === nodeId;
        const isActiveReceiver = activeTx && activeTx.targetId === nodeId;

        node.removeClass('dimmed-temporal active-temporal-node active-sender-node active-receiver-node');

        if (isActiveSender) {
          node.addClass('active-sender-node active-temporal-node');
        } else if (isActiveReceiver) {
          node.addClass('active-receiver-node active-temporal-node');
        } else {
          const nodeStep = node.data('timeStep');
          if (playbackMode === 'cumulative' && nodeStep !== undefined && nodeStep <= timelineStep && nodeStep > 0) {
            // Keep completed nodes illuminated in cumulative mode
          } else if (nodeStep !== timelineStep) {
            node.addClass('dimmed-temporal');
          }
        }
      });

      // Camera auto-tracking if enabled
      if (trackCamera && activeTx) {
        const activeNodes = cy.$(`node[id = "${activeTx.sourceId}"], node[id = "${activeTx.targetId}"]`);
        if (activeNodes.length > 0) {
          cy.animate({
            fit: { eles: activeNodes, padding: 100 },
            duration: 400
          });
        }
      }
    }
  }, [timelineStep, playbackMode, currentStepMeta, trackCamera]);

  // Continuous Timeline Playback Timer with Speed & Auto-Loop Controls
  const timelineStepRef = useRef(timelineStep);
  useEffect(() => {
    timelineStepRef.current = timelineStep;
  }, [timelineStep]);

  useEffect(() => {
    if (isPlaying) {
      const stepDuration = Math.round(2400 / playbackSpeed);
      if (playTimerRef.current) clearInterval(playTimerRef.current);
      playTimerRef.current = setInterval(() => {
        const cur = typeof timelineStepRef.current === 'number' ? timelineStepRef.current : 0;
        let next = cur + 1;
        if (cur >= 4) {
          if (!autoLoop) {
            setIsPlaying(false);
            return;
          }
          next = 0; // Return to t0 (quiescent baseline) so the complete money trail restarts smoothly
        }
        timelineStepRef.current = next;
        setTimelineStep(next);
      }, stepDuration);
    } else {
      if (playTimerRef.current) clearInterval(playTimerRef.current);
    }
    return () => {
      if (playTimerRef.current) clearInterval(playTimerRef.current);
    };
  }, [isPlaying, playbackSpeed, autoLoop, setTimelineStep]);

  // 60FPS High-Definition Canvas Particle Flow & Packet Animation Engine
  useEffect(() => {
    const canvas = animCanvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let isRunning = true;
    const startTime = performance.now();

    const handleResize = () => {
      if (!canvas || !containerRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      canvas.style.width = `${rect.width}px`;
      canvas.style.height = `${rect.height}px`;
      if (cyRef.current) {
        cyRef.current.resize();
      }
    };

    handleResize();
    let resizeObserver = null;
    if (typeof ResizeObserver !== 'undefined' && containerRef.current) {
      resizeObserver = new ResizeObserver(() => {
        handleResize();
      });
      resizeObserver.observe(containerRef.current);
    }
    window.addEventListener('resize', handleResize);

    const renderAnim = (now) => {
      if (!isRunning) return;

      const dpr = window.devicePixelRatio || 1;
      const width = canvas.width / dpr;
      const height = canvas.height / dpr;

      ctx.save();
      ctx.scale(dpr, dpr);
      ctx.clearRect(0, 0, width, height);

      const cy = cyRef.current;
      const activeTx = currentStepMeta?.activeTx;

      // 0. Legitimate Baseline Flow Animation at t0 (Soft Green Pulses on Verifiable Corridors)
      if (cy && timelineStep === 0) {
        const baseEdges = cy.$('edge[id = "e7"], edge[id = "e8"]');
        baseEdges.forEach((edge) => {
          const src = edge.source();
          const tgt = edge.target();
          if (src.length > 0 && tgt.length > 0 && src.visible() && tgt.visible()) {
            const sPos = src.renderedPosition();
            const tPos = tgt.renderedPosition();
            const dx = tPos.x - sPos.x;
            const dy = tPos.y - sPos.y;
            const dist = Math.hypot(dx, dy);
            if (dist > 5) {
              const elapsed = now - startTime;
              const p = (elapsed % (2200 / playbackSpeed)) / (2200 / playbackSpeed);
              const curX = sPos.x + dx * p;
              const curY = sPos.y + dy * p;

              ctx.beginPath();
              ctx.arc(curX, curY, 3.5, 0, Math.PI * 2);
              ctx.fillStyle = '#22C55E';
              ctx.shadowColor = '#22C55E';
              ctx.shadowBlur = 8;
              ctx.fill();
              ctx.shadowBlur = 0;
            }
          }
        });
      }

      if (cy && activeTx && timelineStep > 0) {
        const srcNode = cy.$(`node[id = "${activeTx.sourceId}"]`);
        const tgtNode = cy.$(`node[id = "${activeTx.targetId}"]`);

        if (srcNode.length > 0 && tgtNode.length > 0 && srcNode.visible() && tgtNode.visible()) {
          const srcPos = srcNode.renderedPosition();
          const tgtPos = tgtNode.renderedPosition();

          const dx = tgtPos.x - srcPos.x;
          const dy = tgtPos.y - srcPos.y;
          const dist = Math.hypot(dx, dy);

          if (dist > 5) {
            const nx = -dy / dist;
            const ny = dx / dist;

            // Travel speed: cycle repeats smoothly
            const cycleDuration = 1200 / playbackSpeed;
            const elapsed = now - startTime;
            const cycleProgress = (elapsed % cycleDuration) / cycleDuration;

            // 1. Source Node Emitting Shockwave
            const srcPulse = (elapsed % 1500) / 1500;
            ctx.beginPath();
            ctx.arc(srcPos.x, srcPos.y, 16 + srcPulse * 26, 0, Math.PI * 2);
            ctx.strokeStyle = `rgba(245, 158, 11, ${Math.max(0, 0.7 - srcPulse)})`;
            ctx.lineWidth = 2;
            ctx.stroke();

            // 2. Target Node Arrival Shockwave
            const tgtPulse = ((elapsed + 750) % 1500) / 1500;
            ctx.beginPath();
            ctx.arc(tgtPos.x, tgtPos.y, 18 + tgtPulse * 30, 0, Math.PI * 2);
            ctx.strokeStyle = `rgba(239, 68, 68, ${Math.max(0, 0.8 - tgtPulse)})`;
            ctx.lineWidth = 2.5;
            ctx.stroke();

            // 3. Animated Travelling Monetary Packets (3 staggered packets with comet tails)
            const packetOffsets = [0, 0.35, 0.70];
            packetOffsets.forEach((offset, idx) => {
              const p = (cycleProgress + offset) % 1;
              const curX = srcPos.x + dx * p;
              const curY = srcPos.y + dy * p;

              // Arc deflection along curved edge
              const arcOffset = Math.sin(p * Math.PI) * (dist * 0.12);
              const px = curX + nx * arcOffset;
              const py = curY + ny * arcOffset;

              // Comet particle tail (4 trailing points)
              for (let t = 1; t <= 4; t++) {
                const tailP = Math.max(0, p - t * 0.03);
                const tailCurX = srcPos.x + dx * tailP;
                const tailCurY = srcPos.y + dy * tailP;
                const tailArc = Math.sin(tailP * Math.PI) * (dist * 0.12);
                const txX = tailCurX + nx * tailArc;
                const txY = tailCurY + ny * tailArc;

                ctx.beginPath();
                ctx.arc(txX, txY, Math.max(1, 4.5 - t), 0, Math.PI * 2);
                ctx.fillStyle = activeTx.color
                  ? `${activeTx.color}${Math.floor((0.35 / t) * 255).toString(16).padStart(2, '0')}`
                  : 'rgba(239, 68, 68, 0.2)';
                ctx.fill();
              }

              // Glowing outer halo
              const halo = ctx.createRadialGradient(px, py, 1, px, py, 11);
              halo.addColorStop(0, '#FFFFFF');
              halo.addColorStop(0.3, activeTx.color || '#EF4444');
              halo.addColorStop(1, 'rgba(0,0,0,0)');

              ctx.beginPath();
              ctx.arc(px, py, 11, 0, Math.PI * 2);
              ctx.fillStyle = halo;
              ctx.fill();

              // Central high-energy packet core
              ctx.beginPath();
              ctx.arc(px, py, 4.5, 0, Math.PI * 2);
              ctx.fillStyle = '#FFFFFF';
              ctx.shadowColor = activeTx.color || '#EF4444';
              ctx.shadowBlur = 10;
              ctx.fill();
              ctx.shadowBlur = 0;

              // Floating amount badge above lead packet
              if (idx === 0) {
                const badgeText = activeTx.amount;
                ctx.font = 'bold 9.5px "JetBrains Mono", monospace';
                const metrics = ctx.measureText(badgeText);
                const padX = 6;
                const badgeW = metrics.width + padX * 2;
                const badgeH = 17;
                const badgeX = px - badgeW / 2;
                const badgeY = py - 24;

                ctx.beginPath();
                if (typeof ctx.roundRect === 'function') {
                  ctx.roundRect(badgeX, badgeY, badgeW, badgeH, 4);
                } else {
                  ctx.rect(badgeX, badgeY, badgeW, badgeH);
                }
                ctx.fillStyle = 'rgba(15, 23, 42, 0.92)';
                ctx.fill();
                ctx.strokeStyle = activeTx.color || '#EF4444';
                ctx.lineWidth = 1.2;
                ctx.stroke();

                ctx.fillStyle = '#FFFFFF';
                ctx.fillText(badgeText, badgeX + padX, badgeY + 12);
              }
            });
          }
        }
      }

      ctx.restore();
      animFrameRef.current = requestAnimationFrame(renderAnim);
    };

    animFrameRef.current = requestAnimationFrame(renderAnim);

    return () => {
      isRunning = false;
      if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
      window.removeEventListener('resize', handleResize);
      if (resizeObserver) resizeObserver.disconnect();
    };
  }, [currentStepMeta, timelineStep, playbackSpeed]);

  const handleTogglePlay = () => {
    if (!isPlaying) {
      if (timelineStep >= 4) {
        setTimelineStep(0);
        timelineStepRef.current = 0;
      }
      setIsPlaying(true);
    } else {
      setIsPlaying(false);
    }
  };

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

  return (
    <div className={className || "relative w-full h-[450px] sm:h-[480px] bg-surface rounded-lg border border-border overflow-hidden flex flex-col justify-between select-none"}>
      {/* Top Controls Toolbar: Radial Expansion, Max Node Cap, Layout Switcher, Path Finding */}
      {showTopControls && (
        <div className="p-3 border-b border-border bg-surfaceRaised flex flex-wrap items-center justify-between gap-2.5 z-10 text-xs">
          {/* Left: Ego Hop, Radial Expansion & Layout Switcher */}
          <div className="flex items-center gap-2 flex-wrap">
            <span className="font-semibold text-text">Ego:</span>
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

            {/* Layout Mode Selector */}
            <div className="w-px h-3.5 bg-border mx-1" />
            <div className="flex items-center gap-0.5 font-mono text-[10px] p-0.5 bg-bg rounded border border-border">
              {[
                { id: 'sugiyama', label: 'Sugiyama' },
                { id: 'orbital', label: 'Orbital' },
                { id: 'cose', label: 'COSE' },
                { id: 'circle', label: 'Ring' }
              ].map(l => (
                <button
                  key={l.id}
                  onClick={() => handleLayoutSwitch(l.id)}
                  className={`px-1.5 py-0.5 rounded transition-colors cursor-pointer ${
                    activeLayout === l.id
                      ? 'bg-surfaceRaised font-bold text-accent shadow-xs'
                      : 'text-text-muted hover:text-text'
                  }`}
                  title={`Topology Layout: ${l.label}`}
                >
                  {l.label}
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
            title="Filter out low-value noise and irrelevant retail transactions (< $150)"
          >
            {camouflageGatingEnabled ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
            <span>Filter Low-Value Transfers (&lt; $150)</span>
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
      )}

      {/* Main Graph Viewport with 60FPS Canvas Animation Overlay */}
      <div className="w-full flex-1 relative bg-bg overflow-hidden">
        <div ref={containerRef} className="w-full h-full cursor-grab active:cursor-grabbing bg-bg" />
        <canvas
          ref={animCanvasRef}
          className="absolute inset-0 pointer-events-none z-10 w-full h-full"
        />

        {/* Live Transaction HUD Card */}
        {currentStepMeta && (
          <div className="absolute top-3 left-3 max-w-sm sm:max-w-md w-full z-20 pointer-events-auto transition-all duration-300">
            {timelineStep === 0 ? (
              <div className="p-3 rounded-lg bg-surface/90 backdrop-blur-md border border-border shadow-sm flex items-center justify-between gap-3 text-xs font-mono">
                <div className="flex items-center gap-2.5">
                  <span className="w-2.5 h-2.5 rounded-full bg-cleared animate-pulse" />
                  <div>
                    <span className="text-text font-semibold block">Baseline Topology (08:00 UTC)</span>
                    <span className="text-[10px] text-text-muted">Interbank settlement corridors quiescent</span>
                  </div>
                </div>
                <button
                  onClick={() => { timelineStepRef.current = 1; setTimelineStep(1); setIsPlaying(true); }}
                  className="px-2.5 py-1 rounded bg-accent text-white text-[11px] font-semibold hover:bg-accent/90 cursor-pointer flex items-center gap-1 shadow-xs transition-colors"
                >
                  <Play className="w-3 h-3" />
                  <span>Start Flow</span>
                </button>
              </div>
            ) : (
              <div className="p-3.5 rounded-lg bg-surface/95 backdrop-blur-md border border-border shadow-lg space-y-2.5 text-xs font-mono">
                {/* Header: Phase badge & timestamp */}
                <div className="flex items-center justify-between gap-2 border-b border-border/60 pb-2">
                  <div className="flex items-center gap-2">
                    <span
                      className="w-2.5 h-2.5 rounded-full animate-ping"
                      style={{ backgroundColor: currentStepMeta.activeTx?.color || '#EF4444' }}
                    />
                    <span className="font-bold text-text uppercase tracking-wider text-[11px]">
                      {currentStepMeta.title}
                    </span>
                  </div>
                  <Badge variant="accent" size="sm" className="font-mono">
                    {currentStepMeta.label}
                  </Badge>
                </div>

                {/* Active Transfer Pair */}
                {currentStepMeta.activeTx && (
                  <div className="space-y-1.5">
                    <div className="flex items-center justify-between text-[11px] gap-2">
                      <div className="min-w-0">
                        <span className="text-text-muted block text-[10px]">ORIGINATOR (SENDER)</span>
                        <span className="font-semibold text-text truncate block">{currentStepMeta.activeTx.sourceName}</span>
                      </div>
                      <ArrowRight className="w-4 h-4 text-accent shrink-0 animate-pulse" />
                      <div className="min-w-0 text-right">
                        <span className="text-text-muted block text-[10px]">BENEFICIARY (RECEIVER)</span>
                        <span className="font-semibold text-text truncate block">{currentStepMeta.activeTx.targetName}</span>
                      </div>
                    </div>

                    {/* Amount & Rail */}
                    <div className="p-2 rounded bg-bg border border-border flex items-center justify-between">
                      <div>
                        <span className="text-[10px] text-text-muted block">TRANSACTION VOLUME</span>
                        <div className="flex items-baseline gap-1.5">
                          <span className="text-sm font-bold text-text">{currentStepMeta.activeTx.amount}</span>
                          <span className="text-[10px] text-text-muted font-normal">({currentStepMeta.activeTx.amountBdt})</span>
                        </div>
                      </div>
                      <div className="text-right">
                        <span className="text-[10px] text-text-muted block">PAYMENT RAIL</span>
                        <Badge variant="neutral" size="sm" className="font-bold">
                          {currentStepMeta.activeTx.rail}
                        </Badge>
                      </div>
                    </div>

                    {/* Metrics Row: Hawkes Intensity & Typology */}
                    <div className="grid grid-cols-2 gap-2 text-[10px]">
                      <div className="p-1.5 rounded bg-bg/50 border border-border/50">
                        <span className="text-text-muted block">TYPOLOGY</span>
                        <span className="font-semibold text-critical truncate block">
                          {currentStepMeta.activeTx.typology}
                        </span>
                      </div>
                      <div className="p-1.5 rounded bg-bg/50 border border-border/50">
                        <span className="text-text-muted block">VELOCITY RATE</span>
                        <span className="font-semibold text-text truncate block">
                          {currentStepMeta.activeTx.hawkes}
                        </span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Closed Laundering Loop Detected Banner on Step 4 */}
        {timelineStep === 4 && (
          <div className="absolute bottom-4 right-4 z-20 pointer-events-none animate-in fade-in slide-in-from-bottom duration-300">
            <div className="px-3.5 py-2 rounded-lg bg-critical/15 backdrop-blur-md border border-critical text-critical text-xs font-mono font-bold flex items-center gap-2 shadow-lg">
              <span className="w-2.5 h-2.5 rounded-full bg-critical animate-ping" />
              <span>🚨 3-Hop Wash Loop Closed • 100% Flow Conservation Ring</span>
            </div>
          </div>
        )}
      </div>

      {/* Temporal Timeline Scrubber Playback Bar */}
      <div className="p-3 border-t border-border bg-surfaceRaised/95 backdrop-blur-xs flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3 z-10">
        {/* Left: Playback Controls & Speed */}
        <div className="flex items-center gap-2 flex-wrap">
          {/* Play/Pause & Step Buttons */}
          <div className="flex items-center gap-1 shrink-0">
            <button
              onClick={() => { const n = Math.max(0, (timelineStepRef.current || 0) - 1); setTimelineStep(n); timelineStepRef.current = n; }}
              className="p-1.5 rounded hover:bg-surface text-text-2 hover:text-text border border-border cursor-pointer transition-colors"
              title="Step Backward (Δt - 1)"
            >
              <SkipBack className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={handleTogglePlay}
              className={`px-3 py-1.5 rounded font-mono text-xs font-semibold cursor-pointer transition-all shadow-xs flex items-center gap-1.5 ${
                isPlaying
                  ? 'bg-amber-600 text-white hover:bg-amber-500 animate-pulse'
                  : 'bg-accent text-white hover:bg-accent/90'
              }`}
              title={isPlaying ? 'Pause Playback' : 'Play Transaction Flow Sequence'}
            >
              {isPlaying ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
              <span>{isPlaying ? 'PAUSE' : 'PLAY FLOW'}</span>
            </button>
            <button
              onClick={() => { const n = Math.min(4, (timelineStepRef.current || 0) + 1); setTimelineStep(n); timelineStepRef.current = n; }}
              className="p-1.5 rounded hover:bg-surface text-text-2 hover:text-text border border-border cursor-pointer transition-colors"
              title="Step Forward (Δt + 1)"
            >
              <SkipForward className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => { setIsPlaying(false); setTimelineStep(0); timelineStepRef.current = 0; }}
              className="p-1.5 rounded hover:bg-surface text-text-muted hover:text-text border border-border cursor-pointer transition-colors"
              title="Reset Timeline to Baseline"
            >
              <RotateCcw className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="w-px h-4 bg-border mx-0.5" />

          {/* Speed Selector (0.5x, 1x, 2x) */}
          <div className="flex items-center gap-0.5 p-0.5 bg-bg rounded border border-border font-mono text-[10px]">
            {[
              { speed: 0.5, label: '0.5x' },
              { speed: 1, label: '1x' },
              { speed: 2, label: '2x' }
            ].map(s => (
              <button
                key={s.speed}
                onClick={() => setPlaybackSpeed(s.speed)}
                className={`px-2 py-0.5 rounded transition-colors cursor-pointer ${
                  playbackSpeed === s.speed
                    ? 'bg-surface font-bold text-accent shadow-xs'
                    : 'text-text-muted hover:text-text'
                }`}
                title={`Playback Speed: ${s.label}`}
              >
                {s.label}
              </button>
            ))}
          </div>

          {/* Playback Mode: Cumulative vs Step Focus */}
          <button
            onClick={() => setPlaybackMode(prev => prev === 'cumulative' ? 'single' : 'cumulative')}
            className={`px-2 py-1 rounded border text-[10px] font-mono transition-colors cursor-pointer flex items-center gap-1 ${
              playbackMode === 'cumulative'
                ? 'bg-accent/10 border-accent/40 text-accent font-semibold'
                : 'bg-bg border-border text-text-muted hover:text-text'
            }`}
            title={playbackMode === 'cumulative' ? 'Accumulate completed money trail' : 'Focus only on current transaction'}
          >
            <Layers className="w-3 h-3" />
            <span>{playbackMode === 'cumulative' ? 'Cumulative Trail' : 'Step Focus'}</span>
          </button>

          {/* Auto-Loop Toggle */}
          <button
            onClick={() => setAutoLoop(!autoLoop)}
            className={`p-1.5 rounded border text-[10px] font-mono transition-colors cursor-pointer ${
              autoLoop
                ? 'bg-accent/10 border-accent/40 text-accent'
                : 'bg-bg border-border text-text-muted hover:text-text'
            }`}
            title={autoLoop ? 'Auto-looping active' : 'Auto-loop disabled'}
          >
            <Repeat className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Right: Clickable Timeline Phase Stepper Beads */}
        <div className="flex items-center justify-between gap-1.5 flex-1 max-w-md min-w-[240px]">
          {TIMELINE_STEPS.map((st) => {
            const isCurrent = timelineStep === st.step;
            const isPast = timelineStep > st.step;
            return (
              <button
                key={st.step}
                onClick={() => { setIsPlaying(false); setTimelineStep(st.step); timelineStepRef.current = st.step; }}
                className={`flex-1 flex flex-col items-center gap-1 py-1 px-1.5 rounded transition-all cursor-pointer border ${
                  isCurrent
                    ? 'bg-surface border-accent shadow-xs'
                    : isPast
                      ? 'bg-surfaceRaised border-borderSubtle hover:border-border'
                      : 'border-transparent hover:bg-surface/50 text-text-muted'
                }`}
                title={`${st.label}: ${st.title}`}
              >
                <div className={`w-2.5 h-2.5 rounded-full transition-all ${
                  isCurrent
                    ? 'bg-accent scale-125 ring-2 ring-accent/30'
                    : isPast
                      ? 'bg-accent/70'
                      : 'bg-border'
                }`} />
                <span className={`text-[9.5px] font-mono leading-none ${
                  isCurrent ? 'font-bold text-accent' : isPast ? 'text-text' : 'text-text-muted'
                }`}>
                  {st.step === 0 ? 't₀' : `t${st.step}`}
                </span>
                <span className="text-[8px] text-text-muted font-mono truncate max-w-[55px] hidden sm:inline">
                  {st.step === 0 ? 'Baseline' : st.step === 1 ? 'Smurf' : st.step === 2 ? 'Layer' : st.step === 3 ? 'Wire' : 'Wash'}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Floating Canvas Action Bar (Zoom, Fit, Export) */}
      <div className="absolute top-16 right-3 flex items-center gap-1.5 bg-surface border border-border shadow-md rounded p-1 z-20">
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
        <Button
          variant={trackCamera ? "secondary" : "ghost"}
          size="icon"
          onClick={() => setTrackCamera(!trackCamera)}
          title={trackCamera ? "Auto-Track Camera Active" : "Enable Auto-Track Camera"}
        >
          <Crosshair className={`w-4 h-4 ${trackCamera ? 'text-accent' : 'text-text-2'}`} />
        </Button>
        <div className="w-px h-4 bg-border mx-0.5" />
        <Button variant="ghost" size="icon" onClick={handleExportPNG} title="Export PNG">
          <Download className="w-4 h-4 text-text-2" />
        </Button>
      </div>

      {/* Floating Minimal Legend */}
      <div className="absolute bottom-20 left-3 bg-surface/95 backdrop-blur-xs border border-border shadow-sm rounded p-2 z-20 text-[10px] space-y-1 font-mono">
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
