import { NextRequest, NextResponse } from 'next/server';
import { fetchFastApiWithFallback } from '@/lib/apiAdapter';

interface SubgraphNode {
  id: string;
  label: string;
  entityName: string;
  type: 'corporate' | 'offshore' | 'mule' | 'exchange' | 'individual';
  riskScore: number;
  tier: number;
  jurisdiction: string;
  phiFlow: number;
  lambdaU: number;
  isCamouflage?: boolean;
}

interface SubgraphEdge {
  id: string;
  source: string;
  target: string;
  amount: number;
  currency: string;
  rail: string;
  timestamp: string;
  edgeTrustDelta: number; // learned adaptive edge trust delta_uv
  isCamouflage: boolean;
}

export async function GET(
  req: NextRequest,
  { params }: { params: Promise<{ nodeId: string }> }
) {
  const resolvedParams = await params;
  const nodeId = decodeURIComponent(resolvedParams.nodeId);

  // Deterministic realistic ego-network centered around requested node
  const nodes: SubgraphNode[] = [
    {
      id: nodeId,
      label: 'Root Subject',
      entityName: 'Meghna Industrial & Agro Processing Ltd',
      type: 'corporate',
      riskScore: 0.984,
      tier: 1,
      jurisdiction: 'BGD',
      phiFlow: 0.998,
      lambdaU: 4.82
    },
    {
      id: 'AE-EBIL-4412-8819-3301',
      label: 'Counterparty (Offshore)',
      entityName: 'Gulf Star Commodities FZE (JAFZA Dubai)',
      type: 'offshore',
      riskScore: 0.942,
      tier: 1,
      jurisdiction: 'ARE',
      phiFlow: 1.021,
      lambdaU: 5.12
    },
    {
      id: 'BD20-BSRM-7712-4491-0021',
      label: 'Domestic Commercial',
      entityName: 'BSRM Steels Domestic Supplier',
      type: 'corporate',
      riskScore: 0.082,
      tier: 3,
      jurisdiction: 'BGD',
      phiFlow: 0.124,
      lambdaU: 0.42
    },
    {
      id: 'MFS-BKASH-0171-8840',
      label: 'MFS Smurf Agent',
      entityName: 'Mohammad Rafiqul Islam (MFS Agent)',
      type: 'mule',
      riskScore: 0.892,
      tier: 2,
      jurisdiction: 'BGD',
      phiFlow: 0.982,
      lambdaU: 6.45
    },
    {
      id: 'SG-DBS-8819-0021-9941',
      label: 'Transit Clearing',
      entityName: 'Marina Bay Trade Clearing Pte',
      type: 'offshore',
      riskScore: 0.764,
      tier: 2,
      jurisdiction: 'SGP',
      phiFlow: 1.002,
      lambdaU: 3.12
    },
    {
      id: 'KY-CIMA-7719-4402-1102',
      label: 'Ultimate Beneficial Sink',
      entityName: 'Apex Cayman Capital Holdings Ltd',
      type: 'offshore',
      riskScore: 0.991,
      tier: 1,
      jurisdiction: 'CYM',
      phiFlow: 1.045,
      lambdaU: 4.90
    },
    {
      id: 'CAMO-LICIT-01',
      label: 'Camouflage Edge Node (Licit Utility)',
      entityName: 'Dhaka Electric Supply Co (DESCO)',
      type: 'corporate',
      riskScore: 0.012,
      tier: 3,
      jurisdiction: 'BGD',
      phiFlow: 0.05,
      lambdaU: 0.1,
      isCamouflage: true
    }
  ];

  const edges: SubgraphEdge[] = [
    {
      id: 'E1',
      source: nodeId,
      target: 'AE-EBIL-4412-8819-3301',
      amount: 48500.00,
      currency: 'USD',
      rail: 'SWIFT MT700 (LC)',
      timestamp: '2026-09-02 08:24:10 UTC',
      edgeTrustDelta: 0.945,
      isCamouflage: false
    },
    {
      id: 'E2',
      source: 'MFS-BKASH-0171-8840',
      target: nodeId,
      amount: 9450.00,
      currency: 'USD',
      rail: 'NPSB / BEFTN',
      timestamp: '2026-09-02 07:15:00 UTC',
      edgeTrustDelta: 0.880,
      isCamouflage: false
    },
    {
      id: 'E3',
      source: 'AE-EBIL-4412-8819-3301',
      target: 'SG-DBS-8819-0021-9941',
      amount: 47200.00,
      currency: 'USD',
      rail: 'SWIFT MT103',
      timestamp: '2026-09-02 09:10:00 UTC',
      edgeTrustDelta: 0.912,
      isCamouflage: false
    },
    {
      id: 'E4',
      source: 'SG-DBS-8819-0021-9941',
      target: 'KY-CIMA-7719-4402-1102',
      amount: 46800.00,
      currency: 'USD',
      rail: 'SWIFT MT103',
      timestamp: '2026-09-02 10:45:00 UTC',
      edgeTrustDelta: 0.965,
      isCamouflage: false
    },
    {
      id: 'E5_CAMO',
      source: nodeId,
      target: 'CAMO-LICIT-01',
      amount: 420.00,
      currency: 'USD',
      rail: 'Utility Pay',
      timestamp: '2026-09-01 12:00:00 UTC',
      edgeTrustDelta: 0.042, // pruned when delta floor > 0.10
      isCamouflage: true
    }
  ];

  const localCompute = () => ({
    centerNodeId: nodeId,
    nodes,
    edges,
    totalNodes: nodes.length,
    totalEdges: edges.length,
    camouflagePrunedCount: edges.filter(e => e.isCamouflage).length,
    invariantsSummary: {
      avgFlowRatio: 1.014,
      hawkesBurstDetected: true,
      circuitComplete: true
    }
  });

  const result = await fetchFastApiWithFallback(
    `/api/v1/subgraph/${encodeURIComponent(nodeId)}`,
    { method: 'GET' },
    localCompute,
    { timeoutMs: 2500 }
  );

  return NextResponse.json(result);
}
