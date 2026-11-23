import { describe, it, expect, beforeEach } from 'vitest';
import {
  getAuditChain,
  setAuditChain,
  verifyAuditChain,
  tamperAuditBlock,
  restoreAuditChain,
  createChainedAuditEntry,
  computeSha256
} from '../lib/audit/hashChain';

describe('Tamper-Evident Hash Chain Audit Engine', () => {
  beforeEach(() => {
    restoreAuditChain();
  });

  it('validates a pristine certified genesis chain successfully', async () => {
    const result = await verifyAuditChain();
    expect(result.isValid).toBe(true);
    expect(result.status).toBe('TAMPER_EVIDENT_VERIFIED');
    expect(result.totalEntries).toBeGreaterThanOrEqual(3);
    expect(result.firstBrokenRow).toBeUndefined();
  });

  it('detects tampering when block #1 payload is mutated and returns firstBrokenRow == 0', async () => {
    tamperAuditBlock(1, 'UNAUTHORIZED_ALTERATION: Alert dismissed without MLRO approval.');
    const result = await verifyAuditChain();

    expect(result.isValid).toBe(false);
    expect(result.status).toBe('TAMPER_DETECTED');
    expect(result.firstBrokenRow).toBe(0);
    expect(result.brokenSequence).toBe(1);
    expect(result.error).toContain('Genesis block #1 content altered');
  });

  it('restores chain integrity after tamper simulation', async () => {
    tamperAuditBlock(1);
    let result = await verifyAuditChain();
    expect(result.isValid).toBe(false);

    restoreAuditChain();
    result = await verifyAuditChain();
    expect(result.isValid).toBe(true);
    expect(result.status).toBe('TAMPER_EVIDENT_VERIFIED');
  });

  it('detects pointer tampering at block #2 and returns firstBrokenRow == 1', async () => {
    const chain = getAuditChain();
    // Corrupt block 2's previousHash
    chain[1]!.previousHash = '0'.repeat(64);
    chain[1]!.prevHash = '0'.repeat(64);

    const result = await verifyAuditChain(chain);
    expect(result.isValid).toBe(false);
    expect(result.status).toBe('TAMPER_DETECTED');
    expect(result.firstBrokenRow).toBe(1);
    expect(result.brokenSequence).toBe(2);
  });

  it('appends new audit block with valid hash continuity', async () => {
    const chain = getAuditChain();
    const last = chain[chain.length - 1]!;
    const prevHash = last.currentHash || last.merkleHash;

    const newBlock = await createChainedAuditEntry(
      prevHash,
      chain.length + 1,
      'SAR_DECISION_RATIFIED',
      'Nazmul Hasan, CAMS',
      'BNK-7842',
      'AC-8812903',
      'REG_MANDATE',
      'STR ratified and transmitted to BFIU goAML gateway.'
    );

    chain.push(newBlock);
    const result = await verifyAuditChain(chain);
    expect(result.isValid).toBe(true);
    expect(result.totalEntries).toBe(chain.length);
  });
});
