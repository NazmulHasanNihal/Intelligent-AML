"""
Visual Analytics & Comparative Chart Generators for AML Benchmarks.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import precision_recall_curve, roc_curve, auc


def plot_metric_bars(df_results, title="Multi-Model AML Benchmark Comparison", save_path=None):
    """Generates comparative bar chart across F1, F2, Precision, and Recall."""
    df_melt = df_results.reset_index().melt(
        id_vars=['index'],
        value_vars=['f1_score', 'recall', 'precision', 'f2_score']
    )
    fig = px.bar(
        df_melt,
        x='index',
        y='value',
        color='variable',
        barmode='group',
        title=title,
        labels={'index': 'Model', 'value': 'Score', 'variable': 'Metric'},
        template='plotly_dark'
    )
    if save_path:
        p = Path(save_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(str(p))
    return fig


def plot_pr_roc_curves(model_probs_dict, y_true, title="Precision-Recall & ROC Curves", save_path=None):
    """Plots multi-model PR Curves and ROC Curves."""
    valid_mask = y_true >= 0
    y_clean = y_true[valid_mask]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    for model_name, probs in model_probs_dict.items():
        probs_clean = probs[valid_mask]
        
        # PR Curve
        prec, rec, _ = precision_recall_curve(y_clean, probs_clean)
        pr_auc = auc(rec, prec)
        ax1.plot(rec, prec, label=f"{model_name} (AUC={pr_auc:.3f})")
        
        # ROC Curve
        fpr, tpr, _ = roc_curve(y_clean, probs_clean)
        roc_auc = auc(fpr, tpr)
        ax2.plot(fpr, tpr, label=f"{model_name} (AUC={roc_auc:.3f})")
        
    ax1.set_title("Precision-Recall Curve")
    ax1.set_xlabel("Recall (Fraud Catch Rate)")
    ax1.set_ylabel("Precision")
    ax1.legend(loc="lower left")
    ax1.grid(True, linestyle="--", alpha=0.5)
    
    ax2.set_title("Receiver Operating Characteristic (ROC)")
    ax2.set_xlabel("False Positive Rate (FPR)")
    ax2.set_ylabel("True Positive Rate (TPR)")
    ax2.plot([0, 1], [0, 1], 'k--', alpha=0.5)
    ax2.legend(loc="lower right")
    ax2.grid(True, linestyle="--", alpha=0.5)
    
    plt.tight_layout()
    if save_path:
        p = Path(save_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(str(p), dpi=300)
    plt.close()


def plot_conformal_allocation(confident_licit, confident_fraud, uncertain_review, save_path=None):
    """Plots Conformal Prediction 3-Tier Risk Allocation Donut Chart."""
    labels = ['Auto-Approve (Licit)', 'Auto-Flag (SAR)', 'Compliance Review Queue']
    values = [confident_licit, confident_fraud, uncertain_review]
    colors = ['#2ca02c', '#d62728', '#ff7f0e']
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, marker_colors=colors)])
    fig.update_layout(title_text="Conformal Risk Partition & Queue Load", template="plotly_dark")
    
    if save_path:
        p = Path(save_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(str(p))
    return fig
