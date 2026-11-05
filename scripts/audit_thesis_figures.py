import fitz
import glob
import re
from pathlib import Path

tex_files = glob.glob('papers/University_CSE_Thesis/**/*.tex', recursive=True)
figures_used = set()
for tf in tex_files:
    with open(tf, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
        matches = re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', text)
        for m in matches:
            figures_used.add(Path(m).name)

out_lines = [f"Total figures included in thesis: {len(figures_used)}"]

issues_by_fig = {}
for fname in sorted(figures_used):
    if not fname.endswith('.pdf'):
        continue
    fpath = Path('papers/University_CSE_Thesis/figures') / fname
    if not fpath.exists():
        continue
    doc = fitz.open(fpath)
    page = doc[0]
    rect = page.rect
    fig_issues = []
    
    blocks = page.get_text('blocks')
    for b in blocks:
        if b[4].strip():
            # Check edge margin (< 3.0 pt)
            if b[0] < 3.0:
                fig_issues.append(f"LEFT_CLIP ({b[0]:.1f}pt): {repr(b[4].strip()[:35])}")
            if b[1] < 3.0:
                fig_issues.append(f"TOP_CLIP ({b[1]:.1f}pt): {repr(b[4].strip()[:35])}")
            if b[2] > rect.width - 3.0:
                fig_issues.append(f"RIGHT_CLIP ({rect.width - b[2]:.1f}pt): {repr(b[4].strip()[:35])}")
            if b[3] > rect.height - 3.0:
                fig_issues.append(f"BOTTOM_CLIP ({rect.height - b[3]:.1f}pt): {repr(b[4].strip()[:35])}")
                
    words = page.get_text('words')
    for i in range(len(words)):
        w1 = words[i]
        r1 = fitz.Rect(w1[:4])
        for j in range(i+1, min(i+40, len(words))):
            w2 = words[j]
            r2 = fitz.Rect(w2[:4])
            if r1.intersects(r2):
                intersect = r1.intersect(r2)
                area1 = r1.width * r1.height
                area2 = r2.width * r2.height
                iarea = intersect.width * intersect.height
                if min(area1, area2) > 0 and (iarea / min(area1, area2)) > 0.40:
                    t1 = repr(w1[4])
                    t2 = repr(w2[4])
                    fig_issues.append(f"COLLISION: {t1} & {t2}")
                    
    if fig_issues:
        issues_by_fig[fname] = fig_issues

out_lines.append(f"Thesis figures with issues: {len(issues_by_fig)}")
for fname, f_issues in issues_by_fig.items():
    out_lines.append(f"\n=== {fname} ({len(f_issues)} issues) ===")
    for iss in f_issues[:20]:
        out_lines.append(f"   {iss}")

with open("thesis_figure_audit_results.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))

print(f"Audit written to thesis_figure_audit_results.txt with {len(issues_by_fig)} figures noted.")
