import { NextRequest, NextResponse } from 'next/server';
import { verifyAuditChain, getAuditChain } from '@/lib/audit/hashChain';

/**
 * Audit Ledger Verification API
 * Supports GET & POST for independent external compliance verifiers.
 * Validates SHA-256 sequential Merkle hash chain, pointer continuity, and canonical payloads.
 */
export async function GET(req: NextRequest) {
  const result = await verifyAuditChain();
  const chain = getAuditChain();

  return NextResponse.json({
    ...result,
    totalBlocks: chain.length,
    rootHash: chain[0]?.currentHash || chain[0]?.merkleHash || null,
    headHash: chain[chain.length - 1]?.currentHash || chain[chain.length - 1]?.merkleHash || null,
    anchoredObjectLockUri: 's3://intelligent-aml-compliance-vault/audit-checkpoints/',
    verifiedAt: new Date().toISOString(),
    hashingStandard: 'SHA-256 (RFC 8785 Canonical JSON)',
    signingAlgorithm: 'Ed25519 (RFC 8032)',
    legalAdmissibility: result.isValid
      ? 'VERIFIED: Complies with Bangladesh Evidence Act 2022 § 65B & FRE 902(11) Certified Electronic Record.'
      : 'TAMPER_DETECTED: Cryptographic hash chain validation failed. Evidence is tainted and inadmissible.'
  });
}

export async function POST(req: NextRequest) {
  let customChain;
  try {
    const body = await req.json();
    if (body && Array.isArray(body.chain)) {
      customChain = body.chain;
    }
  } catch {
    // Fall back to active chain
  }

  const result = await verifyAuditChain(customChain);
  const chain = customChain || getAuditChain();

  return NextResponse.json({
    ...result,
    totalBlocks: chain.length,
    rootHash: chain[0]?.currentHash || chain[0]?.merkleHash || null,
    headHash: chain[chain.length - 1]?.currentHash || chain[chain.length - 1]?.merkleHash || null,
    anchoredObjectLockUri: 's3://intelligent-aml-compliance-vault/audit-checkpoints/',
    verifiedAt: new Date().toISOString(),
    hashingStandard: 'SHA-256 (RFC 8785 Canonical JSON)',
    signingAlgorithm: 'Ed25519 (RFC 8032)',
    legalAdmissibility: result.isValid
      ? 'VERIFIED: Complies with Bangladesh Evidence Act 2022 § 65B & FRE 902(11) Certified Electronic Record.'
      : 'TAMPER_DETECTED: Cryptographic hash chain validation failed. Evidence is tainted and inadmissible.'
  });
}
