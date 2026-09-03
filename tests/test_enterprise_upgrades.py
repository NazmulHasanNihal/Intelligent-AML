import pytest
import numpy as np
import torch
import torch.nn.functional as F

from src.models.burst_aware_hgt_conv import BurstAwareHGTConv
from src.utils.conformal import ClassConditionalConformalTriager, TwoTierConformalTriager
from src.utils.streaming import TopKDegreeCapper, DynamicTemporalSlidingWindow


def test_multiscale_temporal_conv_forward():
    """Verifies that Multi-Scale Tri-Band temporal attention executes smoothly with backprop."""
    conv = BurstAwareHGTConv(in_channels=32, out_channels=32, num_heads=4)
    
    num_nodes = 50
    num_edges = 200
    x = torch.randn(num_nodes, 32)
    edge_index = torch.randint(0, num_nodes, (2, num_edges))
    
    # Mix of microsecond bursts (dt=0.01), diurnal gaps (dt=24.0), and long-dwell hibernation (dt=1000.0)
    delta_t = torch.tensor([0.01 if i % 3 == 0 else (24.0 if i % 3 == 1 else 1000.0) for i in range(num_edges)], dtype=torch.float)
    burst_score = torch.randn(num_edges)
    
    out = conv(x, edge_index, delta_t, burst_score)
    assert out.shape == (num_nodes, 32)
    assert not torch.isnan(out).any()
    
    # Backward pass verification
    loss = out.sum()
    loss.backward()
    assert conv.temporal_band_weights.grad is not None
    assert conv.raw_lambda_burst.grad is not None
    assert conv.raw_lambda_diurnal.grad is not None
    assert conv.raw_lambda_seasonal.grad is not None


def test_edge_gated_anti_camouflage():
    """Verifies that the MLP edge-gated filter suppresses synthetic camouflage links."""
    conv = BurstAwareHGTConv(in_channels=32, out_channels=32, num_heads=4, cam_residual_floor=0.10)
    
    x = torch.randn(10, 32)
    edge_index = torch.tensor([[0, 1, 2], [5, 5, 5]], dtype=torch.long)
    delta_t = torch.tensor([1.0, 50.0, 500.0], dtype=torch.float)
    burst_score = torch.tensor([5.0, 0.1, 0.0], dtype=torch.float)
    
    out = conv(x, edge_index, delta_t, burst_score)
    assert out.shape == (10, 32)
    assert not torch.isnan(out).any()


def test_class_conditional_conformal_triager():
    """Verifies that Class-Conditional CRC bounds clean and illicit error rates separately."""
    np.random.seed(42)
    # Severe 1:500 class imbalance
    n_samples = 5000
    y_true = np.zeros(n_samples, dtype=int)
    y_true[:10] = 1  # 0.2% positive prevalence
    
    # Simulated calibrated probabilities
    probs = np.random.beta(0.5, 30.0, size=n_samples)
    probs[:10] = np.random.beta(15.0, 1.0, size=10)  # Fraud scores high
    
    triager = ClassConditionalConformalTriager(alpha_clean=0.01, alpha_illicit=0.05)
    triager.calibrate(probs, y_true)
    
    metrics = triager.evaluate_crc_metrics(probs, y_true)
    
    assert metrics["conditional_coverage_clean"] >= 0.98, "Clean coverage must be >= 98%"
    assert metrics["conditional_coverage_illicit"] >= 0.90, "Illicit recall must be high"
    assert metrics["tier1_precision"] >= 0.85, "Tier 1 precision should be high"
    assert metrics["tier2_analyst_queue_pct"] < 0.05, "Analyst queue must not saturate (<5%)"


def test_topk_degree_capper():
    """Verifies that TopK degree capping eliminates candidate explosion on dense hubs."""
    capper = TopKDegreeCapper(max_degree=10)
    
    # Dense hub: node 99 receives 200 incoming edges
    srcs = torch.arange(200)
    dsts = torch.full((200,), 99, dtype=torch.long)
    edge_index = torch.stack([srcs, dsts])
    delta_t = torch.linspace(0.1, 100.0, 200)
    amounts = torch.linspace(10.0, 5000.0, 200)
    burst = torch.linspace(0.0, 10.0, 200)
    
    capped_edge, capped_dt, capped_amt, capped_burst = capper.cap_temporal_edges(
        edge_index, delta_t, amounts, burst
    )
    
    # Exactly max_degree edges retained for destination node 99
    assert capped_edge.shape[1] == 10
    assert (capped_edge[1] == 99).all()
    # Retained edges should be prioritized (highest recency / burst / amount)
    assert capped_dt.max() < delta_t.max()


def test_dynamic_temporal_sliding_window():
    """Verifies that DynamicTemporalSlidingWindow evicts outdated transactions in O(1) time."""
    window = DynamicTemporalSlidingWindow(window_seconds=3600.0, max_edges=100)
    
    # Insert transactions over a 3-hour period
    for i in range(150):
        # Timestamp in seconds: from t=0 to t=10,800 (3 hours)
        t = float(i * 72)
        window.add_transaction(src=i, dst=i+1, timestamp=t, amount=100.0 + i)
        
    tensors = window.get_active_graph_tensors()
    
    # Outdated edges (older than 3600s from current_t) must be evicted
    assert tensors["window_edge_count"] <= 51
    assert tensors["delta_t"].max() <= 3600.0
