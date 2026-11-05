import fitz
import sys
from pathlib import Path
import shutil

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

pdf_path = Path("papers/University_CSE_Thesis/main.pdf")
doc = fitz.open(pdf_path)
print(f"Total pages in thesis monograph: {len(doc)}")

# Find Figure 1.2 and Figure 2.1 pages
fig1_pages = []
fig2_pages = []
double_question_pages = []

for idx, page in enumerate(doc):
    text = page.get_text()
    if "Figure 1.2" in text or "Operational Architecture" in text:
        fig1_pages.append(idx + 1)
    if "Figure 2.1" in text or "Adversarial Camouflage" in text or "Topological impact" in text:
        fig2_pages.append(idx + 1)
    if "??" in text:
        double_question_pages.append(idx + 1)

print(f"Figure 1.2 found on page(s): {fig1_pages}")
print(f"Figure 2.1 found on page(s): {fig2_pages}")
print(f"Pages with '??' (broken refs): {double_question_pages}")

# Render the pages
artifact_dir = Path(r"C:\Users\SAAD\.gemini\antigravity\brain\26c4505d-0616-4920-a3c3-01117c9a7ce5")

if fig1_pages:
    p1 = fig1_pages[0]
    pix = doc[p1 - 1].get_pixmap(dpi=150)
    out_p1 = artifact_dir / f"thesis_page_{p1}_fig1_2.png"
    pix.save(str(out_p1))
    print(f"Saved rendered page {p1} to {out_p1.name}")

if fig2_pages:
    p2 = fig2_pages[0]
    pix = doc[p2 - 1].get_pixmap(dpi=150)
    out_p2 = artifact_dir / f"thesis_page_{p2}_fig2_1.png"
    pix.save(str(out_p2))
    print(f"Saved rendered page {p2} to {out_p2.name}")

# Also copy the standalone figure PNGs to artifact_dir for high-res direct viewing
shutil.copy(
    "papers/University_CSE_Thesis/figures/fig1_operational_architecture_flowchart.png",
    artifact_dir / "fig1_operational_architecture_flowchart.png"
)
shutil.copy(
    "papers/University_CSE_Thesis/figures/fig21_adversarial_camouflage_topology.png",
    artifact_dir / "fig21_adversarial_camouflage_topology.png"
)
print("Copied high-res figure PNGs to artifact directory.")

