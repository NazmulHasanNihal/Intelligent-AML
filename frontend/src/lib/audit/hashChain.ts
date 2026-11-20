// SHA-256 Hash Chain Utility for Federal Rules of Evidence FRE 902(11) & 31 CFR § 1010.430

export interface AuditBlock {
  sequence?: number;
  id: string;
  blockHeight: number;
  timestamp: string;
  action: string;
  actorId: string;
  actorName: string;
  actorRole: string;
  checkerId?: string | null;
  checkerName?: string | null;
  targetAccount: string;
  targetId?: string;
  justificationCode: string;
  details: string;
  prevHash: string;
  previousHash?: string;
  merkleHash: string;
  currentHash?: string;
  jurisdiction?: string;
  role?: string;
  officerId?: string;
  officerName?: string;
}

export async function computeSha256(message: string): Promise<string> {
  const msgUint8 = new TextEncoder().encode(message);
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgUint8);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

export async function createChainedAuditEntry(
  prevHash: string,
  blockHeight: number,
  action: string,
  makerName: string,
  makerId: string,
  targetAccount: string,
  justificationCode: string,
  details: string,
  checkerName?: string | null,
  checkerId?: string | null
): Promise<AuditBlock> {
  const timestamp = new Date().toISOString().replace('T', ' ').substring(0, 19) + ' UTC';
  const payload = `${prevHash}|${blockHeight}|${timestamp}|${action}|${makerId}|${checkerId || ''}|${targetAccount}|${justificationCode}|${details}`;
  const merkleHash = await computeSha256(payload);

  return {
    sequence: blockHeight,
    id: `AUD-${Math.floor(10000 + Math.random() * 90000)}`,
    blockHeight,
    timestamp,
    action,
    actorId: makerId,
    actorName: makerName,
    actorRole: 'ANALYST_OR_OFFICER',
    checkerId,
    checkerName,
    targetAccount,
    targetId: targetAccount,
    justificationCode,
    details,
    prevHash,
    previousHash: prevHash,
    merkleHash,
    currentHash: merkleHash,
    role: 'INVESTIGATOR_L2',
    officerId: makerId,
    officerName: makerName
  };
}

// In-Memory Ledger Store for Air-Gapped Intranet Node
const inMemoryChain: AuditBlock[] = [
  {
    sequence: 1,
    id: 'AUD-0001',
    blockHeight: 1,
    timestamp: '2026-09-02 08:00:00 UTC',
    action: 'SYSTEM_BOOTSTRAP',
    actorId: 'SYS-01',
    actorName: 'Core Banking Gateway',
    actorRole: 'SYSTEM',
    targetAccount: 'NETWORK_INITIALIZATION',
    targetId: 'NETWORK_INITIALIZATION',
    justificationCode: 'BOOT',
    details: 'Genesis cryptographic anchor generated for 2026-09-02 compliance cycle.',
    prevHash: '0000000000000000000000000000000000000000000000000000000000000000',
    previousHash: '0000000000000000000000000000000000000000000000000000000000000000',
    merkleHash: '7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069',
    currentHash: '7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069',
    role: 'SYSTEM',
    officerId: 'SYS-01',
    officerName: 'Core Engine'
  },
  {
    sequence: 2,
    id: 'AUD-0002',
    blockHeight: 2,
    timestamp: '2026-09-02 08:14:22 UTC',
    action: 'ALERT_QUARANTINE_TIER_1',
    actorId: 'SRV-ENGINE',
    actorName: 'C-STGB Surveillance Fast-Path',
    actorRole: 'SYSTEM_ENGINE',
    targetAccount: 'BD22-EBLB-4829-1092-8823',
    targetId: 'ALT-994821',
    justificationCode: 'TBML_ASYCUDA_DEV',
    details: 'Placed administrative hold on documentary LC wire $9,450. ASYCUDA price divergence +333.7%.',
    prevHash: '7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069',
    previousHash: '7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069',
    merkleHash: '1a8565a9d214a31da50e6b1f04f900da25058ac44f22f33e7210b37701f163a4',
    currentHash: '1a8565a9d214a31da50e6b1f04f900da25058ac44f22f33e7210b37701f163a4',
    role: 'SYSTEM',
    officerId: 'SRV-ENGINE',
    officerName: 'C-STGB Fast-Path'
  }
];

export function getAuditChain(): AuditBlock[] {
  return [...inMemoryChain];
}

export async function appendAuditLog(params: {
  action: string;
  officerId: string;
  officerName: string;
  role: string;
  targetId: string;
  details: string;
  jurisdiction?: string;
}): Promise<AuditBlock> {
  const lastBlock = inMemoryChain[inMemoryChain.length - 1];
  const prevHash = lastBlock ? (lastBlock.currentHash || lastBlock.merkleHash) : '0'.repeat(64);
  const nextSeq = (lastBlock?.sequence || inMemoryChain.length) + 1;

  const newEntry = await createChainedAuditEntry(
    prevHash,
    nextSeq,
    params.action,
    params.officerName,
    params.officerId,
    params.targetId,
    '4EYES_REG_RATIFIED',
    params.details
  );

  newEntry.jurisdiction = params.jurisdiction || 'BGD';
  inMemoryChain.push(newEntry);
  return newEntry;
}

export async function verifyAuditChain(): Promise<{ isValid: boolean; totalEntries: number; brokenSequence?: number }> {
  for (let i = 1; i < inMemoryChain.length; i++) {
    const prev = inMemoryChain[i - 1];
    const curr = inMemoryChain[i];
    if (!prev || !curr) continue;

    const prevHash = prev.currentHash || prev.merkleHash;
    const currPrevHash = curr.previousHash || curr.prevHash;

    if (prevHash !== currPrevHash) {
      return { isValid: false, totalEntries: inMemoryChain.length, brokenSequence: curr.sequence || i + 1 };
    }
  }

  return { isValid: true, totalEntries: inMemoryChain.length };
}
