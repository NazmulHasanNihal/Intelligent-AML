"""
generate_thesis_distinct_figures.py — Generates distinct research-grade diagrams for:
- Fig 3.1: C-STGB Tensor Flow and Computational Data-Path (fig3_1_tensor_flow)
- Fig 4.1: DuckDB / PyArrow Zero-Copy Streaming Ingestion Pipeline (fig4_1_duckdb_arrow_pipeline)
- Fig 8.1: Enterprise FastAPI & Kubernetes Production Topology (fig8_1_fastapi_k8s_topology)
"""

import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 8.5,
    'axes.labelsize': 9.0,
    'axes.titlesize': 9.5,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
})

BASE_DIR = Path(__file__).resolve().parent.parent
thesis_fig_dir = BASE_DIR / "papers" / "University_CSE_Thesis" / "figures"
eaai_fig_dir = BASE_DIR / "papers" / "EAAI_Research_Paper" / "figures"
data_fig_dir = BASE_DIR / "data" / "outputs" / "figures"
TARGET_DIRS = [thesis_fig_dir, eaai_fig_dir, data_fig_dir, BASE_DIR / "papers" / "EAAI_Submission" / "figures", BASE_DIR / "reports" / "figures"]

for d in TARGET_DIRS:
    d.mkdir(parents=True, exist_ok=True)


def save_fig(fig, stem):
    for d in TARGET_DIRS:
        fig.savefig(d / f"{stem}.pdf", bbox_inches="tight", pad_inches=0.15)
        fig.savefig(d / f"{stem}.png", dpi=300, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f" [OK] Generated: {stem}.pdf & .png")


# ==============================================================================
# ==============================================================================
# 1. FIG 3.1: MASTER PIPELINE FLOWCHART
# ==============================================================================
# Maintained by render_publication_diagrams.py
print("Fig 3.1: Maintained by render_publication_diagrams.py")



# ==============================================================================
# 2. FIG 4.1: DUCKDB / ARROW STREAMING DATA PIPELINE
# ==============================================================================
print("Generating Fig 4.1: DuckDB / Arrow Streaming Ingestion Pipeline...")
from redesign_fig4_1_data_pipeline import generate_figure_4_1
fig = generate_figure_4_1()
save_fig(fig, "fig4_1_duckdb_arrow_pipeline")

# ==============================================================================
# 3. FIG 8.3: CLOUD-NATIVE KUBERNETES DEPLOYMENT TOPOLOGY (9.2" x 4.40")
# ==============================================================================
print("Generating Fig 8.3: Enterprise Cloud-Native Kubernetes Deployment Topology...")
from redesign_fig8_3_cloud_native_k8s import generate_figure_8_3
fig = generate_figure_8_3()
save_fig(fig, "fig8_1_fastapi_k8s_topology")

print("All distinct architecture figures successfully generated!")
