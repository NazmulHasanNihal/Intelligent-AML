"""
Intelligent AML — Layers 2 & 3
Model Architectures (HT-GNN, GraphGAN, SAM, Hawkes, Physics-Informed Losses)
"""
import os
import sys
from pathlib import Path

# Windows PyTorch DLL loading safety guard
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
_venv_torch_lib = Path(__file__).resolve().parent.parent.parent / "venv" / "Lib" / "site-packages" / "torch" / "lib"
_dll_handle = None
if _venv_torch_lib.exists():
    os.environ["PATH"] = str(_venv_torch_lib) + ";" + os.environ.get("PATH", "")
    if hasattr(os, "add_dll_directory"):
        try:
            _dll_handle = os.add_dll_directory(str(_venv_torch_lib))
        except Exception:
            pass

import torch

from .htgnn import BurstAwareHGT, CSTGBClassifier, train_htgnn, run_htgnn_pipeline, build_hetero_data as htgnn_build_data
from .burst_aware_hgt_conv import BurstAwareHGTConv
from .graphgan import GraphGAN, GraphGANGenerator, GraphGANDiscriminator, train_graphgan, run_graphgan_pipeline, build_hetero_data as graphgan_build_data
from .adversarial_defense import (
    AdversarialTopologyDefense,
    AdversarialCamouflageGenerator,
    MinimaxAdversarialTrainer,
    CounterfactualRobustnessAuditor,
)
from .continual_learning import (
    ElasticWeightConsolidation,
    TopologicalReservoirBuffer,
    ContinuousLearningEngine,
    DarkExperienceReplayBuffer,
)
from .graph_smote import TypologyClusteredGraphSMOTE, LatentGraphSMOTE, BilinearEdgeGenerator
from .graph_guard import AdversarialGraphGuard, HomophilyDenoisingGate
from .spectral_wavelets import SpectralGraphWaveletConv, ChebyshevSpectralWaveletEngine
from .optimal_transport import SinkhornDomainAligner, EntropicWassersteinLoss
from .focal_tversky_loss import CostSensitiveFocalTverskyLoss
from .threshold_optimizer import OptimalThresholdCalibrator
from .motif_kernel import DirectedMotifKernel
from .neuro_symbolic_loss import NeuroSymbolicAMLLoss, KirchhoffMassConservationLoss, PhysicsInformedAMLLoss
from .sam_optimizer import SAMOptimizer
from .hawkes_process import HawkesIntensityEngine, HawkesTemporalEncoder
from .inference_accelerator import (
    CSTGBHierarchicalAccelerator,
    InMemGraphEmbeddingRingBuffer,
    benchmark_acceleration_gain,
)

HTGNNAccelerator = BurstAwareHGT

__all__ = [
    "BurstAwareHGT",
    "BurstAwareHGTConv",
    "CSTGBClassifier",
    "HTGNNAccelerator",
    "train_htgnn",
    "run_htgnn_pipeline",
    "GraphGAN",
    "GraphGANGenerator",
    "GraphGANDiscriminator",
    "train_graphgan",
    "run_graphgan_pipeline",
    "AdversarialTopologyDefense",
    "AdversarialCamouflageGenerator",
    "MinimaxAdversarialTrainer",
    "CounterfactualRobustnessAuditor",
    "ElasticWeightConsolidation",
    "TopologicalReservoirBuffer",
    "ContinuousLearningEngine",
    "DarkExperienceReplayBuffer",
    "TypologyClusteredGraphSMOTE",
    "LatentGraphSMOTE",
    "BilinearEdgeGenerator",
    "AdversarialGraphGuard",
    "HomophilyDenoisingGate",
    "SpectralGraphWaveletConv",
    "ChebyshevSpectralWaveletEngine",
    "SinkhornDomainAligner",
    "EntropicWassersteinLoss",
    "CostSensitiveFocalTverskyLoss",
    "OptimalThresholdCalibrator",
    "DirectedMotifKernel",
    "NeuroSymbolicAMLLoss",
    "KirchhoffMassConservationLoss",
    "PhysicsInformedAMLLoss",
    "SAMOptimizer",
    "HawkesIntensityEngine",
    "HawkesTemporalEncoder",
    "CSTGBHierarchicalAccelerator",
    "InMemGraphEmbeddingRingBuffer",
    "benchmark_acceleration_gain",
]