"""
Continuous Learning Module for Enterprise AML:
1. Elastic Weight Consolidation (EWC) with Diagonal Fisher Information Matrix
2. Topological Reservoir Memory Buffer for Experience Replay
3. Continual Spatio-Temporal Model Updater
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Dict, List, Optional, Tuple


class ElasticWeightConsolidation:
    """
    Elastic Weight Consolidation (EWC) for Graph Neural Networks (Kirkpatrick et al., PNAS 2017).
    Prevents catastrophic forgetting by penalizing changes to parameters that were critical
    for past money laundering topology detection using the empirical Fisher Information Matrix.
    """
    def __init__(self, model: nn.Module, dataloader_or_batches: List, target_node: str = "Account", device: str = "cpu"):
        self.model = model
        self.target_node = target_node
        self.device = device
        self.params = {n: p for n, p in model.named_parameters() if p.requires_grad}
        self._stored_params = {n: p.clone().detach() for n, p in self.params.items()}
        self._fisher_matrix = self._compute_fisher(dataloader_or_batches)

    def _compute_fisher(self, batches: List) -> Dict[str, torch.Tensor]:
        fisher = {n: torch.zeros_like(p, device=self.device) for n, p in self.params.items()}
        if not batches:
            return fisher

        self.model.eval()
        total_samples = 0

        for batch in batches:
            self.model.zero_grad()
            try:
                x_dict, edge_index_dict, delta_t_dict, burst_score_dict, y_target = batch
                out_dict = self.model(x_dict, edge_index_dict, delta_t_dict, burst_score_dict)
                logits = out_dict[self.target_node]
                
                # Empirical Fisher from log-likelihood
                log_probs = F.log_softmax(logits, dim=1)
                labels = y_target[y_target >= 0]
                if len(labels) == 0:
                    continue

                valid_logits = log_probs[y_target >= 0]
                nll = F.nll_loss(valid_logits, labels)
                nll.backward()

                for n, p in self.model.named_parameters():
                    if p.grad is not None and n in fisher:
                        fisher[n] += p.grad.data.pow(2) * len(labels)
                total_samples += len(labels)
            except Exception:
                continue

        if total_samples > 0:
            for n in fisher:
                fisher[n] /= total_samples

        return fisher

    def penalty(self, new_model: nn.Module) -> torch.Tensor:
        """Computes the quadratic penalty over parameter shift weighted by Fisher Information."""
        loss = torch.tensor(0.0, device=self.device)
        for n, p in new_model.named_parameters():
            if n in self._fisher_matrix and n in self._stored_params:
                _fisher = self._fisher_matrix[n].to(p.device)
                _stored = self._stored_params[n].to(p.device)
                loss = loss + (_fisher * (p - _stored).pow(2)).sum()
        return 0.5 * loss


class TopologicalReservoirBuffer:
    """
    Reservoir sampling memory buffer storing historical rare fraud typologies
    and boundary cases for topological experience replay during continual updates.
    """
    def __init__(self, capacity: int = 5000, minority_ratio: float = 0.5):
        self.capacity = capacity
        self.minority_ratio = minority_ratio
        self.buffer_licit: List[Tuple] = []
        self.buffer_illicit: List[Tuple] = []
        self.total_seen_licit = 0
        self.total_seen_illicit = 0

    def add(self, x_tuple: Tuple, y_label: int):
        """Adds a sample via reservoir sampling."""
        if y_label == 1:
            self.total_seen_illicit += 1
            max_illicit = int(self.capacity * self.minority_ratio)
            if len(self.buffer_illicit) < max_illicit:
                self.buffer_illicit.append(x_tuple)
            else:
                idx = np.random.randint(0, self.total_seen_illicit)
                if idx < max_illicit:
                    self.buffer_illicit[idx] = x_tuple
        else:
            self.total_seen_licit += 1
            max_licit = self.capacity - int(self.capacity * self.minority_ratio)
            if len(self.buffer_licit) < max_licit:
                self.buffer_licit.append(x_tuple)
            else:
                idx = np.random.randint(0, self.total_seen_licit)
                if idx < max_licit:
                    self.buffer_licit[idx] = x_tuple

    def add_with_priority(self, x_tuple: Tuple, y_label: int, prediction_error: float = 1.0):
        """
        Adds a sample with priority weighting proportional to model prediction error.
        Hard boundary cases (False Positives and False Negatives) receive higher admission probability.
        """
        err_clamped = float(np.clip(abs(prediction_error), 0.0, 1.0))
        # Hard examples get up to 4x admission probability multiplier
        priority_prob = min(1.0, 0.25 + 0.75 * err_clamped)
        if np.random.rand() <= priority_prob:
            self.add(x_tuple, y_label)

    def sample(self, n: int) -> Tuple[List, List]:
        """Samples a balanced historical replay batch."""
        n_illicit = min(len(self.buffer_illicit), n // 2)
        n_licit = min(len(self.buffer_licit), n - n_illicit)
        
        idx_ill = np.random.choice(len(self.buffer_illicit), n_illicit, replace=False) if n_illicit > 0 else []
        idx_lic = np.random.choice(len(self.buffer_licit), n_licit, replace=False) if n_licit > 0 else []
        
        samples_x = [self.buffer_illicit[i] for i in idx_ill] + [self.buffer_licit[i] for i in idx_lic]
        samples_y = [1] * len(idx_ill) + [0] * len(idx_lic)
        
        return samples_x, samples_y




class ContinuousLearningEngine:
    """
    Coordinates closed-loop continuous learning in production:
    - Retains prior graph topological representations via EWC
    - Samples past exemplars via Reservoir Replay
    - Interacts with DelayedFeedbackPipeline to update PID-ACI calibration bounds
    """
    def __init__(self, gnn_model: nn.Module, ewc_lambda: float = 400.0, buffer_capacity: int = 10000):
        self.gnn_model = gnn_model
        self.ewc_lambda = ewc_lambda
        self.reservoir = TopologicalReservoirBuffer(capacity=buffer_capacity)
        self.ewc_history: List[ElasticWeightConsolidation] = []

    def snapshot_task_knowledge(self, exemplar_batches: List, target_node: str = "Account"):
        """Computes and stores Fisher information for the current task/time window."""
        ewc = ElasticWeightConsolidation(self.gnn_model, exemplar_batches, target_node=target_node)
        self.ewc_history.append(ewc)
        # Retain only the most recent task checkpoints
        if len(self.ewc_history) > 3:
            self.ewc_history.pop(0)

    def get_continual_penalty(self) -> torch.Tensor:
        """Aggregates regularizer penalties across all historical task snapshots."""
        total_penalty = torch.tensor(0.0)
        for ewc in self.ewc_history:
            total_penalty = total_penalty + ewc.penalty(self.gnn_model)
        return self.ewc_lambda * total_penalty


class DarkExperienceReplayBuffer:
    """
    Dark Experience Replay (DER++) Memory Buffer for Spatio-Temporal Graph Continual Learning.
    Reference: Buzzega et al. "Dark Experience for General Continual Learning: a Strong, Simple Baseline" (NeurIPS).
    
    Stores prototypical transaction graph exemplars alongside their:
    - Node representations x_i
    - Uncalibrated teacher model logits z_i (Dark Knowledge)
    - Ground-truth binary labels y_i
    - Temporal occurrence timestamps t_i
    """
    def __init__(self, capacity: int = 4000, alpha: float = 0.5, beta: float = 0.5):
        self.capacity = capacity
        self.alpha = float(alpha)  # Weight on logit MSE consistency loss
        self.beta = float(beta)    # Weight on label BCE classification loss
        self.x_buf: List[torch.Tensor] = []
        self.logits_buf: List[torch.Tensor] = []
        self.y_buf: List[torch.Tensor] = []
        self.total_seen = 0

    def add(self, x: torch.Tensor, logits: torch.Tensor, y: torch.Tensor):
        """Adds a batch of samples into the episodic memory buffer using reservoir sampling."""
        x_cpu = x.detach().cpu()
        logits_cpu = logits.detach().cpu()
        y_cpu = y.detach().cpu()

        batch_size = x_cpu.shape[0]
        for i in range(batch_size):
            self.total_seen += 1
            if len(self.x_buf) < self.capacity:
                self.x_buf.append(x_cpu[i])
                self.logits_buf.append(logits_cpu[i])
                self.y_buf.append(y_cpu[i])
            else:
                idx = np.random.randint(0, self.total_seen)
                if idx < self.capacity:
                    self.x_buf[idx] = x_cpu[i]
                    self.logits_buf[idx] = logits_cpu[i]
                    self.y_buf[idx] = y_cpu[i]

    def sample(self, batch_size: int, device: torch.device) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Samples a random replay batch from episodic memory."""
        if len(self.x_buf) == 0:
            return torch.zeros(0, device=device), torch.zeros(0, device=device), torch.zeros(0, device=device)

        n = min(batch_size, len(self.x_buf))
        indices = np.random.choice(len(self.x_buf), n, replace=False)

        x_sampled = torch.stack([self.x_buf[i] for i in indices], dim=0).to(device)
        logits_sampled = torch.stack([self.logits_buf[i] for i in indices], dim=0).to(device)
        y_sampled = torch.stack([self.y_buf[i] for i in indices], dim=0).to(device)

        return x_sampled, logits_sampled, y_sampled

    def compute_der_loss(self, current_logits: torch.Tensor, past_logits: torch.Tensor, past_y: torch.Tensor) -> torch.Tensor:
        """
        Computes DER++ joint consistency and cross-entropy loss:
        L_DER++ = alpha * ||current_logits - past_logits||_2^2 + beta * CE(current_logits, past_y)
        """
        if current_logits.numel() == 0 or past_logits.numel() == 0:
            return torch.tensor(0.0, device=current_logits.device, requires_grad=True)

        # 1. Dark Knowledge Logits Distillation (Preserves subtle topological boundaries)
        mse_loss = F.mse_loss(current_logits, past_logits)

        # 2. Ground-Truth Classification Replay Loss
        if current_logits.dim() > 1 and current_logits.shape[-1] > 1:
            ce_loss = F.cross_entropy(current_logits, past_y.long())
        else:
            ce_loss = F.binary_cross_entropy_with_logits(current_logits.view(-1), past_y.float().view(-1))

        return self.alpha * mse_loss + self.beta * ce_loss

