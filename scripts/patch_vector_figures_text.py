import fitz
from pathlib import Path
import shutil

TARGET_DIRS = [
    Path("papers/University_CSE_Thesis/figures"),
    Path("papers/EAAI_Research_Paper/figures"),
    Path("papers/EAAI_Submission/figures"),
    Path("data/outputs/figures"),
    Path("reports/figures"),
]

def patch_operational_workflow():
    src_path = Path("papers/University_CSE_Thesis/figures/fig_operational_workflow.pdf")
    doc = fitz.open(src_path)
    page = doc[0]

    # 1. BurstAware-HGT scoring -> C-STGB Neural Scoring
    rects_ba = page.search_for("BurstAware-")
    rects_hgt = page.search_for("HGT scoring")
    if rects_ba and rects_hgt:
        r = rects_ba[0] | rects_hgt[0]
        page.add_redact_annot(r, fill=(1, 1, 1))
        page.apply_redactions()
        page.insert_text((r.x0, r.y0 + 7.5), "C-STGB Neural", fontsize=7.2, fontname="helv", color=(0.1, 0.1, 0.1))
        page.insert_text((r.x0, r.y0 + 15.5), "Scoring", fontsize=7.2, fontname="helv", color=(0.1, 0.1, 0.1))

    # 2. 50 of 10k tx (0.50%) -> 49 of 10k tx (0.49%)
    rects_50 = page.search_for("50 of 10k tx (0.50%)")
    if rects_50:
        r = rects_50[0]
        page.add_redact_annot(r, fill=(1, 1, 1))
        page.apply_redactions()
        page.insert_text((r.x0, r.y1 - 1.5), "49 of 10k tx (0.49%)", fontsize=6.8, fontname="helv", color=(0.2, 0.2, 0.2))

    # 3. 9,932 of 10k tx (99.32%) -> 9,933 of 10k tx (99.33%)
    rects_9932 = page.search_for("9,932 of 10k tx (99.32%)")
    if rects_9932:
        r = rects_9932[0]
        page.add_redact_annot(r, fill=(1, 1, 1))
        page.apply_redactions()
        page.insert_text((r.x0, r.y1 - 1.5), "9,933 of 10k tx (99.33%)", fontsize=6.8, fontname="helv", color=(0.2, 0.2, 0.2))

    pdf_bytes = doc.tobytes(garbage=3, deflate=True)
    pix = page.get_pixmap(dpi=300)
    doc.close()

    for d in TARGET_DIRS:
        if d.exists():
            out_pdf = d / "fig_operational_workflow.pdf"
            out_pdf.write_bytes(pdf_bytes)
            pix.save(d / "fig_operational_workflow.png")
            print(f"Patched & synced: {out_pdf}")

def patch_system_architecture():
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
    patch_operational_workflow()
    patch_system_architecture()
    print("Vector figures patched successfully!")
