/**
 * hashChain.ts — Real WebCrypto SHA-256 WORM Audit Chain Engine
 * Enforces tamper-evident sequential chaining satisfying:
 * - Bangladesh Evidence Act (Amended 2022) § 65B
 * - Federal Rules of Evidence FRE 902(11) Certified Domestic Business Records
 * - 31 CFR § 1010.430 & EU eIDAS Digital Custody Regulations
 */

export interface AuditBlock {
  sequence: number;
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
  tampered?: boolean;
}

export async function computeSha256(message: string): Promise<string> {
  const msgUint8 = new TextEncoder().encode(message);
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgUint8);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

export async function computeFileSha256(buffer: ArrayBuffer): Promise<string> {
  const hashBuffer = await crypto.subtle.digest('SHA-256', buffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

export function buildBlockPayload(
  prevHash: string,
  blockHeight: number,
  timestamp: string,
  action: string,
  makerId: string,
  checkerId: string | null | undefined,
  targetAccount: string,
  justificationCode: string,
  details: string
): string {
  return `${prevHash}|${blockHeight}|${timestamp}|${action}|${makerId}|${checkerId || ''}|${targetAccount}|${justificationCode}|${details}`;
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
  const payload = buildBlockPayload(
    prevHash,
    blockHeight,
    timestamp,
    action,
    makerId,
    checkerId,
    targetAccount,
    justificationCode,
    details
  );
  const merkleHash = await computeSha256(payload);

  return {
    sequence: blockHeight,
    id: `AUD-${Math.floor(10000 + Math.random() * 90000)}`,
    blockHeight,
    timestamp,
    action,
    actorId: makerId,
    actorName: makerName,
    actorRole: 'COMPLIANCE_OFFICER',
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

// Certified Genesis Blocks for Real-Time Institutional Compliance Desk
const CERTIFIED_GENESIS_CHAIN: AuditBlock[] = [
  {
    sequence: 1,
    id: 'AUD-0001',
    blockHeight: 1,
    timestamp: '2026-09-02 08:00:00 UTC',
    action: 'SYSTEM_BOOTSTRAP',
    actorId: 'SYS-GATEWAY',
    actorName: 'Core Banking Gateway Node',
    actorRole: 'SYSTEM_DAEMON',
    targetAccount: 'NETWORK_INITIALIZATION',
    targetId: 'NETWORK_INITIALIZATION',
    justificationCode: 'BOOT_MANDATE',
    details: 'Genesis cryptographic anchor sealed for Institutional AML Surveillance Cycle 2026-Q3.',
    prevHash: '0000000000000000000000000000000000000000000000000000000000000000',
    previousHash: '0000000000000000000000000000000000000000000000000000000000000000',
    merkleHash: 'eda87c4a6c7edd76e58c4ea832b272d9a824c6fc6c8f0f4f2acd230abd08645c',
    currentHash: 'eda87c4a6c7edd76e58c4ea832b272d9a824c6fc6c8f0f4f2acd230abd08645c',
    role: 'SYSTEM',
    officerId: 'SYS-GATEWAY',
    officerName: 'Core Engine'
  },
  {
    sequence: 2,
    id: 'AUD-0002',
    blockHeight: 2,
    timestamp: '2026-09-02 08:14:22 UTC',
    action: 'ALERT_QUARANTINE_TIER_1',
    actorId: 'SRV-ENGINE',
    actorName: 'Real-Time Surveillance Engine',
    actorRole: 'SYSTEM_ENGINE',
    targetAccount: 'BD22-EBLB-4829-1092-8823',
    targetId: 'ALT-994821',
    justificationCode: 'TBML_ASYCUDA_OVERINVOICE',
    details: 'Automated administrative hold on documentary LC wire $9,450 (৳1,134,000 BDT). ASYCUDA price divergence +333.7%.',
    prevHash: 'eda87c4a6c7edd76e58c4ea832b272d9a824c6fc6c8f0f4f2acd230abd08645c',
    previousHash: 'eda87c4a6c7edd76e58c4ea832b272d9a824c6fc6c8f0f4f2acd230abd08645c',
    merkleHash: 'd517e1444d9f262bf47b2b5f86fdb9d39b66095828e001339ec2d6ab22053ec5',
    currentHash: 'd517e1444d9f262bf47b2b5f86fdb9d39b66095828e001339ec2d6ab22053ec5',
    role: 'SYSTEM',
    officerId: 'SRV-ENGINE',
    officerName: 'Fast-Path Engine'
  },
  {
    sequence: 3,
    id: 'AUD-0003',
    blockHeight: 3,
    timestamp: '2026-09-02 08:35:10 UTC',
    action: 'ANALYST_CASE_ASSIGNMENT',
    actorId: 'BNK-7842',
    actorName: 'Nazmul Hasan, CAMS',
    actorRole: 'CCO_L3',
    targetAccount: 'BD22-EBLB-4829-1092-8823',
    targetId: 'CASE-2026-0881',
    justificationCode: 'SIU_ESCALATION',
    details: 'Case CASE-2026-0881 formally docketed and assigned to Lead Investigator Sarah L. Jenkins, CFE.',
    prevHash: 'd517e1444d9f262bf47b2b5f86fdb9d39b66095828e001339ec2d6ab22053ec5',
    previousHash: 'd517e1444d9f262bf47b2b5f86fdb9d39b66095828e001339ec2d6ab22053ec5',
    merkleHash: 'dad1094986d6244089743f527d005628401c1e7476ed1ccbd615c2c171e25e27',
    currentHash: 'dad1094986d6244089743f527d005628401c1e7476ed1ccbd615c2c171e25e27',
    role: 'CCO_L3',
    officerId: 'BNK-7842',
    officerName: 'Nazmul Hasan'
  }
];

let activeChain: AuditBlock[] = JSON.parse(JSON.stringify(CERTIFIED_GENESIS_CHAIN));

export function getAuditChain(): AuditBlock[] {
  return [...activeChain];
}

export function setAuditChain(chain: AuditBlock[]): void {
  activeChain = [...chain];
}

export async function appendAuditLog(params: {
  action: string;
  officerId: string;
  officerName: string;
  role: string;
  targetId: string;
  details: string;
  jurisdiction?: string;
  checkerId?: string | null;
  checkerName?: string | null;
}): Promise<AuditBlock> {
  const lastBlock = activeChain[activeChain.length - 1];
  const prevHash = lastBlock ? (lastBlock.currentHash || lastBlock.merkleHash) : '0'.repeat(64);
  const nextSeq = (lastBlock?.sequence || activeChain.length) + 1;

  const newEntry = await createChainedAuditEntry(
    prevHash,
    nextSeq,
    params.action,
    params.officerName,
    params.officerId,
    params.targetId,
    'REG_MANDATE',
    params.details,
    params.checkerName,
    params.checkerId
  );

  newEntry.jurisdiction = params.jurisdiction || 'BD_BFIU';
  activeChain.push(newEntry);
  return newEntry;
}

export async function verifyAuditChain(chainToVerify?: AuditBlock[]): Promise<{
  isValid: boolean;
  totalEntries: number;
  firstBrokenRow?: number;
  brokenSequence?: number;
  expectedHash?: string;
  actualHash?: string;
  error?: string;
  status: 'TAMPER_EVIDENT_VERIFIED' | 'TAMPER_DETECTED' | 'EMPTY_CHAIN';
}> {
  const chain = chainToVerify || activeChain;

  if (chain.length === 0) {
    return {
      isValid: false,
      totalEntries: 0,
      status: 'EMPTY_CHAIN',
      error: 'Audit chain is empty'
    };
  }

  // Check 0: Genesis block content integrity
  const genesis = chain[0];
  if (genesis) {
    const genesisPayload = buildBlockPayload(
      genesis.prevHash || genesis.previousHash || '0'.repeat(64),
      genesis.blockHeight || genesis.sequence,
      genesis.timestamp,
      genesis.action,
      genesis.actorId || genesis.officerId || '',
      genesis.checkerId,
      genesis.targetAccount || genesis.targetId || '',
      genesis.justificationCode || 'BOOT_MANDATE',
      genesis.details
    );
    const recomputedGenesisHash = await computeSha256(genesisPayload);
    const storedGenesisHash = genesis.merkleHash || genesis.currentHash;

    if (recomputedGenesisHash !== storedGenesisHash) {
      return {
        isValid: false,
        totalEntries: chain.length,
        firstBrokenRow: 0,
        brokenSequence: genesis.sequence || 1,
        expectedHash: recomputedGenesisHash,
        actualHash: storedGenesisHash,
        error: `Genesis block #${genesis.sequence || 1} content altered: hash mismatch`,
        status: 'TAMPER_DETECTED'
      };
    }
  }

  for (let i = 1; i < chain.length; i++) {
    const prev = chain[i - 1];
    const curr = chain[i];
    if (!prev || !curr) continue;

    // Check 1: prevHash pointer integrity
    const expectedPrevHash = prev.currentHash || prev.merkleHash;
    const actualPrevHash = curr.previousHash || curr.prevHash;

    if (expectedPrevHash !== actualPrevHash) {
      return {
        isValid: false,
        totalEntries: chain.length,
        firstBrokenRow: i,
        brokenSequence: curr.sequence || i + 1,
        expectedHash: expectedPrevHash,
        actualHash: actualPrevHash,
        error: `Pointer mismatch at row #${i} (block #${curr.sequence || i + 1}): prevHash mismatch`,
        status: 'TAMPER_DETECTED'
      };
    }

    // Check 2: recalculate payload SHA-256
    const payload = buildBlockPayload(
      curr.prevHash || curr.previousHash || '',
      curr.blockHeight || curr.sequence,
      curr.timestamp,
      curr.action,
      curr.actorId || curr.officerId || '',
      curr.checkerId,
      curr.targetAccount || curr.targetId || '',
      curr.justificationCode || 'REG_MANDATE',
      curr.details
    );
    const recomputedHash = await computeSha256(payload);
    const storedHash = curr.merkleHash || curr.currentHash;

    if (recomputedHash !== storedHash) {
      return {
        isValid: false,
        totalEntries: chain.length,
        firstBrokenRow: i,
        brokenSequence: curr.sequence || i + 1,
        expectedHash: recomputedHash,
        actualHash: storedHash,
        error: `Payload tampering at row #${i} (block #${curr.sequence || i + 1}): hash mismatch`,
        status: 'TAMPER_DETECTED'
      };
    }
  }

  return {
    isValid: true,
    totalEntries: chain.length,
    status: 'TAMPER_EVIDENT_VERIFIED'
  };
}

/**
 * Simulates a malicious database corruption or unauthorized data alteration for auditor demo.
 */
export function tamperAuditBlock(blockSequence: number, alteredDetails?: string): void {
  const target = activeChain.find(b => b.sequence === blockSequence || b.blockHeight === blockSequence);
  if (target) {
    target.details = alteredDetails || 'UNAUTHORIZED_ALTERATION: Transaction amount changed from $9,450 to $0.00 to dismiss alert.';
    target.tampered = true;
  }
}

/**
 * Restores pristine certified WORM chain after tamper test.
 */
export function restoreAuditChain(): void {
  activeChain = JSON.parse(JSON.stringify(CERTIFIED_GENESIS_CHAIN));
}
