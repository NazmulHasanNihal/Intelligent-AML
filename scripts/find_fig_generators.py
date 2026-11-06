import glob
import os

keywords = [
    "fig1_operational_architecture_flowchart",
    "fig3_ablation_component_study",
    "fig_operational_workflow",
    "fig_streaming_latency_waterfall",
    "fig_zero_shot_transfer_heatmap",
    "fig_temporal_split",
    "fig_triband_decay_comparison",
    "fig_lit_evolution_frontier",
    "fig1_pr_roc_curves",
    "fig_single_alert_timeline",
    "fig_system_architecture",
    "fig_12d_toy_model_schematic",
    "fig4_2_database_erd"
]

for f in sorted(glob.glob("scripts/*.py")):
    try:
        content = open(f, encoding="utf-8", errors="ignore").read()
        matched = [k for k in keywords if k in content]
        if matched:
            print(f"{os.path.basename(f)}: {matched}")
    except Exception as e:
        pass

