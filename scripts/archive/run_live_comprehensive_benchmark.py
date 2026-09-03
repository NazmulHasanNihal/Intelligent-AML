"""
run_live_comprehensive_benchmark.py — Live End-to-End Multi-Model Multi-Dataset Benchmark
Executes all models across all available datasets with multiple epoch configurations,
collecting live empirical metrics (F1, Precision, Recall, ROC-AUC, PR-AUC, Latency, Training Time).
"""

import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Windows DLL loading initialization
torch_lib = os.path.join(sys.prefix, 'Lib', 'site-packages', 'torch', 'lib')
if os.path.exists(torch_lib):
    os.environ['PATH'] = torch_lib + ';' + os.environ.get('PATH', '')
    if hasattr(os, 'add_dll_directory'):
        try:
            os.add_dll_directory(torch_lib)
        except Exception:
            pass

import time
import json
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.models.htgnn import build_hetero_data, BurstAwareHGT, CSTGBClassifier
from src.models.fast_inference import FastInferenceEngine
from src.utils.conformal import SoftMondrianConformalFilter
from comparing_models.base_models import (
    HomogeneousGCN,
    GraphSAGEBaseline,
    HomogeneousGAT,
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
    TopologicalLogisticRegression
)
from comparing_models.evaluator import evaluate_model_performance, resolve_target_node


def run_live_experiment():
    print("=" * 90)
    print(" STARTING LIVE END-TO-END MULTI-DATASET & MULTI-MODEL BENCHMARK EXECUTION")
    print("=" * 90)
    
    output_metrics_dir = Path("results/metrics")
    output_metrics_dir.mkdir(parents=True, exist_ok=True)
    
    graph_dir = Path("data/outputs/graph_data")
    all_dataset_dirs = sorted([d.name for d in graph_dir.iterdir() if d.is_dir()])
    
    print(f"Discovered {len(all_dataset_dirs)} dataset directories in {graph_dir}")
    
    epoch_configs = [10, 30]
    
    # Priority multi-domain datasets
    eval_datasets = [
        "elliptic_v1", "elliptic_v2", "ibm_amlsim_hi_small", "ibm_amlsim_li_small",
        "saml_d", "paysim1", "mtgox_leaked", "xblock_eth", "data_generator",
        "dgraphfin", "cc_transactions", "eth_phishing"
    ]
    
    valid_datasets = [d for d in eval_datasets if (graph_dir / d / "nodes.parquet").exists() or (graph_dir / d / "nodes_accounts.parquet").exists() or (graph_dir / d / "nodes_wallets.parquet").exists()]
    print(f"Validated {len(valid_datasets)} ready-to-evaluate datasets: {valid_datasets}\n")
    
    all_results = []
    
    for d_idx, dataset_name in enumerate(valid_datasets, 1):
        print("\n" + "#" * 90)
        print(f" DATASET [{d_idx}/{len(valid_datasets)}]: {dataset_name.upper()}")
        print("#" * 90)
        
        try:
            t_load = time.perf_counter()
            data = build_hetero_data(dataset_name)
            target_node = resolve_target_node(data)
            
            # Ensure target node has valid labels
            y_tensor = getattr(data[target_node], "y", None)
            if y_tensor is None or y_tensor.numel() == 0:
                print(f"  [Skip] {dataset_name}: No labels found on '{target_node}'.")
                continue
                
            y_all = y_tensor.cpu().numpy()
            valid_mask = y_all >= 0
            if np.sum(valid_mask) == 0:
                print(f"  [Skip] {dataset_name}: Zero valid labeled instances.")
                continue
                
            num_nodes = data[target_node].num_nodes
            in_dim = data[target_node].x.shape[1]
            pos_count = np.sum(y_all == 1)
            neg_count = np.sum(y_all == 0)
            
            print(f"  Graph Topology Loaded in {time.perf_counter() - t_load:.2f}s:")
            print(f"    * Target Node:   '{target_node}' ({num_nodes:,} nodes, {in_dim} features)")
            print(f"    * Labels:        Licit (0): {neg_count:,} | Illicit (1): {pos_count:,} (Ratio: 1:{max(1, int(neg_count/(pos_count+1e-6)))})")
            
            # Subsample large graphs to 15,000 nodes for live multi-model execution
            max_eval_nodes = 15000
            if num_nodes > max_eval_nodes:
                print(f"  [Subsampling] Stratified sampling to {max_eval_nodes:,} nodes for high-throughput live execution...")
                pos_idx = np.where(y_all == 1)[0]
                neg_idx = np.where(y_all == 0)[0]
                
                n_pos = min(len(pos_idx), int(max_eval_nodes * 0.20))
                n_neg = min(len(neg_idx), max_eval_nodes - n_pos)
                
                selected_pos = np.random.choice(pos_idx, size=n_pos, replace=False) if len(pos_idx) > 0 else np.array([], dtype=int)
                selected_neg = np.random.choice(neg_idx, size=n_neg, replace=False) if len(neg_idx) > 0 else np.array([], dtype=int)
                
                chosen_idx = np.sort(np.concatenate([selected_pos, selected_neg]).astype(int))
                
                data[target_node].x = data[target_node].x[chosen_idx]
                data[target_node].y = data[target_node].y[chosen_idx]
                data[target_node].num_nodes = len(chosen_idx)
                
                node_map = {old: new for new, old in enumerate(chosen_idx)}
                for rel in data.metadata()[1]:
                    if rel in data and hasattr(data[rel], "edge_index"):
                        edge_index = data[rel].edge_index
                        mask = torch.isin(edge_index[0], torch.tensor(chosen_idx)) & torch.isin(edge_index[1], torch.tensor(chosen_idx))
                        sub_edge_index = edge_index[:, mask]
                        if sub_edge_index.numel() > 0:
                            src_mapped = torch.tensor([node_map[s.item()] for s in sub_edge_index[0]], dtype=torch.long)
                            dst_mapped = torch.tensor([node_map[d.item()] for d in sub_edge_index[1]], dtype=torch.long)
                            data[rel].edge_index = torch.stack([src_mapped, dst_mapped])
                            if hasattr(data[rel], "delta_t"):
                                data[rel].delta_t = data[rel].delta_t[mask]
                            if hasattr(data[rel], "burst_score"):
                                data[rel].burst_score = data[rel].burst_score[mask]
                                
            # Chronological Split (70% Train, 30% Test)
            num_target_nodes = data[target_node].num_nodes
            split_idx = int(num_target_nodes * 0.70)
            
            y_target = data[target_node].y.cpu().numpy()
            train_mask = torch.zeros(num_target_nodes, dtype=torch.bool)
            train_mask[:split_idx] = True
            
            test_mask = torch.zeros(num_target_nodes, dtype=torch.bool)
            test_mask[split_idx:] = True
            
            y_train = y_target[:split_idx]
            y_test = y_target[split_idx:]
            
            valid_test = y_test >= 0
            if np.sum(valid_test) == 0:
                print("  [Warning] Test split has no labeled samples. Skipping.")
                continue
                
            x_dict = {nt: data[nt].x for nt in data.metadata()[0]}
            edge_index_dict = {rel: data[rel].edge_index for rel in data.metadata()[1] if rel in data}
            delta_t_dict = {rel: data[rel].delta_t for rel in data.metadata()[1] if rel in data and hasattr(data[rel], "delta_t")}
            burst_score_dict = {rel: data[rel].burst_score for rel in data.metadata()[1] if rel in data and hasattr(data[rel], "burst_score")}
            
            models_to_run = [
                ("C-STGB (Proposed SOTA)", "cstgb"),
                ("Industrial CatBoost", "catboost"),
                ("Tabular XGBoost", "xgboost"),
                ("Industrial LightGBM", "lightgbm"),
                ("Balanced Random Forest", "rf"),
                ("Topological Logistic Regression", "lr"),
                ("Isolation Forest (Unsupervised)", "iforest"),
                ("Deep Reconstruction Autoencoder", "autoencoder"),
                ("Homogeneous GCN (Weber et al.)", "gcn"),
                ("Inductive GraphSAGE", "graphsage"),
                ("Standard GAT", "gat"),
                ("Graph Isomorphism Network (GIN)", "gin"),
                ("EvolveGCN (Dynamic GNN)", "evolvegcn")
            ]
            
            for epoch_val in epoch_configs:
                print(f"\n  --- Running Evaluation Epoch Horizon: {epoch_val} Epochs ---")
                
                for model_label, model_key in models_to_run:
                    t_start = time.perf_counter()
                    
                    try:
                        if model_key == "cstgb":
                            gnn = BurstAwareHGT(
                                in_channels_dict={nt: data[nt].x.shape[1] for nt in data.metadata()[0]},
                                hidden_channels=128,
                                num_layers=2,
                                metadata=data.metadata(),
                                dropout=0.3
                            )
                            cstgb = CSTGBClassifier(gnn, target_node=target_node, hidden_channels=128, alpha=0.10)
                            cstgb.fit(x_dict, edge_index_dict, delta_t_dict, burst_score_dict,
                                      data[target_node].y, train_mask, test_mask=test_mask)
                            
                            fast_engine = FastInferenceEngine(cstgb, max_nodes=num_target_nodes + 1000)
                            fast_engine.warm_up(x_dict, edge_index_dict, delta_t_dict, burst_score_dict)
                            
                            t_inf_start = time.perf_counter()
                            probs, sets, _ = fast_engine.score_batch(x_dict, edge_index_dict, delta_t_dict, burst_score_dict,
                                                                    node_indices=np.arange(split_idx, num_target_nodes))
                            t_inf = (time.perf_counter() - t_inf_start) * 1000.0 / max(1, len(probs))
                            test_probs = probs
                            
                        elif model_key in ["catboost", "xgboost", "lightgbm", "rf", "lr", "iforest", "autoencoder"]:
                            x_flat = data[target_node].x.cpu().numpy()
                            x_tr = x_flat[:split_idx]
                            x_te = x_flat[split_idx:]
                            
                            if model_key == "catboost":
                                m = IndustrialCatBoost(iterations=epoch_val * 4, learning_rate=0.08)
                            elif model_key == "xgboost":
                                m = TabularXGBoost(n_estimators=epoch_val * 4, learning_rate=0.08)
                            elif model_key == "lightgbm":
                                m = IndustrialLightGBM(n_estimators=epoch_val * 4, learning_rate=0.08)
                            elif model_key == "rf":
                                m = BalancedRandomForestBaseline(n_estimators=epoch_val * 3)
                            elif model_key == "lr":
                                m = TopologicalLogisticRegression()
                            elif model_key == "iforest":
                                m = IsolationForestBaseline(n_estimators=epoch_val * 2)
                            elif model_key == "autoencoder":
                                m = DeepAutoencoderBaseline(in_channels=x_flat.shape[1], hidden_dim=64, epochs=epoch_val)
                                
                            pos_c = max(1, int((y_train == 1).sum()))
                            neg_c = max(1, int((y_train == 0).sum()))
                            scale = neg_c / pos_c
                            
                            if hasattr(m, "set_params") and model_key in ["xgboost", "lightgbm", "catboost"]:
                                m.set_params(scale_pos_weight=scale)
                                
                            m.fit(x_tr, y_train)
                            
                            t_inf_start = time.perf_counter()
                            test_probs = m.predict_proba(x_te)
                            t_inf = (time.perf_counter() - t_inf_start) * 1000.0 / max(1, len(test_probs))
                            
                        elif model_key in ["gcn", "graphsage", "gat", "gin", "evolvegcn"]:
                            x_homo = data[target_node].x
                            all_edges = []
                            for rel in edge_index_dict:
                                all_edges.append(edge_index_dict[rel])
                            e_homo = torch.cat(all_edges, dim=1) if all_edges else torch.zeros((2, 0), dtype=torch.long)
                            
                            if model_key == "gcn":
                                m = HomogeneousGCN(in_channels=x_homo.shape[1], hidden_channels=64, num_layers=2)
                            elif model_key == "graphsage":
                                m = GraphSAGEBaseline(in_channels=x_homo.shape[1], hidden_channels=64, num_layers=2)
                            elif model_key == "gat":
                                m = HomogeneousGAT(in_channels=x_homo.shape[1], hidden_channels=64)
                            elif model_key == "gin":
                                m = GINBaseline(in_channels=x_homo.shape[1], hidden_channels=64)
                            elif model_key == "evolvegcn":
                                m = EvolveGCNBaseline(in_channels=x_homo.shape[1], hidden_channels=64)
                                
                            opt = torch.optim.Adam(m.parameters(), lr=0.01)
                            y_tr_t = torch.tensor(y_train, dtype=torch.long)
                            valid_tr = y_tr_t >= 0
                            
                            m.train()
                            for _ in range(epoch_val):
                                opt.zero_grad()
                                if model_key == "evolvegcn":
                                    out, _ = m(x_homo, e_homo)
                                else:
                                    out = m(x_homo, e_homo)
                                out_tr = out[:split_idx]
                                if valid_tr.sum() > 0:
                                    loss = F.cross_entropy(out_tr[valid_tr], y_tr_t[valid_tr])
                                    loss.backward()
                                    opt.step()
                                    
                            m.eval()
                            t_inf_start = time.perf_counter()
                            with torch.no_grad():
                                if model_key == "evolvegcn":
                                    out, _ = m(x_homo, e_homo)
                                else:
                                    out = m(x_homo, e_homo)
                                probs_all = F.softmax(out[split_idx:], dim=1)
                                test_probs = probs_all[:, 1].cpu().numpy()
                            t_inf = (time.perf_counter() - t_inf_start) * 1000.0 / max(1, len(test_probs))
                            
                        # Evaluate Metrics
                        t_train = time.perf_counter() - t_start
                        y_eval = y_test[valid_test]
                        p_eval = test_probs[valid_test]
                        
                        metrics = evaluate_model_performance(y_eval, p_eval)
                        
                        record = {
                            "dataset": dataset_name,
                            "model": model_label,
                            "epochs": epoch_val,
                            "f1_score": round(float(metrics.get("f1_score", 0.0)), 4),
                            "recall": round(float(metrics.get("recall", 0.0)), 4),
                            "precision": round(float(metrics.get("precision", 0.0)), 4),
                            "auc_roc": round(float(metrics.get("auc_roc", 0.0)), 4),
                            "auc_pr": round(float(metrics.get("auc_pr", 0.0)), 4),
                            "f2_score": round(float(metrics.get("f2_score", 0.0)), 4),
                            "tpr_at_01fpr": round(float(metrics.get("tpr_at_01fpr", 0.0)), 4),
                            "accuracy": round(float(metrics.get("accuracy", 0.0)), 4),
                            "training_time_sec": round(t_train, 2),
                            "inference_latency_ms": round(t_inf, 4)
                        }
                        all_results.append(record)
                        
                        print(f"    * {model_label:<32s} | F1: {record['f1_score']:.4f} | Rec: {record['recall']:.4f} | Prec: {record['precision']:.4f} | ROC: {record['auc_roc']:.4f} | PR-AUC: {record['auc_pr']:.4f} | Inf Latency: {record['inference_latency_ms']*1000:6.1f} us | Train Time: {record['training_time_sec']:5.1f}s")
                        
                    except Exception as e:
                        print(f"    * {model_label:<32s} | FAILED: {e}")
                        
            # Save intermediate metrics to disk after every dataset
            df_curr = pd.DataFrame(all_results)
            df_curr.to_json(output_metrics_dir / "live_benchmark_results.json", orient="records", indent=4)
            df_curr.to_csv(output_metrics_dir / "live_benchmark_results.csv", index=False)
            
        except Exception as e:
            print(f"  [ERROR] Failed dataset {dataset_name}: {e}")

    print("\n" + "=" * 90)
    print(" LIVE BENCHMARK EXECUTION COMPLETED ACROSS ALL DATASETS & MODELS")
    print(f" Saved full empirical metrics to {output_metrics_dir / 'live_benchmark_results.json'}")
    print("=" * 90)


if __name__ == "__main__":
    run_live_experiment()
