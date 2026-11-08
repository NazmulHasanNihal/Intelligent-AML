"""
scripts/build_ch7_figures.py
Extracts and builds standalone scripts for all Chapter 7 figures (17 scripts).
"""

import os
from pathlib import Path

OUT_DIR = Path("scripts/figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. Figure 7.1: Class Imbalance Log
# -----------------------------------------------------------------------------
with open("scripts/generate_publication_figures_extra.py", "r", encoding="utf-8") as f:
    text = f.read()

start_m = 'print("[1/12] Generating fig_class_imbalance_log...")'
idx_start = text.find(start_m)
idx_end = text.find('save_all(fig, "fig_class_imbalance_log")', idx_start) + len('save_all(fig, "fig_class_imbalance_log")')
snippet = text[idx_start:idx_end]
snippet = snippet.replace('save_all(fig, "fig_class_imbalance_log")', 'save_figure(fig, "fig_class_imbalance_log", pad_inches=0.12)\n    plt.close(fig)')
snippet_indented = "\n".join("    " + l for l in snippet.splitlines())

fig7_1_code = f'''"""
Figure 7.1: Extreme Class Skew Distribution across 14 Benchmarks
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.5)
{snippet_indented}

if __name__ == "__main__":
    generate()
'''
with open(OUT_DIR / "fig7_1_class_imbalance_log.py", "w", encoding="utf-8") as f:
    f.write(fig7_1_code.strip() + "\n")
print("Created fig7_1_class_imbalance_log.py")

# -----------------------------------------------------------------------------
# 2. Figure 7.2: Temporal Split
# -----------------------------------------------------------------------------
with open("scripts/redesign_fig7_2_temporal_split.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("def generate_figure_7_2():")
end_idx = text.find("def main():")
body = text[idx:end_idx]
body = body.replace("def generate_figure_7_2():", "def generate():")

fig7_2_code = f'''"""
Figure 7.2: Zero-Leakage 4-Way Chronological Dataset Split Timeline
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

{body}

if __name__ == "__main__":
    fig = generate()
    save_figure(fig, "fig_temporal_split", pad_inches=0.15)
    plt.close(fig)
'''
with open(OUT_DIR / "fig7_2_temporal_split.py", "w", encoding="utf-8") as f:
    f.write(fig7_2_code.strip() + "\n")
print("Created fig7_2_temporal_split.py")

# -----------------------------------------------------------------------------
# 3. Figure 7.3: Champion vs Runner-Up Delta
# -----------------------------------------------------------------------------
with open("scripts/redesign_fig7_3_champion_delta.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("def generate_fig7_3():")
body = text[idx:]
body = body.replace("def generate_fig7_3():", "def generate():")
idx_save = body.find("for d in TARGET_DIRS:")
body = body[:idx_save] + 'save_figure(fig, "fig_champion_vs_runnerup_delta", pad_inches=0.15)\n    plt.close(fig)\n\nif __name__ == "__main__":\n    generate()\n'

fig7_3_code = f'''"""
Figure 7.3: C-STGB Benchmark Superiority and F1 Lead across 14 Networks
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

{body}
'''
with open(OUT_DIR / "fig7_3_champion_delta.py", "w", encoding="utf-8") as f:
    f.write(fig7_3_code.strip() + "\n")
print("Created fig7_3_champion_delta.py")

# -----------------------------------------------------------------------------
# 4. Figure 7.4: Critical Difference Lollipop
# -----------------------------------------------------------------------------
with open("scripts/redesign_fig7_4_critical_difference.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("def generate_figure_7_4():")
end_idx = text.find("def main():")
body = text[idx:end_idx]
body = body.replace("def generate_figure_7_4():", "def generate():")

fig7_4_code = f'''"""
Figure 7.4: Statistical Significance and Archetype Performance Synthesis
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

{body}

if __name__ == "__main__":
    fig = generate()
    save_figure(fig, "fig_critical_difference_lollipop", pad_inches=0.12)
    save_figure(fig, "fig7_3_critical_difference_lollipop", pad_inches=0.12)
    plt.close(fig)
'''
with open(OUT_DIR / "fig7_4_critical_difference.py", "w", encoding="utf-8") as f:
    f.write(fig7_4_code.strip() + "\n")
print("Created fig7_4_critical_difference.py")

# -----------------------------------------------------------------------------
# 5. Figure 7.5: Multi-Dataset Radar Benchmark
# -----------------------------------------------------------------------------
with open("scripts/generate_all_publication_figures.py", "r", encoding="utf-8") as f:
    text = f.read()

start_m = "# FIGURE 7: Multi-Dataset Radar Benchmark"
idx_start = text.find(start_m)
idx_end = text.find('save_all_formats(fig, "fig7_multi_dataset_radar")', idx_start) + len('save_all_formats(fig, "fig7_multi_dataset_radar")')
snippet = text[idx_start:idx_end]
snippet = snippet.replace('save_all_formats(fig, "fig7_multi_dataset_radar")', 'save_figure(fig, "fig7_multi_dataset_radar", pad_inches=0.12)\n    plt.close(fig)')
snippet_indented = "\n".join("    " + l for l in snippet.splitlines())

fig7_5_code = f'''"""
Figure 7.5: Multi-Criteria Radar Benchmark contrasting C-STGB vs. Baselines
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

C_CSTGB = "#dc2626"
C_GCN   = "#475569"
C_XGB   = "#16a34a"
C_CARE  = "#d97706"
C_EAAI  = "#2563eb"

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.5)
{snippet_indented}

if __name__ == "__main__":
    generate()
'''
with open(OUT_DIR / "fig7_5_radar_benchmark.py", "w", encoding="utf-8") as f:
    f.write(fig7_5_code.strip() + "\n")
print("Created fig7_5_radar_benchmark.py")

# -----------------------------------------------------------------------------
# 6. Figure 7.6: PR and ROC Curves
# -----------------------------------------------------------------------------
start_m = "# FIGURE 1: Precision-Recall & ROC Curves (Double Column: 7.16\" x 2.80\")"
idx_start = text.find(start_m)
idx_end = text.find('save_all_formats(fig, "fig1_pr_roc_curves")', idx_start) + len('save_all_formats(fig, "fig1_pr_roc_curves")')
snippet = text[idx_start:idx_end]
snippet = snippet.replace('save_all_formats(fig, "fig1_pr_roc_curves")', 'save_figure(fig, "fig1_pr_roc_curves", pad_inches=0.12)\n    save_figure(fig, "pr_roc_curves", pad_inches=0.12)\n    plt.close(fig)')
snippet_indented = "\n".join("    " + l for l in snippet.splitlines())

fig7_6_code = f'''"""
Figure 7.6: Comparative PR and ROC Frontiers on Elliptic-v1
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

C_CSTGB = "#dc2626"
C_GCN   = "#475569"
C_XGB   = "#16a34a"
C_CARE  = "#d97706"
C_EAAI  = "#2563eb"

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.5)
{snippet_indented}

if __name__ == "__main__":
    generate()
'''
with open(OUT_DIR / "fig7_6_pr_roc_curves.py", "w", encoding="utf-8") as f:
    f.write(fig7_6_code.strip() + "\n")
print("Created fig7_6_pr_roc_curves.py")

# -----------------------------------------------------------------------------
# 7. Figure 7.7: Stepwise Ablation Progression
# -----------------------------------------------------------------------------
with open("scripts/redesign_fig7_7_ablation_progression.py", "r", encoding="utf-8") as f:
    text_7_7 = f.read()

idx = text_7_7.find("def generate_fig7_7():")
body = text_7_7[idx:]
body = body.replace("def generate_fig7_7():", "def generate():")
idx_save = body.find("for d in TARGET_DIRS:")
body = body[:idx_save] + 'save_figure(fig, "fig3_ablation_component_study", pad_inches=0.15)\n    save_figure(fig, "ablation_study", pad_inches=0.15)\n    plt.close(fig)\n\nif __name__ == "__main__":\n    generate()\n'

fig7_7_code = f'''"""
Figure 7.7: Stepwise Architectural Ablation across Three Benchmark Datasets
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

{body}
'''
with open(OUT_DIR / "fig7_7_ablation_component_study.py", "w", encoding="utf-8") as f:
    f.write(fig7_7_code.strip() + "\n")
print("Created fig7_7_ablation_component_study.py")

# -----------------------------------------------------------------------------
# 8. Figure 7.8: Ablation Waterfall
# -----------------------------------------------------------------------------
with open("scripts/generate_publication_figures_extra.py", "r", encoding="utf-8") as f:
    text_extra = f.read()

start_m = 'print("[10/12] Generating fig_ablation_waterfall...")'
idx_start = text_extra.find(start_m)
idx_end = text_extra.find('save_all(fig, "fig_ablation_waterfall")', idx_start) + len('save_all(fig, "fig_ablation_waterfall")')
snippet = text_extra[idx_start:idx_end]
snippet = snippet.replace('save_all(fig, "fig_ablation_waterfall")', 'save_figure(fig, "fig_ablation_waterfall", pad_inches=0.12)\n    plt.close(fig)')
snippet_indented = "\n".join("    " + l for l in snippet.splitlines())

fig7_8_code = f'''"""
Figure 7.8: Stepwise Cumulative Ablation Waterfall Progression
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.5)
{snippet_indented}

if __name__ == "__main__":
    generate()
'''
with open(OUT_DIR / "fig7_8_ablation_waterfall.py", "w", encoding="utf-8") as f:
    f.write(fig7_8_code.strip() + "\n")
print("Created fig7_8_ablation_waterfall.py")

# -----------------------------------------------------------------------------
# 9. Figure 7.9: Leave-One-Out Impact
# -----------------------------------------------------------------------------
with open("scripts/redesign_fig7_9_leave_one_out.py", "r", encoding="utf-8") as f:
    text_7_9 = f.read()

idx = text_7_9.find("def build_figure():")
end_idx = text_7_9.find("def main():")
body = text_7_9[idx:end_idx]
body = body.replace("def build_figure():", "def generate():")

fig7_9_code = f'''"""
Figure 7.9: Leave-One-Out Component Ablation Impact Waterfall
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

{body}

if __name__ == "__main__":
    fig = generate()
    save_figure(fig, "fig_leave_one_out_impact", pad_inches=0.10)
    plt.close(fig)
'''
with open(OUT_DIR / "fig7_9_leave_one_out_impact.py", "w", encoding="utf-8") as f:
    f.write(fig7_9_code.strip() + "\n")
print("Created fig7_9_leave_one_out_impact.py")

# -----------------------------------------------------------------------------
# 10. Figure 7.10: Invariant Tornado Ranking
# -----------------------------------------------------------------------------
start_m = 'print("[4/12] Generating fig_invariant_importance_tornado...")'
idx_start = text_extra.find(start_m)
idx_end = text_extra.find('save_all(fig, "fig_invariant_importance_tornado")', idx_start) + len('save_all(fig, "fig_invariant_importance_tornado")')
snippet = text_extra[idx_start:idx_end]
snippet = snippet.replace('save_all(fig, "fig_invariant_importance_tornado")', 'save_figure(fig, "fig_invariant_importance_tornado", pad_inches=0.12)\n    plt.close(fig)')
snippet_indented = "\n".join("    " + l for l in snippet.splitlines())

fig7_10_code = f'''"""
Figure 7.10: Factorial Importance Tornado Ranking of 12-D Invariants
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.5)
{snippet_indented}

if __name__ == "__main__":
    generate()
'''
with open(OUT_DIR / "fig7_10_invariant_tornado.py", "w", encoding="utf-8") as f:
    f.write(fig7_10_code.strip() + "\n")
print("Created fig7_10_invariant_tornado.py")

# -----------------------------------------------------------------------------
# 11. Figure 7.11: Adversarial Camouflage Robustness
# -----------------------------------------------------------------------------
start_m = "# FIGURE 9: Camouflage Ratio Robustness (Double Column: 7.16\" x 2.70\")"
idx_start = text.find(start_m)
idx_end = text.find('save_all_formats(fig, "fig9_adversarial_camouflage_robustness")', idx_start) + len('save_all_formats(fig, "fig9_adversarial_camouflage_robustness")')
snippet = text[idx_start:idx_end]
snippet = snippet.replace('save_all_formats(fig, "fig9_adversarial_camouflage_robustness")', 'save_figure(fig, "fig9_adversarial_camouflage_robustness", pad_inches=0.12)\n    plt.close(fig)')
snippet_indented = "\n".join("    " + l for l in snippet.splitlines())

fig7_11_code = f'''"""
Figure 7.11: Adversarial Camouflage Link Robustness on Elliptic-v1
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

C_CSTGB = "#dc2626"
C_GCN   = "#475569"
C_XGB   = "#16a34a"
C_CARE  = "#d97706"
C_EAAI  = "#2563eb"

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.5)
{snippet_indented}

if __name__ == "__main__":
    generate()
'''
with open(OUT_DIR / "fig7_11_camouflage_robustness.py", "w", encoding="utf-8") as f:
    f.write(fig7_11_code.strip() + "\n")
print("Created fig7_11_camouflage_robustness.py")

# -----------------------------------------------------------------------------
# 12. Figure 7.12: Edge Gate Distribution
# -----------------------------------------------------------------------------
start_m = "# FIGURE 17: Edge-Trust Gating Attention Weight Distribution"
idx_start = text.find(start_m)
idx_end = text.find('save_all_formats(fig, "fig_edge_gate_distribution")', idx_start) + len('save_all_formats(fig, "fig_edge_gate_distribution")')
snippet = text[idx_start:idx_end]
snippet = snippet.replace('save_all_formats(fig, "fig_edge_gate_distribution")', 'save_figure(fig, "fig_edge_gate_distribution", pad_inches=0.12)\n    plt.close(fig)')
snippet_indented = "\n".join("    " + l for l in snippet.splitlines())

fig7_12_code = f'''"""
Figure 7.12: Empirical Distribution of Learnable Edge-Trust Gating Weights
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.5)
{snippet_indented}

if __name__ == "__main__":
    generate()
'''
with open(OUT_DIR / "fig7_12_edge_gate_distribution.py", "w", encoding="utf-8") as f:
    f.write(fig7_12_code.strip() + "\n")
print("Created fig7_12_edge_gate_distribution.py")

# -----------------------------------------------------------------------------
# 13. Figure 7.13: t-SNE Manifold Separation
# -----------------------------------------------------------------------------
start_m = "# FIGURE 2: t-SNE 2D Latent Manifold Separation (Double Column: 7.16\" x 2.80\")"
idx_start = text.find(start_m)
idx_end = text.find('save_all_formats(fig, "fig2_tsne_manifold_separation")', idx_start) + len('save_all_formats(fig, "fig2_tsne_manifold_separation")')
snippet = text[idx_start:idx_end]
snippet = snippet.replace('save_all_formats(fig, "fig2_tsne_manifold_separation")', 'save_figure(fig, "fig2_tsne_manifold_separation", pad_inches=0.12)\n    save_figure(fig, "tsne_manifold", pad_inches=0.12)\n    plt.close(fig)')
snippet_indented = "\n".join("    " + l for l in snippet.splitlines())

fig7_13_code = f'''"""
Figure 7.13: t-SNE Latent Manifold Visualization: Baseline vs. C-STGB
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.5)
{snippet_indented}

if __name__ == "__main__":
    generate()
'''
with open(OUT_DIR / "fig7_13_tsne_manifold.py", "w", encoding="utf-8") as f:
    f.write(fig7_13_code.strip() + "\n")
print("Created fig7_13_tsne_manifold.py")

# -----------------------------------------------------------------------------
# 14. Figure 7.14: Zero-Shot Transfer Heatmap
# -----------------------------------------------------------------------------
with open("scripts/generate_final_10_of_10_figures.py", "r", encoding="utf-8") as f:
    text_f10 = f.read()

start_m = 'print("13. GENERATING ZERO-SHOT CROSS-DOMAIN TRANSFER HEATMAP (Ch 7)")'
idx_start = text_f10.find(start_m)
idx_end = text_f10.find('save_fig(fig, ["fig_zero_shot_transfer_heatmap", "fig_transfer_matrix_heatmap"])', idx_start) + len('save_fig(fig, ["fig_zero_shot_transfer_heatmap", "fig_transfer_matrix_heatmap"])')
snippet = text_f10[idx_start:idx_end]
snippet = snippet.replace('save_fig(fig, ["fig_zero_shot_transfer_heatmap", "fig_transfer_matrix_heatmap"])', 'save_figure(fig, "fig_zero_shot_transfer_heatmap", pad_inches=0.12)\n    save_figure(fig, "fig_transfer_matrix_heatmap", pad_inches=0.12)\n    plt.close(fig)')
snippet_indented = "\n".join("    " + l for l in snippet.splitlines())

fig7_14_code = f'''"""
Figure 7.14: Zero-Shot Cross-Domain Generalization on Frozen Weights
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.5)
{snippet_indented}

if __name__ == "__main__":
    generate()
'''
with open(OUT_DIR / "fig7_14_zero_shot_heatmap.py", "w", encoding="utf-8") as f:
    f.write(fig7_14_code.strip() + "\n")
print("Created fig7_14_zero_shot_heatmap.py")

# -----------------------------------------------------------------------------
# 15. Figure 7.15: Streaming Latency Waterfall
# -----------------------------------------------------------------------------
with open("scripts/redesign_fig7_15_streaming_latency.py", "r", encoding="utf-8") as f:
    text_7_15 = f.read()

idx = text_7_15.find("def build_figure():")
end_idx = text_7_15.find("def main():")
body = text_7_15[idx:end_idx]
body = body.replace("def build_figure():", "def generate():")

fig7_15_code = f'''"""
Figure 7.15: Empirical Streaming Latency Distribution for Fast-Path Inference
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

{body}

if __name__ == "__main__":
    fig = generate()
    save_figure(fig, "fig_streaming_latency_waterfall", pad_inches=0.10)
    plt.close(fig)
'''
with open(OUT_DIR / "fig7_15_streaming_latency_waterfall.py", "w", encoding="utf-8") as f:
    f.write(fig7_15_code.strip() + "\n")
print("Created fig7_15_streaming_latency_waterfall.py")

# -----------------------------------------------------------------------------
# 16. Figure 7.16: Fast-Path Latency Comparison
# -----------------------------------------------------------------------------
start_m = 'print("[11/12] Generating fig_fastpath_latency_comparison...")'
idx_start = text_extra.find(start_m)
idx_end = text_extra.find('save_all(fig, "fig_fastpath_latency_comparison")', idx_start) + len('save_all(fig, "fig_fastpath_latency_comparison")')
snippet = text_extra[idx_start:idx_end]
snippet = snippet.replace('save_all(fig, "fig_fastpath_latency_comparison")', 'save_figure(fig, "fig_fastpath_latency_comparison", pad_inches=0.12)\n    plt.close(fig)')
snippet_indented = "\n".join("    " + l for l in snippet.splitlines())

fig7_16_code = f'''"""
Figure 7.16: Comparative Latency Profile: Fast-Path vs. SOTA Dynamic GNNs
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.5)
{snippet_indented}

if __name__ == "__main__":
    generate()
'''
with open(OUT_DIR / "fig7_16_fastpath_latency_comparison.py", "w", encoding="utf-8") as f:
    f.write(fig7_16_code.strip() + "\n")
print("Created fig7_16_fastpath_latency_comparison.py")

# -----------------------------------------------------------------------------
# 17. Figure 7.17: All Datasets PR Curves
# -----------------------------------------------------------------------------
start_m = "# FIGURE 16: All 14 Benchmark Precision-Recall Curves (Double Column: 7.16\" x 5.20\")"
idx_start = text.find(start_m)
idx_end = text.find('save_all_formats(fig, "fig_all_datasets_pr_curves")', idx_start) + len('save_all_formats(fig, "fig_all_datasets_pr_curves")')
snippet = text[idx_start:idx_end]
snippet = snippet.replace('save_all_formats(fig, "fig_all_datasets_pr_curves")', 'save_figure(fig, "fig_all_datasets_pr_curves", pad_inches=0.12)\n    plt.close(fig)')
snippet_indented = "\n".join("    " + l for l in snippet.splitlines())

fig7_17_code = f'''"""
Figure 7.17: Comprehensive 14-Dataset Precision-Recall Curves
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

C_CSTGB = "#dc2626"
C_GCN   = "#475569"
C_XGB   = "#16a34a"
C_CARE  = "#d97706"
C_EAAI  = "#2563eb"

def generate():
    setup_plt(font_size=8.0, title_size=8.8, label_size=8.0)
{snippet_indented}

if __name__ == "__main__":
    generate()
'''
with open(OUT_DIR / "fig7_17_all_datasets_pr_curves.py", "w", encoding="utf-8") as f:
    f.write(fig7_17_code.strip() + "\n")
print("Created fig7_17_all_datasets_pr_curves.py")

print("\n--- ALL 17 CHAPTER 7 FIGURE SCRIPTS BUILT SUCCESSFULLY ---")

