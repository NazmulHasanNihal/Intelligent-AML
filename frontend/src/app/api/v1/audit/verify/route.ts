import { NextRequest, NextResponse } from 'next/server';
import { verifyAuditChain, getAuditChain } from '@/lib/audit/hashChain';
import { fetchFastApiWithFallback } from '@/lib/apiAdapter';

/**
 * Audit Ledger Verification API
 * Supports GET & POST for independent external compliance verifiers.
 * Validates SHA-256 sequential Merkle hash chain, pointer continuity, and canonical payloads.
 */
export const dynamic = 'force-dynamic';

export async function GET(req: NextRequest) {
  const localVerify = async () => {
    const result = await verifyAuditChain();
    const chain = getAuditChain();

    return {
      ...result,
      totalBlocks: chain.length,
      rootHash: chain[0]?.currentHash || chain[0]?.merkleHash || null,
      headHash: chain[chain.length - 1]?.currentHash || chain[chain.length - 1]?.merkleHash || null,
      anchoredObjectLockUri: 's3://intelligent-aml-compliance-vault/audit-checkpoints/',
      verifiedAt: new Date().toISOString(),
      hashingStandard: 'SHA-256 (RFC 8785 Canonical JSON)',
      signingAlgorithm: 'Ed25519 (RFC 8032)',
      legalAdmissibility: result.isValid
        ? 'VERIFIED (Tamper-Evident): Admissibility-ready under Bangladesh Evidence Act, 1872 (Amended 2022) §§ 65A–65B & 73A (Officer Certificate) & FRE 902(11).'
        : 'TAMPER_DETECTED: Cryptographic hash chain validation failed. Evidence is tainted and inadmissible.'
    };
  };

  const result = await fetchFastApiWithFallback(
    '/api/v1/audit/verify',
    { method: 'GET' },
    localVerify,
    { timeoutMs: 2500 }
  );

  return NextResponse.json(result);
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
      ? 'VERIFIED (Tamper-Evident): Admissibility-ready under Bangladesh Evidence Act, 1872 (Amended 2022) §§ 65A–65B & 73A (Officer Certificate) & FRE 902(11).'
      : 'TAMPER_DETECTED: Cryptographic hash chain validation failed. Evidence is tainted and inadmissible.'
  });
}
