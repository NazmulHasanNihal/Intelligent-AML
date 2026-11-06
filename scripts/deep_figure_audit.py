import os
import fitz
import re

FIG_DIR = r"c:\Users\SAAD\Documents\GitHub\Intelligent-AML\papers\University_CSE_Thesis\figures"

tex_files = [
    r"papers\University_CSE_Thesis\main.tex",
    r"papers\University_CSE_Thesis\chapters\ch1_introduction.tex",
    r"papers\University_CSE_Thesis\chapters\ch2_literature_review.tex",
    r"papers\University_CSE_Thesis\chapters\ch3_system_architecture.tex",
    r"papers\University_CSE_Thesis\chapters\ch4_data_pipeline.tex",
    r"papers\University_CSE_Thesis\chapters\ch5_conformal_ethics.tex",
    r"papers\University_CSE_Thesis\chapters\ch6_xai_agentic_sar.tex",
    r"papers\University_CSE_Thesis\chapters\ch7_experiments.tex",
    r"papers\University_CSE_Thesis\chapters\ch8_software_engineering.tex",
    r"papers\University_CSE_Thesis\chapters\ch9_conclusion.tex",
    r"papers\University_CSE_Thesis\chapters\ch10_appendices.tex",
]

thesis_figures = []
for tf in tex_files:
    if not os.path.exists(tf):
        continue
    for line in open(tf, encoding="utf-8", errors="ignore"):
        m = re.findall(r"\\includegraphics(?:\[.*?\])?\{figures/([^}]+)\}", line)
        for fig in m:
            thesis_figures.append(fig)

unique_figs = sorted(set(thesis_figures))
print(f"Total unique figures in thesis: {len(unique_figs)}")

pdf_figs = [f for f in unique_figs if f.endswith(".pdf")]
print(f"Total PDF vector figures in thesis: {len(pdf_figs)}")

for fig_name in pdf_figs:
    pdf_path = os.path.join(FIG_DIR, fig_name)
    if not os.path.exists(pdf_path):
        print(f"MISSING: {fig_name}")
        continue
    doc = fitz.open(pdf_path)
    page = doc[0]
    rect = page.rect
    
    # Get all text words with bounding boxes
    words = page.get_text("words") # (x0, y0, x1, y1, word, block_no, line_no, word_no)
    
    # Check boundary clipping
    clipped_words = []
    for w in words:
        if w[0] < 2.0 or w[1] < 2.0 or w[2] > rect.width - 2.0 or w[3] > rect.height - 2.0:
            clipped_words.append(w[4])
            
    # Check horizontal overlap between words on the same vertical band
    overlaps = []
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            w1 = words[i]
            w2 = words[j]
            # If same block and line, PyMuPDF words don't overlap unless spacing is negative
            if w1[5] == w2[5] and w1[6] == w2[6]:
                continue
            r1 = fitz.Rect(w1[:4])
            r2 = fitz.Rect(w2[:4])
            intersect = r1.intersect(r2)
            if not intersect.is_empty and intersect.width > 2.0 and intersect.height > 2.0:
                overlaps.append((w1[4], w2[4], intersect.width, intersect.height))
                
    if clipped_words or overlaps:
        print(f"\n[!] {fig_name} (Page size: {rect.width:.1f} x {rect.height:.1f})")
        if clipped_words:
            print(f"    Clipped near borders: {clipped_words[:8]}")
        if overlaps:
            print(f"    Text bounding box overlaps ({len(overlaps)}):")
            for o in overlaps[:8]:
                print(f"      '{o[0]}' with '{o[1]}' (overlap: {o[2]:.1f}x{o[3]:.1f} pt)")
    else:
        print(f"OK: {fig_name}")

