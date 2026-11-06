import os
import glob
import fitz  # PyMuPDF

ARTIFACT_DIR = r"C:\Users\SAAD\.gemini\antigravity\brain\26c4505d-0616-4920-a3c3-01117c9a7ce5"
OUT_DIR = os.path.join(ARTIFACT_DIR, "visual_inspection")
os.makedirs(OUT_DIR, exist_ok=True)

FIG_DIR = r"c:\Users\SAAD\Documents\GitHub\Intelligent-AML\papers\University_CSE_Thesis\figures"

flagged_figures = [
    "fig18_graphsmote_synthesis_pipeline.pdf",
    "fig19_conformal_risk_mechanism.pdf",
    "fig1_operational_architecture_flowchart.pdf",
    "fig1_pr_roc_curves.pdf",
    "fig22_triband_spectral_coldstart.pdf",
    "fig3_1_tensor_flow.pdf",
    "fig3_ablation_component_study.pdf",
    "fig4_2_database_erd.pdf",
    "fig8_1_fastapi_k8s_topology.pdf",
    "fig8_2_uml_sequence_lifeline.pdf",
    "fig_12d_toy_model_schematic.pdf",
    "fig_lit_evolution_frontier.pdf",
    "fig_operational_workflow.pdf",
    "fig_regulatory_shields.pdf",
    "fig_single_alert_timeline.pdf",
    "fig_streaming_latency_waterfall.pdf",
    "fig_system_architecture.pdf",
    "fig_temporal_split.pdf",
    "fig_triband_decay_comparison.pdf",
    "fig_zero_shot_transfer_heatmap.pdf"
]

print(f"Rendering {len(flagged_figures)} flagged figures to PNG...")
for fig_name in flagged_figures:
    pdf_path = os.path.join(FIG_DIR, fig_name)
    if not os.path.exists(pdf_path):
        print(f"MISSING: {pdf_path}")
        continue
    try:
        doc = fitz.open(pdf_path)
        page = doc[0]
        # Render at 2.0 zoom (approx 144 DPI) for crisp viewing
        pix = page.get_pixmap(dpi=150)
        out_png = os.path.join(OUT_DIR, fig_name.replace(".pdf", ".png"))
        pix.save(out_png)
        print(f"Rendered: {fig_name} -> {out_png} (size: {pix.width}x{pix.height})")
    except Exception as e:
        print(f"Error rendering {fig_name}: {e}")

print("Done rendering.")

