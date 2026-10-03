"""
checkpoint_manager.py — Cryptographic Model Checkpointing, Serialization & Lineage Registry.
Complies with OCC 2011-12 / SR 11-7 Model Risk Management standards with SHA-256 weight integrity.
"""

import os
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, Union, List
import torch
import torch.nn as nn
from src.utils.logger import get_logger

logger = get_logger("checkpoint_manager")


class CheckpointManager:
    """
    Manages atomic serialization, cryptographic verification, and restoration
    of HT-GNN, CSTGB, and Conformal Prediction model state dictionaries.
    """

    def __init__(self, base_dir: Union[str, Path] = "checkpoints"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _compute_sha256(self, file_path: Path) -> str:
        """Computes SHA-256 hash of a serialized checkpoint binary."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(65536), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def save_checkpoint(
        self,
        model: nn.Module,
        dataset_name: str = "elliptic_v1",
        optimizer: Optional[torch.optim.Optimizer] = None,
        scheduler: Optional[Any] = None,
        conformal_quantiles: Optional[Dict[str, float]] = None,
        hyperparameters: Optional[Dict[str, Any]] = None,
        metrics: Optional[Dict[str, float]] = None,
        epoch: int = 0,
        tag: Optional[str] = None
    ) -> Path:
        """
        Atomically saves a model checkpoint along with calibration metadata and SHA-256 integrity seal.
        """
        timestamp_str = time.strftime("%Y%m%d_%H%M%S")
        tag_str = f"_{tag}" if tag else ""
        filename = f"cstgb_{dataset_name}{tag_str}_{timestamp_str}.pt"
        checkpoint_path = self.base_dir / filename
        meta_path = self.base_dir / f"cstgb_{dataset_name}{tag_str}_{timestamp_str}.meta.json"

        checkpoint_payload = {
            "model_state_dict": model.state_dict(),
            "epoch": epoch,
            "dataset_name": dataset_name,
            "architecture": model.__class__.__name__,
            "conformal_quantiles": conformal_quantiles or {"alpha_0.01": 0.99, "alpha_0.05": 0.95},
            "hyperparameters": hyperparameters or {},
            "metrics": metrics or {},
            "timestamp": time.time(),
            "pytorch_version": torch.__version__
        }

        if optimizer is not None:
            checkpoint_payload["optimizer_state_dict"] = optimizer.state_dict()
        if scheduler is not None and hasattr(scheduler, "state_dict"):
            checkpoint_payload["scheduler_state_dict"] = scheduler.state_dict()

        # Atomic write
        temp_path = checkpoint_path.with_suffix(".tmp")
        torch.save(checkpoint_payload, temp_path)
        if temp_path.exists():
            temp_path.replace(checkpoint_path)

        # Cryptographic checksum for model governance
        sha256_seal = self._compute_sha256(checkpoint_path)

        metadata = {
            "checkpoint_file": filename,
            "sha256_digest": sha256_seal,
            "dataset_name": dataset_name,
            "architecture": model.__class__.__name__,
            "epoch": epoch,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "conformal_quantiles": conformal_quantiles or {},
            "metrics": metrics or {},
            "hyperparameters": hyperparameters or {}
        }

        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        logger.info(
            "Model checkpoint saved successfully",
            checkpoint=str(checkpoint_path),
            sha256=sha256_seal[:16] + "...",
            dataset=dataset_name
        )
        return checkpoint_path

    def load_checkpoint(
        self,
        checkpoint_path: Union[str, Path],
        model: Optional[nn.Module] = None,
        optimizer: Optional[torch.optim.Optimizer] = None,
        device: str = "cpu",
        strict_sha256: bool = True
    ) -> Dict[str, Any]:
        """
        Loads checkpoint with cryptographic integrity verification.
        """
        path = Path(checkpoint_path)
        if not path.exists():
            raise FileNotFoundError(f"Checkpoint not found at {path}")

        meta_path = path.with_suffix(".meta.json")
        if strict_sha256 and meta_path.exists():
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            expected_sha = meta.get("sha256_digest")
            actual_sha = self._compute_sha256(path)
            if expected_sha and actual_sha != expected_sha:
                raise ValueError(
                    f"CRITICAL: Checkpoint integrity verification failed! "
                    f"Expected SHA-256 {expected_sha} but found {actual_sha}."
                )

        payload = torch.load(path, map_location=torch.device(device), weights_only=False)

        if model is not None and "model_state_dict" in payload:
            model.load_state_dict(payload["model_state_dict"])
            logger.info("Restored model weights into target architecture", architecture=model.__class__.__name__)

        if optimizer is not None and "optimizer_state_dict" in payload:
            optimizer.load_state_dict(payload["optimizer_state_dict"])

        return payload

    def list_checkpoints(self, dataset_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lists all registered checkpoints matching query filter."""
        results = []
        for meta_file in sorted(self.base_dir.glob("*.meta.json"), reverse=True):
            try:
                with open(meta_file, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                if dataset_name and meta.get("dataset_name") != dataset_name:
                    continue
                results.append(meta)
            except Exception:
                continue
        return results


checkpoint_manager = CheckpointManager()
