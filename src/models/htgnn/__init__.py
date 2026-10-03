"""
htgnn package — Modular Heterogeneous Temporal Graph Neural Network & C-STGB.
Decomposed into clean, cohesive submodules for production maintainability:
- profiles: Dataset profiles & taxonomy
- features: Temporal, PageRank, and Graphlet motif extractors
- builder: Multi-dataset HeteroData constructor
- model: BurstAwareHGT architecture & regularization
- training: Contrastive pre-training & supervised engine
- cstgb: Cost-sensitive ensemble classifier & SAR generator
"""

from .profiles import (
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

from .features import (
    load_parquet,
    compute_temporal_features,
    compute_personalized_pagerank_taint,
    compute_graphlet_motifs,
)

from .builder import (
    get_neighbor_loader,
    build_hetero_data,
)

from .model import (
    BurstAwareHGT,
    FocalLoss,
    EWC,
)

from .training import (
    train_temporal_contrastive_pretraining,
    train_htgnn,
    extract_ego_neighborhood_embeddings,
)

from .cstgb import (
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
