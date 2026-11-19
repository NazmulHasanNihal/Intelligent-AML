"""
Figure 8.1: System Architecture of Intelligent-AML Production Serving
Standalone publication script for C-STGB monograph.
"""
import sys
import fitz
from pathlib import Path
import shutil

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import TARGET_DIRS

def generate():
    src_path = Path("papers/University_CSE_Thesis/figures/fig_system_architecture.pdf")
    doc = fitz.open(src_path)
    page = doc[0]

    rects_ba = page.search_for("BurstAwareHGT convolutions")
    if rects_ba:
        r = rects_ba[0]
        page.add_redact_annot(r, fill=(1, 1, 1))
        page.apply_redactions()
        page.insert_text((r.x0 - 8.0, r.y1 - 1.5), "C-STGB Spatio-Temporal Convolutions", fontsize=6.2, fontname="helv", color=(0.2, 0.2, 0.2))

    # Update Tier 2 (0.50%) and Tier 3 (99.32%) to 0.49% and 99.33% to match Chapter 5
    rects_50 = page.search_for("0.50% · analyst + swarm")
    if rects_50:
        r = rects_50[0]
        page.add_redact_annot(r, fill=(1, 1, 1))
        page.apply_redactions()
        page.insert_text((r.x0, r.y1 - 1.5), "0.49% · analyst + swarm", fontsize=6.5, fontname="helv", color=(0.357, 0.392, 0.447))

    rects_9932 = page.search_for("99.32% · auto-clear")
    if rects_9932:
        r = rects_9932[0]
        page.add_redact_annot(r, fill=(1, 1, 1))
        page.apply_redactions()
        page.insert_text((r.x0, r.y1 - 1.5), "99.33% · auto-clear", fontsize=6.5, fontname="helv", color=(0.357, 0.392, 0.447))

    pdf_bytes = doc.tobytes(garbage=3, deflate=True)
    pix = page.get_pixmap(dpi=300)
    doc.close()

    for d in TARGET_DIRS:
        if d.exists():
            out_pdf = d / "fig_system_architecture.pdf"
            out_pdf.write_bytes(pdf_bytes)
            pix.save(d / "fig_system_architecture.png")
            print(f"Patched & synced: {out_pdf}")

if __name__ == "__main__":
    generate()
