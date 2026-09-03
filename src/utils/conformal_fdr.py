"""
conformal_fdr.py — Finite-Sample False Discovery Rate (FDR) Conformal Risk Control.
Guarantees mathematically bounded False Positive rates for Financial Intelligence Units (FIUs).

References:
1. Benjamini & Hochberg. "Controlling the False Discovery Rate: a Practical and Powerful Approach to Multiple Testing" (JRSS-B).
2. Bates et al. "Distribution-Free Multiple Testing with Conformal p-Values" (JMLR).
3. Angelopoulos et al. "Learn then Test: Calibrating Predictive Algorithms to Achieve Risk Control" (arXiv).
"""

import numpy as np
import torch
from typing import Dict, List, Tuple, Optional, Union, Any


class BenjaminiHochbergConformalFDR:
    """
    Benjamini-Hochberg Conformal False Discovery Rate (FDR) Controller.
    
    Transforms raw AML risk scores into valid non-parametric conformal p-values,
    then determines exact decision cutoffs guaranteeing that expected False Discovery Rate
    FDR = E[FP / max(1, TP + FP)] <= q_target (e.g., q* = 0.01 or 0.05).
    """
    def __init__(self, q_target: float = 0.05, method: str = "BH"):
        self.q_target = float(q_target)
        self.method = method.upper()  # "BH" (Independent/PRDS) or "BY" (Arbitrary Dependency)
        self.calib_null_scores: Optional[np.ndarray] = None

    def calibrate(self, calib_scores: Union[np.ndarray, torch.Tensor], calib_labels: Union[np.ndarray, torch.Tensor]):
        """
        Calibrates using non-conformity scores on clean/licit accounts (Null Hypothesis H_0).
        Non-conformity score s_i = p(fraud | x_i) or -p(clean | x_i).
        """
        if isinstance(calib_scores, torch.Tensor):
            s = calib_scores.detach().cpu().numpy().flatten()
        else:
            s = np.asarray(calib_scores).flatten()

        if isinstance(calib_labels, torch.Tensor):
            y = calib_labels.detach().cpu().numpy().flatten()
        else:
            y = np.asarray(calib_labels).flatten()

        # Isolate null distribution (Licit clean accounts: y == 0)
        null_mask = (y == 0)
        if np.sum(null_mask) == 0:
            self.calib_null_scores = s
        else:
            self.calib_null_scores = s[null_mask]

        self.calib_null_scores = np.sort(self.calib_null_scores)

    def compute_conformal_p_values(self, test_scores: Union[np.ndarray, torch.Tensor]) -> np.ndarray:
        """
        Computes distribution-free conformal p-values for test transactions:
        p_i = (1 + sum_{j=1}^N I(s_j^{null} >= s_i)) / (N + 1)
        """
        if self.calib_null_scores is None or len(self.calib_null_scores) == 0:
            raise ValueError("Conformal FDR controller must be calibrated before computing p-values.")

        if isinstance(test_scores, torch.Tensor):
            scores = test_scores.detach().cpu().numpy().flatten()
        else:
            scores = np.asarray(test_scores).flatten()

        n_cal = len(self.calib_null_scores)
        
        # Vectorized p-value search: count how many null scores >= score_i
        # Equivalent to: (n_cal - searchsorted(null_scores, score_i) + 1) / (n_cal + 1)
        idx = np.searchsorted(self.calib_null_scores, scores, side='left')
        count_greater_equal = n_cal - idx
        p_values = (count_greater_equal + 1.0) / (n_cal + 1.0)
        
        return np.clip(p_values, 1.0 / (n_cal + 1.0), 1.0)

    def select_alerts(
        self,
        test_scores: Union[np.ndarray, torch.Tensor],
        q_target: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Applies Benjamini-Hochberg (BH) or Benjamini-Yekutieli (BY) multiple testing step-up procedure.
        
        Returns dictionary containing:
        - 'alert_mask': Boolean array indicating flagged high-certainty alerts
        - 'p_values': Conformal p-values
        - 'cutoff_p_value': The threshold p-value p_(k*)
        - 'num_discoveries': Total number of flagged cases
        """
        q = float(q_target) if q_target is not None else self.q_target
        p_vals = self.compute_conformal_p_values(test_scores)
        m = len(p_vals)

        if m == 0:
            return {
                "alert_mask": np.zeros(0, dtype=bool),
                "p_values": p_vals,
                "cutoff_p_value": 0.0,
                "num_discoveries": 0
            }

        # Sort p-values in ascending order
        sort_idx = np.argsort(p_vals)
        p_sorted = p_vals[sort_idx]

        # Multi-testing thresholds
        k_indices = np.arange(1, m + 1)
        if self.method == "BY":
            # Benjamini-Yekutieli correction for arbitrary graph dependency structures
            c_m = np.sum(1.0 / k_indices)
            thresholds = (k_indices / m) * (q / c_m)
        else:
            # Standard Benjamini-Hochberg (BH)
            thresholds = (k_indices / m) * q

        # Step-up condition: find largest k such that p_(k) <= (k/m) * q
        valid_k = np.where(p_sorted <= thresholds)[0]

        if len(valid_k) > 0:
            k_star = valid_k[-1]  # Largest satisfying index
            cutoff_p = float(p_sorted[k_star])
            alert_indices = sort_idx[:k_star + 1]
            
            alert_mask = np.zeros(m, dtype=bool)
            alert_mask[alert_indices] = True
            num_discoveries = len(alert_indices)
        else:
            cutoff_p = 0.0
            alert_mask = np.zeros(m, dtype=bool)
            num_discoveries = 0

        return {
            "alert_mask": alert_mask,
            "p_values": p_vals,
            "cutoff_p_value": cutoff_p,
            "num_discoveries": num_discoveries,
            "guaranteed_fdr": q
        }

    def evaluate_empirical_fdr(self, alert_mask: np.ndarray, y_true: np.ndarray) -> Dict[str, float]:
        """Calculates realized Empirical False Discovery Rate (FDR) and Precision."""
        y = np.asarray(y_true).flatten()
        mask = np.asarray(alert_mask).flatten()

        num_flagged = int(np.sum(mask))
        if num_flagged == 0:
            return {"empirical_fdr": 0.0, "precision": 1.0, "true_positives": 0, "false_positives": 0}

        true_pos = int(np.sum(mask & (y == 1)))
        false_pos = int(np.sum(mask & (y == 0)))
        empirical_fdr = false_pos / num_flagged
        precision = true_pos / num_flagged

        return {
            "empirical_fdr": float(empirical_fdr),
            "precision": float(precision),
            "true_positives": true_pos,
            "false_positives": false_pos,
            "total_alerts": num_flagged
        }
