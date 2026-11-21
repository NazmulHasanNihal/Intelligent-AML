"""
Figure 8.1: System Architecture of Intelligent-AML Production Serving
Standalone publication script for C-STGB monograph.
Fixes white background boxes behind diagram text by matching exact card fills.
"""
import sys
import subprocess
import fitz
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import TARGET_DIRS

def generate():
    # Load clean base PDF from git commit 7e6fa35 to avoid stacked redaction artifacts
    try:
        clean_bytes = subprocess.check_output(
            ["git", "show", "7e6fa35:papers/University_CSE_Thesis/figures/fig_system_architecture.pdf"],
            stderr=subprocess.DEVNULL
        )
        doc = fitz.open(stream=clean_bytes, filetype="pdf")
    except Exception:
        src_path = Path("papers/University_CSE_Thesis/figures/fig_system_architecture.pdf")
        doc = fitz.open(src_path)

    page = doc[0]

    # Exact background fills of enclosing cards:
    # 1. Neural Engine card: #F0E9FA -> (240/255, 233/255, 250/255)
    BG_PURPLE = (240 / 255.0, 233 / 255.0, 250 / 255.0)
    # 2. Tier 2 review card: #FFF3D4 -> (255/255, 243/255, 212/255)
    BG_AMBER = (255 / 255.0, 243 / 255.0, 212 / 255.0)
    # 3. Tier 3 straight-through card: #E6F4EA -> (230/255, 244/255, 234/255)
    BG_GREEN = (230 / 255.0, 244 / 255.0, 234 / 255.0)

    # 1. Cover the legacy white rectangle under "C-STGB Spatio-Temporal Convolutions" with exact card fill (BG_PURPLE)
    # The legacy white rectangle was at Rect(232.92, 221.22, 317.87, 228.48)
    r_conv = fitz.Rect(220.0, 219.0, 340.0, 230.5)
    page.add_redact_annot(r_conv, fill=BG_PURPLE)
    page.apply_redactions()
    page.insert_text(
        (224.9, 226.5),
        "C-STGB Spatio-Temporal Convolutions",
        fontsize=6.2,
        fontname="helv",
        color=(0.2, 0.2, 0.2)
    )

    # 2. Update Tier 2 (0.50%) to 0.49% to match Chapter 5 triage distribution
    rects_50 = page.search_for("0.50% · analyst + swarm")
    if not rects_50:
        rects_50 = page.search_for("0.49% · analyst + swarm")
    if rects_50:
        r = rects_50[0]
        r_box = fitz.Rect(r.x0 - 1.0, r.y0 - 1.0, r.x1 + 1.0, r.y1 + 1.0)
        page.add_redact_annot(r_box, fill=BG_AMBER)
        page.apply_redactions()
        page.insert_text(
            (r.x0, r.y1 - 1.5),
            "0.49% · analyst + swarm",
            fontsize=6.5,
            fontname="helv",
            color=(0.357, 0.392, 0.447)
        )

    # 3. Update Tier 3 (99.32%) to 99.33% to match Chapter 5 triage distribution
    rects_9932 = page.search_for("99.32% · auto-clear")
    if not rects_9932:
        rects_9932 = page.search_for("99.33% · auto-clear")
    if rects_9932:
        r = rects_9932[0]
        r_box = fitz.Rect(r.x0 - 1.0, r.y0 - 1.0, r.x1 + 1.0, r.y1 + 1.0)
        page.add_redact_annot(r_box, fill=BG_GREEN)
        page.apply_redactions()
        page.insert_text(
            (r.x0, r.y1 - 1.5),
            "99.33% · auto-clear",
            fontsize=6.5,
            fontname="helv",
            color=(0.357, 0.392, 0.447)
        )

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
