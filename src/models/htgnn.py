"""
htgnn.py — Modularized Facade & Backward-Compatible Export Layer.

The previous 2,834-line monolith has been decomposed into the modular `src.models.htgnn` package:
- profiles.py: 24-Dataset Universal Taxonomy and Adaptive Hyperparameters
- features.py: Personalized PageRank, Graphlet Motif, and Temporal Feature Extractors
- builder.py: Dynamic HeteroData Graph Construction and NeighborLoader Pipelines
- model.py: BurstAwareHGT Neural Network, FocalLoss, and EWC Regularizer
- training.py: Contrastive Pretraining, Supervised Optimization, and Latent Extraction
- cstgb.py: Cost-Sensitive Temporal Gradient Boosting (C-STGB) Ensemble
"""

from .htgnn.profiles import (
    NODE_TYPES,
    EDGE_TYPES,
    HIDDEN_CHANNELS,
    NUM_LAYERS,
    DROPOUT,
    ACTIVATION,
    JK_MODE,
    DATASET_PROFILES,
    DEFAULT_PROFILE,
    get_dataset_profile,
    OUTPUT_DIR,
)

from .htgnn.features import (
    load_parquet,
    compute_temporal_features,
    compute_personalized_pagerank_taint,
    compute_graphlet_motifs,
)

from .htgnn.builder import (
    get_neighbor_loader,
    build_hetero_data,
)

from .htgnn.model import (
    BurstAwareHGT,
    FocalLoss,
    EWC,
)

from .htgnn.training import (
    train_temporal_contrastive_pretraining,
    train_htgnn,
    extract_ego_neighborhood_embeddings,
)

from .htgnn.cstgb import (
    ResMLPNet,
    ResMLPMetaLearner,
    CSTGBClassifier,
    run_htgnn_pipeline,
)

__all__ = [
    "BurstAwareHGT",
    "CSTGBClassifier",
    "train_htgnn",
    "run_htgnn_pipeline",
    "build_hetero_data",
    "get_dataset_profile",
    "DATASET_PROFILES",
    "DEFAULT_PROFILE",
    "compute_personalized_pagerank_taint",
    "compute_graphlet_motifs",
    "compute_temporal_features",
    "load_parquet",
    "get_neighbor_loader",
    "FocalLoss",
    "EWC",
    "ResMLPNet",
    "ResMLPMetaLearner",
    "extract_ego_neighborhood_embeddings",
    "NODE_TYPES",
    "EDGE_TYPES",
]
