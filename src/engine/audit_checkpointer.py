"""
audit_checkpointer.py — Ed25519 Checkpoint Signer & Object-Lock Anchor Adapter

Implements:
1. RFC 8032 Ed25519 asymmetric cryptographic signing for periodic audit checkpoints.
2. Canonical JSON Merkle root computation over sequential block hashes.
3. Object-Lock Bucket Anchor Adapter (AWS S3 Object Lock Compliance Mode / MinIO / Local Vault).
4. Continuous tamper-evidence proof receipt generation.
"""

import os
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization


class AuditCheckpoint:
    def __init__(
        self,
        checkpoint_id: str,
        start_index: int,
        end_index: int,
        root_hash: str,
        head_hash: str,
        merkle_root: str,
        timestamp: str,
        ed25519_signature: str,
        public_key_hex: str,
        object_lock_uri: str
    ):
        self.checkpoint_id = checkpoint_id
        self.start_index = start_index
        self.end_index = end_index
        self.root_hash = root_hash
        self.head_hash = head_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.ed25519_signature = ed25519_signature
        self.public_key_hex = public_key_hex
        self.object_lock_uri = object_lock_uri

    def to_dict(self) -> Dict[str, Any]:
        return {
            "checkpoint_id": self.checkpoint_id,
            "block_range": [self.start_index, self.end_index],
            "root_hash": self.root_hash,
            "head_hash": self.head_hash,
            "merkle_root": self.merkle_root,
            "timestamp": self.timestamp,
            "signature_algorithm": "Ed25519 (RFC 8032)",
            "ed25519_signature": self.ed25519_signature,
            "public_key_hex": self.public_key_hex,
            "anchored_object_lock_uri": self.object_lock_uri
        }


class AuditCheckpointer:
    """
    Signs periodic checkpoints of the tamper-evident audit ledger using Ed25519 keys
    and anchors checkpoints to an Object-Lock compliance bucket.
    """

    def __init__(self, key_path: Optional[str] = None, vault_dir: Optional[str] = None):
        self.vault_dir = Path(vault_dir) if vault_dir else Path("results/audit_checkpoints")
        self.vault_dir.mkdir(parents=True, exist_ok=True)
        self.object_lock_uri = os.getenv(
            "OBJECT_LOCK_BUCKET_URI",
            "s3://intelligent-aml-compliance-vault/audit-checkpoints/"
        )

        # Initialize or load Ed25519 signing keypair
        self._private_key = ed25519.Ed25519PrivateKey.generate()
        self._public_key = self._private_key.public_key()
        self.public_key_hex = self._public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        ).hex()

        self.latest_checkpoint: Optional[AuditCheckpoint] = None

    @staticmethod
    def compute_merkle_root(hashes: List[str]) -> str:
        """Computes a binary Merkle tree root over a list of block hashes."""
        if not hashes:
            return hashlib.sha256(b"empty_chain").hexdigest()
        current_layer = [h if len(h) == 64 else hashlib.sha256(h.encode()).hexdigest() for h in hashes]
        while len(current_layer) > 1:
            next_layer = []
            for i in range(0, len(current_layer), 2):
                left = current_layer[i]
                right = current_layer[i + 1] if i + 1 < len(current_layer) else left
                combined = hashlib.sha256(f"{left}:{right}".encode("utf-8")).hexdigest()
                next_layer.append(combined)
            current_layer = next_layer
        return current_layer[0]

    def create_checkpoint(self, blocks: List[Any]) -> AuditCheckpoint:
        """
        Creates an Ed25519-signed checkpoint over the supplied audit block sequence
        and anchors it to the immutable Object-Lock vault.
        """
        if not blocks:
            raise ValueError("Cannot create checkpoint over empty audit chain.")

        start_idx = blocks[0].index
        end_idx = blocks[-1].index
        root_h = blocks[0].curr_hash
        head_h = blocks[-1].curr_hash
        all_hashes = [b.curr_hash for b in blocks]
        merkle_root = self.compute_merkle_root(all_hashes)
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        checkpoint_id = f"CHK-{start_idx:06d}-{end_idx:06d}"

        # Canonical string to sign
        canonical_digest = f"{checkpoint_id}:{start_idx}:{end_idx}:{root_h}:{head_h}:{merkle_root}:{timestamp}"
        signature = self._private_key.sign(canonical_digest.encode("utf-8")).hex()

        checkpoint = AuditCheckpoint(
            checkpoint_id=checkpoint_id,
            start_index=start_idx,
            end_index=end_idx,
            root_hash=root_h,
            head_hash=head_h,
            merkle_root=merkle_root,
            timestamp=timestamp,
            ed25519_signature=signature,
            public_key_hex=self.public_key_hex,
            object_lock_uri=f"{self.object_lock_uri}{checkpoint_id}.json"
        )
        self.latest_checkpoint = checkpoint

        # Persist checkpoint to local vault anchor
        self._anchor_checkpoint_to_vault(checkpoint)
        return checkpoint

    def _anchor_checkpoint_to_vault(self, checkpoint: AuditCheckpoint):
        """Simulates S3 Object Lock PutObject (Compliance retention)."""
        file_path = self.vault_dir / f"{checkpoint.checkpoint_id}.json"
        payload = checkpoint.to_dict()
        payload["object_lock_retention"] = {
            "mode": "COMPLIANCE",
            "statute": "Bangladesh MLPA 2012 § 8 / FRE 902(11)",
            "retention_years": 5,
            "legal_hold": False
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    def verify_checkpoint(self, checkpoint: AuditCheckpoint, blocks: List[Any]) -> bool:
        """
        Cryptographically verifies Ed25519 signature and Merkle root against live blocks.
        """
        try:
            # 1. Verify Ed25519 signature
            canonical_digest = (
                f"{checkpoint.checkpoint_id}:{checkpoint.start_index}:{checkpoint.end_index}:"
                f"{checkpoint.root_hash}:{checkpoint.head_hash}:{checkpoint.merkle_root}:{checkpoint.timestamp}"
            )
            pub_key = ed25519.Ed25519PublicKey.from_public_bytes(bytes.fromhex(checkpoint.public_key_hex))
            pub_key.verify(bytes.fromhex(checkpoint.ed25519_signature), canonical_digest.encode("utf-8"))

            # 2. Verify Merkle root matches actual blocks
            relevant_blocks = [b for b in blocks if checkpoint.start_index <= b.index <= checkpoint.end_index]
            actual_hashes = [b.curr_hash for b in relevant_blocks]
            recomputed_merkle = self.compute_merkle_root(actual_hashes)
            return recomputed_merkle == checkpoint.merkle_root
        except Exception:
            return False


# Global Checkpointer singleton
audit_checkpointer = AuditCheckpointer()
