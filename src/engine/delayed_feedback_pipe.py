"""
delayed_feedback_pipe.py — Streaming Delayed-Feedback Ingestion Pipeline.
Handles real-world asynchronous label latency (30–90 day confirmation lag)
and continuously drives PID-Adaptive Conformal Inference (PID-ACI) calibration.
"""

import time
import threading
from collections import deque
from typing import Dict, List, Tuple, Optional, Any, Set
import numpy as np
from src.utils.conformal import DelayedFeedbackACI, AdaptiveConformalInference


class DelayedFeedbackPipeline:
    """
    Asynchronous Delayed-Feedback Ingestion Pipe.
    Buffers scored transactions in chronological delay windows, ingests late-arriving
    SAR confirmations / chargebacks, and executes closed-loop PID-ACI recalibration.
    """
    def __init__(self, target_alpha: float = 0.10,
                 delay_horizon_batches: int = 5,
                 initial_q: float = 0.85,
                 governance_band: Tuple[float, float] = (0.70, 0.95)):
        self.target_alpha = target_alpha
        self.lock = threading.RLock()
        
        # Underlying PID-Controlled Adaptive Conformal Engine
        self.aci = DelayedFeedbackACI(
            alpha=target_alpha,
            delay_horizon=delay_horizon_batches,
            initial_q=initial_q,
            governance_band=governance_band
        )

        # Active Pending Transactions buffer: tx_id -> { 'prob': float, 'ts': float, 'batch_id': int }
        self.pending_transactions: Dict[str, Dict[str, Any]] = {}
        
        # Batch buffer for streaming feedback
        self.current_batch_probs: List[float] = []
        self.current_batch_labels: List[int] = []
        self.batch_size = 50
        
        # Telemetry metrics
        self.total_scored = 0
        self.total_resolved = 0
        self.calibration_steps_count = 0
        self.recent_error_rates: deque = deque(maxlen=100)

    def record_scored_transaction(self, tx_id: str, fraud_probability: float, 
                                  metadata: Optional[Dict[str, Any]] = None) -> None:
        """Buffers a newly scored transaction awaiting future SAR label confirmation."""
        with self.lock:
            self.pending_transactions[tx_id] = {
                "prob": float(fraud_probability),
                "timestamp": time.time(),
                "metadata": metadata or {}
            }
            self.total_scored += 1

    def resolve_label_feedback(self, tx_id: str, confirmed_ground_truth: int) -> Optional[float]:
        """
        Ingests delayed confirmed ground-truth label (e.g. from law enforcement / chargebacks)
        and executes PID-ACI adjustment when batch is full.
        Returns:
            Updated threshold bound (q_t) if a calibration step was executed, else None.
        """
        with self.lock:
            if tx_id not in self.pending_transactions:
                return None

            record = self.pending_transactions.pop(tx_id)
            prob = record["prob"]
            label = int(confirmed_ground_truth)

            self.current_batch_probs.append(prob)
            self.current_batch_labels.append(label)
            self.total_resolved += 1

            # Trigger calibration step once batch threshold is reached
            if len(self.current_batch_probs) >= self.batch_size:
                p_arr = np.array(self.current_batch_probs)
                y_arr = np.array(self.current_batch_labels)

                # Record into ACI and resolve
                self.aci.record_pending_batch(p_arr)
                new_q = self.aci.resolve_delayed_batch(y_arr)
                
                # Compute empirical batch coverage error
                covered = np.where(y_arr == 1, p_arr >= (1.0 - new_q), p_arr <= new_q)
                err = float(np.mean(~covered))
                self.recent_error_rates.append(err)
                self.calibration_steps_count += 1

                # Reset batch buffers
                self.current_batch_probs = []
                self.current_batch_labels = []

                return new_q

            return self.aci.q_t

    def get_current_threshold(self) -> float:
        """Returns the currently active, PID-calibrated confidence threshold."""
        with self.lock:
            return float(self.aci.q_t)

    def get_pipeline_telemetry(self) -> Dict[str, Any]:
        """Returns real-time streaming feedback telemetry and error rate statistics."""
        with self.lock:
            rolling_err = float(np.mean(self.recent_error_rates)) if self.recent_error_rates else self.target_alpha
            return {
                "current_q_t": round(float(self.aci.q_t), 4),
                "target_alpha": self.target_alpha,
                "empirical_error_rate": round(rolling_err, 4),
                "error_drift_gap": round(rolling_err - self.target_alpha, 4),
                "total_scored": self.total_scored,
                "total_resolved": self.total_resolved,
                "pending_queue_size": len(self.pending_transactions),
                "calibration_steps_executed": self.calibration_steps_count,
                "governance_band": [self.aci.gov_min, self.aci.gov_max]
            }
