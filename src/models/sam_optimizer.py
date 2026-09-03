"""
sam_optimizer.py — Sharpness-Aware Minimization (SAM) Optimizer.
Implements Foret et al. (ICLR 2021) Sharpness-Aware Minimization for GNN training.
Finds parameters in flat loss valleys with provably lower generalization error under
extreme class imbalance (< 0.1% fraud) and severe nonstationary concept drift.
"""

import torch
from typing import Dict, List, Tuple, Optional, Any, Callable


class SAMOptimizer(torch.optim.Optimizer):
    """
    Sharpness-Aware Minimization (SAM) Optimizer Wrapper.
    
    Optimizes the minimax objective:
        min_theta max_{||epsilon|| <= rho} L_{train}(theta + epsilon)
        
    Usage:
        optimizer = SAMOptimizer(model.parameters(), base_optimizer=torch.optim.AdamW, rho=0.05, lr=1e-3)
        
        # Training step:
        loss = criterion(model(x), y)
        loss.backward()
        optimizer.first_step(zero_grad=True)
        
        # Second forward-backward pass at perturbed weights:
        criterion(model(x), y).backward()
        optimizer.second_step(zero_grad=True)
    """
    def __init__(self, params, base_optimizer: Callable, rho: float = 0.05, adaptive: bool = False, **kwargs):
        assert rho >= 0.0, f"Invalid rho, should be non-negative: {rho}"
        
        defaults = dict(rho=rho, adaptive=adaptive, **kwargs)
        super(SAMOptimizer, self).__init__(params, defaults)
        
        self.base_optimizer = base_optimizer(self.param_groups, **kwargs)
        self.param_groups = self.base_optimizer.param_groups
        self.defaults.update(self.base_optimizer.defaults)

    @torch.no_grad()
    def first_step(self, zero_grad: bool = False):
        """
        Computes gradient-ascent perturbation epsilon and adds it to model parameters.
        """
        grad_norm = self._grad_norm()
        for group in self.param_groups:
            scale = group["rho"] / (grad_norm + 1e-12)
            
            for p in group["params"]:
                if p.grad is None:
                    continue
                self.state[p]["old_p"] = p.data.clone()
                e_w = (torch.pow(p, 2) if group["adaptive"] else 1.0) * p.grad * scale.to(p)
                p.add_(e_w)  # Climb to local loss peak: theta + epsilon
                
        if zero_grad:
            self.zero_grad()

    @torch.no_grad()
    def second_step(self, zero_grad: bool = False):
        """
        Restores original model parameters and performs the base optimizer step with perturbed gradients.
        """
        for group in self.param_groups:
            for p in group["params"]:
                if p.grad is None:
                    continue
                if "old_p" in self.state[p]:
                    p.data = self.state[p]["old_p"]  # Restore theta
                    
        self.base_optimizer.step()
        
        if zero_grad:
            self.zero_grad()

    @torch.no_grad()
    def step(self, closure: Optional[Callable] = None):
        """
        Single-call step if closure is provided.
        """
        assert closure is not None, "SAM requires a closure for single-call step()."
        closure = torch.enable_grad()(closure)
        
        # 1. Forward-backward at theta
        loss = closure()
        self.first_step(zero_grad=True)
        
        # 2. Forward-backward at theta + epsilon
        closure()
        self.second_step(zero_grad=True)
        
        return loss

    def _grad_norm(self) -> torch.Tensor:
        """Computes global L2 norm of gradients across all parameters."""
        shared_device = self.param_groups[0]["params"][0].device
        norms = []
        for group in self.param_groups:
            for p in group["params"]:
                if p.grad is not None:
                    grad = p.grad
                    if group["adaptive"]:
                        grad = torch.abs(p) * grad
                    norms.append(torch.norm(grad, p=2).to(shared_device))
                    
        if len(norms) == 0:
            return torch.tensor(0.0, device=shared_device)
        return torch.norm(torch.stack(norms), p=2)

    def load_state_dict(self, state_dict):
        super().load_state_dict(state_dict)
        self.base_optimizer.param_groups = self.param_groups
