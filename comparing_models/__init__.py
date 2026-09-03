import os
from pathlib import Path

if os.name == "nt":
    _root = Path(__file__).resolve().parent.parent
    _torch_lib = _root / "venv" / "Lib" / "site-packages" / "torch" / "lib"
    if _torch_lib.exists():
        os.environ["PATH"] = str(_torch_lib) + ";" + os.environ.get("PATH", "")
        if hasattr(os, "add_dll_directory"):
            try:
                os.add_dll_directory(str(_torch_lib))
            except Exception:
                pass

from .base_models import (
    HomogeneousGCN,
    GraphSAGEBaseline,
    StandardGAT,
    GINBaseline,
    EvolveGCNBaseline,
    GCNGRUBaseline,
    TabularXGBoost,
    IndustrialLightGBM,
    IndustrialCatBoost,
    BalancedRandomForestBaseline,
    IsolationForestBaseline,
    DeepAutoencoderBaseline,
    TopologicalLogisticRegression,
    VanillaHGTBaseline,
    CareGNNBaseline
)
from .evaluator import evaluate_model_performance, to_homogeneous_projection, resolve_target_node
from .visualizer import plot_pr_roc_curves, plot_metric_bars, plot_conformal_allocation

__all__ = [
    "HomogeneousGCN",
    "GraphSAGEBaseline",
    "StandardGAT",
    "GINBaseline",
    "EvolveGCNBaseline",
    "GCNGRUBaseline",
    "TabularXGBoost",
    "IndustrialLightGBM",
    "IndustrialCatBoost",
    "BalancedRandomForestBaseline",
    "IsolationForestBaseline",
    "DeepAutoencoderBaseline",
    "TopologicalLogisticRegression",
    "VanillaHGTBaseline",
    "CareGNNBaseline",
    "evaluate_model_performance",
    "to_homogeneous_projection",
    "resolve_target_node",
    "plot_pr_roc_curves",
    "plot_metric_bars",
    "plot_conformal_allocation"
]
