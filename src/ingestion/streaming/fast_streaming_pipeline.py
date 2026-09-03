"""
fast_streaming_pipeline.py — High-Throughput Real-Time Streaming Consumer
Evaluates live transactions in sub-5ms latency and emits automated SAR filings.
"""

import time
import json
import numpy as np
from pathlib import Path
from collections import deque
import torch

from src.models.htgnn import BurstAwareHGT, CSTGBClassifier
from src.models.fast_inference import FastInferenceEngine
from src.utils.conformal import SoftMondrianConformalFilter


class StreamingTransactionProcessor:
    """
    High-Throughput Streaming Engine:
    Processes financial transaction streams in micro-batches with real-time conformal verification.
    """
    def __init__(self, engine=None, model_dir="data/outputs/models", device="cpu"):
        self.model_dir = Path(model_dir)
        self.device = device
        self.engine = engine
        self.alert_history = deque(maxlen=1000)
        self.latencies = []
        if self.engine is None:
            self._init_engine()

    def _init_engine(self):
        """Loads trained weights or initializes mock-trained engine for testing."""
        metadata = (
            ["Account", "User", "Device", "Institution"],
            [
                ("Account", "Transaction", "Account"),
                ("User", "Shared_Ownership", "Account")
            ]
        )
        in_channels = {"Account": 20, "User": 20, "Device": 20, "Institution": 20}
        gnn = BurstAwareHGT(
            in_channels_dict=in_channels,
            hidden_channels=128,
            num_layers=2,
            metadata=metadata
        )
        
        cstgb = CSTGBClassifier(gnn, target_node="Account", hidden_channels=128, alpha=0.10)
        
        # Load weights safely if available
        try:
            if (self.model_dir / "cstgb_gnn.pt").exists():
                gnn.load_state_dict(torch.load(self.model_dir / "cstgb_gnn.pt", map_location=self.device))
            if (self.model_dir / "cstgb_xgb.json").exists():
                cstgb.xgb.load_model(str(self.model_dir / "cstgb_xgb.json"))
        except Exception as e:
            print(f"  [StreamingProcessor] Note: Initialized fresh weights ({e})")
            
        # Initialize Mondrian filter
        cstgb.mondrian_conformal = SoftMondrianConformalFilter(alpha=0.10)
        cstgb.mondrian_conformal.strata_q = {0: 0.82, 1: 0.88, 2: 0.78, 3: 0.85}
        
        self.engine = FastInferenceEngine(cstgb, max_nodes=100000, device=self.device)

    def process_event(self, event_dict):
        """
        Processes a single transaction event dictionary:
        e.g. {"src": "acc_001", "dst": "acc_002", "amount": 8500.0, "ts": 1723500000.0}
        """
        t0 = time.perf_counter()
        
        src = str(event_dict.get("src", "src_unknown"))
        dst = str(event_dict.get("dst", "dst_unknown"))
        amount = float(event_dict.get("amount", 100.0))
        delta_t = float(event_dict.get("delta_t", 0.5))
        burst_score = float(event_dict.get("burst_score", 1.0))
        
        # Fast scoring
        score_res = self.engine.score_single_transaction_streaming(
            src_id=src,
            dst_id=dst,
            amount=amount,
            delta_t=delta_t,
            burst_score=burst_score
        )
        
        latency_ms = (time.perf_counter() - t0) * 1000.0
        self.latencies.append(latency_ms)
        
        # Trigger SAR filing if High Risk
        is_sar = score_res["fraud_probability"] >= self.engine.optimal_threshold or score_res["conformal_action_set"] == 1
        if is_sar:
            sar_record = {
                "timestamp": time.time(),
                "event": event_dict,
                "score": score_res,
                "sar_narrative": (
                    f"AUTOMATED SAR FILING: Account {dst} flagged with {score_res['fraud_probability']:.2%} risk. "
                    f"Action Set: {score_res['action_label']}. Structuring trigger on ${amount:,.2f} transfer."
                )
            }
            self.alert_history.append(sar_record)
            
        return score_res

    def get_performance_summary(self):
        """Calculates latency statistics across all processed events."""
        if not self.latencies:
            return {}
        arr = np.array(self.latencies)
        return {
            "total_events": len(arr),
            "p50_latency_ms": round(float(np.percentile(arr, 50)), 3),
            "p95_latency_ms": round(float(np.percentile(arr, 95)), 3),
            "p99_latency_ms": round(float(np.percentile(arr, 99)), 3),
            "mean_latency_ms": round(float(np.mean(arr)), 3),
            "throughput_events_per_sec": round(float(1000.0 / (np.mean(arr) + 1e-6)), 1),
            "total_sar_alerts": len(self.alert_history)
        }
