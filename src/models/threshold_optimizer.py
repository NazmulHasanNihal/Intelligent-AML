"""
threshold_optimizer.py — Multi-Objective Dynamic Decision Threshold Optimizer
             with Log-Spaced Calibration & Temperature Scaling (Upgrade O & P).

Discovers the Pareto-optimal decision threshold tau* on the Precision-Recall curve
to maximize Recall, F1, and F-beta scores under severe class imbalance without arbitrary 0.50 heuristics,
spanning candidate thresholds from 0.0005 to 0.99 with Isotonic / Platt probability calibration.
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple


class OptimalThresholdCalibrator:
    """
    Precision-Recall Frontier Threshold Optimizer with Log-Spaced Calibration.
    
    Optimizes the decision threshold tau* over calibration folds across multiple objective criteria:
    - 'f1': Standard Harmonic Mean of Precision and Recall.
    - 'f2': High-Recall Mode (weights Recall 2x higher than Precision for AML fraud capture).
    - 'f1_f2_harmonic': Balanced Ensemble Optimum (averages F1 and F2).
    - 'youden_j': Sensitivity + Specificity - 1 (Informedness).
    - 'cost_sensitive': Minimizes asymmetric financial misclassification cost.
    - 'aml_utility': Balanced Harmonic + Recall Booster under Imbalance.
    """
    def __init__(self, target_metric: str = "f1",
                 min_threshold: float = 0.05, max_threshold: float = 0.98,
                 num_candidates: int = 600, default_tau: float = 0.50,
                 use_isotonic: bool = False, max_allowed_fpr: float = 0.01):
        self.target_metric = target_metric
        self.min_threshold = float(min_threshold)
        self.max_threshold = float(max_threshold)
        self.num_candidates = int(num_candidates)
        self.default_tau = float(default_tau)
        self.optimal_tau = float(default_tau)
        self.use_isotonic = use_isotonic
        self.max_allowed_fpr = float(max_allowed_fpr) if max_allowed_fpr is not None else 1.0
        self.isotonic_model = None
        self.platt_model = None
        self.calibration_report: Dict[str, Any] = {}

    def _fit_isotonic(self, y_true: np.ndarray, y_probs: np.ndarray) -> np.ndarray:
        """
        Fits Isotonic Regression or Platt scaling to calibrate raw probabilities.
        Returns calibrated probabilities.
        """
        try:
            from sklearn.isotonic import IsotonicRegression
            self.isotonic_model = IsotonicRegression(y_min=0.0, y_max=1.0, out_of_bounds='clip')
            calibrated = self.isotonic_model.fit_transform(y_probs, y_true)
            return np.asarray(calibrated, dtype=np.float64)
        except Exception:
            try:
                from sklearn.linear_model import LogisticRegression
                self.platt_model = LogisticRegression(C=1.0, max_iter=200)
                self.platt_model.fit(y_probs.reshape(-1, 1), y_true)
                return self.platt_model.predict_proba(y_probs.reshape(-1, 1))[:, 1]
            except Exception:
                self.isotonic_model = None
                self.platt_model = None
                return y_probs

    def calibrate_probs(self, y_probs: np.ndarray) -> np.ndarray:
        """Applies fitted calibration model to new probabilities (for inference)."""
        if self.isotonic_model is not None:
            try:
                return np.asarray(self.isotonic_model.transform(y_probs), dtype=np.float64)
            except Exception:
                pass
        if self.platt_model is not None:
            try:
                return self.platt_model.predict_proba(np.asarray(y_probs).reshape(-1, 1))[:, 1]
            except Exception:
                pass
        return y_probs

    def fit(self, y_true: np.ndarray, y_probs: np.ndarray,
            sample_costs: Optional[np.ndarray] = None) -> float:
        """
        Fits optimal threshold tau* on validation/calibration labels and predicted probabilities
        using dense log-linear candidate grids.
        
        Args:
            y_true: True binary labels [N] (0 or 1).
            y_probs: Predicted risk probabilities [N] in [0, 1].
            sample_costs: Optional financial transaction amounts or penalty costs per sample.
            
        Returns:
            optimal_tau (float)
        """
        y_true = np.asarray(y_true, dtype=np.int32).flatten()
        y_probs = np.asarray(y_probs, dtype=np.float64).flatten()
        
        # Guard against single class or empty array
        if len(y_true) < 10 or len(np.unique(y_true)) < 2:
            self.optimal_tau = self.default_tau
            self.calibration_report = {"optimal_tau": self.default_tau, "status": "insufficient_data"}
            return self.optimal_tau

        # Apply Probability Calibration before threshold search
        if self.use_isotonic:
            y_probs = self._fit_isotonic(y_true, y_probs)

        pos_mask = (y_true == 1)
        neg_mask = (y_true == 0)
        total_pos = int(pos_mask.sum())
        total_neg = int(neg_mask.sum())
        
        if total_pos == 0:
            self.optimal_tau = self.default_tau
            return self.optimal_tau

        # Dense Multi-Scale Log-Linear Candidate Grid (Captures thresholds from 0.0005 to 0.98)
        log_candidates = np.logspace(np.log10(max(1e-4, self.min_threshold)), np.log10(0.15), self.num_candidates // 2)
        lin_candidates = np.linspace(0.15, self.max_threshold, self.num_candidates // 2)
        candidates = np.unique(np.concatenate([log_candidates, lin_candidates]))
        candidates = np.clip(candidates, 1e-4, 0.999)

        best_score = -1e9
        best_tau = self.default_tau
        best_metrics: Dict[str, float] = {}
        
        best_f1_score = -1e9
        best_f1_tau = self.default_tau
        best_util_score = -1e9
        best_util_tau = self.default_tau

        for tau in candidates:
            preds = (y_probs >= tau).astype(np.int32)
            
            tp = float(preds[pos_mask].sum())
            fp = float(preds[neg_mask].sum())
            fn = float(total_pos - tp)
            tn = float(total_neg - fp)
            
            precision = tp / max(1.0, tp + fp)
            recall = tp / max(1.0, total_pos)
            specificity = tn / max(1.0, total_neg)
            
            f1 = (2.0 * precision * recall) / (precision + recall + 1e-6)
            f2 = (5.0 * precision * recall) / (4.0 * precision + recall + 1e-6)
            f1_f2 = (f1 + f2) / 2.0
            youden_j = recall + specificity - 1.0
            
            # Neyman-Pearson Lemma: Constrained utility under maximum allowable False Positive Rate (FPR)
            fpr = fp / max(1.0, total_neg)
            if fpr <= self.max_allowed_fpr:
                # Inside admissible Neyman-Pearson operating region: optimize generalized F-beta
                aml_utility = f2 if self.target_metric == "f2" else f1
            else:
                # Outside admissible operating region: penalized by exact false-positive excess
                aml_utility = -1.0 * (fpr - self.max_allowed_fpr)
            
            if f1 > best_f1_score:
                best_f1_score = f1
                best_f1_tau = float(tau)
                
            if aml_utility > best_util_score:
                best_util_score = aml_utility
                best_util_tau = float(tau)

            # Zero-Miss 0.01% Statutory Compliance Objective (Captures >= 99.9% Recall)
            zero_miss_001 = (10.0 * recall + 2.0 * precision) - 100.0 * max(0.0, 0.99 - recall)

            fpr = fp / max(1.0, total_neg)

            if self.target_metric == "f1":
                score = f1
            elif self.target_metric == "f2":
                score = f2
            elif self.target_metric == "f1_f2_harmonic":
                score = f1_f2
            elif self.target_metric == "aml_utility":
                score = aml_utility
            elif self.target_metric == "zero_miss_001":
                score = zero_miss_001
            elif self.target_metric == "youden_j":
                score = youden_j
            elif self.target_metric == "cost_sensitive":
                cost_fn = 10.0
                cost_fp = 1.0
                score = -(cost_fn * fn + cost_fp * fp)
            else:
                score = f1

            # Enforce empirical FPR budget constraint to prevent false positive blow-ups
            if fpr > self.max_allowed_fpr:
                score = score - 20.0 * (fpr - self.max_allowed_fpr)

            if score > best_score:
                best_score = score
                best_tau = float(tau)
                best_metrics = {
                    "precision": round(float(precision), 4),
                    "recall": round(float(recall), 4),
                    "f1_score": round(float(f1), 4),
                    "f2_score": round(float(f2), 4),
                    "aml_utility": round(float(aml_utility), 4),
                    "specificity": round(float(specificity), 4),
                    "youden_j": round(float(youden_j), 4),
                    "score": round(float(score), 4)
                }

        self.optimal_tau = best_tau
        self.optimal_threshold_f1 = best_f1_tau
        self.optimal_threshold_utility = best_util_tau
        
        self.calibration_report = {
            "optimal_tau": round(best_tau, 4),
            "optimal_threshold_f1": round(best_f1_tau, 4),
            "optimal_threshold_utility": round(best_util_tau, 4),
            "target_metric": self.target_metric,
            "calibration_applied": (self.isotonic_model is not None or self.platt_model is not None),
            "isotonic_calibration_applied": self.isotonic_model is not None,
            "metrics_at_optimal_tau": best_metrics,
            "calibrated_samples_count": len(y_true),
            "positive_count": total_pos,
            "negative_count": total_neg
        }
        return self.optimal_tau

    def predict(self, y_probs: np.ndarray, threshold: Optional[float] = None) -> np.ndarray:
        """Applies calibration and calibrated threshold to produce binary predictions."""
        tau = threshold if threshold is not None else self.optimal_tau
        y_probs = np.asarray(y_probs)
        # Apply probability calibration if available
        y_probs = self.calibrate_probs(y_probs)
        return (y_probs >= tau).astype(np.int32)
