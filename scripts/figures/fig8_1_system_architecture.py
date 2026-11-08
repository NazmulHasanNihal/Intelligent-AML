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
