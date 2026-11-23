# Storage-Level WORM & Tamper-Evident Ledger Architecture

## 1. Architectural Distinction: Tamper-Evident vs. Storage WORM

In compliance engineering and financial crime auditing, there is a strict technical distinction between **application-level tamper evidence** and **storage-level Write-Once-Read-Many (WORM)**:

```
+-----------------------------------------------------------------------------------+
|                        APPLICATION-LEVEL TAMPER EVIDENCE                          |
|  - Cryptographic append-only hash chain (SHA-256 over RFC 8785 Canonical JSON)    |
|  - Pointer continuity: block[i].prev_hash == block[i-1].curr_hash                 |
|  - Asymmetric RFC 8032 Ed25519 signatures over binary Merkle roots               |
|  - Real-time client & API verification detecting exact first broken row index     |
+-----------------------------------------------------------------------------------+
                                        |
                                        v Periodic Anchoring
+-----------------------------------------------------------------------------------+
|                            STORAGE-LEVEL WORM LOCK                                |
|  - AWS S3 Object Lock in COMPLIANCE Mode (or MinIO Object Lock on-prem)           |
|  - Immutable 5-year retention period enforcing BFIU / MLPA 2012 § 25 statutory SLA|
|  - Root account bypass prevention: Even AWS root/IAM admin cannot delete or alter |
|  - Legal Hold flag support for active regulatory investigations                   |
+-----------------------------------------------------------------------------------+
```

---

## 2. Terminology Honesty Standard

Per regulatory guidelines and production audit best practices:
- The in-memory and database audit log is accurately referred to as a **Tamper-Evident Cryptographic Ledger**.
- It is only referred to as **WORM** when anchored to an actual storage-level immutable bucket with Object Lock enabled in Compliance Mode.

---

## 3. Storage WORM Configuration (AWS S3)

### 3.1 Bucket Provisioning with Object Lock
```bash
aws s3api create-bucket \
    --bucket intelligent-aml-compliance-vault \
    --region ap-southeast-1 \
    --create-bucket-configuration LocationConstraint=ap-southeast-1 \
    --object-lock-enabled-for-bucket
```

### 3.2 Default Retention Policy (5 Years Compliance Mode)
```json
{
  "ObjectLockConfiguration": {
    "ObjectLockEnabled": "Enabled",
    "Rule": {
      "DefaultRetention": {
        "Mode": "COMPLIANCE",
        "Days": 1825
      }
    }
  }
}
```

```bash
aws s3api put-object-lock-configuration \
    --bucket intelligent-aml-compliance-vault \
    --object-lock-configuration file://s3-object-lock-policy.json
```

### 3.3 Compliance Mode vs. Governance Mode
| Feature | Governance Mode | Compliance Mode (Intelligent-AML Standard) |
| :--- | :--- | :--- |
| **Bypass by IAM Root** | Allowed with `s3:BypassGovernanceRetention` | **FORBIDDEN (No bypass under any circumstance)** |
| **Premature Deletion** | Allowed by authorized privileged admin | **IMPOSSIBLE until retention expiration (5 years)** |
| **Legal Admissibility**| Internal governance records | **FRE 902(11) & Evidence Act 2022 § 65B Certified** |

---

## 4. On-Premises WORM with MinIO

For on-premises and air-gapped sovereign bank deployments, MinIO provides drop-in S3 Object Lock compliance:

```yaml
# deploy/docker/docker-compose.yml excerpt
services:
  minio-worm-vault:
    image: minio/minio:RELEASE.2024-11-07T00-52-07Z
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_VAULT_ROOT_USER}
      MINIO_ROOT_PASSWORD: ${MINIO_VAULT_ROOT_PASSWORD}
    volumes:
      - minio_worm_data:/data
    healthcheck:
      test: ["CMD", "mc", "ready", "local"]
      interval: 10s
      timeout: 5s
      retries: 5

  minio-worm-init:
    image: minio/mc:RELEASE.2024-11-05T11-41-28Z
    depends_on:
      minio-worm-vault:
        condition: service_healthy
    entrypoint: >
      /bin/sh -c "
      mc alias set wormvault http://minio-worm-vault:9000 $${MINIO_VAULT_ROOT_USER} $${MINIO_VAULT_ROOT_PASSWORD};
      mc mb --with-lock wormvault/intelligent-aml-compliance-vault;
      mc retention set --default COMPLIANCE 1825d wormvault/intelligent-aml-compliance-vault;
      exit 0;
      "
```

---

## 5. Ed25519 Checkpoint Anchoring Protocol

Every milestone batch of audit records triggers an Ed25519 asymmetric cryptographic checkpoint:
1. **Canonical Merkle Root**: The checkpointer (`src/engine/audit_checkpointer.py`) constructs a binary Merkle tree across all block digests in the interval.
2. **Ed25519 Signature**: The compliance node's private Ed25519 key (RFC 8032) signs `(checkpoint_id, start_index, end_index, merkle_root)`.
3. **WORM Vault Upload**: The serialized JSON receipt is uploaded with an Object Lock retention header to `s3://intelligent-aml-compliance-vault/audit-checkpoints/CHK-XXXXXX.json`.
4. **Independent Verifiability**: Any auditor or bank regulator can retrieve the signed checkpoint, verify the signature with the node's public key, and verify that the database hash chain matches the immutable Merkle root.
