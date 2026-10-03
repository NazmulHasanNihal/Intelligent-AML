"""
profiles.py — Universal 24-Dataset Taxonomy and Adaptive Hyperparameter Profiles.
"""
from pathlib import Path

OUTPUT_DIR = Path("data/outputs/graph_data")
NODE_TYPES = ["Account", "User", "Device", "Institution"]
EDGE_TYPES = ["Transaction", "IP_Connection", "Shared_Ownership"]

HIDDEN_CHANNELS = 128
NUM_LAYERS = 6
DROPOUT = 0.3
ACTIVATION = "relu"
JK_MODE = "cat"

DATASET_PROFILES = {
    # Archetype 1: Crypto / Blockchain Transaction Networks
    "elliptic_v1":             {"gnn_layers": 3, "hidden": 128, "lr": 0.001,  "xgb_n": 300, "xgb_depth": 6, "focal_beta": 0.75, "smote_ratio": 0.10},
    "elliptic_v2":             {"gnn_layers": 3, "hidden": 128, "lr": 0.001,  "xgb_n": 300, "xgb_depth": 6, "focal_beta": 0.75, "smote_ratio": 0.10},
    "eth_phishing":            {"gnn_layers": 4, "hidden": 128, "lr": 0.0005, "xgb_n": 600, "xgb_depth": 8, "focal_beta": 0.88, "smote_ratio": 0.20},
    "eth_phishing_2nd":        {"gnn_layers": 4, "hidden": 128, "lr": 0.0005, "xgb_n": 600, "xgb_depth": 8, "focal_beta": 0.88, "smote_ratio": 0.20},
    "xblock_eth":              {"gnn_layers": 4, "hidden": 128, "lr": 0.0005, "xgb_n": 600, "xgb_depth": 8, "focal_beta": 0.88, "smote_ratio": 0.20},
    "mtgox_leaked":            {"gnn_layers": 4, "hidden": 128, "lr": 0.0008, "xgb_n": 1000, "xgb_depth": 9, "focal_beta": 0.95, "smote_ratio": 0.25},
    "smart_ponzi":             {"gnn_layers": 3, "hidden": 96,  "lr": 0.001,  "xgb_n": 300, "xgb_depth": 6, "focal_beta": 0.75, "smote_ratio": 0.10},

    # Archetype 2: Retail Banking & Multi-Tier Layering Networks
    "ibm_amlsim_hi_small":          {"gnn_layers": 4, "hidden": 128, "lr": 0.0005, "xgb_n": 800, "xgb_depth": 10, "focal_beta": 0.98, "smote_ratio": 0.30},
    "ibm_amlsim_hi_small_accounts": {"gnn_layers": 4, "hidden": 128, "lr": 0.0005, "xgb_n": 800, "xgb_depth": 10, "focal_beta": 0.98, "smote_ratio": 0.30},
    "ibm_amlsim_hi_medium":         {"gnn_layers": 4, "hidden": 128, "lr": 0.0005, "xgb_n": 800, "xgb_depth": 10, "focal_beta": 0.98, "smote_ratio": 0.30},
    "ibm_amlsim_hi_medium_accounts":{"gnn_layers": 4, "hidden": 128, "lr": 0.0005, "xgb_n": 800, "xgb_depth": 10, "focal_beta": 0.98, "smote_ratio": 0.30},
    "ibm_amlsim_li_small":          {"gnn_layers": 4, "hidden": 128, "lr": 0.0005, "xgb_n": 800, "xgb_depth": 9,  "focal_beta": 0.96, "smote_ratio": 0.25},
    "ibm_amlsim_li_small_accounts": {"gnn_layers": 4, "hidden": 128, "lr": 0.0005, "xgb_n": 800, "xgb_depth": 9,  "focal_beta": 0.96, "smote_ratio": 0.25},
    "ibm_amlsim_li_medium":         {"gnn_layers": 4, "hidden": 128, "lr": 0.0005, "xgb_n": 800, "xgb_depth": 9,  "focal_beta": 0.96, "smote_ratio": 0.25},
    "ibm_amlsim_li_medium_accounts":{"gnn_layers": 4, "hidden": 128, "lr": 0.0005, "xgb_n": 800, "xgb_depth": 9,  "focal_beta": 0.96, "smote_ratio": 0.25},
    "saml_d":                       {"gnn_layers": 5, "hidden": 128, "lr": 0.0005, "xgb_n": 800,  "xgb_depth": 8,  "focal_beta": 0.92, "smote_ratio": 0.25},
    "synthaml":                     {"gnn_layers": 5, "hidden": 96,  "lr": 0.0005, "xgb_n": 600,  "xgb_depth": 8,  "focal_beta": 0.90, "smote_ratio": 0.20},

    # Archetype 3: High-Velocity Mobile Money & E-Wallets
    "paysim1":                 {"gnn_layers": 5, "hidden": 64, "lr": 0.0001, "xgb_n": 600, "xgb_depth": 10, "focal_beta": 0.95, "smote_ratio": 0.25},
    "paysim_extended":         {"gnn_layers": 5, "hidden": 48, "lr": 0.0001, "xgb_n": 600, "xgb_depth": 10, "focal_beta": 0.95, "smote_ratio": 0.25},

    # Archetype 4: FinTech Lending & Credit Card Fraud
    "dgraphfin":               {"gnn_layers": 4, "hidden": 96, "lr": 0.0005, "xgb_n": 400, "xgb_depth": 7, "focal_beta": 0.85, "smote_ratio": 0.15},
    "cc_transactions":         {"gnn_layers": 4, "hidden": 96, "lr": 0.0003, "xgb_n": 500, "xgb_depth": 8, "focal_beta": 0.90, "smote_ratio": 0.20},
    "ulb_credit_card":         {"gnn_layers": 4, "hidden": 96, "lr": 0.0005, "xgb_n": 400, "xgb_depth": 7, "focal_beta": 0.85, "smote_ratio": 0.15},
    "data_generator":          {"gnn_layers": 4, "hidden": 96, "lr": 0.0005, "xgb_n": 300, "xgb_depth": 6, "focal_beta": 0.80, "smote_ratio": 0.10},
    "live_demo":               {"gnn_layers": 3, "hidden": 64, "lr": 0.001,  "xgb_n": 200, "xgb_depth": 6, "focal_beta": 0.75, "smote_ratio": 0.10},
}
DEFAULT_PROFILE = {"gnn_layers": 4, "hidden": 96, "lr": 0.0005, "xgb_n": 400, "xgb_depth": 7, "focal_beta": 0.80, "smote_ratio": 0.15}

def get_dataset_profile(dataset_name: str) -> dict:
    """Returns the dataset-adaptive hyperparameter profile, falling back to defaults."""
    return DATASET_PROFILES.get(dataset_name, DEFAULT_PROFILE)


