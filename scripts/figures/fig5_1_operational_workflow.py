"""
Figure 5.1: Fast-Path Latency Workflow and Selective Triage
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
            ["git", "show", "7e6fa35:papers/University_CSE_Thesis/figures/fig_operational_workflow.pdf"],
            stderr=subprocess.DEVNULL
        )
        doc = fitz.open(stream=clean_bytes, filetype="pdf")
    except Exception:
        src_path = Path("papers/University_CSE_Thesis/figures/fig_operational_workflow.pdf")
        doc = fitz.open(src_path)

    page = doc[0]

    # Exact background fills of enclosing cards:
    # 1. Top-right Neural Pod card: #E8F1FB -> (232/255, 241/255, 251/255)
    BG_BLUE = (232 / 255.0, 241 / 255.0, 251 / 255.0)
    # 2. Fast-path ego-graph card: #E8F1FB -> (232/255, 241/255, 251/255)
    # 3. Tier 2 review queue card: #FFF3D4 -> (255/255, 243/255, 212/255)
    BG_AMBER = (255 / 255.0, 243 / 255.0, 212 / 255.0)
    # 4. Tier 3 straight-through card: #E6F4EA -> (230/255, 244/255, 234/255)
    BG_GREEN = (230 / 255.0, 244 / 255.0, 234 / 255.0)

    # 1. BurstAware-HGT scoring -> C-STGB Neural Core
    rects_ba = page.search_for("BurstAware")
    rects_hgt = page.search_for("HGT scoring")
    if rects_ba or rects_hgt:
        r_top = rects_ba[0] if rects_ba else rects_hgt[0]
        r_bot = rects_hgt[0] if rects_hgt else rects_ba[0]
        r_redact = fitz.Rect(
            min(r_top.x0, r_bot.x0) - 2.0,
            r_top.y0 - 2.0,
            max(r_top.x1, r_bot.x1) + 6.0,
            r_bot.y1 + 2.0
        )
        page.add_redact_annot(r_redact, fill=BG_BLUE)
        page.apply_redactions()
        # Insert "C-STGB Neural" and "Core" with card's native dark-blue font color
        page.insert_text(
            (r_top.x0 - 2.0, r_top.y1 - 1.0),
            "C-STGB Neural",
            fontsize=7.3,
            fontname="helv",
            color=(0.114, 0.306, 0.537)
        )
        page.insert_text(
            (r_top.x0 + 10.0, r_bot.y1 - 0.5),
            "Core",
            fontsize=7.3,
            fontname="helv",
            color=(0.114, 0.306, 0.537)
        )

    # 1b. Fast-path LRU cache latency: update "cache hit · 0.45 ms" to "cache hit · 0.18 ms"
    rects_hit = page.search_for("cache hit · 0.45 ms")
    if rects_hit:
        r_hit = rects_hit[0]
        r_box = fitz.Rect(r_hit.x0 - 1.0, r_hit.y0 - 1.0, r_hit.x1 + 1.0, r_hit.y1 + 1.0)
        page.add_redact_annot(r_box, fill=BG_BLUE)
        page.apply_redactions()
        page.insert_text(
            (r_hit.x0, r_hit.y1 - 1.5),
            "cache hit · 0.18 ms",
            fontsize=6.5,
            fontname="helv",
            color=(0.357, 0.392, 0.447)
        )

    # 2. 50 of 10k tx (0.50%) -> 49 of 10k tx (0.49%)
    rects_50 = page.search_for("50 of 10k tx (0.50%)")
    if not rects_50:
        rects_50 = page.search_for("49 of 10k tx (0.49%)")
    if rects_50:
        r = rects_50[0]
        r_box = fitz.Rect(r.x0 - 1.0, r.y0 - 1.0, r.x1 + 1.0, r.y1 + 1.0)
        page.add_redact_annot(r_box, fill=BG_AMBER)
        page.apply_redactions()
        page.insert_text(
            (r.x0, r.y1 - 1.5),
            "49 of 10k tx (0.49%)",
            fontsize=6.5,
            fontname="helv",
            color=(0.357, 0.392, 0.447)
        )

    # 3. 9,932 of 10k tx (99.32%) -> 9,933 of 10k tx (99.33%)
    rects_9932 = page.search_for("9,932 of 10k tx (99.32%)")
    if not rects_9932:
        rects_9932 = page.search_for("9,933 of 10k tx (99.33%)")
    if rects_9932:
        r = rects_9932[0]
        r_box = fitz.Rect(r.x0 - 1.0, r.y0 - 1.0, r.x1 + 1.0, r.y1 + 1.0)
        page.add_redact_annot(r_box, fill=BG_GREEN)
        page.apply_redactions()
        page.insert_text(
            (r.x0, r.y1 - 1.5),
            "9,933 of 10k tx (99.33%)",
            fontsize=6.5,
            fontname="helv",
            color=(0.357, 0.392, 0.447)
        )

    pdf_bytes = doc.tobytes(garbage=3, deflate=True)
    pix = page.get_pixmap(dpi=300)
    doc.close()

    for d in TARGET_DIRS:
        if d.exists():
            out_pdf = d / "fig_operational_workflow.pdf"
            out_pdf.write_bytes(pdf_bytes)
            pix.save(d / "fig_operational_workflow.png")
            print(f"Patched & synced: {out_pdf}")

if __name__ == "__main__":
    generate()
