export type ConnectorStatus = 'CONNECTED' | 'SANDBOX_SIMULATED' | 'PAUSED' | 'ERROR';

export interface InstitutionalConnector {
  id: string;
  name: string;
  protocol: string;
  endpoint: string;
  status: ConnectorStatus;
  enabled: boolean;
  lastHeartbeat: string;
  latencyMs: number;
  eventsDelivered: number;
  description: string;
}

export interface WebhookDeliveryLog {
  id: string;
  connectorId: string;
  eventType: string;
  targetAccount: string;
  statusCode: number;
  signaturePrefix: string;
  deliveredAt: string;
  mode: 'serverless-demo' | 'fastapi-live';
}

export const INITIAL_CONNECTORS: InstitutionalConnector[] = [
  {
    id: 'conn-core-t24',
    name: 'Core Banking Settlement Hold (T24)',
    protocol: 'HMAC-SHA256 Webhook / ISO 20022',
    endpoint: 'https://corebanking.internal/api/v2/holds/settlement',
    status: 'SANDBOX_SIMULATED',
    enabled: true,
    lastHeartbeat: '2026-11-23T11:59:42Z',
    latencyMs: 14,
    eventsDelivered: 1280,
    description: 'Enforces real-time Tier 1 settlement holds upon dual 4-eyes ratification.',
  },
  {
    id: 'conn-swift-mt',
    name: 'SWIFT Alliance Access (MT103 / MT700)',
    protocol: 'ISO 20022 pacs.008 / MT700 Stream',
    endpoint: 'wss://swift-gateway.internal/stream',
    status: 'SANDBOX_SIMULATED',
    enabled: true,
    lastHeartbeat: '2026-11-23T11:59:58Z',
    latencyMs: 19,
    eventsDelivered: 8420,
    description: 'Ingests correspondent wire traffic and documentary letters of credit.',
  },
  {
    id: 'conn-bfiu-goaml',
    name: 'BFIU UNODC goAML v4.2 Gateway',
    protocol: 'mTLS XML Filing Dispatch',
    endpoint: 'https://goaml.bfiu.bb.org.bd/api/v4/reports',
    status: 'SANDBOX_SIMULATED',
    enabled: true,
    lastHeartbeat: '2026-11-23T11:50:00Z',
    latencyMs: 42,
    eventsDelivered: 18,
    description: 'Validates and queues statutory STR & CTR XML packages under MLPA 2012 § 25.',
  },
  {
    id: 'conn-sanctions-ofac',
    name: 'OFAC SDN / UN / EU Watchlist Sync',
    protocol: 'Delta List Digest Feed',
    endpoint: 'https://watchlists.internal/ofac-un-eu/digest',
    status: 'SANDBOX_SIMULATED',
    enabled: true,
    lastHeartbeat: '2026-11-23T11:45:00Z',
    latencyMs: 11,
    eventsDelivered: 312,
    description: 'Synchronizes consolidated global sanctions lists with zero PII egress.',
  },
  {
    id: 'conn-case-siem',
    name: 'SOAR / SIEM Audit Mirror (Webhook)',
    protocol: 'signed-json-webhook',
    endpoint: 'http://localhost:8000/api/v1/webhooks/sink',
    status: 'SANDBOX_SIMULATED',
    enabled: false,
    lastHeartbeat: '2026-11-23T10:30:00Z',
    latencyMs: 8,
    eventsDelivered: 64,
    description: 'Forwards tamper-evident WORM block digests and SLA alerts to internal SOC.',
  },
];

export const INITIAL_WEBHOOK_DELIVERIES: WebhookDeliveryLog[] = [
  {
    id: 'WH-2026-881',
    connectorId: 'conn-core-t24',
    eventType: 'HOLD_ENFORCED_TIER1',
    targetAccount: 'BD22-EBLB-4829-1092-8823',
    statusCode: 202,
    signaturePrefix: 'sha256=eda87c4a6c7e',
    deliveredAt: '2026-11-23T10:46:00Z',
    mode: 'serverless-demo',
  },
  {
    id: 'WH-2026-880',
    connectorId: 'conn-bfiu-goaml',
    eventType: 'STR_SCHEMA_VALIDATED',
    targetAccount: 'BD22-SCBL-9912-3341-7719',
    statusCode: 200,
    signaturePrefix: 'sha256=d517e1444d9f',
    deliveredAt: '2026-11-23T10:31:00Z',
    mode: 'serverless-demo',
  },
];

export function isPermittedWebhookTarget(urlStr: string): boolean {
  try {
    const u = new URL(urlStr);
    if (process.env.ALLOW_WEBHOOK_EGRESS === 'true') return u.protocol === 'https:' || u.protocol === 'http:';
    const h = u.hostname.toLowerCase();
    return h === 'localhost' || h === '127.0.0.1' || h.endsWith('.internal') || h.endsWith('.local');
  } catch {
    return false;
  }
}
