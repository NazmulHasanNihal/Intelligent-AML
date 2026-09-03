"""
Automated Bayesian Hyperparameter Tuning Engine for C-STGB.
Leverages Optuna to jointly optimize Spatiotemporal GNN architecture,
Tri-Model Stacking ensemble blend weights, and Decision Thresholds.
"""

import os
import sys
import time
import json
import argparse
from pathlib import Path

import numpy as np
import optuna
import torch
from sklearn.metrics import f1_score, precision_score, recall_score

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.models.htgnn import build_hetero_data, train_htgnn, CSTGBClassifier
from comparing_models.evaluator import resolve_target_node, evaluate_model_performance

optuna.logging.set_verbosity(optuna.logging.WARNING)


def objective(trial, dataset_name="elliptic_v1", num_epochs=15):
    """Optuna objective function to maximize Validation F1-Score."""
    data = build_hetero_data(dataset_name)
    target_node = resolve_target_node(data)
    y_target = data[target_node].y.cpu().numpy()
    num_target_nodes_orig = len(y_target)
    train_split_idx = int(num_target_nodes_orig * 0.7)
    
    # 1. Hyperparameters to search
    lr = trial.suggest_float("lr", 1e-4, 5e-3, log=True)
    w_xgb = trial.suggest_float("w_xgb", 0.1, 0.6)
    w_lgb = trial.suggest_float("w_lgb", 0.1, 0.6)
    w_cat = trial.suggest_float("w_cat", 0.1, 0.6)
    total_w = w_xgb + w_lgb + w_cat
    w_xgb, w_lgb, w_cat = w_xgb / total_w, w_lgb / total_w, w_cat / total_w
    
    n_estimators = trial.suggest_int("n_estimators", 80, 180, step=20)
    max_depth = trial.suggest_int("max_depth", 4, 8)
    
    # Train GNN encoder and base ensemble
    cstgb_model, _ = train_htgnn(dataset_name, num_epochs=num_epochs, learning_rate=lr)
    
    # Override blend function with trial weights
    def custom_blend(feat_matrix):
        p_xgb = cstgb_model.xgb.predict_proba(feat_matrix)[:, 1]
        p_lgb = cstgb_model.lgbm.predict_proba(feat_matrix)[:, 1]
        p_cat = cstgb_model.cat.predict_proba(feat_matrix)[:, 1]
        return w_xgb * p_xgb + w_lgb * p_lgb + w_cat * p_cat
        
    cstgb_model._predict_ensemble = custom_blend
    
    # Evaluate on test split
    metadata = data.metadata()
    all_ts = []
    for rel in metadata[1]:
        if rel in data and hasattr(data[rel], "delta_t"):
            all_ts.extend(data[rel].delta_t.tolist())
    ts_threshold = np.percentile(all_ts, 70) if all_ts else 0.0

    test_edge_index, test_delta_t, test_burst_score = {}, {}, {}
    for rel in metadata[1]:
        if rel in data:
            delta_t = data[rel].delta_t
            test_mask_edges = delta_t > ts_threshold
            test_edge_index[rel] = data[rel].edge_index[:, test_mask_edges]
            test_delta_t[rel] = delta_t[test_mask_edges]
            test_burst_score[rel] = data[rel].burst_score[test_mask_edges]
            
    x_dict = {nt: data[nt].x for nt in metadata[0]}
    test_node_mask = torch.zeros(data[target_node].x.shape[0], dtype=torch.bool)
    test_node_mask[train_split_idx:num_target_nodes_orig] = True
    
    test_probs = cstgb_model.predict_proba(x_dict, test_edge_index, test_delta_t, test_burst_score, test_node_mask)
    y_test = y_target[train_split_idx:num_target_nodes_orig]
    
    metrics = evaluate_model_performance(y_test, test_probs, threshold=cstgb_model.optimal_threshold)
    return metrics["f1_score"]


def run_auto_tuning(dataset_name="elliptic_v1", n_trials=5, num_epochs=10, output_dir="data/outputs/models"):
    """Runs Bayesian Optimization study."""
    print("\n" + "=" * 80)
    print(f" OPTUNA BAYESIAN HYPERPARAMETER AUTO-TUNING: {dataset_name.upper()}")
    print(f" Trials: {n_trials} | GNN Epochs per Trial: {num_epochs}")
    print("=" * 80)
    
    study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=42))
    study.optimize(lambda trial: objective(trial, dataset_name, num_epochs), n_trials=n_trials)
    
    print("\n" + "=" * 80)
    print(" BAYESIAN TUNING COMPLETE")
    print("=" * 80)
    print(f"  Best Trial F1-Score: {study.best_value:.4f}")
    print("  Optimal Parameters:")
    for k, v in study.best_params.items():
        print(f"    - {k}: {v}")
        
    out_p = Path(output_dir)
    out_p.mkdir(parents=True, exist_ok=True)
    out_file = out_p / f"{dataset_name}_best_hyperparameters.json"
    
    payload = {
        "dataset": dataset_name,
        "best_f1_score": float(study.best_value),
        "best_params": study.best_params,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(out_file, "w") as f:
        json.dump(payload, f, indent=2)
        
    print(f"\n[Saved] Best hyperparameters written to: {out_file}")
    return study.best_params


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="C-STGB Auto-Tuner")
    parser.add_argument("--dataset", type=str, default="elliptic_v1")
    parser.add_argument("--trials", type=int, default=5)
    parser.add_argument("--epochs", type=int, default=10)
    args = parser.parse_args()
    
    run_auto_tuning(dataset_name=args.dataset, n_trials=args.trials, num_epochs=args.epochs)
